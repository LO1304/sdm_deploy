import json
from django.core.management.base import BaseCommand
from bibliotheque.models import Wird, EtapeWird
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Charge le Wird Mahuz Al Khafif et ses 19 étapes.'

    def handle(self, *args, **options):
        # 1. Créer le Wird
        wird, created = Wird.objects.get_or_create(
            slug='mahuz-al-khafif',
            defaults={
                'titre': 'Wird Mahuz Al Khafif',
                'auteur': 'Cheikh Ahmadou Bamba',
                'introduction': 'Un wird puissant pour la protection et l\'élévation spirituelle.',
                'description_courte': '19 étapes de dévotion et de protection.',
            }
        )
        
        if not created:
            wird.etapes.all().delete()
            self.stdout.write(self.style.WARNING(f'Mise à jour du Wird: {wird.titre}'))

        etapes_data = [
            # ÉTAPES 1-13 (PLACEHOLDERS)
            {"num": 1, "t_fr": "Ouverture", "t_ar": "الإفتتاح", "rep": 1, "type": "prep"},
            {"num": 2, "t_fr": "Protection 1", "t_ar": "الحماية ١", "rep": 1, "type": "protec"},
            {"num": 3, "t_fr": "Protection 2", "t_ar": "الحماية ٢", "rep": 1, "type": "protec"},
            {"num": 4, "t_fr": "Protection 3", "t_ar": "الحماية ٣", "rep": 1, "type": "protec"},
            {"num": 5, "t_fr": "Invocation 1", "t_ar": "الدعاء ١", "rep": 1, "type": "invoc"},
            {"num": 6, "t_fr": "Invocation 2", "t_ar": "الدعاء ٢", "rep": 1, "type": "invoc"},
            {"num": 7, "t_fr": "Invocation 3", "t_ar": "الدعاء ٣", "rep": 1, "type": "invoc"},
            {"num": 8, "t_fr": "Invocation 4", "t_ar": "الدعاء ٤", "rep": 1, "type": "invoc"},
            {"num": 9, "t_fr": "Invocation 5", "t_ar": "الدعاء ٥", "rep": 1, "type": "invoc"},
            {"num": 10, "t_fr": "Invocation 6", "t_ar": "الدعاء ٦", "rep": 1, "type": "invoc"},
            {"num": 11, "t_fr": "Invocation 7", "t_ar": "الدعاء ٧", "rep": 1, "type": "invoc"},
            {"num": 12, "t_fr": "Invocation 8", "t_ar": "الدعاء ٨", "rep": 1, "type": "invoc"},
            {"num": 13, "t_fr": "Invocation 9", "t_ar": "الدعاء ٩", "rep": 1, "type": "invoc"},
            
            # ÉTAPES 14-19 (CŒUR)
            {
                "num": 14, "t_fr": "Hasbiyallah", "t_ar": "حسبي الله", "rep": 70, "type": "wird_principal",
                "txt_ar": "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ",
                "trans": "Hasbiyallahu la ilaha illa huwa 'alayhi tawakkaltu wa huwa rabbul 'arshil 'azim",
                "trad": "Allah me suffit. Il n'y a de divinité que Lui. En Lui je place ma confiance ; Il est le Seigneur du Trône immense."
            },
            {
                "num": 15, "t_fr": "Istighfar", "t_ar": "الاستغفار", "rep": 70, "type": "istighfar",
                "txt_ar": "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ الَّذِي لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ وَأَتُوبُ إِلَيْهِ",
                "trans": "Astaghfirullahal 'azim al-lazi la ilaha illa huwal hayyul qayyum wa atubu ilayh",
                "trad": "Je demande pardon à Allah l'Immense, celui en dehors de qui il n'y a point de divinité, le Vivant, l'Immuable, et je me repens à Lui."
            },
            {
                "num": 16, "t_fr": "Shahada", "t_ar": "الشهادة", "rep": 50, "type": "shahada",
                "txt_ar": "لَا إِلَهَ إِلَّا اللَّهُ مُحَمَّدٌ رَسُولُ اللَّهِ",
                "trans": "La ilaha illa Allah, Muhammadun Rasulullah",
                "trad": "Il n'y a point de divinité en dehors d'Allah, Muhammad est le Messager d'Allah."
            },
            {
                "num": 17, "t_fr": "Salawat", "t_ar": "الصلاة على النبي", "rep": 100, "type": "salawat",
                "txt_ar": "اللَّهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِ سَيِّدِنَا مُحَمَّدٍ",
                "trans": "Allahumma salli 'ala sayyidina Muhammadin wa 'ala ali sayyidina Muhammad",
                "trad": "Ô Allah, prie sur notre seigneur Muhammad et sur la famille de notre seigneur Muhammad."
            },
            {
                "num": 18, "t_fr": "Tawheed", "t_ar": "التوحيد", "rep": 10, "type": "tawheed",
                "txt_ar": "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
                "trans": "La ilaha illa Allah wahdahu la sharika lah, lahul mulku wa lahul hamdu wa huwa 'ala kulli shay'in qadir",
                "trad": "Il n'y a point de divinité en dehors d'Allah, Seul, sans associé. À Lui la royauté, à Lui la louange, et Il est capable de toute chose."
            },
            {
                "num": 19, "t_fr": "Dua Al-Khatm", "t_ar": "دعاء الختم", "rep": 1, "type": "cloture",
                "txt_ar": "اللَّهُمَّ تَقَبَّلْ مِنَّا إِنَّكَ أَنْتَ السَّمِيعُ الْعَلِيمُ",
                "trans": "Allahumma taqabbal minna innaka antas samiu-l alim",
                "trad": "Ô Allah, accepte cela de notre part, car Tu es l'Audient, l'Omniscient."
            },
        ]

        for d in etapes_data:
            EtapeWird.objects.create(
                wird=wird,
                numero=d["num"],
                titre_arabe=d["t_ar"],
                titre_francais=d["t_fr"],
                texte_arabe=d.get("txt_ar", "[Texte à venir]"),
                transliteration=d.get("trans", ""),
                traduction_francais=d.get("trad", ""),
                repetitions=d["rep"],
                type=d["type"]
            )
        
        self.stdout.write(self.style.SUCCESS(f'Succès: 19 étapes chargées pour {wird.titre}'))
