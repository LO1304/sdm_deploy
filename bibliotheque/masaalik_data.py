"""
Masaalik-ul Jinaan (Les Itinéraires du Paradis) — Cheikh Ahmadou Bamba (RTA)
Curriculum interactif "Mode Duolingo" fidèle au texte du livre (v.1 à v.1562).
Organisation : 4 Grandes Portes, 16 Chapitres, cartes courtes calibrées petit écran,
résumés objectifs fidèles à l'ouvrage et 8 questions intermédiaires par chapitre (128 questions).
"""

MASAALIK_PORTES = [
    {
        "id": 1,
        "code": "porte-1",
        "titre": "Porte I · Préambule & Fondements Spirituels",
        "sous_titre": "Introduction, Fiqh & Soufisme, Science utile, Sagesse profonde, Oraison et Jeûne (v.1–266)",
        "icone": "fa-compass",
        "couleur": "from-emerald-600 to-teal-700",
        "accent": "#34D399",
        "chapitres": [
            {
                "num": 1,
                "slug": "introduction-egalite",
                "titre": "Introduction & Égalité devant Allah",
                "versets": "v.1 – v.79",
                "duree": "4 min",
                "icone": "fa-star-and-crescent",
                "resume": "Cheikh Ahmadou Bamba présente son ouvrage versifié d'après la prose d'Al-Yadâlî (Hâtimat at-Tasawwuf), proclame l'égalité humaine devant Allah fondée uniquement sur la piété, et prie pour quiconque lit ou médite ce livre.",
                "passages": [
                    {"ref": "v.3 – v.4", "titre": "Ce qu'Allah regarde", "texte": "Allah exige de nous la sincérité des actions et l'observance de la bonne conduite (al-adab). Il considère en nous le cœur et les qualités spirituelles, et non ce qui n'est qu'apparent."},
                    {"ref": "v.8 – v.10", "titre": "La lutte intérieure", "texte": "Quiconque lutte contre Satan, contre son âme charnelle et contre sa passion profane obtient le Paradis ; celui qui purifie son cœur de tout vice acquiert la lumière et l'agrément d'Allah."},
                    {"ref": "v.25 – v.38", "titre": "Origine et sources du livre", "texte": "Cheikh Ahmadou Bamba met en vers la prose d'Al-Yadâlî (Hâtimat at-Tasawwuf) et l'enrichit par Al-Dhahab al-Ibrîz, l'Ihyâ d'Al-Ghazâlî et Junnat al-Murîd afin d'offrir un remède aux cœurs malades."},
                    {"ref": "v.47 – v.49", "titre": "Égalité et dignité devant Allah", "texte": "« Ne te laisse pas abuser par ma condition d'homme noir pour ne pas en profiter. L'homme le plus estimé auprès d'Allah est celui qui Le craint le plus, sans discrimination. La couleur de la peau ne saurait être cause de l'idiotie d'un homme. »"},
                    {"ref": "v.51 – v.54", "titre": "La grâce d'Allah n'appartient pas qu'aux anciens", "texte": "Ne réserve pas les dons d'Allah aux seuls anciens : une fine pluie peut en devancer une abondante, mais l'avantage revient à l'abondante. Le Prophète (PSL) a comparé sa communauté à la pluie dont on ignore si le début ou la fin est meilleur."},
                    {"ref": "v.70 – v.77", "titre": "Prière pour le lecteur et plan du livre", "texte": "Cheikh Ahmadou Bamba implore le salut pour quiconque lit, médite, possède, copie ou emprunte ce livre. L'ouvrage s'organise en un préambule suivi de trois chapitres : les créatures, les vices graves, et les qualités (adab)."},
                ],
                "questions": [
                    {"q": "Selon les vers 3–4, que considère Allah chez Ses serviteurs ?", "options": ["Uniquement l'apparence extérieure", "Le cœur et les qualités spirituelles", "La richesse accumulée", "La renommée sociale"], "answer": 1, "explication": "v.4 : Allah « considère en nous le cœur et les qualités spirituelles et non ce qui n'est qu'apparent »."},
                    {"q": "Contre quels trois adversaires faut-il lutter pour obtenir le Paradis (v.8) ?", "options": ["La faim, le froid et le sommeil", "Satan, l'âme charnelle et la passion profane", "Les rois, les savants et les juges", "Les voyages, le commerce et la fatigue"], "answer": 1, "explication": "v.8 cite explicitement la lutte contre Satan, l'âme charnelle et la passion profane."},
                    {"q": "Quel ouvrage en prose Cheikh Ahmadou Bamba a-t-il principalement versifié (v.25 & v.38) ?", "options": ["Hâtimat at-Tasawwuf d'Al-Yadâlî", "Le Muwatta de l'Imam Mâlik", "Sahîh al-Bukhârî", "La Risâla d'Ibn Abî Zayd"], "answer": 0, "explication": "v.25 & v.38 : il a versifié « Hâtimat at-Tasawwuf » (le complément du soufisme) d'Al-Yadâlî."},
                    {"q": "Dans Masaalikul Jinaan, quand l'auteur écrit simplement « il dit » sans citer de nom, de quel savant s'agit-il (v.42) ?", "options": ["Ibn Khaldûn", "L'Imam Al-Ghazâlî", "Al-Bukhârî", "L'Imam Ash-Shâfi'î"], "answer": 1, "explication": "v.42 précise : « Quand je prononce le mot \"il dit\" sans expliciter un nom, c'est du célèbre Ghazâlî qu'il s'agit. »"},
                    {"q": "Quel est le seul critère d'estime auprès d'Allah selon le vers 48 ?", "options": ["La couleur de la peau", "La crainte d'Allah (piété)", "L'ancienneté de la lignée", "La richesse matérielle"], "answer": 1, "explication": "v.48 : « L'homme le plus estimé auprès d'Allah est celui qui Le craint le plus, sans discrimination d'aucune sorte. »"},
                    {"q": "Que dit le vers 49 au sujet de la couleur de la peau ?", "options": ["Elle détermine l'intelligence", "Elle ne saurait être cause de l'idiotie ni d'une mauvaise compréhension", "Elle empêche d'écrire des livres", "Elle définit le rang spirituel"], "answer": 1, "explication": "v.49 affirme clairement que la couleur de la peau ne saurait être cause d'idiotie ni de mauvaise compréhension."},
                    {"q": "Quelle image du vers 53 montre que les générations récentes peuvent recevoir de grandes grâces ?", "options": ["Un arbre sans racines", "Une fine pluie devançant une pluie abondante", "Un navire sans voile", "Une montagne de sable"], "answer": 1, "explication": "v.53 : « Une fine pluie peut en devancer une abondante, mais l'avantage est pour l'abondante. »"},
                    {"q": "Combien de chapitres suivent le Préambule selon le vers 74 ?", "options": ["Deux chapitres", "Trois chapitres", "Cinq chapitres", "Sept chapitres"], "answer": 1, "explication": "v.74 : « Cet ouvrage se compose de trois chapitres précédés d'un préambule. »"},
                ],
            },
            {
                "num": 2,
                "slug": "fiqh-soufisme-science",
                "titre": "Fiqh, Soufisme & Science Utile",
                "versets": "v.80 – v.183",
                "duree": "5 min",
                "icone": "fa-book-open-reader",
                "resume": "Le livre expose l'union obligatoire du fiqh et du soufisme (parole de l'Imam Mâlik), le lien entre science et action, la hiérarchie des sciences, la valeur de chaque respiration et les signes de la vraie science utile.",
                "passages": [
                    {"ref": "v.80 – v.89", "titre": "Unir le Fiqh et le Tasawwuf", "texte": "Le fiqh régit l'action extérieure et le tasawwuf régit les états du cœur. Selon l'Imam Mâlik : pratiquer le fiqh sans soufisme mène à la perversion, le soufisme sans fiqh à l'hérésie (zindîq) ; réunir les deux est le modèle parfait."},
                    {"ref": "v.91 – v.105", "titre": "Science et Action", "texte": "La science est le fondement de l'action, mais elle ne porte de fruits que par la pratique. Un peu d'actions fondées sur la science vaut davantage que beaucoup d'actions accomplies dans l'ignorance."},
                    {"ref": "v.102", "titre": "Le piège de l'ajournement", "texte": "Ajournement du repentir par crainte de récidiver : Cheikh Ahmadou Bamba avertit que cela constitue un piège tendu à l'homme par Satan le rebelle."},
                    {"ref": "v.106 – v.116", "titre": "Critère de la science utile", "texte": "La seule science utile est celle apprise exclusivement pour Allah. Elle inspire la crainte d'Allah, l'humilité, la bonne conduite, purifie le cœur et préserve des péchés — jamais celle apprise pour la gloire ou les polémiques."},
                    {"ref": "v.118 – v.128", "titre": "Hiérarchie des sciences et des actes", "texte": "En tête des sciences vient la théologie (Tawhîd), puis l'exégèse coranique, le Hadîth et le fiqh. La meilleure action profite au plus grand nombre et se fait avec constance. Le pire péché est celui qui endurcit le cœur."},
                    {"ref": "v.137 – v.183", "titre": "Une lumière dans le cœur", "texte": "Chaque respiration vaut une pierre précieuse sans égal. La qualité de savant ne vient pas du nombre de récits débités : « la science est une lumière qui réside dans le cœur », et celui qui ne craint pas Allah n'est pas un vrai 'âlim."},
                ],
                "questions": [
                    {"q": "Que régit chacune des deux parties de la science selon les vers 80–82 ?", "options": ["Le fiqh régit l'action extérieure, le tasawwuf régit les états d'âme", "Les deux régissent uniquement le commerce", "Le tasawwuf remplace le fiqh", "Le fiqh concerne uniquement la grammaire"], "answer": 0, "explication": "v.81–82 : l'exotérique (fiqh) régit l'action des hommes ; l'ésotérique (tasawwuf) régit les états d'âme."},
                    {"q": "Selon l'Imam Mâlik cité aux vers 87–90, qui est le beau modèle à suivre ?", "options": ["Celui qui néglige le fiqh", "Celui qui néglige le soufisme", "Celui qui réunit le fiqh et le tasawwuf", "Celui qui se contente de débattre"], "answer": 2, "explication": "v.89 : « Qui arrive à réunir les deux (le fiqh et le tasawwuf) est un beau modèle ; il faut suivre son exemple. »"},
                    {"q": "Pourquoi l'ajournement du repentir par peur de récidiver est-il dangereux (v.102) ?", "options": ["C'est un signe de sagesse", "C'est un piège tendu par Satan", "C'est recommandé chez les débutants", "Cela augmente les récompenses"], "answer": 1, "explication": "v.102 affirme que retarder le repentir par crainte de récidiver est un piège de Satan."},
                    {"q": "Que vaut un peu d'actions fondées sur la science face à beaucoup d'actions dans l'ignorance (v.105) ?", "options": ["Moins de récompense", "Autant de récompense", "Plus de récompense sans doute", "Aucune différence"], "answer": 2, "explication": "v.105 : « Un peu de bonnes actions fondées sur la science a plus de récompense que beaucoup d'actions avec ignorance. »"},
                    {"q": "Quelle est la meilleure des sciences selon le vers 118 ?", "options": ["La prosodie", "La théologie (profession de foi / Tawhîd)", "La rhétorique", "L'histoire ancienne"], "answer": 1, "explication": "v.118 : « La meilleure des sciences dans leur ensemble est sans controverse la théologie. »"},
                    {"q": "Quelle est la pire désobéissance selon le vers 128 ?", "options": ["Celle qui fait pleurer", "Celle qui endurcit le cœur et fait oublier Allah", "Celle dont on se repent aussitôt", "Une erreur involontaire"], "answer": 1, "explication": "v.128 : « La pire désobéissance est celle qui endurcit le cœur et fait oublier Allah et Son adoration. »"},
                    {"q": "À quoi le vers 138 compare-t-il le temps d'une seule respiration ?", "options": ["À un grain de poussière", "À une pierre précieuse sans égal", "À une heure de sommeil", "À un nuage d'été"], "answer": 1, "explication": "v.138 : « Le temps même d'une respiration vaut une pierre précieuse sans égal. »"},
                    {"q": "Comment les vers 181–183 définissent-ils le véritable savant ('âlim) ?", "options": ["Celui qui parle le plus longtemps", "Celui dont la science est une lumière dans le cœur qui engendre la crainte d'Allah", "Celui qui cherche la célébrité", "Celui qui critique ses frères"], "answer": 1, "explication": "v.181 & v.183 : la science est une lumière résidant dans le cœur ; sans crainte d'Allah, nul n'est vraiment 'âlim."},
                ],
            },
            {
                "num": 3,
                "slug": "sagesse-profonde-oraison",
                "titre": "Sagesse Profonde & Oraison",
                "versets": "v.184 – v.223",
                "duree": "4 min",
                "icone": "fa-sun",
                "resume": "Maximes fondamentales sur la proportion de nos actes envers ce monde et l'Au-delà, suivies des prières surérogatoires qui vivifient le temps : Witr, Fajr, Duhâ (Yoor-Yoor), six rak'as après Maghrib et assise après Subh.",
                "passages": [
                    {"ref": "v.187 – v.191", "titre": "Règles de sagesse profonde", "texte": "Agis pour ce bas-monde à la mesure de ton bref séjour, et pour l'Au-delà à la mesure de ton séjour éternel. Multiplie les bonnes œuvres autant que tu as besoin d'Allah. Si tu crains Allah comme il se doit, toute créature te craindra."},
                    {"ref": "v.195 – v.198", "titre": "Witr et les deux rak'as du Fajr", "texte": "Le Witr est la plus recommandée des prières de la Sunna. Les deux rak'as du Fajr peuvent être rattrapées entre le lever du soleil et midi ; y réciter Ash-Sharh et Al-Fîl offre une protection contre tout ennemi."},
                    {"ref": "v.201 – v.205", "titre": "Maghrib, Zuhr et Asr", "texte": "Prier six rak'as après Maghrib sans interruption déplacée équivaut à douze ans d'adoration agréée. Quatre rak'as avant et après Zuhr garantissent contre la Géhenne ; quatre avant Asr attirent la Miséricorde divine."},
                    {"ref": "v.206 – v.210", "titre": "La prière de Duhâ (Yoor-Yoor)", "texte": "Deux, six ou huit rak'as après le lever du soleil : celui qui observe régulièrement Duhâ, Allah le protège et cette prière intercédera pour lui au Jour du Jugement."},
                    {"ref": "v.214 – v.222", "titre": "L'oraison du matin et les prosternations", "texte": "Rester assis après Subh en assemblée à évoquer Allah jusqu'au lever du soleil vaut un pèlerinage majeur et mineur. Et à chaque inclinaison ou prosternation recueillie, les péchés tombent des épaules du fidèle."},
                ],
                "questions": [
                    {"q": "Comment faut-il proportionner ses actes pour ce monde et l'Au-delà (v.188–189) ?", "options": ["Tout consacrer à ce bas-monde", "Selon la durée du séjour dans chacun des deux mondes", "Négliger toute action", "Attendre la vieillesse"], "answer": 1, "explication": "v.188–189 : agir pour chaque demeure en fonction de la durée du séjour qu'on y fera."},
                    {"q": "Que se passe-t-il si tu crains ton Seigneur l'Unique comme il se doit (v.191) ?", "options": ["Tu perds tes amis", "Chaque être vivant te craint pour cette raison", "Tu n'as plus besoin de prier", "Tu deviens riche immédiatement"], "answer": 1, "explication": "v.191 : « Si tu crains ton Seigneur l'Un, comme il se doit, chaque être vivant te craint pour cette raison. »"},
                    {"q": "Quelles deux sourates est-il recommandé de réciter dans les deux rak'as du Fajr pour être protégé des ennemis (v.198) ?", "options": ["Al-Baqara et Yâ-Sîn", "Ash-Sharh (Alam Nashrah) et Al-Fîl (Alam Tara)", "Al-Kahf et Al-Mulk", "Al-Falaq et An-Nâs"], "answer": 1, "explication": "v.198 mentionne explicitement les deux sourates commençant par « Alam » : Ash-Sharh et Al-Fîl."},
                    {"q": "À combien d'années d'adoration agréée équivalent les 6 rak'as après Maghrib sans interruption déplacée (v.201–202) ?", "options": ["2 ans", "5 ans", "12 ans", "40 ans"], "answer": 2, "explication": "v.202 : « Son action lui vaut, aux yeux d'Allah, l'adoration agréée de douze ans. »"},
                    {"q": "Combien de rak'as surérogatoires sont recommandées pour la prière d'Asr selon le vers 193 ?", "options": ["Quatre avant et quatre après", "Quatre avant, mais non après", "Deux après seulement", "Huit avant"], "answer": 1, "explication": "v.193 : « quatre avant, mais non après celle du milieu de l'après-midi (al-asr) »."},
                    {"q": "Quel est le nombre maximal habituel de rak'as pour Ad-Duhâ (Yoor-Yoor) avant que certains savants ne jugent le surplus blâmable (v.199 & v.210) ?", "options": ["Deux", "Quatre", "Huit", "Vingt"], "answer": 2, "explication": "v.199 & v.210 : on prie 2, 6 ou 8 rak'as ; dépasser 8 est jugé blâmable par certains docteurs."},
                    {"q": "Quelle récompense obtient celui qui reste en dhikr après Subh en assemblée jusqu'au lever du soleil (v.215–216) ?", "options": ["Un jour de jeûne", "Le mérite d'un pèlerinage majeur et mineur parfaits", "Une semaine de prières", "Dix aumônes"], "answer": 1, "explication": "v.216 : il obtient le même mérite que les pèlerinages majeur (Hajj) et mineur (Umra) parfaits."},
                    {"q": "Qu'advient-il des péchés lorsque le fidèle s'incline et se prosterne avec recueillement (v.221–222) ?", "options": ["Ils restent inchangés", "Ils s'effacent et tombent de ses épaules et de sa nuque", "Ils sont reportés", "Ils diminuent seulement le vendredi"], "answer": 1, "explication": "v.222 : « Ses péchés tombent de dessus ses épaules et de sa nuque. »"},
                ],
            },
            {
                "num": 4,
                "slug": "jeune-des-organes",
                "titre": "Le Jeûne des Organes & Achoura",
                "versets": "v.224 – v.266",
                "duree": "4 min",
                "icone": "fa-moon",
                "resume": "La porte du Paradis réservée aux jeûneurs, le jeûne mensuel de trois jours, les vertus et pratiques d'Achoura (10 Muharram), et surtout le véritable jeûne de tous les membres et la sobriété à la rupture.",
                "passages": [
                    {"ref": "v.224 – v.227", "titre": "La porte des jeûneurs & les 3 jours par mois", "texte": "Il existe au Paradis une porte accessible aux seuls jeûneurs. L'Imam Mâlik jeûnait trois jours chaque mois : multipliés par dix par la Bonté d'Allah, cela équivaut à jeûner toute l'année."},
                    {"ref": "v.234 – v.244", "titre": "Achoura (Tamkharit) et ses 12 bonnes pratiques", "texte": "Le 10e jour de Muharram (Achoura) est supérieur à sa veille (Tâsu'â). Parmi ses pratiques recommandées : le jeûne, la prière, les visites familiales, l'aumône, la visite aux malades et aux érudits, caresser la tête d'un orphelin, réciter Al-Ikhlâs 1000 fois et offrir un bon repas à la famille."},
                    {"ref": "v.245 – v.254", "titre": "Les prodiges prophétiques d'Achoura", "texte": "C'est en ce jour qu'Allah pardonna à Adam, posa l'Arche de Noé sur le mont Jûdî, fendit la mer pour Moïse, sauva Jonas du poisson, sortit Joseph du puits et protégea Abraham du feu."},
                    {"ref": "v.255 – v.259", "titre": "Le vrai jeûne engage tous les membres", "texte": "Le jeûne ne se limite pas à s'abstenir de manger et de boire ! Combien n'en retirent que faim et soif ! Tous les organes doivent jeûner : les yeux, les pieds, les oreilles, la langue et même les pensées du cœur."},
                    {"ref": "v.260 – v.265", "titre": "Attention à la gloutonnerie à la rupture", "texte": "Ne te gave pas à l'aube ni au coucher du soleil : se remplir l'estomac à l'excès alourdit le corps, assombrit le cœur et détourne de l'évocation d'Allah, faisant perdre la récompense du jeûne."},
                ],
                "questions": [
                    {"q": "Pourquoi jeûner 3 jours par mois équivaut-il à jeûner tout le temps (v.226–227) ?", "options": ["Parce qu'un mois a 3 jours", "Parce qu'Allah multiplie chaque bonne action par dix", "Parce que c'est réservé aux savants", "Parce que le jeûne nocturne compte double"], "answer": 1, "explication": "v.227 : grâce à la multiplication par dix (3 × 10 = 30 jours), cela équivaut à un jeûne continu."},
                    {"q": "Quel jour correspond à Achoura (v.236) ?", "options": ["Le 1er Ramadan", "Le 10e jour du 1er mois lunaire (Muharram)", "Le 27 Rajab", "Le 15 Sha'bân"], "answer": 1, "explication": "v.236 : Achoura est le 10e jour du 1er mois lunaire (Muharram / Tamkharit)."},
                    {"q": "Combien de pratiques recommandées pour Achoura le livre énumère-t-il aux vers 240–242 ?", "options": ["Quatre", "Sept", "Douze", "Vingt"], "answer": 2, "explication": "v.242 indique « la douzième (12e) des recommandations est de préparer à la famille un repas copieux »."},
                    {"q": "Lequel de ces événements est associé au jour d'Achoura aux vers 246–251 ?", "options": ["Le pardon accordé à Adam et la mer fendue pour Moïse", "La bataille de Badr", "L'Hégire à Médine", "La conquête de La Mecque"], "answer": 0, "explication": "v.246–251 citent Adam, Noé, Moïse, Jonas, Joseph, Abraham, Idrîs, Jésus et David."},
                    {"q": "Que risquent certains jeûneurs selon le vers 256 ?", "options": ["D'obtenir trop de récompenses", "De ne retirer de leur jeûne que la faim et la soif", "De perdre la mémoire", "De ne pas dormir"], "answer": 1, "explication": "v.256 : « Que de jeûneurs parmi les gens qui n'auront de leur jeûne que la faim (et la soif). »"},
                    {"q": "Quels éléments doivent participer au véritable jeûne selon les vers 257–259 ?", "options": ["Seulement l'estomac", "Tous les membres, organes (yeux, langue, oreilles, pas) et les pensées", "Seulement la langue", "Uniquement les mains"], "answer": 1, "explication": "v.257–259 exigent que tous les membres et même les pensées s'abstiennent du prohibé."},
                    {"q": "Quel effet provoque l'excès de nourriture à l'aube ou à la rupture du jeûne (v.264–265) ?", "options": ["Il illumine l'esprit", "Il alourdit le ventre, assombrit le cœur et détourne du dhikr", "Il double la récompense", "Il facilite la prière de nuit"], "answer": 1, "explication": "v.264–265 : un ventre trop rempli rend le cœur obstrué, assombri et détourné de la mention d'Allah."},
                    {"q": "Que procure le fait d'offrir un repas généreux à sa famille le jour d'Achoura (v.244) ?", "options": ["De la fatigue inutile", "L'accroissement des chances de subsistance et de biens par la volonté d'Allah", "Rien de particulier", "L'exemption de la prière"], "answer": 1, "explication": "v.244 : « Le festoiement de notre famille accroît et multiplie nos chances pour l'acquisition des biens. »"},
                ],
            },
        ],
    },
    {
        "id": 2,
        "code": "porte-2",
        "titre": "Porte II · Les Pratiques Vivifiantes du Cœur",
        "sous_titre": "Le Wird, le Dhikr, la Méditation (Fikr), l'Aumône fraternelle et la Lecture du Coran (v.267–601)",
        "icone": "fa-heart-pulse",
        "couleur": "from-amber-600 to-yellow-700",
        "accent": "#FBBF24",
        "chapitres": [
            {
                "num": 5,
                "slug": "wird-guide-spirituel",
                "titre": "Le Wird & Le Guide Spirituel",
                "versets": "v.267 – v.298",
                "duree": "4 min",
                "icone": "fa-water",
                "resume": "Définition du wird (point d'eau spirituel), respect fraternel de toutes les voies soufies (Qâdiriyya, Tijâniyya, etc.), distinction entre prophètes et saints, et nécessité d'un éducateur spirituel.",
                "passages": [
                    {"ref": "v.269 – v.271", "titre": "Définition et sens du Wird", "texte": "Le wird est un acte d'adoration déterminé pratiqué dans un temps régulier. Étymologiquement, « wird » signifie stationner à un point d'eau pour boire ou puiser. Chaque wird mène sans déviation vers l'enceinte scellée d'Allah."},
                    {"ref": "v.272 – v.275", "titre": "Fraternité entre tous les Wirds", "texte": "Qu'il vienne de Cheikh Abd al-Qâdir al-Jîlânî, de Cheikh Ahmad at-Tijânî ou d'un autre Pôle : tous les wirds sont dans la rectitude et appellent à l'adoration d'Allah. Garde-toi d'en mépriser ou d'en critiquer aucun !"},
                    {"ref": "v.276 – v.285", "titre": "Prophètes et Saints", "texte": "Le wird tire son origine du Coran et de la Sunna par révélation (prophètes) ou inspiration (saints). Les prophètes sont impeccables (ma'sûm) et les saints sont protégés (mahfûz) et héritiers des prophètes."},
                    {"ref": "v.287 – v.298", "titre": "Assiduité, respect et guide spirituel", "texte": "Celui qui ne pratique aucun wird perd son temps. Qui n'a jamais été formé par un guide spirituel valable risque que Satan le dirige. Si la paresse t'empêche d'aller au point d'eau, n'empêche pas les autres d'y puiser."},
                ],
                "questions": [
                    {"q": "Que signifie littéralement le mot arabe « wird » selon le vers 270 ?", "options": ["Un voyage en mer", "Stationner sur un point d'eau pour boire ou puiser", "Lire un livre d'histoire", "Jeûner trois jours"], "answer": 1, "explication": "v.270 : le vocable « wird » signifie stationner sur un point d'eau pour boire ou puiser."},
                    {"q": "Quelle attitude Cheikh Ahmadou Bamba ordonne-t-il envers les wirds des autres confréries (v.272–275) ?", "options": ["Les critiquer pour défendre le sien", "Ne jamais en mépriser ni en critiquer aucun car tous mènent à Allah", "Les ignorer complètement", "Ne respecter qu'un seul wird"], "answer": 1, "explication": "v.275 : « Tous les wirds sont dans la rectitude et la probité ; garde-toi d'en mépriser ou d'en critiquer aucun. »"},
                    {"q": "Quels sont les deux fondements textuels du wird selon le vers 278 ?", "options": ["La philosophie et la poésie", "Le Livre révélé (Coran) et la Parole prophétique (Sunna)", "Les coutumes locales", "La seule imagination"], "answer": 1, "explication": "v.278 : le wird a pour fondement le Coran et la Parole prophétique transmise par chaîne de garants."},
                    {"q": "Quelle distinction le vers 277 établit-il entre le prophète et le saint ?", "options": ["Aucune distinction", "La révélation est l'apanage du prophète, l'inspiration celui du saint", "Le saint reçoit une nouvelle loi", "Le prophète n'a pas d'héritiers"], "answer": 1, "explication": "v.277 : « La révélation est l'apanage du prophète, l'inspiration celui du saint. »"},
                    {"q": "Que dit le vers 283 sur la protection des prophètes et des saints ?", "options": ["Les prophètes sont impeccables, les saints sont protégés et honorés", "Aucun d'eux n'est protégé", "Les saints sont supérieurs aux prophètes", "Les prophètes peuvent faillir à leur mission"], "answer": 0, "explication": "v.283 : « Les prophètes du Très-Haut sont impeccables, Ses saints, quant à eux, sont protégés et honorés. »"},
                    {"q": "Quel danger guette celui qui n'a aucun directeur spirituel valable selon le vers 295 ?", "options": ["Il progresse plus vite", "Satan se charge de le diriger vers les voies de la perdition", "Il ne rencontre aucune épreuve", "Il devient automatiquement savant"], "answer": 1, "explication": "v.295 : « Celui qui n'a aucun guide (valable), Satan se chargera de le diriger dans les voies de la perdition. »"},
                    {"q": "Quel conseil donne le vers 297 à celui que la paresse empêche de faire le wird ?", "options": ["Critiquer ceux qui le font", "Ne pas empêcher les autres d'aller puiser au point d'eau", "Interdire les wirds", "Prétendre que le wird est inutile"], "answer": 1, "explication": "v.297 : « Si tu n'es pas capable de franchir la distance vers le point d'eau, ne cherche pas à empêcher les autres d'aller puiser. »"},
                    {"q": "De quoi dépendent la qualité et la quantité des récompenses du wird (v.298) ?", "options": ["De la vitesse de récitation uniquement", "Des qualités du wird et du recueillement du cœur", "Du nombre de spectateurs", "Du lieu géographique seul"], "answer": 1, "explication": "v.298 : elles dépendent « des qualités du wird et du recueillement (disposition du cœur) »."},
                ],
            },
            {
                "num": 6,
                "slug": "dhikr-priere-prophete",
                "titre": "Le Dhikr & La Prière sur le Prophète",
                "versets": "v.299 – v.408",
                "duree": "5 min",
                "icone": "fa-fingerprint",
                "resume": "Précellence du Dhikr (début de la sainteté), règles de bienséance, fruits spirituels de chaque formule (Shahâda, Basmala, Hawqala, Hasbala, Istighfâr), mérites immenses de la Salât 'alâ-n-Nabî et litanie du coucher.",
                "passages": [
                    {"ref": "v.299 – v.304", "titre": "Le Dhikr, début de la sainteté", "texte": "L'évocation habituelle d'Allah est la meilleure action de l'aspirant. La mention du Nom d'Allah constitue le début de la sainteté, et son abandon est le plus haut degré de l'égarement."},
                    {"ref": "v.311 – v.321", "titre": "Voix basse ou voix haute & bienséance", "texte": "Si le fidèle craint l'ostentation (riyâ), il évoque Allah à voix basse ; s'il en est affranchi, la voix haute incite autrui au bien. On s'assoit propre, parfumé, face à la Kaaba, car les anges et les djinns croyants assistent au dhikr."},
                    {"ref": "v.331 – v.355", "titre": "Les fruits de chaque formule", "texte": "La Shahâda est le prix du Paradis et la forteresse d'Allah : elle résume toutes les formules. Le Tahlîl ancre le Tawhîd, le Takbîr et le Hamd la gratitude, la Hawqala et la Hasbala l'abandon à Allah, et l'Istighfâr la crainte d'Allah."},
                    {"ref": "v.356 – v.375", "titre": "Les secrets de la Basmala", "texte": "Réciter 10 fois la Basmala + Hawqala le matin purifie des péchés, éloigne 72 malheurs et confie le fidèle à 70 anges. Récitée 21 fois avant de dormir, elle protège contre la mort subite, le vol et les démons."},
                    {"ref": "v.379 – v.390", "titre": "La Prière sur le Prophète (PSL)", "texte": "C'est la plus méritoire des occupations après les obligations divines. Selon Cheikh As-Sanûssî, elle peut tenir lieu de guide spirituel ; elle voile les défauts, illumine l'intérieur et l'extérieur, et vaut son intercession."},
                    {"ref": "v.401 – v.408", "titre": "La litanie précieuse avant le sommeil", "texte": "Chaque nuit avant de dormir : 4 Al-Fâtiha, 3 Al-Ikhlâs, 4 Al-Bâqiyât as-Sâlihât, 10 Istighfâr et 10 prières sur le Prophète — cela procure une fin de vie très heureuse et d'immenses récompenses."},
                ],
                "questions": [
                    {"q": "Comment le vers 304 qualifie-t-il la mention du Nom d'Allah ?", "options": ["Une simple habitude", "Le début de la sainteté", "Un acte réservé aux vieillards", "Une pratique secondaire"], "answer": 1, "explication": "v.304 : « La mention du Nom d'Allah constitue le début de la sainteté et son abandon est le plus haut degré de l'égarement. »"},
                    {"q": "Dans quel cas le juste milieu (v.312–315) recommande-t-il de faire le dhikr à voix basse ?", "options": ["Toujours le vendredi", "Si le fidèle craint de tomber dans l'ostentation (riyâ)", "Quand il est seul", "Uniquement la nuit"], "answer": 1, "explication": "v.312 : s'il craint le riyâ, il récite à voix basse ; s'il en est affranchi, la voix haute profite par l'imitation."},
                    {"q": "Quel est le fruit de la Hawqala et de la Hasbala (v.346–347) ?", "options": ["La richesse rapide", "L'abandon et la confiance absolue en Allah", "L'éloquence", "La force physique"], "answer": 1, "explication": "v.347 : leurs fruits sont « l'abandon à Allah Très-Haut et la forte volonté de compter sur Lui »."},
                    {"q": "Quelle formule condense à elle seule toutes les autres formules de dhikr (v.352–353) ?", "options": ["Subhânallâh seul", "Lâ ilâha illallâh Muhammadun Rasûlullâh", "Allâhu Akbar seul", "Al-Hamdulillâh seul"], "answer": 1, "explication": "v.352–353 : toutes les formules sont condensées dans « Lâ ilâha illallâh Muhammadun Rasûlullâh »."},
                    {"q": "Combien de fois faut-il réciter la Basmala avant de dormir pour être protégé contre la mort subite et le vol cette nuit-là (v.365–366) ?", "options": ["7 fois", "10 fois", "21 fois", "100 fois"], "answer": 2, "explication": "v.365–366 : « Qui la récite la nuit vingt-et-une (21) fois ni moins ni plus avant de dormir... »"},
                    {"q": "Combien de lettres compte la Basmala, chiffre égal à celui des anges Zabâniya (v.371) ?", "options": ["12 lettres", "19 lettres", "28 lettres", "33 lettres"], "answer": 1, "explication": "v.371 : « Le nombre de ses dix-neuf (19) lettres est graphiquement égal à celui des anges dits Zabâniya. »"},
                    {"q": "Que dit Cheikh As-Sanûssî au sujet de la prière sur le Prophète (v.381–382) ?", "options": ["Elle remplace la prière obligatoire", "Elle peut tenir lieu de guide spirituel vers la proximité du Prophète", "Elle ne se fait que le lundi", "Elle est réservée aux érudits"], "answer": 1, "explication": "v.382 : elle « peut tenir lieu de guide spirituel car elle amène l'aspirant jusqu'à la proximité du Prophète aimé »."},
                    {"q": "Que comprend la litanie nocturne recommandée aux vers 401–406 avant de dormir ?", "options": ["4 Fâtiha, 3 Ikhlâs, 4 Bâqiyât as-Sâlihât, 10 Istighfâr et 10 Salât 'alâ-n-Nabî", "Uniquement 1 Fâtiha", "Uniquement 33 Tasbîh", "Une lecture complète du Coran"], "answer": 0, "explication": "v.402–406 détaillent exactement cette série avant le sommeil."},
                ],
            },
            {
                "num": 7,
                "slug": "fikr-meditation",
                "titre": "Le Fikr — La Méditation",
                "versets": "v.409 – v.459",
                "duree": "4 min",
                "icone": "fa-brain",
                "resume": "La méditation comme miroir du croyant et voie de la certitude (exemple d'Abraham), les sujets recommandés (cieux, terre, bienfaits) et les pensées à éviter, jusqu'au « meilleur jihâd » (v.456).",
                "passages": [
                    {"ref": "v.411 – v.415", "titre": "Dhikr, Fikr et le miroir du cœur", "texte": "L'intimité avec Allah vient du dhikr, et la gnose vient de la méditation (fikr). Une heure de méditation l'emporte sur un an d'adoration. Elle est le miroir qui montre au croyant ses bonnes actions et ses défauts."},
                    {"ref": "v.425 – v.434", "titre": "La foi grandit par la réflexion", "texte": "La certitude née d'une méditation profonde est bien plus solide qu'une croyance irréfléchie. « L'intensité de ta foi augmente en fonction de la profondeur de tes pensées. » C'est par la méditation qu'Abraham acquit sa certitude."},
                    {"ref": "v.442 – v.450", "titre": "Sur quoi méditer ?", "texte": "Les meilleurs sujets de méditation sont les cieux, la terre, les astres, les bienfaits d'Allah (qui augmentent l'amour), la récompense promise et le châtiment. On médite sur les créatures, jamais sur l'Essence du Créateur."},
                    {"ref": "v.451 – v.457", "titre": "Les pensées à fuir et le meilleur Jihâd", "texte": "Ne rumine ni ton dénuement (source de tristesse), ni l'injustice subie (source de haine), ni de longs espoirs mondains. « Le meilleur jihâd consiste à empêcher l'esprit de s'occuper de ce qui ne lui incombe pas. »"},
                ],
                "questions": [
                    {"q": "Que procure respectivement le Dhikr et le Fikr selon le vers 412 ?", "options": ["Le Dhikr procure l'intimité avec Allah, le Fikr procure la gnose", "Les deux procurent le sommeil", "Le Fikr remplace la prière", "Le Dhikr sert seulement aux débutants"], "answer": 0, "explication": "v.412 : « L'intimité avec Allah s'acquiert par la mention constante, quant à la gnose, elle se réalise par la méditation. »"},
                    {"q": "À quoi le vers 414 compare-t-il la méditation ?", "options": ["À une épée", "À un miroir pour le croyant", "À un désert", "À un livre fermé"], "answer": 1, "explication": "v.414–415 : elle tient lieu de miroir qui révèle au croyant ses bonnes œuvres et ses défauts."},
                    {"q": "Sur quoi une seule heure de méditation a-t-elle la prééminence (v.413) ?", "options": ["Sur une semaine de voyage", "Sur l'adoration d'une année entière", "Sur dix minutes de lecture", "Sur un seul jour de jeûne"], "answer": 1, "explication": "v.413 : « On a rapporté la prééminence d'une heure de méditation sur l'adoration d'un an. »"},
                    {"q": "Quel Prophète est cité au vers 434 comme exemple de conviction acquise par la méditation ?", "options": ["Noé (Nûh)", "Abraham (Ibrâhîm)", "Salomon (Sulaymân)", "Job (Ayyûb)"], "answer": 1, "explication": "v.434 : « C'est par la méditation qu'Abraham, l'ami d'Allah, avait acquis sa conviction. »"},
                    {"q": "Comment un Saint a-t-il répondu à la question « Par quoi connais-tu Allah ? » (v.440–441) ?", "options": ["Par mes richesses", "Par Son fait de défaire toutes nos fermes décisions", "Par les rêves", "Par la philosophie grecque"], "answer": 1, "explication": "v.441 : « Je Le connais par Son fait de défaire toutes nos fermes décisions. »"},
                    {"q": "Quelle règle capitale pose le vers 450 sur l'objet de la méditation ?", "options": ["Réfléchir sur les créatures, mais non sur le Créateur Lui-même", "Ne jamais observer le ciel", "Méditer uniquement sur ses richesses", "Éviter toute réflexion"], "answer": 0, "explication": "v.450 : « Il faut beaucoup réfléchir sur les créatures après être instruit, mais non sur le Créateur Lui-même. »"},
                    {"q": "Pourquoi faut-il éviter de ruminer une injustice subie (v.452) ?", "options": ["Cela fait oublier ses droits", "Cela crée une forte haine et de la colère", "Cela donne faim", "Cela réduit le sommeil"], "answer": 1, "explication": "v.452 : penser à l'injustice subie « crée entre vous deux une forte haine et de la colère — sois patient »."},
                    {"q": "En quoi consiste « le meilleur jihâd » selon le vers 456 ?", "options": ["Débattre avec ses adversaires", "Empêcher l'esprit de s'occuper de ce qui ne lui incombe pas", "Voyager loin", "Accumuler des biens"], "answer": 1, "explication": "v.456 : « Le meilleur jihâd consiste à empêcher l'esprit de s'occuper de ce qui ne lui incombe pas. »"},
                ],
            },
            {
                "num": 8,
                "slug": "aumone-bonte-fraternelle",
                "titre": "L'Aumône & La Bonté Fraternelle",
                "versets": "v.460 – v.527",
                "duree": "5 min",
                "icone": "fa-hand-holding-heart",
                "resume": "La récompense exceptionnelle de ceux qui sont au service des créatures, les bienfaits spirituels et protecteurs de l'aumône, l'ordre de priorité (famille, proches, voisins) et les innombrables formes d'aumône sans argent.",
                "passages": [
                    {"ref": "v.462 – v.466", "titre": "Au service des créatures", "texte": "Au Jour du Jugement, un crieur appellera : « Où sont ceux qui ont été au service des créatures ? Entrez au Paradis sans peine ni épreuve ! » Rends donc tes services à tous exclusivement pour l'amour d'Allah."},
                    {"ref": "v.469 – v.471", "titre": "Donner sans craindre la pauvreté", "texte": "Ne thésaurise jamais ta fortune par crainte de pauvreté : c'est Allah qui t'a offert cette richesse. Si tu la dépenses pour Son amour, Il te restituera tout ce que tu auras donné."},
                    {"ref": "v.478 – v.491", "titre": "Les prodiges de l'aumône", "texte": "Une seule aumône écarte 70 sortes de morts affreuses, apaise la colère d'Allah, efface les fautes comme l'eau éteint le feu, guérit les malades, purifie la fortune et met le croyant à son ombre au Jour du Jugement."},
                    {"ref": "v.496 – v.500", "titre": "Pas de discrimination, priorité aux proches", "texte": "Toute discrimination dans l'aumône est interdite. Ne délaisse jamais un proche nécessiteux pour aller donner au loin : on commence par soi-même, puis ceux à notre charge, puis nos voisins."},
                    {"ref": "v.504 – v.527", "titre": "Les aumônes du cœur et du quotidien", "texte": "L'aumône ne se réduit pas à l'argent : une parole douce, un sourire en saluant, un bon conseil, écarter un obstacle du chemin, prêter un outil, visiter un malade, prier pour son frère ou tenir compagnie à une personne seule sont tous des aumônes !"},
                ],
                "questions": [
                    {"q": "Quel appel retentira au Jour du Jugement selon les vers 463–465 ?", "options": ["Où sont les rois ?", "Où sont ceux qui ont été au service des créatures ? Entrez au Paradis sans peine !", "Où sont les plus riches ?", "Où sont les plus célèbres ?"], "answer": 1, "explication": "v.463–465 promettent l'entrée au Paradis sans peine à ceux qui ont servi les créatures pour Allah."},
                    {"q": "Combien de personnes entrent au Paradis grâce à une seule bouchée de pain donnée au pauvre (v.474–477) ?", "options": ["Une seule", "Deux", "Trois (le maître de maison, son épouse et le servant)", "Dix"], "answer": 2, "explication": "v.475–477 citent le maître qui ordonne, son épouse vertueuse qui prépare/donne et le servant qui sert."},
                    {"q": "Combien de sortes de morts affreuses une seule aumône peut-elle écarter (v.481) ?", "options": ["Sept", "Trente", "Soixante-dix (70)", "Cent"], "answer": 2, "explication": "v.481 : « Une seule aumône peut écarter de lui soixante-dix (70) chefs de mort affreuse. »"},
                    {"q": "À quoi le vers 482 compare-t-il l'effet de l'aumône sur les fautes ?", "options": ["Au vent sur le sable", "À l'eau qui éteint le feu", "Au soleil sur la neige", "À la pluie sur les pierres"], "answer": 1, "explication": "v.482 : « Elle possède la vertu d'effacer les fautes comme celle de l'eau à éteindre le feu. »"},
                    {"q": "Quel ordre de priorité les vers 498–500 enseignent-ils pour la dépense et l'aumône ?", "options": ["Les inconnus lointains d'abord", "Soi-même, puis ceux à notre charge, puis nos voisins", "Seulement les voyageurs", "Seulement les étrangers"], "answer": 1, "explication": "v.499–500 : d'abord soi-même, puis ceux qui sont à notre charge, puis les voisins."},
                    {"q": "Si un même bien circule en aumône entre 70 000 personnes pour Allah, quelle est la récompense du dernier donneur (v.502–503) ?", "options": ["Moindre que le premier", "Égale à celle du premier", "Nulle", "Divisée par dix"], "answer": 1, "explication": "v.503 : « La récompense des derniers donneurs égalera celle des premiers. »"},
                    {"q": "Lequel de ces gestes est compté comme aumône aux vers 507–516 ?", "options": ["Ignorer son voisin", "Adresser de douces paroles et sourire au visage d'un croyant", "Critiquer un pauvre", "Thésauriser sa fortune"], "answer": 1, "explication": "v.507 & v.513–514 : paroles douces, compliments, sourire, félicitations et bons conseils sont des aumônes."},
                    {"q": "Que dit le vers 527 à propos d'une personne isolée ?", "options": ["Il faut l'éviter", "Lui tenir compagnie est compté comme une aumône", "Cela ne compte pas", "Il faut lui parler uniquement par lettre"], "answer": 1, "explication": "v.527 inclut le fait de « tenir compagnie à une personne en solitude » parmi les actes d'aumône."},
                ],
            },
            {
                "num": 9,
                "slug": "lecture-ethique-coran",
                "titre": "La Lecture & L'Éthique du Coran",
                "versets": "v.528 – v.601",
                "duree": "5 min",
                "icone": "fa-book-quran",
                "resume": "Ne jamais abandonner le Livre d'Allah (source de toutes les sciences), lire avec méditation et recueillement, les bienfaits de la lecture sur le Mushaf, les meilleurs moments et le respect matériel dû au Livre saint.",
                "passages": [
                    {"ref": "v.529 – v.537", "titre": "Source de toutes les sciences", "texte": "Qui veut la proximité d'Allah ne doit jamais abandonner le Coran : attache-toi à sa lecture, fût-ce 3 hizbs par jour. Le Coran est la source de toutes les sciences ; Satan trompe ceux qui prétendent qu'une autre pratique lui est supérieure."},
                    {"ref": "v.538 – v.546", "titre": "Méditer et appliquer", "texte": "Allah n'a révélé le Coran que pour qu'il soit appliqué. Quelques versets bien compris et médités valent mieux que de nombreuses sourates récitées sans réflexion, tout comme deux rak'as recueillies surpassent toute une nuit de prière distraite."},
                    {"ref": "v.547 – v.556", "titre": "Adab devant la Parole d'Allah", "texte": "Lis le Coran en état de pureté, face à la Kaaba, d'une voix posée et grave (tafkhîm), sans ostentation, conscient que tu t'adresses à ton Seigneur comme si tu Le voyais — car si tu ne Le vois pas, Lui te voit."},
                    {"ref": "v.560 – v.574", "titre": "Moments bénis & lecture sur le Mushaf", "texte": "Aucun moment n'est interdit pour lire le Coran ; les meilleurs sont la fin de la nuit, entre Maghrib et Ishâ, et après Subh. Regarder chaque jour dans le Mushaf fortifie la vue, est inscrit comme adoration et allège la peine des parents dans la tombe."},
                    {"ref": "v.580 – v.598", "titre": "Apprendre, enseigner et respecter le Mushaf", "texte": "« Le meilleur des humains est celui qui apprend le Coran et l'enseigne. » Il est louable d'embrasser le Mushaf et de le parfumer ; il est interdit de poser la tête ou un objet dessus, ou d'étendre les jambes vers lui."},
                ],
                "questions": [
                    {"q": "Quel rythme minimal quotidien de lecture du Coran Cheikh Ahmadou Bamba conseille-t-il au vers 531 ?", "options": ["Un verset par semaine", "Trois (3) hizbs chaque jour", "Seulement pendant le Ramadan", "Dix pages par mois"], "answer": 1, "explication": "v.531 : « Attache-toi à la lecture de ce livre, fût-ce trois (3) Hizb chaque jour. »"},
                    {"q": "Que dit le livre (v.533–534) de ceux qui prétendent que leur pratique soufie vaut mieux que la lecture du Coran ?", "options": ["Ils ont raison", "Ils avancent un argument faux et Satan les a trompés", "C'est une voie supérieure", "C'est recommandé aux savants"], "answer": 1, "explication": "v.534 : « Ont avancé un argument faux, Satan les a trompés par là ; lis le Coran pour avoir l'agrément d'Allah. »"},
                    {"q": "Selon Ibn Abbâs cité aux vers 544–546, qu'est-ce qui vaut mieux que prier toute la nuit avec distraction ?", "options": ["Dormir toute la nuit", "Deux rak'as avec méditation et bon état du cœur", "Lire très vite sans réfléchir", "Parler de religion"], "answer": 1, "explication": "v.545–546 : deux rak'as avec méditation et cœur présent valent mieux que toute une nuit distraite."},
                    {"q": "Y a-t-il un moment interdit pour lire le Saint Coran selon le vers 557 ?", "options": ["Oui, après Asr", "Non, aucun moment n'est interdit selon les hommes dignes de confiance", "Oui, la nuit", "Oui, le lundi"], "answer": 1, "explication": "v.557–559 réfutent l'idée d'une interdiction après Asr : aucun moment n'est interdit."},
                    {"q": "Quels deux bienfaits particuliers le livre associe-t-il à la lecture directe dans le Mushaf (v.564–567) ?", "options": ["Une bonne vision et l'allègement des peines des parents dans la tombe", "La richesse immédiate", "La dispense du jeûne", "Le voyage gratuit"], "answer": 0, "explication": "v.565–567 : Allah gratifie le lecteur d'une bonne vision et allège la peine de ses deux parents."},
                    {"q": "Pourquoi est-il blâmable de ne pas regarder le Coran tous les jours (v.573–574) ?", "options": ["Parce que le papier jaunit", "Car un seul regard posé dans le Mushaf est inscrit comme acte de dévotion", "Parce que c'est interdit le jeudi", "Pour impressionner ses voisins"], "answer": 1, "explication": "v.574 : « Un seul regard jeté dans le Mushaf est mentionné au bénéfice du fidèle comme acte de dévotion. »"},
                    {"q": "Quelle est la nature juridique de la mémorisation du Coran dans la communauté (v.581–583) ?", "options": ["Une obligation divine collective (fard kifâya)", "Un acte facultatif sans importance", "Réservée aux imams seulement", "Interdite contre rémunération"], "answer": 0, "explication": "v.581–583 : c'est une obligation collective ; si un nombre suffisant l'assume, les autres en sont déchargés."},
                    {"q": "Lequel de ces gestes est formellement interdit envers le Mushaf (v.590–592) ?", "options": ["Le parfumer", "Le poser sur un support élevé", "Poser sa tête ou des objets lourds dessus, ou tendre les jambes vers lui", "L'écrire d'une belle écriture lisible"], "answer": 2, "explication": "v.590–592 interdisent de poser la tête ou des objets dessus, ou de tendre ses jambes vers le Livre saint."},
                ],
            },
        ],
    },
    {
        "id": 3,
        "code": "porte-3",
        "titre": "Porte III · Guérir les Vices Graves du Cœur",
        "sous_titre": "Jalousie, Haine, For intérieur, Pleurnicherie, Travail (Kasb) & Tawakkul, Passion du bas-monde et Colère (v.969–1087)",
        "icone": "fa-shield-heart",
        "couleur": "from-rose-700 to-amber-800",
        "accent": "#FB7185",
        "chapitres": [
            {
                "num": 10,
                "slug": "jalousie-haine-for-interieur",
                "titre": "Jalousie, Haine, Méchanceté & For Intérieur",
                "versets": "v.969 – v.997",
                "duree": "4 min",
                "icone": "fa-eye-slash",
                "resume": "Définitions précises du hasad (jalousie), du hiqd (haine) et du ghish (méchanceté/tromperie), leurs remèdes spirituels, et l'appel à embellir le for intérieur plutôt que les apparences.",
                "passages": [
                    {"ref": "v.969 – v.971", "titre": "La jalousie (Hasad)", "texte": "Le hasad consiste à souhaiter la disparition du bien d'un croyant. Le jaloux s'attriste toujours du bien de son frère et ne se réjouit qu'en le voyant dans le malheur."},
                    {"ref": "v.972 – v.974", "titre": "La haine (Hiqd) et la tromperie (Ghish)", "texte": "Le hiqd est de haïr les gens de la bonne direction sans raison valable selon la Sharî'a. Le ghish (méchanceté) consiste à cacher les défauts d'une chose ou d'une personne afin de faire trébucher l'intéressé."},
                    {"ref": "v.975 – v.983", "titre": "Le remède contre la haine", "texte": "Lutte contre ta haine en priant pour ton frère en son absence et en lui souhaitant du bien. Celui qui déteste qui Allah a favorisé s'oppose en réalité à la Volonté souveraine d'Allah !"},
                    {"ref": "v.984 – v.995", "titre": "Embellir le cœur, fuir le prestige mondain", "texte": "Embellis ton for intérieur, lieu du regard d'Allah, plutôt que l'aspect extérieur que regardent les créatures : celui qui perfectionne son cœur voit s'améliorer ses actes et ses paroles. La recherche de gloire et de rivalité éloigne d'Allah."},
                ],
                "questions": [
                    {"q": "Comment le vers 969 définit-il exactement la jalousie (hasad) ?", "options": ["Admirer le bien d'autrui", "Souhaiter la disparition du bien d'un croyant", "Travailler dur pour réussir", "Conseiller son frère"], "answer": 1, "explication": "v.969 : « Souhaiter la disparition du bien d'un croyant est ce qu'on appelle le hasad. »"},
                    {"q": "Qu'est-ce que le « ghish » (méchanceté) selon le vers 973 ?", "options": ["Dire la vérité avec douceur", "Cacher les défauts d'une chose ou personne dans le but de faire trébucher l'intéressé", "Aider un voyageur", "Oublier un rendez-vous"], "answer": 1, "explication": "v.973 définit le ghish comme le fait de dissimuler des défauts pour tromper autrui."},
                    {"q": "Quel remède concret le vers 977 prescrit-il contre la haine envers un frère ?", "options": ["L'éviter à jamais", "Prier pour lui en son absence et lui souhaiter du bien", "Raconter ses erreurs", "Lui répondre durement"], "answer": 1, "explication": "v.977 : « Prie pour lui en son absence et souhaite-lui du bien et non du mal. »"},
                    {"q": "En quoi détester celui qu'Allah a favorisé est-il particulièrement grave (v.978–980) ?", "options": ["On s'oppose à la Volonté souveraine du Créateur", "On perd de l'argent", "On fatigue sa voix", "On manque de sommeil"], "answer": 0, "explication": "v.979–980 : son cœur souffre de l'arrêt d'Allah et s'oppose à Sa Volonté souveraine."},
                    {"q": "Par quoi repousse-t-on l'artifice extérieur associé à un cœur infesté de mauvaises pensées (v.984–985) ?", "options": ["Par de beaux vêtements", "Par la répétition continuelle des Noms d'Allah avec présence du cœur", "Par le silence absolu", "Par les voyages"], "answer": 1, "explication": "v.985 : cet état est repoussé par le dhikr continuel avec la présence du cœur."},
                    {"q": "Quelle différence le vers 987 souligne-t-il entre le regard d'Allah et celui des créatures ?", "options": ["Aucune différence", "Allah considère le cœur et ses qualités, les créatures ne regardent que l'aspect extérieur", "Les créatures voient les pensées secrètes", "Allah regarde seulement les vêtements"], "answer": 1, "explication": "v.987 : « Le Seigneur considère le cœur et ses qualités alors que les créatures ne regardent que l'aspect extérieur. »"},
                    {"q": "Qu'arrive-t-il à celui qui perfectionne l'état de son cœur (v.989) ?", "options": ["Ses actes et ses paroles s'améliorent et il acquiert le bonheur", "Il devient invisible", "Il perd ses biens", "Il ne travaille plus"], "answer": 0, "explication": "v.989 : « Celui qui perfectionne l'état de son cœur voit s'améliorer la qualité de ses actes et de ses paroles. »"},
                    {"q": "Dans quel cas la recherche de distinction ou d'autorité n'éloigne-t-elle pas d'Allah (v.992) ?", "options": ["Jamais", "Uniquement si l'on s'en sert comme moyen pour chercher la Face et l'agrément d'Allah", "Quand on veut faire fortune", "Quand on veut dominer ses rivaux"], "answer": 1, "explication": "v.992 distingue l'objectif purement mondain de l'usage désintéressé au service de la Face d'Allah."},
                ],
            },
            {
                "num": 11,
                "slug": "tawakkul-travail-kasb",
                "titre": "Confiance en Allah, Travail (Kasb) & Abandon",
                "versets": "v.998 – v.1056",
                "duree": "5 min",
                "icone": "fa-briefcase",
                "resume": "Guérir de la pleurnicherie en comprenant le décret divin, éviter les mauvaises opinions et la remise au lendemain, et surtout allier harmonieusement le travail licite (kasb) et la confiance totale en Allah (tawakkul).",
                "passages": [
                    {"ref": "v.998 – v.1009", "titre": "Cesser de se plaindre aux créatures", "texte": "Les humains sont impuissants : Allah en a fini avec quatre choses — la durée de vie, la création, le caractère et la subsistance. Si toutes les créatures se coalisaient, elles ne pourraient déplacer un atome sans Sa permission."},
                    {"ref": "v.1010 – v.1021", "titre": "S'abandonner à Allah sans mépriser le pauvre", "texte": "Compte entièrement sur Allah qui garantit à chaque être sa subsistance. N'accorde jamais dans ton cœur plus de place au riche en te détournant de l'indigent."},
                    {"ref": "v.1026 – v.1035", "titre": "Humilité et danger de la procrastination", "texte": "Se croire supérieur aux autres est une grande illusion : aie bonne opinion des croyants et examine tes propres fautes. La plupart des cris en Enfer ont pour cause la remise au lendemain des actes pieux."},
                    {"ref": "v.1036 – v.1044", "titre": "Allier le travail (Kasb) au Tawakkul", "texte": "Abandonner les activités utiles sous prétexte de tawakkul tout en enviant les gens est le comportement des sots. L'abandon à Allah n'exclut nullement le travail (kasb) : le meilleur comportement consiste à allier les deux !"},
                    {"ref": "v.1049 – v.1056", "titre": "Réunir Sharî'a et Haqîqa", "texte": "Respecte les causes et les moyens extérieurs pour obéir à la Sharî'a, tout en comptant intérieurement sur Allah Seul pour réaliser la Haqîqa : omettre la première mène à l'hérésie, omettre la seconde à l'idolâtrie."},
                ],
                "questions": [
                    {"q": "Quelles sont les quatre choses dont Allah en a déjà fini le décret (v.1001) ?", "options": ["L'or, l'argent, la maison et le voyage", "La durée de vie, la création, le caractère et la fortune (subsistance)", "Les amis, les livres, le métier et le pays", "Le climat, les récoltes, la mer et les vents"], "answer": 1, "explication": "v.1001 énumère exactement : la durée de notre vie, notre création, notre caractère et notre fortune."},
                    {"q": "Que pourraient faire toutes les créatures coalisées sans la permission d'Allah (v.1005–1007) ?", "options": ["Changer ton destin", "Rien — pas même déplacer un seul atome", "Te priver de ta subsistance", "Allonger ta vie"], "answer": 1, "explication": "v.1006–1007 : elles ne pourraient déplacer un seul atome dans le royaume d'Allah sans Sa permission."},
                    {"q": "Quelle attitude envers le riche et l'indigent le vers 1020 interdit-il ?", "options": ["Saluer un riche", "Accorder dans son cœur plus de place au riche en se détournant de l'indigent", "Travailler avec un riche", "Conseiller un indigent"], "answer": 1, "explication": "v.1020–1021 rappellent qu'Allah l'avait même reproché au Prophète (sourate 'Abasa)."},
                    {"q": "Quelle est la cause de la plupart des cris des pécheurs en Enfer selon le vers 1034 ?", "options": ["La pauvreté", "La remise au lendemain (procrastination) des actes pieux", "L'oubli involontaire", "Le manque de livres"], "answer": 1, "explication": "v.1034 : « La plupart des cris des pécheurs demain dans l'Enfer ont pour cause la remise au lendemain des actes pieux. »"},
                    {"q": "Le tawakkul (abandon à Allah) exclut-il le travail (kasb) selon le vers 1037 ?", "options": ["Oui, totalement", "Non, il n'exclut nullement le travail pour gagner son pain", "Seulement pour les jeunes", "Oui, sauf en hiver"], "answer": 1, "explication": "v.1037 : « Sache que l'abandon à Allah n'exclut nullement le Kasb (le travail pour gagner le pain). »"},
                    {"q": "Quel est le meilleur comportement selon le vers 1039 ?", "options": ["Ne compter que sur son propre travail", "Allier le travail (kasb) à l'abandon confiant à Allah", "Vivre de mendicité", "Passer outre tous les moyens"], "answer": 1, "explication": "v.1039 : « Le meilleur comportement est d'allier le Kasb à l'abandon à Allah. »"},
                    {"q": "Comment réalise-t-on l'alliance de la Sharî'a et de la Haqîqa (v.1053–1055) ?", "options": ["En usant des moyens extérieurs (Sharî'a) tout en se soumettant intérieurement à Allah (Haqîqa)", "En rejetant les moyens extérieurs", "En oubliant Allah pendant le travail", "En vivant isolé sans rien faire"], "answer": 0, "explication": "v.1053–1055 : obéir aux lois de la Sharî'a extérieurement et compter sur Allah intérieurement."},
                    {"q": "Que dit le vers 1027 à propos du fait de se croire supérieur aux autres ?", "options": ["C'est un signe de force", "C'est l'une des plus grandes illusions", "C'est permis aux savants", "C'est une marque de fierté légitime"], "answer": 1, "explication": "v.1027 : « Le fait de se croire supérieur aux autres est parmi les plus grandes illusions. »"},
                ],
            },
            {
                "num": 12,
                "slug": "bas-monde-colere-impatience",
                "titre": "Bas-Monde, Désespoir, Colère & Impatience",
                "versets": "v.1057 – v.1087",
                "duree": "4 min",
                "icone": "fa-fire-extinguisher",
                "resume": "Se méfier du long espoir et de l'oisiveté, guérir du désespoir et de l'aveuglement sur ses propres fautes, se détacher de la passion mondaine, et maîtriser la colère ainsi que l'impatience.",
                "passages": [
                    {"ref": "v.1057 – v.1062", "titre": "Brièveté de la vie et danger de l'oisiveté", "texte": "Le long espoir et les projets lointains empêchent le repentir et dessèchent le cœur. Une vie passée dans l'oisiveté est une grave catastrophe : la vie humaine est très précieuse et ne doit être employée qu'à l'utile."},
                    {"ref": "v.1070 – v.1072", "titre": "Remède du désespoir et de l'aveuglement", "texte": "Le remède du désespoir est de méditer la Grandeur et l'infinie Miséricorde d'Allah. Le remède contre le fait de ne voir que les défauts d'autrui est d'accepter leurs excuses et de voiler leurs fautes."},
                    {"ref": "v.1073 – v.1082", "titre": "Guérir de la passion du bas-monde", "texte": "Réfléchis au néant de ce monde : où sont les anciens et leurs richesses ? Ce monde n'est pas une demeure éternelle ; seul est intelligent celui qui œuvre pour l'Au-delà. Quand tu fais un don, rappelle-toi que tu n'es qu'un intermédiaire d'Allah."},
                    {"ref": "v.1083 – v.1087", "titre": "Colère et impatience", "texte": "La colère, l'aigreur et la rage appartiennent aux traits de Satan : leur remède est de savoir que rien n'arrive sans la Volonté d'Allah. Face à l'impatience, remets-toi humblement au Tout-Puissant."},
                ],
                "questions": [
                    {"q": "Quels effets néfastes engendrent le long espoir et les projets lointains (v.1057) ?", "options": ["Ils empêchent le repentir, dessèchent le cœur et causent la paresse", "Ils augmentent la piété", "Ils rendent généreux", "Ils protègent du péché"], "answer": 0, "explication": "v.1057–1058 : ils empêchent de se repentir, engendrent la sécheresse du cœur, la paresse et le péché."},
                    {"q": "Comment le vers 1061 qualifie-t-il une vie passée dans l'oisiveté ?", "options": ["Un repos mérité", "Une vie vaine et une grave catastrophe", "Une marque d'ascèse", "Une chance rare"], "answer": 1, "explication": "v.1061–1062 : une vie passée dans l'oisiveté est une grave catastrophe ; la vie doit être employée à l'utile."},
                    {"q": "Si Allah ne te punit pas aussitôt après un péché, qu'est-ce que cela signifie (v.1066–1068) ?", "options": ["Qu'Il a oublié", "Que ce n'est ni oubli ni relâchement, mais un sursis redoutable (istidrâj)", "Que le péché est devenu licite", "Que tu es à l'abri de tout"], "answer": 1, "explication": "v.1067–1068 mettent en garde contre l'illusion de croire qu'Allah oublie ou se relâche."},
                    {"q": "Quel est le remède contre le désespoir selon le vers 1070 ?", "options": ["S'isoler dans la colère", "Penser à la Grandeur, à la Magnanimité et à la Miséricorde d'Allah", "Se plaindre aux gens", "Abandonner la prière"], "answer": 1, "explication": "v.1070 : méditer la Grandeur et la Miséricorde d'Allah relève le moral et console."},
                    {"q": "Comment guérir de l'aveuglement qui fait voir les défauts d'autrui et oublier les siens (v.1071–1072) ?", "options": ["En dénonçant leurs erreurs publiquement", "En acceptant leurs excuses et en voilant leurs défauts pour qu'Allah voile les tiens", "En coupant tout lien", "En les jugeant sévèrement"], "answer": 1, "explication": "v.1072 : accepter l'excuse des frères et voiler leurs défauts afin qu'Allah voile les nôtres au Jour du Jugement."},
                    {"q": "Qui est véritablement intelligent selon le vers 1077 ?", "options": ["Celui qui accumule le plus d'or", "Celui qui vise la Demeure éternelle en fournissant les efforts nuit et jour", "Celui qui se moque de ce monde sans travailler", "Celui qui multiplie les regrets"], "answer": 1, "explication": "v.1077 : « Seul est intelligent celui qui vise la Demeure éternelle, fournissant les efforts appropriés nuit et jour. »"},
                    {"q": "Pourquoi ne dois-tu jamais tirer orgueil d'un bienfait que tu donnes à autrui (v.1081–1082) ?", "options": ["Parce que c'est Allah qui dispense les faveurs et tu n'es qu'un intermédiaire", "Parce que le don ne compte pas", "Parce que le bénéficiaire oubliera", "Parce que c'est mal vu"], "answer": 0, "explication": "v.1082 : « Le Seigneur Très-Haut dispense les faveurs alors que tu n'es, en réalité, qu'un intermédiaire. »"},
                    {"q": "Quel est le remède contre la colère et la rage selon le vers 1085 ?", "options": ["Se venger immédiatement", "Savoir que rien ne s'accomplit réellement que par la Volonté d'Allah", "Crier plus fort", "Garder rancune longtemps"], "answer": 1, "explication": "v.1085 : « Son remède est de savoir que l'action ne s'accomplit réellement que par la Volonté d'Allah Très-Haut. »"},
                ],
            },
        ],
    },
    {
        "id": 4,
        "code": "porte-4",
        "titre": "Porte IV · Les Qualités, L'Adab & Les Secrets",
        "sous_titre": "Conduite extérieure, Prière de nuit, Shukr, Sabr, Secrets de l'Invocation, Respect des Saints & Sourates (v.1088–1562)",
        "icone": "fa-crown",
        "couleur": "from-indigo-700 to-emerald-800",
        "accent": "#FDE047",
        "chapitres": [
            {
                "num": 13,
                "slug": "adab-priere-nuit",
                "titre": "Bonne Conduite (Adab) & Prière de Nuit",
                "versets": "v.1088 – v.1189",
                "duree": "5 min",
                "icone": "fa-star",
                "resume": "La bonne conduite représente les deux tiers de la dévotion : règles envers les parents, aînés, enfants et égaux, conduite intérieure envers Allah, puis grandeur et secrets facilitant la prière nocturne.",
                "passages": [
                    {"ref": "v.1089 – v.1094", "titre": "L'Adab : les deux tiers de la dévotion", "texte": "La meilleure parure de l'homme est la bonne conduite (al-adab) partout où il passe : les savants disent qu'elle représente près des deux tiers de la dévotion. Elle comprend une part intérieure envers Allah et une part extérieure envers les humains."},
                    {"ref": "v.1102 – v.1111", "titre": "Pardon, parents, aînés et enfants", "texte": "Pardonne à qui t'offense, donne à qui te prive, renoue avec qui t'abandonne. Honore tes parents, tes aînés et ton guide spirituel ; témoigne de pitié envers le plus jeune, et traite ton égal comme tu aimerais être traité."},
                    {"ref": "v.1114 – v.1122", "titre": "La conduite intérieure envers Allah", "texte": "Ne critique jamais le décret d'Allah, ne te tourne pas vers les créatures par convoitise ou crainte. L'aspirant qui prend l'habitude de choisir les solutions de facilité par tiédeur dans la Sharî'a ne réussira jamais."},
                    {"ref": "v.1134 – v.1149", "titre": "Grandeur de la prière de nuit", "texte": "Lève-toi quand les gens dorment : deux rak'as dans la seconde moitié de la nuit valent plus que ce bas-monde et tout ce qu'il contient. Celui qui prolonge la prière nocturne verra abrégée la longueur du Jour du Jugement."},
                    {"ref": "v.1150 – v.1174", "titre": "Ce qui facilite ou empêche le réveil nocturne", "texte": "La sobriété alimentaire, manger exclusivement licite, éviter les péchés le jour et apaiser les soucis mondains facilitent la prière de nuit. À l'inverse, un péché ou une mauvaise nourriture prive le cœur du lever nocturne."},
                ],
                "questions": [
                    {"q": "Quelle proportion de la dévotion représente la bonne conduite selon les savants (v.1092) ?", "options": ["Un dixième", "Près des deux tiers (2/3)", "Un quart", "La moitié exactement"], "answer": 1, "explication": "v.1092 : « Les hommes de science rapportent qu'elle constitue (ou peu s'en faut) les deux tiers (2/3) de la dévotion. »"},
                    {"q": "Comment faut-il traiter respectivement le plus âgé, le plus jeune et son égal (v.1106–1111) ?", "options": ["Honorer le plus âgé, avoir pitié du plus jeune, traiter son égal comme soi-même", "Traiter tout le monde avec indifférence", "Éviter les enfants", "N'honorer que les riches"], "answer": 0, "explication": "v.1106–1111 résument cette règle d'or de l'adab social."},
                    {"q": "Qu'arrive-t-il à l'aspirant qui choisit habituellement la facilité par tiédeur dans la Sharî'a (v.1122) ?", "options": ["Il progresse vite", "Il ne réussira jamais", "Il devient guide", "Il gagne en temps"], "answer": 1, "explication": "v.1122 : « L'aspirant qui prend l'habitude de choisir les facilités dans l'application de la Sharî'a ne réussira jamais. »"},
                    {"q": "Que valent deux rak'as accomplies dans la seconde moitié de la nuit (v.1138–1139) ?", "options": ["Un repas", "Plus que tout ce bas-monde et ce qu'il contient", "Une heure de repos", "Une simple habitude"], "answer": 1, "explication": "v.1138–1139 : deux rak'as dans la deuxième moitié de la nuit ont plus de valeur que ce bas-monde et tout ce qu'il contient."},
                    {"q": "Qu'ont répondu Al-Junayd et Ibn al-Qâsim interrogés en songe sur ce qui leur profitait le plus dans la tombe (v.1142–1144) ?", "options": ["Leurs grands discours", "Les rak'as priées à l'aube", "Leurs voyages", "Leurs biens"], "answer": 1, "explication": "v.1144 : « Il ne nous reste plus de récompense dans notre tombe que celle des rak'as que nous priions à l'aube. »"},
                    {"q": "Pourquoi Sufyân at-Thawrî fut-il empêché de prier la nuit pendant cinq mois (v.1154–1157) ?", "options": ["À cause d'un voyage", "Pour avoir pensé en lui-même qu'un croyant qui pleurait manquait de sincérité", "À cause du froid", "Pour avoir oublié son tapis"], "answer": 1, "explication": "v.1155–1157 montrent la gravité d'un seul mauvais soupçon envers un croyant."},
                    {"q": "Quel effet la nourriture illicite a-t-elle sur la prière de nuit (v.1165–1167) ?", "options": ["Aucun effet", "Elle assombrit le cœur et empêche de se lever la nuit pour prier", "Elle donne plus de force", "Elle améliore la voix"], "answer": 1, "explication": "v.1166–1167 : manger licite purifie le cœur ; la mauvaise nourriture empêche le réveil nocturne."},
                    {"q": "Que conseille le livre à celui qui ne peut pas se lever la nuit à cause d'un lourd sommeil (v.1175–1176) ?", "options": ["Abandonner toute prière surérogatoire", "Faire ses prières surérogatoires après Maghrib et Ishâ et s'efforcer de se lever avant l'aube", "Ne plus prier le matin", "Dormir le jour"], "answer": 1, "explication": "v.1176–1177 recommandent les surérogatoires après Maghrib et Ishâ et un réveil avant le matin."},
                ],
            },
            {
                "num": 14,
                "slug": "reconnaissance-patience",
                "titre": "Reconnaissance (Shukr) & Patience (Sabr)",
                "versets": "v.1190 – v.1317 & v.1362 – v.1384",
                "duree": "5 min",
                "icone": "fa-gem",
                "resume": "Les quatre moments essentiels du temps, les trois degrés de la reconnaissance (Shukr), les trois niveaux hiérarchiques de la patience (300, 600 et 900 degrés) et les « deux gouttes et deux gorgées » aimées d'Allah.",
                "passages": [
                    {"ref": "v.1195 – v.1203", "titre": "Gratitude envers Allah et envers l'intermédiaire", "texte": "Témoigne que tout bienfait vient uniquement d'Allah tout en remerciant sincèrement la personne qui a servi d'intermédiaire : c'est ainsi qu'on unit Haqîqa et Sharî'a. Emploie les bienfaits d'Allah dans Son obéissance."},
                    {"ref": "v.1366 – v.1368", "titre": "Les 3 degrés du Shukr", "texte": "La reconnaissance a trois degrés : le degré supérieur est d'adorer Allah par pure vénération ; le moyen par stricte obéissance ; l'inférieur pour obtenir le Paradis ou être sauvé de l'Enfer."},
                    {"ref": "v.1234 – v.1244", "titre": "Les 3 degrés du Sabr (300 · 600 · 900)", "texte": "La patience dans l'adoration et l'épreuve ('alâ) vaut 300 degrés ; résister aux tentations ('an) vaut 600 degrés ; demeurer ferme et humble dans la paix et l'aisance (fî) vaut 900 degrés : « l'homme le plus brave est celui qui patiente dans la paix et la félicité » !"},
                    {"ref": "v.1253 – v.1270", "titre": "La famille & la discrétion dans l'épreuve", "texte": "Supporter les charges de la famille avec bonté et confiance en Allah est un chemin vers Lui. Cacher sa douleur, son aumône, son adversité et sa pauvreté constitue l'un des plus précieux viatiques pour l'Au-delà."},
                    {"ref": "v.1283 – v.1313", "titre": "Épreuves purificatrices, 2 gouttes & 2 gorgées", "texte": "Allah éprouve celui qu'Il aime pour effacer ses fautes. Les viatiques les plus chers à Allah sont deux gouttes (une larme nocturne par crainte d'Allah, une goutte de sang dans Sa voie) et deux gorgées (une colère réprimée et une épreuve endurée avec patience)."},
                ],
                "questions": [
                    {"q": "Comment réunit-on Haqîqa et Sharî'a lorsqu'on reçoit un bienfait via un humain (v.1196–1198) ?", "options": ["En ne remerciant personne", "En attestant qu'Allah en est la source unique tout en remerciant l'intermédiaire humain", "En remerciant seulement l'humain", "En refusant le don"], "answer": 1, "explication": "v.1197–1198 : reconnaître Allah (Haqîqa) et remercier l'intermédiaire (Sharî'a)."},
                    {"q": "Quel est le degré supérieur de la reconnaissance (Shukr) selon le vers 1367 ?", "options": ["Adorer Allah uniquement par peur", "Adorer Allah ayant pour fin Sa stricte vénération", "Adorer Allah pour être vu", "Adorer Allah seulement dans la richesse"], "answer": 1, "explication": "v.1367 : supérieur = stricte vénération ; moyen = obéissance ; inférieur = Paradis / salut de l'Enfer."},
                    {"q": "Quels sont les trois degrés d'élévation de la patience (v.1236–1241) ?", "options": ["10, 20 et 30", "100, 200 et 300", "300 ('alâ), 600 ('an) et 900 (fî)", "50, 100 et 150"], "answer": 2, "explication": "v.1237, 1239 et 1241 : 300 degrés dans l'adoration/épreuve, 600 contre les tentations, 900 dans la paix et la félicité."},
                    {"q": "Qui est « l'homme le plus brave » selon le vers 1244 ?", "options": ["Celui qui parle fort", "Celui qui patiente dans la paix et la félicité sans se laisser griser", "Celui qui fuit les responsabilités", "Celui qui accumule le plus"], "answer": 1, "explication": "v.1244–1245 : le plus brave est celui qui reste ferme et lucide dans la paix et la félicité."},
                    {"q": "Que dit le vers 1254 au sujet de la famille ?", "options": ["Elle empêche d'adorer Allah", "Elle constitue l'un des chemins qui conduisent vers Allah Très-Haut", "Elle ne concerne pas la spiritualité", "Il faut la délaisser"], "answer": 1, "explication": "v.1254 : « La famille est à supporter, elle constitue l'un des chemins qui conduisent vers Allah Très-Haut. »"},
                    {"q": "Quelles quatre choses cacher constitue un précieux viatique pour l'Au-delà (v.1268–1269) ?", "options": ["Ses livres, ses amis, ses voyages et son nom", "La douleur, l'aumône, l'adversité et la pauvreté", "Sa prière obligatoire, son travail, sa famille et sa maison", "Son âge, sa ville, son métier et ses rêves"], "answer": 1, "explication": "v.1268 : « Cacher la douleur, l'aumône, l'adversité ainsi que la pauvreté. »"},
                    {"q": "Quelle règle courte et lumineuse résume le vers 1302 ?", "options": ["Si un bonheur arrive remercie Allah, si un malheur frappe patiente", "Ne demande rien à personne", "Ne pleure jamais", "Travaille seulement le matin"], "answer": 0, "explication": "v.1302 : « Quand un bonheur t'arrive, remercie Allah ; quand un malheur te frappe, patiente. »"},
                    {"q": "Quelles sont les deux gorgées les plus chères à Allah selon les vers 1312–1313 ?", "options": ["L'eau froide et le miel", "Une colère réprimée pour Allah et une catastrophe endurée avec longanimité", "Le lait et le thé", "Un remède amer et l'eau de pluie"], "answer": 1, "explication": "v.1312–1313 : la gorgée de la colère réprimée et celle d'une épreuve supportée avec patience."},
                ],
            },
            {
                "num": 15,
                "slug": "secrets-invocation",
                "titre": "Secrets & Moments de l'Invocation Exaucée",
                "versets": "v.1318 – v.1361",
                "duree": "4 min",
                "icone": "fa-hands-praying",
                "resume": "Toutes les conditions de perfection du Du'â (subsistance licite, louange, Salât 'alâ-n-Nabî, persévérance sans impatience), les moments bénis, les lieux sacrés et les personnes dont la prière est exaucée.",
                "passages": [
                    {"ref": "v.1318 – v.1324", "titre": "Les conditions d'un Du'â parfait", "texte": "Veille à te nourrir, te vêtir et parler dans le licite ; fais tes ablutions, prie quelques rak'as, tourne-toi vers la Kaaba, loue Allah, prie sur le Prophète (PSL) au début et à la fin, et lève les mains ouvertes avec humilité."},
                    {"ref": "v.1328 – v.1336", "titre": "Concentration, espérance et patience", "texte": "Invoque à voix basse en reconnaissant tes fautes, commence par toi-même puis prie pour la Communauté. Sois résolu, persévérant, ne dis jamais « ma prière n'a pas été exaucée », et passe les deux mains sur ton visage à la fin."},
                    {"ref": "v.1337 – v.1349", "titre": "Les moments où Allah exauce", "texte": "Le Ramadan, le jour d'Arafat, Laylat al-Qadr, le vendredi (en particulier l'heure bénie), la fin de la nuit (sahar), entre l'Adhân et l'Iqâma, aussitôt après les prières obligatoires, après la lecture du Coran, sous la pluie et dans les séances de dhikr."},
                    {"ref": "v.1350 – v.1360", "titre": "Lieux sacrés & personnes exaucées", "texte": "Les lieux sacrés (Kaaba, Multazam, Zamzam, Safâ-Marwa, Arafat, tombeaux des Prophètes et des Saints). Parmi les exaucés : le nécessiteux en détresse, la victime d'injustice, le voyageur, le jeûneur, l'enfant priant pour ses parents, le repenti et qui prie pour son frère en son absence."},
                ],
                "questions": [
                    {"q": "Quelle est la toute première condition citée au vers 1318 pour l'exaucement de l'invocation ?", "options": ["Parler très fort", "Éviter l'illicite dans la nourriture, le vêtement et la parole", "Être en groupe de cent personnes", "Attendre la nuit uniquement"], "answer": 1, "explication": "v.1318 place en tête la pureté du licite en nourriture, vêtement et parole."},
                    {"q": "Par quoi encadre-t-on l'invocation au début et à la fin (v.1322) ?", "options": ["La louange d'Allah et la prière sur le Prophète (PSL)", "Un poème profane", "Un long silence", "Un serment"], "answer": 0, "explication": "v.1322 : louange au Seigneur Miséricordieux et prière sur le Prophète au commencement et à la fin."},
                    {"q": "Par qui le fidèle doit-il commencer lorsqu'il formule ses invocations (v.1328) ?", "options": ["Par ses voisins", "Par lui-même d'abord, pour ne pas sortir les mains vides", "Par les inconnus", "Par les riches"], "answer": 1, "explication": "v.1328 : « Il commence d'abord par lui-même pour ne pas en sortir les mains vides. »"},
                    {"q": "Quelle parole faut-il absolument éviter pour ne pas gâcher son invocation (v.1333) ?", "options": ["Âmîn", "« Ma prière n'est pas exaucée » (l'impatience et le désespoir)", "Subhânallâh", "Al-Hamdulillâh"], "answer": 1, "explication": "v.1333 : « Ne sois pas pressé ou impatient et ne dis pas : ma prière n'est pas exaucée ; surtout ne désespère jamais. »"},
                    {"q": "Quel geste est recommandé après avoir achevé son invocation (v.1335) ?", "options": ["Se lever aussitôt", "Passer les deux mains sur le visage", "Frapper des mains", "Regarder vers le sol"], "answer": 1, "explication": "v.1335 : « On recommande de passer les deux mains sur le visage après l'achèvement de sa prière. »"},
                    {"q": "Lequel de ces moments figure parmi les instants d'exaucement cités aux vers 1343–1349 ?", "options": ["Entre l'Adhân et l'Iqâma, après le Coran et lors de la tombée de la pluie", "Pendant un jeu bruyant", "En cas de colère", "En dormant"], "answer": 0, "explication": "v.1343–1349 énumèrent notamment entre Adhân et Iqâma, après le Coran, sous la pluie et dans le dhikr."},
                    {"q": "Que précise le vers 1356 au sujet de la victime d'une injustice ?", "options": ["Seul un érudit est exaucé", "Sa prière est exaucée, fût-elle même un idolâtre", "Elle doit attendre un an", "Elle n'est exaucée que le vendredi"], "answer": 1, "explication": "v.1356 : « Une quelconque personne victime d'une injustice, fût-elle un idolâtre. »"},
                    {"q": "Que dit le vers 1360 sur le musulman qui prie en bien pour un frère en son absence ?", "options": ["C'est inutile", "Il compte parmi ceux dont la prière est exaucée", "Il doit le prévenir d'abord", "Cela ne compte qu'à La Mecque"], "answer": 1, "explication": "v.1360 cite « un bon musulman qui prie en bien pour un autre musulman en son absence, sans tache »."},
                ],
            },
            {
                "num": 16,
                "slug": "saints-vertus-sourates",
                "titre": "Respect des Saints & Vertus des Sourates",
                "versets": "v.1385 – v.1562",
                "duree": "5 min",
                "icone": "fa-sun",
                "resume": "Respect envers les Saints cachés parmi les hommes, discernement face aux faux guides intéressés, vertus de sourates choisies (Al-Mulk, Al-Baqara, Âyat al-Kursî, Al-Ikhlâs, Al-Kahf, Yâ-Sîn), Sayyidul-Istighfâr et épilogue béni.",
                "passages": [
                    {"ref": "v.1385 – v.1410", "titre": "Respect des Saints cachés", "texte": "Ne critique jamais les Saints d'Allah : avoir bonne conviction en eux est une grâce, les combattre mène au malheur. Ils vivent dissimulés parmi les gens, mangent et subissent les épreuves, et possèdent une lumière d'attraction et une lumière de répulsion."},
                    {"ref": "v.1432 – v.1469", "titre": "Discernement face aux faux guides", "texte": "Fuis les faux cheikhs cupides, jaloux quand on loue un autre maître et ignorants des obligations. Reste dans le juste milieu de la Sunna : « tout point lumineux n'est pas la lune, et tout ce qui éclaire la nuit n'est pas un feu qui réchauffe »."},
                    {"ref": "v.1472 – v.1476", "titre": "Ne jamais juger à l'habit", "texte": "Ne méprise jamais un serviteur d'Allah à cause de son humble vêtement : combien d'hommes en tenue modeste sont pleins de lumières et de secrets divins !"},
                    {"ref": "v.1480 – v.1519", "titre": "Vertus des Sourates du Coran", "texte": "Al-Mulk chaque nuit protège dans la tombe ; Âyat al-Kursî après chaque prière ouvre le Paradis ; Al-Ikhlâs vaut le tiers du Coran ; Al-Kahf le vendredi illumine jusqu'au vendredi suivant ; Yâ-Sîn procure le pardon des fautes."},
                    {"ref": "v.1526 – v.1562", "titre": "Sayyidul-Istighfâr, vices à fuir et Épilogue", "texte": "Récite matin et soir Sayyidul-Istighfâr. Fuis la paresse, la médisance, l'ostentation, la fierté et la jalousie. Cheikh Ahmadou Bamba clôt Masaalikul Jinaan en priant pour qu'il soit un véritable itinéraire vers le Paradis."},
                ],
                "questions": [
                    {"q": "Quelle réponse sage du savant Abd al-Wadûd est citée face aux paroles hermétiques des Saints (v.1394–1395) ?", "options": ["Il faut les condamner aussitôt", "« Je ne comprends pas les propos des Saints : moi je suis ce que je suis, et eux ce qu'ils sont »", "Elles sont toujours fausses", "Il faut les réécrire"], "answer": 1, "explication": "v.1395 enseigne l'humilité face aux propos profonds des Saints qui dépassent notre entendement."},
                    {"q": "Pourquoi Sîdî al-Mukhtâr dit-il qu'il est plus difficile de reconnaître un Saint que de connaître Allah (v.1404–1407) ?", "options": ["Parce que le Saint est dissimulé parmi les humains ordinaires, mangeant et buvant comme eux", "Parce qu'il n'y a plus de Saints", "Parce que les Saints ne parlent jamais", "Parce qu'ils vivent hors du monde"], "answer": 0, "explication": "v.1405–1407 : la Grandeur d'Allah est évidente, tandis que le Saint vit caché parmi les créatures."},
                    {"q": "À quel signe reconnaît-on un faux guide spirituel intéressé (v.1438–1444) ?", "options": ["Il se réjouit du bien des autres maîtres", "Il s'irrite quand on loue un autre cheikh et ne cherche que sa propre gloire et profit matériel", "Il enseigne la Sunna avec humilité", "Il conseille le juste milieu"], "answer": 1, "explication": "v.1438–1444 : le faux guide suffoque de jalousie si l'on loue un autre maître ; le vrai guide veut seulement le salut du disciple."},
                    {"q": "Que signifie le mot « Al-Yaqîn » dans « Adore ton Seigneur jusqu'à ce que te vienne Al-Yaqîn » (v.1462) ?", "options": ["L'âge de quarante ans", "La mort (adorer Allah jusqu'à la mort)", "La richesse", "La retraite d'un mois"], "answer": 1, "explication": "v.1462 corrige les égarés : Al-Yaqîn signifie ici la mort, jamais la dispense d'adorer Allah."},
                    {"q": "Quel conseil donne le vers 1465–1466 sur la meilleure voie ?", "options": ["L'extrémisme", "Rester dans le juste milieu suivant la Tradition prophétique (Sunna)", "L'isolement complet sans loi", "Suivre toutes les apparences"], "answer": 1, "explication": "v.1465–1466 : être juste dans la Sunna constitue le point culminant de la vertu."},
                    {"q": "Quelle sourate lue chaque nuit protège des frayeurs de la tombe (v.1480) ?", "options": ["Al-Mulk (S.67)", "Al-Fîl (S.105)", "Al-Kawthar (S.108)", "Al-Masad (S.111)"], "answer": 0, "explication": "v.1480 : « La lecture de la sourate Al-Mulk (S.67) chaque nuit préserve l'homme de toute frayeur dans la tombe. »"},
                    {"q": "À quelle fraction du Coran équivaut la sourate Al-Ikhlâs (S.112) selon le vers 1504 ?", "options": ["Un dixième", "Un quart", "Un tiers (1/3)", "La moitié"], "answer": 2, "explication": "v.1504 : « La sourate Al-Ikhlâs (S.112) équivaut au tiers du Coran. »"},
                    {"q": "Quel bienfait procure la lecture de la sourate Al-Kahf (S.18) le vendredi (v.1516–1518) ?", "options": ["Elle illumine le lecteur jusqu'au vendredi suivant", "Elle dispense des prières", "Elle se lit seulement la nuit", "Elle dure trois jours"], "answer": 0, "explication": "v.1518 : « Si on la lit un vendredi, elle illumine jusqu'au vendredi suivant au profit du lecteur. »"},
                ],
            },
        ],
    },
]


def get_all_chapitres():
    """Retourne la liste ordonnée des 16 chapitres avec métadonnées de leur Porte."""
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


def build_duolingo_deck(chapitre):
    """
    Construit un parcours fluide étape par étape calibré pour petit écran mobile :
    alterne 1 passage court du livre + 1 à 2 questions intermédiaires fidèles au texte,
    puis le résumé objectif du chapitre et les questions finales.
    """
    deck = []
    passages = chapitre.get("passages", [])
    questions = chapitre.get("questions", [])

    # Carte d'ouverture légère (contexte du chapitre)
    deck.append({
        "type": "intro",
        "tag": f"Chapitre {chapitre['num']} · {chapitre['versets']}",
        "titre": chapitre["titre"],
        "texte": chapitre["resume"],
        "meta": f"{len(passages)} étapes de lecture · {len(questions)} questions intermédiaires",
    })

    # Entrelacer passages courts & questions intermédiaires de façon fluide
    q_idx = 0
    total_p = max(1, len(passages))
    for p_idx, p in enumerate(passages):
        deck.append({
            "type": "passage",
            "tag": f"Masaalikul Jinaan · {p['ref']}",
            "titre": p["titre"],
            "texte": p["texte"],
        })
        # Nombre de questions à intercaler après ce passage
        target_q_done = round(((p_idx + 1) / total_p) * len(questions))
        while q_idx < target_q_done and q_idx < len(questions):
            q = questions[q_idx]
            deck.append({
                "type": "question",
                "q_num": q_idx + 1,
                "q_total": len(questions),
                "question": q["q"],
                "options": q["options"],
                "answer": q["answer"],
                "explication": q["explication"],
            })
            q_idx += 1

    while q_idx < len(questions):
        q = questions[q_idx]
        deck.append({
            "type": "question",
            "q_num": q_idx + 1,
            "q_total": len(questions),
            "question": q["q"],
            "options": q["options"],
            "answer": q["answer"],
            "explication": q["explication"],
        })
        q_idx += 1

    return deck
