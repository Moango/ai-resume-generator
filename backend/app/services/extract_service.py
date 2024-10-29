from openai import OpenAI
import json
import logging
from typing import List
from app.core.openai_client import OpenAIClient

logger = logging.getLogger(__name__)
client = OpenAIClient.get_client()

PROJECT_EXTRACTION_PROMPT = """从文本中提取项目相关信息，要求：
1. 识别所有提到的项目
2. 分析项目描述的完整度
3. 返回JSON格式：
{
    "projects": [
        {
            "name": "项目名称",
            "domain": "项目领域",
            "description": "项目描述",
            "details_level": 1,  # 详细程度评分(1-5的整数)
            "missing_aspects": ["缺失的关键信息1", "缺失的关键信息2"]
        }
    ]
}

注意：
- details_level必须是1到5的整数
- 当项目描述过于简单时，设置为较低的分数（1-2）
- 当项目描述比较完整时，设置为中等分数（3）
- 当项目描述非常详细时，设置为较高分数（4-5）
"""

async def extract_project_info(personal_info: str) -> List[dict]:
    """从个人信息中提取项目信息"""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROJECT_EXTRACTION_PROMPT},
                {"role": "user", "content": personal_info},
            ],
            temperature=0.7,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        
        response = json.loads(completion.choices[0].message.content)
        projects = response.get("projects", [])
        
        # 确保details_level是整数
        for project in projects:
            project["details_level"] = int(project["details_level"])
        
        # 筛选出描述不足的项目
        incomplete_projects = [
            project for project in projects 
            if project["details_level"] < 4 or project["missing_aspects"]
        ]
        
        return incomplete_projects
        
    except Exception as e:
        logger.error(f"Error extracting project info: {str(e)}")
        raise ValueError(f"项目信息提取失败: {str(e)}") 