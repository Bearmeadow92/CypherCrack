# --- CipherCrack GUI (Refined Style) ---
from customtkinter import CTkLabel, CTkFrame, CTkButton, CTkEntry, CTkOptionMenu, CTkTextbox, CTkImage
import tkinter as tk
from PIL import Image
import customtkinter as ctk
import time
from ciphercrack_logic import CipherCrackController  # new import

class CipherCrackGUI:
    def __init__(self, master):
        self.master = master
        self.controller = CipherCrackController(self)

        self._setup_window()
        self._load_images()
        self._create_widgets()
        self._arrange_widgets()
        self.update_fields(self.controller.get_current_cipher())

    def _setup_window(self):
        self.master.title("CipherCrack")
        self.master.geometry("880x720")
        self.master.minsize(880, 720)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.master.configure(bg="#1e1e2f")

    def _load_images(self):
        try:
            sun = Image.open("icons8-sun-24.png").resize((24, 24))
            moon = Image.open("icons8-moon-symbol-24.png").resize((24, 24))
            self.sun_icon = CTkImage(light_image=sun, dark_image=sun)
            self.moon_icon = CTkImage(light_image=moon, dark_image=moon)
        except FileNotFoundError:
            self.sun_icon = self.moon_icon = None

    def _create_widgets(self):
        self.top_bar = CTkFrame(self.master, height=60, fg_color="#262636")
        self.theme_button = CTkButton(
            self.top_bar,
            image=self.sun_icon,
            text="",
            width=40,
            height=40,
            command=self._toggle_theme_with_effect,
            fg_color="#333",
            hover_color="#555"
        )

        self.sidebar = CTkFrame(self.master, width=220, corner_radius=10, fg_color="#2d2d3a")
        self.title_label = CTkLabel(self.sidebar, text="🧬 CipherCrack", font=("Segoe UI", 24, "bold"), text_color="#eeeeee")
        self.cipher_label = CTkLabel(self.sidebar, text="Choose Cipher:", font=("Segoe UI", 13), text_color="#aaaaaa")
        self.cipher_var = tk.StringVar(value=self.controller.current_cipher_name)
        self.cipher_menu = CTkOptionMenu(
            self.sidebar,
            variable=self.cipher_var,
            values=list(self.controller.ciphers.keys()),
            command=self.controller.set_cipher,
            width=180
        )
        self.detect_button = CTkButton(self.sidebar, text="Smart Detect 🔍", command=self.controller.detect_cipher_action, width=180)

        self.main_frame = CTkFrame(self.master, corner_radius=10, fg_color="#1e1e2f")
        self.input_textbox = CTkTextbox(self.main_frame, height=120, width=620, font=("Consolas", 13), fg_color="#23232e", text_color="#eaeaea", border_color="#444", border_width=1)
        self.shift_entry = CTkEntry(self.main_frame, placeholder_text="Shift (Caesar)", font=("Segoe UI", 12), width=300)
        self.key_entry = CTkEntry(self.main_frame, placeholder_text="Key (Vigenère/XOR)", font=("Segoe UI", 12), width=300)

        self.button_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.encrypt_button = CTkButton(self.button_frame, text="Encrypt", command=self.controller.encrypt_action, width=130)
        self.decrypt_button = CTkButton(self.button_frame, text="Decrypt", command=self.controller.decrypt_action, width=130)

        self.output_textbox = CTkTextbox(self.main_frame, height=180, width=620, font=("Consolas", 13), fg_color="#23232e", text_color="#d9d9d9", border_color="#444", border_width=1)

        self.bottom_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.copy_button = CTkButton(self.bottom_frame, text="📋 Copy", command=self.controller.copy_output)
        self.clear_input_button = CTkButton(self.bottom_frame, text="Clear Input", command=self.controller.clear_input)
        self.clear_output_button = CTkButton(self.bottom_frame, text="Clear Output", command=self.controller.clear_output)

    def _arrange_widgets(self):
        self.top_bar.pack(fill="x", side="top")
        self.theme_button.pack(side="right", padx=10, pady=10)

        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.title_label.pack(pady=(20, 15))
        self.cipher_label.pack(pady=(10, 2))
        self.cipher_menu.pack(pady=5)
        self.detect_button.pack(pady=(20, 10))

        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.input_textbox.pack(pady=(10, 10))
        self.shift_entry.pack(pady=4)
        self.key_entry.pack(pady=4)
        self.button_frame.pack(pady=10)
        self.encrypt_button.grid(row=0, column=0, padx=10)
        self.decrypt_button.grid(row=0, column=1, padx=10)
        self.output_textbox.pack(pady=(10, 10))

        self.bottom_frame.pack(pady=10)
        self.copy_button.grid(row=0, column=0, padx=8)
        self.clear_input_button.grid(row=0, column=1, padx=8)
        self.clear_output_button.grid(row=0, column=2, padx=8)

    def _toggle_theme_with_effect(self):
        current = ctk.get_appearance_mode()
        new_theme = "light" if current == "Dark" else "dark"
        for _ in range(5):
            self.master.update_idletasks()
            self.master.update()
            time.sleep(0.02)
        ctk.set_appearance_mode(new_theme)
        self.theme_button.configure(image=self.moon_icon if new_theme == "light" else self.sun_icon)

    def update_fields(self, cipher):
        self.shift_entry.pack_forget()
        self.key_entry.pack_forget()
        if cipher.requires_shift():
            self.shift_entry.pack(pady=5)
        if cipher.requires_key():
            self.key_entry.pack(pady=5)

    def get_input_text(self):
        return self.input_textbox.get("1.0", "end").strip()

    def get_shift(self):
        try:
            return int(self.shift_entry.get() or 3)
        except ValueError:
            return 3

    def get_key(self):
        return self.key_entry.get()

    def set_output_text(self, text):
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("end", text)

    def copy_output_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.output_textbox.get("1.0", "end"))

    def clear_input_text(self):
        self.input_textbox.delete("1.0", "end")

    def clear_output_text(self):
        self.output_textbox.delete("1.0", "end")


# --- Entry Point ---
if __name__ == "__main__":
    root = ctk.CTk()
    gui = CipherCrackGUI(root)
    root.mainloop()
