from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.file_service import save_file
from app.services.document_service import DocumentService
from app.services.ai_service import AIService
from app.services.candidate_service import create_candidate

router = APIRouter(
    prefix="/api/candidates",
    tags=["Candidates"]
)


ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png"
}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # 1. Validate file type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    # 2. Read file
    file_data = await file.read()

    if not file_data:
        raise HTTPException(
            status_code=400,
            detail="Empty file"
        )

    # 3. Save original file in GridFS
    file_id = save_file(
        file_data=file_data,
        filename=file.filename,
        content_type=file.content_type
    )

    # 4. Convert document to images
    try:
        images = DocumentService.get_resume_images(
            str(file_id)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

    if not images:
        raise HTTPException(
            status_code=400,
            detail="Could not extract pages from document"
        )

    # 5. Analyze resume with AI
    try:
        ai_service = AIService()

        candidate_data = ai_service.analyze_resume(
            images
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing resume: {str(e)}"
        )

    # 6. Add resume metadata
    candidate_data["resume"] = {
        "file_id": str(file_id),
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(file_data)
    }

    # 7. Save candidate
    try:
        candidate_id = create_candidate(
            candidate_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving candidate: {str(e)}"
        )

    # 8. Response
    return {
        "message": "Resume processed successfully",
        "candidate_id": str(candidate_id),
        "candidate": candidate_data
    }