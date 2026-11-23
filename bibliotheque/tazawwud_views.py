import json
import random
import uuid
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.urls import reverse

from .models import (
    TazawwudModule, TazawwudLecon, TazawwudQuestion, TazawwudChoix,
    TazawwudProgression, TazawwudReponseHistorique, TazawwudAchat,
    TazawwudCompagnon, TazawwudDefi, TazawwudBadge
)
from .fedapay_service import (
    creer_transaction_fedapay, verifier_transaction_fedapay, valider_achat_confirme
)


def get_rappels_tazawwud():
    """
    Extrait les rappels spirituels vérifiés (versets sources et synthèses à retenir)
    directement depuis les leçons de Tazawwudu-ç-Çighâr.
    """
    lecons = TazawwudLecon.objects.filter(est_revision_finale=False).select_related('module').order_by('module__numero', 'numero')
    rappels = []
    arabic_headers = {
        1: "بَابُ الْمُقَدِّمَةِ وَالتَّوْبَةِ",
        2: "بَابُ الْإِيمَانِ وَالتَّوْحِيدِ",
        3: "بَابُ الْإِسْلَامِ وَالطَّهَارَةِ",
        4: "بَابُ الصَّلَاةِ وَالصِّيَامِ",
        5: "بَابُ الْإِحْسَانِ وَالتَّصَوُّفِ",
    }
    for l in lecons:
        verset_extrait = (l.texte_source or "").strip().split('\n')[0][:220]
        retenir_lignes = [line.strip("•-* \t") for line in (l.a_retenir or "").strip().split('\n') if line.strip()]
        sagesse = retenir_lignes[0] if retenir_lignes else l.description
        rappels.append({
            'lecon_id': l.id,
            'numero': l.numero,
            'titre': l.titre,
            'chapitre': f"Partie {l.module.numero} · {l.module.titre}" if l.module else "Le Viatique",
            'arabe': arabic_headers.get(l.module.numero if l.module else 1, "تَزَوُّدُ الصِّغَارِ"),
            'verset': verset_extrait,
            'sagesse': sagesse,
            'points_cles': retenir_lignes[:3],
        })
    return rappels


GRANDES_ETAPES_META = {
    1: {
        'plage_vers': 'Vers 1 à 92 · 92 vers',
        'arabe': 'بَابُ الْمُقَدِّمَةِ وَالْإِيمَانِ وَالتَّوْحِيدِ',
        'sous_titre': 'Al-Muqaddimah & Al-Imân (La Profession de Foi)',
        'objectif_spirituel': "Enraciner la croyance authentique (Aqîdah) dans le cœur et connaître son Créateur par Ses Attributs de perfection.",
        'piliers_cles': [
            'Intention & Jeunesse',
            'Imân · Islâm · Ihsân',
            'Tawhîd (41 Attributs)',
            'Les 10 Grands Anges',
            'Les 104 Livres Célestes',
            'Les 25 Prophètes & Envoyés',
            'Jour Ultime & Décret Divin',
        ],
        'chiffres_cles': '41 Attributs · 10 Anges · 104 Livres · 6 Piliers de la Foi',
    },
    2: {
        'plage_vers': 'Vers 93 à 163 · 71 vers',
        'arabe': 'بَابُ الْإِسْلَامِ وَالتَّزْكِيَةِ وَالتَّوْبَةِ',
        'sous_titre': 'Al-Islâm I · Piliers, Pureté & Garde des 7 Membres',
        'objectif_spirituel': "Purifier son corps, ses habits et ses 7 organes par le repentir sincère avant de se tenir devant Allah.",
        'piliers_cles': [
            'Les 5 Piliers de l\'Islâm',
            'Shahâdah & Excellence du Dhikr',
            'Sacralité des 5 Prières',
            'Pureté Légale (Tahârah)',
            'Garde des 7 Organes',
            'Repentir Sincère (At-Tawbah)',
            'Distinction Fard / Sunnah',
        ],
        'chiffres_cles': '5 Piliers · 3 Puretés · 7 Organes à garder · 4 Conditions du Repentir',
    },
    3: {
        'plage_vers': 'Vers 164 à 205 · 42 vers',
        'arabe': 'بَابُ فَرَائِضِ الصَّلَاةِ وَالطَّهَارَةِ',
        'sous_titre': 'Al-Islâm II · Fiqh de la Prière, du Wudû\', du Ghusl & du Tayammum',
        'objectif_spirituel': "Accomplir ses ablutions, son bain rituel et sa prière exactement selon les règles validées par les savants malikites.",
        'piliers_cles': [
            '15 Obligations de la Prière',
            '18 Sunan (8 Mu\'akkadah)',
            'Ablutions Wudû\' (7 Fard / 8 Sunan)',
            'Bain Rituel Ghusl (5 Fard / 4 Sunan)',
            'Tayammum (8 Fard / 3 Sunan)',
        ],
        'chiffres_cles': '15 Fard Prière · 7 Fard Wudû\' · 5 Fard Ghusl · 8 Fard Tayammum',
    },
    4: {
        'plage_vers': 'Vers 206 à 273 · 68 vers',
        'arabe': 'بَابُ الصِّيَامِ وَالزَّكَاةِ وَالْحَجِّ وَالْقَضَاءِ',
        'sous_titre': 'Al-Islâm III · Jeûne, Zakât, Hajj & Rattrapage des Prières',
        'objectif_spirituel': "Maîtriser le Jeûne, la Zakât, le Hajj et savoir rattraper sans erreur toute unité de prière manquée derrière l'Imam.",
        'piliers_cles': [
            'Jeûne Siyâm (2 Fard / 3 Sunan)',
            'Aumône Zakât (4 Fard / 3 Sunan)',
            'Pèlerinage Hajj (4 Piliers / 12 Sunan)',
            'Invocation après le Wudû\'',
            'Rattrapage derrière l\'Imam (Masbûq)',
            'Prière du Malade',
        ],
        'chiffres_cles': '2 Fard Jeûne · 4 Fard Zakât · 4 Piliers Hajj · 5 Cas de Rattrapage',
    },
    5: {
        'plage_vers': 'Vers 274 à 308 · 35 vers',
        'arabe': 'بَابُ الْإِحْسَانِ وَالتَّصَوُّفِ وَالْخَاتِمَةِ',
        'sous_titre': 'Al-Ihsân & At-Tasawwuf · Excellence Spirituelle & Sagesse Finale',
        'objectif_spirituel': "Atteindre la présence du cœur (Ihsân), polir son âme auprès d'un Guide éclairé et saisir les 5 trésors de la vie.",
        'piliers_cles': [
            'Degré suprême de l\'Ihsân',
            'Science & Scrupule (Wara\')',
            'Sincérité (Ikhlâs) & Gratitude',
            'Guide Spirituel Éclairé (Cheikh)',
            'Les 5 Situations avant leurs 5 contraires',
            'Épilogue & Du\'â de Bonne Fin',
        ],
        'chiffres_cles': '2 Stations de l\'Ihsân · 4 Vertus Cardinales · 5 Trésors de la Vie',
    },
}


# ── 1. ACCUEIL DU PARCOURS TAZAWWUD ──

@login_required
def tazawwud_home(request):
    """Page d'accueil du parcours avec la route d'apprentissage."""
    modules = TazawwudModule.objects.all().order_by('numero')
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
    progression.verifier_semaine_reset()

    total_lecons = TazawwudLecon.objects.count()
    lecons_terminees_count = progression.lecons_terminees.count()
    pourcentage = int((lecons_terminees_count / total_lecons * 100) if total_lecons > 0 else 0)

    # Vérification des accès aux révisions intensives
    a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)
    modules_payes_ids = list(TazawwudAchat.objects.filter(
        user=request.user, type_achat='MODULE', statut='APPROVED'
    ).values_list('module_id', flat=True))
    terminees_ids = set(progression.lecons_terminees.values_list('id', flat=True))

    modules_data = []
    for m in modules:
        m_lecons = m.lecons.exclude(numero=99).order_by('numero')
        m_total = m_lecons.count()
        m_done = m_lecons.filter(id__in=terminees_ids).count()
        m_pct = int((m_done / m_total * 100) if m_total > 0 else 0)
        is_unlocked = a_forfait_complet or (m.id in modules_payes_ids)
        meta = GRANDES_ETAPES_META.get(m.numero, {})
        nb_questions_mod = TazawwudQuestion.objects.filter(lecon__module=m).exclude(lecon__numero=99).count()
        modules_data.append({
            'module': m,
            'total_lecons': m_total,
            'lecons_terminees': m_done,
            'pourcentage': m_pct,
            'revision_payee': is_unlocked,
            'meta': meta,
            'lecons_list': m_lecons,
            'nb_questions': nb_questions_mod,
        })

    # Réponses à revoir
    nb_erreurs = TazawwudReponseHistorique.objects.filter(user=request.user, est_correct=False).count()

    # Rappels vivants du Viatique
    rappels_list = get_rappels_tazawwud()
    rappel_du_jour = rappels_list[timezone.now().day % len(rappels_list)] if rappels_list else None

    # ── ÉVOLUTION 7 JOURS & COACH "MODE DUOLINGO" (série, jours faits vs jours sautés) ──
    today_d = timezone.now().date()
    day_names_fr = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    jours_7 = []
    for i in range(6, -1, -1):
        jd = today_d - timedelta(days=i)
        done_day = TazawwudReponseHistorique.objects.filter(
            user=request.user, date_tentative__date=jd
        ).exists()
        jours_7.append({
            'label': day_names_fr[jd.weekday()],
            'num': jd.day,
            'done': done_day,
            'is_today': (jd == today_d),
            'missed': (not done_day and jd < today_d),
        })

    done_today = jours_7[-1]['done']
    missed_yesterday = jours_7[-2]['missed'] if len(jours_7) >= 2 else False
    missed_days_count = sum(1 for j in jours_7[:-1] if j['missed'])

    # Calcul de la série active réelle (consécutive jusqu'à aujourd'hui ou hier)
    streak_live = progression.serie_jours or 0
    if done_today and streak_live == 0:
        streak_live = 1

    # Prochaine leçon recommandée (première leçon non terminée)
    next_lecon = TazawwudLecon.objects.filter(est_revision_finale=False).exclude(
        id__in=terminees_ids
    ).order_by('module__numero', 'numero').first() or TazawwudLecon.objects.filter(
        est_revision_finale=False
    ).order_by('module__numero', 'numero').first()

    if done_today:
        coach_mode = 'done_today'
        coach_title = f"Bravo ! Journée validée · Série {streak_live} jour(s) 🔥"
        coach_msg = "Tu as nourri ton âme aujourd'hui avec Tazawwudu-ç-Çighâr. Reviens demain ou continue une étape bonus !"
    elif missed_yesterday:
        coach_mode = 'missed'
        coach_title = "🔥 Rappel de Série : Tu as sauté hier !"
        coach_msg = f"Attention ! {missed_days_count} jour(s) manqué(s) cette semaine. Cheikh Ahmadou Bamba t'attend : fais juste 2 minutes maintenant pour rallumer ta flamme !"
    else:
        coach_mode = 'todo_today'
        coach_title = f"🔥 Ta flamme de {streak_live} jour(s) attend ta leçon du jour !" if streak_live > 0 else "🔥 Lance ta série quotidienne Tazawwudu-ç-Çighâr !"
        coach_msg = "Ne laisse pas passer la journée sans lire 3 petites cartes du livre et répondre aux questions intermédiaires (2 min) !"

    context = {
        'modules_data': modules_data,
        'terminees_ids': terminees_ids,
        'progression': progression,
        'pourcentage': pourcentage,
        'a_forfait_complet': a_forfait_complet,
        'nb_erreurs': nb_erreurs,
        'rappel_du_jour': rappel_du_jour,
        'rappels_json': json.dumps(rappels_list),
        'jours_7': jours_7,
        'streak_live': streak_live,
        'done_today': done_today,
        'coach_mode': coach_mode,
        'coach_title': coach_title,
        'coach_msg': coach_msg,
        'next_lecon': next_lecon,
    }
    return render(request, 'bibliotheque/tazawwud/home.html', context)


# ── 2. TABLEAU DE BORD DE L'ÉLÈVE ──

@login_required
def tazawwud_dashboard(request):
    """
    Tableau de bord complet de l'élève :
    - Progression dans chaque grande partie du livre
    - Résultats et réponses à revoir
    - Activité de la semaine (7 derniers jours) et streak
    - Quiz gratuits vs révisions payantes
    - Compagnons & Classement de la semaine
    """
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
    progression.verifier_semaine_reset()

    modules = TazawwudModule.objects.all().order_by('numero')
    a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)
    modules_payes_ids = set(TazawwudAchat.objects.filter(
        user=request.user, type_achat='MODULE', statut='APPROVED'
    ).values_list('module_id', flat=True))

    terminees_ids = set(progression.lecons_terminees.values_list('id', flat=True))

    # Détail par module
    modules_stats = []
    for m in modules:
        lecons = m.lecons.all()
        lecons_ord = lecons.filter(est_revision_finale=False)
        revision = lecons.filter(est_revision_finale=True).first()

        nb_ord_total = lecons_ord.count()
        nb_ord_done = lecons_ord.filter(id__in=terminees_ids).count()
        rev_done = (revision.id in terminees_ids) if revision else False
        is_rev_unlocked = a_forfait_complet or (m.id in modules_payes_ids)

        modules_stats.append({
            'module': m,
            'nb_lecons': nb_ord_total,
            'nb_terminees': nb_ord_done,
            'pourcentage': int((nb_ord_done / nb_ord_total * 100) if nb_ord_total > 0 else 0),
            'revision': revision,
            'revision_terminee': rev_done,
            'revision_debloquee': is_rev_unlocked,
            'prix_fcfa': 500,
        })

    # Réponses à revoir (dernières erreurs distinctes)
    erreurs = TazawwudReponseHistorique.objects.filter(
        user=request.user, est_correct=False
    ).select_related('question', 'question__lecon').order_by('-date_tentative')[:15]

    # Activité des 7 derniers jours (calendrier / barres)
    today = timezone.now().date()
    jours_activite = []
    max_pts_jour = 10
    for i in range(6, -1, -1):
        j_date = today - timedelta(days=i)
        # Calculer le nombre de réponses données ce jour
        cnt = TazawwudReponseHistorique.objects.filter(
            user=request.user, date_tentative__date=j_date
        ).count()
        pts = cnt * 10
        if pts > max_pts_jour:
            max_pts_jour = pts
        jours_activite.append({
            'date': j_date,
            'nom_jour': j_date.strftime('%a'),
            'reponses': cnt,
            'points': pts,
            'est_aujourdhui': (j_date == today),
        })

    # Compagnons
    amis_ids = list(TazawwudCompagnon.objects.filter(
        Q(demandeur=request.user) | Q(ami=request.user),
        statut='ACCEPTE'
    ).values_list('demandeur_id', 'ami_id'))
    compagnons_ids = set()
    for d, a in amis_ids:
        compagnons_ids.add(d if d != request.user.id else a)

    compagnons = TazawwudProgression.objects.filter(
        user_id__in=compagnons_ids, est_profil_public=True
    ).select_related('user').order_by('-points_semaine')[:5]

    # Classement hebdomadaire général (profils publics)
    classement_hebdo = TazawwudProgression.objects.filter(
        est_profil_public=True, points_semaine__gt=0
    ).select_related('user').order_by('-points_semaine')[:10]

    rappels_list = get_rappels_tazawwud()
    rappel_du_jour = rappels_list[timezone.now().day % len(rappels_list)] if rappels_list else None

    context = {
        'progression': progression,
        'modules_stats': modules_stats,
        'erreurs': erreurs,
        'nb_erreurs': erreurs.count(),
        'jours_activite': jours_activite,
        'max_pts_jour': max_pts_jour,
        'a_forfait_complet': a_forfait_complet,
        'compagnons': compagnons,
        'classement_hebdo': classement_hebdo,
        'rappel_du_jour': rappel_du_jour,
        'rappels_json': json.dumps(rappels_list),
    }
    return render(request, 'bibliotheque/tazawwud/dashboard.html', context)


# ── 3. DÉTAIL D'UN MODULE & LEÇONS ──

@login_required
def tazawwud_module(request, module_id):
    """Affiche la liste des leçons d'un module et son étape de révision bloquante."""
    module = get_object_or_404(TazawwudModule, id=module_id)
    lecons = module.lecons.exclude(numero=99).order_by('numero')
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    terminees_ids = list(progression.lecons_terminees.values_list('id', flat=True))
    a_acces_revision = TazawwudAchat.a_acces_revision(request.user, module)
    a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)
    meta = GRANDES_ETAPES_META.get(module.numero, {})

    context = {
        'module': module,
        'meta': meta,
        'lecons': lecons,
        'terminees_ids': terminees_ids,
        'progression': progression,
        'a_acces_revision': a_acces_revision,
        'a_forfait_complet': a_forfait_complet,
    }
    return render(request, 'bibliotheque/tazawwud/module.html', context)


def _chunk_text_for_small_screen(raw_text, max_chars=230):
    """
    Découpe fidèlement le texte du livre en courtes cartes calibrées pour un petit écran mobile
    (2 à 4 lignes max par écran, sans pavés à scroller, sans modifier le sens du livre).
    """
    import re
    if not raw_text:
        return []
    paragraphs = [p.strip() for p in raw_text.replace('\r', '').split('\n') if p.strip()]
    chunks = []
    cur = ''
    for para in paragraphs:
        # Si le paragraphe est déjà court, on essaie de le regrouper ou de le garder seul
        sentences = re.split(r'(?<=[.!?؛؟])\s+', para)
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            if not cur:
                cur = sent
            elif len(cur) + 1 + len(sent) <= max_chars:
                cur = cur + '\n' + sent if len(sent) > 70 else cur + ' ' + sent
            else:
                chunks.append(cur)
                cur = sent
        if cur and len(cur) >= max_chars * 0.6:
            chunks.append(cur)
            cur = ''
    if cur:
        chunks.append(cur)
    return chunks


def _build_duolingo_lesson_deck(lecon):
    """
    Construit un parcours étape par étape façon Duolingo :
    - Petites cartes de lecture fidèles au livre (calibrées petit écran)
    - Cartes « Ce que dit le livre » (résumé objectif issu des points clés du texte)
    - Questions intermédiaires riches (DB + questions objectives générées directement sur le texte du livre)
      intercalées AU MILIEU de la leçon (6 à 10 questions par chapitre au lieu de 2–3 !).
    """
    import re
    rng = random.Random(f"tazawwud_deck_{lecon.id}")

    source_cards = _chunk_text_for_small_screen(lecon.texte_source or '', max_chars=225)
    summary_lines = [
        line.lstrip('•-*— \t').strip()
        for line in (lecon.a_retenir or '').splitlines()
        if len(line.lstrip('•-*— \t').strip()) >= 18
    ]
    explication_cards = _chunk_text_for_small_screen(lecon.explication or '', max_chars=220)

    # 1. Collecter les questions existantes en base (QCM / Vrai-Faux)
    db_questions = []
    for q in lecon.questions.prefetch_related('choix').order_by('ordre', 'id'):
        choix = [{'id': c.id, 'texte': c.texte, 'est_correct': c.est_correct} for c in q.choix.all()]
        if len(choix) >= 2:
            rng.shuffle(choix)
            db_questions.append({
                'kind': 'question',
                'db_id': q.id,
                'badge': 'Question du Chapitre',
                'texte': q.texte,
                'explication': q.explication_reponse or "Vérifié d'après le texte de Tazawwudu-ç-Çighâr.",
                'points': q.points or 15,
                'choix': choix,
            })

    # 2. Enrichir automatiquement avec des questions intermédiaires OBJECTIVES fidèles au livre
    # (pour passer de 2-3 questions à 7-9 questions par leçon !)
    other_points_pool = list(
        TazawwudLecon.objects.exclude(id=lecon.id)
        .values_list('a_retenir', flat=True)[:25]
    )
    distractor_sentences = []
    for blob in other_points_pool:
        for ln in (blob or '').splitlines():
            cl = ln.lstrip('•-*— \t').strip()
            if 22 <= len(cl) <= 135:
                distractor_sentences.append(cl)

    generated_qs = []

    # 2a. Questions « Compléter la phrase du livre » à partir des points clés de cette leçon
    for idx, pt in enumerate(summary_lines):
        if len(db_questions) + len(generated_qs) >= 8:
            break
        words = [w for w in re.findall(r"[A-Za-zÀ-ÿ'\-]{5,}", pt) if w.lower() not in {'cette', 'celui', 'celle', 'dans', 'pour', 'avec', 'entre', 'comme', 'toute', 'toutes', 'leçon', 'livre', 'cheikh', 'bamba', 'selon', 'doit', 'être', 'aussi', 'notre', 'votre', 'leurs'}]
        if not words:
            continue
        target_word = max(words, key=len)
        blanked = re.sub(r'\b' + re.escape(target_word) + r'\b', '________', pt, count=1)
        if blanked == pt:
            continue
        # Choisir 3 mots distracteurs plausibles issus d'autres phrases du livre
        other_words = list({
            w for s in distractor_sentences
            for w in re.findall(r"[A-Za-zÀ-ÿ'\-]{5,}", s)
            if w.lower() != target_word.lower() and w.lower() not in {'cette', 'celui', 'celle', 'toute', 'toutes', 'cheikh', 'bamba'}
        })
        if len(other_words) < 3:
            other_words = ['Sincérité', 'Ablution', 'Patience', 'Obligation', 'Prophète', 'Prière']
        wrongs = rng.sample([w for w in other_words if w.lower() != target_word.lower()], 3)
        choix = [{'id': 0, 'texte': target_word, 'est_correct': True}] + [
            {'id': 0, 'texte': w, 'est_correct': False} for w in wrongs
        ]
        rng.shuffle(choix)
        generated_qs.append({
            'kind': 'question',
            'db_id': None,
            'badge': 'Compléter le Texte du Livre',
            'texte': f"Complétez cet enseignement fidèle au livre :\n« {blanked} »",
            'explication': f"Phrase complète d'après le livre : « {pt} »",
            'points': 10,
            'choix': choix,
        })

    # 2b. Questions « Ce que dit le livre » (reconnaître l'enseignement exact de cette leçon parmi 4)
    for pt in summary_lines[:3]:
        if len(db_questions) + len(generated_qs) >= 9:
            break
        if len(pt) <= 135 and len(distractor_sentences) >= 3:
            wrongs = rng.sample([s for s in distractor_sentences if s.lower() != pt.lower()], 3)
            choix = [{'id': 0, 'texte': pt, 'est_correct': True}] + [
                {'id': 0, 'texte': w, 'est_correct': False} for w in wrongs
            ]
            rng.shuffle(choix)
            generated_qs.append({
                'kind': 'question',
                'db_id': None,
                'badge': 'Vérification Fidèle au Livre',
                'texte': f"Lequel de ces enseignements appartient directement au chapitre « {lecon.titre} » ?",
                'explication': f"Exact ! Le livre enseigne dans « {lecon.titre} » : {pt}",
                'points': 10,
                'choix': choix,
            })

    # 2c. Question Vrai / Faux fidèle au texte
    if summary_lines and (len(db_questions) + len(generated_qs)) < 8:
        pt0 = summary_lines[0]
        generated_qs.append({
            'kind': 'question',
            'db_id': None,
            'badge': 'Vrai ou Faux · Texte du Livre',
            'texte': f"D'après ce chapitre de Tazawwudu-ç-Çighâr :\n« {pt0} »",
            'explication': f"Vrai ! C'est exactement ce qu'énonce ce passage de « {lecon.titre} ».",
            'points': 10,
            'choix': [
                {'id': 0, 'texte': 'Vrai — C\'est enseigné dans ce passage', 'est_correct': True},
                {'id': 0, 'texte': 'Faux — Le livre dit le contraire', 'est_correct': False},
            ],
        })

    all_questions = db_questions + generated_qs

    # 3. Construire la liste des cartes de lecture (courtes, fidèles au livre)
    read_cards = []
    for i, sc in enumerate(source_cards[:8], 1):
        read_cards.append({
            'kind': 'book',
            'badge': f'Texte du Livre · Passage {i}/{min(len(source_cards), 8)}',
            'title': lecon.titre,
            'texte': sc,
            'footer': 'Tazawwudu-ç-Çighâr · Cheikh Ahmadou Bamba',
        })
    for i, ec in enumerate(explication_cards[:4], 1):
        read_cards.append({
            'kind': 'summary',
            'badge': f'Ce que dit le livre · Synthèse {i}',
            'title': 'Résumé objectif du passage',
            'texte': ec,
            'footer': 'Résumé fidèle au texte sans interprétation subjective',
        })
    if summary_lines:
        for i in range(0, min(len(summary_lines), 6), 2):
            pair = summary_lines[i:i+2]
            read_cards.append({
                'kind': 'summary',
                'badge': 'Points Clés du Livre',
                'title': 'À ancrer dans votre mémoire',
                'texte': '\n\n'.join(f'۞ {p}' for p in pair),
                'footer': f'Chapitre : {lecon.titre}',
            })

    # 4. INTERCALER lecture courte (1-2 cartes) + question intermédiaire (façon Duolingo !)
    deck = []
    q_idx = 0
    for idx_r, rcard in enumerate(read_cards):
        deck.append(rcard)
        # Après chaque 1 ou 2 cartes de lecture, insérer une question intermédiaire !
        if q_idx < len(all_questions) and ((idx_r + 1) % 2 == 0 or idx_r == len(read_cards) - 1):
            deck.append(all_questions[q_idx])
            q_idx += 1

    # Ajouter les questions restantes en fin de parcours (défi de validation du chapitre)
    while q_idx < len(all_questions):
        deck.append(all_questions[q_idx])
        q_idx += 1

    return deck, len(all_questions)


@login_required
def tazawwud_lecon(request, lecon_id):
    """Parcours étape par étape façon Duolingo : courtes cartes calibrées petit écran + questions intermédiaires riches."""
    lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    is_finale_livre = (lecon.numero == 99 or 'finale' in lecon.titre.lower())
    if lecon.est_revision_finale:
        a_acces = TazawwudAchat.a_acces_revision(request.user, None if is_finale_livre else lecon.module)
        if not a_acces:
            return redirect('tazawwud_revision', lecon_id=lecon.id)

    deck, total_questions = _build_duolingo_lesson_deck(lecon)
    next_lecon = TazawwudLecon.objects.filter(
        module=lecon.module, numero__gt=lecon.numero, est_revision_finale=False
    ).order_by('numero').first() or TazawwudLecon.objects.filter(
        module__numero__gt=lecon.module.numero, est_revision_finale=False
    ).order_by('module__numero', 'numero').first()

    context = {
        'lecon': lecon,
        'progression': progression,
        'is_revision_dossier': lecon.est_revision_finale,
        'is_finale_livre': is_finale_livre,
        'deck_json': json.dumps(deck, ensure_ascii=False),
        'total_steps': len(deck),
        'total_questions': total_questions,
        'next_lecon': next_lecon,
    }
    return render(request, 'bibliotheque/tazawwud/lecon.html', context)


# ── 4. QUIZ, RÉVISIONS ET SYSTÈME DE VIES ──

def formater_questions_pour_js(questions_queryset):
    """Encode les questions pour le moteur interactif JS (QCM, V/F, Association, Texte Court)."""
    questions_data = []
    for q in questions_queryset:
        choix_list = [{'id': c.id, 'texte': c.texte, 'est_correct': c.est_correct} for c in q.choix.all()]
        random.shuffle(choix_list)

        q_dict = {
            'id': q.id,
            'texte': q.texte,
            'type_question': q.type_question,
            'difficulte': q.difficulte,
            'points': q.points,
            'explication': q.explication_reponse,
            'choix': choix_list,
            'donnees_extra': q.donnees_extra or {},
        }
        questions_data.append(q_dict)
    return questions_data


@login_required
def tazawwud_quiz(request, lecon_id):
    """Quiz régulier de validation de leçon (gratuit)."""
    lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    # Récupérer les questions de cette leçon
    questions = lecon.questions.all().order_by('ordre', 'id')
    questions_data = formater_questions_pour_js(questions)

    context = {
        'lecon': lecon,
        'module': lecon.module,
        'progression': progression,
        'questions_json': json.dumps(questions_data),
        'is_revision': False,
        'mode_entrainement': False,
    }
    return render(request, 'bibliotheque/tazawwud/quiz.html', context)


@login_required
def tazawwud_revision(request, lecon_id):
    """
    Révision intensive de fin de module ou révision finale.
    Payante : 500 FCFA par module ou 2000 FCFA forfait complet.
    """
    lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    is_finale_livre = (lecon.numero == 99 or 'finale' in lecon.titre.lower())
    # Vérification des droits d'accès (la Révision Finale 99 requiert le forfait COMPLET)
    a_acces = TazawwudAchat.a_acces_revision(request.user, None if is_finale_livre else lecon.module)

    if not a_acces:
        meta = GRANDES_ETAPES_META.get(lecon.module.numero, {}) if lecon.module else {}
        nb_questions_exclusives = lecon.questions.count()
        nb_questions_chapitre = TazawwudQuestion.objects.filter(
            lecon__module=lecon.module
        ).exclude(lecon__numero=99).count() if lecon.module else 0
        total_questions_banque = TazawwudQuestion.objects.count()
        apercu_points = [
            line.lstrip('-•* ').strip()
            for line in (lecon.a_retenir or '').splitlines()
            if line.strip()
        ][:4]
        exemple_question = lecon.questions.filter(type_question='qcm').first()

        modules_payes_ids = set(TazawwudAchat.objects.filter(
            user=request.user, type_achat='MODULE', statut='APPROVED'
        ).values_list('module_id', flat=True))
        a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)

        modules_inclus = []
        for m in TazawwudModule.objects.all().order_by('numero'):
            rev_lecon = m.lecons.filter(est_revision_finale=True).exclude(numero=99).first()
            modules_inclus.append({
                'module': m,
                'meta': GRANDES_ETAPES_META.get(m.numero, {}),
                'rev_lecon': rev_lecon,
                'nb_q_rev': rev_lecon.questions.count() if rev_lecon else 15,
                'debloque': a_forfait_complet or (m.id in modules_payes_ids),
            })

        context = {
            'lecon': lecon,
            'module': lecon.module,
            'meta': meta,
            'is_finale_livre': is_finale_livre,
            'nb_questions_exclusives': nb_questions_exclusives,
            'nb_questions_chapitre': nb_questions_chapitre,
            'total_questions_banque': total_questions_banque,
            'apercu_points': apercu_points,
            'exemple_question': exemple_question,
            'modules_inclus': modules_inclus,
            'prix_module': 500,
            'prix_complet': 2000,
        }
        return render(request, 'bibliotheque/tazawwud/verrouille.html', context)

    # Si c'est la révision finale de tout le livre (lecon 99 ou titre 'Révision Finale')
    if is_finale_livre:
        # Tirer 30 questions variées couvrant tout le livre (en incluant les questions de synthèse)
        all_q_ids = list(TazawwudQuestion.objects.values_list('id', flat=True))
        selected_ids = random.sample(all_q_ids, min(len(all_q_ids), 30))
        questions = list(TazawwudQuestion.objects.filter(id__in=selected_ids))
        random.shuffle(questions)
    else:
        # Révision du module : les 15 questions exclusives de la révision + 5 questions du chapitre = 20 questions
        rev_q_ids = list(lecon.questions.values_list('id', flat=True))
        other_q_ids = list(
            TazawwudQuestion.objects.filter(lecon__module=lecon.module)
            .exclude(lecon_id=lecon.id)
            .exclude(lecon__numero=99)
            .values_list('id', flat=True)
        )
        sampled_other = random.sample(other_q_ids, min(len(other_q_ids), 5))
        combined_ids = rev_q_ids + sampled_other
        questions = list(TazawwudQuestion.objects.filter(id__in=combined_ids))
        random.shuffle(questions)

    questions_data = formater_questions_pour_js(questions)

    context = {
        'lecon': lecon,
        'module': lecon.module,
        'progression': progression,
        'questions_json': json.dumps(questions_data),
        'is_revision': True,
        'is_finale_livre': is_finale_livre,
        'mode_entrainement': False,
    }
    return render(request, 'bibliotheque/tazawwud/quiz.html', context)


@login_required
def tazawwud_entrainement(request):
    """
    Mode entraînement gratuit (toujours accessible même à 0 vie).
    Permet de revoir les questions manquées et de recharger ses 3 vies !
    """
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    # Questions manquées par l'utilisateur
    erreurs_q_ids = list(TazawwudReponseHistorique.objects.filter(
        user=request.user, est_correct=False
    ).values_list('question_id', flat=True).distinct())

    if erreurs_q_ids:
        sample_ids = random.sample(erreurs_q_ids, min(len(erreurs_q_ids), 10))
        questions = TazawwudQuestion.objects.filter(id__in=sample_ids)
    else:
        # Fallback si aucune erreur enregistrée : questions faciles
        questions = TazawwudQuestion.objects.filter(difficulte='facile').order_by('?')[:8]

    questions_data = formater_questions_pour_js(questions)

    context = {
        'progression': progression,
        'questions_json': json.dumps(questions_data),
        'is_revision': False,
        'mode_entrainement': True,
    }
    return render(request, 'bibliotheque/tazawwud/quiz.html', context)


@login_required
def tazawwud_recharger_vies(request):
    """Recharge les vies de l'utilisateur."""
    if request.method == 'POST':
        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
        progression.recharger_vies()
        return JsonResponse({'status': 'success', 'vies': progression.vies_actuelles})
    return JsonResponse({'status': 'error'}, status=405)


# ── 5. APIS DE VALIDATION DES RÉPONSES & SAUVEGARDE ──

@csrf_exempt
@login_required
def api_tazawwud_reponse(request):
    """
    Valide une réponse individuelle, met à jour les vies et enregistre l'historique.
    Supporte : QCM, Vrai/Faux, Association, Réponse Courte.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        reponse_user = data.get('reponse')
        mode_entrainement = data.get('mode_entrainement', False)

        question = get_object_or_404(TazawwudQuestion, id=question_id)
        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

        est_correct = False

        if question.type_question in ['qcm', 'vrai_faux']:
            # reponse_user est l'ID du choix ou le texte
            choix_correct = question.choix.filter(est_correct=True).first()
            if choix_correct:
                if str(reponse_user) == str(choix_correct.id) or str(reponse_user).strip().lower() == choix_correct.texte.strip().lower():
                    est_correct = True

        elif question.type_question == 'texte_court':
            # reponse_user est une chaîne de caractères
            reponses_valides = question.donnees_extra.get('reponses_acceptees', [])
            val_clean = str(reponse_user or '').strip().lower()
            if val_clean in [r.strip().lower() for r in reponses_valides]:
                est_correct = True

        elif question.type_question == 'association':
            # reponse_user est un dict {"gauche": "droite"}
            paires_officielles = question.donnees_extra.get('paires', [])
            paires_dict = {p['gauche'].strip().lower(): p['droite'].strip().lower() for p in paires_officielles}

            if isinstance(reponse_user, dict):
                user_dict = {str(k).strip().lower(): str(v).strip().lower() for k, v in reponse_user.items()}
                # Toutes les paires correspondent ?
                if user_dict == paires_dict:
                    est_correct = True

        # Enregistrement dans l'historique pour analyse des erreurs
        TazawwudReponseHistorique.objects.create(
            user=request.user,
            question=question,
            est_correct=est_correct,
            reponse_donnee=str(reponse_user)[:500]
        )

        vies_restantes = progression.vies_actuelles
        if not est_correct and not mode_entrainement:
            vies_restantes = progression.perdre_vie()

        return JsonResponse({
            'status': 'success',
            'est_correct': est_correct,
            'explication': question.explication_reponse,
            'vies_restantes': vies_restantes,
            'points_gagnes': question.points if est_correct else 0,
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def api_tazawwud_save_score(request):
    """Valide la fin de session de quiz ou révision."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        lecon_id = data.get('lecon_id')
        score = int(data.get('score', 0))
        mode_entrainement = data.get('mode_entrainement', False)

        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

        if mode_entrainement:
            # En mode entraînement, on recharge automatiquement les vies
            progression.recharger_vies()
            return JsonResponse({'status': 'success', 'message': 'Vies rechargées !'})

        if lecon_id:
            lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
            progression.lecons_terminees.add(lecon)

        progression.ajouter_points(score)
        return JsonResponse({'status': 'success', 'nouveau_score': progression.score_total})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# ── 6. PAIEMENTS FEDAPAY (RÉVISIONS PAYANTES) ──

@login_required
def tazawwud_initier_paiement(request):
    """
    Initie une transaction FedaPay :
    - 500 FCFA par module (type_achat='MODULE')
    - 2000 FCFA pour le forfait complet (type_achat='COMPLET')
    """
    if request.method != 'POST':
        return redirect('tazawwud_dashboard')

    type_achat = request.POST.get('type_achat', 'MODULE')
    module_id = request.POST.get('module_id')

    module = None
    if type_achat == 'MODULE':
        module = get_object_or_404(TazawwudModule, id=module_id)
        montant = 500
    else:
        type_achat = 'COMPLET'
        montant = 2000

    reference = f"TZW-{timezone.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

    achat = TazawwudAchat.objects.create(
        user=request.user,
        type_achat=type_achat,
        module=module,
        montant=montant,
        reference=reference,
        statut='PENDING'
    )

    callback_url = request.build_absolute_uri(reverse('tazawwud_paiement_callback'))
    webhook_url = request.build_absolute_uri(reverse('tazawwud_paiement_webhook'))

    customer_data = {
        'firstname': request.user.first_name or request.user.username,
        'lastname': request.user.last_name or 'SDM',
        'email': request.user.email,
        'phone': request.POST.get('telephone', '00000000')
    }

    result = creer_transaction_fedapay(achat, customer_data, callback_url, webhook_url=webhook_url)

    if result.get('success'):
        checkout_url = result.get('checkout_url')
        return redirect(checkout_url)
    else:
        return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
            'achat': achat,
            'statut_visuel': 'erreur',
            'message': result.get('error', "Impossible d'initier la session de paiement DexPay.")
        })


@login_required
def tazawwud_paiement_callback(request):
    """
    Retour après paiement DexPay.
    Vérifie formellement le statut auprès de l'API serveur DexPay avant d'accorder l'accès.
    """
    tx_id = request.GET.get('id')
    reference = request.GET.get('reference') or request.GET.get('ref')

    achat = None
    if reference:
        achat = TazawwudAchat.objects.filter(reference=reference).first()
    if not achat and tx_id:
        achat = TazawwudAchat.objects.filter(fedapay_transaction_id=str(tx_id)).first()

    if not achat:
        return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
            'statut_visuel': 'erreur',
            'message': "Transaction introuvable ou invalide."
        })

    # Interrogation directe et sécurisée du serveur DexPay via la référence de la session
    tx_check = verifier_transaction_fedapay(achat.reference or achat.fedapay_transaction_id or tx_id)

    if tx_check.get('success'):
        status = tx_check.get('status', '').lower()
        if status == 'approved':
            valider_achat_confirme(achat, tx_check.get('data'))
            if achat.type_achat == 'COMPLET':
                revisions_debloquees = TazawwudLecon.objects.filter(
                    est_revision_finale=True
                ).select_related('module').order_by('module__numero', 'numero')
            else:
                revisions_debloquees = TazawwudLecon.objects.filter(
                    module=achat.module, est_revision_finale=True
                ).exclude(numero=99).select_related('module')
            return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
                'achat': achat,
                'revisions_debloquees': revisions_debloquees,
                'statut_visuel': 'succes',
                'message': "Paiement confirmé par DexPay avec succès ! Votre révision intensive et son dossier de synthèse sont débloqués."
            })
        elif status == 'pending':
            return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
                'achat': achat,
                'statut_visuel': 'attente',
                'message': "Transaction en cours de traitement chez l'opérateur. Veuillez patienter ou actualiser."
            })
        else:
            achat.statut = 'DECLINED' if status in ['declined', 'failed'] else 'CANCELED'
            achat.save()
            return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
                'achat': achat,
                'statut_visuel': 'echec',
                'message': f"Le paiement n'a pas abouti (statut : {status}). Aucun montant n'a été débité."
            })

    return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
        'achat': achat,
        'statut_visuel': 'erreur',
        'message': "Impossible de vérifier la transaction auprès de DexPay pour le moment."
    })


@csrf_exempt
def tazawwud_paiement_webhook(request):
    """
    Webhook IPN DexPay (reçu côté serveur en asynchrone).
    Gère les notifications multiples de manière idempotente.
    """
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        event_name = str(payload.get('event') or payload.get('name') or payload.get('type') or '').lower()
        entity = payload.get('data') or payload.get('entity') or payload
        ref = entity.get('reference') or payload.get('reference') or (entity.get('custom_metadata') or {}).get('reference')
        tx_id = entity.get('id') or payload.get('id')

        achat = None
        if ref:
            achat = TazawwudAchat.objects.filter(reference=str(ref)).first()
        if not achat and tx_id:
            achat = TazawwudAchat.objects.filter(fedapay_transaction_id=str(tx_id)).first()

        if not achat:
            return HttpResponse("No matching transaction", status=400)

        raw_status = str(entity.get('status') or payload.get('status') or '').lower()
        if (
            raw_status in ['completed', 'paid', 'success', 'succeeded', 'approved']
            or any(k in event_name for k in ['completed', 'paid', 'success', 'approved'])
        ):
            valider_achat_confirme(achat, payload)
        elif (
            raw_status in ['failed', 'declined', 'canceled', 'cancelled', 'expired']
            or any(k in event_name for k in ['failed', 'declined', 'cancel'])
        ):
            achat.statut = 'CANCELED' if 'cancel' in (raw_status + event_name) else 'DECLINED'
            achat.save()

        return HttpResponse("Webhook processed successfully", status=200)

    except Exception as e:
        return HttpResponse(f"Webhook error: {str(e)}", status=400)


@login_required
def tazawwud_paiement_simulation(request, reference):
    """
    Page de simulation locale / bac à sable pour tester le déblocage
    instantané sans carte bancaire lorsque FEDAPAY_ENVIRONMENT est en démo.
    """
    achat = get_object_or_404(TazawwudAchat, reference=reference, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'payer':
            valider_achat_confirme(achat, {'simulateur': 'bac_a_sable_sdm'})
            return redirect('tazawwud_dashboard')
        else:
            achat.statut = 'CANCELED'
            achat.save()
            return redirect('tazawwud_dashboard')

    return render(request, 'bibliotheque/tazawwud/simulation_paiement.html', {'achat': achat})


# ── 7. COMPAGNONS & FONCTIONNALITÉS SOCIALES ──

@login_required
def tazawwud_compagnons(request):
    """Page sociale : liste des compagnons, demandes reçues et recherche."""
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    # Compagnons confirmés
    liens = TazawwudCompagnon.objects.filter(
        Q(demandeur=request.user) | Q(ami=request.user),
        statut='ACCEPTE'
    ).select_related('demandeur', 'ami')

    amis = []
    for l in liens:
        autre = l.ami if l.demandeur == request.user else l.demandeur
        autre_prog = TazawwudProgression.objects.filter(user=autre).first()
        amis.append({
            'user': autre,
            'progression': autre_prog,
            'lien_id': l.id,
        })

    # Demandes reçues en attente
    demandes_recues = TazawwudCompagnon.objects.filter(ami=request.user, statut='EN_ATTENTE')

    context = {
        'progression': progression,
        'amis': amis,
        'demandes_recues': demandes_recues,
    }
    return render(request, 'bibliotheque/tazawwud/compagnons.html', context)


@csrf_exempt
@login_required
def api_tazawwud_ajouter_compagnon(request):
    """Envoie une demande de compagnon par nom d'utilisateur."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        cible = User.objects.filter(username__iexact=username).first()

        if not cible:
            return JsonResponse({'status': 'error', 'message': "Utilisateur introuvable."})
        if cible == request.user:
            return JsonResponse({'status': 'error', 'message': "Vous ne pouvez pas vous ajouter vous-même."})

        # Vérifier si lien existe déjà
        existant = TazawwudCompagnon.objects.filter(
            Q(demandeur=request.user, ami=cible) | Q(demandeur=cible, ami=request.user)
        ).first()

        if existant:
            if existant.statut == 'ACCEPTE':
                return JsonResponse({'status': 'error', 'message': "Vous êtes déjà compagnons !"})
            elif existant.statut == 'EN_ATTENTE':
                return JsonResponse({'status': 'error', 'message': "Une demande est déjà en attente."})

        TazawwudCompagnon.objects.create(demandeur=request.user, ami=cible, statut='EN_ATTENTE')
        return JsonResponse({'status': 'success', 'message': f"Demande envoyée à {cible.username} !"})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def api_tazawwud_repondre_compagnon(request):
    """Accepte ou refuse une demande de compagnon."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        demande_id = data.get('demande_id')
        decision = data.get('decision') # 'accepter' ou 'refuser'

        demande = get_object_or_404(TazawwudCompagnon, id=demande_id, ami=request.user)
        if decision == 'accepter':
            demande.statut = 'ACCEPTE'
            demande.save()
        else:
            demande.statut = 'REFUSE'
            demande.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def tazawwud_toggle_visibilite(request):
    """Active ou désactive la visibilité publique du profil et de la progression."""
    if request.method == 'POST':
        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
        progression.est_profil_public = not progression.est_profil_public
        progression.save()
        return JsonResponse({'status': 'success', 'est_public': progression.est_profil_public})
    return JsonResponse({'status': 'error'}, status=405)


@login_required
def tazawwud_classement_hebdo(request):
    """Classement hebdomadaire des élèves avec remise à zéro chaque semaine."""
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
    progression.verifier_semaine_reset()

    top_eleves = TazawwudProgression.objects.filter(
        est_profil_public=True
    ).select_related('user').order_by('-points_semaine')[:30]

    context = {
        'progression': progression,
        'top_eleves': top_eleves,
    }
    return render(request, 'bibliotheque/tazawwud/classement.html', context)


# ── 8. DÉFIS ENTRE COMPAGNONS ──

@login_required
def tazawwud_creer_defi(request):
    """Crée un duel de quiz entre compagnons."""
    module_id = request.POST.get('module_id')
    module = get_object_or_404(TazawwudModule, id=module_id) if module_id else None

    # Sélection de 5 questions aléatoires
    if module:
        q_ids = list(TazawwudQuestion.objects.filter(lecon__module=module).values_list('id', flat=True))
    else:
        q_ids = list(TazawwudQuestion.objects.values_list('id', flat=True))

    selected = random.sample(q_ids, min(len(q_ids), 5))
    code = f"DEF-{uuid.uuid4().hex[:6].upper()}"

    defi = TazawwudDefi.objects.create(
        createur=request.user,
        code=code,
        module=module,
        questions_ids=selected,
        statut='EN_ATTENTE'
    )
    return redirect('tazawwud_jouer_defi', code=code)


@login_required
def tazawwud_jouer_defi(request, code):
    """Joue la partie d'un défi."""
    defi = get_object_or_404(TazawwudDefi, code=code)
    questions = TazawwudQuestion.objects.filter(id__in=defi.questions_ids)
    questions_data = formater_questions_pour_js(questions)

    # Si c'est l'adversaire qui rejoint
    if defi.createur != request.user and not defi.adversaire:
        defi.adversaire = request.user
        defi.save()

    context = {
        'defi': defi,
        'questions_json': json.dumps(questions_data),
        'est_createur': (defi.createur == request.user),
    }
    return render(request, 'bibliotheque/tazawwud/defi_play.html', context)
