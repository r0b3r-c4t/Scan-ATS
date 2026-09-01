from fastapi import FastAPI

from app.routes.candidates import router as candidates_router


app = FastAPI(
    title="Scan ATS",
    description="AI-powered Applicant Tracking System",
    version="0.1.0"
)


app.include_router(candidates_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "scan-ats-api"
    }