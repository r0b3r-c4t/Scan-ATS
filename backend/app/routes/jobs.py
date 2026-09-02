from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.database.mongodb import candidates_collection, jobs_collection
from app.schemas.job_schema import JobCreateSchema
from app.schemas.matching_schema import MatchResultSchema
from app.services.matching_service import MatchingService

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


def _object_id_or_400(value: str, field_name: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"Invalid {field_name}")
    return ObjectId(value)


def _job_or_404(job_id: str) -> dict:
    job = jobs_collection.find_one({"_id": _object_id_or_400(job_id, "job_id")})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


def _candidate_or_404(candidate_id: str) -> dict:
    candidate = candidates_collection.find_one(
        {"_id": _object_id_or_400(candidate_id, "candidate_id")}
    )
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


def _serialize(document: dict) -> dict:
    document["_id"] = str(document["_id"])
    return document


@router.post("", status_code=201)
def create_job(job: JobCreateSchema):
    job_data = job.model_dump()
    result = jobs_collection.insert_one(job_data)
    job_data["_id"] = str(result.inserted_id)
    return job_data


@router.get("")
def list_jobs():
    return [_serialize(job) for job in jobs_collection.find()]


@router.get("/{job_id}")
def get_job(job_id: str):
    return _serialize(_job_or_404(job_id))


@router.get("/{job_id}/candidates/{candidate_id}/match", response_model=MatchResultSchema)
def match_candidate(job_id: str, candidate_id: str):
    job = _job_or_404(job_id)
    candidate = _candidate_or_404(candidate_id)
    match = MatchingService.calculate_match(candidate, job)
    return {
        "candidate_id": str(candidate["_id"]),
        "job_id": str(job["_id"]),
        **match,
    }


@router.get("/{job_id}/matches")
def rank_candidates(job_id: str):
    job = _job_or_404(job_id)
    matches = []
    for candidate in candidates_collection.find():
        match = MatchingService.calculate_match(candidate, job)
        matches.append({
            "candidate_id": str(candidate["_id"]),
            "candidate_name": candidate.get("name"),
            "match_percentage": match["match_percentage"],
            "classification": match["classification"],
        })
    return sorted(matches, key=lambda item: item["match_percentage"], reverse=True)
