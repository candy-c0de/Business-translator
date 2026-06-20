import requests
import json
import re




    
user_input= input("Promt: ")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": <Dein OpenRouter API Key>,
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "openrouter/owl-alpha",
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
    })
    )

zusammenhang = re.search(r'"content"\s*(.*?)\s*"refusal"', response.text)

regex_zusammenhang = zusammenhang.group(0)

gefilterter_text = regex_zusammenhang.replace("<final_summary>", "").replace("refusal", ".").replace('content', "").replace("\\n\n", " ").replace('"', '').replace("\\n", " ").replace(r"\s*\n+\s*", "").replace(":", "").replace('  ', ' ')
    

print(gefilterter_text)