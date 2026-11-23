"""
Masaalik-ul Jinaan (Les Itinéraires du Paradis) — Cheikh Ahmadou Bamba (RTA)
Parcours interactif étape par étape fidèle au Sommaire intégral du livre (v.1 à v.1562).
Organisation : 4 Grandes Portes, 32 Chapitres & Sous-chapitres, passages courts calibrés petit écran,
petit résumé objectif avant les questions intermédiaires, et plus de 200 questions fidèles au texte.
"""

MASAALIK_PORTES = [
    {
        "id": 1,
        "code": "porte-1",
        "titre": "Porte I · Introduction & Préambule",
        "sous_titre": "11 leçons · Introduction, Fiqh & Soufisme, Science, Oraison, Jeûne, Wird, Dhikr, Fikr, Aumône & Coran (v.1–601)",
        "icone": "fa-compass",
        "couleur": "from-emerald-600 to-teal-700",
        "accent": "#34D399",
        "chapitres": [
            {
                "num": 1,
                "slug": "introduction-egalite",
                "titre": "Introduction : Sincérité & Égalité devant Allah",
                "versets": "v.1 – v.79",
                "duree": "4 min",
                "icone": "fa-star-and-crescent",
                "resume": "Cheikh Ahmadou Bamba présente son traité versifié d'après la prose d'Al-Yadâlî (Hâtimat at-Tasawwuf), rappelle qu'Allah regarde le cœur, proclame l'égalité humaine fondée uniquement sur la piété (v.47–49) et prie pour tout lecteur.",
                "passages": [
                    {"ref": "v.3 – v.4", "titre": "Ce qu'Allah considère", "texte": "Allah exige de nous la sincérité des actions et l'observance de la bonne conduite (al-adab). Il considère en nous le cœur et les qualités spirituelles, et non ce qui n'est qu'apparent."},
                    {"ref": "v.8 – v.10", "titre": "La lutte intérieure", "texte": "Quiconque lutte contre Satan, contre son âme charnelle et contre sa passion profane obtient le Paradis ; celui qui purifie son cœur de tout vice acquiert la lumière et l'agrément d'Allah."},
                    {"ref": "v.25 – v.42", "titre": "Sources de l'ouvrage", "texte": "L'auteur met en vers Hâtimat at-Tasawwuf d'Al-Yadâlî et puise dans Al-Dhahab al-Ibrîz, l'Ihyâ d'Al-Ghazâlî et Junnat al-Murîd. Quand il écrit simplement « il dit », il s'agit toujours de l'Imam Al-Ghazâlî."},
                    {"ref": "v.47 – v.49", "titre": "Égalité et dignité humaine", "texte": "« Ne te laisse pas abuser par ma condition d'homme noir. L'homme le plus estimé auprès d'Allah est celui qui Le craint le plus, sans discrimination. La couleur de la peau ne saurait être cause de l'idiotie d'un homme. »"},
                    {"ref": "v.51 – v.77", "titre": "Grâce renouvelée & plan du livre", "texte": "Les dons d'Allah ne sont pas réservés aux seuls anciens : une fine pluie peut en devancer une abondante. L'auteur implore le salut pour quiconque lit, médite ou copie ce livre composé d'un Préambule et de trois grands chapitres."},
                ],
                "questions": [
                    {"q": "Selon les vers 3–4, que considère Allah chez Ses serviteurs ?", "options": ["L'apparence extérieure", "Le cœur et les qualités spirituelles", "La richesse matérielle", "La renommée"], "answer": 1, "explication": "v.4 : Allah considère le cœur et les qualités spirituelles et non ce qui n'est qu'apparent."},
                    {"q": "Contre quels trois adversaires faut-il lutter pour obtenir le Paradis (v.8) ?", "options": ["La faim, le froid et le sommeil", "Satan, l'âme charnelle et la passion profane", "Les rois et les juges", "Les voyages"], "answer": 1, "explication": "v.8 cite la lutte contre Satan, l'âme charnelle et la passion profane."},
                    {"q": "Quel ouvrage en prose Cheikh Ahmadou Bamba a-t-il principalement versifié (v.25 & 38) ?", "options": ["Hâtimat at-Tasawwuf d'Al-Yadâlî", "Le Muwatta", "La Risâla", "Sahîh Muslim"], "answer": 0, "explication": "v.25 & v.38 : il a versifié « Hâtimat at-Tasawwuf » (le complément du soufisme) d'Al-Yadâlî."},
                    {"q": "Quand le texte dit simplement « il dit » sans nom, de qui s'agit-il (v.42) ?", "options": ["Ibn Khaldûn", "L'Imam Al-Ghazâlî", "Al-Bukhârî", "Ibn Mâlik"], "answer": 1, "explication": "v.42 précise que « il dit » sans autre mention renvoie à l'Imam Al-Ghazâlî."},
                    {"q": "Quel est le seul critère d'estime auprès d'Allah selon le vers 48 ?", "options": ["La couleur de la peau", "La crainte d'Allah (piété)", "La descendance", "La fortune"], "answer": 1, "explication": "v.48 : l'homme le plus estimé auprès d'Allah est celui qui Le craint le plus, sans discrimination."},
                    {"q": "Quelle image du vers 53 montre que les générations récentes peuvent recevoir de grandes grâces ?", "options": ["Une fine pluie devançant une pluie abondante", "Un arbre sans feuilles", "Un désert sec", "Un vent d'hiver"], "answer": 0, "explication": "v.53 : « Une fine pluie peut en devancer une abondante, mais l'avantage est pour l'abondante. »"},
                    {"q": "Combien de grands chapitres suivent le Préambule (v.74) ?", "options": ["Deux", "Trois", "Cinq", "Huit"], "answer": 1, "explication": "v.74 : l'ouvrage se compose de trois chapitres précédés d'un préambule."},
                ],
            },
            {
                "num": 2,
                "slug": "preambule-fiqh-soufisme",
                "titre": "Préambule (1) : Fiqh, Soufisme & Action",
                "versets": "v.80 – v.105",
                "duree": "4 min",
                "icone": "fa-scale-balanced",
                "resume": "Ce sous-chapitre pose les deux ailes indispensables du croyant : le Fiqh (règles extérieures) et le Tasawwuf (purification du cœur), puis montre comment la science et l'action doivent s'unir sans jamais ajourner le repentir.",
                "passages": [
                    {"ref": "v.80 – v.86", "titre": "Deux branches inséparables", "texte": "La science se divise en exotérique (le fiqh, qui régit l'action) et ésotérique (le tasawwuf, qui régit les états du cœur). Il est obligatoire de commencer par le fiqh puis de réunir les deux."},
                    {"ref": "v.87 – v.90", "titre": "La célèbre règle de l'Imam Mâlik", "texte": "« Celui qui applique le fiqh sans soufisme est un pervers ; celui qui pratique le soufisme sans fiqh est un hérétique (zindîq) ; mais celui qui réunit les deux est un beau modèle à suivre. »"},
                    {"ref": "v.91 – v.99", "titre": "Science, action et vigueur", "texte": "La science et l'action sont les deux moyens vers le bonheur éternel. Éloigne-toi de la paresse et conduis-toi comme si ta mort était imminente."},
                    {"ref": "v.100 – v.105", "titre": "Piège du repentir différé & valeur de la science", "texte": "Retarder le repentir par crainte de récidiver est un piège de Satan. La science est supérieure à l'action car elle en est le fondement : un peu d'actions avec science vaut plus que beaucoup d'actions dans l'ignorance."},
                ],
                "questions": [
                    {"q": "Que régit le Fiqh et que régit le Tasawwuf (v.81–82) ?", "options": ["Le Fiqh régit l'action extérieure, le Tasawwuf régit les états d'âme", "Les deux régissent le commerce", "Le Tasawwuf annule le Fiqh", "Le Fiqh remplace la foi"], "answer": 0, "explication": "v.81–82 : l'exotérique (fiqh) régit l'action ; l'ésotérique (tasawwuf) régit les états d'âme."},
                    {"q": "Par laquelle des deux disciplines faut-il obligatoirement commencer (v.83) ?", "options": ["Le Fiqh avant d'aborder le soufisme", "La poésie", "La rhétorique", "L'histoire"], "answer": 0, "explication": "v.83 : « Il est obligatoire à l'homme de commencer par le fiqh avant d'aborder le soufisme. »"},
                    {"q": "Selon l'Imam Mâlik (v.87–89), qui est le beau modèle à suivre ?", "options": ["Celui qui néglige le fiqh", "Celui qui néglige le soufisme", "Celui qui réunit le fiqh et le tasawwuf", "Celui qui évite toute pratique"], "answer": 2, "explication": "v.89 : celui qui réunit fiqh et tasawwuf est un beau modèle à suivre."},
                    {"q": "Comment le vers 102 qualifie-t-il le fait d'ajourner le repentir par crainte de récidiver ?", "options": ["Une marque de prudence", "Un piège tendu par Satan le rebelle", "Une recommandation", "Un degré élevé"], "answer": 1, "explication": "v.102 avertit que différer le repentir est un piège de Satan."},
                    {"q": "Pourquoi la science est-elle supérieure à l'action (v.103–104) ?", "options": ["Parce qu'elle en est le fondement, même si elle ne porte de fruits que par la pratique", "Parce qu'elle dispense d'agir", "Parce qu'elle est plus facile", "Parce qu'elle donne la célébrité"], "answer": 0, "explication": "v.103–104 : la science est le fondement de l'action et porte ses fruits par l'application."},
                    {"q": "Que vaut un peu d'actions fondées sur la science face à beaucoup d'actions dans l'ignorance (v.105) ?", "options": ["Moins de mérite", "Plus de récompense sans doute", "Exactement pareil", "Aucune récompense"], "answer": 1, "explication": "v.105 : un peu de bonnes actions fondées sur la science a plus de récompense."},
                ],
            },
            {
                "num": 3,
                "slug": "preambule-science-utile",
                "titre": "Préambule (2) : Science Utile & Valeur du Temps",
                "versets": "v.106 – v.183",
                "duree": "5 min",
                "icone": "fa-book-open-reader",
                "resume": "Le livre distingue la science utile (qui inspire crainte d'Allah, humilité et purification du cœur) de la science nuisible (orgueil, disputes), classe les disciplines religieuses et rappelle la valeur inestimable de chaque respiration.",
                "passages": [
                    {"ref": "v.106 – v.117", "titre": "Critère de la science utile", "texte": "La seule science utile est apprise exclusivement pour Allah. Elle inspire la crainte d'Allah, l'humilité, l'ascèse et purifie le cœur ; celle apprise pour les disputes ou le prestige devient un argument contre son auteur."},
                    {"ref": "v.118 – v.128", "titre": "Hiérarchie des sciences et des actions", "texte": "La meilleure science est la théologie (Tawhîd), puis l'exégèse coranique, le Hadîth et le fiqh. La meilleure action profite au plus grand nombre et se fait avec constance. Le pire péché est celui qui endurcit le cœur."},
                    {"ref": "v.133 – v.151", "titre": "Chaque respiration est une pierre précieuse", "texte": "Les morts souhaitent par-dessus tout revenir un court instant pour faire un bienfait. Chaque respiration vaut une pierre précieuse sans égal. Accomplis tes dévotions discrètement loin de l'ostentation."},
                    {"ref": "v.159 – v.183", "titre": "La vraie science est une lumière dans le cœur", "texte": "La vraie science montre à l'homme ses propres défauts et l'incite à la bonté. « La qualité de savant ne s'attribue pas au nombre de récits débités : la science est une lumière résidant dans le cœur. »"},
                ],
                "questions": [
                    {"q": "Quelle est la seule science véritablement utile (v.106) ?", "options": ["Celle apprise pour les polémiques", "Celle apprise et enseignée exclusivement pour l'amour d'Allah", "Celle apprise pour le prestige", "Celle qui nourrit l'orgueil"], "answer": 1, "explication": "v.106 : la seule science utile est apprise et enseignée exclusivement pour Allah."},
                    {"q": "Quelle est la meilleure des sciences dans leur ensemble (v.118) ?", "options": ["La grammaire", "La théologie (profession de foi / Tawhîd)", "La prosodie", "La rhétorique"], "answer": 1, "explication": "v.118 place la théologie en tête, suivie de l'exégèse, du Hadîth et du fiqh."},
                    {"q": "Quelle est la pire désobéissance selon le vers 128 ?", "options": ["Celle qui endurcit le cœur et fait oublier Allah", "Une erreur suivie de repentir", "Une faiblesse passagère", "Un oubli involontaire"], "answer": 0, "explication": "v.128 : la pire désobéissance endurcit le cœur et fait oublier Allah."},
                    {"q": "À quoi le vers 138 compare-t-il le temps d'une seule respiration ?", "options": ["À une goutte d'eau", "À une pierre précieuse sans égal", "À une heure de repos", "À un grain de sable"], "answer": 1, "explication": "v.138 : une respiration vaut une pierre précieuse sans égal."},
                    {"q": "Que dit le vers 170 au sujet de ce que la science utile révèle à l'homme ?", "options": ["Les défauts des autres", "Ses propres défauts de manière claire", "Des secrets politiques", "Des richesses cachées"], "answer": 1, "explication": "v.170 : la science utile fait connaître à l'homme ses propres défauts."},
                    {"q": "Comment le vers 181–183 définit-il le véritable savant ('âlim) ?", "options": ["Celui qui parle le plus", "Celui dont la science est une lumière dans le cœur qui engendre la crainte d'Allah", "Celui qui gagne tous les débats", "Celui qui a le plus de livres"], "answer": 1, "explication": "v.181 & v.183 : la science est une lumière dans le cœur et nul n'est 'âlim sans crainte d'Allah."},
                ],
            },
            {
                "num": 4,
                "slug": "sagesse-profonde",
                "titre": "Sagesse Profonde en Citation",
                "versets": "v.184 – v.191",
                "duree": "3 min",
                "icone": "fa-lightbulb",
                "resume": "Huit vers d'une densité remarquable qui fixent la juste proportion entre nos actes pour ce monde éphémère, notre préparation pour l'Au-delà éternel, notre besoin d'Allah et la crainte révérencielle.",
                "passages": [
                    {"ref": "v.184 – v.186", "titre": "Ne pas abuser des bienfaits d'Allah", "texte": "Si tu jouis des biens procurés par Allah tout en restant détourné de Sa voie sans te repentir résolument, tu cours au péril. N'utilise jamais les biens d'Allah tout en servant autre chose que Lui."},
                    {"ref": "v.187 – v.189", "titre": "La juste mesure des deux mondes", "texte": "Multiplie tes bonnes actions autant que tu as besoin de l'aide d'Allah. Agis pour ce bas-monde en fonction de la brièveté de ton séjour ici-bas, et agis pour l'Au-delà en fonction de l'éternité que tu y passeras."},
                    {"ref": "v.190 – v.191", "titre": "Crainte salutaire d'Allah", "texte": "N'ose désobéir que dans la mesure où tu pourrais supporter le feu de l'Enfer. Et si tu crains ton Seigneur l'Unique comme il se doit, chaque être vivant te craindra par respect."},
                ],
                "questions": [
                    {"q": "À quelle mesure dois-tu multiplier tes bonnes actions pour Allah (v.187) ?", "options": ["Autant que tu as besoin de Son aide", "Une fois par mois", "Uniquement quand tu es riche", "Seulement en voyage"], "answer": 0, "explication": "v.187 : « Multiplie tes bonnes actions pour l'amour d'Allah autant que tu as besoin de Son aide. »"},
                    {"q": "Selon quel critère dois-tu agir pour ce bas-monde (v.188) ?", "options": ["Comme si tu y restais éternellement", "En fonction de la durée de ton séjour ici-bas par rapport à l'Au-delà", "Sans jamais travailler", "En cherchant seulement le luxe"], "answer": 1, "explication": "v.188–189 invitent à proportionner ses efforts à la durée du séjour dans chaque monde."},
                    {"q": "Qu'advient-il de celui qui fausse ce principe entre ce monde et l'Au-delà (v.189) ?", "options": ["Il réussit pleinement", "Il est en déperdition", "Il devient ascète", "Il n'est pas jugé"], "answer": 1, "explication": "v.189 : « Celui qui fausse ce principe est en déperdition. »"},
                    {"q": "Quelle réflexion le vers 190 oppose-t-il à la tentation de désobéir ?", "options": ["N'agis pour l'Enfer que dans la mesure de ta patience à supporter sa chaleur", "Les péchés n'ont pas de conséquence", "Il suffit de se cacher", "Le temps efface tout seul"], "answer": 0, "explication": "v.190 rappelle l'incapacité humaine à supporter le feu de l'Enfer."},
                    {"q": "Quel fruit spirituel le vers 191 promet-il à celui qui craint Allah comme il se doit ?", "options": ["Chaque être vivant le craint (et le respecte) pour cette raison", "Il ne rencontre plus aucun obstacle", "Il devient automatiquement riche", "Il n'a plus besoin de prier"], "answer": 0, "explication": "v.191 : « Si tu crains ton Seigneur l'Un comme il se doit, chaque être vivant te craint pour cette raison. »"},
                    {"q": "Que faut-il faire si l'on s'est détourné de la voie d'Allah malgré Ses bienfaits (v.185) ?", "options": ["Continuer sans y penser", "Se repentir résolument", "Accuser les autres", "Cesser toute activité"], "answer": 1, "explication": "v.185 avertit que s'obstiner sans se repentir résolument expose au châtiment."},
                ],
            },
            {
                "num": 5,
                "slug": "oraison-vivifier-temps",
                "titre": "L'Oraison : Actes qui Vivifient le Temps",
                "versets": "v.192 – v.223",
                "duree": "4 min",
                "icone": "fa-sun",
                "resume": "Détail des prières surérogatoires recommandées pour vivifier le jour et la nuit : Witr, Fajr (avec Ash-Sharh et Al-Fîl), 6 rak'as après Maghrib, Zuhr, Asr, Duhâ (Yoor-Yoor), assise après Subh et vertu des prosternations.",
                "passages": [
                    {"ref": "v.192 – v.198", "titre": "Witr, Fajr et prières liées aux obligatoires", "texte": "Le Witr est la plus recommandée des prières de la Sunna. Les deux rak'as du Fajr peuvent être rattrapées entre le lever du soleil et midi ; y réciter Ash-Sharh et Al-Fîl protège contre tout ennemi."},
                    {"ref": "v.200 – v.205", "titre": "Maghrib, Zuhr et Asr", "texte": "Six rak'as après Maghrib sans interruption déplacée équivalent à douze ans d'adoration agréée. Quatre rak'as avant et après Zuhr garantissent contre la Géhenne ; quatre avant Asr (mais non après) attirent la Miséricorde."},
                    {"ref": "v.206 – v.210", "titre": "La prière de Duhâ (Yoor-Yoor)", "texte": "Prier 2, 6 ou 8 rak'as après le lever du soleil attire la protection d'Allah : au Jour du Jugement, cette prière intercédera pour celui qui l'a observée régulièrement."},
                    {"ref": "v.214 – v.223", "titre": "Assise après Subh & effacement des péchés", "texte": "Rester assis en dhikr après Subh en assemblée jusqu'au lever du soleil vaut un Hajj et une Umra parfaits. À chaque inclinaison et prosternation recueillie, les péchés tombent des épaules du fidèle."},
                ],
                "questions": [
                    {"q": "Quelles deux sourates réciter dans les deux rak'as du Fajr pour être protégé des ennemis (v.198) ?", "options": ["Ash-Sharh (Alam Nashrah) et Al-Fîl (Alam Tara)", "Al-Baqara et Al-Kahf", "Yâ-Sîn et Al-Mulk", "Al-Falaq et An-Nâs"], "answer": 0, "explication": "v.198 cite les deux sourates commençant par « Alam »."},
                    {"q": "À combien d'années d'adoration équivalent les 6 rak'as après Maghrib sans interruption déplacée (v.201–202) ?", "options": ["2 ans", "5 ans", "12 ans", "30 ans"], "answer": 2, "explication": "v.202 : cela vaut aux yeux d'Allah l'adoration agréée de douze ans."},
                    {"q": "Comment se pratiquent les surérogatoires liées à Asr selon le vers 193 ?", "options": ["Quatre avant, mais non après", "Quatre après seulement", "Huit après", "Aucune"], "answer": 0, "explication": "v.193 : quatre avant Asr, mais non après."},
                    {"q": "Quel nombre de rak'as est cité pour la prière de Duhâ (Yoor-Yoor) aux vers 199 & 210 ?", "options": ["2, 6 ou 8 rak'as (dépasser 8 étant blâmable selon certains docteurs)", "12 à 20 rak'as", "1 seule rak'a", "15 rak'as"], "answer": 0, "explication": "v.199 & 210 précisent 2, 6 ou 8 rak'as."},
                    {"q": "Quelle récompense obtient celui qui reste en dhikr après Subh en assemblée jusqu'au lever du soleil (v.215–216) ?", "options": ["Le mérite d'un pèlerinage majeur et mineur parfaits", "Un jour de jeûne", "Dix dirhams d'aumône", "Une nuit de sommeil"], "answer": 0, "explication": "v.216 : même mérite que les pèlerinages majeur et mineur parfaits."},
                    {"q": "Qu'advient-il des péchés lors de l'inclinaison et de la prosternation recueillies (v.221–222) ?", "options": ["Ils s'effacent et tombent des épaules et de la nuque", "Ils restent intacts", "Ils diminuent de moitié seulement", "Ils sont reportés"], "answer": 0, "explication": "v.222 : les péchés tombent de dessus ses épaules et de sa nuque."},
                ],
            },
            {
                "num": 6,
                "slug": "jeune-des-organes",
                "titre": "Le Jeûne des Organes & Achoura",
                "versets": "v.224 – v.266",
                "duree": "4 min",
                "icone": "fa-moon",
                "resume": "La porte du Paradis réservée aux jeûneurs, les 3 jours par mois de l'Imam Mâlik, les 12 recommandations et prodiges d'Achoura, le jeûne complet de tous les membres et la mise en garde contre la gloutonnerie à la rupture.",
                "passages": [
                    {"ref": "v.224 – v.227", "titre": "Porte des jeûneurs & 3 jours par mois", "texte": "Une porte du Paradis n'est accessible qu'aux jeûneurs. L'Imam Mâlik jeûnait trois jours par mois : multipliés par dix par la Bonté d'Allah, cela équivaut à jeûner toute l'année."},
                    {"ref": "v.234 – v.254", "titre": "Achoura (10 Muharram) : pratiques et prodiges", "texte": "Le 10 Muharram (Tamkharit) comporte 12 pratiques recommandées (jeûne, visites familiales, aumône, malade, érudit, orphelin, 1000 Al-Ikhlâs, bon repas familial). C'est le jour du pardon d'Adam, de l'Arche de Noé, de la mer fendue pour Moïse et d'Abraham sauvé du feu."},
                    {"ref": "v.255 – v.259", "titre": "Le jeûne de tous les membres", "texte": "Le jeûne ne consiste pas seulement à s'abstenir de manger et de boire : combien n'en retirent que faim et soif ! Les yeux, les pieds, les oreilles, la langue et les pensées doivent aussi jeûner."},
                    {"ref": "v.260 – v.265", "titre": "Sobriété à l'aube et à la rupture", "texte": "Ne te gave pas à l'aube ni à la rupture : un estomac trop rempli alourdit le corps, assombrit le cœur et détourne de l'évocation d'Allah."},
                ],
                "questions": [
                    {"q": "Pourquoi jeûner 3 jours par mois équivaut-il à jeûner toute l'année (v.226–227) ?", "options": ["Grâce à la multiplication par dix qu'Allah accorde", "Parce que c'est réservé au Ramadan", "Parce que la nuit compte triple", "Parce que le mois dure 10 jours"], "answer": 0, "explication": "v.227 : 3 jours × 10 = 30 jours, comme un jeûne perpétuel."},
                    {"q": "Combien de pratiques recommandées pour Achoura le livre énumère-t-il (v.240–242) ?", "options": ["Cinq", "Huit", "Douze", "Vingt"], "answer": 2, "explication": "v.242 précise la douzième recommandation : préparer un repas généreux à la famille."},
                    {"q": "Lequel de ces prodiges est associé à Achoura aux vers 246–251 ?", "options": ["Le pardon d'Adam, l'Arche de Noé sur le mont Jûdî et la mer fendue pour Moïse", "La bataille d'Uhud", "L'Hégire", "La construction de Médine"], "answer": 0, "explication": "v.246–253 citent Adam, Noé, Moïse, Jonas, Joseph, Abraham, Idrîs, Jésus et David."},
                    {"q": "Que risquent certains jeûneurs selon le vers 256 ?", "options": ["De ne retirer de leur jeûne que la faim et la soif", "D'être dispensés de prière", "De ne plus avoir soif", "D'obtenir une double récompense"], "answer": 0, "explication": "v.256 : beaucoup n'obtiennent de leur jeûne que la faim et la soif."},
                    {"q": "Qu'est-ce qui doit s'abstenir de l'interdit pendant le jeûne (v.257–259) ?", "options": ["Uniquement la bouche", "Tous les membres, les organes et même les mauvaises pensées", "Uniquement les mains", "Uniquement les oreilles"], "answer": 1, "explication": "v.257–259 incluent tous les membres, les sens et les pensées du cœur."},
                    {"q": "Quel effet provoque le fait de se gaver à la rupture du jeûne (v.263–265) ?", "options": ["Un ventre lourd, un cœur assombri et détourné du dhikr", "Un cœur plus lumineux", "Une meilleure concentration", "Un réveil nocturne plus facile"], "answer": 0, "explication": "v.264–265 : l'excès alimentaire obstrue et assombrit le cœur."},
                ],
            },
            {
                "num": 7,
                "slug": "wird-guide-spirituel",
                "titre": "Le Wird (Litanies) & Le Guide Spirituel",
                "versets": "v.267 – v.298",
                "duree": "4 min",
                "icone": "fa-water",
                "resume": "Sens profond du wird (point d'eau spirituel), fraternité absolue envers toutes les voies (Qâdiriyya, Tijâniyya, etc.), statut des Prophètes et des Saints, et nécessité d'un éducateur spirituel valable.",
                "passages": [
                    {"ref": "v.269 – v.271", "titre": "Définition du Wird", "texte": "Le wird est un acte d'adoration déterminé pratiqué dans un temps régulier. Le mot signifie « stationner à un point d'eau pour boire ou puiser ». Chaque wird mène sans déviation vers Allah."},
                    {"ref": "v.272 – v.275", "titre": "Respect de tous les Wirds", "texte": "Qu'il vienne de Cheikh Abd al-Qâdir al-Jîlânî, de Cheikh Ahmad at-Tijânî ou d'un autre Pôle : tous les wirds sont dans la rectitude. Garde-toi d'en mépriser ou d'en critiquer aucun !"},
                    {"ref": "v.276 – v.285", "titre": "Prophètes impeccables & Saints protégés", "texte": "Le wird s'enracine dans le Coran et la Sunna. La révélation appartient au prophète (impeccable), l'inspiration au saint (protégé et héritier du prophète)."},
                    {"ref": "v.290 – v.298", "titre": "Assiduité & Guide spirituel", "texte": "Celui qui ne pratique aucun wird perd son temps. Qui n'a jamais été éduqué par un guide spirituel valable risque que Satan le dirige. Si tu ne peux marcher vers le point d'eau, n'empêche pas les autres d'y puiser."},
                ],
                "questions": [
                    {"q": "Que signifie littéralement le mot « wird » (v.270) ?", "options": ["Stationner à un point d'eau pour boire ou puiser", "Dormir la nuit", "Rédiger une lettre", "Voyager seul"], "answer": 0, "explication": "v.270 donne l'étymologie : stationner sur un point d'eau pour s'abreuver."},
                    {"q": "Quelle attitude adopter envers les wirds des autres confréries (v.272–275) ?", "options": ["Les respecter tous et ne jamais en mépriser ni critiquer aucun", "Ne reconnaître que le sien", "Les dénigrer", "Les ignorer"], "answer": 0, "explication": "v.275 : tous les wirds sont dans la rectitude et appellent à adorer Allah."},
                    {"q": "Quelle différence le vers 277 indique-t-il entre le prophète et le saint ?", "options": ["La révélation est l'apanage du prophète, l'inspiration celui du saint", "Aucune différence", "Le saint annule la Sunna", "Le prophète n'est pas protégé"], "answer": 0, "explication": "v.277 distingue révélation (prophète) et inspiration (saint)."},
                    {"q": "Quel danger court celui qui n'a aucun guide spirituel valable (v.294–295) ?", "options": ["Satan se charge de le diriger vers les voies de la perdition", "Il atteint plus vite la sainteté", "Il évite toutes les épreuves", "Il n'a plus besoin de wird"], "answer": 0, "explication": "v.295 : sans guide valable, Satan se charge de le diriger."},
                    {"q": "Que recommande le vers 297 à celui que la paresse empêche de faire le wird ?", "options": ["Ne pas empêcher les autres d'aller puiser au point d'eau", "Interdire les wirds", "Critiquer les pratiquants", "Se moquer des litanies"], "answer": 0, "explication": "v.297 interdit d'empêcher les autres de s'abreuver au point d'eau."},
                    {"q": "De quoi dépendent les récompenses du wird selon le vers 298 ?", "options": ["Des qualités du wird et du recueillement du cœur", "De la rapidité seule", "Du nombre d'auditeurs", "Du moment de l'année"], "answer": 0, "explication": "v.298 : elles dépendent des qualités du wird et de la disposition du cœur."},
                ],
            },
            {
                "num": 8,
                "slug": "dhikr-priere-prophete",
                "titre": "Le Dhikr & La Prière sur le Prophète",
                "versets": "v.299 – v.408",
                "duree": "5 min",
                "icone": "fa-fingerprint",
                "resume": "Le Dhikr comme début de la sainteté, voix basse vs voix haute, les fruits de chaque formule (Shahâda, Basmala, Hawqala, Hasbala, Istighfâr), les merveilles de la Salât 'alâ-n-Nabî et la litanie du coucher.",
                "passages": [
                    {"ref": "v.299 – v.321", "titre": "Début de la sainteté & bienséance", "texte": "Le dhikr est la meilleure action de l'aspirant : il est le début de la sainteté et son abandon est l'égarement. Si on craint l'ostentation, on récite à voix basse ; sinon à voix haute. On s'assoit propre, parfumé, face à la Kaaba."},
                    {"ref": "v.331 – v.355", "titre": "La Shahâda et les fruits de chaque formule", "texte": "La Shahâda est le prix du Paradis et résume toutes les formules. Le Tahlîl ancre le Tawhîd, le Takbîr et le Hamd la gratitude, la Hawqala et la Hasbala l'abandon à Allah, l'Istighfâr la crainte d'Allah."},
                    {"ref": "v.356 – v.375", "titre": "Les secrets de la Basmala", "texte": "10 Basmala + Hawqala le matin effacent les péchés, éloignent 72 malheurs et confient le fidèle à 70 anges. 21 Basmala avant de dormir protègent contre la mort subite, le vol et les démons."},
                    {"ref": "v.379 – v.408", "titre": "Salât 'alâ-n-Nabî & litanie du soir", "texte": "La prière sur le Prophète (PSL) est la plus méritoire des occupations après les obligations : elle peut tenir lieu de guide spirituel et illumine intérieur et extérieur. Avant dormir : 4 Fâtiha, 3 Ikhlâs, 4 Bâqiyât as-Sâlihât, 10 Istighfâr et 10 Salât."},
                ],
                "questions": [
                    {"q": "Comment le vers 304 qualifie-t-il la mention du Nom d'Allah ?", "options": ["Le début de la sainteté", "Un acte secondaire", "Une simple coutume", "Un effort inutile"], "answer": 0, "explication": "v.304 : la mention du Nom d'Allah est le début de la sainteté."},
                    {"q": "Quel est le fruit de la Hawqala et de la Hasbala (v.346–347) ?", "options": ["L'abandon et la confiance absolue en Allah", "La richesse immédiate", "La célébrité", "La force physique"], "answer": 0, "explication": "v.347 : l'abandon à Allah et la ferme confiance en Lui."},
                    {"q": "Quelle formule condense toutes les autres formules de dhikr (v.352–353) ?", "options": ["Lâ ilâha illallâh Muhammadun Rasûlullâh", "Subhânallâh seul", "Allâhu Akbar seul", "Al-Hamdulillâh seul"], "answer": 0, "explication": "v.352–353 : la Shahâda condense toutes les formules."},
                    {"q": "Combien de Basmala réciter avant de dormir pour être protégé contre la mort subite et le vol (v.365–366) ?", "options": ["7 fois", "10 fois", "21 fois", "99 fois"], "answer": 2, "explication": "v.365–366 : 21 fois, ni moins ni plus, avant de dormir."},
                    {"q": "Que dit Cheikh As-Sanûssî au sujet de la prière sur le Prophète (v.381–382) ?", "options": ["Elle peut tenir lieu de guide spirituel vers la proximité du Prophète", "Elle remplace le jeûne", "Elle est réservée aux imams", "Elle se lit uniquement le vendredi"], "answer": 0, "explication": "v.382 : elle peut tenir lieu de guide spirituel."},
                    {"q": "Que comprend la litanie nocturne recommandée avant le sommeil (v.401–406) ?", "options": ["4 Fâtiha, 3 Ikhlâs, 4 Bâqiyât as-Sâlihât, 10 Istighfâr et 10 Salât 'alâ-n-Nabî", "Uniquement 1 Fâtiha", "Uniquement 33 Tasbîh", "Uniquement Al-Falaq"], "answer": 0, "explication": "v.402–406 énumèrent cette litanie complète avant de dormir."},
                ],
            },
            {
                "num": 9,
                "slug": "fikr-meditation",
                "titre": "Le Fikr ou la Méditation",
                "versets": "v.409 – v.459",
                "duree": "4 min",
                "icone": "fa-brain",
                "resume": "La méditation comme miroir du croyant et clé de la gnose (exemple d'Abraham), les sujets recommandés (cieux, terre, bienfaits) vs les pensées à éviter, et la définition du « meilleur jihâd » (v.456).",
                "passages": [
                    {"ref": "v.411 – v.415", "titre": "Miroir du cœur & 1 heure > 1 an", "texte": "Le dhikr donne l'intimité avec Allah ; le fikr donne la gnose. Une heure de méditation l'emporte sur un an d'adoration. Elle est un miroir qui montre au croyant ses bonnes œuvres et ses défauts."},
                    {"ref": "v.428 – v.441", "titre": "Certitude d'Abraham & parole d'un Saint", "texte": "« L'intensité de ta foi augmente en fonction de la profondeur de tes pensées. » C'est par la méditation qu'Abraham acquit sa conviction. Un Saint dit connaître Allah « par Son fait de défaire nos fermes décisions »."},
                    {"ref": "v.442 – v.450", "titre": "Méditer sur les créatures, non sur l'Essence", "texte": "Les meilleurs sujets sont les cieux, la terre, les astres, les bienfaits d'Allah, la récompense et le châtiment. On réfléchit sur les créatures, mais jamais sur l'Essence du Créateur."},
                    {"ref": "v.451 – v.457", "titre": "Le meilleur Jihâd", "texte": "Ne rumine ni ton dénuement (tristesse) ni l'injustice subie (haine). « Le meilleur jihâd consiste à empêcher l'esprit de s'occuper de ce qui ne lui incombe pas. »"},
                ],
                "questions": [
                    {"q": "Que procure le Dhikr et que procure le Fikr selon le vers 412 ?", "options": ["Le Dhikr procure l'intimité avec Allah, le Fikr procure la gnose", "Les deux procurent le repos", "Le Fikr remplace le Dhikr", "Aucun lien"], "answer": 0, "explication": "v.412 : intimité par le dhikr, gnose par la méditation."},
                    {"q": "À quoi le vers 414 compare-t-il la méditation ?", "options": ["À un miroir pour le croyant", "À un navire", "À une muraille", "À une lampe éteinte"], "answer": 0, "explication": "v.414–415 : un miroir qui révèle bonnes actions et défauts."},
                    {"q": "Quel Prophète est cité au vers 434 comme modèle de certitude par la méditation ?", "options": ["Abraham (Ibrâhîm)", "Salomon", "Noé", "Job"], "answer": 0, "explication": "v.434 cite Abraham, l'ami d'Allah."},
                    {"q": "Quelle règle capitale pose le vers 450 ?", "options": ["Méditer sur les créatures, mais non sur le Créateur Lui-même", "Méditer uniquement sur sa fortune", "Éviter de regarder le ciel", "Ne jamais réfléchir"], "answer": 0, "explication": "v.450 : réfléchir sur les créatures, jamais sur l'Essence du Créateur."},
                    {"q": "Pourquoi éviter de ressasser une injustice subie (v.452) ?", "options": ["Cela engendre une forte haine et de la colère", "Cela fait oublier ses prières", "Cela cause la pauvreté", "Cela réduit le sommeil"], "answer": 0, "explication": "v.452 : cela crée haine et colère ; il faut patienter."},
                    {"q": "En quoi consiste « le meilleur jihâd » selon le vers 456 ?", "options": ["Empêcher l'esprit de s'occuper de ce qui ne lui incombe pas", "Voyager très loin", "Accumuler des biens", "Gagner une dispute"], "answer": 0, "explication": "v.456 définit ainsi le meilleur jihâd."},
                ],
            },
            {
                "num": 10,
                "slug": "aumone-bonte-fraternelle",
                "titre": "L'Aumône & La Bonté Fraternelle",
                "versets": "v.460 – v.527",
                "duree": "5 min",
                "icone": "fa-hand-holding-heart",
                "resume": "L'entrée au Paradis sans peine pour ceux qui servent les créatures, les bienfaits protecteurs de l'aumône, l'interdiction de discriminer, la priorité aux proches et les dizaines d'aumônes accessibles sans argent (sourire, parole douce, aide).",
                "passages": [
                    {"ref": "v.462 – v.471", "titre": "Servir les créatures sans craindre la pauvreté", "texte": "Au Jour du Jugement, on appellera ceux qui ont servi les créatures pour entrer au Paradis sans peine. Ne thésaurise jamais par peur de pauvreté : Allah te restituera tout ce que tu dépenses pour Lui."},
                    {"ref": "v.478 – v.491", "titre": "Bouclier contre 70 morts affreuses", "texte": "Une seule aumône écarte 70 sortes de morts affreuses, apaise la colère d'Allah, efface les fautes comme l'eau éteint le feu, guérit les malades, purifie les biens et abrite le fidèle à son ombre."},
                    {"ref": "v.496 – v.503", "titre": "Équité et priorité aux proches", "texte": "La discrimination dans l'aumône est interdite. Ne délaisse jamais un proche nécessiteux : commence par toi-même, puis ceux à ta charge, puis tes voisins."},
                    {"ref": "v.504 – v.527", "titre": "Les aumônes du sourire et de la fraternité", "texte": "Deux rak'as au matin, une parole douce, un sourire en saluant, un bon conseil, écarter un mal du chemin, prêter un outil, visiter un malade ou tenir compagnie à une personne seule : tout cela est aumône !"},
                ],
                "questions": [
                    {"q": "Qui entrera au Paradis sans peine ni épreuve selon les vers 463–465 ?", "options": ["Ceux qui ont été au service des créatures pour Allah", "Les plus célèbres", "Les plus riches", "Les plus forts"], "answer": 0, "explication": "v.463–465 promettent cela à ceux qui ont servi les créatures pour Allah."},
                    {"q": "Combien de sortes de morts affreuses une seule aumône peut-elle écarter (v.481) ?", "options": ["Sept", "Trente", "Soixante-dix (70)", "Cent"], "answer": 2, "explication": "v.481 : soixante-dix (70) chefs de mort affreuse."},
                    {"q": "À quoi le vers 482 compare-t-il l'effet de l'aumône sur les péchés ?", "options": ["À l'eau qui éteint le feu", "Au vent d'été", "Au sable du désert", "À la nuit"], "answer": 0, "explication": "v.482 : comme l'eau éteint le feu."},
                    {"q": "Quel ordre de priorité les vers 498–500 établissent-ils ?", "options": ["Soi-même, puis ceux à notre charge, puis nos voisins", "Les inconnus lointains d'abord", "Seulement les voyageurs", "Seulement les riches"], "answer": 0, "explication": "v.499–500 : soi-même, puis ceux à notre charge, puis les voisins."},
                    {"q": "Si un bien passe en aumône entre 70 000 personnes, que reçoit le dernier donneur (v.502–503) ?", "options": ["Une récompense égale à celle du premier", "Un dixième", "Rien", "La moitié"], "answer": 0, "explication": "v.503 : la récompense des derniers égale celle des premiers."},
                    {"q": "Lequel de ces actes est compté comme aumône (v.507–527) ?", "options": ["Sourire en saluant, adresser de doux propos et tenir compagnie à une personne seule", "Ignorer son voisin", "Critiquer un pauvre", "Thésauriser"], "answer": 0, "explication": "v.507, 513–514 et 527 citent tous ces gestes fraternels."},
                ],
            },
            {
                "num": 11,
                "slug": "lecture-ethique-coran",
                "titre": "La Lecture du Coran & Ses Règles d'Éthique",
                "versets": "v.528 – v.601",
                "duree": "5 min",
                "icone": "fa-book-quran",
                "resume": "Le Coran comme source de toutes les sciences, 3 hizbs par jour, la méditation supérieure à la lecture distraite, l'adab devant le Livre d'Allah, les bienfaits de la lecture sur le Mushaf et le respect matériel du texte sacré.",
                "passages": [
                    {"ref": "v.529 – v.540", "titre": "Ne jamais abandonner le Coran", "texte": "Lis le Coran sans l'abandonner, fût-ce 3 hizbs par jour. Il est la source de toutes les sciences. Ceux qui prétendent qu'une autre pratique soufie lui est supérieure sont trompés par Satan."},
                    {"ref": "v.541 – v.556", "titre": "Compréhension, recueillement et présence", "texte": "Quelques versets médités valent mieux que de nombreuses sourates lues sans réflexion. Lis en état de pureté, face à la Kaaba, d'une voix grave et posée, comme si tu voyais Allah — car Lui te voit."},
                    {"ref": "v.557 – v.574", "titre": "Lecture sur le Mushaf & regard quotidien", "texte": "Aucun moment n'est interdit pour lire le Coran. Lire dans un Mushaf fortifie la vue et allège la peine des parents dans la tombe. Un seul regard quotidien posé sur le Mushaf est inscrit comme adoration."},
                    {"ref": "v.580 – v.598", "titre": "Enseigner et honorer le Mushaf", "texte": "« Le meilleur des humains est celui qui apprend le Coran et l'enseigne. » Il est louable d'embrasser et parfumer le Mushaf ; il est interdit de poser sa tête ou un objet dessus ou d'étendre les jambes vers lui."},
                ],
                "questions": [
                    {"q": "Quel minimum quotidien de lecture du Coran conseille le vers 531 ?", "options": ["Trois (3) hizbs chaque jour", "Une page par semaine", "Uniquement le vendredi", "Seulement pendant Ramadan"], "answer": 0, "explication": "v.531 conseille au moins trois hizbs chaque jour."},
                    {"q": "Que dit le livre sur ceux qui prétendent que leur pratique vaut mieux que la lecture du Coran (v.533–534) ?", "options": ["Satan les a trompés avec un argument faux", "Ils ont raison", "C'est une voie secrète", "C'est réservé aux savants"], "answer": 0, "explication": "v.534 réfute fermement cette prétention."},
                    {"q": "Y a-t-il un moment interdit pour lire le Coran selon le vers 557 ?", "options": ["Non, aucun moment n'est interdit", "Oui, après Asr", "Oui, la nuit", "Oui, le lundi"], "answer": 0, "explication": "v.557–559 confirment qu'aucun moment n'est interdit."},
                    {"q": "Quels deux bienfaits particuliers le livre attache-t-il à la lecture sur le Mushaf (v.564–567) ?", "options": ["Une bonne vue et l'allègement des peines des parents dans la tombe", "La richesse rapide", "La dispense du jeûne", "Un voyage offert"], "answer": 0, "explication": "v.565–567 mentionnent la bonne vision et l'allègement de la peine des parents."},
                    {"q": "Pourquoi ne faut-il pas passer un jour sans regarder le Coran (v.573–574) ?", "options": ["Un seul regard sur le Mushaf est inscrit comme acte de dévotion", "Pour décorer la maison", "Parce que c'est interdit le jeudi", "Pour impressionner autrui"], "answer": 0, "explication": "v.574 : un seul regard dans le Mushaf compte comme dévotion."},
                    {"q": "Quel geste envers le Mushaf est formellement interdit (v.590–592) ?", "options": ["Poser la tête ou un objet dessus, ou tendre les jambes vers lui", "Le parfumer", "L'embrasser", "Le poser sur un lutrin"], "answer": 0, "explication": "v.590–592 interdisent ces manquements au respect du Livre saint."},
                ],
            },
        ],
    },
    {
        "id": 2,
        "code": "porte-2",
        "titre": "Porte II · Chapitre 1 — La Mystique & L'Ascétisme",
        "sous_titre": "5 sous-chapitres du Sommaire · Les 4 obstacles (Satan, Âme charnelle, Bas-monde, Créatures) et l'Action dévote (v.602–872)",
        "icone": "fa-shield-halved",
        "couleur": "from-teal-700 to-cyan-800",
        "accent": "#2DD4BF",
        "chapitres": [
            {
                "num": 12,
                "slug": "mystique-satan",
                "titre": "Ch.1 (1) : Connaître et Combattre Satan",
                "versets": "v.667 – v.684",
                "duree": "4 min",
                "icone": "fa-shield",
                "resume": "Premier des quatre obstacles de la voie spirituelle dans le Sommaire de Masaalikul Jinaan : identifier les ruses de Satan (insouciance, ajournement, division) et s'en protéger par le refuge en Allah, le dhikr constant et la science.",
                "passages": [
                    {"ref": "Ch.1 · v.667–684", "titre": "Un ennemi déclaré qui agit par la ruse", "texte": "Dans la voie mystique, Satan est le premier obstacle qui détourne l'aspirant : il embellit les distractions futiles, suscite le doute, pousse à remettre le repentir au lendemain et exploite chaque moment d'insouciance."},
                    {"ref": "Lien v.8 & v.102 & v.152", "titre": "Ses armes et sa prison", "texte": "Cheikh Ahmadou Bamba enseigne que Satan abuse les gens par ce qui ne leur profitera ni dans la tombe ni au Jugement. Sa prison est le dhikr abondant et le refuge sincère en Allah ; son arme est la négligence."},
                    {"ref": "Armes du croyant", "titre": "Comment triompher de ses suggestions", "texte": "Le croyant triomphe de Satan par la demande de protection (isti'âdha), la présence du cœur dans la prière, la compagnie d'un guide véridique (v.295) et le respect strict de la Sunna."},
                ],
                "questions": [
                    {"q": "Quel est le premier des quatre obstacles étudiés au Chapitre 1 du Sommaire ?", "options": ["Satan", "La fatigue", "Le voyage", "Le froid"], "answer": 0, "explication": "Le Sommaire du Ch.1 ouvre par Satan (v.667–684), suivi de l'âme charnelle, du bas-monde et des créatures."},
                    {"q": "Comment Satan détourne-t-il principalement les gens selon Masaalikul Jinaan (v.102 & v.152) ?", "options": ["En les poussant à différer le repentir et à s'occuper de choses inutiles pour l'Au-delà", "En les obligeant par la force", "En les faisant jeûner", "En leur enseignant le Coran"], "answer": 0, "explication": "v.102 & v.152 montrent qu'il agit par l'ajournement du repentir et l'occupation futile."},
                    {"q": "Que se passe-t-il quand un aspirant refuse tout guide spirituel valable (v.295) ?", "options": ["Satan se charge de le diriger vers la perdition", "Il devient invulnérable", "Satan s'éloigne seul", "Il n'a plus d'épreuves"], "answer": 0, "explication": "v.295 : celui qui n'a pas de guide valable a Satan pour guide."},
                    {"q": "Quel remède spirituel constitue la meilleure forteresse contre Satan ?", "options": ["Le dhikr constant, le refuge en Allah et la Sunna", "La dispute incessante", "L'isolement dans la colère", "L'orgueil de sa science"], "answer": 0, "explication": "Le dhikr (v.334) et la lutte constante (v.8) constituent la forteresse du croyant."},
                    {"q": "Quelle attitude intérieure donne une prise à Satan ?", "options": ["L'insouciance (ghafla) et la négligence du cœur", "L'humilité", "La lecture du Coran", "L'aumône discrète"], "answer": 0, "explication": "L'insouciance et le péché endurcissent le cœur et ouvrent la porte à Satan."},
                    {"q": "Quelle promesse le vers 8 accorde-t-il à qui lutte contre Satan, l'âme charnelle et la passion ?", "options": ["L'obtention du Paradis", "La célébrité terrestre", "La dispense d'œuvres", "La richesse immédiate"], "answer": 0, "explication": "v.8 : quiconque lutte contre ces trois adversaires obtient le Paradis."},
                ],
            },
            {
                "num": 13,
                "slug": "mystique-ame-charnelle",
                "titre": "Ch.1 (2) : Dompter l'Âme Charnelle (Nafs)",
                "versets": "v.685 – v.694",
                "duree": "4 min",
                "icone": "fa-fire-flame-curved",
                "resume": "Deuxième obstacle du Chapitre 1 : l'âme charnelle (nafs), toujours portée vers la paresse, les plaisirs faciles et les prétentions ; la manière de l'éduquer par la sobriété, l'effort constant et la vigilance.",
                "passages": [
                    {"ref": "Ch.1 · v.685–694", "titre": "L'ennemi intérieur : le Nafs", "texte": "L'âme charnelle (nafs) est l'obstacle le plus proche de l'homme : laissée sans frein, elle réclame le repos excessif, l'orgueil, les passions interdites et fuit les actes de dévotion exigeants."},
                    {"ref": "Lien v.126–127 & v.330", "titre": "Contrarier ses penchants par l'effort juste", "texte": "Les actions les plus purifiantes sont celles qui pèsent sur l'âme charnelle : donner quand on est avare, jeûner quand on est gourmand, rester discret quand on aime la célébrité (v.126–127)."},
                    {"ref": "Lien v.1249 & v.1265", "titre": "Discipline et sobriété", "texte": "L'éducation du nafs passe par la sobriété alimentaire, la maîtrise du sommeil, la discrétion dans les œuvres pies et l'examen lucide de ses propres défauts."},
                ],
                "questions": [
                    {"q": "Quel est le deuxième obstacle spirituel cité au Chapitre 1 du Sommaire ?", "options": ["L'âme charnelle (nafs)", "La pauvreté", "La pluie", "Le travail"], "answer": 0, "explication": "Le Sommaire place l'âme charnelle (v.685–694) juste après Satan."},
                    {"q": "Quelles actions sont particulièrement efficaces pour éduquer le nafs (v.126–127) ?", "options": ["Les actions pénibles à ses penchants : générosité pour l'avare, jeûne pour le vorace, discrétion pour qui aime la gloire", "Céder à tous ses désirs", "Dormir le plus possible", "Chercher les compliments"], "answer": 0, "explication": "v.126–127 donnent ces trois exemples précis d'actions qui brisent les penchants du nafs."},
                    {"q": "Comment acquiert-on les secrets spirituels selon le vers 330 ?", "options": ["En contrariant la passion et l'âme charnelle", "Dans l'oisiveté et la contestation", "En méprisant les autres", "Par le bavardage"], "answer": 0, "explication": "v.330 : on les obtient en contrariant la passion et l'âme charnelle."},
                    {"q": "Quel effet la gloutonnerie a-t-elle sur l'âme et le cœur (v.264) ?", "options": ["Elle rend le cœur obstrué et assombri", "Elle affine la spiritualité", "Elle facilite le dhikr", "Elle efface les fautes"], "answer": 0, "explication": "v.264 montre que l'excès alimentaire assombrit le cœur."},
                    {"q": "Pourquoi l'âme charnelle pousse-t-elle à exhiber ses bonnes œuvres ?", "options": ["Par soif d'éloges et de célébrité", "Par pure humilité", "Pour augmenter le mérite", "Par crainte d'Allah"], "answer": 0, "explication": "v.150–151 & v.1265 recommandent au contraire de cacher ses bonnes actions."},
                    {"q": "Que confère Allah au serviteur sincère qui lutte contre son nafs (v.1392) ?", "options": ["La force de maîtriser son âme charnelle afin qu'elle n'ait plus d'emprise sur lui", "La dispense des obligations", "L'absence totale d'efforts", "Le pouvoir de juger autrui"], "answer": 0, "explication": "v.1392 montre qu'Allah donne à Ses élus la maîtrise de leur âme charnelle."},
                ],
            },
            {
                "num": 14,
                "slug": "mystique-bas-monde",
                "titre": "Ch.1 (3) : Se Détacher du Bas-Monde (Dunyâ)",
                "versets": "v.695 – v.727",
                "duree": "4 min",
                "icone": "fa-hourglass-half",
                "resume": "Troisième obstacle du Chapitre 1 : le bas-monde trompeur et éphémère. Comprendre sa brièveté, l'utiliser comme un pont vers l'Au-delà sans jamais laisser son amour envahir le cœur.",
                "passages": [
                    {"ref": "Ch.1 · v.695–727", "titre": "Un lieu de passage, jamais une demeure", "texte": "Le bas-monde (dunyâ) séduit par son éclat fugitif mais ne tient jamais ses promesses. Celui qui en fait son but ultime se perd, tandis que le sage l'utilise comme simple moyen pour l'Au-delà."},
                    {"ref": "Lien v.10 & v.1074–1077", "titre": "Où sont passés les anciens ?", "texte": "« Où sont-ils les anciens et les richesses qu'ils avaient accumulées ? » Rappelle-toi que ce bas-monde est un lieu de passage : seul est intelligent celui qui œuvre nuit et jour pour la Demeure éternelle."},
                    {"ref": "Lien v.1123–1125 & v.1381", "titre": "Utiliser le licite sans y attacher son cœur", "texte": "Le vrai détachement (zuhd) n'interdit pas de posséder le licite pour adorer Allah et aider sa famille ; il consiste à refouler l'amour exclusif du monde hors du cœur."},
                ],
                "questions": [
                    {"q": "Quel est le troisième obstacle spirituel du Chapitre 1 du Sommaire ?", "options": ["Le bas-monde (dunyâ)", "La prière de nuit", "La lecture", "L'hospitalité"], "answer": 0, "explication": "Le Sommaire traite du bas-monde aux vers 695–727."},
                    {"q": "À quoi parvient celui qui ne s'attarde pas sur les choses de ce bas-monde (v.10) ?", "options": ["À la proximité d'Allah, la Vérité", "À la tristesse permanente", "À l'oubli de ses devoirs", "À la paresse"], "answer": 0, "explication": "v.10 : il parvient à la proximité d'Allah."},
                    {"q": "Quelle question le livre pose-t-il pour guérir de l'attachement au monde (v.1074–1075) ?", "options": ["« Où sont-ils les anciens et les biens qu'ils avaient accumulés ? »", "« Comment gagner plus d'or ? »", "« Qui est le plus célèbre ? »", "« Où construire un palais ? »"], "answer": 0, "explication": "v.1074–1075 rappellent le néant et la fin imminente des biens accumulés."},
                    {"q": "Avec quelle intention doit-on user des biens licites qu'Allah procure (v.1123–1125) ?", "options": ["Avec l'intention de L'adorer, de parvenir aux œuvres pies et d'éviter l'illicite", "Sans aucune intention", "Pour écraser les pauvres", "Pour s'en vanter"], "answer": 0, "explication": "v.1124–1125 : user des biens licites avec l'intention d'obéir à Allah comble de bienfaits."},
                    {"q": "Qu'est-ce qui est condamné aux vers 1381–1383 ?", "options": ["L'amour du monde qui s'empare totalement du cœur avec la thésaurisation", "Le travail honnête", "Nourrir sa famille", "Donner l'aumône"], "answer": 0, "explication": "v.1381–1383 visent l'absorption totale du cœur dans la passion de la fortune."},
                    {"q": "Que signifie méditer sur l'inconstance de ce monde selon les vers 418–419 ?", "options": ["Cela soutient le courage de l'aspirant et assoit sa rectitude", "Cela mène au désespoir", "Cela empêche de travailler", "Cela diminue la foi"], "answer": 0, "explication": "v.418–419 : la méditation sur la fin de ce monde renforce courage et rectitude."},
                ],
            },
            {
                "num": 15,
                "slug": "mystique-creatures-humaines",
                "titre": "Ch.1 (4) : Rapports Justes avec les Créatures",
                "versets": "v.728 – v.741",
                "duree": "4 min",
                "icone": "fa-users",
                "resume": "Quatrième obstacle du Chapitre 1 : l'attachement excessif aux créatures (crainte de leur regard, recherche de leurs éloges, fréquentations nuisibles). Garder son cœur tourné vers Allah tout en servant les humains avec bonté.",
                "passages": [
                    {"ref": "Ch.1 · v.728–741", "titre": "Ne dépendre que du Créateur", "texte": "Les créatures humaines deviennent un obstacle quand on cherche leur approbation, qu'on craint leurs critiques ou qu'on perd son temps dans des compagnies qui éloignent d'Allah."},
                    {"ref": "Lien v.997 & v.1025 & v.1120", "titre": "Ne pas être esclave du regard d'autrui", "texte": "Ne tourne la tête ni par crainte ni par désir vers les créatures, mais aie recours au Créateur. Celui qui abandonne ce dont il est certain pour croire aux propos des gens qui ne le connaissent pas agit comme un somnambule (v.1025)."},
                    {"ref": "Équilibre fraternel", "titre": "Détachement du cœur, service des mains", "texte": "Se détacher de la convoitise envers les créatures ne signifie jamais les mépriser : on leur rend service pour Allah (v.466), on voile leurs défauts et on choisit des compagnons vertueux."},
                ],
                "questions": [
                    {"q": "Quel est le quatrième obstacle cité au Chapitre 1 du Sommaire ?", "options": ["Les créatures humaines (attachement excessif à leur regard et convoitise)", "Les livres", "Les mosquées", "Les montagnes"], "answer": 0, "explication": "Le Sommaire cite les créatures humaines aux vers 728–741."},
                    {"q": "Comment le vers 1025 décrit-il celui qui préfère les propos des humains à ce dont il est certain sur lui-même ?", "options": ["Un somnambule", "Un grand sage", "Un modèle d'humilité", "Un ascète parfait"], "answer": 0, "explication": "v.1025 : il est qualifié de « somnambule »."},
                    {"q": "Vers qui le vers 1120 ordonne-t-il de tourner son cœur en cas de besoin ou de crainte ?", "options": ["Vers le Créateur, et non vers les créatures impuissantes", "Vers les notables influents", "Vers les plus riches", "Vers les foules"], "answer": 0, "explication": "v.1120 : « Ne tourne la tête de quelque côté que ce soit vers les créatures, mais aie recours au Créateur. »"},
                    {"q": "Quelle est la juste attitude sociale tout en restant détaché des créatures (v.466 & v.1072) ?", "options": ["Leur rendre service pour Allah et voiler leurs défauts", "Les insulter et les fuir avec orgueil", "Ne jamais leur sourire", "Refuser de les aider"], "answer": 0, "explication": "Le détachement concerne la convoitise du cœur ; la conduite extérieure reste pleine de bonté et de service."},
                    {"q": "Pourquoi se plaindre aux créatures de ses épreuves est-il vain (v.998) ?", "options": ["Parce qu'elles sont elles-mêmes de pauvres créatures impuissantes", "Parce qu'elles n'entendent pas", "Parce que c'est interdit de parler", "Parce qu'elles sont toujours ennemies"], "answer": 0, "explication": "v.998 rappelle leur impuissance face au Décret d'Allah."},
                    {"q": "Quel défaut naît du désir excessif d'éloges et de la peur des critiques (v.1023–1024) ?", "options": ["L'ignorance spirituelle, la distraction et la perte de sincérité", "La sérénité du cœur", "La force de la foi", "L'amour de la vérité"], "answer": 0, "explication": "v.1023–1024 montrent que ce mal vient de la distraction et trompe le serviteur."},
                ],
            },
            {
                "num": 16,
                "slug": "mystique-action-devote",
                "titre": "Ch.1 (5) : L'Action Dévote Sincère",
                "versets": "v.742 – v.872",
                "duree": "4 min",
                "icone": "fa-hands-holding-circle",
                "resume": "Cinquième volet du Chapitre 1 : les conditions qui rendent l'action dévote vivante et agréée — intention pure (ikhlâs), conformité à la Sunna, persévérance même en petite quantité et présence du cœur.",
                "passages": [
                    {"ref": "Ch.1 · v.742–872", "titre": "Qualité avant quantité", "texte": "L'action dévote n'a de valeur auprès d'Allah que par la sincérité de l'intention (ikhlâs), la conformité à la Loi révélée (Sharî'a) et la présence du cœur."},
                    {"ref": "Lien v.123–125 & v.146", "titre": "Constance et profit multiple", "texte": "Les œuvres les plus aimées d'Allah sont celles accomplies avec persévérance, fussent-elles peu nombreuses, celles qui purifient le cœur et celles qui profitent au plus grand nombre."},
                    {"ref": "Lien v.1192–1193", "titre": "Humilité après l'action", "texte": "Après une bonne œuvre, le serviteur lucide sait qu'Allah Seul lui a facilité cet acte : il reste donc reconnaissant, conscient de son insuffisance et exempt de toute fierté."},
                ],
                "questions": [
                    {"q": "Quelles sont les conditions essentielles d'une action dévote agréée ?", "options": ["Intention pure pour Allah, conformité à la Sunna et présence du cœur", "Être vue par le maximum de gens", "Être accomplie avec orgueil", "Être très rapide"], "answer": 0, "explication": "v.3, v.93 & v.742–872 insistent sur l'ikhlâs, la Sunna et la présence du cœur."},
                    {"q": "Entre une petite action constante et une grande action vite abandonnée, que préfère le sage (v.125) ?", "options": ["L'action accomplie avec persévérance, fût-elle en faible quantité", "L'action accomplie une seule fois", "L'action faite pour être applaudie", "Aucune différence"], "answer": 0, "explication": "v.125 loue l'action accomplie avec persévérance, même en faible quantité."},
                    {"q": "Que doit reconnaître l'adorateur au sujet de l'origine de sa bonne action (v.1192) ?", "options": ["Qu'Allah Seul est à l'origine de son acte et lui a facilité cette grâce", "Qu'il ne doit rien à personne", "Qu'il est supérieur aux autres", "Qu'il mérite les louanges publiques"], "answer": 0, "explication": "v.1192–1193 : attribuer la grâce à Allah préserve de la fierté et de la présomption."},
                    {"q": "Pourquoi les actions exhibées perdent-elles souvent leur mérite au Jour du Jugement (v.150–151) ?", "options": ["Parce qu'elles risquent d'être corrompues par l'ostentation", "Parce qu'Allah ne les voit pas", "Parce qu'elles sont trop courtes", "Parce qu'elles sont faites le jour"], "answer": 0, "explication": "v.150–151 recommandent la discrétion pour préserver la pureté de l'intention."},
                    {"q": "Que dit le vers 146 sur la constance dans l'action ?", "options": ["S'évertuer tout le temps dans les actions avec bonne intention, sans jamais se lasser", "Travailler uniquement en hiver", "Attendre d'être âgé", "Ne faire que les obligations strictes"], "answer": 0, "explication": "v.146 exhorte à la persévérance continue avec bonne intention."},
                    {"q": "Quelle est la relation entre le bien accompli et le bien futur (v.1158–1159) ?", "options": ["Le bien appelle le bien, et une petite quantité en entraîne une grande", "Un petit bien ne sert à rien", "Le bien fatigue le cœur", "Seuls les grands actes comptent"], "answer": 0, "explication": "v.1158–1159 : le bien appelle le bien et une petite graine grandit."},
                ],
            },
        ],
    },
    {
        "id": 3,
        "code": "porte-3",
        "titre": "Porte III · Chapitre 2 — Les Vices Graves & Remèdes",
        "sous_titre": "10 sous-chapitres du Sommaire · Vices apparents/cachés, Orgueil, Riyâ, Hasad, Hiqd, Pleurnicherie, Kasb & Tawakkul, Colère (v.886–1087)",
        "icone": "fa-shield-heart",
        "couleur": "from-rose-700 to-amber-800",
        "accent": "#FB7185",
        "chapitres": [
            {
                "num": 17,
                "slug": "vices-apparents-caches",
                "titre": "Ch.2 (1) : Les Vices Apparents & Cachés",
                "versets": "v.886 – v.920",
                "duree": "4 min",
                "icone": "fa-magnifying-glass",
                "resume": "Ouverture du Chapitre 2 : distinguer les vices apparents des organes (langue, regard, mains, ventre) et les vices cachés du cœur (plus dangereux car invisibles), qui tous dessèchent le cœur et bloquent la lumière.",
                "passages": [
                    {"ref": "Ch.2 · v.886–894", "titre": "Les vices apparents (des organes)", "texte": "Les vices apparents touchent les membres : paroles interdites, médisance, mensonge, regard prohibé, consommation illicite, injustice envers les biens ou l'honneur d'autrui."},
                    {"ref": "Ch.2 · v.895–920", "titre": "Les vices cachés (maladies du cœur)", "texte": "Les vices cachés résident dans le cœur : orgueil, ostentation, jalousie, haine, rancune, avarice, amour du prestige. Ils sont encore plus redoutables car ils peuvent ronger les œuvres pieuses en secret."},
                    {"ref": "Lien v.1532–1535", "titre": "Un seul vice peut gâcher l'œuvre", "texte": "Cheikh Ahmadou Bamba prévient qu'un seul de ces vices graves (médisance, ostentation, fierté, jalousie, présomption) suffit à causer le refus des bonnes actions auprès d'Allah."},
                ],
                "questions": [
                    {"q": "Quelles sont les deux grandes catégories de vices au début du Chapitre 2 ?", "options": ["Les vices apparents (organes) et les vices cachés (cœur)", "Les vices anciens et modernes", "Les vices d'hiver et d'été", "Les vices longs et courts"], "answer": 0, "explication": "Le Sommaire du Ch.2 divise les vices en apparents (v.886–894) et cachés (v.895–920)."},
                    {"q": "Pourquoi les vices cachés du cœur sont-ils particulièrement dangereux ?", "options": ["Parce qu'ils peuvent ronger et invalider les bonnes œuvres en secret", "Parce qu'ils ne comptent pas", "Parce que tout le monde les voit", "Parce qu'ils disparaissent seuls"], "answer": 0, "explication": "v.1534–1535 rappellent qu'un seul vice caché peut entraîner le refus des œuvres."},
                    {"q": "Quel effet les péchés répétés produisent-ils sur le cœur (v.1152) ?", "options": ["Ils entraînent la sécheresse du cœur et bloquent la Miséricorde", "Ils renforcent la mémoire", "Ils améliorent le sommeil", "Ils n'ont aucun effet"], "answer": 0, "explication": "v.1152–1153 : les péchés dessèchent le cœur et s'interposent devant la Miséricorde."},
                    {"q": "Lequel de ces défauts est un vice apparent des organes ?", "options": ["La médisance et les paroles interdites", "La jalousie secrète", "La présomption intérieure", "La rancune cachée"], "answer": 0, "explication": "La médisance et le mensonge s'expriment par l'organe de la langue."},
                    {"q": "Lequel de ces défauts est un vice caché du cœur ?", "options": ["La jalousie (hasad) et l'orgueil (kibr)", "Manger trop vite", "Parler fort", "Marcher vite"], "answer": 0, "explication": "Jalousie, orgueil et ostentation sont des maladies intérieures du cœur."},
                    {"q": "Qu'apporte la purification du cœur de tous ces vices (v.9) ?", "options": ["La lumière et l'agrément d'Allah", "La célébrité mondaine", "La dispense du jeûne", "La fin des responsabilités"], "answer": 0, "explication": "v.9 : purifier son cœur de tous vices procure la lumière et l'agrément d'Allah."},
                ],
            },
            {
                "num": 18,
                "slug": "vices-orgueil-honte-fierte",
                "titre": "Ch.2 (2) : L'Orgueil, la Honte (Hayâ) & la Fierté",
                "versets": "v.921 – v.932",
                "duree": "4 min",
                "icone": "fa-mountain",
                "resume": "Trois premières maladies détaillées au Chapitre 2 : l'orgueil (se croire au-dessus des créatures), la mauvaise timidité qui empêche d'apprendre ou de dire vrai, et la fierté (pire que tous les péchés selon v.1211).",
                "passages": [
                    {"ref": "Ch.2 · v.922–923", "titre": "L'Orgueil (Kibr)", "texte": "L'orgueil consiste à rejeter la vérité et à mépriser les créatures en s'estimant supérieur. Pourtant, nul ne connaît comment finira sa vie ni quelle sera sa destinée demain."},
                    {"ref": "Ch.2 · v.924", "titre": "La mauvaise honte vs la noble pudeur (Hayâ)", "texte": "La noble pudeur devant Allah est sœur de la foi ; mais la fausse honte mondaine qui empêche de poser une question utile, de demander pardon ou d'obéir à Allah est un vice à soigner."},
                    {"ref": "Ch.2 · v.925–932 & v.1211", "titre": "La Fierté (Fakhr)", "texte": "La fierté est pire que les autres péchés (v.1211) : elle inculque à l'homme l'autosuffisance, le rend orgueilleux et négligent, et l'écarte du Chemin d'Allah."},
                ],
                "questions": [
                    {"q": "Quels trois sujets ouvrent la liste des remèdes détaillés du Chapitre 2 (v.922–932) ?", "options": ["L'orgueil, la honte (hayâ) et la fierté", "Le voyage, le jeûne et le commerce", "Le sommeil, la faim et le rire", "L'or, l'argent et les livres"], "answer": 0, "explication": "Le Sommaire liste : 1. L'orgueil (v.922–923), 2. La honte (v.924), 3. La fierté (v.925+)."},
                    {"q": "Pourquoi le vers 1211–1212 dit-il que la fierté est pire que tous les péchés ?", "options": ["Elle inculque l'autosuffisance, rend l'homme orgueilleux et l'écarte du Chemin d'Allah", "Parce qu'elle coûte cher", "Parce qu'elle fait dormir", "Parce qu'elle est visible"], "answer": 0, "explication": "v.1211–1212 : la fierté nourrit l'illusion d'autosuffisance."},
                    {"q": "Quelle est la différence entre la noble pudeur et la mauvaise honte ?", "options": ["La noble pudeur empêche le péché ; la mauvaise honte empêche d'apprendre la religion ou de se repentir", "Elles sont identiques", "La pudeur est un défaut", "Il ne faut jamais avoir de pudeur"], "answer": 0, "explication": "La pudeur devant Allah protège la foi, tandis que la fausse timidité bloque la quête de vérité."},
                    {"q": "Pourquoi ne dois-tu jamais te croire supérieur à quiconque (v.1027 & v.1079) ?", "options": ["Parce que c'est une grande illusion et nul ne connaît sa propre fin", "Parce que tout le monde a le même âge", "Parce que les savants sont égaux aux ignorants", "Parce que la vie est longue"], "answer": 0, "explication": "v.1027 & 1079 : le terme de la vie et son issue demeurent le secret d'Allah."},
                    {"q": "Quel remède inattendu le vers 1210 évoque-t-il quand une faute brise l'orgueil du serviteur ?", "options": ["L'humilité et le repentir sincère peuvent guérir de la fierté et de l'aveuglement", "Continuer à pécher", "Cacher sa faute avec fierté", "Accuser autrui"], "answer": 0, "explication": "v.1210 : l'humiliation devant Allah après une chute peut guérir de l'orgueil."},
                    {"q": "Quel comportement envers un serviteur en humble vêtement prévient l'orgueil (v.1473) ?", "options": ["Ne jamais le mépriser, car il peut être rempli de lumières et de secrets divins", "L'ignorer", "Lui donner des ordres", "Le juger sur son habit"], "answer": 0, "explication": "v.1473–1474 mettent en garde contre le mépris fondé sur l'apparence."},
                ],
            },
            {
                "num": 19,
                "slug": "vices-presomption-ostentation",
                "titre": "Ch.2 (3) : Présomption ('Ujb) & Ostentation (Riyâ)",
                "versets": "v.933 – v.968",
                "duree": "4 min",
                "icone": "fa-masks-theater",
                "resume": "Quatrième et cinquième maladies du Sommaire : la présomption ('ujb — s'admirer soi-même), l'ostentation (riyâ — agir pour être vu) et la recherche de réputation (sum'a), ainsi que leurs remèdes par la discrétion et l'ikhlâs.",
                "passages": [
                    {"ref": "Ch.2 · v.933–938", "titre": "La Présomption ('Ujb)", "texte": "La présomption consiste à s'émerveiller de ses propres œuvres ou de son savoir en oubliant qu'ils sont un pur don d'Allah. Elle conduit à la perte et aveugle le serviteur sur ses lacunes."},
                    {"ref": "Ch.2 · v.939–968 & note v.1157", "titre": "L'Ostentation (Riyâ) et la Sum'a", "texte": "Le Riyâ est le fait d'accomplir un acte louable dans le dessein d'en être estimé ou loué par les humains ; la Sum'a est de vouloir qu'on entende parler de ses bonnes œuvres."},
                    {"ref": "Remèdes", "titre": "Guérir par le secret et la conscience du Regard d'Allah", "texte": "Le remède est de cacher ses œuvres pies (v.150, v.1265), de réciter le dhikr à voix basse si l'on craint le riyâ (v.312) et de se rappeler que les créatures ne peuvent ni sauver ni condamner au Jour du Jugement."},
                ],
                "questions": [
                    {"q": "Comment le livre définit-il le « Riyâ » (ostentation) ?", "options": ["Accomplir un acte louable dans l'unique dessein d'en être estimé ou loué par les humains", "Prier à la mosquée avec sincérité", "Donner en secret", "Enseigner gratuitement"], "answer": 0, "explication": "Note p.38 (v.1157) & v.939–940 : le riyâ vise l'estime et la louange des hommes."},
                    {"q": "Qu'est-ce que le « 'Ujb » (présomption) ?", "options": ["S'admirer pour ses œuvres ou sa science en oubliant la grâce d'Allah", "Demander pardon", "Se sentir humble", "Consulter un savant"], "answer": 0, "explication": "v.933–940 mettent en garde contre l'autosatisfaction et la présomption."},
                    {"q": "Que signifie la « Sum'a » citée au Sommaire (v.939) ?", "options": ["Vouloir faire entendre et répandre le bruit de ses bonnes actions", "Écouter le Coran", "Garder le silence", "Prêter attention au sermon"], "answer": 0, "explication": "Sum'a (de sama'a, entendre) est l'ostentation par la réputation orale."},
                    {"q": "Quelle pratique du vers 312 aide à échapper au riyâ lors du dhikr ?", "options": ["Réciter à voix basse en toute discrétion", "Utiliser un haut-parleur", "Réciter seulement devant une foule", "Arrêter complètement le dhikr"], "answer": 0, "explication": "v.312 : si le fidèle craint le riyâ, il évoque Allah à voix basse."},
                    {"q": "Qu'arrive-t-il à la science apprise pour être admiré ou loué (v.160) ?", "options": ["Elle ne sert à rien au serviteur le Jour de la Résurrection", "Elle double sa récompense", "Elle efface ses fautes", "Elle le rend saint"], "answer": 0, "explication": "v.160 : la science apprise pour être admiré ne sert à rien le Jour dernier."},
                    {"q": "Quel conseil du vers 150–151 protège tes œuvres du riyâ ?", "options": ["Avoir soin de les accomplir discrètement, à l'insu des autres", "Les publier chaque matin", "Les raconter à tout le monde", "Cesser de faire le bien"], "answer": 0, "explication": "v.150–151 : accomplir ses œuvres discrètement préserve leur mérite."},
                ],
            },
            {
                "num": 20,
                "slug": "vices-jalousie-haine-mechancete",
                "titre": "Ch.2 (4) : Jalousie (Hasad), Haine (Hiqd) & Méchanceté",
                "versets": "v.969 – v.983",
                "duree": "4 min",
                "icone": "fa-eye-slash",
                "resume": "Définitions exactes des 6e, 7e et 8e vices du Sommaire (Hasad, Hiqd, Ghish) et remèdes pratiques enseignés par Cheikh Ahmadou Bamba : prier pour son frère en son absence et respecter les dons souverains d'Allah.",
                "passages": [
                    {"ref": "v.969 – v.971", "titre": "La Jalousie (Hasad)", "texte": "Souhaiter la disparition du bien d'un croyant est appelé hasad. Le jaloux s'attriste toujours du bonheur de son frère et ne se réjouit qu'à le voir dans le malheur."},
                    {"ref": "v.972 – v.974", "titre": "La Haine (Hiqd) & la Méchanceté (Ghish)", "texte": "Le hiqd est de haïr les gens de la bonne direction sans raison valable selon la Sharî'a. Le ghish consiste à cacher les défauts d'une chose ou d'une personne afin de faire trébucher l'intéressé."},
                    {"ref": "v.975 – v.983", "titre": "Remède : prier pour son frère en son absence", "texte": "Lutte contre la haine en priant pour ton frère en son absence et en lui souhaitant du bien. Qui déteste celui qu'Allah a favorisé s'oppose en réalité à la Volonté souveraine du Créateur !"},
                ],
                "questions": [
                    {"q": "Comment le vers 969 définit-il exactement le « hasad » (jalousie) ?", "options": ["Souhaiter la disparition du bien d'un croyant", "Vouloir progresser par son travail", "Admirer un savant", "Partager son repas"], "answer": 0, "explication": "v.969 définit le hasad comme le souhait de voir disparaître le bien d'un croyant."},
                    {"q": "Qu'est-ce que le « hiqd » (haine) selon le vers 972 ?", "options": ["Haïr les gens de la bonne direction sans raison valable selon la Sharî'a", "Corriger une injustice légalement", "Éviter le péché", "Garder le silence"], "answer": 0, "explication": "v.972 définit précisément le hiqd."},
                    {"q": "Qu'est-ce que le « ghish » (méchanceté/tromperie) selon le vers 973 ?", "options": ["Cacher les défauts d'une chose ou personne pour faire trébucher l'intéressé", "Conseiller discrètement", "Voiler une faute par miséricorde", "Pardonner une offense"], "answer": 0, "explication": "v.973 définit le ghish comme la dissimulation malveillante d'un défaut."},
                    {"q": "Quel remède concret le vers 977 prescrit-il contre la haine ?", "options": ["Prier pour ton frère en son absence et lui souhaiter du bien", "Crier sa colère", "Raconter ses erreurs", "Rompre tout lien"], "answer": 0, "explication": "v.977 : prier pour lui en son absence et lui souhaiter du bien."},
                    {"q": "Contre qui s'oppose réellement celui qui déteste qui Allah a favorisé (v.978–980) ?", "options": ["Contre la Volonté souveraine d'Allah Lui-même", "Contre un simple voisin", "Contre les lois du commerce", "Contre personne"], "answer": 0, "explication": "v.979–980 : il conçoit du dépit contre l'arrêt souverain d'Allah."},
                    {"q": "Que dit le proverbe cité au vers 1447 sur le jaloux ?", "options": ["« Certes, un jaloux n'est jamais noble (de caractère) »", "« Le jaloux réussit toujours »", "« La jalousie est un petit défaut »", "« Le jaloux est généreux »"], "answer": 0, "explication": "v.1447 : un jaloux n'est jamais noble car il souhaite la perte du bien de ses frères."},
                ],
            },
            {
                "num": 21,
                "slug": "embellir-for-interieur",
                "titre": "Ch.2 (5) : Embellir le For Intérieur & Fuir le Prestige",
                "versets": "v.984 – v.997",
                "duree": "4 min",
                "icone": "fa-gem",
                "resume": "Soigner le cœur plutôt que la façade extérieure, car Allah regarde le cœur tandis que les créatures ne voient que l'apparence ; puis éviter la soif de gloire, d'autorité et la rivalité dans la science religieuse.",
                "passages": [
                    {"ref": "v.984 – v.989", "titre": "La vraie beauté naît du cœur", "texte": "Embellis ton for intérieur, lieu du regard du Maître des créatures, au lieu de soigner uniquement l'extérieur. Celui qui perfectionne l'état de son cœur voit aussitôt s'embellir ses actes et ses paroles."},
                    {"ref": "v.990 – v.992", "titre": "Gloire, autorité et intention", "texte": "La recherche de gloire, le souci du prestige, la soif d'autorité et le désir de se distinguer éloignent d'Allah — sauf si l'on s'en sert comme pur moyen pour chercher Sa Face et Son agrément."},
                    {"ref": "v.993 – v.996", "titre": "Science sans rivalité", "texte": "L'esprit de rivalité ou la volonté de faire fortune dans la science religieuse mène à la perdition. Remercie plutôt Allah d'avoir fait de toi un réceptacle de la science qui te guide."},
                ],
                "questions": [
                    {"q": "Par quoi repousse-t-on l'artifice extérieur cachant un cœur troublé (v.984–985) ?", "options": ["Par la répétition continuelle des Noms d'Allah avec présence du cœur", "Par de nouveaux habits", "Par des discours longs", "Par le sommeil"], "answer": 0, "explication": "v.985 prescrit le dhikr continuel avec présence du cœur."},
                    {"q": "Quelle différence le vers 987 trace-t-il entre le regard d'Allah et celui des créatures ?", "options": ["Allah considère le cœur et ses qualités, les créatures ne regardent que l'aspect extérieur", "Les créatures sondent les cœurs", "Allah regarde l'apparence seulement", "Aucune différence"], "answer": 0, "explication": "v.987 : le Seigneur regarde le cœur, les créatures l'apparence."},
                    {"q": "Que récolte celui qui perfectionne l'état de son cœur (v.988–989) ?", "options": ["Une beauté sans artifice, des actes et paroles améliorés et le bonheur", "L'isolement triste", "La perte de ses amis", "Rien de visible"], "answer": 0, "explication": "v.988–989 : embellir l'intérieur embellit naturellement actes et paroles."},
                    {"q": "Dans quel unique cas une position d'autorité n'éloigne-t-elle pas d'Allah (v.992) ?", "options": ["Si l'on s'en sert comme moyen pour chercher la Face et l'agrément d'Allah", "Si l'on cherche à dominer", "Si l'on vise la fortune", "Si l'on aime les éloges"], "answer": 0, "explication": "v.992 distingue l'objectif mondain du service exclusif d'Allah."},
                    {"q": "À quoi mènent l'esprit de rivalité et l'orgueil dans la science religieuse (v.993–994) ?", "options": ["À la confusion et à la perdition", "À la sainteté", "À la paix du cœur", "À l'agrément divin"], "answer": 0, "explication": "v.994 : tout cela confond le savant et le mène à la perdition."},
                    {"q": "Quelle attitude de gratitude recommande le vers 996 face à la science reçue ?", "options": ["Remercier Allah d'avoir fait de toi un réceptacle de la science qui guide", "Se vanter devant les débutants", "Cacher la science aux autres", "Vendre ses fatwas"], "answer": 0, "explication": "v.996 invite à la gratitude envers Allah."},
                ],
            },
            {
                "num": 22,
                "slug": "vices-pleurnicherie-decret",
                "titre": "Ch.2 (6) : La Pleurnicherie & Le Décret Divin",
                "versets": "v.998 – v.1029",
                "duree": "4 min",
                "icone": "fa-scale-unbalanced",
                "resume": "Guérir de l'habitude de se plaindre aux créatures impuissantes en réalisant que le Décret divin est déjà écrit, qu'Allah garantit chaque subsistance, et qu'il faut garder bonne opinion des croyants sans favoriser le riche sur l'indigent.",
                "passages": [
                    {"ref": "v.998 – v.1009", "titre": "Les 4 décrets & la souveraineté d'Allah", "texte": "Le Seigneur en a fini avec quatre choses : la durée de vie, la création, le caractère et la subsistance. Si toutes les créatures se coalisaient, elles ne déplaceraient pas un seul atome sans Sa permission."},
                    {"ref": "v.1010 – v.1021", "titre": "Confiance en Allah & respect du pauvre", "texte": "Allah assure à tout être sa subsistance. Ne désespère jamais dans le dénuement, et n'accorde jamais dans ton cœur plus de place au riche en te détournant de l'indigent."},
                    {"ref": "v.1026 – v.1029", "titre": "S'accuser soi-même et bien penser d'autrui", "texte": "Avoir une mauvaise opinion des autres et une haute idée de soi-même vient de la faiblesse. Soigne-toi en examinant tes propres fautes et garde toujours bonne opinion des croyants."},
                ],
                "questions": [
                    {"q": "Quelles quatre choses Allah a-t-Il déjà achevé de décréter (v.1001) ?", "options": ["Durée de vie, création, caractère et fortune (subsistance)", "Maison, métier, ville et amis", "Livres, voyages, habits et âge", "Climat, récoltes, mer et vent"], "answer": 0, "explication": "v.1001 énumère ces quatre décrets divins."},
                    {"q": "Que pourraient faire toutes les créatures réunies sans la permission de l'Éternel (v.1005–1007) ?", "options": ["Rien — pas même déplacer un seul atome", "Retirer ta subsistance", "Changer ton destin", "Raccourcir ta vie"], "answer": 0, "explication": "v.1006–1007 affirment leur impuissance totale sans la permission d'Allah."},
                    {"q": "Qui est le garant assermenté de la subsistance de chaque être (v.1014) ?", "options": ["Allah Très-Haut", "Les riches", "Les notables", "Le hasard"], "answer": 0, "explication": "v.1014 : Allah assure à tout être sa subsistance et en est le garant."},
                    {"q": "Quelle attitude envers le riche et l'indigent est blâmée au vers 1020 ?", "options": ["Accorder plus de place au riche dans son cœur en se détournant de l'indigent", "Saluer les deux avec bonté", "Aider l'indigent", "Conseiller le riche"], "answer": 0, "explication": "v.1020–1021 rappellent l'avertissement coranique à ce sujet."},
                    {"q": "D'où provient le fait d'avoir une mauvaise opinion des autres et une idée avantageuse de soi (v.1026) ?", "options": ["De la faiblesse et de la naïveté", "De la clairvoyance", "De la piété", "De la sagesse"], "answer": 0, "explication": "v.1026 attribue cela à la faiblesse et à la naïveté."},
                    {"q": "Comment se soigner des idées noires sur autrui selon les vers 1028–1029 ?", "options": ["En s'accusant soi-même et en gardant bonne opinion sur la fin mystérieuse de tous", "En espionnant ses voisins", "En publiant leurs erreurs", "En s'isolant avec rancœur"], "answer": 0, "explication": "v.1028–1029 recommandent l'autocritique et la bonne opinion envers les croyants."},
                ],
            },
            {
                "num": 23,
                "slug": "vices-remise-lendemain",
                "titre": "Ch.2 (7) : La Remise au Lendemain (Procrastination)",
                "versets": "v.1030 – v.1035",
                "duree": "3 min",
                "icone": "fa-clock-rotate-left",
                "resume": "Six vers saisissants sur le poison de la procrastination : Allah n'oublie pas le poids d'un atome, et la plupart des cris des pécheurs en Enfer viennent d'avoir remis les œuvres pies au lendemain.",
                "passages": [
                    {"ref": "v.1030 – v.1031", "titre": "Le remède à la négligence", "texte": "Guéris-toi de la réticence, de la remise au lendemain des bonnes actions et de la négligence en méditant le châtiment des damnés et la félicité éternelle promise aux vertueux."},
                    {"ref": "v.1032 – v.1033", "titre": "Rien n'est oublié", "texte": "Sache qu'Allah ne néglige ni n'oublie rien de nos actions manifestes ou secrètes : Il demandera compte pour le poids d'un atome, grande ou petite."},
                    {"ref": "v.1034 – v.1035", "titre": "Tu ignores si demain t'appartient", "texte": "« Sache que la plupart des cris des pécheurs demain dans l'Enfer ont pour cause la remise au lendemain des actes pieux : tu ne sais ni si tu vivras jusqu'au lendemain, ni si tu seras capable de les accomplir comme aujourd'hui. »"},
                ],
                "questions": [
                    {"q": "Par quelle méditation le vers 1031 invite-t-il à soigner la remise au lendemain ?", "options": ["La réflexion sur le châtiment et sur la félicité éternelle", "En faisant de longs projets mondains", "En dormant davantage", "En attendant la retraite"], "answer": 0, "explication": "v.1031 prescrit la méditation de l'Au-delà (châtiment et félicité)."},
                    {"q": "Jusqu'à quelle précision Allah demandera-t-Il compte de nos actes (v.1033) ?", "options": ["Jusqu'au poids d'un atome, sans rien omettre", "Seulement les grands actes publics", "Seulement les actes de la dernière année", "Uniquement les paroles"], "answer": 0, "explication": "v.1033 : Il demandera compte pour le poids d'un atome."},
                    {"q": "Quelle est la cause de la plupart des cris des pécheurs en Enfer (v.1034) ?", "options": ["La remise au lendemain des actes pieux", "Le manque de fortune", "La fatigue du travail", "L'absence de voyage"], "answer": 0, "explication": "v.1034 pointe directement la procrastination des œuvres pies."},
                    {"q": "Quelles deux incertitudes le vers 1035 oppose-t-il à « je le ferai demain » ?", "options": ["Tu ne sais ni si tu vivras demain, ni si tu auras encore la capacité de le faire", "Tu ne sais pas quel temps il fera", "Tu ne sais pas qui viendra", "Tu ne sais pas l'heure exacte"], "answer": 0, "explication": "v.1035 : ni la vie de demain ni la capacité d'agir demain ne sont garanties."},
                    {"q": "Allah oublie-t-Il les actions accomplies en secret (v.1032) ?", "options": ["Non, Il ne néglige ni n'oublie rien, manifeste ou secret", "Oui, les petites actions secrètes", "Seulement les bonnes actions", "Seulement la nuit"], "answer": 0, "explication": "v.1032 : rien de manifeste ni de secret n'échappe à Allah."},
                    {"q": "Quel conseil d'action immédiate découle de ces vers ?", "options": ["Accomplir aujourd'hui le bien dont tu es capable sans attendre demain", "Remettre la prière au mois prochain", "Attendre d'être parfait pour commencer", "Remettre le repentir à la vieillesse"], "answer": 0, "explication": "v.1030–1035 appellent à l'empressement immédiat vers les bonnes œuvres."},
                ],
            },
            {
                "num": 24,
                "slug": "travail-kasb-tawakkul",
                "titre": "Ch.2 (8) : Travail (Kasb) & Abandon à Allah (Tawakkul)",
                "versets": "v.1036 – v.1056",
                "duree": "4 min",
                "icone": "fa-briefcase",
                "resume": "Un enseignement central du Mouridisme : le Tawakkul n'exclut jamais le travail licite (Kasb). Utiliser les causes établies par Allah (Sharî'a) tout en plaçant sa confiance absolue en Lui Seul (Haqîqa).",
                "passages": [
                    {"ref": "v.1036 – v.1039", "titre": "Allier le Kasb et le Tawakkul", "texte": "Abandonner le travail utile sous prétexte de s'en remettre à Allah tout en enviant les gens est le comportement des sots. Le tawakkul n'exclut nullement le kasb (travail) : le meilleur comportement est d'allier les deux !"},
                    {"ref": "v.1040 – v.1044", "titre": "Respecter la loi des causes", "texte": "Allah a fondé ce monde sur la loi de cause à effet en mettant des moyens à notre disposition. Vouloir atteindre un but en négligeant les moyens requis est une impertinence et mène à l'échec."},
                    {"ref": "v.1049 – v.1056", "titre": "L'union parfaite de la Sharî'a et de la Haqîqa", "texte": "Agis extérieurement selon les causes (Sharî'a) avec un cœur détaché qui ne compte intérieurement que sur Allah Seul (Haqîqa). Omettre la première est une hérésie ; omettre la seconde mène à l'idolâtrie."},
                ],
                "questions": [
                    {"q": "Comment le vers 1036 qualifie-t-il celui qui cesse de travailler sous prétexte de tawakkul tout en enviant les gens ?", "options": ["Le comportement des sots", "Un grand ascète", "Un saint parfait", "Un sage accompli"], "answer": 0, "explication": "v.1036 critique fermement cette paresse déguisée."},
                    {"q": "Le tawakkul (abandon à Allah) exclut-il le kasb (travail) selon le vers 1037 ?", "options": ["Non, il n'exclut nullement le travail pour gagner son pain", "Oui, totalement", "Oui, sauf pour les commerçants", "Uniquement pour les jeunes"], "answer": 0, "explication": "v.1037 : l'abandon à Allah n'exclut nullement le kasb."},
                    {"q": "En quoi consiste le meilleur comportement selon le vers 1039 ?", "options": ["Allier le travail (kasb) à l'abandon confiant à Allah", "Ne compter que sur ses propres muscles", "Attendre sans rien faire", "Vivre aux dépens d'autrui"], "answer": 0, "explication": "v.1039 : allier le kasb à l'abandon à Allah."},
                    {"q": "Qu'arrive-t-il à qui veut atteindre un but en passant outre les moyens requis (v.1043–1044) ?", "options": ["Il fait preuve d'impertinence et ses efforts seront vains", "Il réussit plus vite", "Il devient un modèle", "Il est excusé"], "answer": 0, "explication": "v.1043–1044 : négliger les moyens établis par Allah rend les efforts vains."},
                    {"q": "Comment réunit-on Sharî'a et Haqîqa dans l'action quotidienne (v.1053–1055) ?", "options": ["Respecter les causes extérieures (Sharî'a) tout en se soumettant intérieurement à Allah (Haqîqa)", "Rejeter la Sharî'a", "Oublier Allah pendant le travail", "Éviter toute action"], "answer": 0, "explication": "v.1053–1055 enseignent cette union harmonieuse."},
                    {"q": "Que dit le vers 1056 si l'on omet l'une des deux (Sharî'a ou Haqîqa) ?", "options": ["Omettre la Sharî'a est hérésie, omettre la Haqîqa est idolâtrie", "Aucune conséquence", "Une seule suffit", "Elles s'opposent toujours"], "answer": 0, "explication": "v.1056 rappelle l'équilibre vital entre les deux."},
                ],
            },
            {
                "num": 25,
                "slug": "long-espoir-passion-monde",
                "titre": "Ch.2 (9) : Long Espoir, Désespoir & Passion du Monde",
                "versets": "v.1057 – v.1082",
                "duree": "4 min",
                "icone": "fa-compass-drafting",
                "resume": "Combattre le long espoir et l'oisiveté, ne pas se laisser leurrer par le sursis d'Allah, guérir du désespoir par Sa Miséricorde, voiler les fautes d'autrui et se détacher de la passion du bas-monde.",
                "passages": [
                    {"ref": "v.1057 – v.1065", "titre": "Danger du long espoir et de l'oisiveté", "texte": "Le long espoir empêche le repentir et dessèche le cœur. Une vie passée dans l'oisiveté est une grave catastrophe : la vie humaine est trop précieuse pour être gaspillée."},
                    {"ref": "v.1066 – v.1072", "titre": "Sursis divin, remède du désespoir & indulgence", "texte": "Si Allah ne te punit pas aussitôt, ce n'est pas un oubli. Le remède du désespoir est de penser à la Magnanimité et à la Miséricorde d'Allah. Et pour guérir de l'aveuglement sur tes propres défauts, accepte les excuses et voile les fautes de tes frères."},
                    {"ref": "v.1073 – v.1082", "titre": "Passion du bas-monde & humilité dans le don", "texte": "Ce bas-monde n'est pas éternel : seul est intelligent qui œuvre pour l'Au-delà. Ne tire jamais gloire d'un bienfait accordé à autrui : c'est Allah qui donne, tu n'es qu'un intermédiaire."},
                ],
                "questions": [
                    {"q": "Que provoquent le long espoir et les projets lointains (v.1057–1058) ?", "options": ["Ils empêchent le repentir, dessèchent le cœur et engendrent la paresse", "Ils fortifient la piété", "Ils effacent les fautes", "Ils apportent la sérénité"], "answer": 0, "explication": "v.1057–1058 montrent leurs effets destructeurs sur l'ardeur spirituelle."},
                    {"q": "Comment le vers 1061 qualifie-t-il une vie passée dans l'oisiveté ?", "options": ["Une vie vaine et une grave catastrophe", "Une vie paisible", "Une marque de sagesse", "Une nécessité"], "answer": 0, "explication": "v.1061–1062 : la vie est très précieuse et doit être employée à l'utile."},
                    {"q": "Quel est le remède du désespoir selon le vers 1070 ?", "options": ["Méditer la Grandeur, la Magnanimité et la Miséricorde d'Allah", "Se plaindre à ses proches", "Cesser de prier", "Oublier l'Au-delà"], "answer": 0, "explication": "v.1070 : penser à la Miséricorde d'Allah relève le moral et console."},
                    {"q": "Comment soigner le défaut de ne voir que les fautes d'autrui (v.1071–1072) ?", "options": ["Accepter leurs excuses et voiler leurs défauts afin qu'Allah voile les tiens", "Les critiquer publiquement", "Rompre avec tous", "Compter leurs erreurs"], "answer": 0, "explication": "v.1072 : voiler les défauts des frères afin qu'Allah voile les nôtres."},
                    {"q": "Qui est seul véritablement intelligent selon le vers 1077 ?", "options": ["Celui qui vise la Demeure éternelle par des efforts nuit et jour", "Celui qui accumule le plus d'argent", "Celui qui dort toute la journée", "Celui qui critique sans agir"], "answer": 0, "explication": "v.1077 définit la vraie intelligence par l'œuvre pour l'Au-delà."},
                    {"q": "Pourquoi ne jamais s'enorgueillir d'un bienfait donné à autrui (v.1081–1082) ?", "options": ["Parce que c'est Allah qui dispense les faveurs et tu n'es qu'un intermédiaire", "Parce que le don est perdu", "Parce que personne ne le voit", "Parce que c'est interdit de donner"], "answer": 0, "explication": "v.1082 rappelle que le donateur n'est qu'un intermédiaire d'Allah."},
                ],
            },
            {
                "num": 26,
                "slug": "mauvais-caractere-impatience",
                "titre": "Ch.2 (10) : Mauvais Caractère (Colère) & Impatience",
                "versets": "v.1083 – v.1087",
                "duree": "3 min",
                "icone": "fa-fire-extinguisher",
                "resume": "Les deux derniers vices du Chapitre 2 : la colère et l'aigreur (traits de Satan guéris par la conscience de la Volonté d'Allah) et l'impatience (source de privation et de découragement, guérie par l'humilité devant le Tout-Puissant).",
                "passages": [
                    {"ref": "v.1083 – v.1085", "titre": "Origine et remède de la colère", "texte": "La colère, l'aigreur, l'humeur hargneuse, l'intolérance et la rage font partie des caractéristiques de Satan le maudit. Leur remède est de savoir que nulle action ne s'accomplit sans la Volonté d'Allah Très-Haut."},
                    {"ref": "v.1086 – v.1087", "titre": "Le défaut d'impatience et ses dangers", "texte": "Si tu es frappé du défaut d'impatience, remets-toi au Tout-Puissant avec humilité pour le repousser : car l'impatience fait tomber dans la privation, le découragement, le regret et la désobéissance."},
                ],
                "questions": [
                    {"q": "À qui le vers 1083 rattache-t-il la colère, l'aigreur, l'intolérance et la rage ?", "options": ["Aux caractéristiques de Satan le maudit", "Aux traits du courage", "À la noblesse", "À la piété"], "answer": 0, "explication": "v.1083 rattache ces travers aux caractéristiques de Satan."},
                    {"q": "Quel est le remède spirituel contre la colère selon le vers 1085 ?", "options": ["Savoir que rien ne s'accomplit réellement que par la Volonté d'Allah", "Se venger sur-le-champ", "Crier plus fort", "Garder rancune"], "answer": 0, "explication": "v.1085 : se rappeler la souveraine Volonté d'Allah éteint la rage."},
                    {"q": "Comment repousser le défaut d'impatience selon le vers 1086 ?", "options": ["En se remettant au Tout-Puissant avec humilité", "En s'énervant davantage", "En abandonnant ses efforts", "En blâmant son entourage"], "answer": 0, "explication": "v.1086 : se remettre au Tout-Puissant avec humilité."},
                    {"q": "Quelles quatre conséquences néfastes l'impatience entraîne-t-elle (v.1087) ?", "options": ["La privation, le découragement, le regret et la désobéissance", "La paix, la joie, l'honneur et la réussite", "Le sommeil et le calme", "La richesse et la gloire"], "answer": 0, "explication": "v.1087 énumère exactement ces quatre chutes."},
                    {"q": "Quelle gorgée est l'une des plus chères à Allah face à la colère (v.1312) ?", "options": ["La gorgée d'une colère réprimée avec courage pour l'agrément d'Allah", "Un discours violent", "Une vengeance rapide", "Un reproche public"], "answer": 0, "explication": "v.1312 loue la colère réprimée pour l'amour d'Allah."},
                    {"q": "Quel comportement remplace le mauvais caractère dès l'ouverture du Chapitre 3 (v.1089) ?", "options": ["La bonne conduite (al-adab), meilleure parure de l'homme", "L'indifférence", "La dureté", "L'isolement"], "answer": 0, "explication": "v.1089 ouvre le Chapitre 3 par la bonne conduite."},
                ],
            },
        ],
    },
    {
        "id": 4,
        "code": "porte-4",
        "titre": "Porte IV · Chapitre 3 — Qualités, Adab & Secrets",
        "sous_titre": "6 grands chapitres · Adab extérieur, Adab intérieur & Prière de nuit, Shukr, Sabr, Invocation, Saints & Sourates (v.1088–1562)",
        "icone": "fa-crown",
        "couleur": "from-amber-600 to-emerald-800",
        "accent": "#FDE047",
        "chapitres": [
            {
                "num": 27,
                "slug": "adab-conduite-exterieure",
                "titre": "Ch.3 (1) : La Conduite Extérieure (Adab social)",
                "versets": "v.1088 – v.1112",
                "duree": "4 min",
                "icone": "fa-handshake",
                "resume": "La bonne conduite constitue près des deux tiers de la dévotion : règles quotidiennes (Basmala, salutation, poignée de main, visite aux malades), pardon à l'offenseur, respect des parents, des aînés, pitié envers les enfants et équité envers son égal.",
                "passages": [
                    {"ref": "v.1089 – v.1094", "titre": "Meilleure parure & 2/3 de la dévotion", "texte": "La meilleure parure de l'homme est la bonne conduite partout où il passe : les savants rapportent qu'elle représente près des deux tiers de la dévotion. Elle comporte un volet intérieur envers Allah et un volet extérieur envers les humains."},
                    {"ref": "v.1095 – v.1101", "titre": "Règles quotidiennes de la Sunna", "texte": "Privilégier la droite, prononcer la Basmala, soigner sa tenue à table, utiliser le siwâk, serrer la main avec les deux mains, bien saluer, visiter le malade, dire Al-Hamdulillâh en éternuant et demander permission avant d'entrer."},
                    {"ref": "v.1102 – v.1111", "titre": "Pardon, parents, aînés, enfants & égaux", "texte": "Pardonne à ton offenseur, donne à qui te prive, renoue avec qui t'abandonne. Honore tes parents, tes aînés et ton guide spirituel ; aie pitié du plus petit, et traite ton égal comme tu aimerais être traité."},
                ],
                "questions": [
                    {"q": "Quelle proportion de la dévotion représente la bonne conduite selon les savants (v.1092) ?", "options": ["Près des deux tiers (2/3)", "Un dixième", "Un quart", "Un cinquième"], "answer": 0, "explication": "v.1092 : elle constitue près des deux tiers de la dévotion."},
                    {"q": "Quels trois actes nobles sont prescrits aux vers 1102–1103 ?", "options": ["Pardonner à l'offenseur, donner à qui te prive et renouer avec qui t'a abandonné", "Rendre coup pour coup", "Couper tout lien familial", "Répondre par le mépris"], "answer": 0, "explication": "v.1102–1103 enseignent ce sommet de noblesse morale."},
                    {"q": "Comment traiter le plus âgé, le plus petit et son égal (v.1106–1111) ?", "options": ["Honorer le plus âgé, avoir pitié du plus petit, traiter son égal comme soi-même", "Traiter chacun avec froideur", "N'honorer que les riches", "Ignorer les jeunes"], "answer": 0, "explication": "v.1106–1111 résument cette règle d'or de l'adab."},
                    {"q": "Que recommande le vers 1101 avant d'entrer dans la chambre d'autrui ?", "options": ["Demander la permission", "Entrer sans bruit", "Attendre la nuit", "Appeler de loin seulement"], "answer": 0, "explication": "v.1101 cite la demande de permission avant de pénétrer chez autrui."},
                    {"q": "Que dit le vers 1104 au sujet des liens de parenté, notamment envers un père ?", "options": ["Ces devoirs de bonté et de maintien du lien deviennent obligatoires, fût-il même idolâtre", "Ils cessent à l'âge adulte", "Ils sont facultatifs", "Ils dépendent de sa richesse"], "answer": 0, "explication": "v.1104 insiste sur l'obligation envers les liens de parenté."},
                    {"q": "Quel devoir envers les enfants le vers 1105 rappelle-t-il ?", "options": ["Veiller à leur éducation afin qu'ils deviennent sages et dans la bonne voie", "Les laisser sans repères", "Ne s'occuper que de leurs jeux", "Attendre qu'ils soient adultes"], "answer": 0, "explication": "v.1105 insiste sur l'éducation des enfants dans la bonne voie."},
                ],
            },
            {
                "num": 28,
                "slug": "adab-interieur-priere-nuit",
                "titre": "Ch.3 (2) : Conduite Intérieure & Prière de Nuit",
                "versets": "v.1113 – v.1189",
                "duree": "5 min",
                "icone": "fa-star",
                "resume": "L'adab intérieur vis-à-vis d'Allah (ne jamais critiquer Son décret ni chercher la facilité par tiédeur), puis les merveilles de la prière nocturne (2 rak'as > ce bas-monde) et les causes qui la facilitent ou l'empêchent.",
                "passages": [
                    {"ref": "v.1113 – v.1122", "titre": "Adab intérieur devant Allah", "texte": "Ne critique jamais le décret d'Allah ni les saints guides, ne te tourne pas vers les créatures par crainte ou désir. L'aspirant qui prend l'habitude de choisir les solutions de facilité par tiédeur ne réussira jamais."},
                    {"ref": "v.1132 – v.1149", "titre": "Merveilles de la prière de nuit", "texte": "Ne passe pas toute la nuit gisant tel un cadavre : deux rak'as dans la seconde moitié de la nuit valent plus que ce bas-monde et tout ce qu'il contient. Prolonger la prière nocturne raccourcit la durée du Jour du Jugement."},
                    {"ref": "v.1150 – v.1174", "titre": "Ce qui facilite ou bloque le lever nocturne", "texte": "La sobriété alimentaire, manger exclusivement licite, éviter les péchés le jour et diminuer les soucis mondains facilitent la prière de nuit. Sufyân at-Thawrî en fut privé 5 mois pour un seul mauvais soupçon envers un croyant !"},
                    {"ref": "v.1175 – v.1186", "titre": "Si le sommeil est trop lourd", "texte": "Si le sommeil empêche de se lever au cœur de la nuit, prie les surérogatoires après Maghrib et Ishâ et lève-toi avant l'aube. « Quiconque prétend aimer son Seigneur et dort toutes les nuits est un menteur » (révélation à David)."},
                ],
                "questions": [
                    {"q": "Qu'advient-il de l'aspirant qui choisit habituellement les facilités par tiédeur (v.1122) ?", "options": ["Il ne réussira jamais", "Il progresse plus vite", "Il obtient le même mérite", "Il devient guide"], "answer": 0, "explication": "v.1122 avertit que la tiédeur systématique mène à l'échec spirituel."},
                    {"q": "Que valent deux rak'as accomplies dans la seconde moitié de la nuit (v.1138–1139) ?", "options": ["Plus que tout ce bas-monde et ce qu'il contient", "Une heure de repos", "Une aumône modique", "Un repas"], "answer": 0, "explication": "v.1138–1139 : plus de valeur que tout ce bas-monde et ce qu'il contient."},
                    {"q": "Qu'ont répondu Al-Junayd et Ibn al-Qâsim interrogés en songe dans leur tombe (v.1142–1144) ?", "options": ["Ce qui leur restait de plus précieux était les rak'as priées à l'aube", "Leurs voyages", "Leurs grands discours", "Leurs richesses"], "answer": 0, "explication": "v.1144 cite les rak'as priées à l'aube."},
                    {"q": "Pourquoi Sufyân at-Thawrî fut-il privé de la prière de nuit pendant 5 mois (v.1154–1157) ?", "options": ["Pour avoir soupçonné en lui-même un croyant qui pleurait d'ostentation", "Pour avoir dormi tard", "À cause d'un voyage", "À cause du froid"], "answer": 0, "explication": "v.1155–1157 illustrent l'impact d'un seul mauvais soupçon."},
                    {"q": "Quel effet la nourriture illicite a-t-elle sur le cœur et la prière nocturne (v.1165–1167) ?", "options": ["Elle empêche l'homme de se lever la nuit pour prier", "Elle donne de l'énergie", "Aucun effet", "Elle améliore le recueillement"], "answer": 0, "explication": "v.1166–1167 : le licite purifie le cœur ; l'illicite bloque le lever nocturne."},
                    {"q": "Que recommande le livre si un lourd sommeil empêche de se lever au milieu de la nuit (v.1175–1177) ?", "options": ["Faire ses surérogatoires après Maghrib et Ishâ et s'efforcer de se lever avant le matin", "Abandonner toute prière surérogatoire", "Dormir le jour entier", "Ne plus faire le Witr"], "answer": 0, "explication": "v.1176–1177 donnent cette solution pratique et progressive."},
                ],
            },
            {
                "num": 29,
                "slug": "reconnaissance-shukr",
                "titre": "Ch.3 (3) : La Reconnaissance envers Allah (Ash-Shukr)",
                "versets": "v.1190 – v.1227 & v.1362 – v.1384",
                "duree": "4 min",
                "icone": "fa-heart",
                "resume": "Les droits d'Allah dans chaque moment (dévotion, bienfait, péché, adversité), l'union de Haqîqa et Sharî'a dans le remerciement, et les trois degrés hiérarchiques du Shukr.",
                "passages": [
                    {"ref": "v.1190 – v.1203", "titre": "Remercier Allah ET l'intermédiaire", "texte": "Témoigne que tout bienfait vient d'Allah Seul (Haqîqa) tout en remerciant celui qui a servi d'intermédiaire (Sharî'a). Sois heureux du Bienfaiteur autant que du bienfait, et utilise Ses dons pour Lui obéir."},
                    {"ref": "v.1206 – v.1225", "titre": "Gratitude jusque dans l'épreuve", "texte": "Dans l'adversité, le droit d'Allah est la résignation et la satisfaction : remercie-Le que l'épreuve n'ait pas été plus grande, qu'elle n'ait pas touché ta foi et qu'elle te purifie ici-bas plutôt que dans l'Au-delà."},
                    {"ref": "v.1362 – v.1371", "titre": "Les 3 degrés du Shukr & l'espoir vrai", "texte": "Le degré supérieur du Shukr est d'adorer Allah par stricte vénération ; le moyen par obéissance ; l'inférieur pour le Paradis ou le salut de l'Enfer. L'espoir vrai agit avec les moyens ; désirer sans agir (tamma') est pure rêverie."},
                ],
                "questions": [
                    {"q": "Comment réunit-on Haqîqa et Sharî'a lorsqu'on reçoit un bienfait (v.1195–1198) ?", "options": ["Reconnaître Allah comme unique source et remercier l'intermédiaire humain", "Ne remercier personne", "Remercier seulement l'humain", "Refuser le bienfait"], "answer": 0, "explication": "v.1197–1198 : Allah (Haqîqa) et l'intermédiaire (Sharî'a)."},
                    {"q": "Que faut-il faire des bienfaits qu'Allah accorde (v.1203 & v.1363) ?", "options": ["S'en aider pour Lui obéir et agir dans ce qu'Il agrée", "Les utiliser dans la désobéissance", "S'en vanter", "Les cacher par avarice"], "answer": 0, "explication": "v.1203 & v.1363 : employer Ses dons dans Son obéissance."},
                    {"q": "Pourquoi remercier Allah même dans une épreuve (v.1223–1225) ?", "options": ["Elle pouvait être plus grande, pouvait toucher la foi, et purifie ici-bas", "Parce que l'épreuve n'existe pas", "Pour se faire plaindre", "Parce qu'Allah ignore nos peines"], "answer": 0, "explication": "v.1223–1225 détaillent ces trois motifs de gratitude dans l'épreuve."},
                    {"q": "Quel est le degré supérieur du Shukr selon le vers 1367 ?", "options": ["Adorer Allah ayant pour fin Sa stricte vénération", "Adorer uniquement par peur de l'Enfer", "Adorer pour être vu", "Adorer seulement dans l'aisance"], "answer": 0, "explication": "v.1367–1368 distinguent les trois degrés (vénération, obéissance, Paradis/Enfer)."},
                    {"q": "Comment le livre appelle-t-il celui qui espère réussir sans utiliser les moyens requis (v.1370–1371) ?", "options": ["« Tamma' » (pure rêverie trompée par la paresse)", "Un grand savant", "Un homme confiant", "Un modèle de gratitude"], "answer": 0, "explication": "v.1370–1371 : l'espoir sans action est appelé tamma' (rêverie)."},
                    {"q": "Que témoigne Allah envers Ses créatures selon le vers 1215 ?", "options": ["Une pitié qu'elles n'ont ni pour elles-mêmes ni pour leurs propres enfants", "De la dureté", "De l'indifférence", "De l'oubli"], "answer": 0, "explication": "v.1215 : Allah ne cherche que notre bien absolu."},
                ],
            },
            {
                "num": 30,
                "slug": "longanimite-sabr",
                "titre": "Ch.3 (4) : La Longanimité ou Patience (As-Sabr)",
                "versets": "v.1228 – v.1317",
                "duree": "5 min",
                "icone": "fa-mountain-sun",
                "resume": "Les 3 degrés hiérarchiques de la patience (300, 600 et 900 degrés), la patience au sein de la famille, le secret de la douleur et de l'aumône, la valeur purificatrice des épreuves et les « deux gouttes et deux gorgées ».",
                "passages": [
                    {"ref": "v.1234 – v.1244", "titre": "Les 3 degrés du Sabr (300 · 600 · 900)", "texte": "La patience dans l'adoration et l'adversité ('alâ) vaut 300 degrés ; résister aux tentations et aux interdits ('an) vaut 600 degrés ; demeurer ferme et humble dans la paix et la félicité (fî) vaut 900 degrés : le plus brave est celui qui patiente dans l'aisance !"},
                    {"ref": "v.1253 – v.1270", "titre": "Famille & viatiques cachés", "texte": "Supporter les charges de la famille avec bonté et confiance en Allah est l'un des chemins qui conduisent à Lui. Cacher sa douleur, son aumône, son adversité et sa pauvreté constitue l'un des plus précieux viatiques."},
                    {"ref": "v.1283 – v.1302", "titre": "Épreuves purificatrices", "texte": "Quand Allah aime un serviteur, Il l'éprouve pour effacer ses péchés (même par une simple piqûre d'épine). « Quand un bonheur t'arrive, remercie Allah ; quand un malheur te frappe, patiente. »"},
                    {"ref": "v.1309 – v.1313", "titre": "Deux gouttes et deux gorgées", "texte": "Les plus précieux viatiques auprès d'Allah sont deux gouttes (une larme nocturne par crainte d'Allah ; une goutte de sang dans Sa voie) et deux gorgées (une colère réprimée pour Allah ; une épreuve supportée avec longanimité)."},
                ],
                "questions": [
                    {"q": "Quels sont les trois degrés d'élévation de la patience (v.1236–1241) ?", "options": ["300 ('alâ), 600 ('an) et 900 (fî)", "10, 20 et 30", "100, 200 et 300", "50, 100 et 200"], "answer": 0, "explication": "v.1237, 1239 et 1241 : 300, 600 et 900 degrés."},
                    {"q": "Qui est « l'homme le plus brave » selon le vers 1244 ?", "options": ["Celui qui patiente dans la paix et la félicité sans se laisser griser", "Celui qui crie le plus fort", "Celui qui fuit sa famille", "Celui qui exhibe ses charismes"], "answer": 0, "explication": "v.1244–1245 : rester ferme et lucide dans la prospérité est le plus haut courage."},
                    {"q": "Comment le vers 1254 décrit-il la famille ?", "options": ["L'un des chemins qui conduisent vers Allah Très-Haut", "Un obstacle à rejeter", "Une chose secondaire", "Une perte de temps"], "answer": 0, "explication": "v.1254 : supporter la famille avec bonté mène vers Allah."},
                    {"q": "Quelles quatre choses cacher constitue un viatique précieux (v.1268–1269) ?", "options": ["La douleur, l'aumône, l'adversité et la pauvreté", "Son nom, son âge, sa ville et son métier", "Ses prières obligatoires", "Ses livres"], "answer": 0, "explication": "v.1268 : douleur, aumône, adversité et pauvreté."},
                    {"q": "Quelle règle d'or résume le vers 1302 ?", "options": ["Dans le bonheur remercie Allah, dans le malheur patiente", "Ne dis rien à personne", "Ne travaille que le matin", "Fuis toute difficulté"], "answer": 0, "explication": "v.1302 : gratitude dans le bonheur, patience dans l'épreuve."},
                    {"q": "Quelles sont les deux gorgées les plus chères à Allah (v.1312–1313) ?", "options": ["La colère réprimée pour Allah et la catastrophe endurée avec patience", "L'eau fraîche et le lait", "Le miel et le thé", "Un remède amer"], "answer": 0, "explication": "v.1312–1313 citent ces deux gorgées spirituelles."},
                ],
            },
            {
                "num": 31,
                "slug": "secrets-invocation",
                "titre": "Ch.3 (5) : Secrets, Moments & Lieux de l'Invocation",
                "versets": "v.1318 – v.1361",
                "duree": "4 min",
                "icone": "fa-hands-praying",
                "resume": "Toutes les conditions d'un Du'â exaucé (subsistance licite, louange, prière sur le Prophète, humilité, persévérance sans impatience), les moments bénis, les lieux sacrés et les catégories de personnes exaucées.",
                "passages": [
                    {"ref": "v.1318 – v.1324", "titre": "Conditions de perfection du Du'â", "texte": "Consomme et revêts le licite, fais tes ablutions, prie quelques rak'as face à la Kaaba, loue Allah et prie sur le Prophète (PSL) au début et à la fin, mains levées et ouvertes avec humilité."},
                    {"ref": "v.1328 – v.1336", "titre": "Persévérance sans jamais désespérer", "texte": "Commence par toi-même puis prie pour la Communauté. Sois concentré et résolu, ne dis jamais « ma prière n'a pas été exaucée », et passe tes deux mains sur ton visage à la fin."},
                    {"ref": "v.1337 – v.1349", "titre": "Moments où Allah exauce", "texte": "Ramadan, Arafat, Laylat al-Qadr, le vendredi (l'heure bénie), la fin de la nuit (sahar), entre Adhân et Iqâma, aussitôt après les prières obligatoires, après le Coran, sous la pluie et dans les séances de dhikr."},
                    {"ref": "v.1350 – v.1360", "titre": "Lieux sacrés & personnes exaucées", "texte": "Kaaba, Multazam, Zamzam, Safâ-Marwa, Arafat, tombeaux des Prophètes et des Saints. Personnes exaucées : nécessiteux en détresse, victime d'injustice, voyageur, jeûneur, enfant pieux pour ses parents, repenti et qui prie pour son frère en son absence."},
                ],
                "questions": [
                    {"q": "Quelle est la première condition citée au vers 1318 pour l'exaucement du Du'â ?", "options": ["Éviter l'illicite en nourriture, vêtement et parole", "Parler très fort", "Être en grande foule", "N'invoquer que la nuit"], "answer": 0, "explication": "v.1318 place la pureté du licite en toute première position."},
                    {"q": "Par quoi encadre-t-on le début et la fin de l'invocation (v.1322) ?", "options": ["La louange d'Allah et la prière sur le Prophète (PSL)", "Un silence long", "Un serment", "Un récit historique"], "answer": 0, "explication": "v.1322 : louange et prière sur le Prophète au début et à la fin."},
                    {"q": "Quelle parole faut-il absolument éviter (v.1333) ?", "options": ["« Ma prière n'est pas exaucée » (impatience et désespoir)", "Âmîn", "Subhânallâh", "Al-Hamdulillâh"], "answer": 0, "explication": "v.1333 met en garde contre l'impatience et le désespoir."},
                    {"q": "Quel geste conclut l'invocation selon le vers 1335 ?", "options": ["Passer les deux mains sur le visage", "Se lever brusquement", "Frapper des mains", "Regarder le sol"], "answer": 0, "explication": "v.1335 recommande de passer les deux mains sur le visage."},
                    {"q": "Que dit le vers 1356 sur la victime d'une injustice ?", "options": ["Sa prière est exaucée, fût-elle même un idolâtre", "Elle n'est exaucée que le vendredi", "Elle doit attendre un an", "Seul un érudit est exaucé"], "answer": 0, "explication": "v.1356 souligne la force de la prière de toute victime d'injustice."},
                    {"q": "Que dit le vers 1360 sur le croyant qui prie en bien pour son frère en son absence ?", "options": ["Il fait partie de ceux dont la prière est exaucée", "C'est inutile", "Il doit le prévenir", "Cela ne compte pas"], "answer": 0, "explication": "v.1360 cite cette prière fraternelle sincère parmi les prières exaucées."},
                ],
            },
            {
                "num": 32,
                "slug": "saints-vertus-sourates",
                "titre": "Ch.3 (6) : Respect des Saints, Sourates & Épilogue",
                "versets": "v.1385 – v.1562",
                "duree": "5 min",
                "icone": "fa-sun",
                "resume": "Ne jamais dénigrer les Saints cachés parmi les humains, discerner les faux guides cupides, demeurer dans le juste milieu de la Sunna, puis pratiquer les vertus des sourates (Al-Mulk, Âyat al-Kursî, Al-Ikhlâs, Al-Kahf, Yâ-Sîn), Sayyidul-Istighfâr et l'épilogue béni.",
                "passages": [
                    {"ref": "v.1385 – v.1412", "titre": "Respect des Saints cachés", "texte": "Évite de critiquer les Saints d'Allah : avoir bonne conviction en eux est une grâce, les combattre mène au malheur. Ils vivent dissimulés parmi les humains, mangeant et subissant les épreuves comme tout homme."},
                    {"ref": "v.1432 – v.1474", "titre": "Discernement & juste milieu de la Sunna", "texte": "Fuis les faux cheikhs cupides et jaloux quand on loue un autre maître. Reste dans le juste milieu de la Sunna : « tout point lumineux n'est pas la lune ». Et ne méprise jamais un serviteur pour son humble habit."},
                    {"ref": "v.1480 – v.1519", "titre": "Vertus des Sourates du Coran", "texte": "Al-Mulk chaque nuit protège dans la tombe ; Âyat al-Kursî après chaque prière ouvre le Paradis ; Al-Ikhlâs équivaut au tiers du Coran ; Al-Kahf le vendredi illumine jusqu'au vendredi suivant ; Yâ-Sîn procure le pardon."},
                    {"ref": "v.1526 – v.1562", "titre": "Sayyidul-Istighfâr & Épilogue de Masaalikul Jinaan", "texte": "Récite matin et soir Sayyidul-Istighfâr. Fuis la paresse, la médisance, l'ostentation et la jalousie. Cheikh Ahmadou Bamba clôt son chef-d'œuvre en priant qu'Allah en fasse un véritable itinéraire vers le Paradis."},
                ],
                "questions": [
                    {"q": "Quelle réponse sage d'Abd al-Wadûd est citée face aux paroles profondes des Saints (v.1394–1395) ?", "options": ["« Je ne comprends pas les propos des Saints : moi je suis ce que je suis, et eux ce qu'ils sont »", "Il faut les condamner aussitôt", "Elles sont fausses", "Il faut les corriger"], "answer": 0, "explication": "v.1395 enseigne l'humilité face aux propos profonds des Saints."},
                    {"q": "À quel signe reconnaît-on un faux guide cupide (v.1438–1444) ?", "options": ["Il s'irrite quand on loue un autre cheikh et ne vise que gloire et profit matériel", "Il souhaite le salut du disciple par n'importe quel vrai maître", "Il enseigne la Sunna", "Il vit humblement"], "answer": 0, "explication": "v.1438–1444 : le vrai guide ne cherche que le salut du disciple."},
                    {"q": "Que signifie « Al-Yaqîn » dans « Adore ton Seigneur jusqu'à ce que te vienne Al-Yaqîn » (v.1462) ?", "options": ["La mort (adorer Allah jusqu'à la mort)", "L'âge de 40 ans", "La richesse", "La retraite"], "answer": 0, "explication": "v.1462 corrige les égarés : nul n'est jamais dispensé d'adorer Allah avant la mort."},
                    {"q": "Quelle sourate récitée chaque nuit préserve des frayeurs de la tombe (v.1480) ?", "options": ["Al-Mulk (S.67)", "Al-Fîl (S.105)", "Al-Kawthar (S.108)", "Al-Masad (S.111)"], "answer": 0, "explication": "v.1480 cite la sourate Al-Mulk chaque nuit."},
                    {"q": "À quelle fraction du Coran équivaut la sourate Al-Ikhlâs (v.1504) ?", "options": ["Un tiers (1/3)", "Un quart", "Un dixième", "La moitié"], "answer": 0, "explication": "v.1504 : Al-Ikhlâs équivaut au tiers du Coran."},
                    {"q": "Quel bienfait procure la lecture de la sourate Al-Kahf le vendredi (v.1516–1518) ?", "options": ["Elle illumine le lecteur jusqu'au vendredi suivant", "Elle dispense du jeûne", "Elle dure trois jours", "Elle se lit seulement la nuit"], "answer": 0, "explication": "v.1518 : elle illumine jusqu'au vendredi suivant."},
                ],
            },
        ],
    },
]


def get_all_chapitres():
    """Retourne la liste ordonnée des 32 chapitres & sous-chapitres avec métadonnées de leur Porte."""
    out = []
    for porte in MASAALIK_PORTES:
        for ch in porte["chapitres"]:
            item = dict(ch)
            item["porte_id"] = porte["id"]
            item["porte_titre"] = porte["titre"]
            item["porte_couleur"] = porte["couleur"]
            item["porte_accent"] = porte["accent"]
            out.append(item)
    return out


def get_chapitre_by_slug(slug):
    all_ch = get_all_chapitres()
    for idx, ch in enumerate(all_ch):
        if ch["slug"] == slug:
            next_ch = all_ch[idx + 1] if idx + 1 < len(all_ch) else None
            prev_ch = all_ch[idx - 1] if idx > 0 else None
            return ch, prev_ch, next_ch
    return None, None, None


import json
import os
import re

_MASAALIK_VERSETS_CACHE = None


def load_masaalik_versets():
    """Charge une seule fois les 1 195 versets intégraux extraits du PDF Masaalik-ul Jinaan."""
    global _MASAALIK_VERSETS_CACHE
    if _MASAALIK_VERSETS_CACHE is None:
        p = os.path.join(os.path.dirname(__file__), "masaalik_versets.json")
        try:
            with open(p, "r", encoding="utf-8") as f:
                raw = json.load(f)
            _MASAALIK_VERSETS_CACHE = {int(k): v for k, v in raw.items()}
        except Exception:
            _MASAALIK_VERSETS_CACHE = {}
    return _MASAALIK_VERSETS_CACHE


def _parse_verse_ranges(versets_str):
    """Parse 'v.1190 – v.1227 & v.1362 – v.1384' en liste de tuples (start, end)."""
    ranges = []
    for part in re.split(r"[&,;]", versets_str or ""):
        nums = [int(x) for x in re.findall(r"\d+", part)]
        if len(nums) >= 2:
            ranges.append((nums[0], nums[1]))
        elif len(nums) == 1:
            ranges.append((nums[0], nums[0]))
    return ranges


def get_chapitre_verbatim_versets(chapitre):
    """Retourne tous les versets authentiques numérotés [(num, texte), ...] couverts par ce chapitre."""
    vmap = load_masaalik_versets()
    out = []
    seen = set()
    for lo, hi in _parse_verse_ranges(chapitre.get("versets", "")):
        for n in range(lo, hi + 1):
            if n in vmap and n not in seen:
                seen.add(n)
                out.append({"num": n, "texte": vmap[n]})
    return out


def build_masaalik_deck(chapitre):
    """
    Parcours fluide étape par étape avec les VRAIS VERSETS AUTHENTIQUES du livre :
      1. Vue d'ensemble du chapitre (plan & nombre de versets authentiques)
      2. Cartes de lecture contenant les VRAIS VERSETS numérotés (3 à 4 versets courts par écran mobile)
         entrecoupés de questions intermédiaires régulières
      3. Petit résumé objectif (« L'essentiel de ce que dit le livre ») AVANT les questions finales
      4. Questions de validation avec explications fidèles au texte
    """
    deck = []
    passages = chapitre.get("passages", [])
    questions = chapitre.get("questions", [])
    verbatim = get_chapitre_verbatim_versets(chapitre)

    # Construire les cartes de lecture : vrais versets numérotés si présents dans le PDF,
    # sinon passages fidèles (pour v.602-968 absents du PDF source)
    reading_cards = []
    if verbatim:
        # 1) Regrouper par blocs de 3 ou 4 versets pour tenir confortablement sur un petit écran mobile
        #    Si le chapitre a <= 36 versets : 100% de TOUS les versets sont affichés étape par étape.
        #    Si le chapitre est très long (> 36 versets) : on affiche les versets exacts correspondant
        #    à chaque repère du chapitre (4 versets autour de chaque passage) + accès intégral en 1 clic.
        if len(verbatim) <= 36:
            chunk_size = 3 if len(verbatim) <= 15 else 4
            for i in range(0, len(verbatim), chunk_size):
                chunk = verbatim[i:i + chunk_size]
                ref = f"v.{chunk[0]['num']} – v.{chunk[-1]['num']}" if len(chunk) > 1 else f"v.{chunk[0]['num']}"
                # Associer un titre thématique si un passage couvre ce verset
                card_title = chapitre["titre"]
                for p in passages:
                    p_ranges = _parse_verse_ranges(p.get("ref", ""))
                    if p_ranges and any(lo <= chunk[0]["num"] <= hi or lo <= chunk[-1]["num"] <= hi for lo, hi in p_ranges):
                        card_title = p["titre"]
                        break
                reading_cards.append({
                    "ref": ref,
                    "titre": card_title,
                    "versets": chunk,
                    "texte": "",
                })
        else:
            # Chapitre long (>36 versets) : extraire pour chaque passage thématique les vrais versets du PDF
            # (4 versets authentiques par carte, sans doublon) + couvrir début, milieu et fin
            vmap = {v["num"]: v for v in verbatim}
            used_nums = set()
            for p in passages:
                p_ranges = _parse_verse_ranges(p.get("ref", ""))
                chunk = []
                for lo, hi in p_ranges:
                    for n in range(lo, hi + 1):
                        if n in vmap and n not in used_nums and len(chunk) < 4:
                            chunk.append(vmap[n])
                            used_nums.add(n)
                if chunk:
                    ref = f"v.{chunk[0]['num']} – v.{chunk[-1]['num']}" if len(chunk) > 1 else f"v.{chunk[0]['num']}"
                    reading_cards.append({
                        "ref": ref,
                        "titre": p["titre"],
                        "versets": chunk,
                        "texte": "",
                    })
            # Ajouter 2 cartes complémentaires si le chapitre a encore beaucoup de versets non couverts
            remaining = [v for v in verbatim if v["num"] not in used_nums]
            if len(remaining) >= 4 and len(reading_cards) < 8:
                mid_idx = len(remaining) // 2
                for start_i in (0, max(4, mid_idx)):
                    extra = remaining[start_i:start_i + 4]
                    if extra and len(reading_cards) < 8:
                        ref = f"v.{extra[0]['num']} – v.{extra[-1]['num']}" if len(extra) > 1 else f"v.{extra[0]['num']}"
                        reading_cards.append({
                            "ref": ref,
                            "titre": f"Suite des versets ({ref})",
                            "versets": extra,
                            "texte": "",
                        })
            reading_cards.sort(key=lambda c: c["versets"][0]["num"])
    else:
        for p in passages:
            reading_cards.append({
                "ref": p["ref"],
                "titre": p["titre"],
                "versets": [],
                "texte": p["texte"],
            })

    total_read = len(reading_cards)

    # 1. Carte d'ouverture avec plan clair de la leçon
    deck.append({
        "type": "intro",
        "tag": f"Leçon {chapitre['num']} · {chapitre['versets']}",
        "titre": chapitre["titre"],
        "texte": (
            f"Lis les versets authentiques de Cheikh Ahmadou Bamba étape par étape ({len(verbatim)} versets dans ce chapitre), "
            f"puis valide ta compréhension avec {len(questions)} questions intermédiaires."
            if verbatim else chapitre["resume"]
        ),
        "etapes_titres": [f"{c['ref']} · {c['titre']}" for c in reading_cards[:6]],
        "meta": f"{total_read} étapes de versets · 1 petit résumé · {len(questions)} questions",
        "verbatim_total": len(verbatim),
    })

    # 2. Entrelacer les cartes de versets et les questions intermédiaires de façon naturelle
    mid_q_count = max(1, len(questions) // 2) if len(questions) >= 3 else (1 if questions else 0)
    q_cursor = 0
    interval = max(1, total_read // (mid_q_count + 1)) if mid_q_count else total_read + 1

    for idx_r, rc in enumerate(reading_cards, 1):
        deck.append({
            "type": "passage",
            "tag": f"Versets {idx_r}/{total_read} · {rc['ref']}",
            "titre": rc["titre"],
            "texte": rc["texte"],
            "versets": rc["versets"],
        })
        if q_cursor < mid_q_count and idx_r < total_read and (idx_r % interval == 0):
            q = questions[q_cursor]
            q_cursor += 1
            deck.append({
                "type": "question",
                "q_num": q_cursor,
                "q_total": len(questions),
                "question": q["q"],
                "options": q["options"],
                "answer": q["answer"],
                "explication": q["explication"],
            })

    # 3. Petit résumé objectif AVANT les questions finales
    deck.append({
        "type": "resume",
        "tag": f"Petit Résumé · {chapitre['versets']}",
        "titre": "L'essentiel à retenir avant les questions finales",
        "texte": chapitre["resume"],
        "points": [f"{p['ref']} — {p['titre']}" for p in passages],
    })

    # 4. Questions finales de validation
    while q_cursor < len(questions):
        q = questions[q_cursor]
        q_cursor += 1
        deck.append({
            "type": "question",
            "q_num": q_cursor,
            "q_total": len(questions),
            "question": q["q"],
            "options": q["options"],
            "answer": q["answer"],
            "explication": q["explication"],
        })

    return deck


# Alias rétrocompatible
build_duolingo_deck = build_masaalik_deck
