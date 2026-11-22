"""
Connexion unique & sécurisée à votre compte Telegram (reste 100% local sur ce PC).
Crée le fichier ignoré par Git : sdm_session.session, puis affiche l'inventaire
des audios et PDFs disponibles dans vos 7 canaux Mourides.
"""
import os
import asyncio
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

API_ID = int(os.environ.get('TELEGRAM_API_ID') or 0)
API_HASH = (os.environ.get('TELEGRAM_API_HASH') or '').strip()

DEFAULT_CHANNELS = [
    'linsaliou',
    'daaraye_s_abdou_rahman_mbacke',
    'khassida_monde',
    'koureloukhaidayi',
    'SerigneSamMbaye',
    'cheikhahmadoubousso',
    'khassidaYiReik',
]


async def main():
    if not API_ID or not API_HASH:
        print("Erreur : TELEGRAM_API_ID ou TELEGRAM_API_HASH manquant dans .env")
        return

    from telethon import TelegramClient
    from telethon.tl.types import InputMessagesFilterMusic, InputMessagesFilterDocument

    session_file = os.path.join(BASE_DIR, 'sdm_session')
    client = TelegramClient(session_file, API_ID, API_HASH)

    print("═══ Connexion Telegram API (SDM Mouride) ═══")
    print("Entrez votre numéro Telegram avec indicatif (ex: +22177xxxxxxx),")
    print("puis le code reçu dans votre application Telegram.")
    await client.start()

    me = await client.get_me()
    print(f"\n✅ Connecté avec succès : {getattr(me, 'first_name', '')} (@{getattr(me, 'username', '')})")
    print("\n═══ Inventaire des 7 canaux Telegram ═══")
    total_audio = 0
    total_docs = 0
    for ch in DEFAULT_CHANNELS:
        try:
            ent = await client.get_entity(ch)
            title = getattr(ent, 'title', ch)
            music = await client.get_messages(ent, limit=1, filter=InputMessagesFilterMusic)
            docs = await client.get_messages(ent, limit=1, filter=InputMessagesFilterDocument)
            total_audio += music.total
            total_docs += docs.total
            print(f"  @{ch:30s} | {title[:30]:30s} | Audios: {music.total:5d} | Docs/PDF: {docs.total:5d}")
        except Exception as e:
            print(f"  @{ch:30s} | Accès impossible : {e}")

    print(f"\nTOTAL DÉTECTÉ : {total_audio} audios + {total_docs} documents/PDFs.")
    print("Session enregistrée dans sdm_session.session. Vous pouvez revenir dans le chat !")
    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
