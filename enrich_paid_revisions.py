# -*- coding: utf-8 -*-
"""
Développement complet du contenu pédagogique des Révisions Payantes (id=33..38)
de Tazawwudu-ç-Çighâr (Le Viatique des Adolescents - Cheikh Ahmadou Bamba) :
- Dossiers de synthèse complets (Mushaf des vers clés, Fiche méthodologique & Cas pratiques, 8-10 Cartes Mémo d'Or)
- 90 nouvelles questions intensives vérifiées (15 par chapitre x 5 chapitres + 15 questions de synthèse générale)
  couvrant les 4 formats : QCM de cas pratiques, Vrai/Faux, Associations, Réponses courtes.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import TazawwudModule, TazawwudLecon, TazawwudQuestion, TazawwudChoix


DOSSIERS_REVISIONS = {
    33: {  # Chapitre 1 (Module 1, numero=10)
        "titre": "Révision Intensive : Chapitre 1 (Al-Imân & At-Tawhîd)",
        "texte_source": (
            "﴿ مَجمُوعُ الآيَاتِ وَالأَبيَاتِ المِفتَاحِيَّةِ لِلبَابِ الأَوَّلِ ﴾\n\n"
            "• النِّيَّةُ وَالإِخلاَصُ (Vers 1-14) :\n"
            "قَالَ الشَّيخُ أَحمَدُ بَامبَا خَادِمُ الرَّسُولِ ﷺ :\n"
            "« يَا نَاشِئًا أَقبِلْ إِلَى التَّزَوُّدِ ... فِي الصِّغَرِ تَحظَ بِأَعلَى السُّؤدُدِ »\n"
            "Jeunesse ! Accours vers le viatique dès le bas âge, tu atteindras ainsi la plus haute noblesse dans les deux mondes.\n\n"
            "• أَركَانُ الدِّينِ الثَّلاَثَةُ (Vers 15-21) :\n"
            "La Religion (Ad-Dîn) repose sur trois fondements indissociables : Al-Imân (la Foi du cœur), Al-Islâm (la soumission des membres par les œuvres) et Al-Ihsân (la perfection spirituelle).\n\n"
            "• عِلمُ التَّوحِيدِ : ٤١ حُكمًا عَقلِيًّا (Vers 22-48) :\n"
            "Il incombe à toute personne responsable (Mukallaf) de connaître :\n"
            "- 20 Attributs nécessaires (Wâjib) à Allah : Al-Wujûd (l'Existence), Al-Qidam (l'Antériorité sans début), Al-Baqâ' (la Pérennité sans fin), Al-Mukhâlafatu lil-hawâdith (la Dissemblance absolue d'avec le créé), Al-Qiyâmu bi-nafsihi (l'Autosuffisance), Al-Wahdâniyyah (l'Unicité dans l'Essence, les Attributs et les Actes), Al-Qudrah (la Toute-Puissance), Al-Irâdah (la Volonté), Al-'Ilm (l'Omniscience), Al-Hayât (la Vie), As-Sam' (l'Ouïe), Al-Basar (la Vue), Al-Kalâm (la Parole sans lettre ni voix) et les 7 états qualificatifs correspondants.\n"
            "- 20 contraires impossibles (Mustahîl) à Son sujet : le néant ('Adam), la contingence (Hudûth), l'extinction (Fanâ'), la ressemblance au créé (Mumâthalah), le besoin d'autrui (Iftiqâr), la multiplicité (Ta'addud), l'impuissance ('Ajz), la contrainte (Karâhah), l'ignorance (Jahl), la mort (Mawt), la surdité (Samam), la cécité ('Amâ), le mutisme (Bakam)...\n"
            "- 1 Attribut possible (Jâ'iz) : Faire exister ou laisser dans le néant tout être contingent (Fî'lu kulli mumkinin aw tarkuhu).\n\n"
            "• سِتَّةُ أَركَانِ الإِيمَانِ (Vers 49-92) :\n"
            "1. Croire en Allah.\n"
            "2. Croire en Ses Anges (créés de lumière, impeccables, ni mâles ni femelles), dont les 10 illustres : Jibrîl (Révélation), Mîkâ'îl (pluie et subsistance), Isrâfîl (Trompe), 'Izrâ'îl (recueil des âmes), Munkar et Nakîr (interrogatoire de la tombe), Raqîb et 'Atîd (scribes des œuvres), Ridwân (gardien du Paradis) et Mâlik (gardien de l'Enfer).\n"
            "3. Croire aux 104 Livres révélés : 100 Feuillets (Suhuf : 10 à Âdam, 50 à Shîth, 30 à Idrîs, 10 à Ibrâhîm) et 4 Grands Livres (Tawrât à Mûsâ, Zabûr à Dâwûd, Injîl à 'Îsâ, Furqân/Coran à Muhammad ﷺ).\n"
            "4. Croire aux Envoyés (Rusul) et à leurs 9 statuts : 4 qualités nécessaires (Sidq/Véracité, Amânah/Fidélité, Tablîgh/Transmission, Fatânah/Sagacité), 4 défauts impossibles (Mensonge, Trahison, Dissimulation, Stupidité) et 1 statut possible (les accidents humains non avilissants comme la maladie, la faim ou le mariage).\n"
            "5. Croire au Jour Ultime (Résurrection, Rassemblement, Balance, Pont Sirât, Intercession, Bassin Kawthar, Paradis et Enfer).\n"
            "6. Croire au Décret Divin (Al-Qadâ' wal-Qadar), bon ou éprouvant, tout en fournissant l'effort d'obéissance."
        ),
        "explication": (
            "DOSSIER DE SYNTHÈSE INTENSIVE — CHAPITRE 1 (VERS 1 À 92) :\n\n"
            "1. TABLEAU RÉCAPITULATIF DES CHIFFRES CLÉS DU DOGME ('AQÎDAH) :\n"
            "• 3 Piliers de la Religion : Imân (Foi intérieure), Islâm (Pratique extérieure), Ihsân (Excellence spirituelle).\n"
            "• 41 Statuts rationnels concernant Allah : 20 Nécessaires (Wâjib) + 20 Impossibles (Mustahîl) + 1 Possible (Jâ'iz).\n"
            "• 9 Statuts concernant les Messagers : 4 Nécessaires + 4 Impossibles + 1 Possible (Total du Dogme = 41 + 9 = 50 articles de la Shahâdah).\n"
            "• 6 Articles de la Foi (Arkân al-Imân) : Allah, les Anges, les Livres, les Messagers, le Jour Dernier, le Décret Divin.\n"
            "• 10 Anges à connaître nominalement : Jibrîl, Mîkâ'îl, Isrâfîl, 'Izrâ'îl, Munkar, Nakîr, Raqîb, 'Atîd, Ridwân, Mâlik.\n"
            "• 104 Livres Célestes : 10 Feuillets (Âdam) + 50 Feuillets (Shîth) + 30 Feuillets (Idrîs) + 10 Feuillets (Ibrâhîm) + Tawrât (Mûsâ) + Zabûr (Dâwûd) + Injîl ('Îsâ) + Al-Furqân (Muhammad ﷺ).\n\n"
            "2. CLASSIFICATION DES 20 ATTRIBUTS D'ALLAH (MÉTHODE TRADITIONNELLE) :\n"
            "• Attribut Essentiel (Sifah Nafsiyyah - 1) : Al-Wujûd (l'Existence).\n"
            "• Attributs de Transcendance / Négatifs (Sifât Salbiyyah - 5) : Al-Qidam, Al-Baqâ', Al-Mukhâlafatu lil-hawâdith, Al-Qiyâmu bi-nafsihi, Al-Wahdâniyyah.\n"
            "• Attributs de Signification (Sifât al-Ma'ânî - 7) : Al-Qudrah, Al-Irâdah, Al-'Ilm, Al-Hayât, As-Sam', Al-Basar, Al-Kalâm.\n"
            "• Attributs Qualificatifs (Sifât Ma'nawiyyah - 7) : Le fait qu'Allah soit Tout-Puissant (Qâdiran), Voulant (Murîdan), Omniscient ('Âliman), Vivant (Hayyan), Entendant (Samî'an), Voyant (Basîran), Parlant (Mutakalliman).\n\n"
            "3. PIÈGES À ÉVITER LORS DE L'ÉPREUVE INTENSIVE :\n"
            "• Ne pas confondre le nombre de feuillets d'Ibrâhîm (10 Suhuf) et d'Idrîs (30 Suhuf), ni les 50 Suhuf de Shîth.\n"
            "• Se rappeler que qualifier les Anges de sexe masculin est une transgression grave, et les qualifier de sexe féminin est une mécréance (Kufr) car cela contredit frontalement le Coran.\n"
            "• Savoir que le Décret Divin (Al-Qadar) n'annule jamais la responsabilité morale : l'être humain est jugé sur ses choix et ses efforts d'obéissance."
        ),
        "a_retenir": (
            "- L'intention pure (Ikhlâs) pour la Face d'Allah est la condition d'acceptation de toute étude et de toute œuvre\n"
            "- La Religion (Ad-Dîn) est un édifice à 3 piliers : Al-Imân (racines), Al-Islâm (tronc et branches) et Al-Ihsân (fruits)\n"
            "- Le Tawhîd compte 41 statuts pour Allah : 20 Attributs nécessaires, 20 contraires impossibles et 1 statut possible\n"
            "- La Parole d'Allah (Al-Kalâm) est éternelle, sans lettre ni voix, et ne ressemble aucunement à la parole des créatures\n"
            "- Les 10 Anges illustres ont chacun une fonction précise (Jibrîl : Révélation, Mîkâ'îl : pluie, Isrâfîl : Trompe, 'Izrâ'îl : âmes, Ridwân : Paradis, Mâlik : Enfer)\n"
            "- Les 104 Livres révélés se répartissent en 100 Suhuf (10 Âdam, 50 Shîth, 30 Idrîs, 10 Ibrâhîm) et 4 Grands Livres (Tawrât, Zabûr, Injîl, Furqân)\n"
            "- Les Prophètes possèdent 4 qualités nécessaires : Sidq (Véracité), Amânah (Fidélité), Tablîgh (Transmission), Fatânah (Sagacité)\n"
            "- Les accidents humains (maladie, faim, sommeil) sont possibles chez les Prophètes pour élever leur rang et servir d'exemple\n"
            "- Les réalités du Jour Ultime incluent l'interrogatoire de la tombe, le Rassemblement, la Balance (Mîzân), le Pont (Sirât) et le Bassin (Kawthar)\n"
            "- Croire au Décret Divin (Al-Qadar) apporte la sérénité face aux épreuves tout en exigeant l'effort constant dans l'obéissance"
        ),
    },
    34: {  # Chapitre 2 (Module 2, numero=6)
        "titre": "Révision Intensive : Chapitre 2 (Al-Islâm I & Pureté de l'Âme)",
        "texte_source": (
            "﴿ مَجمُوعُ الأَبيَاتِ المِفتَاحِيَّةِ لِلبَابِ الثَّانِي ﴾\n\n"
            "• أَركَانُ الإِسلاَمِ الخَمسَةُ وَفَضلُ الشَّهَادَةِ (Vers 93-114) :\n"
            "L'Islâm est bâti sur cinq piliers : le témoignage qu'il n'y a de divinité qu'Allah et que Muhammad ﷺ est Son Messager (Lâ ilâha illâ Allâh, Muhammadun Rasûlullâh), l'accomplissement des cinq prières quotidiennes, l'acquittement de la Zakat, le jeûne du mois de Ramadan et le Pèlerinage à la Maison Sacrée pour qui en a la capacité.\n"
            "La formule « Lâ ilâha illâ Allâh » est le meilleur Dhikr : elle renferme les 50 articles du dogme (41 pour Allah + 9 pour les Messagers).\n\n"
            "• الصَّلَوَاتُ الخَمسُ وَالطَّهَارَةُ الشَّرعِيَّةُ (Vers 115-133) :\n"
            "Les 5 prières prescrites sont : As-Subh (Fajr), Az-Zuhr, Al-'Asr, Al-Maghrib et Al-'Ichâ'.\n"
            "Leur validité requiert 4 conditions de pureté :\n"
            "1. La pureté de l'âme (sincérité pour Allah seul, sans ostentation).\n"
            "2. La pureté du corps (absence de souillure mineure ou majeure et d'impureté matérielle).\n"
            "3. La pureté des vêtements.\n"
            "4. La pureté du lieu de prière.\n"
            "Et l'eau pure et purifiante (Al-Mâ' al-Mutlaq) est celle qui n'a subi aucune altération de sa couleur, de son goût ou de son odeur par une substance impure ou étrangère.\n\n"
            "• حِفظُ الجَوَارِحِ السَّبعِ وَالتَّوبَةُ النَّصُوحُ (Vers 134-155) :\n"
            "Préserve tes 7 membres contre la désobéissance : la langue (mensonge, médisance Ghîbah, calomnie Namîmah), les oreilles, les yeux, le ventre (nourriture illicite et usure), les mains, les pieds et le sexe.\n"
            "Le repentir sincère (At-Tawbah) exige 3 conditions immédiates (et une 4e envers autrui) :\n"
            "1. Cesser immédiatement le péché.\n"
            "2. Éprouver un regret sincère dans le cœur.\n"
            "3. Prendre la ferme résolution de ne plus jamais y retomber.\n"
            "4. Réparer les torts commis envers les créatures (rendre le bien ou demander pardon).\n\n"
            "• التَّميِيزُ بَينَ الفَرضِ وَالسُّنَّةِ (Vers 156-163) :\n"
            "Il est interdit d'agir dans l'adoration sans science : le croyant doit impérativement distinguer l'Obligatoire (Fard) du Traditionnel (Sunnah)."
        ),
        "explication": (
            "DOSSIER DE SYNTHÈSE INTENSIVE — CHAPITRE 2 (VERS 93 À 163) :\n\n"
            "1. TABLEAU RÉCAPITULATIF DES REPÈRES DU CHAPITRE 2 :\n"
            "• 5 Piliers de l'Islâm : Shahâdah, Salât (5 prières), Zakat, Sawm Ramadan, Hajj.\n"
            "• 3 Critères de l'eau pure et purifiante (Mâ' Tahûr) : Couleur (Lawn), Goût (Ta'm), Odeur (Rîh) non altérés.\n"
            "• 4 Conditions de pureté pour la prière : Pureté de l'intention/cœur + Pureté du corps + Pureté de l'habit + Pureté du lieu.\n"
            "• 7 Membres du corps (Al-Jawârih as-Sab'ah) à garder : 1. La Langue, 2. Les Oreilles, 3. Les Yeux, 4. Le Ventre, 5. Les Mains, 6. Les Pieds, 7. Le Sexe.\n"
            "• 3 Conditions de la Tawbah (envers Allah) + 1 Condition supplémentaire (envers les créatures : restitution des droits).\n\n"
            "2. FOCUS ÉTHIQUE : LA GARDE DU VENTRE ET DE LA LANGUE :\n"
            "• Cheikh Ahmadou Bamba insiste sur le fait que la pureté extérieure (eau) est vaine si l'intérieur est souillé par la nourriture illicite (Harâm) ou la médisance (Ghîbah).\n"
            "• Consommer de l'illicite voile le cœur et empêche l'exaucement des invocations (Du'â).\n\n"
            "3. DIFFÉRENCE JURIDIQUE ENTRE FARD ET SUNNAH DANS LES ACTES D'ADORATION :\n"
            "• Le Fard (Obligation divine) est un pilier : son omission volontaire annule l'acte, et son oubli dans la prière ne se répare pas par une simple prosternation de l'oubli (il faut refaire le pilier omis).\n"
            "• La Sunnah (Tradition prophétique) parachève l'acte et procure une immense récompense ainsi que l'amour du Prophète ﷺ."
        ),
        "a_retenir": (
            "- Les 5 piliers de l'Islâm sont la Shahâdah, les 5 Prières, la Zakat, le Jeûne de Ramadan et le Hajj\n"
            "- « Lâ ilâha illâ Allâh » est la meilleure évocation (Dhikr) et résume les 50 articles de foi\n"
            "- Les 5 prières prescrites à heures fixes sont Subh, Zuhr, 'Asr, Maghrib et 'Ichâ'\n"
            "- La prière exige 4 puretés : celle de l'âme (sincérité), du corps, des vêtements et du lieu\n"
            "- L'eau pure et purifiante (Tahûr) est celle dont ni la couleur, ni le goût, ni l'odeur n'ont été altérés\n"
            "- Les 7 membres à préserver du péché sont : la langue, les oreilles, les yeux, le ventre, les mains, les pieds et le sexe\n"
            "- Le repentir sincère (Tawbah) réunit : l'arrêt immédiat du péché, le regret du cœur, la résolution de ne plus recommencer et la réparation des torts\n"
            "- La science précède l'action : tout croyant doit savoir distinguer le Fard (obligatoire) de la Sunnah (tradition)"
        ),
    },
    35: {  # Chapitre 3 (Module 3, numero=5)
        "titre": "Révision Intensive : Chapitre 3 (La Prière & les 3 Purifications)",
        "texte_source": (
            "﴿ مَجمُوعُ الأَبيَاتِ المِفتَاحِيَّةِ لِلبَابِ الثَّالِثِ — الفِقهُ المَالِكِيُّ ﴾\n\n"
            "• فَرَائِضُ الصَّلاَةِ الخَمسَةَ عَشَرَ (15 Obligations de la Prière - Vers 164-175) :\n"
            "1. L'intention (An-Niyyah) ; 2. Le Takbîr al-Ihrâm (« Allâhu Akbar » inaugural) ; 3. Se tenir debout (Al-Qiyâm) pour ce Takbîr ; 4. La récitation de la Fâtihah ; 5. Se tenir debout pour la Fâtihah ; 6. L'inclinaison (Ar-Rukû') ; 7. Le redressement après l'inclinaison (Ar-Raf' minhu) ; 8. La prosternation (As-Sujûd sur le front) ; 9. Le relèvement entre les deux prosternations ; 10. L'assise pour le Salut final ; 11. Le Salut final (« As-salâmu 'alaykum ») ; 12. L'accalmie / sérénité (At-Tuma'nînah) ; 13. L'équilibre / rectitude (Al-I'tidâl) ; 14. L'ordre séquentiel des actes (At-Tartîb) ; 15. L'intention de suivre l'Imam (pour le prieur dirigé).\n\n"
            "• سُنَنُ الصَّلاَةِ الثَّمَانِيَةَ عَشَرَ وَالمُؤَكَّدَاتُ الثَّمَانِي (18 Sunan dont 8 Mu'akkadah - Vers 176-186) :\n"
            "Les 8 Sunnah Mu'akkadah (fortement recommandées : « سَبِّحْ سَمِعَ شَهِدَ أَجمِعْ وَأَعلِنِ ») :\n"
            "1. La Sourate après la Fâtihah ; 2. Se tenir debout pour cette Sourate ; 3. La récitation à voix haute (Jahr) là où elle est prescrite ; 4. La récitation à voix basse (Sirr) là où elle est prescrite ; 5. Tous les Takbîr autres que le Takbîr al-Ihrâm ; 6. Dire « Sami'a Allâhu liman hamidah » ; 7. Le premier Tashahhud ; 8. Le second Tashahhud (et leurs assises).\n\n"
            "• الوُضُوءُ وَالغُسلُ وَالتَّيَمُّمُ (Vers 187-205) :\n"
            "- Ablutions mineures (Wudû') : 7 Obligations (Intention, lavage du visage, lavage des mains/avant-bras jusqu'aux coudes, essuyage de toute la tête, lavage des pieds jusqu'aux chevilles, frottement Dalk, continuité Faur) + 8 Traditions (laver les mains au début, rincer la bouche Madmadah, inspirer l'eau Istinshâq, rejeter l'eau Istinthâr, essuyer les oreilles, renouveler l'eau pour les oreilles, retour des mains dans l'essuyage de la tête, ordre des actes).\n"
            "- Purification majeure (Ghusl) : 5 Obligations (Intention, laver tout le corps sans exception, frottement Dalk, continuité Faur, démêler les cheveux/poils Takhlîl) + 4 Traditions (laver les mains 3 fois au début, rincer la bouche, inspirer l'eau, essuyer l'intérieur des oreilles).\n"
            "- Lustral pulvérulent (Tayammum) : 8 Obligations (Intention, support minéral pur Sa'îd, première frappe, essuyer tout le visage, essuyer les mains jusqu'aux poignets, continuité Faur, accomplissement après l'entrée de l'heure, liaison immédiate à la prière) + 3 Traditions (ordre entre visage et mains, seconde frappe pour les mains, essuyer des poignets jusqu'aux coudes)."
        ),
        "explication": (
            "DOSSIER DE SYNTHÈSE INTENSIVE — CHAPITRE 3 (VERS 164 À 205) :\n\n"
            "1. TABLEAU COMPARATIF DES CHIFFRES DU FIQH (SELON AL-'AWFÎ) :\n"
            "• La Prière (As-Salât) : 15 Obligations (Farâ'id) | 18 Traditions (Sunan) dont 8 Sunnah Mu'akkadah.\n"
            "• Les Ablutions (Al-Wudû') : 7 Obligations (Farâ'id) | 8 Traditions (Sunan).\n"
            "• Le Bain rituel (Al-Ghusl) : 5 Obligations (Farâ'id) | 4 Traditions (Sunan).\n"
            "• Le Tayammum : 8 Obligations (Farâ'id) | 3 Traditions (Sunan).\n\n"
            "2. RÈGLES D'OR DU FIQH MALIKITE À MAÎTRISER POUR L'EXAMEN :\n"
            "• Dans la Prière : La Fâtihah et le Takbîr al-Ihrâm sont des Farâ'id (piliers) ; la Sourate après la Fâtihah, le Tashahhud et « Sami'a Allâhu liman hamidah » sont des Sunnah Mu'akkadah.\n"
            "• Dans le Wudû' et le Ghusl : Le frottement (Ad-Dalk : passer la main sur le membre avec l'eau) et la continuité (Al-Faur / Al-Muwâlât : enchaîner sans laisser sécher) sont des OBLIGATIONS (Farâ'id) en rite malikite !\n"
            "• Dans le Tayammum : L'essuyage obligatoire des mains s'arrête aux POIGNETS (Kû'ayn), tandis que prolonger l'essuyage des poignets jusqu'aux COUDES (Mirfaqayn) ainsi que la seconde frappe sont des Sunan !"
        ),
        "a_retenir": (
            "- La Prière compte 15 actes obligatoires (Farâ'id) dont l'intention, le Takbîr al-Ihrâm, la Fâtihah, le Rukû', le Sujûd, le Salâm final, la Tuma'nînah et l'I'tidâl\n"
            "- La Prière compte 18 actes traditionnels (Sunan), parmi lesquels 8 sont des Sunnah Mu'akkadah (Sourate, Jahr, Sirr, Takbîrs secondaires, Sami'a Allâhu liman hamidah, 1er et 2e Tashahhud)\n"
            "- Un pilier (Fard) oublié dans la prière ne se répare pas par une simple prosternation de l'oubli : il doit obligatoirement être accompli\n"
            "- Les Ablutions (Wudû') comprennent 7 obligations : intention, visage, bras jusqu'aux coudes, tête entière, pieds jusqu'aux chevilles, frottement (Dalk) et continuité (Faur)\n"
            "- Les Ablutions comprennent 8 traditions : laver les mains au début, rincer la bouche, inspirer/rejeter l'eau par le nez, essuyer les oreilles (et renouveler l'eau), retour de l'essuyage de la tête et ordre\n"
            "- Le Ghusl (grande purification) compte 5 obligations : intention, laver tout le corps, frottement (Dalk), continuité (Faur) et démêlage des cheveux (Takhlîl)\n"
            "- Le Tayammum compte 8 obligations (dont 1re frappe, visage, mains aux poignets, entrée de l'heure, liaison à la prière) et 3 traditions (ordre, 2e frappe, essuyer jusqu'aux coudes)\n"
            "- Le Tayammum s'effectue sur un support minéral pur (Sa'îd Tâhir : terre, sable, pierre non calcinée) en cas d'absence d'eau ou de risque médical"
        ),
    },
    36: {  # Chapitre 4 (Module 4, numero=5)
        "titre": "Révision Intensive : Chapitre 4 (Jeûne, Zakat, Hajj & Al-Masbûq)",
        "texte_source": (
            "﴿ مَجمُوعُ الأَبيَاتِ المِفتَاحِيَّةِ لِلبَابِ الرَّابِعِ ﴾\n\n"
            "• الصَّومُ وَالزَّكَاةُ وَالحَجُّ (Vers 206-225) :\n"
            "- Le Jeûne (As-Sawm) : 2 Obligations (1. L'intention nocturne avant l'aube ; 2. L'abstinence de l'aube Fajr au coucher du soleil Maghrib de nourriture, boisson et rapports conjugaux) + 3 Traditions (1. Hâter la rupture Ta'jîl al-Fitr ; 2. Retarder le repas de l'aube Ta'khîr as-Suhûr ; 3. Garder sa langue de toute parole vaine).\n"
            "- La Zakat : 4 Obligations (1. Intention ; 2. Atteinte du seuil imposable Nisâb ; 3. Écoulement d'une année lunaire Hawl pour bétail/monnaie ou maturité pour récoltes ; 4. Distribution aux 8 catégories sans transfert indu) + 3 Traditions (1. Acquittement de bon cœur ; 2. Qualité moyenne du bien donné ; 3. Discrétion sans reproche aux pauvres).\n"
            "- Le Pèlerinage (Al-Hajj) : 4 Piliers Obligatoires (1. L'Ihrâm avec intention ; 2. La station à 'Arafah le 9 Dhû al-Hijjah ; 3. Le Tawâf al-Ifâdah autour de la Ka'bah ; 4. Le Sa'y entre Safâ et Marwah) + 12 Traditions.\n\n"
            "• أَحكَامُ المَسبُوقِ فِي الصَّلَوَاتِ الخَمسِ (Rattrapage derrière l'Imam - Vers 226-263) :\n"
            "- Règle de validation de la Rak'ah : Quiconque rejoint l'Imam dans l'inclinaison (Ar-Rukû') avant que celui-ci ne se redresse a validé la Rak'ah entière.\n"
            "- Règle générale du Masbûq après le Salâm de l'Imam : Il applique le Qadâ' (réparation) pour les paroles (Fâtihah et Sourate) et le Binâ' (continuité) pour les actes (position assise du Tashahhud).\n"
            "- Cas détaillés par prière :\n"
            "  * Subh (2 Rak'ah) : S'il manque la 1re Rak'ah, il se lève après le Salâm de l'Imam et accomplit sa Rak'ah restante avec Fâtihah et Sourate à voix haute (sans Qunût s'il l'a déjà fait avec l'Imam).\n"
            "  * Zuhr et 'Asr (4 Rak'ah à voix basse) : S'il manque 1 Rak'ah, il en fait 1 avec Fâtihah + Sourate ; s'il manque 2 Rak'ah, il en fait 2 avec Fâtihah + Sourate ; s'il manque 3 Rak'ah, il en fait 1 avec Fâtihah + Sourate, s'assoit pour son Tashahhud médian, puis fait 1 avec Fâtihah + Sourate, puis 1 avec Fâtihah seule.\n"
            "  * Maghrib (3 Rak'ah : 2 à voix haute + 1 à voix basse) : S'il manque 1 Rak'ah (il en a prié 2 avec l'Imam), il se lève et fait 1 Rak'ah avec Fâtihah + Sourate à voix haute ! S'il manque 2 Rak'ah (il n'a eu que la 3e avec l'Imam), il se lève, fait 1 Rak'ah avec Fâtihah + Sourate à voix haute, s'assoit pour le Tashahhud (car c'est sa 2e Rak'ah en actes - Binâ' !), puis se lève et fait 1 Rak'ah avec Fâtihah + Sourate à voix haute.\n"
            "  * 'Ichâ' (4 Rak'ah : 2 à voix haute + 2 à voix basse) : S'il manque 1 ou 2 Rak'ah, il les accomplit avec Fâtihah + Sourate à voix haute ; s'il manque 3 Rak'ah (il n'a eu que la 4e avec l'Imam), il se lève, fait 1 Rak'ah avec Fâtihah + Sourate à voix haute, s'assoit pour le Tashahhud médian, puis se lève pour 1 Rak'ah avec Fâtihah + Sourate à voix haute, puis 1 dernière Rak'ah avec Fâtihah seule à voix basse !\n\n"
            "• صَلاَةُ المَرِيضِ (La Prière du Malade - Vers 264-273) :\n"
            "Ordre de priorité selon la capacité : 1. Debout (autonome, puis appuyé) ; 2. Assis (autonome, puis appuyé) ; 3. Allongé sur le côté droit (puis gauche) face à la Qiblah ; 4. Allongé sur le dos, les pieds orientés vers la Qiblah."
        ),
        "explication": (
            "DOSSIER DE SYNTHÈSE INTENSIVE — CHAPITRE 4 (VERS 206 À 273) :\n\n"
            "1. TABLEAU RÉCAPITULATIF DES PILIERS (JEÛNE, ZAKAT, HAJJ) :\n"
            "• Jeûne (Sawm) : 2 Obligations + 3 Traditions.\n"
            "• Aumône Légale (Zakat) : 4 Obligations + 3 Traditions.\n"
            "• Pèlerinage (Hajj) : 4 Obligations + 12 Traditions.\n\n"
            "2. LA CLÉ D'OR POUR RÉSOUDRE TOUS LES CAS PRATIQUES D'AL-MASBÛQ :\n"
            "• Principe malikite : « Qadâ' fî al-Aqwâl, Binâ' fî al-Af'âl » :\n"
            "  - Pour la RÉCITATION (les paroles) : Ce que le retardataire rattrape est considéré comme le DÉBUT de sa prière (les 1re et 2e Rak'ah manquées). Il y récite donc Fâtihah + Sourate (à voix haute pour Subh, Maghrib et 'Ichâ' ; à voix basse pour Zuhr et 'Asr).\n"
            "  - Pour l'ASSISE DU TASHAHHUD (les actes) : Ce qu'il fait après l'Imam est la SUITE du nombre de Rak'ah déjà priées avec l'Imam. Il s'assoit donc pour le Tashahhud chaque fois que son compteur total de Rak'ah atteint 2 !\n"
            "• Exemple classique d'examen (Maghrib avec 2 Rak'ah manquées) : Le fidèle a prié 1 Rak'ah avec l'Imam (la 3e de l'Imam). Quand l'Imam fait le Salâm, le fidèle se lève, accomplit 1 Rak'ah avec Fâtihah + Sourate à voix haute -> son total atteint 2 Rak'ah (1 avec l'Imam + 1 seul), donc il S'ASSOIT pour le Tashahhud, puis il se lève et accomplit sa dernière Rak'ah avec Fâtihah + Sourate à voix haute !"
        ),
        "a_retenir": (
            "- Le Jeûne comporte 2 obligations (intention nocturne et abstinence de l'aube au coucher) et 3 traditions (hâter l'Iftâr, retarder le Suhûr, garder sa langue)\n"
            "- La Zakat comporte 4 obligations (intention, Nisâb, Hawl/échéance, remise aux ayants droit sans transfert indu) et 3 traditions\n"
            "- Le Hajj repose sur 4 piliers obligatoires (Ihrâm, station à 'Arafah, Tawâf al-Ifâdah, Sa'y entre Safâ et Marwah) et 12 traditions\n"
            "- La Rak'ah avec l'Imam est validée si le fidèle s'incline (Rukû') avant que l'Imam ne relève la tête de l'inclinaison\n"
            "- Le Masbûq répare les paroles comme le début de sa prière (Qadâ' : Fâtihah + Sourate) et poursuit les actes comme la suite de sa prière (Binâ' : assise du Tashahhud toutes les 2 Rak'ah)\n"
            "- À Maghrib, celui qui a manqué les 2 premières Rak'ah fait 1 Rak'ah (Fâtihah + Sourate à voix haute), s'assoit pour le Tashahhud, puis fait 1 Rak'ah (Fâtihah + Sourate à voix haute)\n"
            "- À 'Ichâ', celui qui a manqué les 3 premières Rak'ah fait 1 Rak'ah (Fâtihah + Sourate à voix haute), s'assoit pour le Tashahhud, puis fait 1 Rak'ah (Fâtihah + Sourate à voix haute), puis 1 Rak'ah (Fâtihah seule à voix basse)\n"
            "- Le malade prie selon sa capacité dans cet ordre strict : debout, puis assis, puis sur le côté (droit puis gauche), puis sur le dos"
        ),
    },
    37: {  # Chapitre 5 (Module 5, numero=4)
        "titre": "Révision Intensive : Chapitre 5 (Al-Ihsân, Vertus & Sagesse Finale)",
        "texte_source": (
            "﴿ مَجمُوعُ الأَبيَاتِ المِفتَاحِيَّةِ لِلبَابِ الخَامِسِ — الإِحسَانُ وَالتَّصَوُّفُ ﴾\n\n"
            "• مَقَامُ الإِحسَانِ (Vers 274-280) :\n"
            "L'Ihsân consiste à adorer Allah comme si tu Le voyais (degré de la contemplation : Al-Mushâhadah), car même si tu ne Le vois pas, Lui te voit assurément (degré de la vigilance : Al-Murâqabah).\n"
            "Il ne saurait y avoir d'Ihsân authentique sans la rectitude préalable de l'Imân (la Foi) et de l'Islâm (la Loi).\n\n"
            "• التَّحَلِّي بِالفَضَائِلِ وَصُحبَةُ الشَّيخِ المُرَبِّي (Vers 281-294) :\n"
            "Pare ton âme des plus nobles vertus (At-Tahallî) après l'avoir purifiée de ses vices (At-Takhallî) :\n"
            "- La Science utile (Al-'Ilm) et la Clémence (Al-Hilm) ;\n"
            "- Le Scrupule pieux (Al-Wara') et la Crainte révérencielle (At-Taqwâ) ;\n"
            "- La Gratitude (Ach-Chukr) et la Sincérité pure (Al-Ikhlâs) ;\n"
            "- La Générosité (Al-Jûd / As-Sakhâ').\n"
            "Et remets la bride de ton âme charnelle (An-Nafs) à un Guide spirituel éclairé (Cheikh de Tarbiyah) qui connaît les maladies du cœur et leurs remèdes, afin qu'il te conduise à ton Seigneur.\n\n"
            "• اغتِنَامُ الخَمسِ قَبلَ الخَمسِ وَالخَاتِمَةُ المُبَارَكَةُ (Vers 295-308) :\n"
            "Saisis avec empressement cinq bénédictions avant que cinq réalités ne surviennent :\n"
            "1. Ta jeunesse (Chabâbaka) avant ta vieillesse (Haramika) ;\n"
            "2. Ta santé (Sihhataka) avant ta maladie (Saqamika) ;\n"
            "3. Ton aisance (Ghinâka) avant ton indigence (Faqrika) ;\n"
            "4. Ton temps libre (Farâghaka) avant ton occupation (Chughlika) ;\n"
            "5. Ta vie (Hayâtaka) avant ta mort (Mawtika).\n"
            "L'ouvrage s'achève par la louange infinie à Allah (Al-Hamdulillâh) et la prière sur l'Élu Muhammad ﷺ, sa famille et ses nobles Compagnons."
        ),
        "explication": (
            "DOSSIER DE SYNTHÈSE INTENSIVE — CHAPITRE 5 (VERS 274 À 308) :\n\n"
            "1. LES DEUX DEGRÉS D'AL-IHSÂN :\n"
            "• 1er Degré (Al-Mushâhadah — La Contemplation) : Adorer Allah avec une présence du cœur si lumineuse que c'est comme si on Le voyait.\n"
            "• 2e Degré (Al-Murâqabah — La Vigilance constante) : Avoir la certitude permanente qu'Allah nous observe à chaque instant, en public comme en secret.\n\n"
            "2. MÉTHODOLOGIE SOUFIE DE CHEIKH AHMADOU BAMBA :\n"
            "• At-Takhallî (Purification des vices : orgueil, ostentation, envie, paresse) précède et accompagne At-Tahallî (Ornementation par les vertus : science, scrupule Wara', gratitude, sincérité, générosité).\n"
            "• Le rôle du Cheikh de Tarbiyah (Guide spirituel) : Tout comme le corps malade a besoin d'un médecin expert, l'âme (Nafs) sujette aux illusions a besoin d'un maître connaisseur d'Allah ('Ârif billâh) et fidèle à la Sunnah.\n\n"
            "3. LES 5 OPPORTUNITÉS DE LA VIE (AL-GHANÂ'IM AL-KHAMS) :\n"
            "• Ce Hadith prophétique mis en vers par le Cheikh résume toute la vocation de Tazawwudu-ç-Çighâr : transformer le capital éphémère de ce monde (jeunesse, santé, richesse, loisir, vie) en provisions éternelles pour l'Au-delà."
        ),
        "a_retenir": (
            "- Al-Ihsân est le sommet de la religion : « Adorer Allah comme si tu Le voyais, car si tu ne Le vois pas, Lui te voit »\n"
            "- Les deux stations de l'Ihsân sont Al-Mushâhadah (la contemplation) et Al-Murâqabah (la conscience du regard divin)\n"
            "- Les nobles vertus du croyant sont la science ('Ilm), la clémence (Hilm), le scrupule (Wara'), la gratitude (Chukr), la sincérité (Ikhlâs) et la générosité (Sakhâ')\n"
            "- Le scrupule pieux (Al-Wara') consiste à délaisser ce qui est douteux par crainte de tomber dans l'illicite\n"
            "- Le Guide spirituel éclairé (Cheikh de Tarbiyah) éduque l'âme (Nafs), diagnostique ses maladies cachées et la conduit vers la proximité d'Allah\n"
            "- Les 5 opportunités à saisir avant leurs 5 contraires : la jeunesse avant la vieillesse, la santé avant la maladie, la richesse avant la pauvreté, le temps libre avant l'occupation, la vie avant la mort\n"
            "- Tazawwudu-ç-Çighâr (308 vers) unit harmonieusement le Dogme ('Aqîdah), le Droit (Fiqh) et la Spiritualité (Tasawwuf)\n"
            "- Toute étude bénie commence et s'achève par la louange à Allah (Hamd) et la prière sur le Prophète Muhammad ﷺ"
        ),
    },
    38: {  # Grande Révision Finale de Tout le Livre (Module 5, numero=99)
        "titre": "Révision Finale de Tout le Livre (Les 308 Vers)",
        "texte_source": (
            "﴿ الخُلاَصَةُ الجَامِعَةُ لِكِتَابِ تَزَوُّدِ الصِّغَارِ — ٣٠٨ بَيتًا ﴾\n\n"
            "• البَابُ الأَوَّلُ — الإِيمَانُ وَالتَّوحِيدُ (Vers 1 à 92) :\n"
            "Intention pure • 3 Piliers de la Religion (Imân, Islâm, Ihsân) • 20 Attributs nécessaires à Allah + 20 contraires impossibles + 1 statut possible (41 statuts) • 6 Articles de la Foi • 10 Anges illustres • 104 Livres révélés (100 Suhuf + 4 Livres) • 9 Statuts des Prophètes (4 nécessaires, 4 impossibles, 1 possible) • Jour Ultime & Décret Divin.\n\n"
            "• البَابُ الثَّانِي — قَوَاعِدُ الإِسلاَمِ وَطَهَارَةُ البَاطِنِ وَالظَّاهِرِ (Vers 93 à 163) :\n"
            "5 Piliers de l'Islâm • Primauté de « Lâ ilâha illâ Allâh » • Les 5 Prières prescrites • Les 4 puretés (âme, corps, habit, lieu) et les 3 critères de l'eau pure • Garde des 7 membres (langue, oreilles, yeux, ventre, mains, pieds, sexe) • Les 3 (+1) conditions de la Tawbah • Distinction entre Fard et Sunnah.\n\n"
            "• البَابُ الثَّالِثُ — فِقهُ الصَّلاَةِ وَالطَّهَارَاتِ الثَّلاَثِ (Vers 164 à 205) :\n"
            "15 Farâ'id de la Prière • 18 Sunan de la Prière (dont 8 Sunnah Mu'akkadah) • 7 Farâ'id et 8 Sunan du Wudû' • 5 Farâ'id et 4 Sunan du Ghusl • 8 Farâ'id et 3 Sunan du Tayammum.\n\n"
            "• البَابُ الرَّابِعُ — الصَّومُ وَالزَّكَاةُ وَالحَجُّ وَالمَسبُوقُ (Vers 206 à 273) :\n"
            "2 Farâ'id et 3 Sunan du Jeûne • 4 Farâ'id et 3 Sunan de la Zakat • 4 Farâ'id et 12 Sunan du Hajj • Règles complètes d'Al-Masbûq (Qadâ' pour les paroles, Binâ' pour les actes) sur les 5 prières • Les 4 degrés de la prière du malade.\n\n"
            "• البَابُ الخَامِسُ — الإِحسَانُ وَالتَّصَوُّفُ وَالخَاتِمَةُ (Vers 274 à 308) :\n"
            "Les 2 degrés d'Al-Ihsân (Mushâhadah et Murâqabah) • Les nobles vertus (Science, Clémence, Wara', Gratitude, Sincérité, Générosité) • Le Guide spirituel (Cheikh de Tarbiyah) • Les 5 opportunités avant 5 choses • Louange finale et Salât sur le Prophète ﷺ."
        ),
        "explication": (
            "DOSSIER DE SYNTHÈSE GÉNÉRALE — EXAMEN FINAL DES 308 VERS :\n\n"
            "Bienvenue dans le Grand Dossier de la Révision Finale de Tazawwudu-ç-Çighâr. Cette épreuve certifiante puise aléatoirement dans une banque de plus de 200 questions couvrant l'intégralité des 5 Grandes Étapes de l'ouvrage.\n\n"
            "TABLEAU GÉNÉRAL DES NOMBRES SACRÉS DE L'OUVRAGE :\n"
            "• 308 vers au total composés par Cheikh Ahmadou Bamba Khâdimu-r-Rasûl.\n"
            "• 3 Piliers de la Religion : Imân (6 articles), Islâm (5 piliers), Ihsân (2 degrés).\n"
            "• 50 Articles de la Shahâdah : 41 pour Allah (20+20+1) et 9 pour les Messagers (4+4+1).\n"
            "• 10 Anges illustres et 104 Livres révélés (10 Âdam + 50 Shîth + 30 Idrîs + 10 Ibrâhîm + 4 Grands Livres).\n"
            "• 4 Puretés requises, 7 Membres à préserver, 3 (+1) Conditions du Repentir (Tawbah).\n"
            "• Prière : 15 Farâ'id + 18 Sunan (dont 8 Mu'akkadah).\n"
            "• Purifications : Wudû' (7 Farâ'id + 8 Sunan) | Ghusl (5 Farâ'id + 4 Sunan) | Tayammum (8 Farâ'id + 3 Sunan).\n"
            "• Autres Piliers : Jeûne (2 Farâ'id + 3 Sunan) | Zakat (4 Farâ'id + 3 Sunan) | Hajj (4 Farâ'id + 12 Sunan).\n"
            "• Sagesse finale : 5 Opportunités à saisir avant 5 choses."
        ),
        "a_retenir": (
            "- Chapitre 1 (Vers 1-92) : 3 piliers de la Religion, 41 statuts d'Allah, 9 statuts des Prophètes, 6 articles de l'Imân, 10 Anges, 104 Livres\n"
            "- Chapitre 2 (Vers 93-163) : 5 piliers de l'Islâm, 5 prières, 4 puretés, 3 critères de l'eau, 7 membres à garder, 3 (+1) conditions de la Tawbah\n"
            "- Chapitre 3 (Vers 164-205) : Prière (15 Farâ'id / 18 Sunan dont 8 Mu'akkadah), Wudû' (7/8), Ghusl (5/4), Tayammum (8/3)\n"
            "- Chapitre 4 (Vers 206-273) : Jeûne (2/3), Zakat (4/3), Hajj (4/12), Masbûq (Qadâ' en paroles / Binâ' en actes), Malade (4 positions)\n"
            "- Chapitre 5 (Vers 274-308) : Ihsân (Mushâhadah / Murâqabah), Vertus (Science, Wara', Ikhlâs, Chukr, Sakhâ'), Guide spirituel et 5 opportunités avant 5 choses"
        ),
    },
}


# 15 Questions intensives exclusives par chapitre (33..37) + 15 nouvelles questions multi-formats pour la Finale (38)
QUESTIONS_INTENSIVES = {
    33: [  # CHAPITRE 1 — 15 questions intensives
        {
            "texte": "[Cas Pratique - Dogme] Un élève affirme que le nombre total d'articles de foi contenus dans la Shahâdah « Lâ ilâha illâ Allâh, Muhammadun Rasûlullâh » est de 50. Quelle est la décomposition exacte de ces 50 articles selon le Tawhîd ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Les 50 articles du dogme ('Aqâ'id) se composent de 41 statuts pour Allah (20 nécessaires, 20 impossibles, 1 possible) et 9 statuts pour les Messagers (4 nécessaires, 4 impossibles, 1 possible).",
            "choix": [
                ("41 concernant Allah (20+20+1) et 9 concernant les Messagers (4+4+1)", True),
                ("25 concernant Allah et 25 concernant les Messagers", False),
                ("40 concernant Allah et 10 concernant les Anges", False),
                ("30 concernant l'Imân et 20 concernant l'Islâm", False),
            ],
        },
        {
            "texte": "Associez chacun des Attributs divins suivants à sa signification exacte dans Tazawwudu-ç-Çighâr :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Al-Qidam est l'Antériorité sans début, Al-Baqâ' la Pérennité sans fin, Al-Qiyâmu bi-nafsihi l'Autosuffisance absolue et Al-Mukhâlafatu lil-hawâdith la Dissemblance d'avec le créé.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Al-Qidam", "droite": "L'Antériorité sans début"},
                    {"gauche": "Al-Baqâ'", "droite": "La Pérennité sans fin"},
                    {"gauche": "Al-Qiyâmu bi-nafsihi", "droite": "L'Autosuffisance absolue"},
                    {"gauche": "Al-Wahdâniyyah", "droite": "L'Unicité absolue"},
                ]
            },
        },
        {
            "texte": "Associez chaque Prophète au nombre exact de Feuillets (Suhuf) ou au Livre qu'il a reçu d'Allah :",
            "type_question": "association",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Sur les 104 Livres révélés : Shîth a reçu 50 feuillets, Idrîs 30 feuillets, Âdam 10 feuillets, Ibrâhîm 10 feuillets (total = 100 Suhuf), plus les 4 Grands Livres.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Shîth (Seth)", "droite": "50 Feuillets (Suhuf)"},
                    {"gauche": "Idrîs (Énoch)", "droite": "30 Feuillets (Suhuf)"},
                    {"gauche": "Ibrâhîm (Abraham)", "droite": "10 Feuillets (Suhuf)"},
                    {"gauche": "Dâwûd (David)", "droite": "Le Zabûr (Psaumes)"},
                ]
            },
        },
        {
            "texte": "Combien de Livres célestes au total (Feuillets Suhuf et Grands Livres réunis) Allah a-t-Il révélés selon le Chapitre 1 ? (Répondez en chiffres)",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Allah a révélé 104 Livres au total : 100 Feuillets (Suhuf) et 4 Grands Livres (Tawrât, Zabûr, Injîl, Furqân).",
            "donnees_extra": {"reponses_acceptees": ["104", "cent quatre", "104 livres"]},
        },
        {
            "texte": "Selon Cheikh Ahmadou Bamba, attribuer aux Anges le sexe féminin est une simple erreur vénielle sans gravité sur la foi.",
            "type_question": "vrai_faux",
            "difficulte": "difficile",
            "points": 15,
            "explication": "Faux ! Les Anges ne sont ni mâles ni femelles. Les qualifier de mâles est une perversité (Fisq), et les qualifier de femelles est une mécréance (Kufr) car cela dément directement le texte coranique.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Quel est le statut rationnel (Hukm 'Aqlî) du fait qu'Allah crée un être contingent ou le laisse dans le néant ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faire exister tout possible ou le laisser dans le néant (Fi'lu kulli mumkinin aw tarkuhu) est l'unique Attribut Possible (Jâ'iz) à l'égard d'Allah : rien ne L'oblige à créer.",
            "choix": [
                ("Possible (Al-Jâ'iz) à l'égard d'Allah", True),
                ("Obligatoire (Al-Wâjib) à l'égard d'Allah", False),
                ("Impossible (Al-Mustahîl) à l'égard d'Allah", False),
                ("Traditionnel (Sunnah)", False),
            ],
        },
        {
            "texte": "Associez chacun de ces Anges illustres à la mission que lui confie Allah :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Jibrîl est chargé de la Révélation, Mîkâ'îl des pluies et subsistances, Isrâfîl de souffler dans la Trompe (Sûr) et Ridwân de garder le Paradis.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Jibrîl", "droite": "Transmission de la Révélation"},
                    {"gauche": "Mîkâ'îl", "droite": "Pluie et subsistance"},
                    {"gauche": "Isrâfîl", "droite": "Souffler dans la Trompe (Sûr)"},
                    {"gauche": "Ridwân", "droite": "Gardien du Paradis"},
                ]
            },
        },
        {
            "texte": "Parmi les propositions suivantes, laquelle décrit exactement l'Attribut de la Parole d'Allah (Al-Kalâm) dans la doctrine Sunnite exposée par le Cheikh ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "La Parole d'Allah est un Attribut éternel inhérent à Son Essence, exempt de lettres, de sons, de voix, d'antériorité ou de postériorité, et ne ressemble aucunement à la parole des créatures.",
            "choix": [
                ("Une Parole éternelle, sans lettre ni voix, ne ressemblant pas à celle des créatures", True),
                ("Une parole composée de sons successifs apparus dans le temps", False),
                ("Une simple métaphore désignant la pensée humaine", False),
                ("Un attribut facultatif apparu après la création des Anges", False),
            ],
        },
        {
            "texte": "Associez chacune des 4 qualités nécessaires des Prophètes à son contraire impossible :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Les 4 qualités nécessaires des Messagers sont As-Sidq (contre le mensonge Kadhib), Al-Amânah (contre la trahison Khiyânah), At-Tablîgh (contre la dissimulation Kitmân) et Al-Fatânah (contre la stupidité Balâdah).",
            "donnees_extra": {
                "paires": [
                    {"gauche": "As-Sidq (Véracité)", "droite": "Al-Kadhib (Mensonge)"},
                    {"gauche": "Al-Amânah (Fidélité)", "droite": "Al-Khiyânah (Trahison)"},
                    {"gauche": "At-Tablîgh (Transmission)", "droite": "Al-Kitmân (Dissimulation)"},
                    {"gauche": "Al-Fatânah (Sagacité)", "droite": "Al-Balâdah (Stupidité)"},
                ]
            },
        },
        {
            "texte": "Pourquoi Allah permet-Il que Ses Prophètes éprouvent des accidents humains comme la maladie, la faim ou la fatigue (Al-A'râd al-Bashariyyah) ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Ces états humains non avilissants sont possibles (Jâ'iz) chez les Prophètes pour accroître leur récompense, élever leur rang, montrer la bassesse de ce bas-monde et consoler les croyants éprouvés.",
            "choix": [
                ("Pour élever leurs degrés, accroître leur récompense et servir de modèle de patience", True),
                ("Parce qu'ils ne bénéficient pas de l'infaillibilité prophétique ('Ismah)", False),
                ("Pour les dispenser d'accomplir les prières obligatoires", False),
                ("Parce qu'ils peuvent oublier de transmettre une partie de la Révélation", False),
            ],
        },
        {
            "texte": "Quel est le nom de l'Ange gardien de l'Enfer mentionné parmi les 10 Anges à connaître individuellement ?",
            "type_question": "texte_court",
            "difficulte": "facile",
            "points": 15,
            "explication": "L'Ange Mâlik est le gardien de l'Enfer, tandis que Ridwân est le gardien du Paradis.",
            "donnees_extra": {"reponses_acceptees": ["malik", "mâlik", "ange malik"]},
        },
        {
            "texte": "Les deux Anges chargés d'interroger le défunt dans sa tombe s'appellent Raqîb et 'Atîd.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faux ! Raqîb et 'Atîd sont les deux Anges scribes qui inscrivent les œuvres durant la vie. Ceux qui interrogent dans la tombe sont Munkar et Nakîr.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Dans la métaphore de l'édifice religieux exposée au Chapitre 1, quel rôle joue Al-Imân (la Foi) par rapport à Al-Islâm et Al-Ihsân ?",
            "type_question": "qcm",
            "difficulte": "facile",
            "points": 15,
            "explication": "Al-Imân constitue la fondation et les racines invisibles dans le cœur ; sans la validité de l'Imân, aucune œuvre extérieure de l'Islâm n'est acceptée.",
            "choix": [
                ("La fondation intérieure (les racines du cœur) sur laquelle repose tout l'édifice", True),
                ("Un ornement facultatif réservé aux savants âgés", False),
                ("Uniquement les règles juridiques de la vente et du mariage", False),
                ("La dernière étape qui dispense de la prière", False),
            ],
        },
        {
            "texte": "Comment appelle-t-on en arabe le Livre Saint révélé au Prophète Muhammad ﷺ lorsqu'il est désigné comme « Le Discernement » dans le poème ?",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Le Cheikh nomme le Coran « Al-Furqân » (Le Discernement entre le Vrai et le Faux) parmi les 4 Grands Livres révélés.",
            "donnees_extra": {"reponses_acceptees": ["furqan", "al-furqan", "al furqan", "fourqane", "al-fourqane"]},
        },
        {
            "texte": "Croire au Décret Divin (Al-Qadâ' wal-Qadar) autorise l'homme à délaisser les commandements d'Allah en prétextant que tout est déjà écrit.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faux ! Le croyant croit que tout procède du Décret d'Allah tout en restant pleinement responsable d'obéir aux ordres divins et de fuir les péchés.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
    ],

    34: [  # CHAPITRE 2 — 15 questions intensives
        {
            "texte": "[Cas Pratique - Pureté] Un élève veut faire ses ablutions avec une eau dans laquelle est tombée une impureté qui a légèrement modifié son odeur, bien que sa couleur et son goût semblent normaux. Cette eau est-elle valide pour la purification ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Non ! Dès que l'une des trois caractéristiques de l'eau (couleur, goût OU odeur) est altérée par une impureté, l'eau perd sa pureté et ne peut plus purifier.",
            "choix": [
                ("Non, car l'altération d'une seule des 3 qualités (couleur, goût ou odeur) par une impureté invalide l'eau", True),
                ("Oui, tant que les 3 qualités ne sont pas altérées en même temps", False),
                ("Oui, car seule la couleur compte en droit malikite", False),
                ("Oui, si on l'utilise uniquement pour le Ghusl", False),
            ],
        },
        {
            "texte": "Associez chacun des 4 volets de la pureté exigée pour la prière à sa réalité concrète :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Les 4 puretés mentionnées par le Cheikh sont la pureté de l'âme (sincérité Ikhlâs), du corps (Wudû'/Ghusl et absence de souillure), de l'habit et du lieu.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Pureté de l'âme", "droite": "Sincérité pour Allah sans ostentation"},
                    {"gauche": "Pureté du corps", "droite": "Ablutions/Ghusl et corps exempt d'impureté"},
                    {"gauche": "Pureté du vêtement", "droite": "Habit licite et exempt de souillure"},
                    {"gauche": "Pureté du lieu", "droite": "Endroit propre où l'on pose les membres"},
                ]
            },
        },
        {
            "texte": "Combien de membres du corps (Al-Jawârih) le croyant doit-il impérativement préserver du péché selon le Chapitre 2 ? (Répondez en chiffre)",
            "type_question": "texte_court",
            "difficulte": "facile",
            "points": 15,
            "explication": "Les 7 membres sont : la langue, les oreilles, les yeux, le ventre, les mains, les pieds et le sexe.",
            "donnees_extra": {"reponses_acceptees": ["7", "sept", "7 membres"]},
        },
        {
            "texte": "Associez chacun de ces membres parmi les 7 à la faute spécifique dont il faut le préserver :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "La langue doit être gardée de la médisance (Ghîbah) et du mensonge, le ventre des gains illicites (Harâm/Ribâ), les yeux du regard interdit et les oreilles de l'écoute de la calomnie.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "La Langue", "droite": "Mensonge, médisance (Ghîbah) et calomnie"},
                    {"gauche": "Le Ventre", "droite": "Nourriture illicite (Harâm) et usure"},
                    {"gauche": "Les Yeux", "droite": "Regarder l'interdit ou mépriser un musulman"},
                    {"gauche": "Les Oreilles", "droite": "Écouter la médisance, les mensonges et la futilité"},
                ]
            },
        },
        {
            "texte": "[Cas Pratique - Tawbah] Une personne a pris injustement le bien d'un voisin, puis a pleuré de regret et promis à Allah de ne plus recommencer, tout en gardant l'objet volé alors qu'elle peut le rendre. Son repentir (Tawbah) est-il complet ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Non ! Lorsqu'un péché lèse le droit d'une créature, le repentir n'est valide qu'en remplissant la 4e condition : restituer le bien à son propriétaire ou obtenir son pardon.",
            "choix": [
                ("Non, car la réparation des torts envers autrui (restituer le bien ou demander pardon) est une condition obligatoire", True),
                ("Oui, le simple regret intérieur suffit même sans rendre le bien", False),
                ("Oui, s'il fait deux Rak'ah surérogatoires", False),
                ("Non, car le repentir n'est accepté qu'à La Mecque", False),
            ],
        },
        {
            "texte": "Pourquoi Cheikh Ahmadou Bamba qualifie-t-il « Lâ ilâha illâ Allâh » de meilleure évocation (Afdalu-dh-Dhikr) ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Parce qu'elle purifie le cœur de tout polythéisme (Chirk) et renferme par implication l'ensemble des 50 articles du dogme de l'Unicité.",
            "choix": [
                ("Parce qu'elle purifie le cœur du Chirk et contient les 50 articles du dogme", True),
                ("Parce qu'elle dispense d'accomplir les 5 prières quotidiennes", False),
                ("Parce qu'elle ne doit être prononcée qu'une seule fois par an", False),
                ("Parce qu'elle remplace le jeûne de Ramadan", False),
            ],
        },
        {
            "texte": "Parmi les 5 piliers de l'Islâm, lequel n'est obligatoire que pour celui qui en possède la capacité physique et financière (Al-Istitâ'ah) ?",
            "type_question": "qcm",
            "difficulte": "facile",
            "points": 15,
            "explication": "Le Pèlerinage à la Maison Sacrée d'Allah (Al-Hajj) est prescrit une fois dans la vie à quiconque en a la capacité (physique, matérielle et sécurité de la route).",
            "choix": [
                ("Le Pèlerinage à la Maison Sacrée (Al-Hajj)", True),
                ("Les cinq prières quotidiennes", False),
                ("L'attestation de foi (Shahâdah)", False),
                ("La sincérité de l'intention", False),
            ],
        },
        {
            "texte": "Selon le Chapitre 2, il est permis à un musulman de s'engager dans un acte d'adoration sans connaître la différence entre ses obligations (Fard) et ses traditions (Sunnah).",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faux ! Le Cheikh rappelle fermement qu'il est interdit d'accomplir un acte sans en connaître les règles d'Allah, à commencer par la distinction entre le Fard et la Sunnah.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Quel est le premier membre parmi les 7 que le Cheikh ordonne de brider et de surveiller en priorité en raison de ses grands dangers ?",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "La langue (Al-Lisân) est citée en tête des 7 membres car elle est la source du mensonge, de la médisance et de l'ostentation verbale.",
            "donnees_extra": {"reponses_acceptees": ["la langue", "langue", "al-lisan", "lisan"]},
        },
        {
            "texte": "Retarder volontairement une prière obligatoire au-delà de son temps légal sans excuse valable est un grand péché.",
            "type_question": "vrai_faux",
            "difficulte": "facile",
            "points": 10,
            "explication": "Vrai ! Allah a prescrit les 5 prières à des heures déterminées, et le Cheikh met sévèrement en garde contre leur négligence ou leur retardement.",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "Associez chacune des 3 conditions intérieures de la Tawbah à sa définition :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Al-Iqlâ' est l'abandon immédiat du péché, An-Nadam est le remords sincère du cœur, et Al-'Azm est la ferme résolution de ne plus y revenir.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Al-Iqlâ' (Pas présent)", "droite": "Cesser immédiatement le péché"},
                    {"gauche": "An-Nadam (Passé)", "droite": "Regretter sincèrement dans son cœur"},
                    {"gauche": "Al-'Azm (Futur)", "droite": "Décider fermement de ne plus jamais y retomber"},
                ]
            },
        },
        {
            "texte": "Quel effet spirituel produit la consommation de nourriture illicite (Harâm) sur les actes d'adoration selon le Chapitre 2 ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "La nourriture illicite obscurcit le cœur, souille l'intérieur et fait obstacle à l'acceptation des œuvres et à l'exaucement des invocations.",
            "choix": [
                ("Elle obscurcit le cœur et empêche l'acceptation des œuvres et des invocations", True),
                ("Elle annule uniquement le Tayammum mais pas la prière", False),
                ("Elle est automatiquement effacée par le simple lavage des mains", False),
                ("Elle n'a aucun impact tant que l'habit est propre", False),
            ],
        },
        {
            "texte": "Si l'eau change d'aspect à cause de la terre naturelle du sol sur lequel elle coule ou stagne, reste-t-elle pure et purifiante ?",
            "type_question": "vrai_faux",
            "difficulte": "difficile",
            "points": 15,
            "explication": "Vrai ! En Fiqh malikite, l'eau altérée par son propre gîte naturel (terre, argile, mousse aquatique) reste pure et purifiante (Tahûr).",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "Combien de prières obligatoires quotidiennes sont prescrites au musulman responsable chaque jour et nuit ? (Répondez en chiffre)",
            "type_question": "texte_court",
            "difficulte": "facile",
            "points": 10,
            "explication": "Cinq (5) prières obligatoires quotidiennes : Subh, Zuhr, 'Asr, Maghrib et 'Ichâ'.",
            "donnees_extra": {"reponses_acceptees": ["5", "cinq", "5 prieres", "5 prières"]},
        },
        {
            "texte": "Laquelle de ces attitudes annule la pureté de l'âme (la 1re condition de pureté) dans l'adoration ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "L'ostentation (Ar-Riyâ' : agir pour être vu et loué par les gens) détruit la pureté de l'intention (Ikhlâs).",
            "choix": [
                ("L'ostentation (Ar-Riyâ' : chercher le regard et les éloges des créatures)", True),
                ("Le fait de prier seul chez soi la nuit", False),
                ("Le fait de réciter une sourate courte après la Fâtihah", False),
                ("Le fait de faire ses ablutions à l'eau froide", False),
            ],
        },
    ],

    35: [  # CHAPITRE 3 — 15 questions intensives
        {
            "texte": "[Cas Pratique - Prière] Un fidèle accomplit sa prière en réciter parfaitement la Fâtihah, mais oublie de réciter la Sourate qui suit dans la première Rak'ah. Quel est le statut de la récitation de cette Sourate selon le Chapitre 3 ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "La Fâtihah est l'un des 15 actes obligatoires (Farâ'id), tandis que la Sourate après la Fâtihah fait partie des 8 Sunnah Mu'akkadah (traditions fortement recommandées).",
            "choix": [
                ("C'est une Sunnah Mu'akkadah (tradition fortement recommandée), contrairement à la Fâtihah qui est un Fard", True),
                ("C'est un Fard absolu dont l'oubli oblige à recommencer toute la prière depuis le début", False),
                ("C'est un acte interdit dans les prières à voix basse", False),
                ("C'est une obligation uniquement dans la 3e et la 4e Rak'ah", False),
            ],
        },
        {
            "texte": "Associez chaque chapitre rituel du Chapitre 3 au nombre exact de ses Actes Obligatoires (Farâ'id) selon Tazawwudu-ç-Çighâr :",
            "type_question": "association",
            "difficulte": "difficile",
            "points": 25,
            "explication": "Dans le Chapitre 3 : La Prière compte 15 Farâ'id, les Ablutions (Wudû') 7 Farâ'id, le Ghusl 5 Farâ'id et le Tayammum 8 Farâ'id.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "La Prière (As-Salât)", "droite": "15 Obligations (Farâ'id)"},
                    {"gauche": "Les Ablutions (Al-Wudû')", "droite": "7 Obligations (Farâ'id)"},
                    {"gauche": "Le Bain rituel (Al-Ghusl)", "droite": "5 Obligations (Farâ'id)"},
                    {"gauche": "Le Tayammum", "droite": "8 Obligations (Farâ'id)"},
                ]
            },
        },
        {
            "texte": "Associez chacun de ces actes de la Prière à sa catégorie juridique exacte (Fard ou Sunnah Mu'akkadah) :",
            "type_question": "association",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Le Takbîr al-Ihrâm et le Salâm final sont des Farâ'id (piliers), tandis que le Tashahhud et le fait de dire « Sami'a Allâhu liman hamidah » sont des Sunnah Mu'akkadah.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Takbîr al-Ihrâm (Takbîr d'ouverture)", "droite": "Acte Obligatoire (Fard)"},
                    {"gauche": "Dire « Sami'a Allâhu liman hamidah »", "droite": "Sunnah Mu'akkadah"},
                    {"gauche": "Le Salut final (As-Salâm)", "droite": "Acte Obligatoire (Fard)"},
                    {"gauche": "Le Tashahhud (1er et 2e)", "droite": "Sunnah Mu'akkadah"},
                ]
            },
        },
        {
            "texte": "Parmi les 18 Traditions (Sunan) de la Prière, combien sont qualifiées de « Sunnah Mu'akkadah » (fortement recommandées) dans le poème ? (Répondez en chiffre)",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Parmi les 18 Sunan de la Prière, 8 sont des Sunnah Mu'akkadah (Sourate, station debout pour elle, voix haute, voix basse, Takbîrs secondaires, Sami'a Allâhu liman hamidah, 1er Tashahhud, 2e Tashahhud).",
            "donnees_extra": {"reponses_acceptees": ["8", "huit", "8 sunnah"]},
        },
        {
            "texte": "[Cas Pratique - Ablutions] Lors de ses ablutions (Wudû'), une personne plonge son bras sous le robinet sans passer sa main dessus pour frotter l'eau sur la peau. A-t-elle rempli toutes les obligations du Wudû' en rite malikite ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Non ! Le frottement (Ad-Dalk : passer la main sur le membre avec l'eau) est la 6e des 7 obligations (Farâ'id) du Wudû' et l'une des 5 obligations du Ghusl.",
            "choix": [
                ("Non, car le frottement (Ad-Dalk) fait partie des 7 obligations (Farâ'id) du Wudû'", True),
                ("Oui, car le frottement n'est obligatoire que dans le Tayammum", False),
                ("Oui, le simple contact de l'eau suffit sans frottement", False),
                ("Non, car il faut frotter uniquement avec une pierre", False),
            ],
        },
        {
            "texte": "Dans les Ablutions mineures (Wudû'), l'essuyage des oreilles et le rinçage de la bouche (Madmadah) font partie des 7 obligations (Farâ'id).",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faux ! Le rinçage de la bouche, l'inspiration de l'eau par le nez et l'essuyage des oreilles font partie des 8 Traditions (Sunan) du Wudû', tandis que l'essuyage de la tête entière est un Fard.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "[Cas Pratique - Tayammum] Dans le Tayammum, quelle est la limite obligatoire (Fard) de l'essuyage des mains, et quelle est la limite traditionnelle (Sunnah) ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "En rite malikite, l'essuyage des mains jusqu'aux poignets (Al-Kû'ayn) est obligatoire (Fard), tandis que prolonger l'essuyage des poignets jusqu'aux coudes (Al-Mirfaqayn) est une Sunnah.",
            "choix": [
                ("Jusqu'aux poignets est Obligatoire (Fard), et prolonger jusqu'aux coudes est Traditionnel (Sunnah)", True),
                ("Jusqu'aux épaules est Obligatoire, et jusqu'aux coudes est Sunnah", False),
                ("Seul le bout des doigts est Obligatoire, et la paume est Sunnah", False),
                ("Jusqu'aux coudes est Obligatoire, et jusqu'aux poignets est interdit", False),
            ],
        },
        {
            "texte": "Comment appelle-t-on en arabe l'obligation d'accomplir les actes des ablutions (ou du Ghusl) à la suite les uns des autres sans interruption prolongée ?",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "La continuité immédiate s'appelle Al-Faur (ou Al-Muwâlât) : c'est la 7e obligation du Wudû' et la 4e obligation du Ghusl.",
            "donnees_extra": {"reponses_acceptees": ["faur", "al-faur", "fawr", "al-fawr", "muwalat", "al-muwalat", "continuité", "continuite"]},
        },
        {
            "texte": "Parmi les 5 obligations du Bain rituel (Al-Ghusl), laquelle concerne spécifiquement les cheveux et la barbe ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Le démêlage des cheveux et des poils (At-Takhlîl) avec les doigts pour faire parvenir l'eau jusqu'à la racine de la peau est l'une des 5 obligations du Ghusl.",
            "choix": [
                ("Démêler les cheveux et les poils avec les doigts (At-Takhlîl) pour que l'eau atteigne l'épiderme", True),
                ("Se raser obligatoirement la tête à chaque Ghusl", False),
                ("Appliquer du parfum avant de verser l'eau", False),
                ("Essuyer uniquement le sommet des cheveux sans les mouiller", False),
            ],
        },
        {
            "texte": "Il est valide de faire le Tayammum avant l'entrée de l'heure de la prière obligatoire et d'attendre une heure avant de prier.",
            "type_question": "vrai_faux",
            "difficulte": "difficile",
            "points": 15,
            "explication": "Faux ! Parmi les 8 obligations du Tayammum figurent l'accomplissement après l'entrée de l'heure et la liaison immédiate (Al-Ittisâl) entre le Tayammum et la prière.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Associez chaque terme arabe de la Prière à sa définition exacte :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "At-Tuma'nînah est l'accalmie/stabilisation des membres, Al-I'tidâl l'équilibre droit, Ar-Rukû' l'inclinaison et As-Sujûd la prosternation.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "At-Tuma'nînah", "droite": "L'accalmie et la stabilisation des membres"},
                    {"gauche": "Al-I'tidâl", "droite": "La rectitude et l'équilibre du corps"},
                    {"gauche": "Ar-Rukû'", "droite": "L'inclinaison"},
                    {"gauche": "As-Sujûd", "droite": "La prosternation sur le front"},
                ]
            },
        },
        {
            "texte": "Combien d'actes traditionnels (Sunan) comporte le Bain rituel (Al-Ghusl) selon le Chapitre 3 ? (Répondez en chiffre)",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Le Ghusl comporte 5 obligations (Farâ'id) et 4 traditions (Sunan : laver les mains au début, rincer la bouche, inspirer l'eau par le nez, essuyer l'intérieur des oreilles).",
            "donnees_extra": {"reponses_acceptees": ["4", "quatre", "4 traditions", "4 sunan"]},
        },
        {
            "texte": "Lors des ablutions (Wudû'), quelle est la part de la tête qu'il est obligatoire (Fard) d'essuyer selon l'école malikite exposée dans Tazawwudu-ç-Çighâr ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "L'essuyage de la totalité de la tête (Mashu jamî'i ar-ra's) est la 4e obligation du Wudû' ; le retour des mains de la nuque vers le front (Radd al-yadayn) est une Sunnah.",
            "choix": [
                ("L'essuyage de toute la tête (aller), tandis que le retour des mains est une Sunnah", True),
                ("Uniquement trois cheveux sur le front", False),
                ("Uniquement la nuque et le cou", False),
                ("L'essuyage de la tête est entièrement facultatif", False),
            ],
        },
        {
            "texte": "Pour celui qui prie derrière un Imam (Al-Ma'mûm), formuler l'intention de suivre l'Imam fait partie des 15 obligations de la prière.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Vrai ! L'intention de suivre l'Imam (Niyyat al-Iqtidâ') est comptée parmi les 15 Farâ'id de la prière pour le prieur dirigé.",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "Dans le Tayammum, combien de frappes sur le sol pur sont obligatoires et laquelle est traditionnelle (Sunnah) ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "La première frappe (Ad-Darbah al-Ûlâ) fait partie des 8 obligations du Tayammum, tandis que la seconde frappe pour les mains fait partie des 3 traditions.",
            "choix": [
                ("La 1re frappe est Obligatoire (Fard) et la 2e frappe est Traditionnelle (Sunnah)", True),
                ("Les deux frappes sont toutes deux facultatives", False),
                ("Il faut obligatoirement frapper le sol 7 fois", False),
                ("Seule la 2e frappe est obligatoire", False),
            ],
        },
    ],

    36: [  # CHAPITRE 4 — 15 questions intensives
        {
            "texte": "[Cas Pratique - Al-Masbûq à Maghrib] Un fidèle rejoint l'Imam dans la 3e et dernière Rak'ah de la prière de Maghrib (il a donc manqué les 2 premières Rak'ah). Comment doit-il rattraper ses 2 Rak'ah après le Salâm de l'Imam ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 25,
            "explication": "Selon la règle Qadâ' (paroles) / Binâ' (actes) : il se lève, accomplit 1 Rak'ah avec Fâtihah et Sourate à voix haute, S'ASSOIT pour le Tashahhud (car c'est sa 2e Rak'ah au total en comptant celle priée avec l'Imam), puis se lève et accomplit sa dernière Rak'ah avec Fâtihah et Sourate à voix haute !",
            "choix": [
                ("Il fait 1 Rak'ah (Fâtihah + Sourate à voix haute), s'assoit pour le Tashahhud, puis fait 1 Rak'ah (Fâtihah + Sourate à voix haute)", True),
                ("Il fait 2 Rak'ah d'affilée avec Fâtihah seule à voix basse sans s'asseoir entre elles", False),
                ("Il fait 2 Rak'ah à voix basse sans Sourate, puis refait la prière depuis le début", False),
                ("Il fait 1 seule Rak'ah car Maghrib se raccourcit pour le retardataire", False),
            ],
        },
        {
            "texte": "[Cas Pratique - Al-Masbûq à 'Ichâ'] Un fidèle rejoint l'Imam à la 4e et dernière Rak'ah de la prière de 'Ichâ' (il a manqué les 3 premières Rak'ah). Comment complète-t-il sa prière après le Salâm de l'Imam ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 25,
            "explication": "Il a prié 1 Rak'ah avec l'Imam. Après le Salâm : 1) Il se lève et fait 1 Rak'ah avec Fâtihah + Sourate à voix haute ; 2) Il s'assoit pour son Tashahhud médian (car il en est à 2 Rak'ah en actes) ; 3) Il se lève et fait 1 Rak'ah avec Fâtihah + Sourate à voix haute (sa 2e en paroles) ; 4) Il se lève sans Tashahhud et fait 1 dernière Rak'ah avec Fâtihah seule à voix basse !",
            "choix": [
                ("1 Rak'ah (Fâtihah+Sourate voix haute), assise du Tashahhud, puis 1 Rak'ah (Fâtihah+Sourate voix haute), puis 1 Rak'ah (Fâtihah seule voix basse)", True),
                ("3 Rak'ah consécutives avec Fâtihah seule à voix basse sans aucune assise intermédiaire", False),
                ("2 Rak'ah à voix basse puis 1 Rak'ah à voix haute", False),
                ("1 Rak'ah avec Fâtihah seule, assise, puis 2 Rak'ah avec Sourate à voix haute", False),
            ],
        },
        {
            "texte": "Associez chaque pilier étudié au Chapitre 4 au nombre exact de ses Obligations (Farâ'id) et Traditions (Sunan) :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Dans le Chapitre 4 : Le Jeûne compte 2 obligations et 3 traditions ; la Zakat 4 obligations et 3 traditions ; le Hajj 4 obligations et 12 traditions.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Le Jeûne (As-Sawm)", "droite": "2 Obligations et 3 Traditions"},
                    {"gauche": "L'Aumône Légale (Az-Zakat)", "droite": "4 Obligations et 3 Traditions"},
                    {"gauche": "Le Pèlerinage (Al-Hajj)", "droite": "4 Obligations et 12 Traditions"},
                ]
            },
        },
        {
            "texte": "À quel moment précis un retardataire (Masbûq) qui entre à la mosquée valide-t-il la Rak'ah en cours avec l'Imam ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Celui qui rejoint l'Imam dans l'inclinaison (Ar-Rukû') en posant ses mains sur ses genoux avant que l'Imam ne relève la tête a validé la Rak'ah. S'il arrive après le redressement de l'Imam, il doit rattraper cette Rak'ah.",
            "choix": [
                ("Lorsqu'il rejoint l'Imam en inclinaison (Rukû') avant que l'Imam ne se redresse", True),
                ("Même s'il rejoint l'Imam lors de la seconde prosternation (Sujûd)", False),
                ("Uniquement s'il était présent avant le Takbîr d'ouverture de l'Imam", False),
                ("Même s'il rejoint l'Imam pendant le Tashahhud final", False),
            ],
        },
        {
            "texte": "Associez les 3 traditions (Sunan) du Jeûne à leur formulation exacte :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Les 3 traditions du Jeûne sont : hâter la rupture (Ta'jîl al-Fitr) dès le coucher du soleil, retarder le repas de l'aube (Ta'khîr as-Suhûr) et préserver sa langue des futilités.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Au coucher du soleil (Maghrib)", "droite": "Hâter la rupture du jeûne (Ta'jîl al-Fitr)"},
                    {"gauche": "À la fin de la nuit (avant Fajr)", "droite": "Retarder le repas de l'aube (Ta'khîr as-Suhûr)"},
                    {"gauche": "Durant toute la journée", "droite": "Retenir sa langue de toute parole vaine"},
                ]
            },
        },
        {
            "texte": "Dans la règle malikite du Masbûq (« Qadâ' fî al-Aqwâl, Binâ' fî al-Af'âl »), que signifie le terme « Qadâ' » appliqué aux paroles (la récitation) ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "« Qadâ' fî al-Aqwâl » signifie qu'en matière de récitation, le retardataire considère ce qu'il rattrape comme le DÉBUT de sa prière (ce qu'il a manqué) : il récite donc Fâtihah + Sourate pour la 1re et la 2e Rak'ah manquées.",
            "choix": [
                ("Qu'en matière de récitation, il accomplit les Rak'ah manquées comme étant le début de sa prière (Fâtihah + Sourate)", True),
                ("Qu'il est dispensé de réciter la Fâtihah dans toutes les Rak'ah rattrapées", False),
                ("Qu'il doit attendre le lendemain pour refaire toute sa prière", False),
                ("Qu'il doit réciter uniquement le Tashahhud debout", False),
            ],
        },
        {
            "texte": "Quel est le nom arabe du seuil minimal de richesse à partir duquel la Zakat devient obligatoire ?",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Le seuil minimal imposable s'appelle le Nisâb (An-Nisâb), deuxième obligation de la Zakat après l'intention.",
            "donnees_extra": {"reponses_acceptees": ["nisab", "an-nisab", "nissab", "niçab"]},
        },
        {
            "texte": "Parmi les 4 piliers obligatoires du Pèlerinage (Al-Hajj), l'omission de la station à 'Arafah invalide le Hajj et ne peut pas être simplement compensée par une offrande.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Vrai ! Le Prophète ﷺ a dit : « Le Hajj, c'est 'Arafah ». C'est le pilier central parmi les 4 obligations du Hajj (Ihrâm, 'Arafah, Tawâf al-Ifâdah, Sa'y).",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "[Cas Pratique - Prière du Malade] Un malade est totalement incapable de se tenir debout et incapable de rester assis, même appuyé. Quelle est la position qu'il doit adopter immédiatement après dans l'ordre prescrit ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "L'ordre graduel est : 1. Debout ; 2. Assis ; 3. Allongé sur le côté (le côté droit étant privilégié, sinon le gauche) face à la Qiblah ; 4. Allongé sur le dos, pieds vers la Qiblah.",
            "choix": [
                ("Prier allongé sur le côté (de préférence le côté droit) face à la Qiblah, sinon sur le dos les pieds vers la Qiblah", True),
                ("Abandonner totalement la prière jusqu'à sa guérison complète", False),
                ("Demander à un proche de prier à sa place", False),
                ("Payer un repas par prière sans prier", False),
            ],
        },
        {
            "texte": "Associez chacun des 4 piliers obligatoires du Hajj à sa description :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Les 4 obligations du Hajj sont : l'Ihrâm (entrée en sacralisation), le Wuqûf à 'Arafah, le Tawâf al-Ifâdah autour de la Ka'bah et le Sa'y entre Safâ et Marwah.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Al-Ihrâm", "droite": "Entrée en état de sacralisation avec l'intention"},
                    {"gauche": "Wuqûf bi-'Arafah", "droite": "Station sur la plaine de 'Arafah le 9 Dhû al-Hijjah"},
                    {"gauche": "Tawâf al-Ifâdah", "droite": "Sept tours rituels autour de la Ka'bah"},
                    {"gauche": "As-Sa'y", "droite": "Parcours rituel entre les collines de Safâ et Marwah"},
                ]
            },
        },
        {
            "texte": "Combien de traditions (Sunan) comporte le Pèlerinage (Al-Hajj) dans l'énumération du Chapitre 4 ? (Répondez en chiffre)",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Le Hajj comporte 4 obligations (Farâ'id) et 12 traditions (Sunan : 4 liées à l'Ihrâm, 4 au Tawâf et 4 au Sa'y).",
            "donnees_extra": {"reponses_acceptees": ["12", "douze", "12 traditions", "12 sunan"]},
        },
        {
            "texte": "Pour que le jeûne obligatoire de Ramadan soit valide, l'intention (An-Niyyah) doit être formulée la nuit avant l'apparition de l'aube (Fajr).",
            "type_question": "vrai_faux",
            "difficulte": "facile",
            "points": 15,
            "explication": "Vrai ! L'intention nocturne (Tabyît an-Niyyah) est la première des 2 obligations du jeûne.",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "En matière de Zakat sur les récoltes agricoles (céréales, dattes), faut-il attendre l'écoulement d'une année entière (Al-Hawl) après la moisson ou l'acquitter dès la récolte ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Contrairement au bétail et à la monnaie qui exigent le Hawl (1 an lunaire), la Zakat des cultures s'acquitte dès la maturité et la moisson (« Et acquittez-en le droit le jour de la récolte »).",
            "choix": [
                ("Elle s'acquitte dès la maturité et la récolte, sans attendre un an", True),
                ("Il faut attendre deux années lunaires", False),
                ("Les récoltes agricoles ne sont jamais soumises à la Zakat", False),
                ("Elle ne se donne qu'au mois de Muharram", False),
            ],
        },
        {
            "texte": "Si un retardataire rejoint l'Imam dans la 2e Rak'ah de la prière de Subh (Fajr), doit-il réciter de nouveau le Qunût lorsqu'il rattrape sa 1re Rak'ah manquée s'il l'a déjà récité avec l'Imam ?",
            "type_question": "vrai_faux",
            "difficulte": "difficile",
            "points": 15,
            "explication": "Faux ! Comme l'explique le Cheikh, s'il a déjà accompli le Qunût derrière l'Imam, il ne le répète pas en rattrapant sa Rak'ah restante.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Parmi les 3 traditions (Sunan) de la Zakat, laquelle concerne la qualité du bien prélevé ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Les 3 traditions de la Zakat sont : la donner de bon cœur, choisir un bien de qualité moyenne (sans chercher à donner le pire ni exiger le plus précieux) et ne pas accompagner le don de reproches.",
            "choix": [
                ("Prélever sur des biens de qualité moyenne (ni les pires ni les plus précieux) et donner sans reproche", True),
                ("Donner uniquement les bêtes malades ou défectueuses", False),
                ("Annoncer publiquement le montant au marché pour être applaudi", False),
                ("Reporter la distribution de plusieurs années sans raison", False),
            ],
        },
    ],

    37: [  # CHAPITRE 5 — 15 questions intensives
        {
            "texte": "[Cas Pratique - Al-Ihsân] Un disciple demande la différence entre les deux degrés d'Al-Ihsân contenus dans la parole : « Adorer Allah comme si tu Le voyais, car si tu ne Le vois pas, Lui te voit ». Comment les maîtres du Tasawwuf nomment-ils ces deux degrés ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Le premier degré (« comme si tu Le voyais ») est Al-Mushâhadah (la Contemplation spirituelle), et le second degré (« Lui te voit ») est Al-Murâqabah (la Vigilance constante sous le regard d'Allah).",
            "choix": [
                ("Al-Mushâhadah (la Contemplation) et Al-Murâqabah (la Vigilance sous le regard divin)", True),
                ("Al-Qadâ' (la Réparation) et Al-Binâ' (la Continuité)", False),
                ("Ad-Dalk (le Frottement) et Al-Faur (l'Enchaînement)", False),
                ("Al-Jahr (la Voix haute) et As-Sirr (la Voix basse)", False),
            ],
        },
        {
            "texte": "Associez chacune des 5 opportunités précieuses de la vie à son contraire avant lequel il faut impérativement la saisir (Hadith des 5 avant 5) :",
            "type_question": "association",
            "difficulte": "facile",
            "points": 25,
            "explication": "Les 5 opportunités à saisir sont : la jeunesse avant la vieillesse, la santé avant la maladie, l'aisance avant l'indigence, le temps libre avant l'occupation et la vie avant la mort.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Ta jeunesse (Chabâbaka)", "droite": "Avant ta vieillesse (Haramika)"},
                    {"gauche": "Ta santé (Sihhataka)", "droite": "Avant ta maladie (Saqamika)"},
                    {"gauche": "Ton aisance (Ghinâka)", "droite": "Avant ton indigence (Faqrika)"},
                    {"gauche": "Ton temps libre (Farâghaka)", "droite": "Avant ton occupation (Chughlika)"},
                    {"gauche": "Ta vie (Hayâtaka)", "droite": "Avant ta mort (Mawtika)"},
                ]
            },
        },
        {
            "texte": "Associez chacune de ces nobles vertus soufies recommandées au Chapitre 5 à sa définition exacte :",
            "type_question": "association",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Al-Wara' est le scrupule pieux face au douteux, Al-Hilm la clémence et maîtrise de soi, Ach-Chukr la gratitude et Al-Ikhlâs la pureté d'intention.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Al-Wara' (Le Scrupule pieux)", "droite": "Délaisser ce qui est douteux par crainte de l'illicite"},
                    {"gauche": "Al-Hilm (La Clémence / Longanimité)", "droite": "Maîtriser sa colère et pardonner avec douceur"},
                    {"gauche": "Ach-Chukr (La Gratitude)", "droite": "Utiliser les bienfaits d'Allah dans Son obéissance"},
                    {"gauche": "Al-Ikhlâs (La Sincérité)", "droite": "Purifier ses actes de toute recherche d'éloge humain"},
                ]
            },
        },
        {
            "texte": "Quel terme arabe désigne le « Scrupule pieux » qui pousse le croyant à s'abstenir du douteux pour protéger sa religion ?",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Le scrupule pieux s'appelle Al-Wara' (الورع).",
            "donnees_extra": {"reponses_acceptees": ["wara", "wara'", "al-wara", "al-wara'", "al wara"]},
        },
        {
            "texte": "Selon Cheikh Ahmadou Bamba, un aspirant peut atteindre la perfection d'Al-Ihsân (le Soufisme) tout en abandonnant les règles du Fiqh (la Prière, le Jeûne) et du Tawhîd.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faux ! Le Cheikh enseigne que le Tasawwuf (Al-Ihsân) est le couronnement de l'Imân et de l'Islâm : quiconque prétend à la spiritualité en délaissant la Loi (Charî'ah) est dans l'illusion.",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Pourquoi l'aspirant véridique (Al-Murîd) doit-il confier son éducation spirituelle (At-Tarbiyah) à un Guide éclairé (Cheikh Murabbî) ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Parce que l'âme charnelle (An-Nafs) est sujette à des maladies subtiles (orgueil, illusion, ostentation) que seul un maître connaisseur d'Allah et fidèle à la Sunnah sait diagnostiquer et guérir.",
            "choix": [
                ("Pour diagnostiquer les maladies subtiles de l'âme (Nafs) et la conduire sur la voie droite vers Allah", True),
                ("Pour être dispensé d'apprendre ses obligations religieuses", False),
                ("Pour acquérir la renommée mondaine et la richesse matérielle", False),
                ("Parce que le Guide remplace le jugement d'Allah sans effort du disciple", False),
            ],
        },
        {
            "texte": "Dans la méthodologie de purification du cœur, comment appelle-t-on le fait de vider l'âme de ses vices (At-Takhallî) avant de l'orner des nobles vertus (At-Tahallî) ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 20,
            "explication": "L'éducation soufie procède par At-Takhallî (se débarrasser des maladies du cœur : orgueil, envie, ostentation) et At-Tahallî (se parer des vertus : sincérité, gratitude, générosité).",
            "choix": [
                ("At-Takhallî (la purification des vices) suivi d'At-Tahallî (l'ornementation par les vertus)", True),
                ("Al-Jahr suivi d'As-Sirr", False),
                ("Al-Madmadah suivi d'Al-Istinshâq", False),
                ("At-Tawâf suivi d'As-Sa'y", False),
            ],
        },
        {
            "texte": "Combien de vers au total compte le poème intégral Tazawwudu-ç-Çighâr composé par Cheikh Ahmadou Bamba ? (Répondez en chiffres)",
            "type_question": "texte_court",
            "difficulte": "facile",
            "points": 15,
            "explication": "L'ouvrage Tazawwudu-ç-Çighâr comporte exactement 308 vers.",
            "donnees_extra": {"reponses_acceptees": ["308", "308 vers", "trois cent huit"]},
        },
        {
            "texte": "La véritable Gratitude (Ach-Chukr) envers Allah se limite à prononcer « Al-Hamdulillâh » avec la langue, même si l'on utilise ses membres pour désobéir à Allah.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faux ! La gratitude complète unit le cœur (reconnaître que le bienfait vient d'Allah), la langue (Le louer) et les membres (employer Ses bienfaits dans Son obéissance et non dans le péché).",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Parmi les 5 opportunités à saisir, pourquoi la Jeunesse (Ach-Chabâb) est-elle citée en tout premier lieu dans Tazawwudu-ç-Çighâr ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Parce que la jeunesse est l'âge de la force, de la mémoire vive et de l'énergie pure : ce que l'on grave dans le cœur durant la jeunesse demeure solide toute la vie.",
            "choix": [
                ("Parce que c'est l'âge de la vigueur du corps et de la vivacité de la mémoire pour bâtir des fondations durables", True),
                ("Parce que les personnes âgées n'ont plus le droit de se repentir", False),
                ("Parce que les jeunes ne sont soumis à aucune obligation après la puberté", False),
                ("Uniquement pour des raisons de rime poétique", False),
            ],
        },
        {
            "texte": "Par quels deux actes spirituels bénis Cheikh Ahmadou Bamba clôture-t-il son ouvrage Tazawwudu-ç-Çighâr ?",
            "type_question": "qcm",
            "difficulte": "facile",
            "points": 15,
            "explication": "Conformément à la tradition prophétique, il clôture comme il a commencé : par la Louange à Allah (Al-Hamdulillâh) et la Prière et le Salut sur le Prophète Muhammad ﷺ, sa famille et ses Compagnons.",
            "choix": [
                ("Par la Louange à Allah (Hamd) et la Prière sur le Prophète Muhammad ﷺ, sa famille et ses Compagnons", True),
                ("Par un chapitre sur l'astronomie et la géométrie", False),
                ("Par une liste des rois de l'époque", False),
                ("Par les règles du commerce maritime", False),
            ],
        },
        {
            "texte": "La Science utile (Al-'Ilm) qui ne s'accompagne pas de la mise en pratique (Al-'Amal) et de la sincérité (Al-Ikhlâs) devient un argument contre son détenteur.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Vrai ! Le savoir en Islam est recherché pour être mis en pratique avec sincérité pour Allah.",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "Comment appelle-t-on en arabe l'âme charnelle qui incite au mal et à la paresse lorsqu'elle n'est pas éduquée ?",
            "type_question": "texte_court",
            "difficulte": "moyen",
            "points": 15,
            "explication": "L'âme charnelle est appelée An-Nafs (ou An-Nafs al-Ammârah bis-sû').",
            "donnees_extra": {"reponses_acceptees": ["nafs", "an-nafs", "al-nafs", "la nafs"]},
        },
        {
            "texte": "Quelle vertu est directement opposée à l'avarice (Al-Bukhl) et à l'attachement excessif aux biens de ce monde ?",
            "type_question": "qcm",
            "difficulte": "facile",
            "points": 15,
            "explication": "La générosité (Al-Jûd / As-Sakhâ') dépense volontiers pour la satisfaction d'Allah et le secours des créatures.",
            "choix": [
                ("La Générosité (Al-Jûd / As-Sakhâ')", True),
                ("L'Ostentation (Ar-Riyâ')", False),
                ("La Médisance (Al-Ghîbah)", False),
                ("L'Orgueil (Al-Kibr)", False),
            ],
        },
        {
            "texte": "L'ouvrage Tazawwudu-ç-Çighâr couvre successivement les 3 dimensions du Hadith de Jibrîl : Al-Imân (Chapitre 1), Al-Islâm (Chapitres 2, 3 et 4) et Al-Ihsân (Chapitre 5).",
            "type_question": "vrai_faux",
            "difficulte": "facile",
            "points": 15,
            "explication": "Vrai ! Toute l'architecture des 5 Grandes Étapes du livre suit fidèlement l'ordre des 3 piliers de la Religion : Imân, Islâm, Ihsân.",
            "choix": [("Vrai", True), ("Faux", False)],
        },
    ],

    38: [  # GRANDE RÉVISION FINALE (Lecon 99) — 15 questions transversales multi-formats supplémentaires
        {
            "texte": "[Synthèse Générale] Associez chacune des 5 Grandes Étapes de Tazawwudu-ç-Çighâr à sa plage de vers et à son thème central :",
            "type_question": "association",
            "difficulte": "difficile",
            "points": 25,
            "explication": "Les 308 vers se répartissent en 5 Grandes Étapes : Étape 1 (1-92 : Imân & Tawhîd), Étape 2 (93-163 : Bases de l'Islâm & Pureté), Étape 3 (164-205 : Prière & Purifications), Étape 4 (206-273 : Jeûne, Zakat, Hajj & Masbûq), Étape 5 (274-308 : Ihsân & Soufisme).",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Étape 1 (Vers 1 à 92)", "droite": "Fondations de la Foi (Al-Imân & At-Tawhîd)"},
                    {"gauche": "Étape 2 (Vers 93 à 163)", "droite": "Piliers de l'Islâm, 7 Membres & Tawbah"},
                    {"gauche": "Étape 3 (Vers 164 à 205)", "droite": "Obligations et Traditions de la Prière et des 3 Purifications"},
                    {"gauche": "Étape 4 (Vers 206 à 273)", "droite": "Jeûne, Zakat, Hajj et Rattrapage d'Al-Masbûq"},
                    {"gauche": "Étape 5 (Vers 274 à 308)", "droite": "Al-Ihsân, Vertus, Guide Spirituel et 5 Opportunités"},
                ]
            },
        },
        {
            "texte": "[Synthèse Chiffrée] Associez chaque domaine étudié dans le livre à son nombre exact d'éléments :",
            "type_question": "association",
            "difficulte": "difficile",
            "points": 25,
            "explication": "104 Livres révélés, 15 Farâ'id de la Prière, 18 Sunan de la Prière (dont 8 Mu'akkadah) et 7 Membres du corps à préserver.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Livres Célestes révélés (Suhuf + Grands Livres)", "droite": "104"},
                    {"gauche": "Actes Obligatoires (Farâ'id) de la Prière", "droite": "15"},
                    {"gauche": "Actes Traditionnels (Sunan) de la Prière", "droite": "18"},
                    {"gauche": "Membres du corps à préserver du péché", "droite": "7"},
                ]
            },
        },
        {
            "texte": "[Synthèse Purifications] Associez chacune des 3 purifications rituelles au nombre exact de ses Obligations (Farâ'id) et Traditions (Sunan) :",
            "type_question": "association",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Le Wudû' compte 7 Farâ'id et 8 Sunan ; le Ghusl 5 Farâ'id et 4 Sunan ; le Tayammum 8 Farâ'id et 3 Sunan.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "Ablutions mineures (Al-Wudû')", "droite": "7 Obligations et 8 Traditions"},
                    {"gauche": "Purification majeure (Al-Ghusl)", "droite": "5 Obligations et 4 Traditions"},
                    {"gauche": "Lustral pulvérulent (At-Tayammum)", "droite": "8 Obligations et 3 Traditions"},
                ]
            },
        },
        {
            "texte": "Combien d'Attributs nécessaires (Wâjib) à Allah tout croyant responsable doit-il connaître dans le chapitre du Tawhîd ? (Répondez en chiffre)",
            "type_question": "texte_court",
            "difficulte": "facile",
            "points": 15,
            "explication": "20 Attributs nécessaires à Allah (auxquels s'opposent 20 contraires impossibles, plus 1 statut possible = 41).",
            "donnees_extra": {"reponses_acceptees": ["20", "vingt", "20 attributs"]},
        },
        {
            "texte": "Quel juriste malikite classique Cheikh Ahmadou Bamba cite-t-il comme référence dans son exposé des obligations et traditions de la prière et de la purification ?",
            "type_question": "texte_court",
            "difficulte": "difficile",
            "points": 20,
            "explication": "Il cite l'érudit malikite Al-'Awfî (العوفي).",
            "donnees_extra": {"reponses_acceptees": ["al-awfi", "awfi", "al-'awfi", "al awfi", "el awfi"]},
        },
        {
            "texte": "Dans la prière, le frottement (Ad-Dalk) et la continuité (Al-Faur) sont des obligations des ablutions (Wudû') et du bain rituel (Ghusl).",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Vrai ! En Fiqh malikite, Ad-Dalk et Al-Faur sont des obligations (Farâ'id) aussi bien dans le Wudû' que dans le Ghusl.",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "[Cas Pratique Transversal] Un jeune musulman prie avec un vêtement propre et des ablutions complètes, mais il accomplit sa prière dans le seul but d'être complimenté par ses amis pour sa piété. Quelle condition fondamentale du Chapitre 2 a-t-il rompue ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 20,
            "explication": "Il a rompu la 1re des 4 puretés : la pureté de l'âme (Al-Ikhlâs), en tombant dans l'ostentation (Ar-Riyâ').",
            "choix": [
                ("La pureté de l'âme (Al-Ikhlâs), car l'ostentation (Riyâ') annule la récompense de l'œuvre", True),
                ("La pureté du lieu de prière", False),
                ("L'obligation du frottement (Ad-Dalk)", False),
                ("La règle du rattrapage d'Al-Masbûq", False),
            ],
        },
        {
            "texte": "[Cas Pratique Transversal] Un fidèle arrive à la mosquée pour la prière de Zuhr alors que l'Imam vient de se relever de l'inclinaison (Rukû') de la 2e Rak'ah. Combien de Rak'ah ce fidèle aura-t-il validées avec l'Imam à la fin de la prière de Zuhr (4 Rak'ah) ?",
            "type_question": "qcm",
            "difficulte": "difficile",
            "points": 25,
            "explication": "Comme l'Imam s'était déjà redressé du Rukû' de la 2e Rak'ah, le fidèle a manqué la 1re et la 2e Rak'ah ! Il ne valide avec l'Imam que la 3e et la 4e Rak'ah (soit 2 Rak'ah validées et 2 Rak'ah à rattraper).",
            "choix": [
                ("2 Rak'ah validées (la 3e et la 4e), et il devra rattraper les 2 premières Rak'ah après le Salâm de l'Imam", True),
                ("3 Rak'ah validées, car il a rejoint l'Imam avant la prosternation de la 2e Rak'ah", False),
                ("4 Rak'ah validées, il n'a rien à rattraper", False),
                ("Aucune Rak'ah validée, il doit attendre la prière de 'Asr", False),
            ],
        },
        {
            "texte": "Associez chaque Livre Céleste au Prophète sur qui il a été descendu :",
            "type_question": "association",
            "difficulte": "facile",
            "points": 20,
            "explication": "La Tawrât à Mûsâ, le Zabûr à Dâwûd, l'Injîl à 'Îsâ et Al-Furqân (le Coran) à Muhammad ﷺ.",
            "donnees_extra": {
                "paires": [
                    {"gauche": "At-Tawrât (La Torah)", "droite": "Mûsâ (Moïse)"},
                    {"gauche": "Az-Zabûr (Les Psaumes)", "droite": "Dâwûd (David)"},
                    {"gauche": "Al-Injîl (L'Évangile)", "droite": "'Îsâ (Jésus)"},
                    {"gauche": "Al-Furqân (Le Coran)", "droite": "Muhammad ﷺ"},
                ]
            },
        },
        {
            "texte": "Lequel de ces actes fait partie des 15 obligations (Farâ'id) de la Prière et NON des Sunan ?",
            "type_question": "qcm",
            "difficulte": "moyen",
            "points": 15,
            "explication": "La récitation de la Fâtihah est un pilier obligatoire (Fard), alors que la Sourate suivante, le Tashahhud et les Takbîrs secondaires sont des Sunnah Mu'akkadah.",
            "choix": [
                ("La récitation de la Fâtihah et l'accalmie (At-Tuma'nînah)", True),
                ("La récitation d'une Sourate après la Fâtihah", False),
                ("Le premier et le second Tashahhud", False),
                ("Dire « Sami'a Allâhu liman hamidah »", False),
            ],
        },
        {
            "texte": "Dans la Zakat, il est permis de transférer l'aumône vers une région lointaine alors que des pauvres nécessiteux se trouvent sur le lieu même du prélèvement.",
            "type_question": "vrai_faux",
            "difficulte": "moyen",
            "points": 15,
            "explication": "Faux ! La 4e obligation de la Zakat interdit de la transférer au-delà de la distance de raccourcissement de la prière tant qu'il y a des ayants droit sur place (sauf besoin beaucoup plus pressant ailleurs).",
            "choix": [("Vrai", False), ("Faux", True)],
        },
        {
            "texte": "Quel est le nombre total d'articles de la Foi (Arkân al-Imân) exposés dans le Chapitre 1 ? (Répondez en chiffre)",
            "type_question": "texte_court",
            "difficulte": "facile",
            "points": 10,
            "explication": "Les 6 articles de la Foi : croire en Allah, en Ses Anges, en Ses Livres, en Ses Envoyés, au Jour Ultime et au Décret Divin.",
            "donnees_extra": {"reponses_acceptees": ["6", "six", "6 articles", "6 piliers"]},
        },
        {
            "texte": "Quelle est la signification française exacte du titre « Tazawwudu-ç-Çighâr » donné par Cheikh Ahmadou Bamba à cet ouvrage ?",
            "type_question": "qcm",
            "difficulte": "facile",
            "points": 15,
            "explication": "At-Tazawwud signifie l'approvisionnement en viatique (provisions de voyage pour l'Au-delà), et Aç-Çighâr désigne les jeunes / adolescents : « Le Viatique des Adolescents ».",
            "choix": [
                ("Le Viatique des Adolescents (ou l'approvisionnement spirituel de la jeunesse)", True),
                ("Le Livre des Conquêtes Militaires", False),
                ("Le Traité de l'Agriculture et des Pluies", False),
                ("L'Histoire des Anciens Empires", False),
            ],
        },
        {
            "texte": "Le premier Tashahhud et le second Tashahhud dans la prière ont le statut juridique de Sunnah Mu'akkadah (tradition fortement recommandée), tandis que l'assise pour le Salut final est un Fard.",
            "type_question": "vrai_faux",
            "difficulte": "difficile",
            "points": 15,
            "explication": "Vrai ! En Fiqh malikite, le texte du Tashahhud et la première assise sont des Sunnah Mu'akkadah, tandis que la durée de l'assise permettant de prononcer le Salut final (Al-Julûs lis-Salâm) est un Fard.",
            "choix": [("Vrai", True), ("Faux", False)],
        },
        {
            "texte": "Quel est le nom de l'Ange chargé de souffler dans la Trompe (As-Sûr) pour annoncer la fin du monde et la Résurrection ?",
            "type_question": "texte_court",
            "difficulte": "facile",
            "points": 15,
            "explication": "L'Ange Isrâfîl est chargé de souffler dans la Trompe (As-Sûr).",
            "donnees_extra": {"reponses_acceptees": ["israfil", "isrâfîl", "ange israfil"]},
        },
    ],
}


def run():
    updated_dossiers = 0
    created_questions = 0

    for lecon_id, data in DOSSIERS_REVISIONS.items():
        lecon = TazawwudLecon.objects.filter(id=lecon_id).first()
        if not lecon:
            continue
        lecon.titre = data["titre"]
        lecon.texte_source = data["texte_source"]
        lecon.explication = data["explication"]
        lecon.a_retenir = data["a_retenir"]
        lecon.save()
        updated_dossiers += 1

        # Ajouter les questions intensives sans dupliquer si déjà présentes
        questions_list = QUESTIONS_INTENSIVES.get(lecon_id, [])
        for idx, q_data in enumerate(questions_list, start=1):
            q_obj, created = TazawwudQuestion.objects.update_or_create(
                lecon=lecon,
                texte=q_data["texte"],
                defaults={
                    "type_question": q_data["type_question"],
                    "difficulte": q_data["difficulte"],
                    "points": q_data["points"],
                    "explication_reponse": q_data["explication"],
                    "donnees_extra": q_data.get("donnees_extra", {}),
                    "ordre": idx,
                },
            )
            if "choix" in q_data:
                q_obj.choix.all().delete()
                for c_texte, c_correct in q_data["choix"]:
                    TazawwudChoix.objects.create(
                        question=q_obj,
                        texte=c_texte,
                        est_correct=c_correct,
                    )
            if created:
                created_questions += 1

    total_q = TazawwudQuestion.objects.count()
    print(
        f"Contenu des paiements enrichi avec succès : {updated_dossiers} dossiers de révision intensive mis à jour, "
        f"{created_questions} nouvelles questions intensives créées (Banque totale = {total_q} questions)."
    )


if __name__ == "__main__":
    run()
