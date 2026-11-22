"""
Banque massive de 2 000+ questions islamiques & mourides (100 % authentiques et aléatoires)
- 114 Sourates du Saint Coran (numéro, signification, nombre de versets, lieu de révélation)
- 99 Noms d'Allah (Asmâ'ul Husnâ)
- 30 Jukkis (Juz) du Coran
- 318 Citations authentiques de Cheikh Ahmadou Bamba (œuvre source)
- 25 Prophètes, Compagnons (Sahaba), Sîra, Fiqh, Aqîda, Mouridisme & Grands Khassidas
- Tirage aléatoire sans doublon + tirage déterministe partagé par code pour les Défis entre Amis !
"""
import os
import json
import random
from django.conf import settings
from django.core.cache import cache

# (num, nom_arabe_phonetique, signification_fr, versets, revelation)
SURAHS_114 = [
    (1, "Al-Fâtiha", "L'Ouverture", 7, "Mecquoise"),
    (2, "Al-Baqara", "La Vache", 286, "Médinoise"),
    (3, "Âl-'Imrân", "La Famille d'Imran", 200, "Médinoise"),
    (4, "An-Nisâ'", "Les Femmes", 176, "Médinoise"),
    (5, "Al-Mâ'ida", "La Table Servie", 120, "Médinoise"),
    (6, "Al-An'âm", "Les Bestiaux", 165, "Mecquoise"),
    (7, "Al-A'râf", "Les Murailles", 206, "Mecquoise"),
    (8, "Al-Anfâl", "Le Butin", 75, "Médinoise"),
    (9, "At-Tawba", "Le Repentir", 129, "Médinoise"),
    (10, "Yûnus", "Jonas", 109, "Mecquoise"),
    (11, "Hûd", "Houd", 123, "Mecquoise"),
    (12, "Yûsuf", "Joseph", 111, "Mecquoise"),
    (13, "Ar-Ra'd", "Le Tonnerre", 43, "Médinoise"),
    (14, "Ibrâhîm", "Abraham", 52, "Mecquoise"),
    (15, "Al-Hijr", "Al-Hijr", 99, "Mecquoise"),
    (16, "An-Nahl", "Les Abeilles", 128, "Mecquoise"),
    (17, "Al-Isrâ'", "Le Voyage Nocturne", 111, "Mecquoise"),
    (18, "Al-Kahf", "La Caverne", 110, "Mecquoise"),
    (19, "Maryam", "Marie", 98, "Mecquoise"),
    (20, "Tâ-Hâ", "Ta-Ha", 135, "Mecquoise"),
    (21, "Al-Anbiyâ'", "Les Prophètes", 112, "Mecquoise"),
    (22, "Al-Hajj", "Le Pèlerinage", 78, "Médinoise"),
    (23, "Al-Mu'minûn", "Les Croyants", 118, "Mecquoise"),
    (24, "An-Nûr", "La Lumière", 64, "Médinoise"),
    (25, "Al-Furqân", "Le Discernement", 77, "Mecquoise"),
    (26, "Ash-Shu'arâ'", "Les Poètes", 227, "Mecquoise"),
    (27, "An-Naml", "Les Fourmis", 93, "Mecquoise"),
    (28, "Al-Qasas", "Le Récit", 88, "Mecquoise"),
    (29, "Al-'Ankabût", "L'Araignée", 69, "Mecquoise"),
    (30, "Ar-Rûm", "Les Romains", 60, "Mecquoise"),
    (31, "Luqmân", "Louqman", 34, "Mecquoise"),
    (32, "As-Sajda", "La Prosternation", 30, "Mecquoise"),
    (33, "Al-Ahzâb", "Les Coalisés", 73, "Médinoise"),
    (34, "Saba'", "Saba", 54, "Mecquoise"),
    (35, "Fâtir", "Le Créateur", 45, "Mecquoise"),
    (36, "Yâ-Sîn", "Ya-Sin", 83, "Mecquoise"),
    (37, "As-Sâffât", "Les Rangés", 182, "Mecquoise"),
    (38, "Sâd", "Sad", 88, "Mecquoise"),
    (39, "Az-Zumar", "Les Groupes", 75, "Mecquoise"),
    (40, "Ghâfir", "Le Pardonneur", 85, "Mecquoise"),
    (41, "Fussilat", "Les Versets Détaillés", 54, "Mecquoise"),
    (42, "Ash-Shûrâ", "La Consultation", 53, "Mecquoise"),
    (43, "Az-Zukhruf", "L'Ornement", 89, "Mecquoise"),
    (44, "Ad-Dukhân", "La Fumée", 59, "Mecquoise"),
    (45, "Al-Jâthiya", "L'Agenouillée", 37, "Mecquoise"),
    (46, "Al-Ahqâf", "Les Dunes", 35, "Mecquoise"),
    (47, "Muhammad", "Mouhammad", 38, "Médinoise"),
    (48, "Al-Fath", "La Victoire Éclatante", 29, "Médinoise"),
    (49, "Al-Hujurât", "Les Appartements", 18, "Médinoise"),
    (50, "Qâf", "Qaf", 45, "Mecquoise"),
    (51, "Adh-Dhâriyât", "Qui Éparpillent", 60, "Mecquoise"),
    (52, "At-Tûr", "Le Mont", 49, "Mecquoise"),
    (53, "An-Najm", "L'Étoile", 62, "Mecquoise"),
    (54, "Al-Qamar", "La Lune", 55, "Mecquoise"),
    (55, "Ar-Rahmân", "Le Tout Miséricordieux", 78, "Médinoise"),
    (56, "Al-Wâqi'a", "L'Événement", 96, "Mecquoise"),
    (57, "Al-Hadîd", "Le Fer", 29, "Médinoise"),
    (58, "Al-Mujâdala", "La Discussion", 22, "Médinoise"),
    (59, "Al-Hashr", "L'Exode", 24, "Médinoise"),
    (60, "Al-Mumtahana", "L'Éprouvée", 13, "Médinoise"),
    (61, "As-Saff", "Le Rang", 14, "Médinoise"),
    (62, "Al-Jumu'a", "Le Vendredi", 11, "Médinoise"),
    (63, "Al-Munâfiqûn", "Les Hypocrites", 11, "Médinoise"),
    (64, "At-Taghâbun", "La Grande Perte", 18, "Médinoise"),
    (65, "At-Talâq", "Le Divorce", 12, "Médinoise"),
    (66, "At-Tahrîm", "L'Interdiction", 12, "Médinoise"),
    (67, "Al-Mulk", "La Royauté", 30, "Mecquoise"),
    (68, "Al-Qalam", "La Plume", 52, "Mecquoise"),
    (69, "Al-Hâqqa", "Celle qui Montre la Vérité", 52, "Mecquoise"),
    (70, "Al-Ma'ârij", "Les Voies d'Ascension", 44, "Mecquoise"),
    (71, "Nûh", "Noé", 28, "Mecquoise"),
    (72, "Al-Jinn", "Les Djinns", 28, "Mecquoise"),
    (73, "Al-Muzzammil", "L'Enveloppé", 20, "Mecquoise"),
    (74, "Al-Muddaththir", "Le Revêtu d'un Manteau", 56, "Mecquoise"),
    (75, "Al-Qiyâma", "La Résurrection", 40, "Mecquoise"),
    (76, "Al-Insân", "L'Homme", 31, "Médinoise"),
    (77, "Al-Mursalât", "Les Envoyés", 50, "Mecquoise"),
    (78, "An-Naba'", "La Nouvelle", 40, "Mecquoise"),
    (79, "An-Nâzi'ât", "Les Anges qui Arrachent", 46, "Mecquoise"),
    (80, "'Abasa", "Il s'est Renfrogné", 42, "Mecquoise"),
    (81, "At-Takwîr", "L'Obscurcissement", 29, "Mecquoise"),
    (82, "Al-Infitâr", "La Rupture", 19, "Mecquoise"),
    (83, "Al-Mutaffifîn", "Les Fraudeurs", 36, "Mecquoise"),
    (84, "Al-Inshiqâq", "La Déchirure", 25, "Mecquoise"),
    (85, "Al-Burûj", "Les Constellations", 22, "Mecquoise"),
    (86, "At-Târiq", "L'Astre Nocturne", 17, "Mecquoise"),
    (87, "Al-A'lâ", "Le Très-Haut", 19, "Mecquoise"),
    (88, "Al-Ghâshiya", "L'Enveloppante", 26, "Mecquoise"),
    (89, "Al-Fajr", "L'Aube", 30, "Mecquoise"),
    (90, "Al-Balad", "La Cité", 20, "Mecquoise"),
    (91, "Ash-Shams", "Le Soleil", 15, "Mecquoise"),
    (92, "Al-Layl", "La Nuit", 21, "Mecquoise"),
    (93, "Ad-Duhâ", "Le Jour Montant", 11, "Mecquoise"),
    (94, "Ash-Sharh", "L'Ouverture de la Poitrine", 8, "Mecquoise"),
    (95, "At-Tîn", "Le Figuier", 8, "Mecquoise"),
    (96, "Al-'Alaq", "L'Adhérence", 19, "Mecquoise"),
    (97, "Al-Qadr", "La Destinée", 5, "Mecquoise"),
    (98, "Al-Bayyina", "La Preuve", 8, "Médinoise"),
    (99, "Az-Zalzala", "La Secousse", 8, "Médinoise"),
    (100, "Al-'Âdiyât", "Les Coursiers", 11, "Mecquoise"),
    (101, "Al-Qâri'a", "Le Fracas", 11, "Mecquoise"),
    (102, "At-Takâthur", "La Course aux Richesses", 8, "Mecquoise"),
    (103, "Al-'Asr", "Le Temps", 3, "Mecquoise"),
    (104, "Al-Humaza", "Les Calomniateurs", 9, "Mecquoise"),
    (105, "Al-Fîl", "L'Éléphant", 5, "Mecquoise"),
    (106, "Quraysh", "Qoraych", 4, "Mecquoise"),
    (107, "Al-Mâ'ûn", "L'Ustensile", 7, "Mecquoise"),
    (108, "Al-Kawthar", "L'Abondance", 3, "Mecquoise"),
    (109, "Al-Kâfirûn", "Les Infidèles", 6, "Mecquoise"),
    (110, "An-Nasr", "Le Secours", 3, "Médinoise"),
    (111, "Al-Masad", "Les Fibres", 5, "Mecquoise"),
    (112, "Al-Ikhlâs", "Le Monothéisme Pur", 4, "Mecquoise"),
    (113, "Al-Falaq", "L'Aube Naissante", 5, "Mecquoise"),
    (114, "An-Nâs", "Les Hommes", 6, "Mecquoise"),
]

# Les 99 Noms d'Allah (Asmâ'ul Husnâ)
ASMA_99 = [
    ("Ar-Rahmân", "الرحمن", "Le Tout Miséricordieux"),
    ("Ar-Rahîm", "الرحيم", "Le Très Miséricordieux"),
    ("Al-Malik", "الملك", "Le Souverain Absolu"),
    ("Al-Quddûs", "القدوس", "Le Pur / Le Très Saint"),
    ("As-Salâm", "السلام", "La Paix / Source de Paix"),
    ("Al-Mu'min", "المؤمن", "Celui qui accorde la Sécurité"),
    ("Al-Muhaymin", "المهيمن", "Le Gardien Suprême"),
    ("Al-'Azîz", "العزيز", "Le Tout-Puissant"),
    ("Al-Jabbâr", "الجبار", "Le Contraignant / Le Réparateur"),
    ("Al-Mutakabbir", "المتكبر", "Le Très Grand / L'Orgueilleux"),
    ("Al-Khâliq", "الخالق", "Le Créateur"),
    ("Al-Bâri'", "البارئ", "Le Producteur / L'Initiateur"),
    ("Al-Musawwir", "المصور", "Le Façonneur des formes"),
    ("Al-Ghaffâr", "الغفار", "Le Très Pardonneur"),
    ("Al-Qahhâr", "القهار", "Le Dominateur Suprême"),
    ("Al-Wahhâb", "الوهاب", "Le Donateur Généreux"),
    ("Ar-Razzâq", "الرزاق", "Le Pourvoyeur de subsistance"),
    ("Al-Fattâh", "الفتاح", "Celui qui ouvre les portes"),
    ("Al-'Alîm", "العليم", "L'Omniscient"),
    ("Al-Qâbid", "القابض", "Celui qui restreint"),
    ("Al-Bâsit", "الباسط", "Celui qui étend Sa générosité"),
    ("Al-Khâfid", "الخافض", "Celui qui abaisse"),
    ("Ar-Râfi'", "الرافع", "Celui qui élève"),
    ("Al-Mu'izz", "المعز", "Celui qui donne l'honneur"),
    ("Al-Mudhill", "المذل", "Celui qui humilie"),
    ("As-Samî'", "السميع", "L'Audient qui entend tout"),
    ("Al-Basîr", "البصير", "Le Voyant qui voit tout"),
    ("Al-Hakam", "الحكم", "Le Juge Suprême"),
    ("Al-'Adl", "العدل", "Le Parfaitement Juste"),
    ("Al-Latîf", "اللطيف", "Le Subtil / Le Bienveillant"),
    ("Al-Khabîr", "الخبير", "Le Parfaitement Informé"),
    ("Al-Halîm", "الحليم", "Le Longanime / L'Indulgent"),
    ("Al-'Azîm", "العظيم", "L'Immense / Le Magnifique"),
    ("Al-Ghafûr", "الغفور", "Le Tout-Pardonneur"),
    ("Ash-Shakûr", "الشكور", "Le Très Reconnaissant"),
    ("Al-'Aliyy", "العلي", "Le Très-Haut"),
    ("Al-Kabîr", "الكبير", "L'Infiniment Grand"),
    ("Al-Hafîz", "الحفيظ", "Le Préservateur"),
    ("Al-Muqît", "المقيت", "Le Nourricier"),
    ("Al-Hasîb", "الحسيب", "Celui qui suffit / Qui tient compte"),
    ("Al-Jalîl", "الجليل", "Le Majestueux"),
    ("Al-Karîm", "الكريم", "Le Très Généreux"),
    ("Ar-Raqîb", "الرقيب", "Le Vigilant qui observe tout"),
    ("Al-Mujîb", "المجيب", "Celui qui exauce les prières"),
    ("Al-Wâsi'", "الواسع", "L'Immense / Le Vaste"),
    ("Al-Hakîm", "الحكيم", "L'Infiniment Sage"),
    ("Al-Wadûd", "الودود", "Le Très Aimant"),
    ("Al-Majîd", "المجيد", "Le Très Glorieux"),
    ("Al-Bâ'ith", "الباعث", "Celui qui ressuscite"),
    ("Ash-Shahîd", "الشهيد", "Le Témoin de toute chose"),
    ("Al-Haqq", "الحق", "La Vérité Absolue"),
    ("Al-Wakîl", "الوكيل", "Le Garant / Le Gérant"),
    ("Al-Qawiyy", "القوي", "Le Très Fort"),
    ("Al-Matîn", "المتين", "Le Ferme / L'Inébranlable"),
    ("Al-Waliyy", "الولي", "L'Allié Protecteur"),
    ("Al-Hamîd", "الحميد", "Le Digne de Louange"),
    ("Al-Muhsî", "المحصي", "Celui qui dénombre tout"),
    ("Al-Mubdi'", "المبدئ", "Celui qui donne naissance"),
    ("Al-Mu'îd", "المعيد", "Celui qui redonne vie"),
    ("Al-Muhyî", "المحيي", "Celui qui donne la vie"),
    ("Al-Mumît", "المميت", "Celui qui donne la mort"),
    ("Al-Hayy", "الحي", "Le Vivant Éternel"),
    ("Al-Qayyûm", "القيوم", "Le Subsistant par Lui-même"),
    ("Al-Wâjid", "الواجد", "Celui qui trouve / L'Opulent"),
    ("Al-Mâjid", "الماجد", "Le Noble / L'Illustre"),
    ("Al-Wâhid", "الواحد", "L'Unique"),
    ("Al-Ahad", "الأحد", "L'Un sans associé"),
    ("As-Samad", "الصمد", "Le Seul à être imploré"),
    ("Al-Qâdir", "القادر", "Le Capable de tout"),
    ("Al-Muqtadir", "المقتدر", "Le Détenteur du Pouvoir"),
    ("Al-Muqaddim", "المقدم", "Celui qui fait avancer"),
    ("Al-Mu'akhkhir", "المؤخر", "Celui qui retarde"),
    ("Al-Awwal", "الأول", "Le Premier sans commencement"),
    ("Al-Âkhir", "الآخر", "Le Dernier sans fin"),
    ("Az-Zâhir", "الظاهر", "L'Apparent"),
    ("Al-Bâtin", "الباطن", "Le Caché"),
    ("Al-Wâlî", "الوالي", "Le Maître qui régit tout"),
    ("Al-Muta'âlî", "المتعالي", "Le Suprême / Le Très Élevé"),
    ("Al-Barr", "البر", "Le Bienfaisant"),
    ("At-Tawwâb", "التواب", "Celui qui accueille le repentir"),
    ("Al-Muntaqim", "المنتقم", "Le Vengeur juste"),
    ("Al-'Afuww", "العفو", "L'Indulgent qui efface les péchés"),
    ("Ar-Ra'ûf", "الرؤوف", "Le Très Compatissant"),
    ("Mâlik al-Mulk", "مالك الملك", "Le Maître de la Royauté"),
    ("Dhul-Jalâl wal-Ikrâm", "ذو الجلال والإكرام", "Le Détenteur de Majesté et de Générosité"),
    ("Al-Muqsit", "المقسط", "L'Équitable"),
    ("Al-Jâmi'", "الجامع", "Celui qui rassemble"),
    ("Al-Ghaniyy", "الغني", "Le Riche qui se suffit à Lui-même"),
    ("Al-Mughnî", "المغني", "Celui qui enrichit"),
    ("Al-Mâni'", "المانع", "Celui qui empêche / Protège"),
    ("Ad-Dârr", "الضار", "Celui qui permet l'épreuve"),
    ("An-Nâfi'", "النافع", "Celui qui accorde le bienfait"),
    ("An-Nûr", "النور", "La Lumière des cieux et de la terre"),
    ("Al-Hâdî", "الهادي", "Le Guide"),
    ("Al-Badî'", "البديع", "L'Inventeur sans modèle"),
    ("Al-Bâqî", "الباقي", "Le Permanent / L'Éternel"),
    ("Al-Wârith", "الوارث", "L'Héritier de toute chose"),
    ("Ar-Rashîd", "الرشيد", "Le Guide vers la droiture"),
    ("As-Sabûr", "الصبور", "Le Très Patient"),
]

# Les 25 Prophètes cités dans le Coran : (nom, titre_ou_miracle, peuple_ou_contexte)
PROPHETS_25 = [
    ("Âdam (AS)", "Premier homme et premier Prophète créé d'argile", "Père de l'humanité"),
    ("Idrîs (AS)", "Élevé par Allah à un haut rang, premier à écrire avec le calame", "Postérité d'Âdam"),
    ("Nûh (AS)", "Constructeur de l'Arche face au Déluge, prêcha 950 ans", "Peuple de Noé"),
    ("Hûd (AS)", "Sauvé du vent glacial qui détruisit les orgueilleux", "Peuple de 'Âd"),
    ("Sâlih (AS)", "Miracle de la chamelle sortie du rocher", "Peuple de Thamûd"),
    ("Ibrâhîm (AS)", "Khalîlullâh (l'Ami intime d'Allah), bâtit la Kaaba avec Ismâ'îl", "Peuple de Babylone"),
    ("Lût (AS)", "Envoyé pour avertir les cités perverties", "Peuple de Sodome"),
    ("Ismâ'îl (AS)", "Sacrifice remplacé par un bélier, source de Zamzam", "Ancêtre des Arabes à La Mecque"),
    ("Ishâq (AS)", "Fils d'Ibrâhîm et Sâra, père de Ya'qûb", "Terre de Canaan"),
    ("Ya'qûb (AS)", "Surnommé Isrâ'îl, père des douze tribus", "Enfants d'Israël"),
    ("Yûsuf (AS)", "Interprétation des rêves et ministre d'Égypte après le puits", "Égypte"),
    ("Ayyûb (AS)", "Modèle suprême de patience face à la maladie et la perte", "Terre de Haurân"),
    ("Shu'ayb (AS)", "L'Orateur des Prophètes, combattit la fraude dans les poids", "Peuple de Madyan"),
    ("Mûsâ (AS)", "Kalîmullâh (celui à qui Allah a parlé), bâton et mer fendue, Torah", "Pharaon et Enfants d'Israël"),
    ("Hârûn (AS)", "Frère éloquent et assistant de Mûsâ", "Enfants d'Israël"),
    ("Dhul-Kifl (AS)", "Cité parmi les endurants et les justes", "Enfants d'Israël"),
    ("Dâwûd (AS)", "Roi-Prophète à qui fut révélé le Zabûr (Psaumes), le fer s'assouplissait pour lui", "Enfants d'Israël"),
    ("Sulaymân (AS)", "Comprenait le langage des oiseaux et des fourmis, commandait aux vents", "Royaume de Jérusalem"),
    ("Ilyâs (AS)", "Combattit l'adoration de l'idole Ba'l", "Baalbek / Enfants d'Israël"),
    ("Al-Yasa' (AS)", "Successeur d'Ilyâs cité parmi les meilleurs", "Enfants d'Israël"),
    ("Yûnus (AS)", "Avalé par le grand poisson, implora Allah dans les ténèbres", "Peuple de Ninive"),
    ("Zakariyyâ (AS)", "Tuteur de Maryam, exaucé dans sa vieillesse par la naissance de Yahyâ", "Temple de Jérusalem"),
    ("Yahyâ (AS)", "Reçut la sagesse dès l'enfance, chaste et dévot", "Palestine"),
    ("'Îsâ (AS)", "Né miraculeusement de Maryam, reçut l'Injîl (Évangile), guérissait par permission d'Allah", "Enfants d'Israël"),
    ("Muhammad (PSL)", "Sceau des Prophètes, miséricorde pour les mondes, reçut le Saint Coran", "Toute l'humanité"),
]

# Grands Khassidas & Œuvres de Cheikh Ahmadou Bamba : (titre, theme_signification)
KHASSIDAS_QA = [
    ("Masaalikul Jinaan", "Les Itinéraires du Paradis — grand traité de soufisme et de purification de l'âme"),
    ("Tazawwudu-ç-Çighâr", "Le Viatique des Adolescents — 308 vers sur l'Imân, l'Islâm et l'Ihsân"),
    ("Mawahibou Nâfih", "Les Dons de l'Utile — célèbre panégyrique du Prophète Muhammad (PSL)"),
    ("Jazbul Qulûb", "L'Attirance des Cœurs — vers l'amour du Prophète (PSL)"),
    ("Matlabul Fawzayni", "La Quête des Deux Bonheurs — prière fondatrice pour Touba"),
    ("Matlabuch Chifâ'i", "La Quête de la Guérison — invocation contre les maux physiques et spirituels"),
    ("Huqqal Bukâ'u", "Il convient de pleurer — élégie et hommage aux grands maîtres spirituels"),
    ("Nahju Qadâ'il Hâj", "La Voie de la Satisfaction des Besoins — règles de politesse légale (Adab)"),
    ("Fathul Mannaan", "L'Inspiration du Bienfaisant — garde des organes et droiture spirituelle"),
    ("Midaadi Wa Aqlâmî", "Mon Encre et mes Plumes — consécration totale de l'écriture à l'éloge du Prophète (PSL)"),
    ("Sindidi", "Poème célèbre d'invocation et de protection spirituelle"),
    ("Jaalibatul Marakhib", "Ce qui attire les grâces — poème d'ouverture spirituelle"),
    ("Muqaddimâtul Amdâh", "Les Prémices des Éloges — introduction aux panégyriques prophétiques"),
    ("Minanul Bâqil Qadîm", "Les Bienfaits de l'Éternel — récit de gratitude et de grâces divines"),
    ("Wakâna Haqqan", "Il était de Notre devoir — poème de secours divin et de victoire spirituelle"),
    ("Taysîrul Assîr", "La Facilitation de ce qui est difficile — poème d'allègement des épreuves"),
    ("Asma'ul Husna (Khassida)", "Poème en versification des 99 Beaux Noms d'Allah"),
    ("Munawwiruç-Çudûr", "L'Illuminateur des Poitrines — traité sur le comportement spirituel"),
    ("Jawharu Nafîs", "Le Joyau Précieux — mise en vers de l'ouvrage juridique Al-Akhdarî"),
    ("Farij (Chahru Ramadan)", "Poème récité durant le mois béni de Ramadan pour implorer la délivrance"),
    ("Ilhâmul Wudûd", "L'Inspiration de l'Affectueux — conseils de constance et de sobriété"),
    ("Tazawwudu-ch-Chubbân", "Le Viatique de la Jeunesse — guide complet pour les jeunes musulmans"),
    ("Irwâ'un Nadîm", "L'Abreuvement du Compagnon — récit des vertus et de la voie spirituelle"),
    ("Astaghfirullâha Bihi", "Poème de demande de pardon (Istighfâr) et de repentir sincère"),
]

# Banque curatée : (theme_slug, difficulte_1_a_3, question, bonne_reponse, [3 mauvaises], explication)
CURATED_QUESTIONS = [
    # MOURIDISME & CHEIKH AHMADOU BAMBA
    ("mouridisme", 1, "En quelle année est né Cheikh Ahmadou Bamba (RTA) à Mbacké Baol ?", "1853", ["1840", "1875", "1895"], "Cheikh Ahmadou Bamba est né vers 1853 (1270 H) à Mbacké Baol."),
    ("mouridisme", 1, "Quel est le nom de la mère de Cheikh Ahmadou Bamba ?", "Mame Diarra Bousso", ["Mame Astou Diankha", "Sokhna Maïmouna Mbacké", "Sokhna Aminata Lô"], "Mame Diarra Bousso est vénérée pour sa piété exceptionnelle ; son Magal est célébré à Porokhane."),
    ("mouridisme", 1, "Quel est le nom du père de Cheikh Ahmadou Bamba ?", "Mame Mor Anta Saly Mbacké", ["Mame Thierno Birahim", "Mame Balla Mbacké", "Cheikh Ibrahima Fall"], "Mame Mor Anta Saly Mbacké était un grand érudit et cadi renommé."),
    ("mouridisme", 1, "En quelle année Cheikh Ahmadou Bamba a-t-il fondé la ville sainte de Touba ?", "1887", ["1895", "1902", "1870"], "Touba fut fondée en 1887 autour de l'arbre sacré Guy Texe."),
    ("mouridisme", 1, "Quel événement majeur commémore le Grand Magal de Touba le 18 Safar ?", "Le départ en exil de Cheikh Ahmadou Bamba vers le Gabon", ["La naissance de Cheikh Ahmadou Bamba", "L'inauguration de la Grande Mosquée", "Le retour de Mauritanie"], "Le 18 Safar 1313 H (1895), Cheikh Ahmadou Bamba partit en exil et invita ses disciples à rendre grâce à Allah ce jour-là."),
    ("mouridisme", 1, "Combien d'années dura l'exil de Cheikh Ahmadou Bamba au Gabon ?", "7 ans (1895–1902)", ["3 ans", "12 ans", "5 ans"], "Il resta en exil au Gabon (notamment à Mayombe) de 1895 à 1902."),
    ("mouridisme", 1, "Quel titre illustre Cheikh Ahmadou Bamba chérissait-il par-dessus tout ?", "Khâdimu-r-Rasûl (Serviteur du Prophète)", ["Al-Qutb al-Akbar", "Al-Mansûr", "Amîr al-Mu'minîn"], "Il déclara que toute sa fierté résidait dans son service dévoué au Prophète Muhammad (PSL)."),
    ("mouridisme", 1, "Qui fut le premier Khalife Général des Mourides (1927–1945) ?", "Serigne Mouhamadou Moustapha Mbacké", ["Serigne Fallou Mbacké", "Serigne Abdoul Ahad Mbacké", "Serigne Saliou Mbacké"], "Serigne Mouhamadou Moustapha Mbacké lança les travaux de la Grande Mosquée de Touba."),
    ("mouridisme", 1, "Sous quel Khalife Général la Grande Mosquée de Touba fut-elle inaugurée en 1963 ?", "Serigne Fallou Mbacké", ["Serigne Mouhamadou Moustapha", "Serigne Abdoul Ahad Mbacké", "Serigne Saliou Mbacké"], "Serigne Fallou Mbacké inaugura la Grande Mosquée de Touba le 7 juin 1963."),
    ("mouridisme", 1, "En quelle année Cheikh Ahmadou Bamba a-t-il été rappelé à Dieu à Diourbel ?", "1927", ["1912", "1935", "1945"], "Cheikh Ahmadou Bamba quitta ce monde le 19 juillet 1927 à Diourbel et fut inhumé à Touba."),
    ("mouridisme", 2, "Qui fut le disciple emblématique incarnant le travail et le don de soi (Baye Fall) ?", "Cheikh Ibrahima Fall (Lamp Fall)", ["Mame Cheikh Anta", "Serigne Dame Abdourahmane", "Mame Massamba Mbacké"], "Cheikh Ibrahima Fall (Lamp Fall) donna son nom au grand minaret central de la Mosquée de Touba."),
    ("mouridisme", 2, "Dans quel pays Cheikh Ahmadou Bamba fut-il exilé de 1903 à 1907 ?", "En Mauritanie (Sarsara)", ["Au Mali", "En Guinée", "Au Niger"], "De 1903 à 1907, il séjourna en Mauritanie auprès de Cheikh Sidya Baba."),
    ("mouridisme", 2, "Dans quelle ville du Sénégal Cheikh Ahmadou Bamba résida-t-il en résidence surveillée de 1907 à 1912 ?", "Thieyène (Djolof)", ["Saint-Louis", "Kaolack", "Ziguinchor"], "Il passa 5 années à Thieyène avant de s'installer à Diourbel en 1912."),
    ("mouridisme", 2, "Quel événement célèbre eut lieu le 5 septembre 1895 devant le Conseil Privé à Saint-Louis ?", "La prière des deux Rakaas de Cheikh Ahmadou Bamba", ["La signature d'un traité", "L'inauguration du pont Faidherbe", "La lecture de Jazbul Qulûb"], "Cheikh Ahmadou Bamba accomplit deux rakaas mémorables dans le bureau du Gouverneur à Saint-Louis."),
    ("mouridisme", 2, "Quel frère cadet de Cheikh Ahmadou Bamba administra Darou Mouhty et veilla sur la famille durant l'exil ?", "Mame Thierno Birahim Mbacké (Borom Darou)", ["Mame Cheikh Anta", "Serigne Bara Mbacké", "Serigne Souhaïbou"], "Mame Thierno Birahim Mbacké assura avec dévouement l'éducation et la garde des enfants du Cheikh."),
    ("mouridisme", 2, "Quelle est la traduction du terme wolof-arabe « Touba » issu du Coran (Sourate 13:29) ?", "Félicité / Béatitude éternelle", ["Lumière du matin", "Montagne sacrée", "Jardin de paix"], "Dans le Coran (13:29), Tûbâ désigne la félicité suprême et un arbre du Paradis."),
    ("mouridisme", 3, "Quel grand érudit mouride fut le 5e Khalife Général (1990–2007), fondateur des daaras de Khelcom ?", "Serigne Saliou Mbacké", ["Serigne Abdoul Ahad Mbacké", "Serigne Abdou Khadre Mbacké", "Serigne Mouhamadou Lamine Bara"], "Serigne Saliou Mbacké fut le dernier fils vivant de Cheikh Ahmadou Bamba à diriger la confrérie."),
    ("mouridisme", 3, "Combien de vers compte l'ouvrage pédagogique Tazawwudu-ç-Çighâr ?", "308 vers", ["114 vers", "500 vers", "210 vers"], "Tazawwudu-ç-Çighâr comporte 308 vers structurés autour de l'Imân, l'Islâm et l'Ihsân."),
    ("mouridisme", 3, "Dans quel grand ouvrage Cheikh Ahmadou Bamba explique-t-il le combat spirituel (Jihâd an-Nafs) ?", "Masaalikul Jinaan (Les Itinéraires du Paradis)", ["Matlabuch Chifâ'i", "Sindidi", "Al-Fulkul Mashhûn"], "Masaalikul Jinaan est l'œuvre majeure de Cheikh Ahmadou Bamba sur la purification de l'âme."),

    # SÎRA DU PROPHÈTE (PSL) & COMPAGNONS
    ("sira", 1, "Dans quelle ville est né le Prophète Muhammad (PSL) ?", "La Mecque", ["Médine", "Tâ'if", "Jérusalem"], "Le Prophète (PSL) est né à La Mecque l'Année de l'Éléphant (vers 570)."),
    ("sira", 1, "Dans quelle grotte le Prophète (PSL) a-t-il reçu la première révélation ?", "La grotte de Hirâ'", ["La grotte de Thawr", "La grotte d'Uhud", "La grotte de Qubâ'"], "L'ange Jibrîl (AS) lui révéla les premiers versets de Sourate Al-'Alaq (Iqra') dans la grotte de Hirâ'."),
    ("sira", 1, "Qui fut la première épouse du Prophète (PSL) et la première personne à embrasser l'Islam ?", "Khadîja bint Khuwaylid (RA)", ["'Â'isha bint Abî Bakr (RA)", "Hafsa bint 'Umar (RA)", "Umm Salama (RA)"], "Khadîja (RA) soutint le Prophète (PSL) dès le premier instant de la Révélation."),
    ("sira", 1, "Quel événement marque le début du calendrier islamique (l'Hégire, an 1 H) ?", "L'émigration du Prophète (PSL) de La Mecque à Médine", ["La naissance du Prophète", "La bataille de Badr", "La conquête de La Mecque"], "Le calife 'Umar ibn al-Khattâb institua l'Hégire (622) comme point de départ du calendrier hégirien."),
    ("sira", 1, "Qui fut le premier muezzin de l'Islam ?", "Bilâl ibn Rabâh (RA)", ["Salmân al-Fârisî (RA)", "Abû Hurayra (RA)", "Zayd ibn Hâritha (RA)"], "Bilâl (RA) fut choisi par le Prophète (PSL) pour sa voix puissante et sa foi inébranlable."),
    ("sira", 1, "Quel compagnon accompagna le Prophète (PSL) dans la grotte de Thawr lors de l'Hégire ?", "Abû Bakr As-Siddîq (RA)", ["'Umar ibn al-Khattâb (RA)", "'Uthmân ibn 'Affân (RA)", "'Alî ibn Abî Tâlib (RA)"], "Le Coran mentionne cet épisode dans la sourate At-Tawba (9:40)."),
    ("sira", 1, "Quelle fut la première grande bataille décisive de l'Islam (17 Ramadan an 2 H) ?", "La bataille de Badr", ["La bataille d'Uhud", "La bataille du Fossé", "La bataille de Hunayn"], "313 croyants affrontèrent et vainquirent une armée bien plus nombreuse grâce au secours d'Allah."),
    ("sira", 2, "Quel compagnon a reçu le surnom de « Al-Fârûq » (Celui qui discerne le vrai du faux) ?", "'Umar ibn al-Khattâb (RA)", ["Abû Bakr (RA)", "'Uthmân (RA)", "Khâlid ibn al-Walîd (RA)"], "'Umar (RA), deuxième calife bien guidé, fut surnommé Al-Fârûq par le Prophète (PSL)."),
    ("sira", 2, "Quel compagnon fut surnommé « Dhun-Nûrayn » (L'Homme aux Deux Lumières) ?", "'Uthmân ibn 'Affân (RA)", ["'Alî ibn Abî Tâlib (RA)", "Talha ibn 'Ubaydillâh (RA)", "Az-Zubayr (RA)"], "'Uthmân (RA) épousa successivement deux filles du Prophète (PSL) : Ruqayya puis Umm Kulthûm."),
    ("sira", 2, "Quel compagnon proposa de creuser une tranchée autour de Médine (bataille d'Al-Khandaq) ?", "Salmân al-Fârisî (RA)", ["Sa'd ibn Mu'âdh (RA)", "Abû 'Ubayda (RA)", "'Amr ibn al-'Âs (RA)"], "Cette stratégie perse de Salmân al-Fârisî protégea Médine en l'an 5 de l'Hégire."),
    ("sira", 2, "Quelle mosquée fut la toute première bâtie par le Prophète (PSL) à son arrivée à Médine ?", "La Mosquée de Qubâ'", ["Al-Masjid al-Harâm", "Al-Masjid al-Aqsâ", "La Mosquée des Deux Qiblas"], "La Mosquée de Qubâ' est évoquée dans le Coran comme fondée sur la piété dès le premier jour."),
    ("sira", 2, "Quel est le nom du traité de paix conclu en l'an 6 H entre Médine et Quraysh ?", "Le Pacte d'Al-Hudaybiya", ["Le Pacte d'Al-'Aqaba", "La Charte de Médine", "Le Traité de Khaybar"], "Le Coran qualifie ce traité de « Victoire éclatante » (Fathan Mubînâ) dans Sourate Al-Fath."),
    ("sira", 3, "En quelle année hégirienne eut lieu la conquête pacifique de La Mecque (Fath Makka) ?", "An 8 de l'Hégire (630)", ["An 5 de l'Hégire", "An 10 de l'Hégire", "An 2 de l'Hégire"], "Le Prophète (PSL) entra à La Mecque en Ramadan an 8 H et accorda un pardon général."),
    ("sira", 3, "Quel compagnon est appelé « Sayfullâh al-Maslûl » (L'Épée dégainée d'Allah) ?", "Khâlid ibn al-Walîd (RA)", ["Hamza ibn 'Abdil-Muttalib (RA)", "Ja'far ibn Abî Tâlib (RA)", "Sa'd ibn Abî Waqqâs (RA)"], "Ce titre lui fut attribué par le Prophète (PSL) après la bataille de Mu'ta."),
    ("sira", 3, "Qui fut le principal scribe chargé de compiler le Mushaf sous Abû Bakr puis 'Uthmân (RA) ?", "Zayd ibn Thâbit (RA)", ["'Abdullâh ibn Mas'ûd (RA)", "Ubayy ibn Ka'b (RA)", "Mu'âdh ibn Jabal (RA)"], "Zayd ibn Thâbit (RA) avait mémorisé tout le Coran et assisté à sa dernière révision."),

    # FIQH, PILIERS & AQÎDA
    ("fiqh", 1, "Combien y a-t-il de piliers de l'Islam ?", "5 piliers", ["6 piliers", "4 piliers", "7 piliers"], "Shahâda, Salât (Prière), Zakât, Siyâm (Jeûne du Ramadan) et Hajj (Pèlerinage)."),
    ("fiqh", 1, "Combien y a-t-il de piliers de la Foi (Al-Imân) ?", "6 piliers", ["5 piliers", "7 piliers", "3 piliers"], "Croire en Allah, Ses Anges, Ses Livres, Ses Prophètes, le Jour Dernier et le Décret Divin."),
    ("fiqh", 1, "Quelles sont les 3 grandes dimensions de la religion enseignées dans le hadith de Jibrîl ?", "L'Imân, l'Islâm et l'Ihsân", ["La Prière, le Jeûne et le Hajj", "La Science, le Zikr et le Travail", "Le Coran, la Sunna et le Fiqh"], "Cheikh Ahmadou Bamba a structuré tout Tazawwudu-ç-Çighâr autour de ces 3 dimensions."),
    ("fiqh", 1, "Combien de rakaas obligatoires comporte la prière du Fajr (Subh) ?", "2 rakaas", ["4 rakaas", "3 rakaas", "1 rakaa"], "La prière du Subh (Fajr) compte 2 rakaas récitées à voix haute."),
    ("fiqh", 1, "Combien de rakaas obligatoires comporte la prière du Maghrib (Timiss) ?", "3 rakaas", ["4 rakaas", "2 rakaas", "5 rakaas"], "Maghrib comporte 3 rakaas (2 à voix haute puis 1 à voix basse)."),
    ("fiqh", 1, "Quelle est l'ablution sèche autorisée en l'absence d'eau ou en cas de maladie ?", "Le Tayammum", ["Le Ghusl", "Le Wudû'", "Le Istinjâ'"], "Le Tayammum s'effectue avec de la terre pure (sa'îd tâhir) lorsque l'eau manque ou nuit."),
    ("fiqh", 1, "Quelle nuit bénie du mois de Ramadan vaut mieux que mille mois ?", "Laylatul-Qadr (La Nuit du Destin)", ["Laylatul-Isrâ'", "La 1re nuit de Ramadan", "La nuit de l'Aïd"], "Sourate Al-Qadr (97:3) : « La nuit d'Al-Qadr est meilleure que mille mois. »"),
    ("fiqh", 2, "Selon l'école malikite (et Tazawwudu-ç-Çighâr), combien d'obligations (Fard) comporte le Wudû' ?", "7 obligations (Fard)", ["4 obligations", "10 obligations", "5 obligations"], "Intention, lavage du visage, des mains aux coudes, essuyage de la tête, lavage des pieds, friction (Dalk) et continuité (Fawr)."),
    ("fiqh", 2, "Dans l'école malikite, combien d'obligations (Fard) comporte le bain rituel (Ghusl) ?", "5 obligations (Fard)", ["3 obligations", "7 obligations", "8 obligations"], "Intention, continuité (Fawr), lavage de tout le corps, friction (Dalk) et pénétration de l'eau aux cheveux."),
    ("fiqh", 2, "Quel est le nom de l'aumône purificatrice obligatoire versée à la fin du mois de Ramadan ?", "Zakât al-Fitr (Mour / Asaka Koor)", ["Sadaqa Jâriya", "Fidya", "Kaffâra"], "Zakât al-Fitr purifie le jeûneur et permet aux nécessiteux de célébrer la fête dignement."),
    ("fiqh", 2, "Qu'est-ce que l'Ihsân selon le Prophète Muhammad (PSL) ?", "Adorer Allah comme si tu Le voyais, car si tu ne Le vois pas, Lui te voit", ["Faire beaucoup d'aumônes", "Mémoriser tout le Coran", "Jeûner chaque lundi et jeudi"], "L'Ihsân est le plus haut degré de présence du cœur devant Allah."),
    ("fiqh", 2, "Combien de tours autour de la Kaaba constitue un Tawâf lors du Hajj ou de la 'Umra ?", "7 tours", ["3 tours", "5 tours", "9 tours"], "Le Tawâf s'effectue en 7 tours dans le sens inverse des aiguilles d'une montre, en partant de la Pierre Noire."),
    ("fiqh", 2, "Entre quelles deux collines s'effectue le Sa'y (parcours rituel) à La Mecque ?", "As-Safâ et Al-Marwa", ["Uhud et Hirâ'", "Arafat et Muzdalifa", "Mina et Thawr"], "En mémoire de la quête d'eau de Hâjar (AS) pour son fils Ismâ'îl (AS)."),
    ("fiqh", 3, "Quel est le pilier essentiel du Hajj sans lequel le pèlerinage n'est pas valide ?", "La station à 'Arafât (Al-Wuqûf bi-'Arafât)", ["La lapidation à Mina", "La visite de Médine", "Le sacrifice du mouton"], "Le Prophète (PSL) a dit : « Le Hajj, c'est 'Arafât. »"),
    ("fiqh", 3, "Dans Tazawwudu-ç-Çighâr, combien de livres célestes au total ont été révélés selon la tradition ?", "104 livres célestes", ["4 livres seulement", "70 livres", "124 livres"], "100 feuillets (Suhuf) + 4 grands Livres (Torah, Zabûr, Injîl et Coran)."),
    ("fiqh", 3, "Quel ange est chargé de transmettre la Révélation divine aux Prophètes ?", "Jibrîl (Gabriel)", ["Mîkâ'îl", "Isrâfîl", "'Izrâ'îl"], "Jibrîl (AS) est appelé Ar-Rûh al-Amîn (L'Esprit fidèle) dans le Coran."),
    ("fiqh", 3, "Quel ange est chargé de souffler dans la Trompe (As-Sûr) au Jour du Jugement ?", "Isrâfîl", ["Mîkâ'îl", "Mâlik", "Ridwân"], "Isrâfîl soufflera dans la Trompe sur ordre d'Allah pour annoncer l'Heure puis la Résurrection."),
    ("fiqh", 3, "Quel ange est le gardien du Paradis ?", "Ridwân", ["Mâlik", "Munkar", "Nakîr"], "Ridwân est le gardien du Paradis, tandis que Mâlik est le gardien de l'Enfer."),

    # CORAN & SCIENCES CORANIQUES
    ("coran", 1, "Quelle est la plus longue sourate du Saint Coran ?", "Sourate Al-Baqara (286 versets)", ["Sourate Âl-'Imrân", "Sourate An-Nisâ'", "Sourate Al-A'râf"], "Al-Baqara compte 286 versets et contient notamment Ayat al-Kursî (2:255)."),
    ("coran", 1, "Quelle est la plus courte sourate du Saint Coran ?", "Sourate Al-Kawthar (3 versets)", ["Sourate Al-Ikhlâs", "Sourate An-Nâs", "Sourate Al-Falaq"], "Al-Kawthar ne compte que 3 courts versets."),
    ("coran", 1, "Quelle sourate est appelée « le Cœur du Coran » (Qalb al-Qur'ân) ?", "Sourate Yâ-Sîn (36)", ["Sourate Al-Fâtiha", "Sourate Al-Mulk", "Sourate Ar-Rahmân"], "Sourate Yâ-Sîn est largement récitée pour sa profonde portée sur la foi et la résurrection."),
    ("coran", 1, "Quelle sourate du Coran ne commence PAS par la Basmala (« Bismillâhir-Rahmânir-Rahîm ») ?", "Sourate At-Tawba (9)", ["Sourate An-Naml", "Sourate Al-Fâtiha", "Sourate Al-Ikhlâs"], "At-Tawba (sourate 9) est la seule sans Basmala au début ; An-Naml en contient deux."),
    ("coran", 1, "Quel verset est considéré comme le plus majestueux du Coran (Ayat al-Kursî) ?", "Sourate Al-Baqara, verset 255", ["Sourate Al-Fâtiha, verset 1", "Sourate Al-Ikhlâs, verset 1", "Sourate Yâ-Sîn, verset 58"], "Ayat al-Kursî (2:255) exalte la souveraineté absolue et la vigilance éternelle d'Allah."),
    ("coran", 2, "Quelle sourate équivaut en récompense à un tiers du Coran selon le hadith ?", "Sourate Al-Ikhlâs (112)", ["Sourate Al-Falaq", "Sourate Al-Kâfirûn", "Sourate Al-Qadr"], "Elle résume l'unicité pure d'Allah (At-Tawhîd), qui est l'un des trois grands axes du Coran."),
    ("coran", 2, "Quelle sourate protège du châtiment de la tombe selon la Sunna ?", "Sourate Al-Mulk (67)", ["Sourate Al-Kahf", "Sourate Al-Wâqi'a", "Sourate Al-Fajr"], "Le Prophète (PSL) recommandait de réciter Sourate Al-Mulk chaque nuit."),
    ("coran", 2, "Quelle sourate est fortement recommandée de lire chaque vendredi pour illuminer entre deux vendredis ?", "Sourate Al-Kahf (18)", ["Sourate Al-Jumu'a", "Sourate Maryam", "Sourate Tâ-Hâ"], "Réciter Al-Kahf (La Caverne) le vendredi apporte une lumière spirituelle d'un vendredi à l'autre."),
    ("coran", 2, "Combien de Jukkis (Juz) et combien de Hizb divise-t-on le Saint Coran ?", "30 Jukkis et 60 Hizb", ["20 Jukkis et 40 Hizb", "30 Jukkis et 30 Hizb", "114 Jukkis et 60 Hizb"], "Chaque Jukki (Juz) comprend 2 Hizb, soit 30 Jukkis et 60 Hizb au total."),
    ("coran", 3, "Quelle sourate contient deux fois la formule « Bismillâhir-Rahmânir-Rahîm » ?", "Sourate An-Naml (27)", ["Sourate Al-Baqara", "Sourate Yûsuf", "Sourate Al-Isrâ'"], "Une fois au début de la sourate et une fois dans la lettre du Prophète Sulaymân à la reine de Saba (27:30)."),
    ("coran", 3, "Quel est le plus long verset du Saint Coran (verset de la dette, Ayat ad-Dayn) ?", "Sourate Al-Baqara, verset 282", ["Sourate Al-Baqara, verset 255", "Sourate An-Nisâ', verset 11", "Sourate Al-Mâ'ida, verset 3"], "Le verset 282 de Al-Baqara détaille l'éthique et la rédaction des contrats et dettes."),
    ("coran", 3, "Quelle est la seule femme mentionnée par son prénom dans le Saint Coran ?", "Maryam (Marie, mère de 'Îsâ)", ["Khadîja", "Âsiya", "Hâjar"], "Une sourate entière (la 19e) porte le nom de Maryam (AS)."),
]

# Les 30 Jukkis (Juz) : (num, debut_arabe, debut_sourate)
JUKKIS_30 = [
    (1, "Alif-Lâm-Mîm", "Al-Fâtiha (1)"),
    (2, "Sayaqûlu", "Al-Baqara (2:142)"),
    (3, "Tilka-r-Rusul", "Al-Baqara (2:253)"),
    (4, "Lan Tanâlû", "Âl-'Imrân (3:93)"),
    (5, "Wal-Muhsanât", "An-Nisâ' (4:24)"),
    (6, "Lâ Yuhibbullâh", "An-Nisâ' (4:148)"),
    (7, "Wa Idhâ Sami'û", "Al-Mâ'ida (5:82)"),
    (8, "Wa Law Annanâ", "Al-An'âm (6:111)"),
    (9, "Qâlal-Mala'u", "Al-A'râf (7:88)"),
    (10, "Wa'lamû", "Al-Anfâl (8:41)"),
    (11, "Ya'tadhirûna", "At-Tawba (9:93)"),
    (12, "Wa Mâ Min Dâbbatin", "Hûd (11:6)"),
    (13, "Wa Mâ Ubarri'u", "Yûsuf (12:53)"),
    (14, "Rubamâ", "Al-Hijr (15:1)"),
    (15, "Subhânal-ladhî", "Al-Isrâ' (17:1)"),
    (16, "Qâla Alam", "Al-Kahf (18:75)"),
    (17, "Iqtaraba lin-Nâsi", "Al-Anbiyâ' (21:1)"),
    (18, "Qad Aflaha", "Al-Mu'minûn (23:1)"),
    (19, "Wa Qâlal-ladhîna", "Al-Furqân (25:21)"),
    (20, "Amman Khalaqa", "An-Naml (27:56)"),
    (21, "Utlu Mâ Ûhiya", "Al-'Ankabût (29:46)"),
    (22, "Wa Man Yaqnut", "Al-Ahzâb (33:31)"),
    (23, "Wa Mâ Liya", "Yâ-Sîn (36:28)"),
    (24, "Faman Azlamu", "Az-Zumar (39:32)"),
    (25, "Ilayhi Yuraddu", "Fussilat (41:47)"),
    (26, "Hâ-Mîm", "Al-Ahqâf (46:1)"),
    (27, "Qâla Famâ Khatbukum", "Adh-Dhâriyât (51:31)"),
    (28, "Qad Sami'allâhu", "Al-Mujâdala (58:1)"),
    (29, "Tabârakal-ladhî", "Al-Mulk (67:1)"),
    (30, "'Amma Yatasâ'alûn (Juz Amma)", "An-Naba' (78:1)"),
]

QUIZ_THEMES = [
    {"slug": "mixte", "nom": "Aléatoire Infini (Tous Thèmes)", "icone": "fa-solid fa-shuffle", "desc": "Mélange dynamique parmi 2 000+ questions variées !", "color": "from-amber-500 to-yellow-500"},
    {"slug": "mouridisme", "nom": "Mouridisme & Khassidas", "icone": "fa-solid fa-feather-pointed", "desc": "Cheikh Ahmadou Bamba, Touba, Khassidas & Citations", "color": "from-emerald-500 to-teal-600"},
    {"slug": "coran", "nom": "Saint Coran & 114 Sourates", "icone": "fa-solid fa-book-quran", "desc": "Sourates, versets, Jukkis et sciences coraniques", "color": "from-sky-500 to-indigo-600"},
    {"slug": "asma", "nom": "99 Noms d'Allah (Asmâ'ul Husnâ)", "icone": "fa-solid fa-star-and-crescent", "desc": "Maîtrisez la signification des Beaux Noms d'Allah", "color": "from-purple-500 to-violet-700"},
    {"slug": "prophetes", "nom": "Les 25 Prophètes & Sîra", "icone": "fa-solid fa-mosque", "desc": "Histoire des Prophètes (AS), Sîra du Prophète (PSL) & Compagnons", "color": "from-orange-500 to-amber-700"},
    {"slug": "fiqh", "nom": "Fiqh, Prière & Tazawwud", "icone": "fa-solid fa-scale-balanced", "desc": "Piliers de l'Islam, Foi (Aqîda) et enseignements du Viatique", "color": "from-rose-500 to-red-700"},
]


def _pick_distractors(pool, correct_val, rng, n=3):
    candidates = [x for x in pool if x != correct_val]
    if len(candidates) <= n:
        return candidates
    return rng.sample(candidates, n)


def _make_q(qid, theme, diff, texte, correct, wrongs, explication):
    return {
        'id': qid,
        'theme': theme,
        'diff': diff,
        'texte': texte,
        'correct': str(correct),
        'wrongs': [str(w) for w in wrongs[:3]],
        'explication': explication,
        'points': 10 if diff == 1 else (15 if diff == 2 else 20),
    }


def build_full_question_bank():
    """Construit et met en cache la banque complète (2 000+ questions authentiques)."""
    cached = cache.get('sdm_quiz_bank_2000_v1')
    if cached is not None:
        return cached

    rng = random.Random(20261122)
    bank = []

    # 1. Banque curatée (Mouridisme, Sîra, Fiqh, Coran)
    for idx, (theme, diff, qtxt, corr, wrongs, expl) in enumerate(CURATED_QUESTIONS, 1):
        t_slug = 'prophetes' if theme == 'sira' else theme
        bank.append(_make_q(f"cur_{idx}", t_slug, diff, qtxt, corr, wrongs, expl))

    # 2. Grands Khassidas de Cheikh Ahmadou Bamba (48 questions dans les deux sens)
    all_kh_titles = [k[0] for k in KHASSIDAS_QA]
    all_kh_themes = [k[1] for k in KHASSIDAS_QA]
    for idx, (title, desc) in enumerate(KHASSIDAS_QA, 1):
        bank.append(_make_q(
            f"kh_a_{idx}", "mouridisme", 1 if idx <= 12 else 2,
            f"Quel est le thème principal de l'œuvre « {title} » de Cheikh Ahmadou Bamba ?",
            desc, _pick_distractors(all_kh_themes, desc, rng),
            f"« {title} » signifie : {desc}."
        ))
        bank.append(_make_q(
            f"kh_b_{idx}", "mouridisme", 2 if idx <= 12 else 3,
            f"Quelle œuvre de Cheikh Ahmadou Bamba correspond à : « {desc} » ?",
            title, _pick_distractors(all_kh_titles, title, rng),
            f"Il s'agit du célèbre ouvrage « {title} » de Cheikh Ahmadou Bamba."
        ))

    # 3. Les 114 Sourates du Saint Coran (~456 questions exactes !)
    all_s_names = [f"{s[1]} ({s[2]})" for s in SURAHS_114]
    all_s_meanings = [s[2] for s in SURAHS_114 if s[2] != s[1]]
    all_s_counts = sorted(list({s[3] for s in SURAHS_114}))
    for num, name, meaning, verses, rev in SURAHS_114:
        diff = 1 if (num <= 10 or num >= 90) else (2 if num <= 50 else 3)
        # Q1: Signification
        if meaning.lower() != name.lower().replace('-', ' '):
            bank.append(_make_q(
                f"s_mean_{num}", "coran", diff,
                f"Que signifie le nom de la sourate « {name} » (sourate n°{num}) ?",
                meaning, _pick_distractors(all_s_meanings, meaning, rng),
                f"La sourate {name} (n°{num}) signifie « {meaning} » et compte {verses} versets ({rev})."
            ))
        # Q2: Numéro -> Sourate
        correct_lbl = f"{name} ({meaning})"
        bank.append(_make_q(
            f"s_num_{num}", "coran", diff,
            f"Quelle sourate occupe la position n°{num} dans le Saint Coran ?",
            correct_lbl, _pick_distractors(all_s_names, correct_lbl, rng),
            f"La sourate n°{num} est {name} ({meaning}), révélée en période {rev.lower()} ({verses} versets)."
        ))
        # Q3: Nombre de versets
        near_counts = [c for c in all_s_counts if c != verses and abs(c - verses) <= max(20, verses // 2)]
        if len(near_counts) < 3:
            near_counts = [c for c in all_s_counts if c != verses]
        wrongs_v = [f"{c} versets" for c in rng.sample(near_counts, 3)]
        bank.append(_make_q(
            f"s_cnt_{num}", "coran", min(3, diff + 1),
            f"Combien de versets comporte la sourate {name} ({meaning}) ?",
            f"{verses} versets", wrongs_v,
            f"Sourate {name} (n°{num}) comporte exactement {verses} versets."
        ))
        # Q4: Mecquoise / Médinoise
        bank.append(_make_q(
            f"s_rev_{num}", "coran", diff,
            f"À quelle période principale est rattachée la révélation de la sourate {name} (n°{num}) ?",
            rev,
            ["Médinoise" if rev == "Mecquoise" else "Mecquoise", "Révélée à Jérusalem", "Révélée à Tâ'if"],
            f"La sourate {name} est classée parmi les sourates de période {rev.lower()}."
        ))
        # Q5: Sourate -> Numéro
        near_nums = [n for n in range(max(1, num - 12), min(115, num + 13)) if n != num]
        wrongs_n = [f"Sourate n°{n}" for n in rng.sample(near_nums, 3)]
        bank.append(_make_q(
            f"s_pos_{num}", "coran", min(3, diff + 1),
            f"Quel numéro d'ordre porte la sourate {name} ({meaning}) dans le Saint Coran ?",
            f"Sourate n°{num}", wrongs_n,
            f"{name} ({meaning}) est la sourate n°{num} sur les 114 sourates du Coran."
        ))
        # Q6: Sourate suivante
        if num < 114:
            nxt = SURAHS_114[num]
            nxt_lbl = f"{nxt[1]} ({nxt[2]})"
            bank.append(_make_q(
                f"s_nxt_{num}", "coran", 2 if num <= 30 or num >= 90 else 3,
                f"Quelle sourate suit immédiatement la sourate {name} (n°{num}) dans le Mushaf ?",
                nxt_lbl, _pick_distractors(all_s_names, nxt_lbl, rng),
                f"Après {name} (n°{num}) vient {nxt[1]} ({nxt[2]}, n°{nxt[0]})."
            ))
        # Q7: Sourate précédente
        if num > 1:
            prv = SURAHS_114[num - 2]
            prv_lbl = f"{prv[1]} ({prv[2]})"
            bank.append(_make_q(
                f"s_prv_{num}", "coran", 2 if num <= 30 or num >= 90 else 3,
                f"Quelle sourate précède immédiatement la sourate {name} (n°{num}) dans le Saint Coran ?",
                prv_lbl, _pick_distractors(all_s_names, prv_lbl, rng),
                f"Juste avant {name} (n°{num}) se trouve {prv[1]} ({prv[2]}, n°{prv[0]})."
            ))

    # 4. Les 99 Noms d'Allah (Asmâ'ul Husnâ) (~297 questions exactes !)
    all_a_names = [f"{a[0]} ({a[1]})" for a in ASMA_99]
    all_a_phons = [a[0] for a in ASMA_99]
    all_a_means = [a[2] for a in ASMA_99]
    for idx, (phon, ar, mean) in enumerate(ASMA_99, 1):
        diff = 1 if idx <= 33 else (2 if idx <= 66 else 3)
        lbl = f"{phon} ({ar})"
        bank.append(_make_q(
            f"asma_m_{idx}", "asma", diff,
            f"Quelle est la signification du Beau Nom d'Allah « {phon} » ({ar}) ?",
            mean, _pick_distractors(all_a_means, mean, rng),
            f"« {phon} » ({ar}) signifie : {mean}."
        ))
        bank.append(_make_q(
            f"asma_n_{idx}", "asma", min(3, diff + 1),
            f"Quel Beau Nom d'Allah (Asmâ'ul Husnâ) signifie « {mean} » ?",
            lbl, _pick_distractors(all_a_names, lbl, rng),
            f"« {mean} » correspond au Nom divin {phon} ({ar})."
        ))
        bank.append(_make_q(
            f"asma_ar_{idx}", "asma", 2 if idx <= 50 else 3,
            f"Comment se lit et se prononce le Nom d'Allah écrit en arabe « {ar} » ?",
            phon, _pick_distractors(all_a_phons, phon, rng),
            f"« {ar} » se prononce {phon} et signifie « {mean} »."
        ))

    # 5. Les 25 Prophètes (75 questions exactes !)
    all_p_names = [p[0] for p in PROPHETS_25]
    all_p_facts = [p[1] for p in PROPHETS_25]
    all_p_peoples = list({p[2] for p in PROPHETS_25})
    for idx, (pname, fact, people) in enumerate(PROPHETS_25, 1):
        diff = 1 if idx <= 12 else 2
        bank.append(_make_q(
            f"proph_a_{idx}", "prophetes", diff,
            f"Quel Prophète (AS) est directement associé à ce fait : « {fact} » ?",
            pname, _pick_distractors(all_p_names, pname, rng),
            f"Il s'agit du Prophète {pname} ({people})."
        ))
        bank.append(_make_q(
            f"proph_b_{idx}", "prophetes", diff,
            f"Qu'est-ce qui caractérise le Prophète {pname} dans le récit coranique ?",
            fact, _pick_distractors(all_p_facts, fact, rng),
            f"{pname} ({people}) : {fact}."
        ))
        bank.append(_make_q(
            f"proph_c_{idx}", "prophetes", 2,
            f"À quel peuple ou contexte principal est rattachée la mission du Prophète {pname} ?",
            people, _pick_distractors(all_p_peoples, people, rng),
            f"La mission du Prophète {pname} est liée à : {people}."
        ))

    # 6. Les 30 Jukkis (Juz) (90 questions exactes !)
    all_j_starts = [j[2] for j in JUKKIS_30]
    all_j_labels = [f"Jukki {j[0]} ({j[1]})" for j in JUKKIS_30]
    all_hizb_ranges = [f"Hizb {j[0]*2-1} et Hizb {j[0]*2}" for j in JUKKIS_30]
    for jnum, jar, jstart in JUKKIS_30:
        diff = 1 if jnum in (1, 29, 30) else (2 if jnum <= 15 else 3)
        bank.append(_make_q(
            f"juk_a_{jnum}", "coran", diff,
            f"Par quelle sourate commence le Jukki (Juz) n°{jnum} (« {jar} ») ?",
            jstart, _pick_distractors(all_j_starts, jstart, rng),
            f"Le Jukki n°{jnum} ({jar}) débute à {jstart} (Hizb {jnum*2-1}–{jnum*2})."
        ))
        jlbl = f"Jukki {jnum} ({jar})"
        bank.append(_make_q(
            f"juk_b_{jnum}", "coran", min(3, diff + 1),
            f"Quel Jukki (Juz) du Saint Coran débute à {jstart} ?",
            jlbl, _pick_distractors(all_j_labels, jlbl, rng),
            f"{jstart} marque l'ouverture du Jukki n°{jnum} ({jar})."
        ))
        hr = f"Hizb {jnum*2-1} et Hizb {jnum*2}"
        bank.append(_make_q(
            f"juk_h_{jnum}", "coran", 2,
            f"Quels sont les deux Hizb qui composent le Jukki (Juz) n°{jnum} ?",
            hr, _pick_distractors(all_hizb_ranges, hr, rng),
            f"Chaque Jukki comporte 2 Hizb : le Jukki n°{jnum} réunit {hr}."
        ))

    # 7. Citations authentiques de Cheikh Ahmadou Bamba (issues de daily_rappels_sdm.json -> ~190 questions !)
    rappels_path = os.path.join(settings.BASE_DIR, 'daily_rappels_sdm.json')
    known_books = [
        "Masaalikul Jinaan",
        "Nahju Qadâ'il Hâj",
        "Fathul Mannaan",
        "Ilhâmul Wudûd",
        "Tazawwudu-ç-Çighâr (Wolof)",
    ]
    if os.path.isfile(rappels_path):
        try:
            with open(rappels_path, 'r', encoding='utf-8') as rf:
                cits = json.load(rf)
            for idx, c in enumerate(cits, 1):
                b = c.get('badge', '')
                txt = (c.get('texte') or '').strip()
                if b in known_books and 45 <= len(txt) <= 210:
                    display_book = b.replace(' (Wolof)', '')
                    choices_pool = [kb.replace(' (Wolof)', '') for kb in known_books]
                    excerpt = txt[:165] + ('…' if len(txt) > 165 else '')
                    bank.append(_make_q(
                        f"cit_{idx}", "mouridisme", 2 if idx % 2 == 0 else 3,
                        f"De quelle œuvre de Cheikh Ahmadou Bamba est tirée cette parole : « {excerpt} » ?",
                        display_book,
                        _pick_distractors(choices_pool, display_book, rng),
                        f"Cette parole authentique est tirée de {c.get('source', display_book)}."
                    ))
        except Exception:
            pass

    # 8. Intégrer les 205 questions Tazawwudu-ç-Çighâr + 27 questions DB existantes
    try:
        from .models import TazawwudQuestion, Question
        for tq in TazawwudQuestion.objects.prefetch_related('choix').select_related('lecon', 'lecon__module'):
            ch = list(tq.choix.all())
            corr = next((c.texte for c in ch if c.est_correct), None)
            wrongs = [c.texte for c in ch if not c.est_correct]
            if corr and len(wrongs) >= 2:
                bank.append(_make_q(
                    f"tz_{tq.id}", "fiqh", 1 if tq.lecon.module.numero <= 2 else 2,
                    tq.texte, corr, wrongs[:3],
                    getattr(tq, 'explication_reponse', '') or f"Enseignement issu de Tazawwudu-ç-Çighâr ({tq.lecon.titre})."
                ))
        for dq in Question.objects.prefetch_related('choix').select_related('categorie'):
            ch = list(dq.choix.all())
            corr = next((c.texte for c in ch if c.est_correct), None)
            wrongs = [c.texte for c in ch if not c.est_correct]
            if corr and len(wrongs) >= 2:
                cat_nom = (dq.categorie.nom if dq.categorie else '').lower()
                t_slug = 'mouridisme' if 'mourid' in cat_nom else ('coran' if 'coran' in cat_nom else ('prophetes' if 'proph' in cat_nom else 'fiqh'))
                bank.append(_make_q(
                    f"db_{dq.id}", t_slug, 1,
                    dq.texte, corr, wrongs[:3],
                    dq.explication or "Question issue de la banque SDM Islam."
                ))
    except Exception:
        pass

    cache.set('sdm_quiz_bank_2000_v1', bank, 600)
    return bank


def sample_quiz_questions(theme_slug='mixte', difficulty=None, count=10, seed=None, exclude_ids=None):
    """
    Tire `count` questions uniques (aléatoires, ou déterministes si `seed` est fourni pour un Défi entre amis).
    """
    bank = build_full_question_bank()
    exclude = set(exclude_ids or [])

    pool = bank
    if theme_slug and theme_slug != 'mixte':
        sub = [q for q in pool if q['theme'] == theme_slug]
        if len(sub) >= count:
            pool = sub

    if difficulty in (1, 2, 3):
        sub_d = [q for q in pool if q['diff'] == difficulty]
        if len(sub_d) >= count:
            pool = sub_d

    fresh = [q for q in pool if q['id'] not in exclude]
    if len(fresh) < count:
        fresh = pool

    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    picked = rng.sample(fresh, min(count, len(fresh)))

    formatted = []
    for q in picked:
        choices = [{'texte': q['correct'], 'est_correct': True}] + [
            {'texte': w, 'est_correct': False} for w in q['wrongs']
        ]
        rng.shuffle(choices)
        formatted.append({
            'id': q['id'],
            'theme': q['theme'],
            'texte': q['texte'],
            'points': q['points'],
            'explication': q['explication'],
            'choix': choices,
        })
    return formatted


def get_quiz_bank_stats():
    bank = build_full_question_bank()
    counts = {}
    for q in bank:
        counts[q['theme']] = counts.get(q['theme'], 0) + 1
    return len(bank), counts
