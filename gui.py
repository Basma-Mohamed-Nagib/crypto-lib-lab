"""
gui.py
------
Cryptography Lib Lab Project — Graphical User Interface
Scenario : Secure Student Records
Algorithm: Hybrid Encryption (AES-256-CBC + RSA-2048)
Features : Encrypt, Decrypt, Base64 preview, SHA-256 verification
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import base64
import os

from crypto_utils import (
    generate_rsa_keys,
    generate_aes_key,
    encrypt_file,
    encrypt_aes_key,
    decrypt_aes_key,
    decrypt_file,
    verify_files,
)

# ── Paths ────────────────────────────────────────
BASE_DIR          = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR          = os.path.join(BASE_DIR, "keys")
OUTPUT_DIR        = os.path.join(BASE_DIR, "output")
PRIVATE_KEY       = os.path.join(KEYS_DIR, "private.pem")
PUBLIC_KEY        = os.path.join(KEYS_DIR, "public.pem")
ENCRYPTED_FILE    = os.path.join(OUTPUT_DIR, "students_encrypted.bin")
ENCRYPTED_AES_KEY = os.path.join(OUTPUT_DIR, "aes_key_encrypted.bin")
DECRYPTED_FILE    = os.path.join(OUTPUT_DIR, "students_decrypted.csv")

os.makedirs(KEYS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ════════════════════════════════════════════════
#  Main Application
# ════════════════════════════════════════════════
class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Lib Lab — Hybrid Encryption")
        self.root.geometry("780x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.input_file = tk.StringVar()
        self._build_ui()

    # ── UI Builder ───────────────────────────────
    def _build_ui(self):
        # Title
        tk.Label(
            self.root, text="Cryptography Lib Lab",
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2e", fg="#cba6f7"
        ).pack(pady=(18, 2))

        tk.Label(
            self.root, text="Hybrid Encryption  •  AES-256-CBC  +  RSA-2048",
            font=("Helvetica", 10),
            bg="#1e1e2e", fg="#a6adc8"
        ).pack(pady=(0, 14))

        # File selector
        frame_file = tk.Frame(self.root, bg="#1e1e2e")
        frame_file.pack(fill="x", padx=30)

        tk.Label(frame_file, text="Input File:", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Helvetica", 10)).pack(side="left")

        tk.Entry(frame_file, textvariable=self.input_file, width=48,
                 bg="#313244", fg="#cdd6f4", insertbackground="white",
                 relief="flat", font=("Courier", 10)).pack(side="left", padx=8)

        tk.Button(frame_file, text="Browse", command=self._browse,
                  bg="#89b4fa", fg="#1e1e2e", font=("Helvetica", 9, "bold"),
                  relief="flat", padx=8).pack(side="left")

        # Action buttons
        frame_btns = tk.Frame(self.root, bg="#1e1e2e")
        frame_btns.pack(pady=14)

        btn_style = {"font": ("Helvetica", 11, "bold"), "relief": "flat",
                     "padx": 18, "pady": 8, "cursor": "hand2"}

        tk.Button(frame_btns, text="🔑  Generate RSA Keys",
                  bg="#a6e3a1", fg="#1e1e2e",
                  command=self._generate_keys, **btn_style).grid(row=0, column=0, padx=8)

        tk.Button(frame_btns, text="🔒  Encrypt",
                  bg="#f38ba8", fg="#1e1e2e",
                  command=self._encrypt, **btn_style).grid(row=0, column=1, padx=8)

        tk.Button(frame_btns, text="🔓  Decrypt & Verify",
                  bg="#89dceb", fg="#1e1e2e",
                  command=self._decrypt, **btn_style).grid(row=0, column=2, padx=8)

        # Base64 preview label
        tk.Label(self.root, text="📋 Encrypted Output Preview (Base64)",
                 bg="#1e1e2e", fg="#f9e2af",
                 font=("Helvetica", 10, "bold")).pack(anchor="w", padx=30, pady=(6, 2))

        self.base64_box = scrolledtext.ScrolledText(
            self.root, height=5, width=88,
            bg="#181825", fg="#a6e3a1",
            font=("Courier", 9), relief="flat",
            state="disabled"
        )
        self.base64_box.pack(padx=30, pady=(0, 10))

        # Log output
        tk.Label(self.root, text="📟 Log",
                 bg="#1e1e2e", fg="#f9e2af",
                 font=("Helvetica", 10, "bold")).pack(anchor="w", padx=30)

        self.log_box = scrolledtext.ScrolledText(
            self.root, height=10, width=88,
            bg="#181825", fg="#cdd6f4",
            font=("Courier", 9), relief="flat",
            state="disabled"
        )
        self.log_box.pack(padx=30, pady=(2, 14))

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self.root, textvariable=self.status_var,
                 bg="#313244", fg="#a6adc8",
                 font=("Helvetica", 9), anchor="w"
                 ).pack(fill="x", side="bottom", ipady=4, padx=0)

    # ── Helpers ──────────────────────────────────
    def _browse(self):
        path = filedialog.askopenfilename(
            filetypes=[("All files", "*.*"), ("CSV", "*.csv"),
                       ("Text", "*.txt"), ("JSON", "*.json")])
        if path:
            self.input_file.set(path)

    def _log(self, msg, color="#cdd6f4"):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_base64(self, text):
        self.base64_box.configure(state="normal")
        self.base64_box.delete("1.0", "end")
        self.base64_box.insert("end", text)
        self.base64_box.configure(state="disabled")

    def _status(self, msg):
        self.status_var.set(msg)

    # ── Actions ──────────────────────────────────
    def _generate_keys(self):
        def task():
            self._log("\n── Generating RSA-2048 Key Pair ──")
            self._status("Generating RSA keys...")
            try:
                generate_rsa_keys(PRIVATE_KEY, PUBLIC_KEY)
                self._log("[+] Private key saved → keys/private.pem", "#a6e3a1")
                self._log("[+] Public  key saved → keys/public.pem",  "#a6e3a1")
                self._status("✅ RSA keys generated.")
                messagebox.showinfo("Done", "RSA key pair generated successfully!")
            except Exception as e:
                self._log(f"[!] Error: {e}", "#f38ba8")
                self._status("❌ Key generation failed.")
        threading.Thread(target=task, daemon=True).start()

    def _encrypt(self):
        path = self.input_file.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showwarning("No file", "Please select a valid input file first.")
            return
        if not os.path.exists(PUBLIC_KEY):
            messagebox.showwarning("No Keys", "Generate RSA keys first!")
            return

        def task():
            self._log("\n── Encrypting ──────────────────────")
            self._status("Encrypting...")
            try:
                aes_key = generate_aes_key()
                self._log(f"[+] AES-256 key generated: {aes_key.hex()[:32]}...", "#cba6f7")

                encrypt_file(path, ENCRYPTED_FILE, aes_key)
                self._log(f"[+] File encrypted → output/students_encrypted.bin", "#a6e3a1")

                encrypt_aes_key(aes_key, PUBLIC_KEY, ENCRYPTED_AES_KEY)
                self._log(f"[+] AES key encrypted with RSA → output/aes_key_encrypted.bin", "#a6e3a1")

                # Base64 preview
                with open(ENCRYPTED_FILE, "rb") as f:
                    raw = f.read()
                b64 = base64.b64encode(raw).decode()
                self._set_base64(b64[:800] + "\n...(truncated)")
                self._log(f"[+] Base64 preview generated ({len(b64)} chars total)", "#f9e2af")

                self._status("✅ Encryption complete.")
            except Exception as e:
                self._log(f"[!] Error: {e}", "#f38ba8")
                self._status("❌ Encryption failed.")
        threading.Thread(target=task, daemon=True).start()

    def _decrypt(self):
        if not os.path.exists(ENCRYPTED_FILE):
            messagebox.showwarning("No Data", "Encrypt a file first!")
            return
        if not os.path.exists(PRIVATE_KEY):
            messagebox.showwarning("No Keys", "Generate RSA keys first!")
            return

        def task():
            self._log("\n── Decrypting & Verifying ──────────")
            self._status("Decrypting...")
            try:
                aes_key = decrypt_aes_key(ENCRYPTED_AES_KEY, PRIVATE_KEY)
                self._log("[+] AES key recovered via RSA private key.", "#cba6f7")

                decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, aes_key)
                self._log(f"[+] File decrypted → output/students_decrypted.csv", "#a6e3a1")

                match = verify_files(self.input_file.get() or DECRYPTED_FILE, DECRYPTED_FILE)
                if match:
                    self._log("✅ SHA-256 MATCH — Decrypted file = Original!", "#a6e3a1")
                    self._status("✅ Decryption & verification successful!")
                    messagebox.showinfo("Success", "Decryption successful!\nSHA-256 verified ✅")
                else:
                    self._log("❌ SHA-256 MISMATCH!", "#f38ba8")
                    self._status("❌ Verification failed.")
            except Exception as e:
                self._log(f"[!] Error: {e}", "#f38ba8")
                self._status("❌ Decryption failed.")
        threading.Thread(target=task, daemon=True).start()


# ── Entry Point ──────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
