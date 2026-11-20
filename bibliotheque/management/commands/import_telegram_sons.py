import os
import re
import json
import time
import shutil
import asyncio
import tempfile
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
from bibliotheque.models import Son, Khassida, Coran

AUDIO_EXTS = {'.mp3', '.m4a', '.ogg', '.opus', '.wav', '.aac', '.flac'}
PDF_EXTS = {'.pdf'}


def clean_title(raw_name, fallback='Document Mouride'):
    name = os.path.splitext(os.path.basename(raw_name or ''))[0]
    name = re.sub(r'^[0-9]+[\s_\-\.]+', '', name)
    name = re.sub(r'[_\-]+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:200] or fallback


def detect_audio_category(title, performer, caption, default_cat='KHASSIDA'):
    hay = f"{title} {performer} {caption}".lower()
    if any(k in hay for k in ['sourate', 'surah', 'coran', 'quran', 'jukki', 'juz', 'alafasy', 'sudais', 'hussary', 'minshawi']):
        return 'CORAN'
    if any(k in hay for k in ['adhan', 'azan', 'appel a la priere']):
        return 'ADHAN'
    if any(k in hay for k in ['wolofal', 'wakhtane', 'mbaye diakhate', 'moussa ka', 'ndenkaane', 'serigne abdou rahmane']):
        return 'WAKHTANE'
    if any(k in hay for k in ['xam xam', 'xam-xam', 'tafsir', 'tazawwud', 'fiqh', 'cours', 'conference', 'explication']):
        return 'XAM_XAM'
    if any(k in hay for k in ['zikr', 'wird', 'istighfar', 'salatou', 'drouss']):
        return 'ZIKR'
    if any(k in hay for k in ['rajass', 'sam fall', 'bayefall', 'baye fall']):
        return 'RAJASS'
    return default_cat


def detect_pdf_target(title, caption):
    """Détermine si un PDF Telegram est un Coran (Jukki/Kamil/Mushaf) ou un Khassida."""
    hay = f"{title} {caption}".lower()
    m_jukki = re.search(r'\b(?:jukki|juz|hizb)\s*(\d{1,2})\b', hay)
    if m_jukki:
        num = int(m_jukki.group(1))
        if 1 <= num <= 30:
            return 'CORAN', num, f"Jukki {num} (Juz {num})"
    if any(k in hay for k in ['coran', 'quran', 'kamil', 'kaamil', 'mushaf', 'warsh', 'hafs']):
        return 'CORAN', None, title[:100]
    return 'KHASSIDA', None, title[:255]


class Command(BaseCommand):
    help = (
        "Importe en masse (1000+ fichiers) des Audios (Khassidas, Coran, Wakhtane, Xam Xam, Zikr...), "
        "Khassidas PDF et Corans PDF depuis un ou plusieurs groupes/canaux Telegram via Telethon (--channel) "
        "ou un export local (--dossier), avec classement automatique dans les Dossiers & Profils SDM."
    )

    def add_arguments(self, parser):
        parser.add_argument('--dossier', type=str, help="Chemin d'un dossier local (ex: export Telegram Desktop)")
        parser.add_argument(
            '--channel',
            nargs='+',
            type=str,
            help="Un ou plusieurs liens ou @noms de canaux/groupes Telegram (ex: https://t.me/koureloukhaidayi)",
        )
        parser.add_argument(
            '--type',
            type=str,
            default='all',
            choices=['all', 'audio', 'pdf'],
            help="Type de médias à récupérer : all (Audios + PDFs), audio uniquement, ou pdf uniquement",
        )
        parser.add_argument(
            '--categorie',
            type=str,
            default='KHASSIDA',
            choices=[c[0] for c in Son.CATEGORIES],
            help="Catégorie audio par défaut si la détection automatique ne trouve pas plus précis",
        )
        parser.add_argument('--auto-cat', action='store_true', default=True, help="Classer automatiquement chaque audio dans le bon dossier")
        parser.add_argument('--auteur', type=str, default='', help="Profil Kourel / Maître par défaut")
        parser.add_argument('--limit', type=int, default=1500, help="Nombre max de fichiers à importer (défaut: 1500)")
        parser.add_argument('--api-id', type=int, default=0, help="Telegram API ID (ou env TELEGRAM_API_ID)")
        parser.add_argument('--api-hash', type=str, default='', help="Telegram API HASH (ou env TELEGRAM_API_HASH)")
        parser.add_argument('--local', action='store_true', help="Forcer l'enregistrement local sans Cloudinary")
        parser.add_argument('--sync-json', action='store_true', default=True, help="Ajouter les audios Cloudinary dans verified_open_sons.json")

    def handle(self, *args, **options):
        dossier = options.get('dossier')
        channels = options.get('channel') or []
        self.media_type = options['type']
        self.default_cat = options['categorie']
        self.auto_cat = bool(options.get('auto_cat', True))
        self.default_auteur = (options.get('auteur') or '').strip()
        self.limit = options['limit']
        self.force_local = bool(options.get('local'))
        self.sync_json = bool(options.get('sync_json', True))
        self.stats = {'audio': 0, 'khassida_pdf': 0, 'coran_pdf': 0, 'skipped': 0, 'errors': 0}

        if not dossier and not channels:
            raise CommandError("Spécifiez --dossier <chemin> OU --channel <lien_telegram ...>.")

        if dossier:
            self._import_from_folder(dossier)
        elif channels:
            api_id = options['api_id'] or int(os.environ.get('TELEGRAM_API_ID') or 0)
            api_hash = options['api_hash'] or os.environ.get('TELEGRAM_API_HASH', '').strip()
            if not api_id or not api_hash:
                raise CommandError(
                    "Fournissez --api-id et --api-hash (ou les variables TELEGRAM_API_ID / TELEGRAM_API_HASH "
                    "obtenues sur https://my.telegram.org), OU utilisez --dossier avec un export Telegram Desktop."
                )
            asyncio.run(self._import_from_channels(channels, api_id, api_hash))

        self.stdout.write(self.style.SUCCESS(
            f"\n=== BILAN IMPORT TELEGRAM ===\n"
            f"  Audios ajoutés       : {self.stats['audio']}\n"
            f"  Khassidas PDF ajoutés: {self.stats['khassida_pdf']}\n"
            f"  Corans PDF ajoutés   : {self.stats['coran_pdf']}\n"
            f"  Ignorés (doublons)   : {self.stats['skipped']}\n"
            f"  Erreurs              : {self.stats['errors']}"
        ))

    def _append_to_verified_json(self, titre, auteur, categorie, secure_url):
        if not self.sync_json or not secure_url.startswith('https://'):
            return
        json_path = os.path.join(settings.BASE_DIR, 'verified_open_sons.json')
        try:
            data = []
            if os.path.isfile(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            if any(x.get('lien_audio_externe') == secure_url for x in data):
                return
            data.append({
                'titre': titre[:200],
                'auteur_voix': auteur[:150],
                'categorie': categorie,
                'lien_audio_externe': secure_url,
            })
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.stderr.write(f"  [Attention sync JSON] {e}")

    def _upload_and_save_audio(self, file_path, titre, auteur, categorie):
        if Son.objects.filter(titre__iexact=titre).exists():
            self.stats['skipped'] += 1
            return False

        secure_url = ''
        if not self.force_local:
            try:
                import cloudinary.uploader
                folder = f"media/audios/telegram/{categorie.lower()}"
                res = cloudinary.uploader.upload(
                    file_path,
                    resource_type='video',
                    folder=folder,
                    use_filename=True,
                    unique_filename=True,
                )
                secure_url = res.get('secure_url') or ''
            except Exception as e:
                self.stderr.write(f"  [Cloudinary audio indisponible, bascule locale] {e}")
                secure_url = ''

        if not secure_url:
            ext = os.path.splitext(file_path)[1].lower() or '.mp3'
            local_dir = os.path.join(settings.BASE_DIR, 'static', 'audios_locaux', categorie.lower())
            os.makedirs(local_dir, exist_ok=True)
            safe_slug = re.sub(r'[^a-zA-Z0-9_\-]+', '_', titre)[:70] or 'audio_sdm'
            local_fname = f"{safe_slug}{ext}"
            shutil.copy2(file_path, os.path.join(local_dir, local_fname))
            secure_url = f"/static/audios_locaux/{categorie.lower()}/{local_fname}"

        final_auteur = (auteur or 'Kourel Mouride')[:150]
        Son.objects.create(
            titre=titre[:200],
            auteur_voix=final_auteur,
            categorie=categorie,
            lien_audio_externe=secure_url,
        )
        self._append_to_verified_json(titre, final_auteur, categorie, secure_url)
        self.stats['audio'] += 1
        mode_lbl = 'LOCAL' if secure_url.startswith('/static/') else 'CLOUDINARY'
        self.stdout.write(self.style.SUCCESS(f"  [AUDIO {mode_lbl} · {categorie}] {titre} — {final_auteur}"))
        return True

    def _upload_and_save_pdf(self, file_path, raw_title, caption='', auteur=''):
        target, numero, clean_t = detect_pdf_target(raw_title, caption)
        safe_fname = (re.sub(r'[^a-zA-Z0-9_\-]+', '_', clean_t)[:70] or 'document_sdm') + '.pdf'

        if target == 'CORAN':
            if numero and Coran.objects.filter(numero=numero).exists():
                self.stats['skipped'] += 1
                return False
            if Coran.objects.filter(titre__iexact=clean_t).exists():
                self.stats['skipped'] += 1
                return False
            obj = Coran(titre=clean_t[:100], numero=numero, est_premium=False)
            with open(file_path, 'rb') as fp:
                obj.fichier_pdf.save(safe_fname, File(fp), save=True)
            self.stats['coran_pdf'] += 1
            self.stdout.write(self.style.SUCCESS(f"  [CORAN PDF] {obj.titre}"))
            return True

        if Khassida.objects.filter(titre__iexact=clean_t).exists():
            self.stats['skipped'] += 1
            return False
        obj = Khassida(
            titre=clean_t[:255],
            auteur=(auteur or 'Cheikh Ahmadou Bamba')[:255],
            est_premium=False,
        )
        with open(file_path, 'rb') as fp:
            obj.fichier_pdf.save(safe_fname, File(fp), save=True)
        self.stats['khassida_pdf'] += 1
        self.stdout.write(self.style.SUCCESS(f"  [KHASSIDA PDF] {obj.titre}"))
        return True

    def _import_from_folder(self, dossier):
        if not os.path.isdir(dossier):
            raise CommandError(f"Dossier introuvable : {dossier}")

        meta_by_relpath = {}
        result_json = os.path.join(dossier, 'result.json')
        if os.path.isfile(result_json):
            try:
                with open(result_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for msg in data.get('messages', []):
                    rel = msg.get('file')
                    if rel:
                        txt = msg.get('text', '')
                        if isinstance(txt, list):
                            txt = ' '.join(x.get('text', '') if isinstance(x, dict) else str(x) for x in txt)
                        meta_by_relpath[os.path.normpath(rel)] = {
                            'title': msg.get('title') or '',
                            'performer': msg.get('performer') or '',
                            'caption': str(txt or ''),
                        }
            except Exception:
                pass

        found_files = []
        for root, _, files in os.walk(dossier):
            for fname in sorted(files):
                ext = os.path.splitext(fname)[1].lower()
                if (self.media_type in ('all', 'audio') and ext in AUDIO_EXTS) or (
                    self.media_type in ('all', 'pdf') and ext in PDF_EXTS
                ):
                    found_files.append(os.path.join(root, fname))

        self.stdout.write(f"Trouvé {len(found_files)} fichier(s) dans {dossier}.")
        done = 0
        for fpath in found_files:
            if done >= self.limit:
                break
            ext = os.path.splitext(fpath)[1].lower()
            rel = os.path.normpath(os.path.relpath(fpath, dossier))
            meta = meta_by_relpath.get(rel, {})
            titre = (meta.get('title') or '').strip() or clean_title(fpath)
            auteur = (meta.get('performer') or '').strip() or self.default_auteur
            caption = meta.get('caption') or ''
            try:
                if ext in AUDIO_EXTS:
                    cat = detect_audio_category(titre, auteur, caption, self.default_cat) if self.auto_cat else self.default_cat
                    if self._upload_and_save_audio(fpath, titre, auteur or 'Kourel Khassida', cat):
                        done += 1
                elif ext in PDF_EXTS:
                    if self._upload_and_save_pdf(fpath, titre, caption, auteur):
                        done += 1
            except Exception as e:
                self.stats['errors'] += 1
                self.stderr.write(f"  [Erreur] {fpath}: {e}")

    async def _import_from_channels(self, channel_links, api_id, api_hash):
        try:
            from telethon import TelegramClient
            from telethon.errors import FloodWaitError
            from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeFilename
        except ImportError:
            raise CommandError("Installez telethon d'abord : pip install telethon")

        session_path = os.path.join(os.path.dirname(__file__), 'sdm_telegram_admin')
        client = TelegramClient(session_path, api_id, api_hash)
        await client.start()
        self.stdout.write(self.style.SUCCESS("Connexion Telegram API réussie !"))

        total_done = 0
        for channel_link in channel_links:
            if total_done >= self.limit:
                break
            m = re.search(r'(?:t\.me/|telegram\.me/|@)([A-Za-z0-9_+]+)', channel_link)
            entity_ref = channel_link.strip() if ('/+' in channel_link or 'joinchat' in channel_link) else (m.group(1) if m else channel_link.strip())

            self.stdout.write(f"\n--- Scan du canal/groupe : {entity_ref} ---")
            try:
                entity = await client.get_entity(entity_ref)
                channel_title = getattr(entity, 'title', None) or str(entity_ref)
            except Exception as e:
                self.stderr.write(f"  [Impossible d'accéder à {entity_ref}] {e}")
                continue

            async for message in client.iter_messages(entity, limit=None):
                if total_done >= self.limit:
                    break
                if not message.media or not getattr(message, 'document', None):
                    continue

                doc = message.document
                mime = (getattr(doc, 'mime_type', '') or '').lower()
                is_audio = mime.startswith('audio/')
                is_pdf = (mime == 'application/pdf')
                title, performer, filename = '', '', ''

                for attr in getattr(doc, 'attributes', []) or []:
                    if isinstance(attr, DocumentAttributeAudio):
                        is_audio = True
                        title = (attr.title or '').strip()
                        performer = (attr.performer or '').strip()
                    elif isinstance(attr, DocumentAttributeFilename):
                        filename = (attr.file_name or '').strip()
                        ext_f = os.path.splitext(filename)[1].lower()
                        if ext_f in AUDIO_EXTS:
                            is_audio = True
                        elif ext_f in PDF_EXTS:
                            is_pdf = True

                if is_audio and self.media_type not in ('all', 'audio'):
                    continue
                if is_pdf and self.media_type not in ('all', 'pdf'):
                    continue
                if not is_audio and not is_pdf:
                    continue

                caption = (message.message or '').strip()
                final_title = title or (clean_title(filename) if filename else (caption.splitlines()[0][:120] if caption else f"{channel_title} #{message.id}"))
                final_auteur = performer or self.default_auteur or channel_title

                # Pré-vérification doublon avant téléchargement Telegram (gain énorme de temps/bande passante)
                if is_audio and Son.objects.filter(titre__iexact=final_title).exists():
                    self.stats['skipped'] += 1
                    continue
                if is_pdf:
                    t_kind, t_num, t_clean = detect_pdf_target(final_title, caption)
                    if t_kind == 'CORAN' and ((t_num and Coran.objects.filter(numero=t_num).exists()) or Coran.objects.filter(titre__iexact=t_clean).exists()):
                        self.stats['skipped'] += 1
                        continue
                    if t_kind == 'KHASSIDA' and Khassida.objects.filter(titre__iexact=t_clean).exists():
                        self.stats['skipped'] += 1
                        continue

                ext = os.path.splitext(filename)[1].lower() if filename else ('.pdf' if is_pdf else '.mp3')
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                    tmp_path = tmp.name

                try:
                    await client.download_media(message, file=tmp_path)
                    if is_audio:
                        cat = detect_audio_category(final_title, final_auteur, caption, self.default_cat) if self.auto_cat else self.default_cat
                        if self._upload_and_save_audio(tmp_path, final_title, final_auteur, cat):
                            total_done += 1
                    elif is_pdf:
                        if self._upload_and_save_pdf(tmp_path, final_title, caption, final_auteur):
                            total_done += 1
                except FloodWaitError as fw:
                    wait_s = int(getattr(fw, 'seconds', 10)) + 2
                    self.stderr.write(f"  [Telegram FloodWait] Pause automatique {wait_s}s...")
                    await asyncio.sleep(wait_s)
                except Exception as e:
                    self.stats['errors'] += 1
                    self.stderr.write(f"  [Erreur] {final_title}: {e}")
                finally:
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass

        await client.disconnect()
