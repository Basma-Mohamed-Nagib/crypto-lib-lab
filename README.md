# 🔐 Cryptography Lib Lab — Hybrid Encryption

A cryptography application that encrypts and decrypts real student records using **Hybrid Encryption (AES-256 + RSA-2048)**.

Built as part of the Cryptography / Information Security Lab course.

---

## 📌 Scenario
Secure Student Records — encrypting a CSV file containing student names, IDs, and grades.

---

## ⚙️ Algorithms Used

| Algorithm | Type | Purpose |
|-----------|------|---------|
| AES-256-CBC | Symmetric | Encrypt the actual data file |
| RSA-2048 | Asymmetric | Encrypt the AES key |
| SHA-256 | Hash | Verify decrypted file matches original |
| Base64 | Encoding | Display ciphertext in readable format |

---

## 🗂️ Project Structure

```
crypto_project/
├── main.py              # Main program (terminal)
├── crypto_utils.py      # All encryption/decryption functions
├── gui.py               # Graphical user interface (Tkinter)
├── data/
│   └── students.csv     # Original input data
├── keys/
│   ├── private.pem      # RSA private key
│   └── public.pem       # RSA public key
└── output/
    ├── students_encrypted.bin   # AES encrypted file
    ├── aes_key_encrypted.bin    # RSA encrypted AES key
    └── students_decrypted.csv   # Decrypted output
```

---

## 🚀 How to Run

### 1. Install the required library
```bash
pip install pycryptodome
```

### 2. Run via terminal
```bash
python main.py
```

### 3. Run with GUI
```bash
python gui.py
```

---

## 🔄 How It Works

```
students.csv
    ↓ Encrypt with AES-256-CBC
students_encrypted.bin
    +
AES Key → Encrypt with RSA Public Key → aes_key_encrypted.bin

─────────────── Decryption ───────────────

aes_key_encrypted.bin
    ↓ Decrypt with RSA Private Key
AES Key recovered
    ↓ Decrypt students_encrypted.bin
students_decrypted.csv
    ↓ SHA-256 verification
✅ Matches original
```

---

## 🖥️ GUI Features

- 🟢 **Generate RSA Keys** — generates public/private key pair
- 🔴 **Encrypt** — encrypts the selected file
- 🔵 **Decrypt & Verify** — decrypts and verifies with SHA-256
- 📋 **Base64 Preview** — displays ciphertext in readable Base64 format
- 📟 **Live Log** — shows each step as it executes

---

## 📦 Dependencies

- [PyCryptodome](https://pycryptodome.readthedocs.io/) — AES, RSA, Padding
- `hashlib` — SHA-256 (built-in)
- `base64` — Base64 encoding (built-in)
- `tkinter` — GUI (built-in)

---

## 📋 Program Flow

1. Load original data from file
2. Generate RSA-2048 key pair
3. Generate random AES-256 key
4. Encrypt file with AES-CBC + random IV
5. Encrypt AES key with RSA public key
6. Save ciphertext + encrypted AES key
7. Decrypt AES key with RSA private key
8. Decrypt file with recovered AES key
9. Verify with SHA-256 hash comparison
