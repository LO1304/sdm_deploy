import os
import re
import json
import tempfile
import asyncio
from django.core.management.base import BaseCommand, CommandError
from bibliotheque.models import Son

AUDIO_EXTS = {'.mp3', '.m4a', '.ogg', '.opus', '.wav', '.aac', '.flac'}


def clean_audio_title(raw_name):
    name = os.path.splitext(os.path.basename(raw_name))[0]
    name = re.sub(r'^[0-9]+[\s_\-\.]+', '', name)
    name = re.sub(r'[_\-]+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:200] or "Audio Mouride"


class Command(BaseCommand):
    help = (
        "Importe en masse des audios (Khassidas, Coran, Wakhtane, Zikr...) depuis un groupe/canal Telegram "
        "(soit via un dossier d'export Telegram Desktop --dossier, soit directement via Telethon --channel) "
        "et les héberge de manière permanente sur Cloudinary + Supabase."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dossier',
            type=str,
            help="Chemin d'un dossier contenant les audios (ex: export Telegram Desktop)",
        )
        parser.add_argument(
            '--channel',
            type=str,
            help="Lien ou @nom du canal/groupe Telegram (ex: https://t.me/koureloukhaidayi)",
        )
        parser.add_argument(
            '--categorie',
            type=str,
            default='KHASSIDA',
            choices=[c[0] for c in Son.CATEGORIES],
            help="Catégorie cible dans la base SDM (KHASSIDA, CORAN, WAKHTANE, ZIKR, XAM_XAM, RAJASS, ADHAN)",
        )
        parser.add_argument(
            '--auteur',
            type=str,
            default='',
            help="Auteur / Kourel par défaut si non précisé dans les métadonnées",
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help="Nombre maximum d'audios à importer par exécution (défaut: 100)",
        )
        parser.add_argument(
            '--api-id',
            type=int,
            default=0,
            help="Telegram API ID (ou variable d'environnement TELEGRAM_API_ID)",
        )
        parser.add_argument(
            '--api-hash',
            type=str,
            default='',
            help="Telegram API HASH (ou variable d'environnement TELEGRAM_API_HASH)",
        )

    def handle(self, *args, **options):
        dossier = options.get('dossier')
        channel = options.get('channel')
        categorie = options['categorie']
        default_auteur = (options.get('auteur') or '').strip()
        limit = options['limit']

        if not dossier and not channel:
            raise CommandError("Spécifiez --dossier <chemin> OU --channel <lien_telegram>.")

        if dossier:
            self._import_from_folder(dossier, categorie, default_auteur, limit)
        elif channel:
            api_id = options['api_id'] or int(os.environ.get('TELEGRAM_API_ID') or 0)
            api_hash = options['api_hash'] or os.environ.get('TELEGRAM_API_HASH', '').strip()
            if not api_id or not api_hash:
                raise CommandError(
                    "Pour importer directement depuis un lien Telegram, fournissez --api-id et --api-hash "
                    "(ou les variables TELEGRAM_API_ID / TELEGRAM_API_HASH obtenues sur https://my.telegram.org), "
                    "OU utilisez --dossier avec un export Telegram Desktop."
                )
            asyncio.run(self._import_from_channel(channel, categorie, default_auteur, limit, api_id, api_hash))

    def _upload_and_save(self, file_path, titre, auteur, categorie):
        import cloudinary.uploader

        if Son.objects.filter(titre__iexact=titre).exists():
            self.stdout.write(f"  [Ignoré - déjà présent] {titre}")
            return False

        folder = f"media/audios/telegram/{categorie.lower()}"
        res = cloudinary.uploader.upload(
            file_path,
            resource_type='video',
            folder=folder,
            use_filename=True,
            unique_filename=True,
        )
        secure_url = res.get('secure_url')
        if not secure_url:
            self.stderr.write(f"  [Erreur Cloudinary] Aucun lien retourné pour {titre}")
            return False

        Son.objects.create(
            titre=titre[:200],
            auteur_voix=(auteur or 'Kourel Mouride')[:150],
            categorie=categorie,
            lien_audio_externe=secure_url,
        )
        self.stdout.write(self.style.SUCCESS(f"  [OK] {titre} ({auteur or categorie})"))
        return True

    def _import_from_folder(self, dossier, categorie, default_auteur, limit):
        if not os.path.isdir(dossier):
            raise CommandError(f"Dossier introuvable : {dossier}")

        # Si result.json (export Telegram Desktop) existe, lire les métadonnées (performer / title / caption)
        meta_by_relpath = {}
        result_json = os.path.join(dossier, 'result.json')
        if os.path.isfile(result_json):
            try:
                with open(result_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for msg in data.get('messages', []):
                    rel = msg.get('file')
                    if rel:
                        meta_by_relpath[os.path.normpath(rel)] = {
                            'title': msg.get('title') or '',
                            'performer': msg.get('performer') or '',
                        }
            except Exception:
                pass

        audio_files = []
        for root, _, files in os.walk(dossier):
            for fname in sorted(files):
                ext = os.path.splitext(fname)[1].lower()
                if ext in AUDIO_EXTS:
                    audio_files.append(os.path.join(root, fname))

        self.stdout.write(f"Trouvé {len(audio_files)} fichier(s) audio dans {dossier}.")
        imported = 0
        for fpath in audio_files:
            if imported >= limit:
                break
            rel = os.path.normpath(os.path.relpath(fpath, dossier))
            meta = meta_by_relpath.get(rel, {})
            titre = (meta.get('title') or '').strip() or clean_audio_title(fpath)
            auteur = (meta.get('performer') or '').strip() or default_auteur or 'Kourel Khassida'
            try:
                if self._upload_and_save(fpath, titre, auteur, categorie):
                    imported += 1
            except Exception as e:
                self.stderr.write(f"  [Erreur] {fpath}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Import terminé : {imported} nouveau(x) son(s) ajouté(s)."))

    async def _import_from_channel(self, channel_link, categorie, default_auteur, limit, api_id, api_hash):
        try:
            from telethon import TelegramClient
            from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeFilename
        except ImportError:
            raise CommandError("Installez telethon d'abord : pip install telethon")

        m = re.search(r'(?:t\.me/|telegram\.me/|@)([A-Za-z0-9_]+)', channel_link)
        entity_name = m.group(1) if m else channel_link.strip()

        session_path = os.path.join(os.path.dirname(__file__), 'sdm_telegram_admin')
        client = TelegramClient(session_path, api_id, api_hash)
        await client.start()

        self.stdout.write(f"Connexion Telegram réussie. Scan du canal @{entity_name}...")
        imported = 0
        async for message in client.iter_messages(entity_name, limit=limit * 3):
            if imported >= limit:
                break
            if not message.media or not getattr(message, 'document', None):
                continue

            doc = message.document
            mime = (getattr(doc, 'mime_type', '') or '').lower()
            is_audio = mime.startswith('audio/')
            title = ''
            performer = ''
            filename = ''
            for attr in getattr(doc, 'attributes', []) or []:
                if isinstance(attr, DocumentAttributeAudio):
                    is_audio = True
                    title = (attr.title or '').strip()
                    performer = (attr.performer or '').strip()
                elif isinstance(attr, DocumentAttributeFilename):
                    filename = (attr.file_name or '').strip()
                    if os.path.splitext(filename)[1].lower() in AUDIO_EXTS:
                        is_audio = True

            if not is_audio:
                continue

            final_title = title or (clean_audio_title(filename) if filename else f"Audio @{entity_name} #{message.id}")
            final_auteur = performer or default_auteur or f"Kourel @{entity_name}"

            if Son.objects.filter(titre__iexact=final_title).exists():
                self.stdout.write(f"  [Ignoré - déjà présent] {final_title}")
                continue

            ext = os.path.splitext(filename)[1].lower() if filename else '.mp3'
            if ext not in AUDIO_EXTS:
                ext = '.mp3'

            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                tmp_path = tmp.name

            try:
                self.stdout.write(f"  Téléchargement depuis Telegram : {final_title}...")
                await client.download_media(message, file=tmp_path)
                if self._upload_and_save(tmp_path, final_title, final_auteur, categorie):
                    imported += 1
            except Exception as e:
                self.stderr.write(f"  [Erreur] {final_title}: {e}")
            finally:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

        await client.disconnect()
        self.stdout.write(self.style.SUCCESS(f"Import Telegram terminé : {imported} nouveau(x) son(s) ajouté(s)."))
