import logging
import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

def get_fedapay_base_url():
    env = getattr(settings, 'FEDAPAY_ENVIRONMENT', 'sandbox').lower()
    if env == 'live' or env == 'production':
        return 'https://api.fedapay.com/v1'
    return 'https://sandbox-api.fedapay.com/v1'

def get_fedapay_headers():
    secret_key = getattr(settings, 'FEDAPAY_SECRET_KEY', '')
    return {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json',
    }

def creer_transaction_fedapay(achat, customer_data, callback_url):
    """
    Crée une transaction auprès de l'API officielle FedaPay
    et génère le token/URL de redirection de paiement.
    """
    secret_key = getattr(settings, 'FEDAPAY_SECRET_KEY', '')
    base_url = get_fedapay_base_url()

    # Si nous sommes en mode démo / simulation locale sans clé FedaPay valide
    if not secret_key or secret_key.startswith('sk_sandbox_demo') or 'mock' in secret_key:
        logger.warning("FedaPay: Utilisation du mode simulation (clé démo configurée).")
        achat.fedapay_transaction_id = f"sim_{achat.reference}"
        achat.metadata_json = {
            'mode': 'simulation',
            'simulated_at': timezone.now().isoformat()
        }
        achat.save()
        # Redirection vers la page de simulation / validation
        return {
            'success': True,
            'is_simulation': True,
            'checkout_url': f"/tazawwud/paiement/simulation/{achat.reference}/",
            'transaction_id': achat.fedapay_transaction_id,
        }

    try:
        url = f"{base_url}/transactions"
        payload = {
            "description": f"SDM Tazawwud - {achat.get_type_achat_display()}",
            "amount": int(achat.montant),
            "currency": {"iso": "XOF"},
            "callback_url": callback_url,
            "customer": {
                "firstname": customer_data.get('firstname', achat.user.first_name or achat.user.username),
                "lastname": customer_data.get('lastname', achat.user.last_name or 'SDM'),
                "email": customer_data.get('email', achat.user.email or f"{achat.user.username}@sdm-mouride.com"),
                "phone_number": {
                    "number": customer_data.get('phone', '00000000')
                }
            },
            "custom_metadata": {
                "achat_id": achat.id,
                "reference": achat.reference,
                "user_id": achat.user.id,
                "type_achat": achat.type_achat,
                "module_id": achat.module.id if achat.module else None,
            }
        }

        resp = requests.post(url, json=payload, headers=get_fedapay_headers(), timeout=15)
        data = resp.json()

        if resp.status_code in [200, 201]:
            # Récupérer l'ID de la transaction créée
            # FedaPay renvoie {"v1/transaction": {"id": 123, ...}}
            tx_data = data.get('v1/transaction') or data.get('transaction') or data
            tx_id = tx_data.get('id')

            achat.fedapay_transaction_id = str(tx_id)
            achat.metadata_json = tx_data
            achat.save()

            # Générer le token de paiement
            token_url = f"{base_url}/transactions/{tx_id}/token"
            token_resp = requests.post(token_url, headers=get_fedapay_headers(), timeout=15)
            token_data = token_resp.json()

            checkout_url = token_data.get('url')
            if not checkout_url and 'token' in token_data:
                checkout_url = f"https://checkout.fedapay.com/checkout?token={token_data['token']}"

            return {
                'success': True,
                'is_simulation': False,
                'checkout_url': checkout_url,
                'transaction_id': tx_id
            }
        else:
            logger.error(f"FedaPay Create Error: {resp.status_code} - {resp.text}")
            return {
                'success': False,
                'error': data.get('message', f"Erreur FedaPay ({resp.status_code})")
            }

    except Exception as e:
        logger.exception("Erreur lors de la communication avec FedaPay")
        return {
            'success': False,
            'error': str(e)
        }

def verifier_transaction_fedapay(transaction_id):
    """
    Vérifie le statut réel d'une transaction directement auprès de l'API FedaPay.
    Retourne: {'success': bool, 'status': 'approved'|'pending'|'declined'|'canceled', 'data': dict}
    """
    if str(transaction_id).startswith('sim_'):
        return {
            'success': True,
            'status': 'approved',
            'is_simulation': True,
            'data': {'simulated': True}
        }

    base_url = get_fedapay_base_url()
    try:
        url = f"{base_url}/transactions/{transaction_id}"
        resp = requests.get(url, headers=get_fedapay_headers(), timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            tx = data.get('v1/transaction') or data.get('transaction') or data
            status = tx.get('status', '').lower()
            return {
                'success': True,
                'status': status,
                'data': tx
            }
        else:
            return {
                'success': False,
                'error': f"Statut FedaPay introuvable ({resp.status_code})"
            }
    except Exception as e:
        logger.exception("Erreur lors de la vérification FedaPay")
        return {
            'success': False,
            'error': str(e)
        }

def valider_achat_confirme(achat, transaction_details=None):
    """
    Passe l'achat en APPROVED de manière idempotente et accorde l'accès.
    """
    if achat.statut == 'APPROVED':
        return True # Déjà validé (idempotence)

    achat.statut = 'APPROVED'
    achat.date_confirmation = timezone.now()
    if transaction_details:
        current_meta = achat.metadata_json or {}
        current_meta['confirmation'] = transaction_details
        achat.metadata_json = current_meta
    achat.save()
    logger.info(f"Achat {achat.reference} ({achat.type_achat}) validé pour l'utilisateur {achat.user.username}")
    return True
