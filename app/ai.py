import requests
from app.documents import DocumentAssistant


class AICompanion:
    def __init__(self, model="mistral"):
        self.model = model
        self.docs = DocumentAssistant(model=model)

    def ask_ollama(self, prompt):
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]

    def ask_about_document(self, question):
        context = self.docs.query(question)
        prompt = f"Baseado no seguinte texto:\n{context}\n\nResponda à pergunta: {question}"
        return self.ask_ollama(prompt)
