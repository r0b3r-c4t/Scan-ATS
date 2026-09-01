from app.services.document_service import DocumentService
from app.services.ai_service import AIService


FILE_ID = "6a965828f84f93ec99b6c52f"


images = DocumentService.get_resume_images(FILE_ID)

print(f"Sending {len(images)} pages to AI...")

ai_service = AIService()

result = ai_service.analyze_resume(images[:1])

print("\n===== AI RESULT =====\n")
print(result)