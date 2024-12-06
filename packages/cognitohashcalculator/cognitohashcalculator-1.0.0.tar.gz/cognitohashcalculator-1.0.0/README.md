# **Secret Hash Generator**

This function, `calculate_secret_hash`, generates a secure hash using HMAC (Hash-based Message Authentication Code) and SHA-256. It's useful for authentication and securely verifying user credentials for Amazon Cognito.

---

## **Function Overview**

### **`calculate_secret_hash`**

This function creates a secret hash by combining the username and client ID, secured with a client secret key.

### **Parameters**
- **`client_id`** *(str)*:  
  The unique identifier for the client.
  
- **`client_secret`** *(str)*:  
  The secret key associated with the client ID, used for hashing.
  
- **`username`** *(str)*:  
  The username or user identifier to include in the hash computation.

### **Returns**
- A **base64-encoded string** representing the HMAC SHA-256 hash.

---

## **Dependencies**
The function uses Python's **standard library**, so no external installations are required. Specifically, it uses:
- **`hmac`**
- **`hashlib`**
- **`base64`**

---

## **Usage**

```python
from mylibrary import calculate_secret_hash

# Example inputs
client_id = "exampleClientId123"
client_secret = "superSecretKey456"
username = "user@example.com"

# Generate the secret hash
secret_hash = calculate_secret_hash(client_id, client_secret, username)
print(f"Generated Secret Hash: {secret_hash}")
