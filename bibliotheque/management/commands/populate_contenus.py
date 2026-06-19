import os
from django.core.management.base import BaseCommand
from bibliotheque.models import ContenuDuJour

CONTENUS_AUTHENTIQUES = [
    {
        "verset": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ\n\nAllah ! Point de divinité à part Lui, le Vivant, Celui qui subsiste par lui-même. Ni somnolence ni sommeil ne Le saisissent.\n— Sourate Al-Baqarah (2:255)",
        "beuyit": "Le repentir est une obligation immédiate pour tout pécheur, ne le retarde point.\n— Masalikoul Djinane",
        "rappel": "Les actes ne valent que par les intentions et chacun n'a pour lui que ce qu'il a eu l'intention de faire.\n— Sahih Al-Bukhari"
    },
    {
        "verset": "وَالْعَصْرِ ۙ إِنَّ الْإِنسَانَ لَفِي خُسْرٍ ۙ إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ\n\nPar le Temps ! L'homme est certes, en perdition, sauf ceux qui croient et accomplissent les bonnes œuvres.\n— Sourate Al-Asr (103:1-3)",
        "beuyit": "Purifie ton cœur de l'ostentation et de l'orgueil, car ces maux annulent les bonnes œuvres.\n— Masalikoul Djinane",
        "rappel": "Celui qui ne fait pas miséricorde aux gens, Allah ne lui fera pas miséricorde.\n— Sahih Muslim"
    },
    {
        "verset": "لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا\n\nAllah n'impose à aucune âme une charge supérieure à sa capacité.\n— Sourate Al-Baqarah (2:286)",
        "beuyit": "L'amour sincère du Prophète (PSL) est la clé de la réussite ici-bas et dans l'au-delà.\n— Matlaboul Fawzaini",
        "rappel": "Le meilleur d'entre vous est celui qui apprend le Coran et l'enseigne.\n— Sahih Al-Bukhari"
    },
    {
        "verset": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ۙ إِنَّ مَعَ الْعُسْرِ يُسْرًا\n\nÀ côté de la difficulté est, certes, une facilité ! Oui, à côté de la difficulté est, certes, une facilité !\n— Sourate Ash-Sharh (94:5-6)",
        "beuyit": "Garde le silence sauf pour dire du bien, car la langue est source de nombreux péchés.\n— Masalikoul Djinane",
        "rappel": "Il y a dans le corps un morceau de chair. S'il est sain, tout le corps est sain ; s'il est corrompu, tout le corps est corrompu. C'est le cœur.\n— Bukhari & Muslim"
    },
    {
        "verset": "إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ ۚ يَا أَيُّهَا الَّذِينَ آمَنُوا صَلُّوا عَلَيْهِ وَسَلِّمُوا تَسْلِيمًا\n\nCertes, Allah et Ses Anges prient sur le Prophète ; ô vous qui croyez priez sur lui et adressez-lui vos salutations.\n— Sourate Al-Ahzab (33:56)",
        "beuyit": "Consacre ton temps à l'évocation d'Allah (Zikr) pour illuminer ton esprit.\n— Masalikoul Djinane",
        "rappel": "Celui qui prie sur moi une fois, Allah prie sur lui dix fois.\n— Sahih Muslim"
    },
    {
        "verset": "إِنَّ أَكْرَمَكُمْ عِندَ اللَّهِ أَتْقَاكُمْ\n\nLe plus noble d'entre vous, auprès d'Allah, est le plus pieux.\n— Sourate Al-Hujurat (49:13)",
        "beuyit": "Fuis la jalousie comme tu fuirais le feu, car elle consume les bonnes œuvres.\n— Masalikoul Djinane",
        "rappel": "Ne vous jalousez pas, ne vous haïssez pas, ne vous tournez pas le dos et soyez des serviteurs d'Allah, frères.\n— Sahih Muslim"
    },
    {
        "verset": "وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ\n\nEt votre Seigneur dit : Appelez-Moi, Je vous répondrai.\n— Sourate Ghafir (40:60)",
        "beuyit": "Place ta confiance entière (Tawakkul) en Allah dans toutes tes affaires.\n— Matlaboul Fawzaini",
        "rappel": "L'invocation est l'essence même de l'adoration.\n— Sunan at-Tirmidhi"
    }
]

class Command(BaseCommand):
    help = "Peuple la base de données avec 7 contenus du jour 100% authentiques (Coran, Hadith, Khassida)"

    def handle(self, *args, **options):
        self.stdout.write("--- Nettoyage de la base de données... ---")
        ContenuDuJour.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Anciens contenus supprimés."))

        self.stdout.write("--- Début de l'insertion des nouveaux contenus authentiques ---")
        count = 0
        for item in CONTENUS_AUTHENTIQUES:
            ContenuDuJour.objects.create(
                verset_du_jour=item["verset"],
                beuyit_du_jour=item["beuyit"],
                rappel_dujour=item["rappel"]
            )
            count += 1
                
        self.stdout.write(self.style.SUCCESS(f"Terminé : {count} nouveaux contenus ajoutés !"))
        self.stdout.write(f"Total des contenus dans la base : {ContenuDuJour.objects.count()}")
