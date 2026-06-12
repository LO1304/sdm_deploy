import os
import re
import json
import io
import urllib.request
import urllib.parse
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from bibliotheque.models import Khassida, Coran

MAX_SIZE = 10 * 1024 * 1024  # 10 Mo (limite Cloudinary)


def compress_pdf(pdf_bytes, target_size=MAX_SIZE):
    """Compresse un PDF pour qu'il passe sous la limite de taille en compressant aussi les images."""
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Suppression des métadonnées inutiles
    writer.add_metadata({})

    # Compression des flux internes et des images
    for page in writer.pages:
        try:
            page.compress_content_streams()
        except Exception:
            pass
        try:
            for img in page.images:
                try:
                    # Compression agressive de l'image intégrée (JPEG qualité 30)
                    img.replace(img.image, quality=30)
                except Exception:
                    pass
        except Exception:
            pass

    # Suppression des doublons
    try:
        writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    except Exception:
        try:
            writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
        except Exception:
            pass

    output = io.BytesIO()
    writer.write(output)
    compressed = output.getvalue()

    return compressed


class Command(BaseCommand):
    help = 'Scrape khassidaenpdf.net and import PDFs into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Limiter le nombre de Khassidas a importer (pour les tests)',
        )

    def handle(self, *args, **options):
        limit = options['limit']

        self.stdout.write("Recuperation de la page d'accueil de khassidaenpdf.net...")
        try:
            req = urllib.request.Request("https://khassidaenpdf.net/", headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req)
            html = res.read().decode('utf-8')
        except Exception as e:
            self.stderr.write(f"Erreur lors du telechargement de la page : {e}")
            return

        # On nettoie les backslashes pour parser le JSON plus facilement
        clean_html = html.replace('\\"', '"').replace('\\\\', '\\')

        # On trouve tous les objets JSON qui ressemblent a un Khassida
        pattern = re.compile(r'\{"id":"[a-z0-9]+","nomFrancais":"[^"]+".*?\}')
        matches = pattern.findall(clean_html)

        books = []
        for m in matches:
            try:
                obj = json.loads(m)
                if "nomFrancais" in obj:
                    books.append(obj)
            except Exception:
                pass

        if not books:
            self.stderr.write("Aucun Khassida trouve. La structure du site a peut-etre change.")
            return

        self.stdout.write(self.style.SUCCESS(f"{len(books)} Khassidas trouves dans le code HTML."))

        if limit:
            books = books[:limit]
            self.stdout.write(f"Limite a {limit} Khassidas pour ce test.")

        imported_count = 0
        skipped_count = 0
        compressed_count = 0

        for book in books:
            titre = book.get('nomFrancais', 'Inconnu')
            safe_titre = titre.encode('ascii', 'ignore').decode('ascii')
            auteur = book.get('auteur', 'Cheikh Ahmadou Bamba Mbacke')
            files = book.get('files', [])

            # Déterminer si c'est un Coran ou un Khassida
            titre_lower = titre.lower()
            is_coran = any(mot in titre_lower for mot in ['juz', 'jukki', 'coran', 'quran', 'sourate'])
            
            TargetModel = Coran if is_coran else Khassida

            # Vérifier si le document existe déjà
            existing_doc = TargetModel.objects.filter(titre=titre).first()
            if existing_doc:
                if existing_doc.fichier_pdf:
                    self.stdout.write(f"Ignore : '{safe_titre}' existe deja avec son PDF dans {'Coran' if is_coran else 'Khassida'}.")
                    skipped_count += 1
                    continue
                else:
                    self.stdout.write(f"Mise a jour : '{safe_titre}' existe mais n'a pas de PDF. Re-telechargement...")
                    document = existing_doc
            else:
                if is_coran:
                    document = Coran(titre=titre)
                else:
                    document = Khassida(titre=titre, auteur=auteur)

            if files and len(files) > 0 and files[0]:
                pdf_filename = files[0]
                pdf_url = f"https://khassidaenpdf.net/BOOKS/{urllib.parse.quote(pdf_filename)}"
                self.stdout.write(f"Telechargement de '{safe_titre}'...")

                try:
                    pdf_req = urllib.request.Request(pdf_url, method="GET", headers={'User-Agent': 'Mozilla/5.0'})
                    pdf_res = urllib.request.urlopen(pdf_req, timeout=30)
                    pdf_content = pdf_res.read()
                    original_size = len(pdf_content)

                    # Compression si le fichier depasse 10 Mo
                    if original_size > MAX_SIZE:
                        self.stdout.write(
                            f"  -> Fichier trop gros ({original_size / 1024 / 1024:.1f} Mo), compression en cours..."
                        )
                        try:
                            pdf_content = compress_pdf(pdf_content)
                            new_size = len(pdf_content)
                            self.stdout.write(
                                f"  -> Compresse : {original_size / 1024 / 1024:.1f} Mo -> {new_size / 1024 / 1024:.1f} Mo"
                            )
                            compressed_count += 1

                            if new_size > MAX_SIZE:
                                self.stderr.write(
                                    self.style.WARNING(
                                        f"  -> Attention : apres compression le fichier fait encore {new_size / 1024 / 1024:.1f} Mo. Sauvegarde quand meme..."
                                    )
                                )
                        except Exception as e:
                            self.stderr.write(
                                self.style.ERROR(f"  -> Echec de la compression pour '{safe_titre}': {e}")
                            )

                    document.fichier_pdf.save(pdf_filename, ContentFile(pdf_content), save=False)
                    self.stdout.write(self.style.SUCCESS(f"  -> Succes : '{safe_titre}' importe."))
                except urllib.error.HTTPError as e:
                    self.stderr.write(
                        self.style.ERROR(f"  -> Erreur HTTP {e.code} pour '{safe_titre}'. URL: {pdf_url}")
                    )
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"  -> Erreur de telechargement pour '{safe_titre}': {e}")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f"  -> Pas de fichier PDF trouve pour '{safe_titre}', importe sans PDF.")
                )

            # On sauvegarde le document dans tous les cas
            document.save()
            imported_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTermine ! {imported_count} importes, {skipped_count} ignores, {compressed_count} comprimes."
            )
        )
