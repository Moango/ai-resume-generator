import logging
from typing import Dict, List
from .project_analysis_service import analyze_project
from .extract_service import extract_project_info

logger = logging.getLogger(__name__)

async def enhance_project_descriptions(personal_info: str) -> Dict:
    """增强项目描述的完整流程"""
    try:
        # 1. 提取项目信息
        incomplete_projects = await extract_project_info(personal_info)
        
        # 2. 对每个不完整的项目进行分析
        enhanced_projects = []
        for project in incomplete_projects:
            # 生成项目分析和确认问题
            project_details = await analyze_project(
                project["name"], 
                project["domain"]
            )
            
            enhanced_projects.append({
                "project": project,
                "analysis": project_details["analysis"],
                "questions": project_details["questions"],
                "missing_aspects": project["missing_aspects"]
            })
        
        return {
            "original_info": personal_info,
            "enhanced_projects": enhanced_projects
        }
        
    except Exception as e:
        logger.error(f"Error enhancing project descriptions: {str(e)}")
        raise ValueError(f"项目描述增强失败: {str(e)}") 