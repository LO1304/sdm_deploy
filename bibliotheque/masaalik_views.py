import json
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .masaalik_data import (
    MASAALIK_PORTES,
    get_all_chapitres,
    get_chapitre_by_slug,
    build_masaalik_deck,
    get_chapitre_verbatim_versets,
    get_masaalik_exam,
)


def _compute_streak(active_days):
    """Calcule la série consécutive en jours jusqu'à aujourd'hui ou hier."""
    if not active_days:
        return 0
    unique_days = set(active_days)
    today = datetime.date.today()
    cur = today if today.isoformat() in unique_days else (today - datetime.timedelta(days=1))
    streak = 0
    while cur.isoformat() in unique_days:
        streak += 1
        cur -= datetime.timedelta(days=1)
    return streak


def _get_session_progress(request):
    prog = request.session.get("masaalik_progress")
    if not isinstance(prog, dict):
        prog = {"chapters": {}, "active_days": [], "xp": 0, "streak": 0}
    return prog


def apprentissage_home(request):
    """Grand pôle unifié d'Apprentissage : Masaalik-ul Jinaan, Tazawwudu-ç-Çighâr et œuvres à venir."""
    all_ch = get_all_chapitres()
    upcoming_books = [
        {
            "titre": "Tazawwudu-sh-Shubbân",
            "sous_titre": "Le Viatique de la Jeunesse",
            "desc": "Guide complet des obligations religieuses, de la piété et de la conduite du jeune croyant.",
            "icone": "fa-seedling",
        },
        {
            "titre": "Nahju Qadâ'il Hâj",
            "sous_titre": "La Voie de la Satisfaction des Besoins",
            "desc": "Les règles d'or de la bienséance (Al-Adab), du respect des parents, des maîtres et de la communauté.",
            "icone": "fa-hands-holding-circle",
        },
        {
            "titre": "Jawharu-n-Nafîs",
            "sous_titre": "Le Joyau Précieux (Fiqh)",
            "desc": "Versification du précis de jurisprudence d'Al-Akhdarî : pureté, prière et pratiques quotidiennes.",
            "icone": "fa-gem",
        },
        {
            "titre": "Munawwiru-ç-Çudûr",
            "sous_titre": "L'Illuminateur des Cœurs",
            "desc": "Éducation spirituelle, purification des organes et élévation morale selon Cheikh Ahmadou Bamba.",
            "icone": "fa-sun",
        },
    ]
    return render(request, "bibliotheque/apprentissage_home.html", {
        "masaalik_total_chapitres": len(all_ch),
        "masaalik_total_questions": sum(len(c["questions"]) for c in all_ch),
        "upcoming_books": upcoming_books,
    })


def masaalik_home(request):
    """Accueil de l'Académie Masaalik-ul Jinaan en Mode Duolingo (4 Grandes Portes · 16 Chapitres)."""
    prog = _get_session_progress(request)
    all_ch = get_all_chapitres()
    today = datetime.date.today()
    today_iso = today.isoformat()
    yest_iso = (today - datetime.timedelta(days=1)).isoformat()

    # Construire calendrier 7 jours côté serveur (sera aussi fusionné avec localStorage côté client)
    day_labels = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    active_set = set(prog.get("active_days") or [])
    week_days = []
    for delta in range(6, -1, -1):
        d = today - datetime.timedelta(days=delta)
        week_days.append({
            "iso": d.isoformat(),
            "label": day_labels[d.weekday()],
            "num": d.day,
            "is_today": d == today,
            "done": d.isoformat() in active_set,
        })

    context = {
        "portes": MASAALIK_PORTES,
        "total_chapitres": len(all_ch),
        "total_questions": sum(len(c["questions"]) for c in all_ch),
        "week_days": week_days,
        "today_iso": today_iso,
        "yest_iso": yest_iso,
        "session_progress_json": json.dumps(prog, ensure_ascii=False),
        "all_chapitres_meta_json": json.dumps(
            [{"slug": c["slug"], "num": c["num"], "titre": c["titre"], "versets": c["versets"]} for c in all_ch],
            ensure_ascii=False,
        ),
    }
    return render(request, "bibliotheque/masaalik/home.html", context)


@login_required(login_url='/login/')
def masaalik_chapitre(request, slug):
    """Lecteur étape par étape pour une leçon de Masaalik-ul Jinaan (compte requis pour sauvegarder notes & progression)."""
    chapitre, prev_ch, next_ch = get_chapitre_by_slug(slug)
    if not chapitre:
        raise Http404("Chapitre Masaalikul Jinaan introuvable")

    deck = build_masaalik_deck(chapitre)
    verbatim = get_chapitre_verbatim_versets(chapitre)
    context = {
        "chapitre": chapitre,
        "prev_ch": prev_ch,
        "next_ch": next_ch,
        "deck_json": json.dumps(deck, ensure_ascii=False),
        "verbatim_versets": verbatim,
        "verbatim_count": len(verbatim),
        "total_steps": len(deck),
        "total_questions": len(chapitre["questions"]),
    }
    return render(request, "bibliotheque/masaalik/chapitre.html", context)


@login_required(login_url='/login/')
def masaalik_examen(request, exam_slug):
    """Test de fin de Grande Porte (porte-1..4) ou Grand Examen Final Masaalik-ul Jinaan."""
    exam = get_masaalik_exam(exam_slug)
    if not exam:
        raise Http404("Examen Masaalik-ul Jinaan introuvable")
    return render(request, "bibliotheque/masaalik/examen.html", {
        "exam": exam,
        "questions_json": json.dumps(exam["questions"], ensure_ascii=False),
        "total_questions": len(exam["questions"]),
    })


@csrf_exempt
@require_POST
def masaalik_save_progress(request):
    """Sauvegarde la note /20, les étoiles, les XP et la flamme dans la session Django."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "JSON invalide"}, status=400)

    slug = str(payload.get("slug") or "").strip()
    correct = max(0, int(payload.get("correct") or 0))
    total = max(1, int(payload.get("total") or 1))
    note_20 = round((correct / total) * 20, 1)
    if note_20.is_integer():
        note_20 = int(note_20)
    stars = 3 if note_20 >= 16 else (2 if note_20 >= 12 else (1 if note_20 >= 8 else 0))
    xp_earned = 25 + correct * 10 + (20 if note_20 == 20 else 0)

    prog = _get_session_progress(request)
    chapters = prog.setdefault("chapters", {})
    prev_best = chapters.get(slug, {}).get("note_20", 0)
    chapters[slug] = {
        "note_20": max(prev_best, note_20),
        "last_note_20": note_20,
        "stars": max(chapters.get(slug, {}).get("stars", 0), stars),
        "completed": True,
        "updated_at": datetime.date.today().isoformat(),
    }

    today_iso = datetime.date.today().isoformat()
    active_days = list(prog.get("active_days") or [])
    if today_iso not in active_days:
        active_days.append(today_iso)
    prog["active_days"] = active_days[-60:]
    prog["xp"] = int(prog.get("xp") or 0) + xp_earned
    prog["streak"] = _compute_streak(prog["active_days"])

    request.session["masaalik_progress"] = prog
    request.session.modified = True

    # Message de remerciement & félicitations personnalisé fidèle au souhait de l'utilisateur
    if note_20 >= 18:
        merci_msg = "Mâshâ'Allah ! Merci infiniment pour ton sérieux et ta constance dans l'étude de Masaalikul Jinaan. Cheikh Ahmadou Bamba a prié pour quiconque médite cet ouvrage (v.70) !"
    elif note_20 >= 14:
        merci_msg = "Alhamdoulillah ! Merci pour ta belle progression aujourd'hui. Continue sur cet élan lumineux, tu maîtrises de mieux en mieux les enseignements de Serigne Touba !"
    elif note_20 >= 10:
        merci_msg = "Bravo et merci pour ton effort ! Tu avances étape par étape dans Masaalikul Jinaan. N'hésite pas à rejouer le chapitre pour viser les 3 étoiles !"
    else:
        merci_msg = "Merci d'avoir pris le temps d'étudier aujourd'hui ! L'apprentissage est un chemin : rejoue ce chapitre calmement pour ancrer chaque enseignement et faire grimper ta note."

    return JsonResponse({
        "ok": True,
        "note_20": note_20,
        "stars": stars,
        "xp_earned": xp_earned,
        "total_xp": prog["xp"],
        "streak": prog["streak"],
        "merci_msg": merci_msg,
        "progress": prog,
    })
