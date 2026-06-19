import os
from django.core.management.base import BaseCommand
from bibliotheque.models import ContenuDuJour

CITATIONS = [
    {
        "verset": "Le repentir est une obligation immédiate pour tout pécheur, ne le retarde point.",
        "beuyit": "Masalikoul Djinane (Les Itinéraires du Paradis)",
        "rappel": "Ne remets jamais à demain la purification de ton cœur, car nul ne connaît l'heure de son départ."
    },
    {
        "verset": "Purifie ton cœur de l'ostentation et de l'orgueil, car ces maux annulent les bonnes œuvres.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Agis exclusivement pour la face d'Allah, sans chercher l'approbation des hommes."
    },
    {
        "verset": "La meilleure des provisions pour l'au-delà est la crainte pieuse (Taqwa).",
        "beuyit": "Tazawwudus Saghîr (Le Viatique des Jeunes)",
        "rappel": "Rappelle-toi qu'Allah te voit en tout lieu et en tout instant."
    },
    {
        "verset": "Consacre ton temps à l'évocation d'Allah (Zikr) pour illuminer ton esprit.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Le Zikr est la nourriture de l'âme, ne laisse pas ton cœur s'assécher."
    },
    {
        "verset": "L'amour sincère du Prophète (PSL) est la clé de la réussite ici-bas et dans l'au-delà.",
        "beuyit": "Matlaboul Fawzaini",
        "rappel": "Multiplie les prières sur le Prophète, elles dissipent les soucis et attirent la grâce."
    },
    {
        "verset": "Garde le silence sauf pour dire du bien, car la langue est source de nombreux péchés.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Avant de parler, demande-toi si tes paroles sont utiles et véridiques."
    },
    {
        "verset": "Pardonne à ceux qui t'ont fait du tort, Allah te pardonnera tes propres fautes.",
        "beuyit": "Nahju Qada'il Hajj",
        "rappel": "La grandeur d'âme se mesure à sa capacité de pardonner et de faire le bien."
    },
    {
        "verset": "La patience dans les épreuves est une lumière qui dissipe les ténèbres du désespoir.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Face à la difficulté, garde confiance en Allah, car après la difficulté vient la facilité."
    },
    {
        "verset": "Ne méprise aucun musulman, car le secret d'Allah peut être caché en lui.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "L'humilité est la marque des grands hommes. Traite chaque personne avec respect."
    },
    {
        "verset": "Sois constant dans l'accomplissement de tes prières à l'heure prescrite.",
        "beuyit": "Tazawwudus Saghîr",
        "rappel": "La prière est le premier acte sur lequel tu seras interrogé, veille sur elle."
    },
    {
        "verset": "Celui qui cherche le savoir cherche le Paradis.",
        "beuyit": "Tazawwudush Shubban",
        "rappel": "L'ignorance est une maladie, guéris-la par l'apprentissage des sciences religieuses."
    },
    {
        "verset": "Évite la compagnie des personnes corrompues, car elles ternissent le cœur.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Entoure-toi de gens vertueux qui te rappellent ton Seigneur."
    },
    {
        "verset": "Ne sois pas l'esclave de tes passions, sois l'esclave d'Allah seul.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Dompte ton égo (Nafs) avant qu'il ne te domine."
    },
    {
        "verset": "La politesse (Adab) et le bon comportement valent mieux que de nombreuses œuvres surérogatoires.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Le bon comportement est la véritable parure du croyant."
    },
    {
        "verset": "Fuis la jalousie comme tu fuirais le feu, car elle consume les bonnes œuvres.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Souhaite pour ton frère ce que tu souhaites pour toi-même."
    },
    {
        "verset": "La vraie richesse réside dans le contentement du cœur (Qana'a).",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Sois satisfait de ce qu'Allah t'a accordé et tu seras le plus riche des hommes."
    },
    {
        "verset": "Hâte-toi vers les bonnes œuvres avant que la mort ne te surprenne.",
        "beuyit": "Tazawwudus Saghîr",
        "rappel": "Le temps est ton capital le plus précieux, ne le gaspille pas."
    },
    {
        "verset": "Celui qui remercie Allah verra ses bienfaits augmenter.",
        "beuyit": "Nahju Qada'il Hajj",
        "rappel": "Prends l'habitude de dire Alhamdoulillah dans chaque situation."
    },
    {
        "verset": "Garde tes prières rituelles comme la prunelle de tes yeux.",
        "beuyit": "Tazawwudush Shubban",
        "rappel": "La régularité dans la prière purifie le cœur et l'âme."
    },
    {
        "verset": "Place ta confiance entière (Tawakkul) en Allah dans toutes tes affaires.",
        "beuyit": "Matlaboul Fawzaini",
        "rappel": "Fais les causes, mais sache que seul Allah décide du résultat."
    },
    {
        "verset": "L'aumône (Sadaqa) éteint la colère du Seigneur.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Donne même un sourire, car c'est aussi une aumône."
    },
    {
        "verset": "Honore tes parents, car ta réussite dépend de leur satisfaction.",
        "beuyit": "Tazawwudush Shubban",
        "rappel": "Le Paradis se trouve sous les pieds des mères."
    },
    {
        "verset": "Prie la nuit (Tahajjud) pendant que les autres dorment.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Le dernier tiers de la nuit est un moment d'intimité privilégiée avec Allah."
    },
    {
        "verset": "L'obéissance au guide spirituel (Cheikh) mène vers la lumière.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Suis les recommandations de ton guide avec sincérité et soumission."
    },
    {
        "verset": "Prie pour l'unité de la communauté musulmane (Oumma).",
        "beuyit": "Matlabush Shifa",
        "rappel": "Demande à Allah la paix et la miséricorde pour tous les croyants."
    },
    {
        "verset": "Sois juste envers toi-même et envers les autres.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "La justice est le fondement de la piété et de la paix intérieure."
    },
    {
        "verset": "Invoque Allah abondamment (Dhikr Kathira).",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Que ta langue ne cesse jamais d'être humidifiée par l'évocation d'Allah."
    },
    {
        "verset": "Celui qui s'attache fermement à la Sunna ne s'égarera jamais.",
        "beuyit": "Tazawwudus Saghîr",
        "rappel": "Prends le Prophète (PSL) comme seul modèle absolu de conduite."
    },
    {
        "verset": "Ne te préoccupe pas des défauts d'autrui, corrige d'abord les tiens.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "Celui qui connaît ses propres défauts n'a pas le temps de critiquer ceux des autres."
    },
    {
        "verset": "Aime pour l'amour d'Allah et déteste pour l'amour d'Allah.",
        "beuyit": "Masalikoul Djinane",
        "rappel": "L'amour en Allah est le lien le plus solide de la foi."
    }
]

class Command(BaseCommand):
    help = "Peuple la base de données avec 30 contenus du jour (Citations de Khassidas)"

    def handle(self, *args, **options):
        self.stdout.write("--- Début de l'insertion des contenus du jour ---")
        
        count = 0
        for item in CITATIONS:
            # Vérifier si ce verset existe déjà pour éviter les doublons lors des exécutions répétées
            if not ContenuDuJour.objects.filter(verset_du_jour=item["verset"]).exists():
                ContenuDuJour.objects.create(
                    verset_du_jour=item["verset"],
                    beuyit_du_jour=item["beuyit"],
                    rappel_dujour=item["rappel"]
                )
                count += 1
                
        self.stdout.write(self.style.SUCCESS(f"Terminé : {count} nouveaux contenus ajoutés !"))
        self.stdout.write(f"Total des contenus dans la base : {ContenuDuJour.objects.count()}")
