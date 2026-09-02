from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.candidates import router as candidates_router
from app.routes.jobs import router as jobs_router


app = FastAPI(
    title="Scan ATS",
    description="AI-powered Applicant Tracking System",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates_router)
app.include_router(jobs_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "scan-ats-api"
    }
