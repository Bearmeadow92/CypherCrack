# ciphercrack_logic.py
import base64
import re

try:
    from nltk.corpus import words as nltk_words
    nltk_available = True
    word_set = set(nltk_words.words())
except Exception:
    nltk_available = False
    word_set = set()

# --- Cipher Base Class ---
class Cipher:
    def encrypt(self, text, key=None, shift=0):
        raise NotImplementedError

    def decrypt(self, text, key=None, shift=0):
        raise NotImplementedError

    def requires_key(self): return False
    def requires_shift(self): return False

# --- Cipher Implementations ---
class CaesarCipher(Cipher):
    def encrypt(self, text, shift=3, **kwargs):
        return ''.join(chr((ord(c)-(65 if c.isupper() else 97)+shift)%26+(65 if c.isupper() else 97)) if c.isalpha() else c for c in text)

    def decrypt(self, text, shift=3, **kwargs):
        return ''.join(chr((ord(c)-(65 if c.isupper() else 97)-shift)%26+(65 if c.isupper() else 97)) if c.isalpha() else c for c in text)

    def requires_shift(self): return True

class VigenereCipher(Cipher):
    def encrypt(self, text, key, **kwargs):
        if not key: return text
        key = key.lower()
        return ''.join(chr((ord(c)-(65 if c.isupper() else 97)+ord(key[i%len(key)])-97)%26+(65 if c.isupper() else 97)) if c.isalpha() else c for i,c in enumerate(text))

    def decrypt(self, text, key, **kwargs):
        if not key: return text
        key = key.lower()
        return ''.join(chr((ord(c)-(65 if c.isupper() else 97)-(ord(key[i%len(key)])-97))%26+(65 if c.isupper() else 97)) if c.isalpha() else c for i,c in enumerate(text))

    def requires_key(self): return True

class XORCipher(Cipher):
    def encrypt(self, text, key, **kwargs):
        if not key: return text
        return ''.join(chr(ord(c)^ord(key[i%len(key)])) for i,c in enumerate(text))

    def decrypt(self, text, key, **kwargs):
        return self.encrypt(text, key)

    def requires_key(self): return True

class ROT13Cipher(CaesarCipher):
    def encrypt(self, text, **kwargs): return super().encrypt(text, shift=13)
    def decrypt(self, text, **kwargs): return super().decrypt(text, shift=13)

class Base64Cipher(Cipher):
    def encrypt(self, text, **kwargs): return base64.b64encode(text.encode()).decode()
    def decrypt(self, text, **kwargs): return base64.b64decode(text).decode(errors="ignore")

# --- Cipher Detection ---
class CipherDetector:
    def __init__(self):
        self.word_set = word_set

    def _word_score(self, text):
        return sum(1 for w in re.findall(r"\b[a-zA-Z]{2,}\b", text) if w.lower() in self.word_set) if nltk_available else 0

    def _is_base64(self, s):
        try: return base64.b64encode(base64.b64decode(s)).decode() == s
        except Exception: return False

    def detect(self, text):
        results = []
        if nltk_available:
            caesar = [(s, self._word_score(CaesarCipher().decrypt(text, shift=s)), CaesarCipher().decrypt(text, shift=s)) for s in range(1,26)]
            caesar.sort(key=lambda x:x[1], reverse=True)
            total = sum(score for _,score,_ in caesar)
            if caesar and total > 0:
                for shift, score, result in caesar[:3]:
                    confidence = (score / total) * 100
                    results.append(f"Caesar (shift {shift}) - Confidence: {confidence:.2f}%\n{result}")
        else:
            results.append("Caesar detection requires NLTK.")

        if self._is_base64(text):
            decoded = Base64Cipher().decrypt(text)
            results.append(f"Base64 Decoded:\n{decoded}")

        return "\n\n".join(results) if results else "❌ Could not confidently detect cipher."

# --- Controller ---
class CipherCrackController:
    def __init__(self, gui):
        self.gui = gui
        self.detector = CipherDetector()
        self.ciphers = {
            "Caesar": CaesarCipher(),
            "Vigenère": VigenereCipher(),
            "ROT13": ROT13Cipher(),
            "XOR": XORCipher(),
            "Base64": Base64Cipher()
        }
        self.current_cipher_name = "Caesar"

    def get_current_cipher(self): return self.ciphers[self.current_cipher_name]

    def set_cipher(self, name):
        self.current_cipher_name = name
        self.gui.update_fields(self.get_current_cipher())

    def encrypt_action(self):
        try:
            out = self.get_current_cipher().encrypt(self.gui.get_input_text(), key=self.gui.get_key(), shift=self.gui.get_shift())
        except Exception as e:
            out = f"⚠️ Encryption Error: {e}"
        self.gui.set_output_text(out)

    def decrypt_action(self):
        try:
            out = self.get_current_cipher().decrypt(self.gui.get_input_text(), key=self.gui.get_key(), shift=self.gui.get_shift())
        except Exception as e:
            out = f"⚠️ Decryption Error: {e}"
        self.gui.set_output_text(out)

    def detect_cipher_action(self):
        self.gui.set_output_text(self.detector.detect(self.gui.get_input_text()))

    def copy_output(self): self.gui.copy_output_to_clipboard()
    def clear_input(self): self.gui.clear_input_text()
    def clear_output(self): self.gui.clear_output_text()
    def update_theme_icon(self, theme): pass  # placeholder if GUI wants to use it
