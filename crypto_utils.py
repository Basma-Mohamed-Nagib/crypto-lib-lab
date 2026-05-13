"""
Hybrid Encryption (AES + RSA).
"""

import os
import hashlib
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad


# ──────────────────────────────────────────────
# 1. RSA Key Generation
# ──────────────────────────────────────────────

def generate_rsa_keys(private_path="keys/private.pem", public_path="keys/public.pem"):
    """Generate RSA 2048-bit key pair and save to files."""
    key = RSA.generate(2048)

    with open(private_path, "wb") as f:
        f.write(key.export_key())

    with open(public_path, "wb") as f:
        f.write(key.publickey().export_key())

    print(f"[+] RSA keys generated successfully.")
    print(f"    Private key → {private_path}")
    print(f"    Public key  → {public_path}")


# ──────────────────────────────────────────────
# 2. AES Key Generation
# ──────────────────────────────────────────────

def generate_aes_key():
    """Generate a random 256-bit AES key."""
    return os.urandom(32)  # 32 bytes = 256 bits


# ──────────────────────────────────────────────
# 3. File Encryption (AES)
# ──────────────────────────────────────────────

def encrypt_file(input_path, output_path, aes_key):
    """
    Encrypt a file using AES-CBC.
    Generates a random IV and prepends it to the ciphertext.
    Returns the IV used.
    """
    iv = os.urandom(16)  # Random 128-bit IV
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    with open(input_path, "rb") as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_path, "wb") as f:
        f.write(iv + ciphertext)  # Save IV + ciphertext together

    print(f"[+] File encrypted successfully → {output_path}")
    return iv


# ──────────────────────────────────────────────
# 4. AES Key Encryption (RSA)
# ──────────────────────────────────────────────

def encrypt_aes_key(aes_key, public_key_path, output_path):
    """Encrypt the AES key using RSA public key (OAEP padding)."""
    with open(public_key_path, "rb") as f:
        public_key = RSA.import_key(f.read())

    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)

    with open(output_path, "wb") as f:
        f.write(encrypted_key)

    print(f"[+] AES key encrypted with RSA → {output_path}")


# ──────────────────────────────────────────────
# 5. AES Key Decryption (RSA)
# ──────────────────────────────────────────────

def decrypt_aes_key(encrypted_key_path, private_key_path):
    """Decrypt the AES key using RSA private key."""
    with open(private_key_path, "rb") as f:
        private_key = RSA.import_key(f.read())

    with open(encrypted_key_path, "rb") as f:
        encrypted_key = f.read()

    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_key)

    print(f"[+] AES key decrypted successfully using RSA private key.")
    return aes_key


# ──────────────────────────────────────────────
# 6. File Decryption (AES)
# ──────────────────────────────────────────────

def decrypt_file(input_path, output_path, aes_key):
    """
    Decrypt a file using AES-CBC.
    Reads IV from the first 16 bytes of the encrypted file.
    """
    with open(input_path, "rb") as f:
        data = f.read()

    iv = data[:16]           # First 16 bytes = IV
    ciphertext = data[16:]   # Rest = actual ciphertext

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_path, "wb") as f:
        f.write(plaintext)

    print(f"[+] File decrypted successfully → {output_path}")


# ──────────────────────────────────────────────
# 7. Verification (SHA-256)
# ──────────────────────────────────────────────

def verify_files(original_path, decrypted_path):
    """Compare SHA-256 hashes of original and decrypted files."""
    def sha256(path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    hash_original  = sha256(original_path)
    hash_decrypted = sha256(decrypted_path)

    print(f"\n[SHA-256 Verification]")
    print(f"  Original  : {hash_original}")
    print(f"  Decrypted : {hash_decrypted}")

    if hash_original == hash_decrypted:
        print("  Result    :  SUCCESS — Decrypted file matches the original!")
    else:
        print("  Result    :  FAILED — Files do NOT match!")

    return hash_original == hash_decrypted