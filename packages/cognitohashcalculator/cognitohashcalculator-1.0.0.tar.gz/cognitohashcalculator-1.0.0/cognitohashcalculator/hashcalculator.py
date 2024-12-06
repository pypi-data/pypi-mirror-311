import hmac
import hashlib
import base64

def calculate_secret_hash(client_id, client_secret, username):
    message = username + client_id
    digest = hmac.new(
        client_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode('utf-8')