"""
Récupère tous les posts (textes + images) de @MedisbuOfficiel via Telethon :
- Extrait les textes/rappels/enseignements propres (nettoyés des liens t.me/@MedisbuOfficiel)
- Télécharge les images des posts dans telegram_downloads_tmp/medisbu_raw/ pour re-création propre SDM
- Génère des versions retravaillées propres estampillées SDM (en réutilisant les 6 décors Nano Banana SDM)
  et enregistre tous les rappels quotidiens dans daily_rappels_sdm.json pour rotation automatique chaque jour !
"""
import os
import re
import json
import asyncio
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

RAPPELS_JSON_PATH = os.path.join(BASE_DIR, 'daily_rappels_sdm.json')
RAW_IMG_DIR = os.path.join(BASE_DIR, 'telegram_downloads_tmp', 'medisbu_raw')

SDM_THEMES = [
    'sdm_touba_emerald.jpg',
    'sdm_parchemin_royal.jpg',
    'sdm_nuit_medine.jpg',
    'sdm_kaaba_or.jpg',
    'sdm_firdaws_jade.jpg',
    'sdm_sufi_dawn.jpg',
]


def clean_post_text(raw):
    if not raw:
        return ''
    txt = raw
    # Retirer mentions/liens promotionnels tiers (Medisbu / Telegram / WhatsApp / numéros)
    txt = re.sub(r'https?://\S+', '', txt)
    txt = re.sub(r't\.me/\S+', '', txt, flags=re.I)
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
    txt = re.sub(r'(?i)\bmedisbu\b[^\n]*', '', txt)
    txt = re.sub(r'(?i)(?:rejoignez|abonnez|suivez|partagez|contact|whatsapp|t[eé]l[eé]gram)[^\n]*', '', txt)
    txt = re.sub(r'[\U00010000-\U0010ffff]+', '', txt)
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    cleaned = '\n'.join(lines).strip()
    return cleaned


def split_arabic_and_french(text):
    """Sépare proprement le texte arabe et le texte français/wolof d'un post."""
    ar_lines = []
    fr_lines = []
    for ln in text.splitlines():
        ar_chars = len(re.findall(r'[\u0600-\u06FF]', ln))
        if ar_chars > len(ln) * 0.35:
            ar_lines.append(ln)
        else:
            fr_lines.append(ln)
    return '\n'.join(ar_lines).strip(), '\n'.join(fr_lines).strip()


def detect_category_badge(text):
    low = text.lower()
    if any(k in low for k in ['sourate', 'verset', 'coran', 'allah dit', 'قال الله']):
        return 'Verset & Méditation'
    if any(k in low for k in ['hadith', 'prophète', 'rassoul', 'envoyé d\'allah', 'قال رسول']):
        return 'Hadith Prophétique'
    if any(k in low for k in ['serigne touba', 'cheikh ahmadou bamba', 'khadim', 'khassida', 'boroom touba', 'mbacké', 'xadiim']):
        return 'Sagesse de Cheikh Ahmadou Bamba'
    return 'Rappel Spirituel SDM'


async def run():
    from telethon import TelegramClient

    os.makedirs(RAW_IMG_DIR, exist_ok=True)
    api_id = int(os.environ['TELEGRAM_API_ID'])
    api_hash = os.environ['TELEGRAM_API_HASH']

    client = TelegramClient(os.path.join(BASE_DIR, 'sdm_session'), api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        print("Erreur : session non autorisée.")
        await client.disconnect()
        return

    ent = await client.get_entity('MedisbuOfficiel')
    print(f"Scan de @MedisbuOfficiel ({getattr(ent, 'title', '')})...", flush=True)

    rappels = []
    seen_texts = set()
    img_count = 0
    post_count = 0

    async for msg in client.iter_messages(ent, limit=500):
        post_count += 1
        raw_txt = (msg.message or '').strip()
        cleaned = clean_post_text(raw_txt)

        has_photo = bool(msg.photo)
        raw_img_rel = ''
        if has_photo and img_count < 80:
            try:
                fname = f"medisbu_{msg.id}.jpg"
                fpath = os.path.join(RAW_IMG_DIR, fname)
                if not os.path.isfile(fpath):
                    await asyncio.wait_for(client.download_media(msg, file=fpath), timeout=20)
                if os.path.isfile(fpath) and os.path.getsize(fpath) > 5_000:
                    raw_img_rel = fname
                    img_count += 1
            except Exception as e:
                print(f"  [Err img #{msg.id}] {e}")

        if len(cleaned) >= 28:
            key = re.sub(r'\W+', '', cleaned.lower())[:90]
            if key not in seen_texts:
                seen_texts.add(key)
                ar, fr = split_arabic_and_french(cleaned)
                badge = detect_category_badge(cleaned)
                theme = SDM_THEMES[len(rappels) % len(SDM_THEMES)]
                rappels.append({
                    'id': f"sdm_rappel_{msg.id}",
                    'msg_id': msg.id,
                    'date_post': msg.date.strftime('%Y-%m-%d') if msg.date else '',
                    'badge': badge,
                    'arabe': ar[:600],
                    'texte': (fr or cleaned)[:750],
                    'source': 'SDM · Enseignements & Sagesse',
                    'theme_image': f"/static/images/sdm_rappels/{theme}",
                    'has_source_photo': bool(raw_img_rel),
                    'raw_photo': raw_img_rel,
                })

    await client.disconnect()

    with open(RAPPELS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(rappels, f, ensure_ascii=False, indent=2)

    print(f"\n=== BILAN @MedisbuOfficiel ===")
    print(f"  Posts scannés       : {post_count}")
    print(f"  Images téléchargées : {img_count} (dans telegram_downloads_tmp/medisbu_raw/)")
    print(f"  Rappels uniques SDM : {len(rappels)} (enregistrés dans daily_rappels_sdm.json)")


if __name__ == '__main__':
    asyncio.run(run())
