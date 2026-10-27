import json
import random
import uuid
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.urls import reverse

from .models import (
    TazawwudModule, TazawwudLecon, TazawwudQuestion, TazawwudChoix,
    TazawwudProgression, TazawwudReponseHistorique, TazawwudAchat,
    TazawwudCompagnon, TazawwudDefi, TazawwudBadge
)
from .fedapay_service import (
    creer_transaction_fedapay, verifier_transaction_fedapay, valider_achat_confirme
)


def get_rappels_tazawwud():
    """
    Extrait les rappels spirituels vérifiés (versets sources et synthèses à retenir)
    directement depuis les leçons de Tazawwudu-ç-Çighâr.
    """
    lecons = TazawwudLecon.objects.filter(est_revision_finale=False).select_related('module').order_by('module__numero', 'numero')
    rappels = []
    arabic_headers = {
        1: "بَابُ الْمُقَدِّمَةِ وَالتَّوْبَةِ",
        2: "بَابُ الْإِيمَانِ وَالتَّوْحِيدِ",
        3: "بَابُ الْإِسْلَامِ وَالطَّهَارَةِ",
        4: "بَابُ الصَّلَاةِ وَالصِّيَامِ",
        5: "بَابُ الْإِحْسَانِ وَالتَّصَوُّفِ",
    }
    for l in lecons:
        verset_extrait = (l.texte_source or "").strip().split('\n')[0][:220]
        retenir_lignes = [line.strip("•-* \t") for line in (l.a_retenir or "").strip().split('\n') if line.strip()]
        sagesse = retenir_lignes[0] if retenir_lignes else l.description
        rappels.append({
            'lecon_id': l.id,
            'numero': l.numero,
            'titre': l.titre,
            'chapitre': f"Partie {l.module.numero} · {l.module.titre}" if l.module else "Le Viatique",
            'arabe': arabic_headers.get(l.module.numero if l.module else 1, "تَزَوُّدُ الصِّغَارِ"),
            'verset': verset_extrait,
            'sagesse': sagesse,
            'points_cles': retenir_lignes[:3],
        })
    return rappels


# ── 1. ACCUEIL DU PARCOURS TAZAWWUD ──

@login_required
def tazawwud_home(request):
    """Page d'accueil du parcours avec la route d'apprentissage."""
    modules = TazawwudModule.objects.all().order_by('numero')
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
    progression.verifier_semaine_reset()

    total_lecons = TazawwudLecon.objects.count()
    lecons_terminees_count = progression.lecons_terminees.count()
    pourcentage = int((lecons_terminees_count / total_lecons * 100) if total_lecons > 0 else 0)

    # Vérification des accès aux révisions intensives
    a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)
    modules_payes_ids = list(TazawwudAchat.objects.filter(
        user=request.user, type_achat='MODULE', statut='APPROVED'
    ).values_list('module_id', flat=True))

    modules_data = []
    for m in modules:
        m_lecons = m.lecons.all()
        m_total = m_lecons.count()
        m_done = m_lecons.filter(id__in=progression.lecons_terminees.values_list('id', flat=True)).count()
        m_pct = int((m_done / m_total * 100) if m_total > 0 else 0)
        is_unlocked = a_forfait_complet or (m.id in modules_payes_ids)
        modules_data.append({
            'module': m,
            'total_lecons': m_total,
            'lecons_terminees': m_done,
            'pourcentage': m_pct,
            'revision_payee': is_unlocked,
        })

    # Réponses à revoir
    nb_erreurs = TazawwudReponseHistorique.objects.filter(user=request.user, est_correct=False).count()

    # Rappels vivants du Viatique
    rappels_list = get_rappels_tazawwud()
    rappel_du_jour = rappels_list[timezone.now().day % len(rappels_list)] if rappels_list else None

    context = {
        'modules_data': modules_data,
        'progression': progression,
        'pourcentage': pourcentage,
        'a_forfait_complet': a_forfait_complet,
        'nb_erreurs': nb_erreurs,
        'rappel_du_jour': rappel_du_jour,
        'rappels_json': json.dumps(rappels_list),
    }
    return render(request, 'bibliotheque/tazawwud/home.html', context)


# ── 2. TABLEAU DE BORD DE L'ÉLÈVE ──

@login_required
def tazawwud_dashboard(request):
    """
    Tableau de bord complet de l'élève :
    - Progression dans chaque grande partie du livre
    - Résultats et réponses à revoir
    - Activité de la semaine (7 derniers jours) et streak
    - Quiz gratuits vs révisions payantes
    - Compagnons & Classement de la semaine
    """
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
    progression.verifier_semaine_reset()

    modules = TazawwudModule.objects.all().order_by('numero')
    a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)
    modules_payes_ids = set(TazawwudAchat.objects.filter(
        user=request.user, type_achat='MODULE', statut='APPROVED'
    ).values_list('module_id', flat=True))

    terminees_ids = set(progression.lecons_terminees.values_list('id', flat=True))

    # Détail par module
    modules_stats = []
    for m in modules:
        lecons = m.lecons.all()
        lecons_ord = lecons.filter(est_revision_finale=False)
        revision = lecons.filter(est_revision_finale=True).first()

        nb_ord_total = lecons_ord.count()
        nb_ord_done = lecons_ord.filter(id__in=terminees_ids).count()
        rev_done = (revision.id in terminees_ids) if revision else False
        is_rev_unlocked = a_forfait_complet or (m.id in modules_payes_ids)

        modules_stats.append({
            'module': m,
            'nb_lecons': nb_ord_total,
            'nb_terminees': nb_ord_done,
            'pourcentage': int((nb_ord_done / nb_ord_total * 100) if nb_ord_total > 0 else 0),
            'revision': revision,
            'revision_terminee': rev_done,
            'revision_debloquee': is_rev_unlocked,
            'prix_fcfa': 500,
        })

    # Réponses à revoir (dernières erreurs distinctes)
    erreurs = TazawwudReponseHistorique.objects.filter(
        user=request.user, est_correct=False
    ).select_related('question', 'question__lecon').order_by('-date_tentative')[:15]

    # Activité des 7 derniers jours (calendrier / barres)
    today = timezone.now().date()
    jours_activite = []
    max_pts_jour = 10
    for i in range(6, -1, -1):
        j_date = today - timedelta(days=i)
        # Calculer le nombre de réponses données ce jour
        cnt = TazawwudReponseHistorique.objects.filter(
            user=request.user, date_tentative__date=j_date
        ).count()
        pts = cnt * 10
        if pts > max_pts_jour:
            max_pts_jour = pts
        jours_activite.append({
            'date': j_date,
            'nom_jour': j_date.strftime('%a'),
            'reponses': cnt,
            'points': pts,
            'est_aujourdhui': (j_date == today),
        })

    # Compagnons
    amis_ids = list(TazawwudCompagnon.objects.filter(
        Q(demandeur=request.user) | Q(ami=request.user),
        statut='ACCEPTE'
    ).values_list('demandeur_id', 'ami_id'))
    compagnons_ids = set()
    for d, a in amis_ids:
        compagnons_ids.add(d if d != request.user.id else a)

    compagnons = TazawwudProgression.objects.filter(
        user_id__in=compagnons_ids, est_profil_public=True
    ).select_related('user').order_by('-points_semaine')[:5]

    # Classement hebdomadaire général (profils publics)
    classement_hebdo = TazawwudProgression.objects.filter(
        est_profil_public=True, points_semaine__gt=0
    ).select_related('user').order_by('-points_semaine')[:10]

    rappels_list = get_rappels_tazawwud()
    rappel_du_jour = rappels_list[timezone.now().day % len(rappels_list)] if rappels_list else None

    context = {
        'progression': progression,
        'modules_stats': modules_stats,
        'erreurs': erreurs,
        'nb_erreurs': erreurs.count(),
        'jours_activite': jours_activite,
        'max_pts_jour': max_pts_jour,
        'a_forfait_complet': a_forfait_complet,
        'compagnons': compagnons,
        'classement_hebdo': classement_hebdo,
        'rappel_du_jour': rappel_du_jour,
        'rappels_json': json.dumps(rappels_list),
    }
    return render(request, 'bibliotheque/tazawwud/dashboard.html', context)


# ── 3. DÉTAIL D'UN MODULE & LEÇONS ──

@login_required
def tazawwud_module(request, module_id):
    """Affiche la liste des leçons d'un module et son étape de révision bloquante."""
    module = get_object_or_404(TazawwudModule, id=module_id)
    lecons = module.lecons.all().order_by('numero')
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    terminees_ids = list(progression.lecons_terminees.values_list('id', flat=True))
    a_acces_revision = TazawwudAchat.a_acces_revision(request.user, module)
    a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)

    context = {
        'module': module,
        'lecons': lecons,
        'terminees_ids': terminees_ids,
        'progression': progression,
        'a_acces_revision': a_acces_revision,
        'a_forfait_complet': a_forfait_complet,
    }
    return render(request, 'bibliotheque/tazawwud/module.html', context)


@login_required
def tazawwud_lecon(request, lecon_id):
    """Lecture interactive en étapes (Découverte -> Source -> Comprendre -> À Retenir)."""
    lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    if lecon.est_revision_finale:
        return redirect('tazawwud_revision', lecon_id=lecon.id)

    context = {
        'lecon': lecon,
        'progression': progression,
    }
    return render(request, 'bibliotheque/tazawwud/lecon.html', context)


# ── 4. QUIZ, RÉVISIONS ET SYSTÈME DE VIES ──

def formater_questions_pour_js(questions_queryset):
    """Encode les questions pour le moteur interactif JS (QCM, V/F, Association, Texte Court)."""
    questions_data = []
    for q in questions_queryset:
        choix_list = [{'id': c.id, 'texte': c.texte, 'est_correct': c.est_correct} for c in q.choix.all()]
        random.shuffle(choix_list)

        q_dict = {
            'id': q.id,
            'texte': q.texte,
            'type_question': q.type_question,
            'difficulte': q.difficulte,
            'points': q.points,
            'explication': q.explication_reponse,
            'choix': choix_list,
            'donnees_extra': q.donnees_extra or {},
        }
        questions_data.append(q_dict)
    return questions_data


@login_required
def tazawwud_quiz(request, lecon_id):
    """Quiz régulier de validation de leçon (gratuit)."""
    lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    # Récupérer les questions de cette leçon
    questions = lecon.questions.all().order_by('ordre', 'id')
    questions_data = formater_questions_pour_js(questions)

    context = {
        'lecon': lecon,
        'module': lecon.module,
        'progression': progression,
        'questions_json': json.dumps(questions_data),
        'is_revision': False,
        'mode_entrainement': False,
    }
    return render(request, 'bibliotheque/tazawwud/quiz.html', context)


@login_required
def tazawwud_revision(request, lecon_id):
    """
    Révision intensive de fin de module ou révision finale.
    Payante : 500 FCFA par module ou 2000 FCFA forfait complet.
    """
    lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    # Vérification des droits d'accès
    a_acces = TazawwudAchat.a_acces_revision(request.user, lecon.module)

    if not a_acces:
        # Afficher la page de présentation et de déblocage avec prix
        context = {
            'lecon': lecon,
            'module': lecon.module,
            'prix_module': 500,
            'prix_complet': 2000,
        }
        return render(request, 'bibliotheque/tazawwud/verrouille.html', context)

    # Si c'est la révision finale de tout le livre (lecon 99 ou titre 'Révision Finale')
    if lecon.numero == 99 or 'finale' in lecon.titre.lower():
        # Tirer 25 questions aléatoires de toute la banque du livre
        all_q_ids = list(TazawwudQuestion.objects.values_list('id', flat=True))
        selected_ids = random.sample(all_q_ids, min(len(all_q_ids), 25))
        questions = TazawwudQuestion.objects.filter(id__in=selected_ids).order_by('?')
    else:
        # Révision du module : questions du module + questions de la révision
        questions = TazawwudQuestion.objects.filter(lecon__module=lecon.module).order_by('?')[:15]

    questions_data = formater_questions_pour_js(questions)

    context = {
        'lecon': lecon,
        'module': lecon.module,
        'progression': progression,
        'questions_json': json.dumps(questions_data),
        'is_revision': True,
        'mode_entrainement': False,
    }
    return render(request, 'bibliotheque/tazawwud/quiz.html', context)


@login_required
def tazawwud_entrainement(request):
    """
    Mode entraînement gratuit (toujours accessible même à 0 vie).
    Permet de revoir les questions manquées et de recharger ses 3 vies !
    """
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    # Questions manquées par l'utilisateur
    erreurs_q_ids = list(TazawwudReponseHistorique.objects.filter(
        user=request.user, est_correct=False
    ).values_list('question_id', flat=True).distinct())

    if erreurs_q_ids:
        sample_ids = random.sample(erreurs_q_ids, min(len(erreurs_q_ids), 10))
        questions = TazawwudQuestion.objects.filter(id__in=sample_ids)
    else:
        # Fallback si aucune erreur enregistrée : questions faciles
        questions = TazawwudQuestion.objects.filter(difficulte='facile').order_by('?')[:8]

    questions_data = formater_questions_pour_js(questions)

    context = {
        'progression': progression,
        'questions_json': json.dumps(questions_data),
        'is_revision': False,
        'mode_entrainement': True,
    }
    return render(request, 'bibliotheque/tazawwud/quiz.html', context)


@login_required
def tazawwud_recharger_vies(request):
    """Recharge les vies de l'utilisateur."""
    if request.method == 'POST':
        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
        progression.recharger_vies()
        return JsonResponse({'status': 'success', 'vies': progression.vies_actuelles})
    return JsonResponse({'status': 'error'}, status=405)


# ── 5. APIS DE VALIDATION DES RÉPONSES & SAUVEGARDE ──

@csrf_exempt
@login_required
def api_tazawwud_reponse(request):
    """
    Valide une réponse individuelle, met à jour les vies et enregistre l'historique.
    Supporte : QCM, Vrai/Faux, Association, Réponse Courte.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        reponse_user = data.get('reponse')
        mode_entrainement = data.get('mode_entrainement', False)

        question = get_object_or_404(TazawwudQuestion, id=question_id)
        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

        est_correct = False

        if question.type_question in ['qcm', 'vrai_faux']:
            # reponse_user est l'ID du choix ou le texte
            choix_correct = question.choix.filter(est_correct=True).first()
            if choix_correct:
                if str(reponse_user) == str(choix_correct.id) or str(reponse_user).strip().lower() == choix_correct.texte.strip().lower():
                    est_correct = True

        elif question.type_question == 'texte_court':
            # reponse_user est une chaîne de caractères
            reponses_valides = question.donnees_extra.get('reponses_acceptees', [])
            val_clean = str(reponse_user or '').strip().lower()
            if val_clean in [r.strip().lower() for r in reponses_valides]:
                est_correct = True

        elif question.type_question == 'association':
            # reponse_user est un dict {"gauche": "droite"}
            paires_officielles = question.donnees_extra.get('paires', [])
            paires_dict = {p['gauche'].strip().lower(): p['droite'].strip().lower() for p in paires_officielles}

            if isinstance(reponse_user, dict):
                user_dict = {str(k).strip().lower(): str(v).strip().lower() for k, v in reponse_user.items()}
                # Toutes les paires correspondent ?
                if user_dict == paires_dict:
                    est_correct = True

        # Enregistrement dans l'historique pour analyse des erreurs
        TazawwudReponseHistorique.objects.create(
            user=request.user,
            question=question,
            est_correct=est_correct,
            reponse_donnee=str(reponse_user)[:500]
        )

        vies_restantes = progression.vies_actuelles
        if not est_correct and not mode_entrainement:
            vies_restantes = progression.perdre_vie()

        return JsonResponse({
            'status': 'success',
            'est_correct': est_correct,
            'explication': question.explication_reponse,
            'vies_restantes': vies_restantes,
            'points_gagnes': question.points if est_correct else 0,
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def api_tazawwud_save_score(request):
    """Valide la fin de session de quiz ou révision."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        lecon_id = data.get('lecon_id')
        score = int(data.get('score', 0))
        mode_entrainement = data.get('mode_entrainement', False)

        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

        if mode_entrainement:
            # En mode entraînement, on recharge automatiquement les vies
            progression.recharger_vies()
            return JsonResponse({'status': 'success', 'message': 'Vies rechargées !'})

        if lecon_id:
            lecon = get_object_or_404(TazawwudLecon, id=lecon_id)
            progression.lecons_terminees.add(lecon)

        progression.ajouter_points(score)
        return JsonResponse({'status': 'success', 'nouveau_score': progression.score_total})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# ── 6. PAIEMENTS FEDAPAY (RÉVISIONS PAYANTES) ──

@login_required
def tazawwud_initier_paiement(request):
    """
    Initie une transaction FedaPay :
    - 500 FCFA par module (type_achat='MODULE')
    - 2000 FCFA pour le forfait complet (type_achat='COMPLET')
    """
    if request.method != 'POST':
        return redirect('tazawwud_dashboard')

    type_achat = request.POST.get('type_achat', 'MODULE')
    module_id = request.POST.get('module_id')

    module = None
    if type_achat == 'MODULE':
        module = get_object_or_404(TazawwudModule, id=module_id)
        montant = 500
    else:
        type_achat = 'COMPLET'
        montant = 2000

    reference = f"TZW-{timezone.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

    achat = TazawwudAchat.objects.create(
        user=request.user,
        type_achat=type_achat,
        module=module,
        montant=montant,
        reference=reference,
        statut='PENDING'
    )

    callback_url = request.build_absolute_uri(reverse('tazawwud_paiement_callback'))
    webhook_url = request.build_absolute_uri(reverse('tazawwud_paiement_webhook'))

    customer_data = {
        'firstname': request.user.first_name or request.user.username,
        'lastname': request.user.last_name or 'SDM',
        'email': request.user.email,
        'phone': request.POST.get('telephone', '00000000')
    }

    result = creer_transaction_fedapay(achat, customer_data, callback_url, webhook_url=webhook_url)

    if result.get('success'):
        checkout_url = result.get('checkout_url')
        return redirect(checkout_url)
    else:
        return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
            'achat': achat,
            'statut_visuel': 'erreur',
            'message': result.get('error', "Impossible d'initier la session de paiement DexPay.")
        })


@login_required
def tazawwud_paiement_callback(request):
    """
    Retour après paiement DexPay.
    Vérifie formellement le statut auprès de l'API serveur DexPay avant d'accorder l'accès.
    """
    tx_id = request.GET.get('id')
    reference = request.GET.get('reference') or request.GET.get('ref')

    achat = None
    if reference:
        achat = TazawwudAchat.objects.filter(reference=reference).first()
    if not achat and tx_id:
        achat = TazawwudAchat.objects.filter(fedapay_transaction_id=str(tx_id)).first()

    if not achat:
        return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
            'statut_visuel': 'erreur',
            'message': "Transaction introuvable ou invalide."
        })

    # Interrogation directe et sécurisée du serveur DexPay via la référence de la session
    tx_check = verifier_transaction_fedapay(achat.reference or achat.fedapay_transaction_id or tx_id)

    if tx_check.get('success'):
        status = tx_check.get('status', '').lower()
        if status == 'approved':
            valider_achat_confirme(achat, tx_check.get('data'))
            return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
                'achat': achat,
                'statut_visuel': 'succes',
                'message': "Paiement confirmé par DexPay avec succès ! Votre révision est débloquée."
            })
        elif status == 'pending':
            return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
                'achat': achat,
                'statut_visuel': 'attente',
                'message': "Transaction en cours de traitement chez l'opérateur. Veuillez patienter ou actualiser."
            })
        else:
            achat.statut = 'DECLINED' if status in ['declined', 'failed'] else 'CANCELED'
            achat.save()
            return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
                'achat': achat,
                'statut_visuel': 'echec',
                'message': f"Le paiement n'a pas abouti (statut : {status}). Aucun montant n'a été débité."
            })

    return render(request, 'bibliotheque/tazawwud/paiement_status.html', {
        'achat': achat,
        'statut_visuel': 'erreur',
        'message': "Impossible de vérifier la transaction auprès de DexPay pour le moment."
    })


@csrf_exempt
def tazawwud_paiement_webhook(request):
    """
    Webhook IPN DexPay (reçu côté serveur en asynchrone).
    Gère les notifications multiples de manière idempotente.
    """
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        event_name = str(payload.get('event') or payload.get('name') or payload.get('type') or '').lower()
        entity = payload.get('data') or payload.get('entity') or payload
        ref = entity.get('reference') or payload.get('reference') or (entity.get('custom_metadata') or {}).get('reference')
        tx_id = entity.get('id') or payload.get('id')

        achat = None
        if ref:
            achat = TazawwudAchat.objects.filter(reference=str(ref)).first()
        if not achat and tx_id:
            achat = TazawwudAchat.objects.filter(fedapay_transaction_id=str(tx_id)).first()

        if not achat:
            return HttpResponse("No matching transaction", status=400)

        raw_status = str(entity.get('status') or payload.get('status') or '').lower()
        if (
            raw_status in ['completed', 'paid', 'success', 'succeeded', 'approved']
            or any(k in event_name for k in ['completed', 'paid', 'success', 'approved'])
        ):
            valider_achat_confirme(achat, payload)
        elif (
            raw_status in ['failed', 'declined', 'canceled', 'cancelled', 'expired']
            or any(k in event_name for k in ['failed', 'declined', 'cancel'])
        ):
            achat.statut = 'CANCELED' if 'cancel' in (raw_status + event_name) else 'DECLINED'
            achat.save()

        return HttpResponse("Webhook processed successfully", status=200)

    except Exception as e:
        return HttpResponse(f"Webhook error: {str(e)}", status=400)


@login_required
def tazawwud_paiement_simulation(request, reference):
    """
    Page de simulation locale / bac à sable pour tester le déblocage
    instantané sans carte bancaire lorsque FEDAPAY_ENVIRONMENT est en démo.
    """
    achat = get_object_or_404(TazawwudAchat, reference=reference, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'payer':
            valider_achat_confirme(achat, {'simulateur': 'bac_a_sable_sdm'})
            return redirect('tazawwud_dashboard')
        else:
            achat.statut = 'CANCELED'
            achat.save()
            return redirect('tazawwud_dashboard')

    return render(request, 'bibliotheque/tazawwud/simulation_paiement.html', {'achat': achat})


# ── 7. COMPAGNONS & FONCTIONNALITÉS SOCIALES ──

@login_required
def tazawwud_compagnons(request):
    """Page sociale : liste des compagnons, demandes reçues et recherche."""
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)

    # Compagnons confirmés
    liens = TazawwudCompagnon.objects.filter(
        Q(demandeur=request.user) | Q(ami=request.user),
        statut='ACCEPTE'
    ).select_related('demandeur', 'ami')

    amis = []
    for l in liens:
        autre = l.ami if l.demandeur == request.user else l.demandeur
        autre_prog = TazawwudProgression.objects.filter(user=autre).first()
        amis.append({
            'user': autre,
            'progression': autre_prog,
            'lien_id': l.id,
        })

    # Demandes reçues en attente
    demandes_recues = TazawwudCompagnon.objects.filter(ami=request.user, statut='EN_ATTENTE')

    context = {
        'progression': progression,
        'amis': amis,
        'demandes_recues': demandes_recues,
    }
    return render(request, 'bibliotheque/tazawwud/compagnons.html', context)


@csrf_exempt
@login_required
def api_tazawwud_ajouter_compagnon(request):
    """Envoie une demande de compagnon par nom d'utilisateur."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        cible = User.objects.filter(username__iexact=username).first()

        if not cible:
            return JsonResponse({'status': 'error', 'message': "Utilisateur introuvable."})
        if cible == request.user:
            return JsonResponse({'status': 'error', 'message': "Vous ne pouvez pas vous ajouter vous-même."})

        # Vérifier si lien existe déjà
        existant = TazawwudCompagnon.objects.filter(
            Q(demandeur=request.user, ami=cible) | Q(demandeur=cible, ami=request.user)
        ).first()

        if existant:
            if existant.statut == 'ACCEPTE':
                return JsonResponse({'status': 'error', 'message': "Vous êtes déjà compagnons !"})
            elif existant.statut == 'EN_ATTENTE':
                return JsonResponse({'status': 'error', 'message': "Une demande est déjà en attente."})

        TazawwudCompagnon.objects.create(demandeur=request.user, ami=cible, statut='EN_ATTENTE')
        return JsonResponse({'status': 'success', 'message': f"Demande envoyée à {cible.username} !"})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def api_tazawwud_repondre_compagnon(request):
    """Accepte ou refuse une demande de compagnon."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    try:
        data = json.loads(request.body)
        demande_id = data.get('demande_id')
        decision = data.get('decision') # 'accepter' ou 'refuser'

        demande = get_object_or_404(TazawwudCompagnon, id=demande_id, ami=request.user)
        if decision == 'accepter':
            demande.statut = 'ACCEPTE'
            demande.save()
        else:
            demande.statut = 'REFUSE'
            demande.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def tazawwud_toggle_visibilite(request):
    """Active ou désactive la visibilité publique du profil et de la progression."""
    if request.method == 'POST':
        progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
        progression.est_profil_public = not progression.est_profil_public
        progression.save()
        return JsonResponse({'status': 'success', 'est_public': progression.est_profil_public})
    return JsonResponse({'status': 'error'}, status=405)


@login_required
def tazawwud_classement_hebdo(request):
    """Classement hebdomadaire des élèves avec remise à zéro chaque semaine."""
    progression, _ = TazawwudProgression.objects.get_or_create(user=request.user)
    progression.verifier_semaine_reset()

    top_eleves = TazawwudProgression.objects.filter(
        est_profil_public=True
    ).select_related('user').order_by('-points_semaine')[:30]

    context = {
        'progression': progression,
        'top_eleves': top_eleves,
    }
    return render(request, 'bibliotheque/tazawwud/classement.html', context)


# ── 8. DÉFIS ENTRE COMPAGNONS ──

@login_required
def tazawwud_creer_defi(request):
    """Crée un duel de quiz entre compagnons."""
    module_id = request.POST.get('module_id')
    module = get_object_or_404(TazawwudModule, id=module_id) if module_id else None

    # Sélection de 5 questions aléatoires
    if module:
        q_ids = list(TazawwudQuestion.objects.filter(lecon__module=module).values_list('id', flat=True))
    else:
        q_ids = list(TazawwudQuestion.objects.values_list('id', flat=True))

    selected = random.sample(q_ids, min(len(q_ids), 5))
    code = f"DEF-{uuid.uuid4().hex[:6].upper()}"

    defi = TazawwudDefi.objects.create(
        createur=request.user,
        code=code,
        module=module,
        questions_ids=selected,
        statut='EN_ATTENTE'
    )
    return redirect('tazawwud_jouer_defi', code=code)


@login_required
def tazawwud_jouer_defi(request, code):
    """Joue la partie d'un défi."""
    defi = get_object_or_404(TazawwudDefi, code=code)
    questions = TazawwudQuestion.objects.filter(id__in=defi.questions_ids)
    questions_data = formater_questions_pour_js(questions)

    # Si c'est l'adversaire qui rejoint
    if defi.createur != request.user and not defi.adversaire:
        defi.adversaire = request.user
        defi.save()

    context = {
        'defi': defi,
        'questions_json': json.dumps(questions_data),
        'est_createur': (defi.createur == request.user),
    }
    return render(request, 'bibliotheque/tazawwud/defi_play.html', context)
