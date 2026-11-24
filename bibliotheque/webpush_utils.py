"""
SDM Mouride — Moteur Web Push VAPID (Notifications réelles dans la barre OS même application fermée).
- Auto-génère et persiste les clés VAPID dans WebPushConfig (ou lit VAPID_PUBLIC_KEY / VAPID_PRIVATE_KEY).
- Envoie des notifications Web Push chiffrées RFC 8291 via pywebpush.
- Planificateur léger en arrière-plan vérifiant Prières, Wird Mahuz (06h30/17h00), Verset, Citation, Étude & Nouveaux Sons/Khassidas.
"""
import base64
import datetime as dt
import json
import os
import sys
import threading
import time

from django.conf import settings
from django.core.cache import cache
from django.db import close_old_connections

_WORKER_STARTED = False
_WORKER_LOCK = threading.Lock()


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def get_or_create_vapid_keys():
    """Retourne (public_key_b64url, private_key_pem) persistants."""
    env_pub = (os.environ.get('VAPID_PUBLIC_KEY') or '').strip()
    env_priv = (os.environ.get('VAPID_PRIVATE_KEY') or '').strip()
    if env_pub and env_priv:
        return env_pub, env_priv.replace('\\n', '\n')

    cached = cache.get('sdm_vapid_keys_v1')
    if cached and len(cached) == 2:
        return cached

    from bibliotheque.models import WebPushConfig
    cfg = WebPushConfig.objects.order_by('id').first()
    if cfg and cfg.public_key and cfg.private_key_pem:
        pair = (cfg.public_key.strip(), cfg.private_key_pem.strip())
        cache.set('sdm_vapid_keys_v1', pair, 3600)
        return pair

    # Générer une nouvelle paire ECDSA P-256 standard Web Push
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec

    private_key = ec.generate_private_key(ec.SECP256R1())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode('utf-8')

    public_raw = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    public_b64 = _b64url_encode(public_raw)

    cfg = WebPushConfig.objects.create(public_key=public_b64, private_key_pem=private_pem)
    pair = (cfg.public_key, cfg.private_key_pem)
    cache.set('sdm_vapid_keys_v1', pair, 3600)
    return pair


def send_webpush(sub, title, body, url='/', tag=None, silent=False, kind='general', sound_url=''):
    """Envoie une notification Web Push réelle à un abonnement WebPushSubscription."""
    try:
        from pywebpush import webpush, WebPushException
    except Exception as e:
        return False, f"pywebpush-missing: {e}"

    try:
        _, priv_pem = get_or_create_vapid_keys()
        payload = json.dumps({
            'title': str(title or 'SDM Mouride'),
            'body': str(body or ''),
            'url': url or '/',
            'tag': tag or f"sdm-push-{int(time.time())}",
            'silent': bool(silent),
            'kind': kind or 'general',
            'soundUrl': sound_url or '',
            'ts': int(time.time() * 1000),
        }, ensure_ascii=False)

        webpush(
            subscription_info={
                'endpoint': sub.endpoint,
                'keys': {
                    'p256dh': sub.p256dh,
                    'auth': sub.auth,
                },
            },
            data=payload,
            vapid_private_key=priv_pem,
            vapid_claims={'sub': 'mailto:contact@sdm-mouride.com'},
            ttl=3600,
        )
        return True, 'sent'
    except Exception as exc:
        resp = getattr(exc, 'response', None)
        status_code = getattr(resp, 'status_code', None)
        if status_code in (404, 410):
            try:
                sub.is_active = False
                sub.save(update_fields=['is_active', 'updated_at'])
            except Exception:
                pass
            return False, f"expired-{status_code}"
        return False, str(exc)[:180]


def _to_min(hhmm):
    try:
        parts = str(hhmm or '').strip()[:5].split(':')
        if len(parts) != 2:
            return -1
        return int(parts[0]) * 60 + int(parts[1])
    except Exception:
        return -1


def _load_daily_content():
    """Récupère Verset du Jour, Citation, derniers Son/Khassida et prières par défaut (mis en cache 2 min)."""
    cached = cache.get('sdm_push_daily_ctx_v1')
    if cached:
        return cached

    from bibliotheque.models import Khassida, Son, Wird, ContenuDuJour, ParametresPriere

    latest_son = Son.objects.only('id', 'titre', 'auteur_voix').order_by('-id').first()
    latest_kh = Khassida.objects.only('id', 'titre').order_by('-id').first()
    wird_obj = Wird.objects.filter(titre__icontains='Mahuz').first() or Wird.objects.first()
    wird_url = f"/wird/{wird_obj.slug}/" if (wird_obj and wird_obj.slug) else "/wird/mahuz-al-khafif/"

    citation = {
        'id': 'mj_v1089',
        'texte': "La meilleure parure dont l'homme puisse se parer est la bonne conduite (al-adab) partout où il passe.",
        'source': "Masaalik-ul Jinaan · Cheikh Ahmadou Bamba (RTA)",
    }
    rappels_path = os.path.join(settings.BASE_DIR, 'daily_rappels_sdm.json')
    if os.path.isfile(rappels_path):
        try:
            with open(rappels_path, 'r', encoding='utf-8') as rf:
                cits = json.load(rf)
            if cits:
                c = cits[dt.date.today().toordinal() % len(cits)]
                citation = {
                    'id': c.get('id') or 'mj_v1089',
                    'texte': (c.get('texte') or '')[:200],
                    'source': f"{c.get('oeuvre') or 'Masaalik-ul Jinaan'} · {c.get('auteur') or 'Cheikh Ahmadou Bamba (RTA)'}",
                }
        except Exception:
            pass

    verset = {
        'fr': "N'est-ce point par l'évocation d'Allah que se tranquillisent les cœurs ?",
        'ref': "Sourate Ar-Ra'd (13:28)",
    }
    cnt_qs = ContenuDuJour.objects.order_by('id')
    if cnt_qs.exists():
        raw_c = cnt_qs[dt.date.today().timetuple().tm_yday % cnt_qs.count()]
        parts = (raw_c.verset_du_jour or '').split('\n— ')
        ref = parts[1] if len(parts) > 1 else 'Saint Coran'
        subs = parts[0].split('\n\n')
        verset = {
            'fr': (subs[1] if len(subs) > 1 else subs[0])[:220],
            'ref': ref,
        }

    prayers = [
        {'name': 'Fajr (Subh)', 'time': '05:45'},
        {'name': 'Tisbar (Dhuhr)', 'time': '13:15'},
        {'name': 'Takussan (Asr)', 'time': '16:35'},
        {'name': 'Timiss (Maghrib)', 'time': '18:55'},
        {'name': 'Guéwé (Isha)', 'time': '20:05'},
    ]
    cfg = ParametresPriere.objects.first()
    if cfg:
        def _f(v, fb):
            try:
                return v.strftime('%H:%M') if v else fb
            except Exception:
                return str(v)[:5] if v else fb
        prayers = [
            {'name': 'Fajr (Subh)', 'time': _f(getattr(cfg, 'fajr', None), '05:45')},
            {'name': 'Tisbar (Dhuhr)', 'time': _f(getattr(cfg, 'tisbar', None), '13:15')},
            {'name': 'Takussan (Asr)', 'time': _f(getattr(cfg, 'takussan', None), '16:35')},
            {'name': 'Timiss (Maghrib)', 'time': _f(getattr(cfg, 'timiss', None), '18:55')},
            {'name': 'Guéwé (Isha)', 'time': _f(getattr(cfg, 'guewe', None), '20:05')},
        ]

    ctx = {
        'latest_son': {'id': latest_son.id, 'titre': latest_son.titre, 'auteur': latest_son.auteur_voix or 'Kourel Mouride'} if latest_son else None,
        'latest_kh': {'id': latest_kh.id, 'titre': latest_kh.titre} if latest_kh else None,
        'wird_url': wird_url,
        'citation': citation,
        'verset': verset,
        'prayers': prayers,
    }
    cache.set('sdm_push_daily_ctx_v1', ctx, 120)
    return ctx


def process_due_webpushes():
    """Parcourt les abonnements Web Push actifs et envoie les alertes arrivées à échéance."""
    from bibliotheque.models import WebPushSubscription

    subs = list(WebPushSubscription.objects.filter(is_active=True)[:300])
    if not subs:
        return {'checked': 0, 'sent': 0}

    ctx = _load_daily_content()
    utc_now = dt.datetime.now(dt.timezone.utc)
    sent_count = 0

    for sub in subs:
        prefs = sub.prefs_json or {}
        if prefs.get('enabled') is False:
            continue

        # Heure locale de l'utilisateur via tz_offset_min (JS getTimezoneOffset(): UTC - local en minutes)
        offset_min = int(sub.tz_offset_min or 0)
        local_dt = utc_now - dt.timedelta(minutes=offset_min)
        today = local_dt.strftime('%Y-%m-%d')
        now_min = local_dt.hour * 60 + local_dt.minute

        fired = dict(sub.fired_json or {})
        dirty = False
        rem_silent = (prefs.get('soundMode') == 'silent')
        pray_silent = (prefs.get('prayerSoundMode', prefs.get('soundMode')) == 'silent')
        rem_sound = prefs.get('reminderSoundUrl', '')
        pray_sound = prefs.get('prayerSoundUrl', '')

        # 1. Nouveau Son
        if prefs.get('sonEnabled', True) and ctx['latest_son']:
            sid = int(ctx['latest_son']['id'])
            if sub.last_seen_son_id == 0:
                sub.last_seen_son_id = sid
                dirty = True
            elif sid > sub.last_seen_son_id:
                ok, _ = send_webpush(
                    sub,
                    f"🎧 Nouveau Son : {ctx['latest_son']['titre']}",
                    f"{ctx['latest_son']['auteur']} vient d'être ajouté sur SDM Mouride.",
                    url=f"/collection/son/?autoplay={sid}",
                    tag=f"sdm-son-{sid}",
                    silent=rem_silent,
                    kind='son',
                    sound_url=rem_sound,
                )
                sub.last_seen_son_id = sid
                dirty = True
                if ok:
                    sent_count += 1

        # 2. Nouveau Khassida PDF
        if prefs.get('khassidaEnabled', True) and ctx['latest_kh']:
            kid = int(ctx['latest_kh']['id'])
            if sub.last_seen_khassida_id == 0:
                sub.last_seen_khassida_id = kid
                dirty = True
            elif kid > sub.last_seen_khassida_id:
                ok, _ = send_webpush(
                    sub,
                    f"📚 Nouveau Khassida : {ctx['latest_kh']['titre']}",
                    "Touchez pour lire ce nouveau Khassida sur SDM Mouride.",
                    url=f"/lire/khassida/{kid}/",
                    tag=f"sdm-kh-{kid}",
                    silent=rem_silent,
                    kind='khassida',
                    sound_url=rem_sound,
                )
                sub.last_seen_khassida_id = kid
                dirty = True
                if ok:
                    sent_count += 1

        # 3. Heures de Prière
        if prefs.get('prayerEnabled', True):
            prayers = sub.prayers_json if (isinstance(sub.prayers_json, list) and len(sub.prayers_json) >= 5) else ctx['prayers']
            lead = int(prefs.get('prayerLeadMin', 5) or 0)
            for p in prayers:
                pm = _to_min(p.get('time'))
                key = f"prayer_{today}_{p.get('name')}"
                if pm >= 0 and not fired.get(key) and (pm - lead) <= now_min <= (pm + 15):
                    fired[key] = int(time.time())
                    dirty = True
                    msg = f"La prière de {p.get('name')} est prévue à {p.get('time')}. Préparez vos ablutions." if lead > 0 else f"Il est l'heure de la prière de {p.get('name')} ({p.get('time')})."
                    ok, _ = send_webpush(
                        sub,
                        f"🕌 Heure de la Prière : {p.get('name')}",
                        msg,
                        url='/',
                        tag=key,
                        silent=pray_silent,
                        kind='prayer',
                        sound_url=pray_sound,
                    )
                    if ok:
                        sent_count += 1
                    break

        # 4. Wird Mahuz (Matin & Soir)
        if prefs.get('wirdEnabled', True):
            wm = _to_min(prefs.get('wirdMorningTime', '06:30'))
            we = _to_min(prefs.get('wirdEveningTime', '17:00'))
            k_m = f"wird_m_{today}"
            if wm >= 0 and not fired.get(k_m) and wm <= now_min <= (wm + 20):
                fired[k_m] = int(time.time())
                dirty = True
                ok, _ = send_webpush(
                    sub,
                    "📿 Rappel Wird Mahuz du Matin (après Suba)",
                    "Touchez pour ouvrir le compteur sacré et accomplir votre Wird Mahuz.",
                    url=ctx['wird_url'],
                    tag=k_m,
                    silent=rem_silent,
                    kind='wird',
                    sound_url=rem_sound,
                )
                if ok:
                    sent_count += 1
            k_e = f"wird_e_{today}"
            if we >= 0 and not fired.get(k_e) and we <= now_min <= (we + 20):
                fired[k_e] = int(time.time())
                dirty = True
                ok, _ = send_webpush(
                    sub,
                    "📿 Rappel Wird Mahuz du Soir (après Takussan)",
                    "N'oubliez pas votre Wird Mahuz du soir. Touchez pour ouvrir le compteur !",
                    url=ctx['wird_url'],
                    tag=k_e,
                    silent=rem_silent,
                    kind='wird',
                    sound_url=rem_sound,
                )
                if ok:
                    sent_count += 1

        # 5. Verset du Jour
        if prefs.get('verseEnabled', True):
            vm = _to_min(prefs.get('verseTime', '07:30'))
            kv = f"verse_{today}"
            if vm >= 0 and not fired.get(kv) and vm <= now_min <= (vm + 20):
                fired[kv] = int(time.time())
                dirty = True
                ok, _ = send_webpush(
                    sub,
                    f"📖 Verset du Jour · {ctx['verset']['ref']}",
                    ctx['verset']['fr'],
                    url='/?tab=spirit&load=verset',
                    tag=kv,
                    silent=rem_silent,
                    kind='verse',
                    sound_url=rem_sound,
                )
                if ok:
                    sent_count += 1

        # 6. Citation de Cheikh Ahmadou Bamba
        if prefs.get('citationEnabled', True):
            cm = _to_min(prefs.get('citationTime', '13:30'))
            kc = f"citation_{today}"
            if cm >= 0 and not fired.get(kc) and cm <= now_min <= (cm + 20):
                fired[kc] = int(time.time())
                dirty = True
                ok, _ = send_webpush(
                    sub,
                    "۞ Parole de Cheikh Ahmadou Bamba",
                    f"« {ctx['citation']['texte']} » — {ctx['citation']['source']}",
                    url=f"/?tab=spirit&cid={ctx['citation']['id']}",
                    tag=kc,
                    silent=rem_silent,
                    kind='citation',
                    sound_url=rem_sound,
                )
                if ok:
                    sent_count += 1

        # 7. Suivi d'Étude Quotidien
        if prefs.get('studyEnabled', True):
            sm = _to_min(prefs.get('studyTime', '19:30'))
            ks = f"study_{today}"
            if sm >= 0 and not fired.get(ks) and sm <= now_min <= (sm + 20):
                fired[ks] = int(time.time())
                dirty = True
                ok, _ = send_webpush(
                    sub,
                    "🔥 Votre leçon du jour vous attend !",
                    "3 minutes sur Masaalik-ul Jinaan ou Tazawwudu-ç-Çighâr suffisent pour garder votre série !",
                    url='/apprentissage/',
                    tag=ks,
                    silent=rem_silent,
                    kind='study',
                    sound_url=rem_sound,
                )
                if ok:
                    sent_count += 1

        if dirty:
            # Limiter la taille de fired_json aux 40 entrées les plus récentes
            if len(fired) > 40:
                keep = sorted(fired.items(), key=lambda kv: kv[1])[-40:]
                fired = dict(keep)
            sub.fired_json = fired
            try:
                sub.save(update_fields=['fired_json', 'last_seen_son_id', 'last_seen_khassida_id', 'updated_at'])
            except Exception:
                pass

    return {'checked': len(subs), 'sent': sent_count}


def start_background_push_worker():
    """Démarre un thread léger en arrière-plan pour envoyer les Web Push programmés toutes les 60s."""
    global _WORKER_STARTED
    skip_cmds = {'migrate', 'makemigrations', 'collectstatic', 'shell', 'check', 'test', 'loaddata', 'dumpdata'}
    if any(cmd in sys.argv for cmd in skip_cmds):
        return
    if os.environ.get('SDM_DISABLE_PUSH_WORKER') == '1':
        return
    with _WORKER_LOCK:
        if _WORKER_STARTED:
            return
        _WORKER_STARTED = True

    def _loop():
        time.sleep(20)
        while True:
            try:
                if cache.add('sdm_webpush_tick_lock', '1', timeout=50):
                    close_old_connections()
                    process_due_webpushes()
                    close_old_connections()
            except Exception:
                pass
            time.sleep(55)

    t = threading.Thread(target=_loop, name='sdm-webpush-worker', daemon=True)
    t.start()
