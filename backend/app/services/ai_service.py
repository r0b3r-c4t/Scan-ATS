from ollama import Client
import json


class AIService:

    def __init__(self):
        self.model = "scan-ats-qwen3-vl-instruct:4b"
        self.client = Client(host="http://127.0.0.1:11434")

    def analyze_resume(self, images: list[bytes]) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": self._build_prompt(),
                    "images": images
                }
            ],
            format="json",
            options={
                "num_ctx": 8192,
                "num_predict": 3000,
                "temperature": 0
            }
        )

        print("=== RAW OLLAMA RESPONSE ===")
        print(response)

        print("CONTENT:")
        print(repr(response.message.content))

        print("THINKING:")
        print(repr(response.message.thinking))

        if not response.message.content:
            raise RuntimeError(
                "Ollama returned no final content."
            )

        try:
            data = json.loads(response.message.content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON returned by Ollama: {e}")
        
        return data

    def _build_prompt(self) -> str:
        return """
Analiza el CV proporcionado y extrae únicamente la información visible.

Devuelve ÚNICAMENTE un JSON válido con esta estructura:

{
    "name": null,
    "email": null,
    "phone": null,
    "location": null,
    "summary": null,
    "skills": [],
    "experience": [],
    "education": [],
    "certifications": [],
    "projects": []
}

Reglas:

- Extrae únicamente información visible en el CV.
- No inventes información.
- Si un campo individual no aparece, utiliza null.
- Si una lista no contiene información, utiliza [].
- Analiza toda la información disponible.
- Mantén el contenido original cuando sea posible.
- No agregues explicaciones.
- No utilices Markdown.
- La respuesta debe ser únicamente JSON válido.
- Identifica proyectos personales, académicos o profesionales mencionados en el CV.
- No confundas proyectos con experiencia laboral.
"""
