"""
Synchronisation de masse TURBO (cryptg + pipeline concurrent + ffmpeg) Telegram -> Cloudinary -> JSON
- Téléchargement + compression intelligente (64kbps mono > 4.5 Mo) + upload Cloudinary EN PARALLÈLE (4 workers)
- Timeout strict sur chaque téléchargement Telegram (zéro blocage possible)
- Phase 1 : Khassidas PDF & Corans PDF (< 9.8 Mo Cloudinary Free, filtrage anti-hors-sujet & anti-doublon prod)
- Phase 2 : 1000+ Audios équilibrés sur tous les canaux actifs, rangés dans les Dossiers & Profils existants
- Sauvegarde incrémentale sécurisée (telegram_checkpoint.json)
"""
import os
import re
import sys
import json
import html
import time
import asyncio
import argparse
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

AUDIO_EXTS = {'.mp3', '.m4a', '.ogg', '.opus', '.wav', '.aac'}

# (username, default_cat, default_profile, audio_quota, pdf_quota)
CHANNEL_PLAN = [
    ('koureloukhaidayi', 'KHASSIDA', 'Kourel Khassida Touba', 420, 95),
    ('KURELSQACIDAS', 'KHASSIDA', 'Kourels Qacidas', 240, 80),
    ('khassidaYiReik', 'KHASSIDA', 'Khassida Yi Rëk', 220, 95),
    ('khassida_monde', 'KHASSIDA', 'Beugkhassida Officiel', 180, 95),
    ('daaraye_s_abdou_rahman_mbacke', 'WAKHTANE', 'Cheikh Abdou Rahmane Mbacké', 140, 180),
    ('linsaliou', 'KHASSIDA', 'Serigne Bassirou Khelcom', 100, 25),
    ('SerigneSamMbaye', 'XAM_XAM', 'Serigne Sam Mbaye', 5, 5),
]

SONS_JSON_PATH = os.path.join(BASE_DIR, 'verified_open_sons.json')
PDFS_JSON_PATH = os.path.join(BASE_DIR, 'verified_open_pdfs.json')
CHECKPOINT_PATH = os.path.join(BASE_DIR, 'telegram_checkpoint.json')

JUNK_PDF_KEYWORDS = [
    'brochure', 'senegal 2050', 'sénégal 2050', 'facture', 'devis',
    'curriculum', 'recrutement', 'offre emploi', 'catalogue prix', 'menu ',
    'formulaire inscription', 'bulletin de notes', 'attestation',
]

BAD_PERFORMERS = {
    '<unknown>', 'unknown', 'my recording', 'recording', 'audio', 'voice',
    'none', 'null', 'artist', 'unknown artist', 'whatsapp', 'telegram',
}


def strip_emojis(text):
    return re.sub(r'[\U00010000-\U0010ffff\u2600-\u27BF]+', ' ', text or '')


def clean_title(raw_name, fallback='Audio Mouride'):
    name = os.path.splitext(os.path.basename(raw_name or ''))[0]
    name = strip_emojis(name)
    name = re.sub(r'_\d{6}_\d{6}$', '', name)
    name = re.sub(r'^(?:nouveaut[eé]|exclu|new)[\s_\-:\.]*', '', name, flags=re.I)
    name = re.sub(r'^[0-9]{1,3}[\s_\-\.]+(?=[A-Za-zÀ-ÿ\u0600-\u06FF])', '', name)
    name = re.sub(r'[_\-]+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip(' .-_')
    return name[:185] or fallback


def slugify(text, maxlen=68):
    s = re.sub(r'[^a-zA-Z0-9_\-]+', '_', strip_emojis(text or ''))
    s = re.sub(r'_+', '_', s).strip('_')
    return (s[:maxlen] or 'sdm_file')


def norm_key(text):
    return re.sub(r'[^a-z0-9\u0600-\u06FF]+', '', (text or '').lower())


def detect_audio_category(title, performer, caption, default_cat):
    hay = f"{title} {performer} {caption}".lower()
    if any(k in hay for k in ['sourate', 'surah', 'coran', 'quran', 'alafasy', 'sudais', 'hussary', 'minshawi', 'jukki']):
        return 'CORAN'
    if any(k in hay for k in ['adhan', 'azan']):
        return 'ADHAN'
    if any(k in hay for k in ['kurel', 'kourel', 'wksm', 'htdkh', 'farij', 'khassida', 'xasida']):
        return 'KHASSIDA'
    if any(k in hay for k in ['serigne sam', 'sam mbaye', 'tazawwud', 'fiqh', 'cours', 'conference', 'xam xam', 'xam-xam', 'hazali', 'ghazali', 'imamul']):
        return 'XAM_XAM'
    if 'tafsir' in hay and 'tafsir diop' not in hay and 's tafsir' not in hay and 'serigne tafsir' not in hay:
        return 'XAM_XAM'
    if any(k in hay for k in ['mbaye diakhate', 'moussa ka', 'wolofal', 'wakhtane', 'jataay', 'ndiguel', 'abdou rahmane', 'abdou rahman']):
        return 'WAKHTANE'
    if any(k in hay for k in ['zikr', 'wird', 'drouss', 'istighfar', 'salatou']):
        return 'ZIKR'
    if any(k in hay for k in ['rajass', 'baye fall', 'bayefall']):
        return 'RAJASS'
    return default_cat


def normalize_profile_name(performer, channel_default, title=''):
    raw = strip_emojis(performer or '').strip()
    if raw.lower() in BAD_PERFORMERS or len(raw) < 3 or raw.isdigit():
        raw = ''
    low = f"{raw} {title}".lower()

    if any(k in low for k in ['nurud darayni', 'nourou darayni', 'nurudaraini', 'nurud daryni', 'nourou daryni']):
        return 'Kourel Nurud Darayni (HT)'
    if 'mafatihul bichri' in low or 'mafatihoul bichri' in low or 'mafatih' in low:
        return 'Kourel Mafatihul Bichri (HT)'
    if 'asnal khadim' in low or 'asna khadim' in low:
        return 'Kourel Asnal Khadim (HT)'
    if 'machrabus chafi' in low or 'machrabou' in low:
        return 'Kourel Machrabus Chafi (HT)'
    if 'tazawudus' in low or 'tazawwud' in low:
        return 'Kourel Tazawudus Sikhar (HT)'
    if 'serigne saliou' in low or 's. saliou' in low or 's saliou' in low:
        return 'Kourel Serigne Saliou Mbacké'
    if 'massamba' in low or 'wksm' in low:
        return 'Wa Keur Serigne Massamba'
    if 'sam mbaye' in low:
        return 'Serigne Sam Mbaye'
    if 'abdou rahmane' in low or 'abdou rahman' in low:
        return 'Cheikh Abdou Rahmane Mbacké'
    if 'bassirou khelcom' in low or 'khelcom' in low or 'khel com' in low:
        return 'Serigne Bassirou Khelcom'
    if 'mbaye diakhate' in low or 'mbaye diakhaté' in low:
        return 'Serigne Mbaye Diakhaté (Wolofal)'
    if 'moussa ka' in low:
        return 'Cheikh Moussa Ka (Wolofal)'
    if 'ibra gueye' in low:
        return 'Serigne Ibra Gueye'
    if 'saliou thiam' in low:
        return 'Serigne Saliou Thiam'
    if 'darou mouhty' in low or 'darou mousty' in low:
        return 'Kourel Wa Darou Mouhty'
    if 'hizbut' in low or 'htdkh' in low or 'kurel ht' in low or 'kourel ht' in low:
        return 'Kourel National Hizbut Tarqiyyah'
    if 'serigne mahib' in low or 'cheikh mahib' in low:
        return 'Kourel Serigne Mahib'
    if 'modou diop' in low or 'moustapha diop' in low or 'tafsir diop' in low or 'youssou ndao' in low:
        return 'Grands Récitateurs Mourides'
    if raw and not raw.startswith('@') and not raw.startswith('http') and len(raw) <= 65:
        return raw
    return channel_default


def detect_pdf_target(title, caption):
    hay = f"{title} {caption}".lower()
    if any(jk in hay for jk in JUNK_PDF_KEYWORDS):
        return 'JUNK', None, ''
    m_jukki = re.search(r'\b(?:jukki|juz|hizb)\s*(\d{1,2})\b', hay)
    if m_jukki:
        num = int(m_jukki.group(1))
        if 1 <= num <= 30:
            return 'CORAN', num, f"Jukki {num} (Juz {num})"
    if any(k in hay for k in ['coran', 'quran', 'kamil', 'kaamil', 'mushaf', 'warsh', 'hafs', 'sourat', 'souraat', 'yaassin', 'yassin', 'al mulk', 'al kahf', 'al waqia']):
        return 'CORAN', None, title[:95]
    return 'KHASSIDA', None, title[:240]


def load_json(path, default):
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return default


def save_json(path, data):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def fetch_existing_prod_khassida_keys():
    keys = set()
    try:
        import requests
        r = requests.get('https://sdm-mourit.onrender.com/collection/khassida/', timeout=20)
        if r.status_code == 200:
            for m in re.findall(r'alt="1re page de ([^"]+)"', r.text):
                keys.add(norm_key(html.unescape(m)))
            for m in re.findall(r'class="item-title"[^>]*>([^<]+)<', r.text):
                keys.add(norm_key(html.unescape(m)))
    except Exception:
        pass
    return keys


def get_ffmpeg_bin():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def compress_audio_if_needed(src_path, ffmpeg_bin, threshold_mb=4.2):
    orig_size = os.path.getsize(src_path)
    if not ffmpeg_bin or orig_size <= threshold_mb * 1024 * 1024:
        return src_path, orig_size, False

    out_path = src_path + '.opt.mp3'
    try:
        cmd = [
            ffmpeg_bin, '-y', '-i', src_path,
            '-vn', '-ac', '1', '-ar', '44100', '-b:a', '64k',
            '-loglevel', 'error', out_path
        ]
        res = subprocess.run(cmd, timeout=75, capture_output=True)
        if res.returncode == 0 and os.path.isfile(out_path):
            new_size = os.path.getsize(out_path)
            if 20_000 < new_size < orig_size * 0.9:
                return out_path, new_size, True
    except Exception:
        pass
    try:
        if os.path.isfile(out_path):
            os.remove(out_path)
    except OSError:
        pass
    return src_path, orig_size, False


async def run_sync(args):
    import cloudinary
    import cloudinary.uploader
    from telethon import TelegramClient
    from telethon.errors import FloodWaitError
    from telethon.tl.types import (
        InputMessagesFilterMusic, InputMessagesFilterDocument,
        DocumentAttributeAudio, DocumentAttributeFilename,
    )

    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True,
    )

    ffmpeg_bin = get_ffmpeg_bin()
    t0 = time.time()
    print(f"Turbo Sync | cryptg actif | FFmpeg: {'OK' if ffmpeg_bin else 'OFF'} | Workers: {args.workers}", flush=True)

    api_id = int(os.environ.get('TELEGRAM_API_ID') or 0)
    api_hash = (os.environ.get('TELEGRAM_API_HASH') or '').strip()
    session_file = os.path.join(BASE_DIR, 'sdm_session')
    client = TelegramClient(session_file, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        print("Session Telegram non autorisée. Lancez python telegram_login.py")
        await client.disconnect()
        sys.exit(2)

    sons_list = load_json(SONS_JSON_PATH, [])
    pdfs_list = load_json(PDFS_JSON_PATH, [])
    checkpoint = load_json(CHECKPOINT_PATH, {'done_msg_keys': [], 'uploaded_bytes': 0})

    done_keys = set(checkpoint.get('done_msg_keys', []))
    existing_son_keys = {norm_key(x.get('titre')) for x in sons_list}
    existing_pdf_keys = {norm_key(x.get('titre')) for x in pdfs_list} | fetch_existing_prod_khassida_keys()
    print(f"Base actuelle : {len(sons_list)} sons, {len(existing_pdf_keys)} PDFs connus.", flush=True)

    max_bytes = int(args.max_gb * (1024 ** 3))
    state = {'uploaded_bytes': 0, 'audios': 0, 'khassidas_pdf': 0, 'corans_pdf': 0, 'skipped': 0, 'errors': 0}

    executor = ThreadPoolExecutor(max_workers=args.workers + 2)
    loop = asyncio.get_running_loop()
    sem = asyncio.Semaphore(args.workers)
    flush_lock = asyncio.Lock()

    async def flush_all():
        async with flush_lock:
            save_json(SONS_JSON_PATH, sons_list)
            save_json(PDFS_JSON_PATH, pdfs_list)
            save_json(CHECKPOINT_PATH, {
                'done_msg_keys': list(done_keys),
                'uploaded_bytes': checkpoint.get('uploaded_bytes', 0) + state['uploaded_bytes'],
            })

    def do_upload_pdf(tmp_path, pub_id):
        return cloudinary.uploader.upload(tmp_path, resource_type='raw', public_id=pub_id, overwrite=False)

    def do_compress_and_upload_audio(tmp_path, folder, slug):
        final_path, final_size, compressed = compress_audio_if_needed(tmp_path, ffmpeg_bin)
        try:
            res = cloudinary.uploader.upload(
                final_path, resource_type='video', folder=folder, public_id=slug, overwrite=False
            )
            return res.get('secure_url') or '', final_size, compressed
        finally:
            if compressed and final_path != tmp_path:
                try:
                    os.remove(final_path)
                except OSError:
                    pass

    active_plan = CHANNEL_PLAN
    if getattr(args, 'channels', None):
        wanted = {c.strip().lower().lstrip('@') for c in args.channels.split(',') if c.strip()}
        active_plan = [row for row in CHANNEL_PLAN if row[0].lower() in wanted]

    # ══════════════════════════════════════════════════════════════
    # PHASE 1 : KHASSIDAS PDF & CORANS PDF (< 9.8 Mo Cloudinary Free)
    # ══════════════════════════════════════════════════════════════
    if args.mode in ('all', 'pdf'):
        print("\n═══════════════ PHASE 1 : KHASSIDAS & CORANS PDF ═══════════════", flush=True)
        for ch_ref, _, _, _, pdf_quota in active_plan:
            if state['uploaded_bytes'] >= max_bytes or (state['khassidas_pdf'] + state['corans_pdf']) >= args.max_pdfs:
                break
            try:
                ent = await client.get_entity(ch_ref)
            except Exception as e:
                print(f"[Canal ignoré @{ch_ref}] {e}", flush=True)
                continue

            # Collecter d'abord les messages candidats (ultra rapide, métadonnées seules!)
            candidates = []
            rem_global = args.max_pdfs - (state['khassidas_pdf'] + state['corans_pdf'])
            target_ch = min(pdf_quota, rem_global)
            async for msg in client.iter_messages(ent, limit=args.scan_depth, filter=InputMessagesFilterDocument):
                if len(candidates) >= target_ch:
                    break
                doc = getattr(msg, 'document', None)
                if not doc:
                    continue
                msg_key = f"pdf:{ch_ref}:{msg.id}"
                if msg_key in done_keys:
                    continue
                size = int(getattr(doc, 'size', 0) or 0)
                if size < 15_000 or size > 9_800_000:
                    continue
                filename = ''
                for a in getattr(doc, 'attributes', []) or []:
                    if isinstance(a, DocumentAttributeFilename):
                        filename = (a.file_name or '').strip()
                mime = (getattr(doc, 'mime_type', '') or '').lower()
                if mime != 'application/pdf' and not filename.lower().endswith('.pdf'):
                    continue
                caption = (msg.message or '').strip()
                raw_t = clean_title(filename, fallback=(caption.splitlines()[0][:100] if caption else f"Khassida {ch_ref} #{msg.id}"))
                p_kind, p_num, p_title = detect_pdf_target(raw_t, caption)
                if p_kind == 'JUNK' or not p_title:
                    done_keys.add(msg_key)
                    continue
                pk = norm_key(p_title)
                if not pk or pk in existing_pdf_keys:
                    done_keys.add(msg_key)
                    state['skipped'] += 1
                    continue
                existing_pdf_keys.add(pk)
                candidates.append((msg, msg_key, size, p_kind, p_num, p_title))

            if not candidates:
                continue
            print(f"▶ PDFs @{ch_ref} : {len(candidates)} nouveaux PDFs uniques à importer...", flush=True)

            async def handle_pdf(item):
                msg, msg_key, size, p_kind, p_num, p_title = item
                if state['uploaded_bytes'] >= max_bytes:
                    return
                async with sem:
                    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                        tmp_path = tmp.name
                    try:
                        await asyncio.wait_for(client.download_media(msg, file=tmp_path), timeout=40)
                        with open(tmp_path, 'rb') as fp:
                            if fp.read(4) != b'%PDF':
                                done_keys.add(msg_key)
                                return
                        sub_dir = 'coran_pdf' if p_kind == 'CORAN' else 'khassidas'
                        pub_id = f"media/{sub_dir}/{slugify(f'tg_{ch_ref}_{msg.id}_{p_title}', 68)}.pdf"
                        res = await loop.run_in_executor(executor, do_upload_pdf, tmp_path, pub_id)
                        sec_url = res.get('secure_url') or ''
                        if sec_url:
                            pdfs_list.append({
                                'kind': p_kind,
                                'titre': p_title,
                                'auteur': 'Cheikh Ahmadou Bamba' if p_kind == 'KHASSIDA' else 'Saint Coran',
                                'numero': p_num,
                                'fichier_pdf': pub_id,
                                'secure_url': sec_url,
                                'source': f"@{ch_ref}",
                            })
                            done_keys.add(msg_key)
                            state['uploaded_bytes'] += os.path.getsize(tmp_path)
                            if p_kind == 'CORAN':
                                state['corans_pdf'] += 1
                            else:
                                state['khassidas_pdf'] += 1
                            tot_p = state['khassidas_pdf'] + state['corans_pdf']
                            print(f"  [PDF #{tot_p:3d} · {p_kind:8s} · {size/1048576:.1f}Mo] {p_title[:58]}", flush=True)
                            if tot_p % 15 == 0:
                                await flush_all()
                    except asyncio.TimeoutError:
                        state['errors'] += 1
                        print(f"  [Timeout PDF] {p_title[:42]}", flush=True)
                    except FloodWaitError as fw:
                        await asyncio.sleep(int(getattr(fw, 'seconds', 8)) + 2)
                    except Exception as e:
                        state['errors'] += 1
                        print(f"  [Err PDF] {p_title[:42]}: {e}", flush=True)
                    finally:
                        try:
                            os.remove(tmp_path)
                        except OSError:
                            pass

            await asyncio.gather(*(handle_pdf(it) for it in candidates))
            await flush_all()

    # ══════════════════════════════════════════════════════════════
    # PHASE 2 : 1000+ AUDIOS MOURIDES EN PARALLÈLE
    # ══════════════════════════════════════════════════════════════
    if args.mode in ('all', 'audio'):
        print("\n═══════════════ PHASE 2 : 1000+ AUDIOS MOURIDES ═══════════════", flush=True)
        for ch_ref, default_cat, default_prof, audio_quota, _ in active_plan:
            if state['uploaded_bytes'] >= max_bytes or state['audios'] >= args.max_audios:
                break
            try:
                ent = await client.get_entity(ch_ref)
            except Exception as e:
                print(f"[Canal ignoré @{ch_ref}] {e}", flush=True)
                continue

            rem_global = args.max_audios - state['audios']
            target_ch = min(audio_quota, rem_global)
            max_dl_bytes = 92_000_000 if ch_ref == 'SerigneSamMbaye' else int(args.max_audio_mb * 1024 * 1024)
            dl_timeout = 120 if ch_ref == 'SerigneSamMbaye' else 45

            # Scanner métadonnées d'abord (instantané!) et trier par taille croissante pour importer un max de pistes rapides!
            raw_candidates = []
            async for msg in client.iter_messages(ent, limit=args.scan_depth, filter=InputMessagesFilterMusic):
                if len(raw_candidates) >= target_ch * 2:
                    break
                doc = getattr(msg, 'document', None)
                if not doc:
                    continue
                msg_key = f"aud:{ch_ref}:{msg.id}"
                if msg_key in done_keys:
                    continue
                size = int(getattr(doc, 'size', 0) or 0)
                if size < 35_000 or size > max_dl_bytes:
                    continue
                title = performer = filename = ''
                for a in getattr(doc, 'attributes', []) or []:
                    if isinstance(a, DocumentAttributeAudio):
                        title = (a.title or '').strip()
                        performer = (a.performer or '').strip()
                    elif isinstance(a, DocumentAttributeFilename):
                        filename = (a.file_name or '').strip()
                caption = (msg.message or '').strip()
                raw_t = title or filename or (caption.splitlines()[0][:120] if caption else f"{default_prof} #{msg.id}")
                final_title = clean_title(raw_t, fallback=f"{default_prof} #{msg.id}")
                sk = norm_key(final_title)
                if not sk or len(sk) < 3 or sk in existing_son_keys:
                    done_keys.add(msg_key)
                    state['skipped'] += 1
                    continue
                existing_son_keys.add(sk)
                ext = os.path.splitext(filename)[1].lower() if filename else '.mp3'
                if ext not in AUDIO_EXTS:
                    ext = '.mp3'
                raw_candidates.append((size, msg, msg_key, final_title, performer, caption, ext))

            # Trier par taille croissante : les MP3 compacts (1-6 Mo) passent en priorité -> vitesse x4 et quota optimal !
            raw_candidates.sort(key=lambda x: x[0])
            candidates = raw_candidates[:target_ch]
            if not candidates:
                continue
            print(f"\n▶ Audios @{ch_ref} : {len(candidates)} pistes sélectionnées (taille {candidates[0][0]/1048576:.1f}–{candidates[-1][0]/1048576:.1f} Mo)...", flush=True)

            async def handle_audio(item):
                size, msg, msg_key, final_title, performer, caption, ext = item
                if state['uploaded_bytes'] >= max_bytes or state['audios'] >= args.max_audios:
                    return
                async with sem:
                    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                        tmp_path = tmp.name
                    try:
                        await asyncio.wait_for(client.download_media(msg, file=tmp_path), timeout=dl_timeout)
                        if os.path.getsize(tmp_path) < 20_000:
                            return
                        cat = detect_audio_category(final_title, performer, caption, default_cat)
                        prof = normalize_profile_name(performer, default_prof, final_title)
                        slug = slugify(f"{ch_ref}_{msg.id}_{final_title}", 72)
                        folder = f"media/audios/telegram/{cat.lower()}"
                        sec_url, up_size, was_comp = await loop.run_in_executor(
                            executor, do_compress_and_upload_audio, tmp_path, folder, slug
                        )
                        if sec_url:
                            sons_list.append({
                                'titre': final_title,
                                'auteur_voix': prof,
                                'categorie': cat,
                                'lien_audio_externe': sec_url,
                            })
                            done_keys.add(msg_key)
                            state['uploaded_bytes'] += up_size
                            state['audios'] += 1
                            tag = f"{size/1048576:.1f}->{up_size/1048576:.1f}Mo" if was_comp else f"{up_size/1048576:.1f}Mo"
                            if state['audios'] <= 15 or state['audios'] % 10 == 0:
                                elapsed = time.time() - t0
                                print(f"  [AUD #{state['audios']:4d} · {cat:8s} · {tag:11s} · {elapsed:5.0f}s] {prof[:24]:24s} | {final_title[:42]}", flush=True)
                            if state['audios'] % 20 == 0:
                                await flush_all()
                    except asyncio.TimeoutError:
                        state['errors'] += 1
                        print(f"  [Timeout AUD] {final_title[:42]} ({size/1048576:.1f}Mo)", flush=True)
                    except FloodWaitError as fw:
                        wait_s = int(getattr(fw, 'seconds', 8)) + 2
                        print(f"  [FloodWait] {wait_s}s", flush=True)
                        await asyncio.sleep(wait_s)
                    except Exception as e:
                        state['errors'] += 1
                        print(f"  [Err AUD] {final_title[:42]}: {e}", flush=True)
                    finally:
                        try:
                            os.remove(tmp_path)
                        except OSError:
                            pass

            await asyncio.gather(*(handle_audio(it) for it in candidates))
            await flush_all()

    await flush_all()
    executor.shutdown(wait=True)
    await client.disconnect()

    elapsed = time.time() - t0
    print("\n═══════════════════ BILAN FINAL TELEGRAM SYNC ═══════════════════", flush=True)
    print(f"  Durée totale                   : {elapsed/60:.1f} min", flush=True)
    print(f"  Nouveaux Audios ajoutés        : {state['audios']} (Total catalogue : {len(sons_list)})", flush=True)
    print(f"  Nouveaux Khassidas PDF ajoutés : {state['khassidas_pdf']}", flush=True)
    print(f"  Nouveaux Corans PDF ajoutés    : {state['corans_pdf']} (Total PDFs JSON : {len(pdfs_list)})", flush=True)
    print(f"  Doublons évités                : {state['skipped']}", flush=True)
    print(f"  Erreurs / Timeouts             : {state['errors']}", flush=True)
    print(f"  Volume Cloudinary uploadé      : {state['uploaded_bytes'] / (1024**3):.2f} Go", flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['all', 'audio', 'pdf'], default='all')
    parser.add_argument('--max-pdfs', type=int, default=350)
    parser.add_argument('--max-audios', type=int, default=1050)
    parser.add_argument('--scan-depth', type=int, default=2000)
    parser.add_argument('--max-gb', type=float, default=5.8)
    parser.add_argument('--max-audio-mb', type=float, default=14.0)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--channels', type=str, default='')
    args = parser.parse_args()
    asyncio.run(run_sync(args))
