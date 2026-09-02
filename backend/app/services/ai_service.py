import json
import time
from typing import Any

from ollama import Client



class AIService:

    def __init__(self):
        self.model = "scan-ats-qwen3-vl-instruct:4b"
        self.client = Client(host="http://127.0.0.1:11434")

    def analyze_resume(
        self,
        content: str | list[bytes],
        content_type: str
    ) -> dict[str, Any]:

        if content_type == "text":
            message = {
                "role": "user",
                "content": self._build_prompt() + "\n\nCV:\n" + content
            }

        else:
            message = {
                "role": "user",
                "content": self._build_prompt(),
                "images": content
            }

        start = time.perf_counter()

        response = self.client.chat(
            model=self.model,
            messages=[message],
            format="json",
            options={
                "num_predict": 3000,
                "temperature": 0,
                "num_ctx": 8192,
            },
        )

        ollama_time = time.perf_counter() - start

        print("=== RAW OLLAMA RESPONSE ===")
        print(response)

        print("CONTENT:")
        print(repr(response.message.content))

        print("THINKING:")
        print(repr(response.message.thinking))

        prompt_token_count = response.prompt_eval_count or 0
        output_token_count = response.eval_count or 0
        prompt_eval_duration = response.prompt_eval_duration or 0
        eval_duration = response.eval_duration or 0

        print("\n=== OLLAMA METRICS ===")

        print(f"Total Ollama:       {ollama_time:.3f}s")
        print(f"Prompt tokens:      {prompt_token_count}")
        print(f"Output tokens:      {output_token_count}")
        print(f"Total tokens:       {prompt_token_count + output_token_count}")

        print(
            f"Prompt eval time:   "
            f"{prompt_eval_duration / 1_000_000_000:.3f}s"
        )

        print(
            f"Generation time:    "
            f"{eval_duration / 1_000_000_000:.3f}s"
        )

        print("======================\n")

        if not response.message.content:
            raise RuntimeError(
                "Ollama returned no final content."
            )

        try:
            data = json.loads(response.message.content)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"Invalid JSON returned by Ollama: {e}"
            )

        if not isinstance(data, dict):
            raise RuntimeError(
                "Ollama returned JSON that is not an object."
            )

        return data

        ollama_time = time.perf_counter() - start

        print("=== RAW OLLAMA RESPONSE ===")
        print(response)

        print("CONTENT:")
        print(repr(response.message.content))

        print("THINKING:")
        print(repr(response.message.thinking))

        prompt_token_count = response.prompt_eval_count or 0
        output_token_count = response.eval_count or 0
        prompt_eval_duration = response.prompt_eval_duration or 0
        eval_duration = response.eval_duration or 0

        print("\n=== OLLAMA METRICS ===")

        print(f"Total Ollama:       {ollama_time:.3f}s")

        print(
            f"Prompt tokens:      "
            f"{prompt_token_count}"
        )

        print(
            f"Output tokens:      "
            f"{output_token_count}"
        )

        print(
            f"Total tokens:       "
            f"{prompt_token_count + output_token_count}"
        )

        print(
            f"Prompt eval time:   "
            f"{prompt_eval_duration / 1_000_000_000:.3f}s"
        )

        print(
            f"Generation time:    "
            f"{eval_duration / 1_000_000_000:.3f}s"
        )

        print("======================\n")

        if not response.message.content:
            raise RuntimeError(
                "Ollama returned no final content."
            )

        try:
            data = json.loads(response.message.content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON returned by Ollama: {e}")
        
        if not isinstance(data, dict):
            raise RuntimeError("Ollama returned JSON that is not an object.")

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
