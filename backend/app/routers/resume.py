from fastapi import APIRouter, HTTPException
from app.models.resume import ResumeInput, ResumeOutput, ResumeModificationInput
from app.services.openai_service import generate_resume, modify_resume_section
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate_resume", response_model=ResumeOutput)
async def create_resume(input: ResumeInput):
    logger.info(f"Received input: {input}")
    try:
        # 传入position_name参数
        resume = await generate_resume(
            input.personal_info, 
            input.job_description,
            input.position_name
        )
        return ResumeOutput(resume=resume)
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="生成简历时发生错误")

@router.post("/modify_resume", response_model=ResumeOutput)
async def modify_resume(input: ResumeModificationInput):
    logger.info(f"Received modification request: {input}")
    try:
        modified_resume = await modify_resume_section(
            input.current_resume,
            input.section,
            input.modification_request
        )
        return ResumeOutput(resume=modified_resume)
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="修改简历时发生错误")
