RESUME_GENERATION_PROMPT = """你是一位资深的招聘专家和简历顾问，具有丰富的人才评估经验。你需要帮助候选人创建一份突出的简历。
请使用Markdown格式生成简历内容。

关键原则：
1. 突出核心竞争力
2. 强调与JD匹配度
3. 使用数据支撑成果
4. 保持专业表述
"""

RESUME_MODIFICATION_PROMPT = """修改简历指定部分：
1. 其他部分不变
2. 符合职位要求
3. 保持专业性
4. 使用Markdown
5. 保持原结构"""

JD_ANALYSIS_PROMPT = """分析职位描述，返回JSON：
{
    "skills": {"required": [], "preferred": []},
    "responsibilities": [],
    "background": {"industry": "", "experience": "", "level": "", "team": ""}
}"""

PERSONAL_INFO_ANALYSIS_PROMPT = """分析个人背景，返回JSON：
{
    "basic": {
        "name": "",
        "email": "",
        "phone": "",
        "location": ""
    },
    "skills": [],
    "achievements": [],
    "experience": "",
    "strengths": []
}"""

SECTION_GENERATION_PROMPTS = {
    "summary": """生成个人简介：
- 匹配职位需求
- 突出核心优势
- 强调关键成就
- 说明发展方向""",
    
    "skills": """生成技能特长：
- 按类别分组
- 标注熟练度
- 突出匹配项
- 强调实战经验""",
    
    "experience": """生成工作经验：
- 按时间倒序
- 突出相关项目
- 说明技术方案
- 量化成果"""
}
