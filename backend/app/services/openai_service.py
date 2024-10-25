from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import logging
import asyncio
from app.templates.resume.system_prompts import (
    JD_ANALYSIS_PROMPT,
    PERSONAL_INFO_ANALYSIS_PROMPT,
    SECTION_GENERATION_PROMPTS,
    RESUME_MODIFICATION_PROMPT
)
from app.templates.resume.section_templates import RESUME_STRUCTURE  # 修复导入

logger = logging.getLogger(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("BASE_URL"))


async def analyze_job_description(job_description: str) -> dict:
    """分析职位描述，提取关键要求"""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": JD_ANALYSIS_PROMPT},
                {"role": "user", "content": job_description},
            ],
            temperature=0.7,
            max_tokens=4096,
            response_format={"type": "json_object"},  # 指定返回JSON格式
        )

        response_content = completion.choices[0].message.content.strip()
        try:
            return json.loads(response_content)
        except json.JSONDecodeError as je:
            logger.error(f"Invalid JSON response: {response_content}")
            logger.error(f"JSON decode error: {str(je)}")
            raise ValueError("职位分析结果格式错误")

    except Exception as e:
        logger.error(f"Error analyzing job description: {str(e)}")
        raise ValueError(f"职位分析失败: {str(e)}")


async def analyze_personal_info(personal_info: str) -> dict:
    """分析个人信息，提取关键特点"""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PERSONAL_INFO_ANALYSIS_PROMPT},
                {"role": "user", "content": personal_info},
            ],
            temperature=0.7,
            max_tokens=4096,
            response_format={"type": "json_object"},  # 指定返回JSON格式
        )

        response_content = completion.choices[0].message.content.strip()
        try:
            return json.loads(response_content)
        except json.JSONDecodeError as je:
            logger.error(f"Invalid JSON response: {response_content}")
            logger.error(f"JSON decode error: {str(je)}")
            raise ValueError("个人信息分析结果格式错误")

    except Exception as e:
        logger.error(f"Error analyzing personal info: {str(e)}")
        raise ValueError(f"个人信息分析失败: {str(e)}")


async def generate_section(
    section: str, jd_analysis: dict, personal_analysis: dict
) -> str:
    """生成简历特定部分"""
    try:
        context = {"jd": jd_analysis, "personal": personal_analysis}

        section_requirements = {
            "summary": """
要求：
1. 开头点明具体的业务领域和年限
2. 描述2-3个最有说服力的项目成果
3. 说明在特定技术领域的专长和深度
4. 结尾要体现对目标职位的理解和规划

注意：
- 避免使用"精通"、"专家"等主观词
- 性能优化必须有完整上下文
- 突出行业经验和业务理解
- 保持简洁专业，避免套话""",
            "skills": """
要求：
1. 技术栈分类：
   - 后端：框架、中间件、数据库
   - 前端：框架、构建工具、UI库
   - DevOps：容器、CI/CD、监控
   - 云服务：具体平台和产品
   
2. 技能描述：
   - 结合具体项目场景
   - 说明解决的业务问题
   - 提供性能和可用性数据

3. 技能评级：
   - 避免使用主观评
   - 用项目经验说明熟练程度
   - 强调解决复杂问题的能力
   - 突出技术深度和广度""",
            "experience": """
要求：
1. 项目背景：
   - 业务场景和价值
   - 团队规模和角色
   - 项目难点和挑战

2. 技术实现：
   - 架构设计和考虑
   - 核心功能实现
   - 性能优化方案
   - 运维和监控方案

3. 项目成果：
   - 具体的业务指标
   - 完整的性能数据
   - 可量化的改进
   - 团队贡献和影响

注意：
- 所有数据必须有具体场景
- 突出个人贡献和角色
- 体现技术深度和广度
- 强调解决问题的能力""",
        }

        prompt = f"""基于以下背景生成{section}部分：
{json.dumps(context, ensure_ascii=False, indent=2)}

{section_requirements.get(section, '')}

特别注意：
1. 内容必须真实可信
2. 避免模板化表述
3. 突出个人特色
4. 与职位高度相关"""

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SECTION_GENERATION_PROMPTS[section]},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4096,
        )

        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating {section}: {str(e)}")
        raise ValueError(f"生成{section}失败: {str(e)}")


async def generate_resume(personal_info: str, job_description: str, position_name: str) -> str:
    """分步骤生成简历"""
    try:
        # 并行执行分析任务
        jd_analysis, personal_analysis = await asyncio.gather(
            analyze_job_description(job_description),
            analyze_personal_info(personal_info),
        )
        logger.info("Analysis completed")

        # 在context中添加职位名称
        context = {
            "position_name": position_name,
            "jd": jd_analysis,
            "personal": personal_analysis
        }

        # 构建联系方式
        contact = "\n".join(
            [
                f"- 邮箱：{personal_analysis['basic']['email']}",
                f"- 电话：{personal_analysis['basic']['phone']}",
                f"- 地址：{personal_analysis['basic']['location']}",
            ]
        )

        # 并行生成各个部分，移除education
        sections = await asyncio.gather(
            *[
                generate_section(section, jd_analysis, personal_analysis)
                for section in ["summary", "skills", "experience"]
            ]
        )
        logger.info("All sections generated")

        # 组装简历，包含position_name
        resume_md = RESUME_STRUCTURE.format(
            name=personal_analysis["basic"]["name"],
            position_name=position_name,  # 添加职位名称
            contact=contact,
            summary=sections[0],
            skills=sections[1],
            work_experience=sections[2],
        )

        return resume_md

    except Exception as e:
        logger.error(f"Error generating resume: {str(e)}")
        raise ValueError(f"生成简历失败: {str(e)}")


async def modify_resume_section(
    resume_md: str, section: str, modification_request: str
) -> str:
    """修改简历特定部分的函数"""
    try:
        prompt = f"""
        请修改以下Markdown格式简历的 {section} 部分：

        当前简历：
        {resume_md}

        用户的修改要求：
        {modification_request}

        请返回完整的修改后的简历，确保：
        1. 只修改 {section} 部分
        2. 保持其他部分完全不变
        3. 修改符合用户的要求
        4. 保持专业的表述方式
        5. 保持Markdown格式
        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": RESUME_MODIFICATION_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4096,
            presence_penalty=0.6,
            frequency_penalty=0.3,
        )

        modified_resume = completion.choices[0].message.content.strip()
        return modified_resume

    except Exception as e:
        logger.error(f"Error modifying resume: {str(e)}")
        raise ValueError(f"修改简历时发生错误: {str(e)}")
