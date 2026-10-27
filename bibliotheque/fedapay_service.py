import logging
import requests
from urllib.parse import urlparse
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_dexpay_keys():
    api_key = getattr(settings, 'DEXPAY_API_KEY', '') or getattr(settings, 'FEDAPAY_PUBLIC_KEY', '')
    api_secret = getattr(settings, 'DEXPAY_API_SECRET', '') or getattr(settings, 'FEDAPAY_SECRET_KEY', '')
    return api_key.strip(), api_secret.strip()


def get_dexpay_base_url():
    """
    Détermine automatiquement l'URL de base de l'API DexPay :
    - Sandbox / Test (pk_test_ / sk_test_) : https://api-sandbox.dexpay.africa/api/v1
    - Production (pk_live_ / sk_live_)     : https://api.dexpay.africa/api/v1
    """
    api_key, api_secret = get_dexpay_keys()
    env = getattr(settings, 'DEXPAY_ENVIRONMENT', 'test').lower()

    if api_key.startswith('pk_test_') or api_secret.startswith('sk_test_') or env in ['test', 'sandbox']:
        return 'https://api-sandbox.dexpay.africa/api/v1'
    return 'https://api.dexpay.africa/api/v1'


def get_dexpay_headers():
    api_key, api_secret = get_dexpay_keys()
    return {
        'x-api-key': api_key,
        'x-api-secret': api_secret,
        'Content-Type': 'application/json',
    }


def _normalize_public_url(url_str, fallback_path='/tazawwud/paiement/callback/'):
    """
    DexPay valide strictement que success_url, failure_url et webhook_url
    soient des URLs publiques avec nom de domaine valide (pas localhost / testserver).
    """
    if not url_str:
        return f"https://sdm-mourit.onrender.com{fallback_path}"
    parsed = urlparse(url_str)
    host = (parsed.hostname or '').lower()
    if host in ['localhost', '127.0.0.1', 'testserver', '0.0.0.0', '']:
        path_and_query = parsed.path or fallback_path
        if parsed.query:
            path_and_query += f"?{parsed.query}"
        return f"https://sdm-mourit.onrender.com{path_and_query}"
    if url_str.startswith('http://') and ('onrender.com' in host or 'sdm-mouride.com' in host):
        return 'https://' + url_str[len('http://'):]
    return url_str


def creer_transaction_fedapay(achat, customer_data, callback_url, webhook_url=None):
    """
    Crée une session de paiement auprès de l'API officielle DexPay
    (POST /api/v1/checkout-sessions) et retourne le lien de paiement (payment_url).
    """
    api_key, api_secret = get_dexpay_keys()

    # Fallback simulation si aucune clé DexPay n'est configurée
    if not api_key or not api_secret or 'demo' in api_secret or 'mock' in api_secret:
        logger.warning("DexPay: Clés absentes ou démo, utilisation du mode simulation.")
        achat.fedapay_transaction_id = f"sim_{achat.reference}"
        achat.metadata_json = {
            'provider': 'dexpay_simulation',
            'simulated_at': timezone.now().isoformat(),
        }
        achat.save()
        return {
            'success': True,
            'is_simulation': True,
            'checkout_url': f"/tazawwud/paiement/simulation/{achat.reference}/",
            'transaction_id': achat.fedapay_transaction_id,
        }

    base_url = get_dexpay_base_url()
    clean_callback = _normalize_public_url(callback_url, '/tazawwud/paiement/callback/')
    sep = '&' if '?' in clean_callback else '?'
    success_url = f"{clean_callback}{sep}reference={achat.reference}&status=success"
    failure_url = f"{clean_callback}{sep}reference={achat.reference}&status=failed"

    if not webhook_url:
        webhook_url = clean_callback.replace('/callback/', '/webhook/')
    clean_webhook = _normalize_public_url(webhook_url, '/tazawwud/paiement/webhook/')

    if achat.type_achat == 'COMPLET':
        item_name = "Tazawwudu-ç-Çighâr — Forfait Complet Révisions (Tout le Livre)"
    elif achat.module:
        item_name = f"Tazawwudu-ç-Çighâr — Révision Partie {achat.module.numero} ({achat.module.titre})"
    else:
        item_name = f"Tazawwudu-ç-Çighâr — {achat.get_type_achat_display()}"

    payload = {
        "reference": achat.reference,
        "item_name": item_name[:120],
        "amount": int(achat.montant),
        "currency": "XOF",
        "success_url": success_url,
        "failure_url": failure_url,
        "webhook_url": clean_webhook,
    }

    try:
        url = f"{base_url}/checkout-sessions"
        resp = requests.post(url, json=payload, headers=get_dexpay_headers(), timeout=15)
        data = resp.json() if resp.content else {}

        if resp.status_code in [200, 201]:
            session_data = data.get('data') or data
            payment_url = (
                session_data.get('payment_url')
                or session_data.get('sandbox_payment_url')
                or (session_data.get('payment_attempt') or {}).get('cashout_url')
            )
            tx_ref = session_data.get('reference') or session_data.get('id') or achat.reference

            achat.fedapay_transaction_id = str(tx_ref)
            achat.metadata_json = {
                'provider': 'dexpay',
                'session': session_data,
            }
            achat.save()

            return {
                'success': True,
                'is_simulation': False,
                'checkout_url': payment_url,
                'transaction_id': str(tx_ref),
            }
        else:
            logger.error(f"DexPay Create Error ({resp.status_code}): {resp.text}")
            return {
                'success': False,
                'error': data.get('message', f"Erreur DexPay ({resp.status_code})"),
            }

    except Exception as e:
        logger.exception("Erreur lors de la communication avec DexPay")
        return {
            'success': False,
            'error': str(e),
        }


def verifier_transaction_fedapay(transaction_id_or_ref):
    """
    Vérifie le statut réel d'une session de paiement directement auprès du serveur DexPay :
    GET {base_url}/checkout-sessions/{reference}
    Retourne: {'success': bool, 'status': 'approved'|'pending'|'declined'|'canceled', 'data': dict}
    """
    if not transaction_id_or_ref:
        return {'success': False, 'error': 'Référence manquante'}

    if str(transaction_id_or_ref).startswith('sim_'):
        return {
            'success': True,
            'status': 'approved',
            'is_simulation': True,
            'data': {'simulated': True},
        }

    base_url = get_dexpay_base_url()
    try:
        url = f"{base_url}/checkout-sessions/{transaction_id_or_ref}"
        resp = requests.get(url, headers=get_dexpay_headers(), timeout=15)
        if resp.status_code == 200:
            raw = resp.json()
            tx = raw.get('data') or raw
            raw_status = str(tx.get('status') or '').lower()
            attempt_status = str((tx.get('payment_attempt') or {}).get('status') or '').lower()
            completed_at = tx.get('completed_at')
            total_payments = int(tx.get('total_payments') or 0)

            if (
                raw_status in ['completed', 'paid', 'success', 'succeeded', 'approved']
                or attempt_status in ['completed', 'paid', 'success', 'succeeded', 'approved']
                or completed_at is not None
                or total_payments > 0
            ):
                norm_status = 'approved'
            elif raw_status in ['failed', 'declined', 'expired', 'error'] or attempt_status in ['failed', 'declined']:
                norm_status = 'declined'
            elif raw_status in ['canceled', 'cancelled'] or attempt_status in ['canceled', 'cancelled']:
                norm_status = 'canceled'
            else:
                norm_status = 'pending'

            return {
                'success': True,
                'status': norm_status,
                'raw_status': raw_status,
                'data': tx,
            }
        else:
            return {
                'success': False,
                'error': f"Session DexPay introuvable ({resp.status_code})",
            }
    except Exception as e:
        logger.exception("Erreur lors de la vérification DexPay")
        return {
            'success': False,
            'error': str(e),
        }


def valider_achat_confirme(achat, transaction_details=None):
    """
    Passe l'achat en APPROVED de manière idempotente et accorde l'accès.
    """
    if achat.statut == 'APPROVED':
        return True  # Déjà validé (idempotence)

    achat.statut = 'APPROVED'
    achat.date_confirmation = timezone.now()
    if transaction_details:
        current_meta = achat.metadata_json or {}
        current_meta['confirmation'] = transaction_details
        achat.metadata_json = current_meta
    achat.save()
    logger.info(f"Achat DexPay {achat.reference} ({achat.type_achat}) validé pour {achat.user.username}")
    return True
