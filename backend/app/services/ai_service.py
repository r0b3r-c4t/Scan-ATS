from ollama import chat


class AIService:

    def __init__(self):
        self.model = "qwen3-vl:4b"

    def analyze_resume(
        self,
        images: list[bytes]
    ) -> str:

        response = chat(
    model=self.model,
    messages=[
        {
            "role": "user",
            "content": self._build_prompt(),
            "images": images
        }
    ],
    options={
        "num_predict": 500
    }
)

        print("=== RAW OLLAMA RESPONSE ===")
        print(response)
        print("============================")

        print("MESSAGE:")
        print(response.message)

        print("CONTENT:")
        print(repr(response.message.content))

        return response.message.content

    @staticmethod
    def _build_prompt() -> str:
        return """
Analyze this resume for an Applicant Tracking System.

Extract the information visible in all pages.

Return ONLY valid JSON.
Do not provide explanations.
Do not provide reasoning.
Do not describe your analysis.

Use exactly this structure:

{
    "name": null,
    "email": null,
    "phone": null,
    "location": null,
    "summary": null,
    "skills": [],
    "experience": [],
    "education": [],
    "certifications": []
}

Rules:
- Extract only information actually present in the resume.
- Never invent information.
- Use null when a single-value field is missing.
- Use [] when a list has no information.
- Combine information from all pages.
- Keep the original wording where practical.
- Return JSON only.
"""