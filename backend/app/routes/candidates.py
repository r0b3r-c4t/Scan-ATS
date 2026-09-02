from bson import ObjectId
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.services.ai_service import AIService
from app.services.candidate_service import create_candidate
from app.services.document_service import DocumentService
from app.services.file_service import save_file
from app.services.candidate_evaluation_service import evaluate_candidate
from app.database.mongodb import candidates_collection, grid_fs

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
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    file_data = await file.read()

    if not file_data:
        raise HTTPException(
            status_code=400,
            detail="Empty file"
        )

    file_id = save_file(
        file_data=file_data,
        filename=file.filename,
        content_type=file.content_type
    )

    try:
        images = DocumentService.get_resume_images(str(file_id))
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

    try:
        candidate_data = AIService().analyze_resume(images)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing resume: {str(e)}"
        )

    candidate_data["resume"] = {
        "file_id": str(file_id),
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(file_data)
    }

    try:
        candidate_id = create_candidate(candidate_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving candidate: {str(e)}"
        )

    # EVALUATE CANDIDATE AND UPDATE IN DATABASE
    try:
        candidate_data["candidate_score"] = evaluate_candidate(candidate_data)
        candidates_collection.update_one(
            {"_id": candidate_id},
            {"$set": {"candidate_score": candidate_data["candidate_score"]}}
        )
    except Exception as e:
        print(f"Error evaluating candidate: {str(e)}")
        # Don't fail the upload if evaluation fails
        candidate_data["candidate_score"] = None

    return {
        "message": "Resume processed successfully",
        "candidate_id": str(candidate_id),
        "candidate": candidate_data
    }


@router.get("")
def list_candidates():
    candidates = [
        {
            "id": str(candidate["_id"]),
            "name": candidate.get("name"),
            "candidate_score": candidate.get("candidate_score", {}).get("score"),
            "classification": candidate.get("candidate_score", {}).get("classification"),
        }
        for candidate in candidates_collection.find()
    ]
    return sorted(candidates, key=lambda item: item["candidate_score"] or -1, reverse=True)


@router.get("/{candidate_id}")
def get_candidate(candidate_id: str):
    if not ObjectId.is_valid(candidate_id):
        raise HTTPException(status_code=400, detail="Invalid candidate_id")

    candidate = candidates_collection.find_one({"_id": ObjectId(candidate_id)})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate["_id"] = str(candidate["_id"])
    return candidate


@router.get("/{candidate_id}/resume")
def get_candidate_resume(candidate_id: str):
    """Download the resume file for a candidate"""
    if not ObjectId.is_valid(candidate_id):
        raise HTTPException(status_code=400, detail="Invalid candidate_id")

    candidate = candidates_collection.find_one({"_id": ObjectId(candidate_id)})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    resume_info = candidate.get("resume")
    if not resume_info or not resume_info.get("file_id"):
        raise HTTPException(status_code=404, detail="Resume file not found")

    try:
        file_id = ObjectId(resume_info["file_id"])
        file_obj = grid_fs.get(file_id)
        filename = resume_info.get("filename", "resume.pdf")
        content_type = resume_info.get("content_type", "application/pdf")
        
        return FileResponse(
            file_obj,
            filename=filename,
            media_type=content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving resume: {str(e)}")


@router.get("/{candidate_id}/score")
def get_candidate_score(candidate_id: str):
    if not ObjectId.is_valid(candidate_id):
        raise HTTPException(status_code=400, detail="Invalid candidate_id")

    candidate = candidates_collection.find_one({"_id": ObjectId(candidate_id)})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    evaluation = candidate.get("candidate_score")
    if evaluation is None:
        evaluation = evaluate_candidate(candidate)
        candidates_collection.update_one(
            {"_id": candidate["_id"]},
            {"$set": {"candidate_score": evaluation}}
        )

    return {"candidate_id": str(candidate["_id"]), **evaluation}


@router.post("/{candidate_id}/recalculate-score")
def recalculate_candidate_score(candidate_id: str):
    """Recalculate the score for a specific candidate."""
    if not ObjectId.is_valid(candidate_id):
        raise HTTPException(status_code=400, detail="Invalid candidate_id")

    candidate = candidates_collection.find_one({"_id": ObjectId(candidate_id)})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Recalculate score
    try:
        new_score = evaluate_candidate(candidate)
        candidates_collection.update_one(
            {"_id": candidate["_id"]},
            {"$set": {"candidate_score": new_score}}
        )
        return {
            "message": "Score recalculated successfully",
            "candidate_id": str(candidate["_id"]),
            **new_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recalculating score: {str(e)}")


@router.post("/recalculate-scores")
def recalculate_all_scores():
    """Recalculate scores for all candidates in the database."""
    try:
        candidates = list(candidates_collection.find())
        updated_count = 0
        errors = []

        for candidate in candidates:
            try:
                new_score = evaluate_candidate(candidate)
                candidates_collection.update_one(
                    {"_id": candidate["_id"]},
                    {"$set": {"candidate_score": new_score}}
                )
                updated_count += 1
            except Exception as e:
                errors.append({
                    "candidate_id": str(candidate.get("_id", "unknown")),
                    "error": str(e)
                })

        return {
            "message": f"Recalculated scores for {updated_count} candidate(s)",
            "updated_count": updated_count,
            "total_candidates": len(candidates),
            "errors": errors if errors else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recalculating all scores: {str(e)}")
