from fastapi import APIRouter, HTTPException
from app.models.resume import ResumeInput, ResumeOutput
from app.services.openai_service import generate_resume
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate_resume", response_model=ResumeOutput)
async def create_resume(input: ResumeInput):
    logger.info(f"Received input: {input}")
    try:
        resume = await generate_resume(input.personal_info, input.job_description)
        logger.info(f"Generated resume: {resume}")
        return ResumeOutput(resume=resume)
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the resume")
