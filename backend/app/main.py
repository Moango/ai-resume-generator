from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import resume

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(resume.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Resume Generator API"}
