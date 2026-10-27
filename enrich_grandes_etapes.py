# -*- coding: utf-8 -*-
"""
Enrichissement pédagogique complet des 5 Grandes Étapes (TazawwudModule)
et des 31 Leçons (TazawwudLecon) de Tazawwudu-ç-Çighâr (Le Viatique des Adolescents)
de Cheikh Ahmadou Bamba Khâdimu-r-Rasûl (308 vers).
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import TazawwudModule, TazawwudLecon


MODULES_ENRICHIS = {
    1: {
        "titre": "Les Fondations de la Foi (Al-Imân & At-Tawhîd)",
        "description": (
            "Première grande étape (Vers 1 à 92) : L'intention pure, l'exhortation à la jeunesse, "
            "les trois piliers de la Religion (Imân, Islâm, Ihsân), la science du Tawhîd "
            "(les 20 Attributs nécessaires à Allah, les 20 contraires impossibles et l'Attribut possible) "
            "ainsi que les 6 articles de la Foi (Allah, Ses Anges, Ses 104 Livres, Ses Envoyés, le Jour Ultime et le Décret Divin)."
        ),
    },
    2: {
        "titre": "Les Bases de la Pratique & la Pureté de l'Âme (Al-Islâm I)",
        "description": (
            "Deuxième grande étape (Vers 93 à 163) : Les 5 piliers de l'Islâm, la primauté de la Shahâdah "
            "(meilleur Dhikr), le caractère sacré des 5 prières quotidiennes, les 4 conditions de la pureté légale "
            "(corps, habits, lieu), la préservation des 7 membres du corps contre les péchés, les conditions du repentir "
            "sincère (At-Tawbah) et la nécessité de distinguer l'Obligatoire (Fard) du Traditionnel (Sunnah)."
        ),
    },
    3: {
        "titre": "La Prière et la Purification en Détail (Al-Islâm II)",
        "description": (
            "Troisième grande étape (Vers 164 à 205) : Étude méthodique du Fiqh malikite selon Al-'Awfî : "
            "les 15 Actes Obligatoires (Farâ'id) et les 18 Actes Traditionnels (dont les 8 Sunnah Mu'akkadah) de la Prière, "
            "les 7 obligations et 8 traditions des Ablutions mineures (Wudû'), les 5 obligations et 4 traditions "
            "de la Purification majeure (Ghusl), et les 8 obligations et 3 traditions du Tayammum."
        ),
    },
    4: {
        "titre": "Jeûne, Zakat, Pèlerinage & Rattrapage des Prières (Al-Islâm III)",
        "description": (
            "Quatrième grande étape (Vers 206 à 273) : Les règles du Jeûne de Ramadan (2 obligations, 3 traditions), "
            "de l'Aumône Légale Zakat (4 obligations, 3 traditions) et du Pèlerinage Hajj (4 obligations, 12 traditions), "
            "suivies du guide complet sur le rattrapage des prières derrière l'Imam (Al-Masbûq pour les 5 prières) "
            "et les modalités de la prière du malade."
        ),
    },
    5: {
        "titre": "La Perfection Spirituelle & le Soufisme (Al-Ihsân & At-Tasawwuf)",
        "description": (
            "Cinquième grande étape (Vers 274 à 308) : Le sommet de la pyramide spirituelle (Al-Ihsân : adorer Allah "
            "comme si tu Le voyais), l'acquisition des nobles vertus (science, scrupule, gratitude, sincérité, générosité), "
            "l'éducation spirituelle auprès d'un Guide Éclairé (Cheikh de Tarbiyah), la saisie des 5 opportunités de la vie "
            "avant leurs 5 contraires, et la clôture bénie de l'ouvrage."
        ),
    },
}


LECONS_ENRICHIES = {
    # ══════════════════════════════════════════════════════════════════
    # MODULE 1 : LES FONDATIONS DE LA FOI (IMÂN)
    # ══════════════════════════════════════════════════════════════════
    (1, 1): {
        "description": "Vers 1 à 11 : Louange à Allah, prière sur le Prophète (ﷺ), dédicace aux jeunes et explication du titre Tazawwudu-ç-Çighâr.",
        "explication": (
            "Dans ces vers d'ouverture (1 à 11), Cheikh Ahmadou Bamba se présente avec une humilité exemplaire comme "
            "« Ahmad, l'esclave de Dieu et le serviteur du Prophète (Khâdimu-r-Rasûl) ».\n\n"
            "Il commence par rendre grâce à Allah Qui l'a comblé du bienfait de l'Islâm, de l'Imân et de l'Ihsân, puis adresse "
            "ses salutations sur le Prophète Muhammad (ﷺ), sa famille et ses compagnons. Il expose ensuite la vocation de cet ouvrage : "
            "offrir aux jeunes (et à tout croyant) un « Viatique » (provision de voyage spirituel) clair, concis et suffisant pour connaître "
            "ses devoirs envers son Seigneur dès l'adolescence, car l'adoration accomplie dans la jeunesse élève le serviteur au Jour du Jugement."
        ),
        "a_retenir": (
            "• L'auteur se nomme Ahmad, esclave d'Allah et serviteur du Prophète (ﷺ)\n"
            "• Tazawwudu-ç-Çighâr signifie « Le Viatique des Adolescents »\n"
            "• Tout acte méritoire commence par la Basmala, la Louange à Allah (Hamdala) et la Prière sur le Prophète\n"
            "• La jeunesse est l'âge d'or pour acquérir les fondements de la foi et de l'adoration\n"
            "• Ce livre réunit l'essentiel de la théologie (Tawhîd), du droit (Fiqh) et de la spiritualité (Tasawwuf)"
        ),
    },
    (1, 2): {
        "description": "Vers 12 à 18 : Exhortation fraternelle aux adolescents : droiture, quête du savoir, révision assidue et maîtrise de l'âme.",
        "explication": (
            "Dans ce préambule vibrant (vers 12 à 18), Cheikh Ahmadou Bamba s'adresse directement aux jeunes : « Ô vous les adolescents ! ».\n\n"
            "Il leur trace une méthode d'excellence : ne se préoccuper que de droiture, rechercher ardemment le savoir utile, "
            "assimiler et réviser constamment ses leçons, et fuir les assemblées de futilités et d'insouciance. "
            "Il enseigne que l'âme charnelle (Nafs) penche naturellement vers la paresse et les passions : celui qui la bride par la science "
            "et la piété triomphe, tandis que celui qui remet son repentir à plus tard risque d'être surpris par le trépas."
        ),
        "a_retenir": (
            "• S'attacher exclusivement à la droiture et à la quête du savoir utile\n"
            "• Assimiler ses leçons et les réviser avec constance\n"
            "• Fuir les assemblées de futilités qui éteignent la lumière du cœur\n"
            "• Lutter contre les passions de l'âme charnelle (Nafs) dès le jeune âge\n"
            "• Se hâter vers le repentir sincère sans jamais procrastiner"
        ),
    },
    (1, 3): {
        "description": "Vers 19 à 21 : L'architecture tripartite de la Religion : Al-Imân (la Foi), Al-Islâm (la Pratique) et Al-Ihsân (l'Excellence).",
        "explication": (
            "Les vers 19 à 21 posent le plan directeur de toute la religion musulmane, conformément au célèbre Hadith de Jibrîl (Gabriel).\n\n"
            "La Religion d'Allah repose sur trois piliers indissociables :\n"
            "1. Al-Imân (la Profession de Foi) : la croyance ferme du cœur en Dieu, Ses attributs et les vérités révélées.\n"
            "2. Al-Islâm (la Soumission pratique) : l'accomplissement des actes cultuels avec les membres du corps.\n"
            "3. Al-Ihsân (la Perfection spirituelle) : la présence du cœur et la sincérité totale face au Regard divin."
        ),
        "a_retenir": (
            "• La Religion de notre Seigneur se compose de 3 grandes parties complémentaires\n"
            "• 1re partie : Al-Imân (la Foi et la Croyance juste dans le cœur)\n"
            "• 2e partie : Al-Islâm (les Pratiques cultuelles et l'obéissance des membres)\n"
            "• 3e partie : Al-Ihsân (la Perfection spirituelle et la pureté de l'intention)\n"
            "• La foi sans la pratique est incomplète, et la pratique sans l'Ihsân manque d'âme"
        ),
    },
    (1, 4): {
        "description": "Vers 22 à 42 : La science du Tawhîd : les 20 Attributs nécessaires à Allah, les 20 contraires impossibles et l'Attribut possible.",
        "explication": (
            "Dans les vers 22 à 42, le Cheikh expose la quintessence du Tawhîd (unicité divine) que tout croyant responsable (Mukallaf) "
            "doit connaître.\n\n"
            "Il énumère les 20 Attributs nécessaires (Wâjib) à Allah : l'Existence (Wujûd), la Prééternité (Qidam), la Pérennité (Baqâ'), "
            "la Différence absolue d'avec les créatures (Mukhâlafatu lil-hawâdith), l'Autonomie (Qiyâmuhu bi-nafsihi), l'Unicité (Wahdâniyyah), "
            "la Puissance (Qudrah), la Volonté (Irâdah), la Science ('Ilm), la Vie (Hayât), l'Ouïe (Sam'), la Vue (Basar) et la Parole (Kalâm), "
            "ainsi que les 7 attributs de qualification correspondants.\n\n"
            "À ces 20 qualités s'opposent 20 défauts absolument impossibles (Mustahîl) à Son sujet (le néant, le commencement, la fin, "
            "l'impuissance, l'ignorance, etc.). Enfin, l'Attribut possible (Jâ'iz) à Son égard est de créer ou de ne pas créer tout être possible. "
            "L'ensemble de ces 41 attributs est résumé dans la parole sacrée : Lâ ilâha illâ Allâh."
        ),
        "a_retenir": (
            "• Tout croyant doit connaître les 41 attributs relatifs à la Connaissance d'Allah\n"
            "• 20 Attributs sont Nécessaires (Wâjib) : Existence, Prééternité, Pérennité, Unicité, Puissance, Volonté, Science, Vie, Ouïe, Vue, Parole...\n"
            "• 20 Attributs contraires sont Impossibles (Mustahîl) à Son sujet (néant, impuissance, ignorance, mort, surdité...)\n"
            "• 1 Attribut est Possible (Jâ'iz) : faire exister ou laisser dans le néant toute créature possible\n"
            "• La formule « Lâ ilâha illâ Allâh » renferme le sens de tous ces attributs de perfection"
        ),
    },
    (1, 5): {
        "description": "Vers 43 à 50 : La foi aux Anges (Al-Malâ'ikah), leur infaillibilité et les 10 grands Anges à connaître nommément.",
        "explication": (
            "Les vers 43 à 50 détaillent le deuxième pilier de la foi : la croyance aux Anges.\n\n"
            "Ce sont des créatures subtiles façonnées de lumière, totalement préservées de tout péché (infaillibles) : ils ne désobéissent "
            "jamais à Allah et exécutent fidèlement Ses ordres. Ils ne sont ni mâles ni femelles, ne mangent ni ne boivent.\n\n"
            "Le Cheikh cite les 10 Anges qu'il faut connaître en détail : Jibrîl (Gabriel, chargé de la Révélation), Mîkâ'îl (chargé de la pluie "
            "et des subsistances), Isrâfîl (chargé de souffler dans la Trompe), 'Azrâ'îl (l'Ange de la mort), Raqîb et 'Atîd (les deux scribes "
            "qui inscrivent les œuvres), Munkar et Nakîr (chargés de l'interrogatoire dans la tombe), Ridwân (gardien du Paradis) et Mâlik (gardien de l'Enfer)."
        ),
        "a_retenir": (
            "• Les Anges sont des êtres honorés créés de lumière et totalement préservés du péché\n"
            "• Ils ne mangent pas, ne boivent pas et ne se lassent jamais de glorifier Allah\n"
            "• Il faut connaître les 10 grands Anges : Jibrîl, Mîkâ'îl, Isrâfîl et 'Azrâ'îl\n"
            "• Raqîb et 'Atîd inscrivent les paroles et les actes ; Munkar et Nakîr interrogent dans la tombe\n"
            "• Ridwân garde le Paradis et Mâlik garde l'Enfer"
        ),
    },
    (1, 6): {
        "description": "Vers 51 à 57 : La foi aux 104 Livres Célestes révélés par Allah et aux 4 grands Livres majeurs.",
        "explication": (
            "Les vers 51 à 57 exposent le troisième pilier de la foi : croire en tous les Livres révélés par Allah à Ses prophètes.\n\n"
            "Leur nombre total est de 104 Livres sacrés, dont le contenu originel est pure vérité. Parmi eux, 100 sont des Feuillets (Suhuf) "
            "révélés à Adam (10), Seth / Shîth (50), Idrîs (30) et Ibrâhîm (10), auxquels s'ajoutent les 4 grands Livres majeurs :\n"
            "• La Thora (Tawrât) révélée à Moussa (Moïse),\n"
            "• Les Psaumes (Zabûr) révélés à Daoud (David),\n"
            "• L'Évangile (Injîl) révélé à 'Issa (Jésus),\n"
            "• Et le Saint Coran (Al-Furqân), révélé au Sceau des Prophètes Muhammad (ﷺ), qui récapitule, confirme et abroge les législations antérieures."
        ),
        "a_retenir": (
            "• Allah a révélé 104 Livres célestes véridiques à Ses prophètes\n"
            "• Les 4 grands Livres sont : la Thora (Moussa), le Zabûr (Daoud), l'Injîl ('Issa) et le Coran (Muhammad ﷺ)\n"
            "• 100 Feuillets (Suhuf) furent révélés à Adam (10), Shîth (50), Idrîs (30) et Ibrâhîm (10)\n"
            "• Le Saint Coran est la Parole incréée d'Allah, préservée de toute altération jusqu'à la fin des temps"
        ),
    },
    (1, 7): {
        "description": "Vers 58 à 70 : La foi aux Prophètes et Envoyés (Ar-Rusul), leurs qualités obligatoires et les 25 Prophètes cités dans le Coran.",
        "explication": (
            "Dans les vers 58 à 70, Cheikh Ahmadou Bamba présente le quatrième pilier de la foi : la croyance aux Envoyés d'Allah.\n\n"
            "Tous les Prophètes possèdent obligatoirement 3 qualités : la Véracité / Sincérité (Sidq), la Fidélité / Infaillibilité (Amânah) "
            "et la Transmission intégrale du Message (Tablîgh), auxquelles s'ajoute la Sagacité (Fatânah). Leurs contraires (le mensonge, "
            "la trahison et la dissimulation) leur sont absolument impossibles.\n\n"
            "Il est permis à leur sujet d'éprouver les accidents humains qui ne diminuent en rien leur rang élevé (faim, maladie bénigne, mariage). "
            "Le Cheikh rappelle les 25 prophètes mentionnés dans le Coran, couronnés par notre maître Muhammad (ﷺ), le meilleur des êtres créés."
        ),
        "a_retenir": (
            "• Les Envoyés possèdent obligatoirement la Sincérité (Sidq), la Fidélité (Amânah) et la Transmission (Tablîgh)\n"
            "• Le mensonge, la trahison et la dissimulation d'une partie du message leur sont impossibles\n"
            "• Les accidents humains nobles (manger, se marier, maladie non repoussante) sont possibles à leur égard\n"
            "• Allah a envoyé 124 000 prophètes (dont 313 Messagers) ; 25 sont nommés dans le Saint Coran\n"
            "• Le Prophète Muhammad (ﷺ) est le Sceau des Prophètes et le Seigneur des enfants d'Adam"
        ),
    },
    (1, 8): {
        "description": "Vers 71 à 82 : La foi au Jour Ultime (Al-Yawm al-Âkhir) : tombe, Résurrection, Balance, Pont Sirât, Bassin et Demeures éternelles.",
        "explication": (
            "Les vers 71 à 82 décrivent avec précision le cinquième pilier de la foi : la croyance au Jour Dernier et à toutes ses étapes.\n\n"
            "Cela comprend l'interrogatoire dans la tombe, la Résurrection des corps (Ba'th), le Grand Rassemblement (Hashr), la reddition des comptes "
            "(Hisâb), la pesée des œuvres sur la Balance (Mîzân), la remise des Livres des actes (dans la main droite pour les bienheureux), "
            "la traversée du Pont (Sirât) tendu au-dessus de la Géhenne, le Bassin (Hawd) du Prophète (ﷺ), la Grande Intercession (Shafâ'ah), "
            "ainsi que l'éternité du Paradis pour les croyants et le châtiment de l'Enfer. Le Cheikh exhorte l'élève à se réveiller de l'insouciance "
            "en préparant dès aujourd'hui son viatique pour ce Jour solennel."
        ),
        "a_retenir": (
            "• Croire au Jour Ultime implique d'être convaincu de toutes les étapes de l'Au-delà\n"
            "• Étapes clés : la Résurrection, le Grand Rassemblement, la Reddition des comptes et la Balance (Mîzân)\n"
            "• La traversée du Pont Sirât, le Bassin (Hawd) et l'Intercession du Prophète (ﷺ)\n"
            "• La remise des registres des œuvres (main droite pour les élus) et la demeure éternelle au Paradis\n"
            "• La méditation du Jour Dernier éveille le cœur et pousse à l'excellence des actes"
        ),
    },
    (1, 9): {
        "description": "Vers 83 à 92 : La foi au Décret Divin (Al-Qadâ' wa-l-Qadar) et la conclusion lumineuse du chapitre de l'Imân.",
        "explication": (
            "Les vers 83 à 92 couronnent le chapitre de la Foi par son sixième pilier : la croyance au Décret et à la Prédestination d'Allah.\n\n"
            "Le croyant a la certitude absolue que tout ce qui advient dans l'univers — en secret ou en public, le bien comme l'épreuve, "
            "la douceur comme l'amertume — procède exclusivement de la Science éternelle, de la Volonté et de la Puissance d'Allah.\n\n"
            "Cette foi procure au cœur une sérénité inébranlable : le croyant fournit les efforts prescrits par la Loi divine tout en s'en "
            "remettant totalement à son Seigneur, sans orgueil dans la réussite ni désespoir dans l'épreuve."
        ),
        "a_retenir": (
            "• 6e pilier de la Foi : croire au Décret Divin (Al-Qadâ' wa-l-Qadar)\n"
            "• Tout ce qui arrive dans l'univers procède de la Volonté et de la Science éternelle d'Allah\n"
            "• Nul ne peut repousser ce qu'Allah a décrété, ni empêcher ce qu'Il a destiné\n"
            "• La foi au destin allie l'effort responsable (respect des commandements) et la confiance sereine (Tawakkul)\n"
            "• Ainsi s'achèvent les 6 piliers de l'Imân : Allah, Ses Anges, Ses Livres, Ses Envoyés, le Jour Ultime et le Décret"
        ),
    },
    (1, 10): {
        "description": "Synthèse Magistrale & Épreuve Intensive de la Grande Étape 1 (Vers 1 à 92 : Imân & Tawhîd).",
        "texte_source": (
            "۞ SYNTHÈSE DES VERS 1 À 92 — BÂB AL-IMÂN WA-T-TAWHÎD ۞\n\n"
            "« Les parties qui composent la Religion de notre SEIGNEUR sont : la Profession de Foi (Imân), "
            "les Pratiques Cultuelles de Soumission à DIEU (Islâm) et la Perfection Spirituelle (Ihsân)...\n"
            "Puisse DIEU te guider par l'Onction de la Profession : IL N'Y A DE DIEU QU'ALLAH, MUHAMMAD EST L'ENVOYÉ D'ALLAH ! »"
        ),
        "explication": (
            "Cette étape de Révision Intensive valide votre maîtrise complète de la Grande Étape 1 (Les Fondations de la Foi).\n\n"
            "Avant de lancer le quiz intensif, assurez-vous de maîtriser :\n"
            "1. L'intention de Cheikh Ahmadou Bamba et ses conseils aux adolescents (droiture, science, révision, fuite des futilités).\n"
            "2. Les 3 parties de la Religion : Imân, Islâm, Ihsân.\n"
            "3. Les 41 Attributs relatifs à la Connaissance d'Allah (20 nécessaires, 20 impossibles, 1 possible).\n"
            "4. Les 10 Anges nommés, les 104 Livres révélés (dont les 4 majeurs), les qualités des Envoyés, les étapes du Jour Ultime et le Décret Divin."
        ),
        "a_retenir": (
            "• 3 parties de la Religion : Imân (Foi), Islâm (Pratique), Ihsân (Perfection spirituelle)\n"
            "• 41 Attributs à connaître : 20 nécessaires à Allah, 20 impossibles, 1 possible\n"
            "• 10 Anges à connaître nommément (Jibrîl, Mîkâ'îl, Isrâfîl, 'Azrâ'îl, Raqîb, 'Atîd, Munkar, Nakîr, Ridwân, Mâlik)\n"
            "• 104 Livres célestes dont 4 majeurs : Thora, Zabûr, Injîl et le Saint Coran\n"
            "• 3 qualités obligatoires des Prophètes : Sincérité (Sidq), Fidélité (Amânah), Transmission (Tablîgh)\n"
            "• 6 piliers de la Foi : Allah, les Anges, les Livres, les Envoyés, le Jour Ultime et le Décret Divin"
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # MODULE 2 : LES BASES DE LA PRATIQUE (ISLÂM - 1)
    # ══════════════════════════════════════════════════════════════════
    (2, 1): {
        "description": "Vers 93 à 94 : Définition d'Al-Islâm et énumération des 5 Piliers pratiques de la soumission à Allah.",
        "explication": (
            "Avec les vers 93 et 94 s'ouvre la deuxième grande partie du livre consacrée à Al-Islâm (la Soumission pratique par les œuvres).\n\n"
            "Cheikh Ahmadou Bamba enseigne aux adolescents que l'Islâm repose sur cinq colonnes fondamentales :\n"
            "1. La mention du Nom d'Allah par l'attestation de foi (Shahâdah / Dhikr),\n"
            "2. L'accomplissement assidu des cinq Prières canoniques (Salât),\n"
            "3. Le Jeûne du mois béni de Ramadan (Siyâm),\n"
            "4. L'acquittement de l'Aumône légale purificatrice (Zakât),\n"
            "5. Le Pèlerinage à la Maison Sacrée de La Mecque (Hajj) pour celui qui en a la capacité."
        ),
        "a_retenir": (
            "• Al-Islâm désigne la soumission active à Allah par l'observance des actes cultuels\n"
            "• 1er pilier : Le témoignage de Foi (Lâ ilâha illâ Allâh, Muhammadun Rasûlullâh)\n"
            "• 2e pilier : L'accomplissement des 5 Prières quotidiennes aux heures prescrites\n"
            "• 3e et 4e piliers : Le Jeûne du mois de Ramadan et l'Aumône légale (Zakât)\n"
            "• 5e pilier : Le Pèlerinage à La Mecque (Hajj) pour qui en a les moyens"
        ),
    },
    (2, 2): {
        "description": "Vers 95 à 98 : La primauté de la Shahâdah, la meilleure formule de Dhikr qui purifie le cœur.",
        "explication": (
            "Les vers 95 à 98 approfondissent le premier pilier de l'Islâm : la formule « Lâ ilâha illâ Allâh, Muhammadun Rasûlullâh ».\n\n"
            "Le Cheikh rappelle que cette parole bénie constitue le plus noble et le plus méritoire de tous les Dhikr (mentions d'Allah). "
            "Prononcée avec sincérité, certitude et compréhension, elle efface les fautes, illumine le cœur du croyant et constitue "
            "la clé du Paradis et du salut éternel."
        ),
        "a_retenir": (
            "• La Shahâdah est la clé d'entrée dans l'Islâm et le sceau du salut\n"
            "• « Lâ ilâha illâ Allâh » est la plus excellente formule de Dhikr\n"
            "• Elle associe l'attestation de l'Unicité divine et la reconnaissance de la mission prophétique de Muhammad (ﷺ)\n"
            "• La mention constante d'Allah (Dhikr) apaise les cœurs et fortifie la foi"
        ),
    },
    (2, 3): {
        "description": "Vers 99 à 115 : Le caractère sacré des 5 prières obligatoires et la gravité extrême de leur négligence.",
        "explication": (
            "Dans les vers 99 à 115, Cheikh Ahmadou Bamba consacre un développement solennel à l'obligation des cinq prières quotidiennes.\n\n"
            "Établies par le Coran, la Sunnah et le Consensus unanime des savants (Ijmâ'), les cinq prières sont la colonne vertébrale de la religion. "
            "Le Cheikh met sévèrement en garde contre toute négligence ou retard volontaire : celui qui abandonne la prière par négation de son "
            "caractère obligatoire sort de l'Islâm, et celui qui la délaisse par paresse s'expose à un péril immense ici-bas et dans l'Au-delà. "
            "Chaque prière doit être accomplie dans son temps prescrit avec humilité et recueillement (Khushû')."
        ),
        "a_retenir": (
            "• L'obligation des 5 prières est prouvée par le Coran, la Sunnah et le Consensus (Ijmâ')\n"
            "• Les 5 prières quotidiennes sont : Subh (Fajr), Dhuhr, 'Asr, Maghrib et 'Ishâ'\n"
            "• La prière est le premier acte sur lequel le serviteur sera jugé au Jour de la Résurrection\n"
            "• Il est impératif d'accomplir chaque prière dès l'entrée de son heure légale\n"
            "• Accomplir la prière avec recueillement préserve de la turpitude et du blâmable"
        ),
    },
    (2, 4): {
        "description": "Vers 116 à 118 : L'obligation préalable de la Pureté Légale (At-Tahârah) avant toute prière.",
        "explication": (
            "Les vers 116 à 118 établissent la règle d'or de la purification : « La clé de la prière est la pureté ».\n\n"
            "Se purifier de la souillure rituelle (Hadath mineur ou majeur) et de l'impureté matérielle (Khabath / Najâsah) est une obligation "
            "formelle avant d'entrer en prière. Celui qui prie volontairement sans purification voit son acte rejeté. La pureté concerne à la fois "
            "le corps du prieur, ses vêtements et l'emplacement où il se prosterne."
        ),
        "a_retenir": (
            "• La purification (Tahârah) est la condition sine qua non de validité de la prière\n"
            "• On distingue la pureté du Hadath (par le Wudû', le Ghusl ou le Tayammum) et la pureté du Khabath\n"
            "• Trois éléments doivent être purs de toute souillure : le corps, le vêtement et le lieu de prière\n"
            "• La pureté extérieure prépare l'âme à la pureté intérieure devant Allah"
        ),
    },
    (2, 5): {
        "description": "Vers 119 à 163 : Pureté intérieure, garde des 7 membres, conditions du Repentir (Tawbah) et science des obligations.",
        "explication": (
            "Ce grand enseignement (vers 119 à 163) relie le Fiqh extérieur à la purification spirituelle du cœur.\n\n"
            "1. La garde des 7 membres : Cheikh Ahmadou Bamba explique que la vraie prière exige aussi de préserver ses sept organes "
            "contre la désobéissance : la langue (médisance, mensonge), les oreilles, les yeux (regards illicites), le ventre (nourriture illicite), "
            "les mains, les pieds et le sexe.\n\n"
            "2. Le Repentir (At-Tawbah) : Toute faute doit être immédiatement effacée par un repentir sincère réunissant le regret profond, "
            "l'abandon immédiat du péché, la ferme résolution de ne plus y revenir et la réparation des droits d'autrui.\n\n"
            "3. Science avant l'action : Enfin, nul acte cultuel n'est agréé si l'on ignore la distinction entre ses actes obligatoires (Fard) "
            "et ses actes traditionnels (Sunnah)."
        ),
        "a_retenir": (
            "• Préserver les 7 membres du péché : langue, yeux, oreilles, ventre, mains, pieds et sexe\n"
            "• Veiller scrupuleusement à la licéité (Halâl) de sa nourriture et de ses vêtements\n"
            "• Conditions du Repentir (Tawbah) : regret sincère, arrêt immédiat, résolution de ne plus recommencer et restitution des droits\n"
            "• L'orgueil, l'ostentation (Riyâ'), l'envie (Hasad) et la médisance annulent la récompense des œuvres\n"
            "• Il est obligatoire d'apprendre à distinguer les Farâ'id (obligations) des Sunan (traditions) dans ses adorations"
        ),
    },
    (2, 6): {
        "description": "Synthèse Magistrale & Épreuve Intensive de la Grande Étape 2 (Vers 93 à 163 : Piliers, Pureté, 7 Membres & Repentir).",
        "texte_source": (
            "۞ SYNTHÈSE DES VERS 93 À 163 — BÂB AL-ISLÂM WA-T-TAZKIYAH ۞\n\n"
            "« Votre soumission (Al-Islâm) — ô adolescents ! — consiste en la mention du Nom de DIEU, les cinq Prières, "
            "le Jeûne de Ramadan, l'Aumône légale et le Pèlerinage...\n"
            "Préservez vos sept organes des péchés et hâtez-vous vers un repentir sincère ! »"
        ),
        "explication": (
            "Cette étape de Révision Intensive récapitule toute la Grande Étape 2.\n\n"
            "Points essentiels à maîtriser :\n"
            "• Les 5 piliers de l'Islâm et l'excellence de la Shahâdah.\n"
            "• Le statut des 5 prières et les 3 réceptacles de la pureté (corps, vêtement, lieu).\n"
            "• Les 7 organes à préserver du péché (langue, yeux, oreilles, ventre, mains, pieds, sexe).\n"
            "• Les conditions du repentir sincère (Tawbah) et l'obligation de connaître les règles du Fard et de la Sunnah avant d'agir."
        ),
        "a_retenir": (
            "• Les 5 piliers de l'Islâm : Shahâdah, Salât, Siyâm, Zakât, Hajj\n"
            "• La pureté (Tahârah) exige la propreté du corps, des habits et du lieu de prière\n"
            "• Les 7 membres à garder : langue, oreilles, yeux, ventre, mains, pieds et sexe\n"
            "• Le repentir (Tawbah) est une obligation immédiate après tout manquement\n"
            "• Connaître la différence entre Fard (obligatoire) et Sunnah (traditionnel) conditionne la validité de l'adoration"
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # MODULE 3 : LA PRIÈRE ET LA PURIFICATION EN DÉTAIL (ISLÂM - 2)
    # ══════════════════════════════════════════════════════════════════
    (3, 1): {
        "description": "Vers 164 à 173 : Les 15 Actes Obligatoires (Farâ'id) de la Prière selon la jurisprudence malikite.",
        "explication": (
            "Dans les vers 164 à 173, Cheikh Ahmadou Bamba énumère avec une clarté remarquable les **15 Actes Obligatoires (Farâ'id)** "
            "de la prière selon l'imam Al-'Awfî (école malikite).\n\n"
            "Ces 15 piliers indispensables sont :\n"
            "1. La formulation de l'intention (Niyyah),\n"
            "2. Le Takbîr al-Ihrâm (« Allâhu Akbar » d'entrée en prière),\n"
            "3. Se tenir debout (Qiyâm) pour ce Takbîr,\n"
            "4. La récitation de la Fâtihah,\n"
            "5. Se tenir debout pendant la Fâtihah,\n"
            "6. L'inclinaison (Rukû'),\n"
            "7. Le redressement après l'inclinaison (Raf' min ar-rukû'),\n"
            "8. La prosternation (Sujûd) sur le front,\n"
            "9. Le redressement entre les deux prosternations,\n"
            "10. L'assise finale pour le Salâm,\n"
            "11. Le Salâm final (« As-salâmu 'alaykum »),\n"
            "12. La sérénité / stabilité des membres dans chaque posture (Tuma'nînah),\n"
            "13. L'équilibre / droiture en se redressant (I'tidâl),\n"
            "14. Le respect de l'ordre séquentiel des actes (Tartîb),\n"
            "15. L'intention de suivre l'Imam pour celui qui prie en groupe."
        ),
        "a_retenir": (
            "• La prière compte 15 Actes Obligatoires (Farâ'id) dont l'omission volontaire annule la prière\n"
            "• Entrée : Intention (Niyyah), Takbîr al-Ihrâm et station debout\n"
            "• Récitation : Lecture intégrale de la Sourate Al-Fâtihah en station debout\n"
            "• Mouvements : Rukû' (inclinaison), redressement, Sujûd (prosternation) et assise entre les deux\n"
            "• Clôture et tenue : Assise finale, Salâm, sérénité (Tuma'nînah), équilibre (I'tidâl) et ordre des actes"
        ),
    },
    (3, 2): {
        "description": "Vers 174 à 186 : Les Actes Traditionnels (Sunan) de la Prière et les 8 Sunnah Mu'akkadah.",
        "explication": (
            "Les vers 174 à 186 présentent les **Actes Traditionnels (Sunan)** de la prière, symbolisés par les lettres « Hayyun » (18 en tout, "
            "dont **8 Sunnah Mu'akkadah** fortement recommandées symbolisées par la lettre Hâ' = 8).\n\n"
            "Parmi ces traditions figurent : l'Iqâmah, la récitation d'une sourate (ou passage du Coran) après la Fâtihah dans les deux "
            "premières Rak'ât, la station debout pour cette sourate, la lecture à voix haute (Jahr) ou à voix basse (Sirr) selon la prière, "
            "les Takbîrât de transition (autres que celui d'entrée), la parole « Sami'a Allâhu liman hamidah », le premier et le second "
            "Tashahhud, l'assise pour le Tashahhud, et la prière sur le Prophète (ﷺ) lors du dernier Tashahhud."
        ),
        "a_retenir": (
            "• La prière comporte 18 actes traditionnels (Sunan), dont 8 Sunnah Mu'akkadah majeures\n"
            "• Réciter une Sourate après la Fâtihah lors des deux premières unités (Rak'ât)\n"
            "• Respecter la voix haute (Subh, Maghrib, 'Ishâ') et la voix basse (Dhuhr, 'Asr)\n"
            "• Dire « Sami'a Allâhu liman hamidah » en se relevant du Rukû' et prononcer les Takbîrât de mouvement\n"
            "• Accomplir le premier et le second Tashahhud ainsi que la Salât sur le Prophète (ﷺ)"
        ),
    },
    (3, 3): {
        "description": "Vers 187 à 197 : Les Ablutions mineures (Wudû' : 7 obligations, 8 traditions) et le Bain rituel (Ghusl : 5 obligations, 4 traditions).",
        "explication": (
            "Les vers 187 à 197 détaillent avec précision les deux purifications par l'eau :\n\n"
            "1. **L'Ablution mineure (Wudû')** :\n"
            "• **7 Obligations (Farâ'id)** : l'intention, le lavage du visage, le lavage des mains et avant-bras jusqu'aux coudes, "
            "l'essuyage (Mash) de toute la tête, le lavage des pieds jusqu'aux chevilles, le frottement (Dalk) et la continuité immédiate (Fawr).\n"
            "• **8 Traditions (Sunan)** : se laver les mains au début (3 fois), se rincer la bouche (Madmadah), aspirer et rejeter l'eau des narines "
            "(Istinshâq / Istinthâr), revenir en arrière lors de l'essuyage de la tête, essuyer les oreilles, renouveler l'eau pour les oreilles "
            "et respecter l'ordre des membres.\n\n"
            "2. **La Purification majeure (Ghusl)** :\n"
            "• **5 Obligations** : l'intention, le lavage intégral de tout le corps, le frottement (Dalk), la continuité (Fawr) et le démêlage "
            "des cheveux (Takhlîl).\n"
            "• **4 Traditions** : se laver les mains au début, se rincer la bouche, nettoyer les narines et essuyer l'intérieur des oreilles."
        ),
        "a_retenir": (
            "• Wudû' (Ablutions) : 7 Obligations (Intention, visage, bras aux coudes, essuyage tête, pieds aux chevilles, frottement, continuité)\n"
            "• Wudû' : 8 Traditions (Lavage initial des mains, bouche, nez, retour sur la tête, oreilles, eau neuve pour les oreilles, ordre)\n"
            "• Ghusl (Bain rituel) : 5 Obligations (Intention, laver tout le corps, frottement, continuité, pénétrer les cheveux)\n"
            "• Ghusl : 4 Traditions (Se laver les mains au début, rincer la bouche, nettoyer les narines, essuyer le trou des oreilles)"
        ),
    },
    (3, 4): {
        "description": "Vers 198 à 205 : La Lustration Pulvérale (At-Tayammum) : ses 8 obligations et ses 3 actes traditionnels.",
        "explication": (
            "Dans les vers 198 à 205, Cheikh Ahmadou Bamba expose les règles du **Tayammum** (purification par la terre/sable pur) "
            "lorsque l'eau manque ou que son usage est médicalement dangereux.\n\n"
            "• **Les 8 Obligations du Tayammum** (symbolisées par la lettre Hâ' = 8) : 1. L'intention, 2. L'utilisation d'un support minéral pur "
            "(Sa'îd Tâhir : sable, pierre, terre non altérée), 3. La première pose des mains sur le sol, 4. L'essuyage de tout le visage, "
            "5. L'essuyage des mains jusqu'aux poignets, 6. La continuité immédiate (Fawr), 7. L'accomplissement après l'entrée de l'heure "
            "de la prière, et 8. L'enchaînement direct avec la prière.\n"
            "• **Les 3 Traditions du Tayammum** : 1. Respecter l'ordre (visage puis mains), 2. La seconde pose des mains sur le sol, "
            "et 3. L'essuyage des avant-bras des poignets jusqu'aux coudes."
        ),
        "a_retenir": (
            "• Le Tayammum remplace l'eau en cas d'absence d'eau ou d'incapacité médicale de l'utiliser\n"
            "• Il comporte 8 Obligations : Intention, sol pur (Sa'îd Tâhir), 1re frappe, essuyer le visage, essuyer les poignets, continuité, entrée de l'heure, liaison à la prière\n"
            "• Il comporte 3 Traditions : Ordre (visage puis mains), 2e frappe sur le sol et essuyage jusqu'aux coudes\n"
            "• Le Tayammum illustre la miséricorde et la facilité de la Loi islamique"
        ),
    },
    (3, 5): {
        "description": "Synthèse Magistrale & Épreuve Intensive de la Grande Étape 3 (Vers 164 à 205 : Prière, Wudû', Ghusl & Tayammum).",
        "texte_source": (
            "۞ SYNTHÈSE DES VERS 164 À 205 — BÂB AS-SALÂT WA-T-TAHÂRAH ۞\n\n"
            "« Les Actes Obligatoires de la prière sont au nombre de quinze, d'après ce qu'a mentionné Al-'Awfî...\n"
            "Les Obligations de nos Ablutions sont sept, celles du Bain rituel sont cinq, et celles du Tayammum sont huit. »"
        ),
        "explication": (
            "Cette étape de Révision Intensive valide votre maîtrise des chiffres et règles d'or du Fiqh de la Prière et de la Purification :\n"
            "• Prière : 15 Obligations (Farâ'id) et 18 Traditions (dont 8 Sunnah Mu'akkadah).\n"
            "• Wudû' (Ablutions mineures) : 7 Obligations et 8 Traditions.\n"
            "• Ghusl (Purification majeure) : 5 Obligations et 4 Traditions.\n"
            "• Tayammum (Lustration pulvérale) : 8 Obligations et 3 Traditions."
        ),
        "a_retenir": (
            "• Prière : 15 Obligations (Farâ'id) + 18 Traditions (dont 8 Sunnah Mu'akkadah)\n"
            "• Wudû' : 7 Obligations + 8 Traditions (visage, bras aux coudes, tête, pieds aux chevilles, Dalk, Fawr)\n"
            "• Ghusl : 5 Obligations + 4 Traditions (intention, corps entier, Dalk, Fawr, démêlage des cheveux)\n"
            "• Tayammum : 8 Obligations + 3 Traditions (terre pure, 1re frappe, visage, poignets, heure entrée)"
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # MODULE 4 : JEÛNE, ZAKAT, PÈLERINAGE & RATTRAPAGE (ISLÂM - 3)
    # ══════════════════════════════════════════════════════════════════
    (4, 1): {
        "description": "Vers 206 à 209 : Le Jeûne (As-Siyâm) : ses 2 obligations fondamentales et ses 3 actes traditionnels.",
        "explication": (
            "Les vers 206 à 209 exposent avec concision les règles du **Jeûne (As-Siyâm)** :\n\n"
            "• **Les 2 Obligations du Jeûne** :\n"
            "1. La formulation de l'intention (Niyyah) avant l'aube,\n"
            "2. L'abstention totale (Imsâk), depuis l'apparition de l'aube véridique (Fajr) jusqu'au coucher complet du soleil (Maghrib), "
            "de tout ce qui rompt le jeûne (nourriture, boisson et rapports conjugaux).\n\n"
            "• **Les 3 Actes Traditionnels (Sunan) du Jeûne** :\n"
            "1. Hâter la rupture du jeûne (Iftâr) dès que le coucher du soleil est certain,\n"
            "2. Retarder le dernier repas nocturne (Suhûr) vers la fin de la nuit avant l'aube,\n"
            "3. Préserver sa langue de toute parole vaine ou blessante pendant le jeûne."
        ),
        "a_retenir": (
            "• Le Jeûne comporte exactement 2 Obligations : l'Intention (Niyyah) et l'Abstention (Imsâk) de l'aube au coucher du soleil\n"
            "• Il comporte 3 Traditions (Sunan) : hâter l'Iftâr au coucher du soleil, retarder le Suhûr avant l'aube, et retenir sa langue du mal\n"
            "• Le jeûne éduque l'âme à la maîtrise de soi et à la piété (Taqwâ)"
        ),
    },
    (4, 2): {
        "description": "Vers 210 à 214 : L'Aumône Légale (Az-Zakât) : ses 4 obligations et ses 3 règles traditionnelles.",
        "explication": (
            "Les vers 210 à 214 détaillent le quatrième pilier de l'Islâm : **l'Aumône Légale (Az-Zakât)**.\n\n"
            "• **Les 4 Obligations de la Zakât** :\n"
            "1. La formulation de l'intention au moment du prélèvement,\n"
            "2. L'écoulement d'une année lunaire complète (Hawl) ou la maturité de la récolte,\n"
            "3. L'atteinte du seuil minimal imposable (Nisâb),\n"
            "4. Le refus de la disperser hors du lieu où elle est due (sauf nécessité légale) et sa remise aux ayants droit légitimes.\n\n"
            "• **Les 3 Traditions de la Zakât** : l'acquitter de bon cœur sans reproche, choisir parmi ses biens de bonne qualité, "
            "et éviter l'ostentation afin de préserver la dignité du bénéficiaire."
        ),
        "a_retenir": (
            "• La Zakât compte 4 Obligations : l'Intention, l'échéance annuelle (Hawl), l'atteinte du Nisâb (seuil imposable) et la distribution sur place aux ayants droit\n"
            "• Elle compte 3 Traditions : donner de bon gré, prélever sur des biens sains et agir avec discrétion\n"
            "• La Zakât purifie les biens du donateur et renforce la solidarité fraternelle"
        ),
    },
    (4, 3): {
        "description": "Vers 215 à 231 : Le Pèlerinage à La Mecque (Al-Hajj) : ses 4 piliers obligatoires et ses 12 traditions.",
        "explication": (
            "Dans les vers 215 à 231, Cheikh Ahmadou Bamba expose les rites du **Pèlerinage à la Maison Sacrée d'Allah (Al-Hajj)**.\n\n"
            "• **Les 4 Piliers Obligatoires (Arkân) du Hajj** (dont l'omission ne peut être compensée par une offrande) :\n"
            "1. L'entrée en état de sacralisation avec l'intention (Ihrâm),\n"
            "2. La procession circumambulatoire d'affluence autour de la Ka'bah (Tawâf al-Ifâdah),\n"
            "3. Le parcours rapide (Sa'y) entre les collines d'As-Safâ et d'Al-Marwah,\n"
            "4. La station solennelle sur le mont 'Arafât (Wuqûf bi-'Arafah).\n\n"
            "• Le Cheikh détaille également les **12 traditions (Sunan)** rattachées à ces rites (4 lors de l'Ihrâm : bain, vêtements sans couture, "
            "prière de 2 Rak'ât, Talbiyah ; 4 lors du Tawâf : marche à pied, baiser la Pierre Noire, allure vive des hommes lors des 3 premiers tours, "
            "invocations ; et 4 lors du Sa'y : baiser la Pierre avant de sortir, monter sur Safâ et Marwah, hâter le pas entre les deux bornes vertes, "
            "et invoquer Allah sur les deux collines)."
        ),
        "a_retenir": (
            "• Les 4 Piliers Obligatoires du Hajj : 1. L'Ihrâm (intention), 2. Le Tawâf al-Ifâdah, 3. Le Sa'y entre Safâ et Marwah, 4. La station à 'Arafât\n"
            "• 4 Traditions de l'Ihrâm : Ghusl préalable, habits sans couture, 2 Rak'ât et prononciation de la Talbiyah\n"
            "• 4 Traditions du Tawâf : marcher à pied, saluer la Pierre Noire, pas pressé (Raml) aux 3 premiers tours et invocations\n"
            "• 4 Traditions du Sa'y : monter sur Safâ et Marwah, hâter le pas dans la vallée centrale et multiplier les invocations"
        ),
    },
    (4, 4): {
        "description": "Vers 232 à 273 : Invocations des ablutions, rattrapage des prières derrière l'Imam (Al-Masbûq) et prière du malade.",
        "explication": (
            "Cette leçon très riche (vers 232 à 273) regroupe des enseignements pratiques indispensables au quotidien :\n\n"
            "1. **L'invocation après les ablutions** (vers 232-235) : Celui qui prononce la Shahâdah et l'invocation prophétique après son Wudû' "
            "voit les huit portes du Paradis s'ouvrir pour lui.\n\n"
            "2. **Le rattrapage des Rak'ât manquées derrière l'Imam (Al-Masbûq)** (vers 236-263) : Règle fondamentale malikite : "
            "on rattrape la **récitation** (Al-Qadâ' fî al-aqwâl) et l'on bâtit les **assises** (Al-Binâ' fî al-af'âl). "
            "Le Cheikh détaille cas par cas comment compléter Subh, Dhuhr, 'Asr, Maghrib et 'Ishâ' lorsqu'on rejoint l'Imam en cours de prière, "
            "ainsi que le nombre de Rak'ât des prières surérogatoires (Fajr, Witr).\n\n"
            "3. **La prière du malade** (vers 264-273) : Selon sa capacité, le malade prie debout (avec ou sans appui), sinon assis, "
            "sinon couché sur le côté droit, le côté gauche ou sur le dos face à la Qiblah."
        ),
        "a_retenir": (
            "• Dire la Shahâdah après ses ablutions ouvre les 8 portes du Paradis\n"
            "• Règle du retardataire (Masbûq) : rattraper la récitation (Qadâ') et bâtir les postures d'assise (Binâ')\n"
            "• Pour obtenir une Rak'ah avec l'Imam, il faut le rejoindre avant qu'il ne se relève de l'inclinaison (Rukû')\n"
            "• Le malade prie selon sa capacité : debout, debout avec appui, assis en tailleur, assis appuyé, ou allongé face à la Qiblah"
        ),
    },
    (4, 5): {
        "description": "Synthèse Magistrale & Épreuve Intensive de la Grande Étape 4 (Vers 206 à 273 : Jeûne, Zakât, Hajj & Rattrapage).",
        "texte_source": (
            "۞ SYNTHÈSE DES VERS 206 À 273 — BÂB AS-SIYÂM WA-Z-ZAKÂT WA-L-HAJJ ۞\n\n"
            "« Notre Jeûne comporte deux Obligations... Quant à l'Aumône Légale, on compte ses Obligations au nombre de quatre...\n"
            "Les Actes Obligatoires du Pèlerinage sont au nombre de quatre : l'Ihrâm, le Tawâf, le Sa'y et la station à 'Arafât. »"
        ),
        "explication": (
            "Cette étape de Révision Intensive valide votre maîtrise de la Grande Étape 4 :\n"
            "• Jeûne (Siyâm) : 2 Obligations (Intention + Abstention) et 3 Traditions.\n"
            "• Aumône Légale (Zakât) : 4 Obligations et 3 Traditions.\n"
            "• Pèlerinage (Hajj) : 4 Piliers Obligatoires et 12 Traditions (4 pour l'Ihrâm, 4 pour le Tawâf, 4 pour le Sa'y).\n"
            "• Règles du retardataire derrière l'Imam (Masbûq) et ordre des postures de la prière du malade."
        ),
        "a_retenir": (
            "• Jeûne : 2 Obligations (Intention, Abstention) + 3 Traditions (hâter l'Iftâr, retarder le Suhûr, garder sa langue)\n"
            "• Zakât : 4 Obligations (Intention, année Hawl, seuil Nisâb, non-dispersion) + 3 Traditions\n"
            "• Hajj : 4 Piliers Obligatoires (Ihrâm, Tawâf, Sa'y Safâ-Marwah, station à 'Arafât) + 12 Traditions\n"
            "• Retardataire (Masbûq) : une Rak'ah est acquise si l'on rejoint l'Imam dans le Rukû'\n"
            "• Prière du malade : graduation ordonnée de la station debout jusqu'à la position allongée"
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # MODULE 5 : LA PERFECTION SPIRITUELLE (IHSÂN & TASAWWUF)
    # ══════════════════════════════════════════════════════════════════
    (5, 1): {
        "description": "Vers 274 à 276 : Définition d'Al-Ihsân, le sommet de la présence spirituelle et de la vigilance du cœur.",
        "explication": (
            "Les vers 274 à 276 ouvrent la cinquième et dernière grande partie du livre, consacrée à **Al-Ihsân (la Perfection Spirituelle "
            "et le Soufisme authentique)**.\n\n"
            "Cheikh Ahmadou Bamba rappelle la définition prophétique : « L'Ihsân consiste à adorer Allah comme si tu Le voyais ; car même si "
            "tu ne Le vois pas, Lui, certes, te voit ». Cette conscience permanente du Regard divin (Murâqabah) transforme chaque acte "
            "d'adoration en une rencontre vivante, empreinte de révérence, de pudeur et de sincérité absolue."
        ),
        "a_retenir": (
            "• Al-Ihsân est le degré d'excellence spirituelle qui couronne l'Imân et l'Islâm\n"
            "• Il consiste à adorer Allah comme si on Le voyait (station de contemplation — Mushâhadah)\n"
            "• À défaut de Le voir, avoir la certitude constante qu'Allah nous voit à chaque instant (station de vigilance — Murâqabah)\n"
            "• L'Ihsân purifie le cœur de toute hypocrisie et de toute négligence"
        ),
    },
    (5, 2): {
        "description": "Vers 277 à 292 : Les nobles vertus du Tasawwuf et la nécessité d'un Guide Spirituel Éclairé (Cheikh de Tarbiyah).",
        "explication": (
            "Dans les vers 277 à 292, Cheikh Ahmadou Bamba livre une véritable charte d'éducation spirituelle (Tarbiyah).\n\n"
            "Il recommande à l'aspirant qui souhaite s'élever vers les hauts degrés spirituels de se parer des plus nobles vertus : "
            "la science ('Ilm), le scrupule pieux (Wara'), la gratitude (Shukr), la sincérité pure (Ikhlâs), la générosité, la patience (Sabr), "
            "le silence méditatif et la maîtrise de ses passions.\n\n"
            "Surtout, il souligne l'importance capitale de confier son éducation spirituelle à un **Guide Éclairé et Véridique (Shaykh Murabbî)** "
            "qui connaît les maladies de l'âme et leurs remèdes, afin de conduire le disciple en sécurité vers l'Agrément d'Allah."
        ),
        "a_retenir": (
            "• Les piliers de l'élévation spirituelle : Science, Scrupule (Wara'), Gratitude, Sincérité (Ikhlâs) et Patience\n"
            "• Moins parler, moins dormir et moins manger (dans la juste mesure prophétique) illuminent le cœur\n"
            "• S'attacher à un Guide Spirituel Éclairé (Cheikh) permet de guérir les défauts cachés de l'âme (Nafs)\n"
            "• Se conformer aux conseils du maître spirituel avec respect, constance et humilité"
        ),
    },
    (5, 3): {
        "description": "Vers 293 à 308 : Saisir les 5 situations précieuses avant leurs 5 contraires, et l'Épilogue béni de l'ouvrage.",
        "explication": (
            "Dans ce final lumineux (vers 293 à 308), Cheikh Ahmadou Bamba transmet aux jeunes la célèbre exhortation du Prophète (ﷺ) :\n"
            "« Tirez profit de cinq situations avant que cinq autres ne vous surviennent » :\n"
            "1. Votre **jeunesse** avant votre vieillesse,\n"
            "2. Votre **bonne santé** avant votre maladie,\n"
            "3. Votre **richesse (aisance)** avant votre dénuement,\n"
            "4. Votre **temps libre** avant vos préoccupations,\n"
            "5. Votre **vie** avant votre mort.\n\n"
            "Car après cette vie terrestre, il n'existe plus que deux demeures : le Paradis éternel ou l'Enfer. Le Cheikh conclut son ouvrage "
            "en implorant Allah d'accorder à tout lecteur et étudiant de ce Viatique une foi inébranlable, une bonne fin (Husn al-Khâtimah) "
            "et le salut éternel, avant de clore par la Louange à Allah et la Prière sur le Prophète (ﷺ)."
        ),
        "a_retenir": (
            "• Saisir 5 trésors avant leurs 5 contraires selon la recommandation du Prophète (ﷺ) :\n"
            "• 1. La jeunesse avant la vieillesse · 2. La santé avant la maladie\n"
            "• 3. L'aisance avant la pauvreté · 4. Le temps libre avant l'occupation\n"
            "• 5. La vie terrestre avant la mort (car l'Au-delà est l'heure des comptes et non des œuvres)\n"
            "• Clôture du Viatique par l'invocation pour une fin heureuse (Husn al-Khâtimah) et la Salât sur le Prophète (ﷺ)"
        ),
    },
    (5, 4): {
        "description": "Synthèse Magistrale & Épreuve Intensive de la Grande Étape 5 (Vers 274 à 308 : Ihsân, Vertus, Guide & 5 Situations).",
        "texte_source": (
            "۞ SYNTHÈSE DES VERS 274 À 308 — BÂB AL-IHSÂN WA-L-KHÂTIMAH ۞\n\n"
            "« Votre Perfection Spirituelle — ô adolescents ! — consiste à adorer DIEU comme si vous Le voyiez...\n"
            "Exploitez cinq situations bien avant leurs cinq alternatives : votre jeunesse avant la vieillesse, "
            "votre santé avant la maladie, votre richesse avant la pauvreté, votre temps libre avant l'occupation "
            "et votre vie avant la mort ! »"
        ),
        "explication": (
            "Cette étape de Révision Intensive couronne la Cinquième Grande Étape du livre :\n"
            "• Définition de l'Ihsân (Mushâhadah et Murâqabah).\n"
            "• Les vertus cardinales du disciple (science, scrupule, sincérité, gratitude) et le rôle du Guide Spirituel (Cheikh).\n"
            "• Les 5 opportunités précieuses de l'existence à saisir avant leurs 5 contraires et les invocations finales de Cheikh Ahmadou Bamba."
        ),
        "a_retenir": (
            "• Al-Ihsân : adorer Allah comme si tu Le voyais, car Lui te voit à tout instant\n"
            "• Vertus du disciple : Science ('Ilm), Scrupule (Wara'), Sincérité (Ikhlâs), Gratitude (Shukr)\n"
            "• Nécessité d'un Guide Spirituel Éclairé (Cheikh) pour l'éducation de l'âme (Tarbiyah)\n"
            "• Les 5 opportunités : Jeunesse, Santé, Richesse, Temps libre et Vie avant leurs 5 contraires\n"
            "• Tazawwudu-ç-Çighâr compte 308 vers réunissant l'Imân, l'Islâm et l'Ihsân"
        ),
    },
    (5, 99): {
        "description": "Grande Synthèse Générale de l'Ouvrage (Vers 1 à 308) — Examen de Maîtrise de Tazawwudu-ç-Çighâr (100+ questions variées).",
        "texte_source": (
            "۞ KHÂTIMAT AL-KITÂB — SYNTHÈSE GÉNÉRALE DES 308 VERS DE TAZAWWUDU-Ç-ÇIGHÂR ۞\n\n"
            "1. Bâb al-Muqaddimah wa-l-Imân (Vers 1 à 92) : Intention, 3 parties de la Religion, 41 Attributs, 6 Piliers de la Foi.\n"
            "2. Bâb al-Islâm wa-t-Tazkiyah (Vers 93 à 163) : 5 Piliers de l'Islâm, Prière, Pureté, 7 membres et Repentir (Tawbah).\n"
            "3. Bâb as-Salât wa-t-Tahârah (Vers 164 à 205) : 15 Fard & 18 Sunnah de la Prière, Wudû' (7/8), Ghusl (5/4), Tayammum (8/3).\n"
            "4. Bâb as-Siyâm wa-z-Zakât wa-l-Hajj (Vers 206 à 273) : Jeûne (2/3), Zakât (4/3), Hajj (4/12), Rattrapage (Masbûq) & Malade.\n"
            "5. Bâb al-Ihsân wa-t-Tasawwuf (Vers 274 à 308) : Ihsân, Vertus, Guide Spirituel et les 5 Situations précieuses."
        ),
        "explication": (
            "Félicitations ! Vous voici devant la Grande Révision Finale de Tazawwudu-ç-Çighâr.\n\n"
            "À chaque tentative, 25 questions sont tirées aléatoirement parmi une banque vérifiée de plus de 115 questions (QCM, Vrai/Faux, "
            "Associations de paires et Réponses courtes) couvrant l'intégralité des 308 vers de Cheikh Ahmadou Bamba."
        ),
        "a_retenir": (
            "• 3 parties de la Religion : Imân (Foi), Islâm (Pratique), Ihsân (Perfection spirituelle)\n"
            "• Tawhîd : 20 attributs nécessaires, 20 impossibles, 1 possible (41 au total)\n"
            "• Purification : Wudû' (7 Fard / 8 Sunnah), Ghusl (5 Fard / 4 Sunnah), Tayammum (8 Fard / 3 Sunnah)\n"
            "• Prière : 15 Obligations (Farâ'id) et 18 Traditions (dont 8 Sunnah Mu'akkadah)\n"
            "• Autres piliers : Jeûne (2 Fard / 3 Sunnah), Zakât (4 Fard / 3 Sunnah), Hajj (4 Piliers / 12 Sunnah)\n"
            "• Ihsân : Adorer Allah comme si tu Le voyais et saisir les 5 situations (Jeunesse, Santé, Richesse, Temps libre, Vie)"
        ),
    },
}


def run_enrichment():
    updated_modules = 0
    for num, data in MODULES_ENRICHIS.items():
        m = TazawwudModule.objects.filter(numero=num).first()
        if m:
            m.titre = data["titre"]
            m.description = data["description"]
            m.save()
            updated_modules += 1

    updated_lecons = 0
    for (mod_num, lec_num), data in LECONS_ENRICHIES.items():
        lecon = TazawwudLecon.objects.filter(module__numero=mod_num, numero=lec_num).first()
        if lecon:
            lecon.description = data["description"]
            lecon.explication = data["explication"]
            lecon.a_retenir = data["a_retenir"]
            if "texte_source" in data and data["texte_source"]:
                lecon.texte_source = data["texte_source"]
            lecon.save()
            updated_lecons += 1

    print(f"Enrichissement terminé : {updated_modules} Grandes Étapes et {updated_lecons} Leçons enrichies avec succès !")


if __name__ == "__main__":
    run_enrichment()
