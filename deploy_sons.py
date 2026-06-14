import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Son

SONS_DATA = [
    {
        "titre": "yamane yaroumo kourel1 Dmb touba alieu gamou 2025",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/yamane yaroumo kourel1 Dmb touba alieu gamou 2025.mp3"
    },
    {
        "titre": "diawartou kourel1 mafatihoul bichri touba alieu ga",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/diawartou kourel1 mafatihoul bichri touba alieu ga.mp3"
    },
    {
        "titre": "YAKHINII WKSM KOUREL 1 TOUTANK HTDKH 16 JOUR RAMADAN 2026",
        "auteur_voix": "Kourel 1 TOUTANK HTDKH",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/YAKHINII WKSM KOUREL 1 TOUTANK HTDKH 16 JOUR RAMADAN 2026.mp3"
    },
    {
        "titre": "Wawasaynal Insaana - Sgne Abdoul Ahad Toure",
        "auteur_voix": "Sgne Abdoul Ahad Toure",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Wawasaynal Insaana - Sgne Abdoul Ahad Toure.mp3"
    },
    {
        "titre": "Walajtu Wuluujan - Wa Keur Sgne Massamba",
        "auteur_voix": "Wa Keur Sgne Massamba",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Walajtu Wuluujan - Wa Keur Sgne Massamba.mp3"
    },
    {
        "titre": "Wajaba Hamdul Xaaliqi - Sgne Moussa Gueye Ndar",
        "auteur_voix": "Sgne Moussa Gueye Ndar",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Wajaba Hamdul Xaaliqi - Sgne Moussa Gueye Ndar.mp3"
    },
    {
        "titre": "Ndiarignou Xassida yi Serigne Abdou Rahmane ",
        "auteur_voix": "Serigne Abdou Rahmane",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Ndiarignou Xassida yi Serigne Abdou Rahmane .mp3"
    },
    {
        "titre": "Muhammadun - Sgne Modou DIOP",
        "auteur_voix": "Sgne Modou DIOP",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Muhammadun - Sgne Modou DIOP.mp3"
    },
    {
        "titre": "Midaadi - Sgne Youssou Ndao",
        "auteur_voix": "Sgne Youssou Ndao",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Midaadi - Sgne Youssou Ndao.mp3"
    },
    {
        "titre": "Matlabul Fawzeyni Kurel 1 Kaolack HTDKH C\u00e9l\u00e9\ud835\udc1b\ud835\udc2b\ud835\udc1a\ud835\udc2d\ud835\udc22\ud835\udc28\ud835\udc27 \ud835\udc1d\ud835\udc2e \ud835\udc0c\ud835\udc1a\ud835\udc30\ud835\udc25\ud835\udc22\ud835\udc1d\ud835\udc2e \ud835\udc0d\ud835\udc1a\ud835\udc1b\ud835\udc22",
        "auteur_voix": "Kurel 1 Kaolack HTDKH",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Matlabul_Fawzeyni_Kurel_1_Kaolack_HTDKH_C\u00e9l\u00e9\ud835\udc1b\ud835\udc2b\ud835\udc1a\ud835\udc2d\ud835\udc22\ud835\udc28\ud835\udc27_\ud835\udc1d\ud835\udc2e_\ud835\udc0c\ud835\udc1a\ud835\udc30\ud835\udc25\ud835\udc22\ud835\udc1d\ud835\udc2e_\ud835\udc0d\ud835\udc1a\ud835\udc1b\ud835\udc22.m4a"
    },
    {
        "titre": "Mafatihul Djinane Kurel 1 Kaolack HTDKH C\u00e9l\u00e9\ud835\udc1b\ud835\udc2b\ud835\udc1a\ud835\udc2d\ud835\udc22\ud835\udc28\ud835\udc27 \ud835\udc1d\ud835\udc2e \ud835\udc0c\ud835\udc1a\ud835\udc30\ud835\udc25\ud835\udc22\ud835\udc1d\ud835\udc2e \ud835\udc0d\ud835\udc1a\ud835\udc1b\ud835\udc22",
        "auteur_voix": "Kurel 1 Kaolack HTDKH",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Mafatihul_Djinane_Kurel_1_Kaolack_HTDKH_C\u00e9l\u00e9\ud835\udc1b\ud835\udc2b\ud835\udc1a\ud835\udc2d\ud835\udc22\ud835\udc28\ud835\udc27_\ud835\udc1d\ud835\udc2e_\ud835\udc0c\ud835\udc1a\ud835\udc30\ud835\udc25\ud835\udc22\ud835\udc1d\ud835\udc2e_\ud835\udc0d\ud835\udc1a\ud835\udc1b\ud835\udc22.m4a"
    },
    {
        "titre": "Madal Khabirou Lissanou Choukry Kourel Taverny Journ\u00e9e Cheikh Ahmadou",
        "auteur_voix": "Kourel Taverny",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Madal_Khabirou_Lissanou_Choukry_Kourel_Taverny_Journ\u00e9e_Cheikh_Ahmadou.mp3"
    },
    {
        "titre": "J30 YAZALBUCHARATY RABBI WKSM KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J30 YAZALBUCHARATY_RABBI WKSM KUREL ASNA KHADIM HT.mp3"
    },
    {
        "titre": "J30 MIDADI WKSM KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J30 MIDADI WKSM KUREL ASNA KHADIM HT.mp3"
    },
    {
        "titre": "J30 LAMYABDU S M SY KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J30 LAMYABDU S M SY KUREL ASNA KHADIM HT.mp3"
    },
    {
        "titre": "J30 FARIJ HT KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J30 FARIJ HT KUREL ASNA KHADIM HT.mp3"
    },
    {
        "titre": "J29 JAALIBATUL MARAKHIB S TAFSIR DIOP KUREL SERIGNE ABDUL AHAD MBACKE",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J29_JAALIBATUL_MARAKHIB_S_TAFSIR_DIOP_KUREL_SERIGNE_ABDUL_AHAD_MBACKE.mp3"
    },
    {
        "titre": "J29 LAMYABDU S M SY KUREL SERIGNE ABDUL AHAD MBACKE HT",
        "auteur_voix": "Kurel SERIGNE ABDUL AHAD MBACKE HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J29 LAMYABDU S M SY KUREL SERIGNE ABDUL AHAD MBACKE HT.mp3"
    },
    {
        "titre": "J29 FARIJ  HT KUREL SERIGNE ABDUL AHAD MBACKE HT",
        "auteur_voix": "Kurel SERIGNE ABDUL AHAD MBACKE HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J29 FARIJ  HT KUREL SERIGNE ABDUL AHAD MBACKE HT.mp3"
    },
    {
        "titre": "J28 LAYANTAHI LAMYANKHU S TAFSIR DIOP KUREL MAFATIHUL BICHRI HT",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J28_LAYANTAHI_LAMYANKHU_S_TAFSIR_DIOP_KUREL_MAFATIHUL_BICHRI_HT.mp3"
    },
    {
        "titre": "J28 LAMYABDU CHAHRU RAMADAN S M SY KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J28_LAMYABDU_CHAHRU_RAMADAN_S_M_SY_KUREL_MAFATIHUL_BICHRI_HT_DAKAR.mp3"
    },
    {
        "titre": "J28 YAZALBUCHARATI S CISSE KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J28 YAZALBUCHARATI S CISSE KUREL MAFATIHUL BICHRI HT DAKAR.mp3"
    },
    {
        "titre": "J28 LILLAHIKULIYATI S M SY KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J28 LILLAHIKULIYATI S M SY KUREL MAFATIHUL BICHRI HT DAKAR.mp3"
    },
    {
        "titre": "J28 FARIJ HT KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J28 FARIJ HT KUREL MAFATIHUL BICHRI HT DAKAR.mp3"
    },
    {
        "titre": "J28 BUCHRALANA S CISSE KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J28 BUCHRALANA S CISSE KUREL MAFATIHUL BICHRI HT DAKAR.mp3"
    },
    {
        "titre": "J28 AHBABTU WKSM KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J28 AHBABTU WKSM KUREL MAFATIHUL BICHRI HT DAKAR.mp3"
    },
    {
        "titre": "J27 LAMYABDU CHAHRU RAMADAN S M SY KUREL WAKEUR SERIGNE MASSAMBA",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J27_LAMYABDU_CHAHRU_RAMADAN_S_M_SY_KUREL_WAKEUR_SERIGNE_MASSAMBA.mp3"
    },
    {
        "titre": "J27 ASTAHFIRULAHI BIHI S M SY KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J27_ASTAHFIRULAHI_BIHI_S_M_SY_KUREL_WAKEUR_SERIGNE_MASSAMBA_HT.mp3"
    },
    {
        "titre": "J27 RABBI WKSM KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J27 RABBI WKSM KUREL WAKEUR SERIGNE MASSAMBA HT.mp3"
    },
    {
        "titre": "J27 MAWAHIBOU WKSM KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J27 MAWAHIBOU WKSM KUREL WAKEUR SERIGNE MASSAMBA HT.mp3"
    },
    {
        "titre": "J27 FARIJ HT KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J27 FARIJ HT KUREL WAKEUR SERIGNE MASSAMBA HT.mp3"
    },
    {
        "titre": "J26 YAAMOUKRIMA ZALAT S CISSE KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J26_YAAMOUKRIMA_ZALAT_S_CISSE_KUREL_NURUD_DARAYNI_HT_RUFISQUE.mp3"
    },
    {
        "titre": "J26 LAMYABDU S M LAMINE GUEYE KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J26_LAMYABDU_S_M_LAMINE_GUEYE_KUREL_NURUD_DARAYNI_HT_RUFISQUE.mp3"
    },
    {
        "titre": "J26 YAAZAL BUCHARATY WKSM KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J26 YAAZAL BUCHARATY WKSM KUREL NURUD DARAYNI HT RUFISQUE.mp3"
    },
    {
        "titre": "J26 RUMNA S MB DIOP KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J26 RUMNA S MB DIOP KUREL NURUD DARAYNI HT RUFISQUE.mp3"
    },
    {
        "titre": "J26 MAN ZANANI S M SY KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J26 MAN ZANANI S M SY KUREL NURUD DARAYNI HT RUFISQUE.mp3"
    },
    {
        "titre": "J26 FARIJ HT KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J26 FARIJ HT KUREL NURUD DARAYNI HT RUFISQUE.mp3"
    },
    {
        "titre": "J26 ALAA INANI S A FALL KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J26 ALAA INANI S A FALL KUREL NURUD DARAYNI HT RUFISQUE.mp3"
    },
    {
        "titre": "J25 LAMYABDU FAZALLAZI S TAFSIR DIOP KUREL SERIGNE SALIOU MBACKE",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J25_LAMYABDU_FAZALLAZI_S_TAFSIR_DIOP_KUREL_SERIGNE_SALIOU_MBACKE.mp3"
    },
    {
        "titre": "J25 RABIYAH AHMADU HT KUREL SERIGNE SALIOU MBACKE HT",
        "auteur_voix": "Kurel SERIGNE SALIOU MBACKE HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J25 RABIYAH AHMADU HT KUREL SERIGNE SALIOU MBACKE HT.mp3"
    },
    {
        "titre": "J25 FARIJ HT KUREL SERIGNE SALIOU MBACKE HT",
        "auteur_voix": "Kurel SERIGNE SALIOU MBACKE HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J25 FARIJ HT KUREL SERIGNE SALIOU MBACKE HT.mp3"
    },
    {
        "titre": "J25 AJABANI WKSM  KUREL SERIGNE SALIOU MBACKE HT",
        "auteur_voix": "Kurel SERIGNE SALIOU MBACKE HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J25 AJABANI WKSM  KUREL SERIGNE SALIOU MBACKE HT.mp3"
    },
    {
        "titre": "J24 WALAQAD KARAMNA S M DIOP KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J24_WALAQAD_KARAMNA_S_M_DIOP_KUREL_MAFATIHUL_BICHRI_HT_RUFISQUE.mp3"
    },
    {
        "titre": "J24 MATLABUS CHIFAHI S TAFSIR DIOP KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J24_MATLABUS_CHIFAHI_S_TAFSIR_DIOP_KUREL_MAFATIHUL_BICHRI_HT_RUFISQUE.mp3"
    },
    {
        "titre": "J24 LAMYABDU S M SY KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J24 LAMYABDU S M SY KUREL MAFATIHUL BICHRI HT RUFISQUE.mp3"
    },
    {
        "titre": "J24 INNILAKHILLUN WKSM KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J24 INNILAKHILLUN WKSM KUREL MAFATIHUL BICHRI HT RUFISQUE.mp3"
    },
    {
        "titre": "J24 FARIJ HT KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J24 FARIJ HT KUREL MAFATIHUL BICHRI HT RUFISQUE.mp3"
    },
    {
        "titre": "J24 BUCHRALANAA S A FALL KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J24 BUCHRALANAA S A FALL KUREL MAFATIHUL BICHRI HT RUFISQUE.mp3"
    },
    {
        "titre": "J24 ALLAHU BARRUN S CISSE KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J24 ALLAHU BARRUN S CISSE KUREL MAFATIHUL BICHRI HT RUFISQUE.mp3"
    },
    {
        "titre": "J23 TAYSIRUL ASSIR S TAFSIR DIOP KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J23_TAYSIRUL_ASSIR_S_TAFSIR_DIOP_KUREL_NURUD_DARAYNI_HT_THIES.mp3"
    },
    {
        "titre": "J23 ILAANABIYIN S MASSAMBA NIASS KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J23_ILAANABIYIN_S_MASSAMBA_NIASS_KUREL_NURUD_DARAYNI_HT_THIES.mp3"
    },
    {
        "titre": "J23 FARJI HT KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J23 FARJI HT KUREL NURUD DARAYNI HT THIES.mp3"
    },
    {
        "titre": "J23 AHBABTU WKSM KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J23 AHBABTU WKSM KUREL NURUD DARAYNI HT THIES.mp3"
    },
    {
        "titre": "J23 AHANZANI S M SY KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J23 AHANZANI S M SY KUREL NURUD DARAYNI HT THIES.mp3"
    },
    {
        "titre": "J22 MADALKHABIROU LISSANU CHUKRY WA NDIAREME KUREL NURUD DARAYNI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22_MADALKHABIROU_LISSANU_CHUKRY_WA_NDIAREME_KUREL_NURUD_DARAYNI.mp3"
    },
    {
        "titre": "J22 LAMYABDU CHAHRU RAMADAN S SALIOU MBACKE KUREL NURUD DARAYNI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22_LAMYABDU_CHAHRU_RAMADAN_S_SALIOU_MBACKE_KUREL_NURUD_DARAYNI.mp3"
    },
    {
        "titre": "J22 BISMILAHI LAZI S CH GUEYE MAHIB KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22_BISMILAHI_LAZI_S_CH_GUEYE_MAHIB_KUREL_NURUD_DARAYNI_HT_TOUBA.mp3"
    },
    {
        "titre": "J22 AHMADU MUHNIYAN YASAYIDI S TAFSIR DIOP KUREL NURUD DARAYNI HT",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22_AHMADU_MUHNIYAN_YASAYIDI_S_TAFSIR_DIOP_KUREL_NURUD_DARAYNI_HT.mp3"
    },
    {
        "titre": "J22 YASAYIDI  S TAFSIR DIOP KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22 YASAYIDI  S TAFSIR DIOP KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J22 YAMUKRIMA DAYFI WKSM KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22 YAMUKRIMA DAYFI WKSM KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J22 QALU S ALIOUNE FALL KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22 QALU S ALIOUNE FALL KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J22 MAHAWTAL S A KHADRE SEYE KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22 MAHAWTAL S A KHADRE SEYE KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J22 FAZAT QILAMI S MODOU THIAM  KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22 FAZAT QILAMI S MODOU THIAM  KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J22 BISMILLAHIL KARIM S CISSE KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J22 BISMILLAHIL KARIM S CISSE KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J21 LAMYABDU CHAHRU RAMADAN S BASSIROU SENE KUREL NURUD DARAYNI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J21_LAMYABDU_CHAHRU_RAMADAN_S_BASSIROU_SENE_KUREL_NURUD_DARAYNI.mp3"
    },
    {
        "titre": "J21 YAAZALWUDIOUDI S A DIOP KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J21 YAAZALWUDIOUDI S A DIOP KUREL NURUD DARAYNI HT DAKAR.mp3"
    },
    {
        "titre": "J21 WAAJAKHAT NI  S M THIAM KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J21 WAAJAKHAT NI  S M THIAM KUREL NURUD DARAYNI HT DAKAR.mp3"
    },
    {
        "titre": "J21 INI AQULU S MATAR MBAYE KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J21 INI AQULU S MATAR MBAYE KUREL NURUD DARAYNI HT DAKAR.mp3"
    },
    {
        "titre": "J21 HUQQA WKSM KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J21 HUQQA WKSM KUREL NURUD DARAYNI HT DAKAR.mp3"
    },
    {
        "titre": "J21 FARIJ HT KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J21 FARIJ HT KUREL NURUD DARAYNI HT DAKAR.mp3"
    },
    {
        "titre": "J21 FARIHA FARIHA WKSM KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J21 FARIHA_FARIHA WKSM KUREL NURUD DARAYNI HT DAKAR.mp3"
    },
    {
        "titre": "J20 TAWBATU NACOUH S MBAYE DIOP KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J20_TAWBATU_NACOUH_S_MBAYE_DIOP_KUREL_TAZAWUDUS_SIKHAR_HT_DAKAR.mp3"
    },
    {
        "titre": "J20 INNALLAZINA S BOLLE MBAYE KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J20_INNALLAZINA_S_BOLLE_MBAYE_KUREL_TAZAWUDUS_SIKHAR_HT_DAKAR.mp3"
    },
    {
        "titre": "J20 ALAA INANI HUZNY S ALIOUNE FALL KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J20_ALAA_INANI_HUZNY_S_ALIOUNE_FALL_KUREL_TAZAWUDUS_SIKHAR_HT_DAKAR.mp3"
    },
    {
        "titre": "J20 FAZALAZINA S IBRAHIMA LO KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J20 FAZALAZINA S IBRAHIMA LO KUREL TAZAWUDUS SIKHAR HT DAKAR.mp3"
    },
    {
        "titre": "J20 FARIJ HT KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J20 FARIJ HT KUREL TAZAWUDUS SIKHAR HT DAKAR.mp3"
    },
    {
        "titre": "J20 ATAABA S BOLLE MBAYE KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J20 ATAABA S BOLLE MBAYE KUREL TAZAWUDUS SIKHAR HT DAKAR.mp3"
    },
    {
        "titre": "J19 MIDADI WA AQLAMI S BOLLE MBAYE KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19_MIDADI_WA_AQLAMI_S_BOLLE_MBAYE_KUREL_MAFATIHUL_BICHRI_HT_TOUBA.mp3"
    },
    {
        "titre": "J19 LISSANU CHUKRY MADALKHABIRU S DAME LO KUREL MAFATIHUL BICHRI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19_LISSANU_CHUKRY_MADALKHABIRU_S_DAME_LO_KUREL_MAFATIHUL_BICHRI.mp3"
    },
    {
        "titre": "J19 LAMYABDU CHAHRU RAMADAN HT KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19_LAMYABDU_CHAHRU_RAMADAN_HT_KUREL_MAFATIHUL_BICHRI_HT_TOUBA.mp3"
    },
    {
        "titre": "J19 AHBABTU FATAHA FUZTY WKSM KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19_AHBABTU_FATAHA_FUZTY_WKSM_KUREL_MAFATIHUL_BICHRI_HT_TOUBA.mp3"
    },
    {
        "titre": "J19 YAAMOUKRIMA WKSM KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19 YAAMOUKRIMA WKSM KUREL MAFATIHUL BICHRI HT TOUBA.mp3"
    },
    {
        "titre": "J19 MINALKHADIMI S MB DIOP KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19 MINALKHADIMI S MB DIOP KUREL MAFATIHUL BICHRI HT TOUBA.mp3"
    },
    {
        "titre": "J19 LIHALAMALNAZIRU S M SY KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19 LIHALAMALNAZIRU S M SY KUREL MAFATIHUL BICHRI HT TOUBA.mp3"
    },
    {
        "titre": "J19 FARIJ HT KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J19 FARIJ HT KUREL MAFATIHUL BICHRI HT TOUBA.mp3"
    },
    {
        "titre": "J18 LAMYABDU S MBAYE DIOP KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J18_LAMYABDU_S_MBAYE_DIOP_KUREL_NURUD_DARAYNI_HT_DAROU_MANANE.mp3"
    },
    {
        "titre": "J18 CHAHRU RAMADAN S M SY KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J18_CHAHRU_RAMADAN_S_M_SY_KUREL_NURUD_DARAYNI_HT_DAROU_MANANE.mp3"
    },
    {
        "titre": "J18 MAWAHIBOU WKSM KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J18 MAWAHIBOU WKSM KUREL NURUD DARAYNI HT DAROU MANANE.mp3"
    },
    {
        "titre": "J18 FARIJ HT KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J18 FARIJ HT KUREL NURUD DARAYNI HT DAROU MANANE.mp3"
    },
    {
        "titre": "J18 BISMILAHILAZI WKSM KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J18 BISMILAHILAZI WKSM KUREL NURUD DARAYNI HT DAROU MANANE.mp3"
    },
    {
        "titre": "J17 JAZBU WKSM KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J17 JAZBU WKSM KUREL ASNA KHADIM HT.mp3"
    },
    {
        "titre": "J17 FARIJ HT KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J17 FARIJ HT KUREL ASNA KHADIM HT.mp3"
    },
    {
        "titre": "J02 MATLABU FAWZAYNI S TAFSIR DIOP KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J02_MATLABU_FAWZAYNI_S_TAFSIR_DIOP_KUREL_NURUD_DARAYNI_HT_TOUBA.mp3"
    },
    {
        "titre": "J02 YAKHAYRA S MODOU DEME KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J02 YAKHAYRA S MODOU DEME KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J02 MADALMUNA S CHEIKH LO KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J02 MADALMUNA S CHEIKH LO KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J02 MADADTU WKSM KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J02 MADADTU WKSM KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J02 LAMYABDOU S MBAYE DIOP KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J02 LAMYABDOU S MBAYE DIOP KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J02 KHASSIDA RAMADAN HT KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J02 KHASSIDA RAMADAN HT KUREL NURUD DARAYNI HT TOUBA.mp3"
    },
    {
        "titre": "J01 HADAA IQUL FADAA IL S TAFSIR DIOP KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J01_HADAA_IQUL_FADAA_IL_S_TAFSIR_DIOP_KUREL_MACHRABUS_CHAFI_HT.mp3"
    },
    {
        "titre": "J01 YAKHAYRA WKSM KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J01 YAKHAYRA WKSM KUREL MACHRABUS CHAFI HT.mp3"
    },
    {
        "titre": "J01 MATLABU CHIFAHI  S TAFSIR DIOP KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J01 MATLABU CHIFAHI  S TAFSIR DIOP KUREL MACHRABUS CHAFI HT.mp3"
    },
    {
        "titre": "J01 LAMYABDU S M SY KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J01 LAMYABDU S M SY KUREL MACHRABUS CHAFI HT.mp3"
    },
    {
        "titre": "J01 FARIJ HT KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J01 FARIJ HT KUREL MACHRABUS CHAFI HT.mp3"
    },
    {
        "titre": "J01 BICHAHRI RAMADAN S M L GUEYE KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/J01 BICHAHRI RAMADAN S M L GUEYE KUREL MACHRABUS CHAFI HT.mp3"
    },
    {
        "titre": "Huqqal Bukaa-u  -  Sgne Moustapha Diop",
        "auteur_voix": "Sgne Moustapha Diop",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/Huqqal Bukaa-u  -  Sgne Moustapha Diop.mp3"
    },
    {
        "titre": "ASSIROU S A KH GASSAMA KOUREL 1 TOUTANK HTDKH 16 JOUR RAMADAN 2026",
        "auteur_voix": "Kourel 1 TOUTANK HTDKH",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/ASSIROU_S_A_KH_GASSAMA_KOUREL_1_TOUTANK_HTDKH_16_JOUR_RAMADAN_2026.mp3"
    },
    {
        "titre": "02 Jeunesse et l'islam",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/Khassida Ramadan 2026/02 Jeunesse et l'islam.mp3"
    },
    {
        "titre": "Achinu - Kurel Asnal Khadim HT",
        "auteur_voix": "Kurel Asnal Khadim HT",
        "categorie": "KHASSIDA",
        "fichier_audio": "audios/khassida/ACHINU_WKSM_KUREL_ASNAL_KHADIM_HT.mp3"
    }
]

def run():
    print("Insertion des sons dans la base de donnees de production...")
    for item in SONS_DATA:
        obj, created = Son.objects.get_or_create(
            titre=item['titre'],
            defaults={
                'auteur_voix': item['auteur_voix'],
                'categorie': item['categorie'],
                'fichier_audio': item['fichier_audio']
            }
        )
        if created:
            print(f"Ajouté : {item['titre']}")
        else:
            # Update to ensure file path is correct
            obj.fichier_audio = item['fichier_audio']
            obj.auteur_voix = item['auteur_voix']
            obj.save()
            print(f"Mis à jour : {item['titre']}")
    
    print("Tous les sons ont été synchronisés.")

if __name__ == '__main__':
    run()
