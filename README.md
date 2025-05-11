🧬 CipherCrack
CipherCrack is a sleek, modern GUI tool for encrypting, decrypting, and detecting classic ciphers — designed with new technologists in mind. Featuring a beautiful dark mode, smart detection logic powered by NLTK, and a clean interface built with CustomTkinter.

🚀 Features
🔐 Encrypt and decrypt using:

Caesar Cipher

Vigenère Cipher

XOR Cipher

ROT13

Base64

🧠 Smart Detect:

Automatically analyzes input to detect likely Caesar or Base64 ciphers

Uses NLTK’s English word corpus to intelligently score Caesar shifts

🌗 Dark/Light Mode toggle with animated theme switching

🎨 Clean and responsive GUI built with CustomTkinter

🧪 Built for beginner cryptographers and tinkerers

📦 Setup
bash
Copy
Edit
pip install customtkinter pillow nltk
Then run Python and download the word list for smart detection:

python
Copy
Edit
import nltk
nltk.download('words')
▶️ Usage
From your terminal:

bash
Copy
Edit
python ciphercrack_gui.py
Ensure these files are in the same folder:

ciphercrack_gui.py

ciphercrack_logic.py

icons8-sun-24.png

icons8-moon-symbol-24.png

💡 Future Ideas
Add frequency analysis for substitution ciphers

Plug in hash detection (e.g. MD5, SHA256 checksums)

Visual bar for smart detection confidence

Sound FX on button click (totally optional 🔊)

🛠️ Built With
Python 3

CustomTkinter

NLTK

Love for learning encryption the fun way

📜 License
MIT — feel free to use, fork, and remix.

Made with ❤️ by Jesse Fletcher

Want a copy saved as a GitHub Gist or zipped into a starter repo package? I can prep that too.
