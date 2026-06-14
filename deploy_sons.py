import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Son

SONS_DATA = [
    {
        "titre": "Achinu - Kurel Asnal Khadim HT",
        "auteur_voix": "Kurel Asnal Khadim HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476589/media/audios/khassida/ACHINU_WKSM_KUREL_ASNAL_KHADIM_HT.mp3.mp3"
    },
    {
        "titre": "02 Jeunesse et l'islam",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476636/media/audios/khassida/Khassida%20Ramadan%202026/02%20Jeunesse%20et%20l%27islam.mp3.mp3"
    },
    {
        "titre": "ASSIROU S A KH GASSAMA KOUREL 1 TOUTANK HTDKH 16 JOUR RAMADAN 2026",
        "auteur_voix": "Kourel 1 TOUTANK HTDKH",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476644/media/audios/khassida/Khassida%20Ramadan%202026/ASSIROU_S_A_KH_GASSAMA_KOUREL_1_TOUTANK_HTDKH_16_JOUR_RAMADAN_2026.mp3.mp3"
    },
    {
        "titre": "Huqqal Bukaa-u  -  Sgne Moustapha Diop",
        "auteur_voix": "Sgne Moustapha Diop",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476700/media/audios/khassida/Khassida%20Ramadan%202026/Huqqal%20Bukaa-u%20%20-%20%20Sgne%20Moustapha%20Diop.mp3.mp3"
    },
    {
        "titre": "J01 BICHAHRI RAMADAN S M L GUEYE KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476713/media/audios/khassida/Khassida%20Ramadan%202026/J01%20BICHAHRI%20RAMADAN%20S%20M%20L%20GUEYE%20KUREL%20MACHRABUS%20CHAFI%20HT.mp3.mp3"
    },
    {
        "titre": "J01 FARIJ HT KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476720/media/audios/khassida/Khassida%20Ramadan%202026/J01%20FARIJ%20HT%20KUREL%20MACHRABUS%20CHAFI%20HT.mp3.mp3"
    },
    {
        "titre": "J01 LAMYABDU S M SY KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476728/media/audios/khassida/Khassida%20Ramadan%202026/J01%20LAMYABDU%20S%20M%20SY%20KUREL%20MACHRABUS%20CHAFI%20HT.mp3.mp3"
    },
    {
        "titre": "J01 MATLABU CHIFAHI  S TAFSIR DIOP KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476741/media/audios/khassida/Khassida%20Ramadan%202026/J01%20MATLABU%20CHIFAHI%20%20S%20TAFSIR%20DIOP%20KUREL%20MACHRABUS%20CHAFI%20HT.mp3.mp3"
    },
    {
        "titre": "J01 YAKHAYRA WKSM KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476761/media/audios/khassida/Khassida%20Ramadan%202026/J01%20YAKHAYRA%20WKSM%20KUREL%20MACHRABUS%20CHAFI%20HT.mp3.mp3"
    },
    {
        "titre": "J01 HADAA IQUL FADAA IL S TAFSIR DIOP KUREL MACHRABUS CHAFI HT",
        "auteur_voix": "Kurel MACHRABUS CHAFI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476838/media/audios/khassida/Khassida%20Ramadan%202026/J01_HADAA_IQUL_FADAA_IL_S_TAFSIR_DIOP_KUREL_MACHRABUS_CHAFI_HT.mp3.mp3"
    },
    {
        "titre": "J02 KHASSIDA RAMADAN HT KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476846/media/audios/khassida/Khassida%20Ramadan%202026/J02%20KHASSIDA%20RAMADAN%20HT%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J02 LAMYABDOU S MBAYE DIOP KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476851/media/audios/khassida/Khassida%20Ramadan%202026/J02%20LAMYABDOU%20S%20MBAYE%20DIOP%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J02 MADADTU WKSM KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476865/media/audios/khassida/Khassida%20Ramadan%202026/J02%20MADADTU%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J02 MADALMUNA S CHEIKH LO KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476882/media/audios/khassida/Khassida%20Ramadan%202026/J02%20MADALMUNA%20S%20CHEIKH%20LO%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J02 YAKHAYRA S MODOU DEME KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476894/media/audios/khassida/Khassida%20Ramadan%202026/J02%20YAKHAYRA%20S%20MODOU%20DEME%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J02 MATLABU FAWZAYNI S TAFSIR DIOP KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476934/media/audios/khassida/Khassida%20Ramadan%202026/J02_MATLABU_FAWZAYNI_S_TAFSIR_DIOP_KUREL_NURUD_DARAYNI_HT_TOUBA.mp3.mp3"
    },
    {
        "titre": "J17 FARIJ HT KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781476942/media/audios/khassida/Khassida%20Ramadan%202026/J17%20FARIJ%20HT%20KUREL%20ASNA%20KHADIM%20HT.mp3.mp3"
    },
    {
        "titre": "J17 JAZBU WKSM KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477039/media/audios/khassida/Khassida%20Ramadan%202026/J17%20JAZBU%20WKSM%20KUREL%20ASNA%20KHADIM%20HT.mp3.mp3"
    },
    {
        "titre": "J18 BISMILAHILAZI WKSM KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477057/media/audios/khassida/Khassida%20Ramadan%202026/J18%20BISMILAHILAZI%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20DAROU%20MANANE.mp3.mp3"
    },
    {
        "titre": "J18 FARIJ HT KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477063/media/audios/khassida/Khassida%20Ramadan%202026/J18%20FARIJ%20HT%20KUREL%20NURUD%20DARAYNI%20HT%20DAROU%20MANANE.mp3.mp3"
    },
    {
        "titre": "J18 MAWAHIBOU WKSM KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477149/media/audios/khassida/Khassida%20Ramadan%202026/J18%20MAWAHIBOU%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20DAROU%20MANANE.mp3.mp3"
    },
    {
        "titre": "J18 CHAHRU RAMADAN S M SY KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477162/media/audios/khassida/Khassida%20Ramadan%202026/J18_CHAHRU_RAMADAN_S_M_SY_KUREL_NURUD_DARAYNI_HT_DAROU_MANANE.mp3.mp3"
    },
    {
        "titre": "J18 LAMYABDU S MBAYE DIOP KUREL NURUD DARAYNI HT DAROU MANANE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477169/media/audios/khassida/Khassida%20Ramadan%202026/J18_LAMYABDU_S_MBAYE_DIOP_KUREL_NURUD_DARAYNI_HT_DAROU_MANANE.mp3.mp3"
    },
    {
        "titre": "J19 FARIJ HT KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477174/media/audios/khassida/Khassida%20Ramadan%202026/J19%20FARIJ%20HT%20KUREL%20MAFATIHUL%20BICHRI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J19 LIHALAMALNAZIRU S M SY KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477183/media/audios/khassida/Khassida%20Ramadan%202026/J19%20LIHALAMALNAZIRU%20S%20M%20SY%20KUREL%20MAFATIHUL%20BICHRI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J19 MINALKHADIMI S MB DIOP KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477209/media/audios/khassida/Khassida%20Ramadan%202026/J19%20MINALKHADIMI%20S%20MB%20DIOP%20KUREL%20MAFATIHUL%20BICHRI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J19 YAAMOUKRIMA WKSM KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477219/media/audios/khassida/Khassida%20Ramadan%202026/J19%20YAAMOUKRIMA%20WKSM%20KUREL%20MAFATIHUL%20BICHRI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J19 AHBABTU FATAHA FUZTY WKSM KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477262/media/audios/khassida/Khassida%20Ramadan%202026/J19_AHBABTU_FATAHA_FUZTY_WKSM_KUREL_MAFATIHUL_BICHRI_HT_TOUBA.mp3.mp3"
    },
    {
        "titre": "J19 LAMYABDU CHAHRU RAMADAN HT KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477274/media/audios/khassida/Khassida%20Ramadan%202026/J19_LAMYABDU_CHAHRU_RAMADAN_HT_KUREL_MAFATIHUL_BICHRI_HT_TOUBA.mp3.mp3"
    },
    {
        "titre": "J19 LISSANU CHUKRY MADALKHABIRU S DAME LO KUREL MAFATIHUL BICHRI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477288/media/audios/khassida/Khassida%20Ramadan%202026/J19_LISSANU_CHUKRY_MADALKHABIRU_S_DAME_LO_KUREL_MAFATIHUL_BICHRI.mp3.mp3"
    },
    {
        "titre": "J19 MIDADI WA AQLAMI S BOLLE MBAYE KUREL MAFATIHUL BICHRI HT TOUBA",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477301/media/audios/khassida/Khassida%20Ramadan%202026/J19_MIDADI_WA_AQLAMI_S_BOLLE_MBAYE_KUREL_MAFATIHUL_BICHRI_HT_TOUBA.mp3.mp3"
    },
    {
        "titre": "J20 ATAABA S BOLLE MBAYE KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477341/media/audios/khassida/Khassida%20Ramadan%202026/J20%20ATAABA%20S%20BOLLE%20MBAYE%20KUREL%20TAZAWUDUS%20SIKHAR%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J20 FARIJ HT KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477348/media/audios/khassida/Khassida%20Ramadan%202026/J20%20FARIJ%20HT%20KUREL%20TAZAWUDUS%20SIKHAR%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J20 FAZALAZINA S IBRAHIMA LO KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477355/media/audios/khassida/Khassida%20Ramadan%202026/J20%20FAZALAZINA%20S%20IBRAHIMA%20LO%20KUREL%20TAZAWUDUS%20SIKHAR%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J20 ALAA INANI HUZNY S ALIOUNE FALL KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477372/media/audios/khassida/Khassida%20Ramadan%202026/J20_ALAA_INANI_HUZNY_S_ALIOUNE_FALL_KUREL_TAZAWUDUS_SIKHAR_HT_DAKAR.mp3.mp3"
    },
    {
        "titre": "J20 INNALLAZINA S BOLLE MBAYE KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477391/media/audios/khassida/Khassida%20Ramadan%202026/J20_INNALLAZINA_S_BOLLE_MBAYE_KUREL_TAZAWUDUS_SIKHAR_HT_DAKAR.mp3.mp3"
    },
    {
        "titre": "J20 TAWBATU NACOUH S MBAYE DIOP KUREL TAZAWUDUS SIKHAR HT DAKAR",
        "auteur_voix": "Kurel TAZAWUDUS SIKHAR HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477411/media/audios/khassida/Khassida%20Ramadan%202026/J20_TAWBATU_NACOUH_S_MBAYE_DIOP_KUREL_TAZAWUDUS_SIKHAR_HT_DAKAR.mp3.mp3"
    },
    {
        "titre": "J21 FARIHA FARIHA WKSM KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477429/media/audios/khassida/Khassida%20Ramadan%202026/J21%20FARIHA_FARIHA%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J21 FARIJ HT KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477436/media/audios/khassida/Khassida%20Ramadan%202026/J21%20FARIJ%20HT%20KUREL%20NURUD%20DARAYNI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J21 HUQQA WKSM KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477477/media/audios/khassida/Khassida%20Ramadan%202026/J21%20HUQQA%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J21 INI AQULU S MATAR MBAYE KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477492/media/audios/khassida/Khassida%20Ramadan%202026/J21%20INI%20AQULU%20S%20MATAR%20MBAYE%20KUREL%20NURUD%20DARAYNI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J21 WAAJAKHAT NI  S M THIAM KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477499/media/audios/khassida/Khassida%20Ramadan%202026/J21%20WAAJAKHAT%20NI%20%20S%20M%20THIAM%20KUREL%20NURUD%20DARAYNI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J21 YAAZALWUDIOUDI S A DIOP KUREL NURUD DARAYNI HT DAKAR",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477505/media/audios/khassida/Khassida%20Ramadan%202026/J21%20YAAZALWUDIOUDI%20S%20A%20DIOP%20KUREL%20NURUD%20DARAYNI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J21 LAMYABDU CHAHRU RAMADAN S BASSIROU SENE KUREL NURUD DARAYNI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477516/media/audios/khassida/Khassida%20Ramadan%202026/J21_LAMYABDU_CHAHRU_RAMADAN_S_BASSIROU_SENE_KUREL_NURUD_DARAYNI.mp3.mp3"
    },
    {
        "titre": "J22 BISMILLAHIL KARIM S CISSE KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477527/media/audios/khassida/Khassida%20Ramadan%202026/J22%20BISMILLAHIL%20KARIM%20S%20CISSE%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J22 FAZAT QILAMI S MODOU THIAM  KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477535/media/audios/khassida/Khassida%20Ramadan%202026/J22%20FAZAT%20QILAMI%20S%20MODOU%20THIAM%20%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J22 MAHAWTAL S A KHADRE SEYE KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477542/media/audios/khassida/Khassida%20Ramadan%202026/J22%20MAHAWTAL%20S%20A%20KHADRE%20SEYE%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J22 QALU S ALIOUNE FALL KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477548/media/audios/khassida/Khassida%20Ramadan%202026/J22%20QALU%20S%20ALIOUNE%20FALL%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J22 YAMUKRIMA DAYFI WKSM KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477558/media/audios/khassida/Khassida%20Ramadan%202026/J22%20YAMUKRIMA%20DAYFI%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J22 YASAYIDI  S TAFSIR DIOP KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477567/media/audios/khassida/Khassida%20Ramadan%202026/J22%20YASAYIDI%20%20S%20TAFSIR%20DIOP%20KUREL%20NURUD%20DARAYNI%20HT%20TOUBA.mp3.mp3"
    },
    {
        "titre": "J22 AHMADU MUHNIYAN YASAYIDI S TAFSIR DIOP KUREL NURUD DARAYNI HT",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477598/media/audios/khassida/Khassida%20Ramadan%202026/J22_AHMADU_MUHNIYAN_YASAYIDI_S_TAFSIR_DIOP_KUREL_NURUD_DARAYNI_HT.mp3.mp3"
    },
    {
        "titre": "J22 BISMILAHI LAZI S CH GUEYE MAHIB KUREL NURUD DARAYNI HT TOUBA",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477614/media/audios/khassida/Khassida%20Ramadan%202026/J22_BISMILAHI_LAZI_S_CH_GUEYE_MAHIB_KUREL_NURUD_DARAYNI_HT_TOUBA.mp3.mp3"
    },
    {
        "titre": "J22 LAMYABDU CHAHRU RAMADAN S SALIOU MBACKE KUREL NURUD DARAYNI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477623/media/audios/khassida/Khassida%20Ramadan%202026/J22_LAMYABDU_CHAHRU_RAMADAN_S_SALIOU_MBACKE_KUREL_NURUD_DARAYNI.mp3.mp3"
    },
    {
        "titre": "J22 MADALKHABIROU LISSANU CHUKRY WA NDIAREME KUREL NURUD DARAYNI",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477634/media/audios/khassida/Khassida%20Ramadan%202026/J22_MADALKHABIROU_LISSANU_CHUKRY_WA_NDIAREME_KUREL_NURUD_DARAYNI.mp3.mp3"
    },
    {
        "titre": "J23 AHANZANI S M SY KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477645/media/audios/khassida/Khassida%20Ramadan%202026/J23%20AHANZANI%20S%20M%20SY%20KUREL%20NURUD%20DARAYNI%20HT%20THIES.mp3.mp3"
    },
    {
        "titre": "J23 AHBABTU WKSM KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477666/media/audios/khassida/Khassida%20Ramadan%202026/J23%20AHBABTU%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20THIES.mp3.mp3"
    },
    {
        "titre": "J23 FARJI HT KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477681/media/audios/khassida/Khassida%20Ramadan%202026/J23%20FARJI%20HT%20KUREL%20NURUD%20DARAYNI%20HT%20THIES.mp3.mp3"
    },
    {
        "titre": "J23 ILAANABIYIN S MASSAMBA NIASS KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477703/media/audios/khassida/Khassida%20Ramadan%202026/J23_ILAANABIYIN_S_MASSAMBA_NIASS_KUREL_NURUD_DARAYNI_HT_THIES.mp3.mp3"
    },
    {
        "titre": "J23 TAYSIRUL ASSIR S TAFSIR DIOP KUREL NURUD DARAYNI HT THIES",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477764/media/audios/khassida/Khassida%20Ramadan%202026/J23_TAYSIRUL_ASSIR_S_TAFSIR_DIOP_KUREL_NURUD_DARAYNI_HT_THIES.mp3.mp3"
    },
    {
        "titre": "J24 ALLAHU BARRUN S CISSE KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477779/media/audios/khassida/Khassida%20Ramadan%202026/J24%20ALLAHU%20BARRUN%20S%20CISSE%20KUREL%20MAFATIHUL%20BICHRI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J24 BUCHRALANAA S A FALL KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477796/media/audios/khassida/Khassida%20Ramadan%202026/J24%20BUCHRALANAA%20S%20A%20FALL%20KUREL%20MAFATIHUL%20BICHRI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J24 FARIJ HT KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477808/media/audios/khassida/Khassida%20Ramadan%202026/J24%20FARIJ%20HT%20KUREL%20MAFATIHUL%20BICHRI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J24 INNILAKHILLUN WKSM KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477827/media/audios/khassida/Khassida%20Ramadan%202026/J24%20INNILAKHILLUN%20WKSM%20KUREL%20MAFATIHUL%20BICHRI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J24 LAMYABDU S M SY KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477841/media/audios/khassida/Khassida%20Ramadan%202026/J24%20LAMYABDU%20S%20M%20SY%20KUREL%20MAFATIHUL%20BICHRI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J24 MATLABUS CHIFAHI S TAFSIR DIOP KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477858/media/audios/khassida/Khassida%20Ramadan%202026/J24_MATLABUS_CHIFAHI_S_TAFSIR_DIOP_KUREL_MAFATIHUL_BICHRI_HT_RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J24 WALAQAD KARAMNA S M DIOP KUREL MAFATIHUL BICHRI HT RUFISQUE",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477900/media/audios/khassida/Khassida%20Ramadan%202026/J24_WALAQAD_KARAMNA_S_M_DIOP_KUREL_MAFATIHUL_BICHRI_HT_RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J25 AJABANI WKSM  KUREL SERIGNE SALIOU MBACKE HT",
        "auteur_voix": "Kurel SERIGNE SALIOU MBACKE HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477928/media/audios/khassida/Khassida%20Ramadan%202026/J25%20AJABANI%20WKSM%20%20KUREL%20SERIGNE%20SALIOU%20MBACKE%20HT.mp3.mp3"
    },
    {
        "titre": "J25 FARIJ HT KUREL SERIGNE SALIOU MBACKE HT",
        "auteur_voix": "Kurel SERIGNE SALIOU MBACKE HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477935/media/audios/khassida/Khassida%20Ramadan%202026/J25%20FARIJ%20HT%20KUREL%20SERIGNE%20SALIOU%20MBACKE%20HT.mp3.mp3"
    },
    {
        "titre": "J25 RABIYAH AHMADU HT KUREL SERIGNE SALIOU MBACKE HT",
        "auteur_voix": "Kurel SERIGNE SALIOU MBACKE HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477949/media/audios/khassida/Khassida%20Ramadan%202026/J25%20RABIYAH%20AHMADU%20HT%20KUREL%20SERIGNE%20SALIOU%20MBACKE%20HT.mp3.mp3"
    },
    {
        "titre": "J25 LAMYABDU FAZALLAZI S TAFSIR DIOP KUREL SERIGNE SALIOU MBACKE",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477961/media/audios/khassida/Khassida%20Ramadan%202026/J25_LAMYABDU_FAZALLAZI_S_TAFSIR_DIOP_KUREL_SERIGNE_SALIOU_MBACKE.mp3.mp3"
    },
    {
        "titre": "J26 ALAA INANI S A FALL KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477981/media/audios/khassida/Khassida%20Ramadan%202026/J26%20ALAA%20INANI%20S%20A%20FALL%20KUREL%20NURUD%20DARAYNI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J26 FARIJ HT KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477989/media/audios/khassida/Khassida%20Ramadan%202026/J26%20FARIJ%20HT%20KUREL%20NURUD%20DARAYNI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J26 MAN ZANANI S M SY KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781477997/media/audios/khassida/Khassida%20Ramadan%202026/J26%20MAN%20ZANANI%20S%20M%20SY%20KUREL%20NURUD%20DARAYNI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J26 RUMNA S MB DIOP KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478029/media/audios/khassida/Khassida%20Ramadan%202026/J26%20RUMNA%20S%20MB%20DIOP%20KUREL%20NURUD%20DARAYNI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J26 YAAZAL BUCHARATY WKSM KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478075/media/audios/khassida/Khassida%20Ramadan%202026/J26%20YAAZAL%20BUCHARATY%20WKSM%20KUREL%20NURUD%20DARAYNI%20HT%20RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J26 LAMYABDU S M LAMINE GUEYE KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478082/media/audios/khassida/Khassida%20Ramadan%202026/J26_LAMYABDU_S_M_LAMINE_GUEYE_KUREL_NURUD_DARAYNI_HT_RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J26 YAAMOUKRIMA ZALAT S CISSE KUREL NURUD DARAYNI HT RUFISQUE",
        "auteur_voix": "Kurel NURUD DARAYNI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478094/media/audios/khassida/Khassida%20Ramadan%202026/J26_YAAMOUKRIMA_ZALAT_S_CISSE_KUREL_NURUD_DARAYNI_HT_RUFISQUE.mp3.mp3"
    },
    {
        "titre": "J27 FARIJ HT KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478100/media/audios/khassida/Khassida%20Ramadan%202026/J27%20FARIJ%20HT%20KUREL%20WAKEUR%20SERIGNE%20MASSAMBA%20HT.mp3.mp3"
    },
    {
        "titre": "J27 MAWAHIBOU WKSM KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478176/media/audios/khassida/Khassida%20Ramadan%202026/J27%20MAWAHIBOU%20WKSM%20KUREL%20WAKEUR%20SERIGNE%20MASSAMBA%20HT.mp3.mp3"
    },
    {
        "titre": "J27 RABBI WKSM KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478185/media/audios/khassida/Khassida%20Ramadan%202026/J27%20RABBI%20WKSM%20KUREL%20WAKEUR%20SERIGNE%20MASSAMBA%20HT.mp3.mp3"
    },
    {
        "titre": "J27 ASTAHFIRULAHI BIHI S M SY KUREL WAKEUR SERIGNE MASSAMBA HT",
        "auteur_voix": "Kurel WAKEUR SERIGNE MASSAMBA HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478194/media/audios/khassida/Khassida%20Ramadan%202026/J27_ASTAHFIRULAHI_BIHI_S_M_SY_KUREL_WAKEUR_SERIGNE_MASSAMBA_HT.mp3.mp3"
    },
    {
        "titre": "J28 AHBABTU WKSM KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478205/media/audios/khassida/Khassida%20Ramadan%202026/J28%20AHBABTU%20WKSM%20KUREL%20MAFATIHUL%20BICHRI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J28 BUCHRALANA S CISSE KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478230/media/audios/khassida/Khassida%20Ramadan%202026/J28%20BUCHRALANA%20S%20CISSE%20KUREL%20MAFATIHUL%20BICHRI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J28 FARIJ HT KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478236/media/audios/khassida/Khassida%20Ramadan%202026/J28%20FARIJ%20HT%20KUREL%20MAFATIHUL%20BICHRI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J28 LILLAHIKULIYATI S M SY KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478247/media/audios/khassida/Khassida%20Ramadan%202026/J28%20LILLAHIKULIYATI%20S%20M%20SY%20KUREL%20MAFATIHUL%20BICHRI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J28 YAZALBUCHARATI S CISSE KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478277/media/audios/khassida/Khassida%20Ramadan%202026/J28%20YAZALBUCHARATI%20S%20CISSE%20KUREL%20MAFATIHUL%20BICHRI%20HT%20DAKAR.mp3.mp3"
    },
    {
        "titre": "J28 LAMYABDU CHAHRU RAMADAN S M SY KUREL MAFATIHUL BICHRI HT DAKAR",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478289/media/audios/khassida/Khassida%20Ramadan%202026/J28_LAMYABDU_CHAHRU_RAMADAN_S_M_SY_KUREL_MAFATIHUL_BICHRI_HT_DAKAR.mp3.mp3"
    },
    {
        "titre": "J28 LAYANTAHI LAMYANKHU S TAFSIR DIOP KUREL MAFATIHUL BICHRI HT",
        "auteur_voix": "Kurel MAFATIHUL BICHRI HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478324/media/audios/khassida/Khassida%20Ramadan%202026/J28_LAYANTAHI_LAMYANKHU_S_TAFSIR_DIOP_KUREL_MAFATIHUL_BICHRI_HT.mp3.mp3"
    },
    {
        "titre": "J29 FARIJ  HT KUREL SERIGNE ABDUL AHAD MBACKE HT",
        "auteur_voix": "Kurel SERIGNE ABDUL AHAD MBACKE HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478330/media/audios/khassida/Khassida%20Ramadan%202026/J29%20FARIJ%20%20HT%20KUREL%20SERIGNE%20ABDUL%20AHAD%20MBACKE%20HT.mp3.mp3"
    },
    {
        "titre": "J29 LAMYABDU S M SY KUREL SERIGNE ABDUL AHAD MBACKE HT",
        "auteur_voix": "Kurel SERIGNE ABDUL AHAD MBACKE HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478335/media/audios/khassida/Khassida%20Ramadan%202026/J29%20LAMYABDU%20S%20M%20SY%20KUREL%20SERIGNE%20ABDUL%20AHAD%20MBACKE%20HT.mp3.mp3"
    },
    {
        "titre": "J29 JAALIBATUL MARAKHIB S TAFSIR DIOP KUREL SERIGNE ABDUL AHAD MBACKE",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478419/media/audios/khassida/Khassida%20Ramadan%202026/J29_JAALIBATUL_MARAKHIB_S_TAFSIR_DIOP_KUREL_SERIGNE_ABDUL_AHAD_MBACKE.mp3.mp3"
    },
    {
        "titre": "J30 FARIJ HT KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478431/media/audios/khassida/Khassida%20Ramadan%202026/J30%20FARIJ%20HT%20KUREL%20ASNA%20KHADIM%20HT.mp3.mp3"
    },
    {
        "titre": "J30 LAMYABDU S M SY KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478438/media/audios/khassida/Khassida%20Ramadan%202026/J30%20LAMYABDU%20S%20M%20SY%20KUREL%20ASNA%20KHADIM%20HT.mp3.mp3"
    },
    {
        "titre": "J30 MIDADI WKSM KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478484/media/audios/khassida/Khassida%20Ramadan%202026/J30%20MIDADI%20WKSM%20KUREL%20ASNA%20KHADIM%20HT.mp3.mp3"
    },
    {
        "titre": "J30 YAZALBUCHARATY RABBI WKSM KUREL ASNA KHADIM HT",
        "auteur_voix": "Kurel ASNA KHADIM HT",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478534/media/audios/khassida/Khassida%20Ramadan%202026/J30%20YAZALBUCHARATY_RABBI%20WKSM%20KUREL%20ASNA%20KHADIM%20HT.mp3.mp3"
    },
    {
        "titre": "Madal Khabirou Lissanou Choukry Kourel Taverny Journ\u00e9e Cheikh Ahmadou",
        "auteur_voix": "Kourel Taverny",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478551/media/audios/khassida/Khassida%20Ramadan%202026/Madal_Khabirou_Lissanou_Choukry_Kourel_Taverny_Journ%C3%A9e_Cheikh_Ahmadou.mp3.mp3"
    },
    {
        "titre": "Midaadi - Sgne Youssou Ndao",
        "auteur_voix": "Sgne Youssou Ndao",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478655/media/audios/khassida/Khassida%20Ramadan%202026/Midaadi%20-%20Sgne%20Youssou%20Ndao.mp3.mp3"
    },
    {
        "titre": "Muhammadun - Sgne Modou DIOP",
        "auteur_voix": "Sgne Modou DIOP",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478663/media/audios/khassida/Khassida%20Ramadan%202026/Muhammadun%20-%20Sgne%20Modou%20DIOP.mp3.mp3"
    },
    {
        "titre": "Ndiarignou Xassida yi Serigne Abdou Rahmane ",
        "auteur_voix": "Serigne Abdou Rahmane",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478673/media/audios/khassida/Khassida%20Ramadan%202026/Ndiarignou%20Xassida%20yi%20Serigne%20Abdou%20Rahmane%20.mp3.mp3"
    },
    {
        "titre": "Wajaba Hamdul Xaaliqi - Sgne Moussa Gueye Ndar",
        "auteur_voix": "Sgne Moussa Gueye Ndar",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478684/media/audios/khassida/Khassida%20Ramadan%202026/Wajaba%20Hamdul%20Xaaliqi%20-%20Sgne%20Moussa%20Gueye%20Ndar.mp3.mp3"
    },
    {
        "titre": "Walajtu Wuluujan - Wa Keur Sgne Massamba",
        "auteur_voix": "Wa Keur Sgne Massamba",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478712/media/audios/khassida/Khassida%20Ramadan%202026/Walajtu%20Wuluujan%20-%20Wa%20Keur%20Sgne%20Massamba.mp3.mp3"
    },
    {
        "titre": "Wawasaynal Insaana - Sgne Abdoul Ahad Toure",
        "auteur_voix": "Sgne Abdoul Ahad Toure",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478720/media/audios/khassida/Khassida%20Ramadan%202026/Wawasaynal%20Insaana%20-%20Sgne%20Abdoul%20Ahad%20Toure.mp3.mp3"
    },
    {
        "titre": "YAKHINII WKSM KOUREL 1 TOUTANK HTDKH 16 JOUR RAMADAN 2026",
        "auteur_voix": "Kourel 1 TOUTANK HTDKH",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478729/media/audios/khassida/Khassida%20Ramadan%202026/YAKHINII%20WKSM%20KOUREL%201%20TOUTANK%20HTDKH%2016%20JOUR%20RAMADAN%202026.mp3.mp3"
    },
    {
        "titre": "diawartou kourel1 mafatihoul bichri touba alieu ga",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478736/media/audios/khassida/Khassida%20Ramadan%202026/diawartou%20kourel1%20mafatihoul%20bichri%20touba%20alieu%20ga.mp3.mp3"
    },
    {
        "titre": "yamane yaroumo kourel1 Dmb touba alieu gamou 2025 (1)",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478746/media/audios/khassida/Khassida%20Ramadan%202026/yamane%20yaroumo%20kourel1%20Dmb%20touba%20alieu%20gamou%202025%20%281%29.mp3.mp3"
    },
    {
        "titre": "yamane yaroumo kourel1 Dmb touba alieu gamou 2025",
        "auteur_voix": "",
        "categorie": "KHASSIDA",
        "lien_audio_externe": "https://res.cloudinary.com/dcajqzg2h/video/upload/v1781478754/media/audios/khassida/Khassida%20Ramadan%202026/yamane%20yaroumo%20kourel1%20Dmb%20touba%20alieu%20gamou%202025.mp3.mp3"
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
                'lien_audio_externe': item['lien_audio_externe']
            }
        )
        if created:
            print(f"Ajouté : {item['titre'].encode('ascii', 'replace').decode()}")
        else:
            obj.lien_audio_externe = item['lien_audio_externe']
            obj.auteur_voix = item['auteur_voix']
            obj.save()
            print(f"Mis à jour : {item['titre'].encode('ascii', 'replace').decode()}")

if __name__ == '__main__':
    run()
