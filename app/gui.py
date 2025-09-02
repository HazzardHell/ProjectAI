import tkinter as tk
from tkinter import filedialog, messagebox
from app.ai import AICompanion


class CompanionGUI:
    def __init__(self, root):
        self.companion = AICompanion()
        self.root = root
        self.root.title("PC Companion AI")

        # Área de texto
        self.text_area = tk.Text(root, wrap="word", height=20, width=60)
        self.text_area.pack(padx=10, pady=10)

        # Entrada do usuário
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(side=tk.LEFT, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Botão de enviar
        self.send_button = tk.Button(
            root, text="Enviar", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Botão de carregar PDF
        self.load_button = tk.Button(
            root, text="Carregar PDF", command=self.load_document)
        self.load_button.pack(side=tk.LEFT, padx=5)

    def send_message(self, event=None):
        user_text = self.entry.get()
        if not user_text.strip():
            return
        self.text_area.insert(tk.END, f"Você: {user_text}\n")

        # Se tiver documento carregado → responde com base nele
        if self.companion.docs.db:
            resposta = self.companion.ask_about_document(user_text)
        else:
            resposta = self.companion.ask_ollama(user_text)

        self.text_area.insert(tk.END, f"IA: {resposta}\n\n")
        self.entry.delete(0, tk.END)

    def load_document(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if filepath:
            self.companion.docs.load_pdf(filepath)
            messagebox.showinfo(
                "Documento", f"📄 Documento carregado:\n{filepath}")
            self.text_area.insert(
                tk.END, f"[INFO] Documento carregado: {filepath}\n\n")
