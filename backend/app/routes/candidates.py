from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.file_service import save_file
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
async def upload_resume(
    file: UploadFile = File(...)
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    file_data = await file.read()

    file_id = save_file(
        file_data=file_data,
        filename=file.filename,
        content_type=file.content_type
    )

    resume_data = {
        "file_id": str(file_id),
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(file_data)
    }

    candidate_id = create_candidate(resume_data)

    return {
        "message": "Resume uploaded successfully",

        "candidate_id": str(candidate_id),

        "resume": resume_data,

        "processing": {
            "status": "uploaded"
        }
    }