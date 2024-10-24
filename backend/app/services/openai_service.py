from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import logging

logger = logging.getLogger(__name__)
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

async def generate_resume(personal_info: str, job_description: str) -> str:
    """生成定制简历的函数"""
    
    system_prompt = """你是一位资深的招聘专家和简历顾问，具有丰富的人才评估经验。你需要帮助候选人创建一份突出的简历。
    请使用Markdown格式生成简历内容。

    简历结构要求：
    # 姓名
    
    ## 联系方式
    - 邮箱：xxx
    - 电话：xxx
    - 地址：xxx
    
    ## 个人简介
    [简洁有力的个人介绍，突出核心竞争力和与JD的匹配度]
    
    ## 技能特长
    ### 专业技能
    - 技能1：[详细说明精通程度和实践经验]
    - 技能2：[详细说明精通程度和实践经验]
    
    ### 开发工具
    - 工具1：[使用经验]
    - 工具2：[使用经验]
    
    ## 工作经验
    ### [公司名称] (YYYY.MM - YYYY.MM)
    #### [职位名称]
    
    **项目一：[项目名称]**
    - 业务背景：[项目背景和挑战]
    - 技术方案：[采用的技术栈和架构]
    - 个人职责：[具体负责的工作]
    - 技术难点：[遇到的挑战和解决方案]
    - 项目成果：[具体的数据指标改进]
    
    ## 教育背景
    ### [学校名称] (YYYY.MM - YYYY.MM)
    - 专业：[专业名称]
    - 学位：[学位类型]
    """

    prompt = f"""
    请基于以下信息生成一份专业的Markdown格式简历：

    个人信息：
    {personal_info}

    目标职位JD：
    {job_description}

    要求：
    1. 深入分析JD，提取关键要求：
       - 必备技能和加分项
       - 经验年限和领域要求
       - 职责范围和期望

    2. 项目经验要体现：
       - 完整的项目周期参与
       - 核心技术难点攻克
       - 架构设计能力
       - 团队协作经验
       - 具体的业务价值

    3. 技能描述要分层次：
       - 重点突出与JD匹配的技能
       - 体现技术深度和广度
       - 强调实战经验

    4. 个人优势要突出：
       - 技术专长和创新能力
       - 解决问题的方法论
       - 团队合作和沟通能力
       - 持续学习和成长意愿

    5. 数据指标要具体：
       - 性能优化的具体提升
       - 业务指标的改善
       - 团队效率的提升
       - 成本节省的程度
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096,
            presence_penalty=0.6,
            frequency_penalty=0.3,
        )
        
        resume_md = completion.choices[0].message.content.strip()
        return resume_md
        
    except Exception as e:
        logger.error(f"Error generating resume: {str(e)}")
        raise ValueError(f"生成简历时发生错误: {str(e)}")

async def modify_resume_section(
    resume_md: str, 
    section: str, 
    modification_request: str
) -> str:
    """修改简历特定部分的函数"""
    
    system_prompt = """你是一位专业的简历优化专家。你的任务是根据用户的要求修改简历的特定部分。
    要求：
    1. 保持简历其他部分不变
    2. 确保修改后的内容与职位要求保持一致
    3. 维持专业的表述方式
    4. 保持Markdown格式
    5. 保持原有的结构和风格
    """

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
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            presence_penalty=0.6,
            frequency_penalty=0.3,
        )
        
        modified_resume = completion.choices[0].message.content.strip()
        return modified_resume
        
    except Exception as e:
        logger.error(f"Error modifying resume: {str(e)}")
        raise ValueError(f"修改简历时发生错误: {str(e)}")
