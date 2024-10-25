from pydantic import BaseModel, Field
from typing import Literal

class ResumeInput(BaseModel):
    personal_info: str
    job_description: str
    position_name: str = Field(description="目标职位名称")

class ResumeOutput(BaseModel):
    resume: str

class ResumeModificationInput(BaseModel):
    current_resume: str
    section: Literal["summary", "skills", "experience", "education", "contact"] = Field(
        description="要修改的简历部分"
    )
    modification_request: str = Field(
        description="修改要求"
    )






