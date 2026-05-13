"""
main.py
-------
Cryptography Lib Lab Project
Scenario : Secure Student Records
Algorithm: Hybrid Encryption (AES-256-CBC + RSA-2048)
"""

from crypto_utils import (
    generate_rsa_keys,
    generate_aes_key,
    encrypt_file,
    encrypt_aes_key,
    decrypt_aes_key,
    decrypt_file,
    verify_files,
)

# ── File Paths ──────────────────────────────────
ORIGINAL_FILE       = "data/students.csv"
ENCRYPTED_FILE      = "output/students_encrypted.bin"
DECRYPTED_FILE      = "output/students_decrypted.csv"
ENCRYPTED_AES_KEY   = "output/aes_key_encrypted.bin"
PRIVATE_KEY         = "keys/private.pem"
PUBLIC_KEY          = "keys/public.pem"


def main():
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("output", exist_ok=True)
    os.makedirs("keys", exist_ok=True)
    print("=" * 55)
    print("   Cryptography Lib Lab — Hybrid Encryption Demo")
    print("=" * 55)

    # ── Step 1: Load original data ──────────────────
    print("\n[Step 1] Loading original data...")
    with open(ORIGINAL_FILE, "r") as f:
        print(f.read())
    print(f"  File loaded: {ORIGINAL_FILE}")

    # ── Step 2: Generate RSA key pair ───────────────
    print("\n[Step 2] Generating RSA-2048 key pair...")
    generate_rsa_keys(PRIVATE_KEY, PUBLIC_KEY)

    # ── Step 3: Generate AES key ─────────────────────
    print("\n[Step 3] Generating AES-256 key...")
    aes_key = generate_aes_key()
    print(f"  AES Key (hex): {aes_key.hex()}")

    # ── Step 4: Encrypt the file with AES ───────────
    print("\n[Step 4] Encrypting file with AES-256-CBC...")
    encrypt_file(ORIGINAL_FILE, ENCRYPTED_FILE, aes_key)

    # ── Step 5: Encrypt AES key with RSA ────────────
    print("\n[Step 5] Encrypting AES key with RSA public key...")
    encrypt_aes_key(aes_key, PUBLIC_KEY, ENCRYPTED_AES_KEY)

    # ── Step 6: Show encrypted output sample ────────
    print("\n[Step 6] Encrypted file preview (first 32 bytes as hex):")
    with open(ENCRYPTED_FILE, "rb") as f:
        print(f"  {f.read(32).hex()} ...")

    # ── Step 7: Decrypt AES key with RSA ────────────
    print("\n[Step 7] Decrypting AES key with RSA private key...")
    recovered_aes_key = decrypt_aes_key(ENCRYPTED_AES_KEY, PRIVATE_KEY)
    print(f"  Recovered AES Key (hex): {recovered_aes_key.hex()}")

    # ── Step 8: Decrypt the file with AES ───────────
    print("\n[Step 8] Decrypting file with recovered AES key...")
    decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, recovered_aes_key)

    # ── Step 9: Verify ──────────────────────────────
    print("\n[Step 9] Verifying integrity...")
    verify_files(ORIGINAL_FILE, DECRYPTED_FILE)

    print("\n" + "=" * 55)
    print("   Demo complete!")
    print("=" * 55)


if __name__ == "__main__":
    main()