from pydantic import BaseModel

class ResumeInput(BaseModel):
    personal_info: str
    job_description: str

class ResumeOutput(BaseModel):
    resume: str



