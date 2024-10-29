import json
import logging
from typing import Dict, List
from app.core.openai_client import OpenAIClient

logger = logging.getLogger(__name__)
client = OpenAIClient.get_client()

PROJECT_ANALYSIS_PROMPT = """作为一位资深技术专家，请根据项目名称和领域，生成详细的项目分析，返回JSON格式：
{
    "business_scenario": {
        "background": "项目背景和业务痛点",
        "target_users": "目标用户和核心需求",
        "scale": "项目规模和影响范围",
        "constraints": "可能的业务约束"
    },
    "tech_solution": {
        "tech_stack": "核心技术栈选型",
        "architecture": "系统架构设计",
        "modules": "关键模块划分",
        "data_flow": "数据流设计"
    },
    "challenges": {
        "performance": "性能挑战",
        "stability": "稳定性问题",
        "scalability": "扩展性考虑",
        "security": "安全性要求"
    },
    "business_value": {
        "efficiency": "效率提升指标",
        "cost": "成本节省指标",
        "quality": "质量改进指标",
        "experience": "用户体验提升"
    },
    "team_role": {
        "composition": "团队组成建议",
        "responsibilities": "关键角色职责",
        "collaboration": "协作流程设计",
        "management": "项目管理方式"
    }
}

请基于项目名称和领域，生成合理的分析内容。确保所有字段都有具体的描述。"""

async def analyze_project(project_name: str, domain: str) -> Dict:
    """分析项目并生成建议场景"""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROJECT_ANALYSIS_PROMPT},
                {"role": "user", "content": f"项目名称：{project_name}\n领域：{domain}"},
            ],
            temperature=0.7,
            max_tokens=2048,
            response_format={"type": "json_object"}
        )
        
        project_analysis = json.loads(completion.choices[0].message.content)
        
        # 生成确认问题
        questions = generate_confirmation_questions(project_analysis)
        
        return {
            "analysis": project_analysis,
            "questions": questions
        }
        
    except Exception as e:
        logger.error(f"Error analyzing project: {str(e)}")
        raise ValueError(f"项目分析失败: {str(e)}")

def generate_confirmation_questions(analysis: Dict) -> List[Dict]:
    """根据分析结果生成确认问题"""
    return [
        {
            "type": "业务场景",
            "current": analysis["business_scenario"]["background"],
            "confirm": "这是否符合您的项目实际情况？",
            "details": "请补充具体的业务背景和目标："
        },
        {
            "type": "技术方案",
            "current": analysis["tech_solution"]["tech_stack"],
            "confirm": "您使用了这些技术栈吗？",
            "details": "请说明实际使用的核心技术："
        },
        {
            "type": "技术难点",
            "current": analysis["challenges"]["performance"],
            "confirm": "您是否遇到了类似的技术难点？",
            "details": "请描述您解决的关键技术问题："
        },
        {
            "type": "业务价值",
            "current": analysis["business_value"]["efficiency"],
            "confirm": "这些价值指标是否准确？",
            "details": "请提供实际的业务改进数据："
        },
        {
            "type": "团队角色",
            "current": analysis["team_role"]["responsibilities"],
            "confirm": "这是否符合您在项目中的角色？",
            "details": "请说明您的具体职责和贡献："
        }
    ] 