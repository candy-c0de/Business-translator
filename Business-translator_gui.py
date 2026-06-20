import requests
import json
import re
import tkinter as tk
from tkinter import ttk, messagebox

# GUI-Version des Originals: keine neuen Features hinzugefügt
API_KEY = <dein OpenRouter API Key>
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/owl-alpha"


class TranslatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Business Translator")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Deutscher Text:").pack(anchor="w")
        self.input_text = tk.Text(frame, height=10, wrap="word")
        self.input_text.pack(fill="both", expand=False)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=8)

        self.translate_btn = ttk.Button(btn_frame, text="Übersetzen", command=self.translate)
        self.translate_btn.pack(side="left")

        self.clear_btn = ttk.Button(btn_frame, text="Eingabe löschen", command=self.clear_input)
        self.clear_btn.pack(side="left", padx=8)

        ttk.Label(frame, text="Übersetzung (Business-Englisch):").pack(anchor="w")
        self.output_text = tk.Text(frame, height=12, wrap="word")
        self.output_text.pack(fill="both", expand=True)

    def clear_input(self):
        self.input_text.delete("1.0", tk.END)

    def translate(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Leerer Text", "Bitte zuerst Text eingeben.")
            return

        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                        Übersetze den folgenden Text in professionelles Business-Englisch auf C1-Niveau. 

                        Berücksichtige dabei diese Vorgaben:
                        1. Zielgruppe: Mein Chef und meine Kunden. Der Ton muss absolut höflich, respektvoll, professionell und kompetent sein.
                        2. Sprachebene: Nutze typische Business-Redewendungen und vermeide Umgangssprache oder zu wörtliche Übersetzungen.
                        3. Struktur: Der Text soll klar, präzise und leicht verständlich sein,
                           behalte das Format einer geschäftlichen E-Mail bei und halte den text so kurz wie möglich
                        4. Name des kunden ist als [Name_vom_Kunde] gekennstzeichnet und der Name des Users als [dein_Name] gekennstzeichnet

                        Hier ist der deutsche Text:
                        {user_input}
                        """
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            resp = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload), timeout=30)
        except Exception as e:
            messagebox.showerror("Fehler", f"Netzwerkfehler: {e}")
            return

        text = resp.text

        # Verwende die gleiche (einfache) Extraktionslogik wie im Originalscript
        try:
            zusammenhang = re.search(r'"content"\s*(.*?)\s*"refusal"', text)
            if zusammenhang:
                regex_zusammenhang = zusammenhang.group(0)
                gefilterter_text = regex_zusammenhang.replace("<final_summary>", "").replace("refusal", ".").replace('content', "").replace("\\n\\n", " ").replace('"', '').replace("\\n", " ").replace(r"\\s*\\n+\\s*", "").replace(":", "").replace('  ', ' ')
            else:
                # Fallback: zeige die rohe Antwort
                gefilterter_text = text
        except Exception:
            gefilterter_text = text

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, gefilterter_text)


if __name__ == "__main__":
    app = TranslatorGUI()
    app.mainloop()
