from app.services.document_service import DocumentService
from app.services.ai_service import AIService


FILE_ID = "6a9774df215d3e7d3953e0a1"


images = DocumentService.get_resume_images(FILE_ID)

print(f"Pages processed: {len(images)}")

ai_service = AIService()

result = ai_service.analyze_resume(images[:1])

print("\n===== AI RESULT =====\n")

print(result)

print("\n===== NAME =====")
print(result["name"])

print("\n===== EMAIL =====")
print(result["email"])

print("\n===== SKILLS =====")
print(result["skills"])