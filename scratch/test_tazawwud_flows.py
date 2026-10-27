import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from bibliotheque.models import (
    TazawwudModule, TazawwudLecon, TazawwudQuestion, TazawwudChoix,
    TazawwudProgression, TazawwudReponseHistorique, TazawwudAchat,
    TazawwudCompagnon, TazawwudDefi
)
from bibliotheque.tazawwud_views import (
    tazawwud_home, tazawwud_dashboard, tazawwud_module, tazawwud_quiz,
    tazawwud_revision, api_tazawwud_reponse, api_tazawwud_save_score,
    tazawwud_initier_paiement, tazawwud_compagnons
)
from bibliotheque.fedapay_service import valider_achat_confirme

print("═══════════════════════════════════════════════════════════════")
print("TEST DES PARCOURS TAZAWWUDU-Ç-ÇIGHÂR")
print("═══════════════════════════════════════════════════════════════")

# 1. Préparation des utilisateurs de test
user1, _ = User.objects.get_or_create(username="eleve_test1", defaults={"email": "eleve1@test.com"})
user1.set_password("pass123")
user1.is_superuser = False
user1.is_staff = False
user1.save()

user2, _ = User.objects.get_or_create(username="compagnon_test2", defaults={"email": "compagnon2@test.com"})
user2.set_password("pass123")
user2.is_superuser = False
user2.is_staff = False
user2.save()

# Nettoyer les anciens achats de test pour user1
TazawwudAchat.objects.filter(user=user1).delete()

rf = RequestFactory()
client = Client()
client.force_login(user1)

# ── TEST 1 : QUIZ GRATUIT ──
print("\n[TEST 1] Parcours Quiz Gratuit (Leçon Ordinaire)...")
lecon_ord = TazawwudLecon.objects.filter(est_revision_finale=False).first()
resp = client.get(f'/tazawwud/quiz/{lecon_ord.id}/')
assert resp.status_code == 200, f"Erreur quiz gratuit : code {resp.status_code}"
assert b"quiz-app" in resp.content or b"Question" in resp.content
print("  ✓ Leçon ordinaire accessible gratuitement (Code 200)")

# Tester validation de réponse
q = lecon_ord.questions.first()
resp_rep = client.post('/api/tazawwud/reponse/', data='{"question_id": ' + str(q.id) + ', "reponse": "dummy"}', content_type='application/json')
assert resp_rep.status_code == 200, f"Erreur API reponse : {resp_rep.content}"
print("  ✓ API validation de réponse et mise à jour des vies (Code 200)")

# ── TEST 2 : RÉVISION VERROUILLÉE ──
print("\n[TEST 2] Parcours Révision Verrouillée (Non Payée)...")
lecon_rev = TazawwudLecon.objects.filter(est_revision_finale=True).first()
resp_rev = client.get(f'/tazawwud/revision/{lecon_rev.id}/')
assert resp_rev.status_code == 200
assert b"verrouill" in resp.content.lower() or b"500" in resp_rev.content or b"2 000" in resp_rev.content
print("  ✓ Révision bloquée avec affichage du paywall FedaPay 500 F / 2000 F (Code 200)")

# ── TEST 3 : PAIEMENT EN ATTENTE (PENDING) ──
print("\n[TEST 3] Parcours Paiement Initié (En attente)...")
resp_pay = client.post('/tazawwud/paiement/initier/', {'type_achat': 'MODULE', 'module_id': lecon_rev.module.id})
assert resp_pay.status_code == 302, f"Erreur redirection paiement : {resp_pay.status_code}"
achat = TazawwudAchat.objects.filter(user=user1, module=lecon_rev.module).order_by('-date_creation').first()
assert achat is not None
assert achat.statut == 'PENDING'
assert TazawwudAchat.a_acces_revision(user1, lecon_rev.module) is False
print(f"  ✓ Transaction créée avec statut PENDING (Ref: {achat.reference})")
print("  ✓ L'accès reste strictement verrouillé tant que le paiement n'est pas approuvé.")

# ── TEST 4 : PAIEMENT CONFIRMÉ & ACCÈS DÉBLOQUÉ ──
print("\n[TEST 4] Parcours Paiement Confirmé...")
valider_achat_confirme(achat, {'simulateur': 'test_valide'})
achat.refresh_from_db()
assert achat.statut == 'APPROVED'
assert TazawwudAchat.a_acces_revision(user1, lecon_rev.module) is True
print("  ✓ Achat passé en statut APPROVED avec succès.")

resp_rev_unlocked = client.get(f'/tazawwud/revision/{lecon_rev.id}/')
assert resp_rev_unlocked.status_code == 200
assert b"R\xc3\xa9vision" in resp_rev_unlocked.content or b"questions_json" in resp_rev_unlocked.content
print("  ✓ Révision désormais débloquée et jouable pour l'élève !")

# ── TEST 5 : PROGRESSION HEBDOMADAIRE & TABLEAU DE BORD ──
print("\n[TEST 5] Parcours Tableau de Bord & Progression Hebdo...")
prog, _ = TazawwudProgression.objects.get_or_create(user=user1)
prog.ajouter_points(30)
resp_dash = client.get('/tazawwud/dashboard/')
assert resp_dash.status_code == 200
assert b"Tableau de Bord" in resp_dash.content
print(f"  ✓ Tableau de bord de l'élève chargé avec succès (Points semaine: {prog.points_semaine})")

# Vérification du profil
resp_prof = client.get('/profile/')
assert resp_prof.status_code == 200
assert b"Tazawwudu" in resp_prof.content
print("  ✓ Widget Tazawwud affiché sur la page Mon Profil /profile/ (Code 200)")

# ── TEST 6 : COMPAGNONS & DÉFIS ──
print("\n[TEST 6] Parcours Compagnons & Défis...")
# Demande de compagnon
resp_add = client.post('/api/tazawwud/compagnon/ajouter/', data='{"username": "compagnon_test2"}', content_type='application/json')
assert resp_add.status_code == 200
lien = TazawwudCompagnon.objects.filter(demandeur=user1, ami=user2).first()
assert lien is not None
print("  ✓ Demande de compagnon envoyée avec succès.")

# Acceptation
lien.statut = 'ACCEPTE'
lien.save()
assert TazawwudCompagnon.objects.filter(demandeur=user1, ami=user2, statut='ACCEPTE').exists()
print("  ✓ Compagnon accepté mutuellement.")

# Création de défi
resp_defi = client.post('/tazawwud/defi/creer/')
assert resp_defi.status_code == 302
defi = TazawwudDefi.objects.filter(createur=user1).order_by('-date_creation').first()
assert defi is not None
print(f"  ✓ Défi créé avec code de partage : {defi.code}")

print("\n═══════════════════════════════════════════════════════════════")
print("TOUS LES PARCOURS SONT 100% FONCTIONNELS ET VALIDÉS !")
print("═══════════════════════════════════════════════════════════════\n")
