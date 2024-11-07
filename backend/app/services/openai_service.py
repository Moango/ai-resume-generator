from app.core.openai_client import OpenAIClient
import json
import logging
import asyncio
from app.templates.resume.system_prompts import (
    INTERVIEWER_REVIEW_PROMPT,
    JD_ANALYSIS_PROMPT,
    PERSONAL_INFO_ANALYSIS_PROMPT,
    SECTION_GENERATION_PROMPTS,
    RESUME_MODIFICATION_PROMPT,
)
from app.templates.resume.section_templates import RESUME_STRUCTURE
from app.templates.resume.section_requirements import SECTION_REQUIREMENTS

logger = logging.getLogger(__name__)

client = OpenAIClient.get_client()


async def analyze_job_description(jd: str) -> dict:
    """深入分析职位需求"""
    try:
        prompt = f"""请深入分析这份JD，提取以下信息：
1. 核心技能要求
2. 关键项目经验期望
3. 加分项和隐含要求
4. 招聘方真正看重的能力
5. 区分必要条件和优先条件

JD内容：{jd}
"""
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": JD_ANALYSIS_PROMPT},
                {"role": "user", "content": prompt},
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


async def analyze_personal_info(info: str) -> dict:
    """分析个人信息并挖掘潜力"""
    try:
        prompt = f"""请分析这份个人信息，并进行合理延伸：
1. 已具备的核心能力
2. 可以合理延伸的相关经验
3. 潜在的技术能力和项目经验
4. 可以突出的竞争优势
5. 需要重点包装的方向

个人信息：{info}
"""
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PERSONAL_INFO_ANALYSIS_PROMPT},
                {"role": "user", "content": prompt},
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

        prompt = f"""
                    基于以下背景生成{section}部分：
                    {json.dumps(context, ensure_ascii=False, indent=2)}

                    {SECTION_REQUIREMENTS.get(section, '')}

                    特别注意：
                    1. 内容必须真实可信
                    2. 避免模板化表述
                    3. 突出个人特色
                    4. 与职位高度相关
                """

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


async def generate_resume(
    personal_info: str, job_description: str, position_name: str
) -> str:
    """分步骤生成简历"""
    try:
        # 并行执行分析任务
        jd_analysis, personal_analysis = await asyncio.gather(
            analyze_job_description(job_description),
            analyze_personal_info(personal_info),
        )
        logger.info("Analysis completed")

        # 在context中添加职位名
        context = {
            "position_name": position_name,
            "jd": jd_analysis,
            "personal": personal_analysis,
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
                for section in ["summary", "skills", "work_history", "experience"]
            ]
        )
        logger.info("All sections generated")

        # 组装简历时添加work_history
        resume_md = RESUME_STRUCTURE.format(
            name=personal_analysis["basic"]["name"],
            position_name=position_name,
            contact=contact,
            summary=sections[0],
            skills=sections[1],
            work_history=sections[2],
            work_experience=sections[3],
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


async def review_section(section_name: str, content: str) -> str:
    """从面试官视角审查简历内容"""
    try:
        prompt = f"""请审查以下简历{section_name}部分的内容：

{content}

请从面试官视角给出详细的审查意见。"""

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": INTERVIEWER_REVIEW_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error reviewing {section_name}: {str(e)}")
        raise ValueError(f"审查{section_name}失败: {str(e)}")


async def review_and_improve_section(
    section_name: str, content: str, jd_analysis: dict, personal_analysis: dict
) -> dict:
    """从面试官视角审查简历内容并生成改进版本"""
    try:
        # 1. 先获取面试官的审查意见
        review_prompt = f"""请审查以下简历{section_name}部分的内容：

{content}

请从面试官视角给出详细的审查意见。"""

        review_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": INTERVIEWER_REVIEW_PROMPT},
                {"role": "user", "content": review_prompt},
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        review_feedback = review_completion.choices[0].message.content.strip()

        # 2. 基于审查意见生成改进版本
        improve_prompt = f"""基于以下面试官的审查意见，改进简历内容：

原始内容：
{content}

面试官审查意见：
{review_feedback}

请生成改进后的内容，要求：
1. 解决审查意见中指出的所有问题
2. 保持原有的优点
3. 确保所有数据和描述真实可信
4. 加强技术深度和业务价值的展示
5. 提供更具体的项目和技术细节
6. 使用更专业的描述方式

背景信息：
{json.dumps({"jd": jd_analysis, "personal": personal_analysis}, ensure_ascii=False, indent=2)}
"""

        improve_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SECTION_GENERATION_PROMPTS[section_name]},
                {"role": "user", "content": improve_prompt},
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        improved_content = improve_completion.choices[0].message.content.strip()

        return {
            "original": content,
            "review": review_feedback,
            "improved": improved_content,
        }

    except Exception as e:
        logger.error(f"Error reviewing and improving {section_name}: {str(e)}")
        raise ValueError(f"审查并改进{section_name}失败: {str(e)}")
