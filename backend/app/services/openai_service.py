from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import logging
import re

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.chatanywhere.tech/v1"
)

logger = logging.getLogger(__name__)

def detect_language(text: str) -> str:
    # 简单的语言检测：检查是否包含中文字符
    if re.search(r'[\u4e00-\u9fff]', text):
        return "chinese"
    return "english"

async def generate_resume(personal_info: str, job_description: str) -> str:
    # 检测输入语言
    language = detect_language(personal_info + job_description)
    
    # 根据语言选择提示语
    if language == "chinese":
        prompt = f"""
        基于以下个人信息：
        {personal_info}

        以及职位描述：
        {job_description}

        生成一份最匹配职位要求的简历，以JSON格式输出。
        JSON必须包含以下键（键名使用英文，值使用中文）：
        "name"（姓名）, 
        "contact"（联系方式，包含email、phone和location）, 
        "summary"（个人总结）, 
        "skills"（技能，数组格式）, 
        "experience"（工作经验，对象数组，每个对象包含position、company、duration和responsibilities）, 
        "education"（教育背景，对象数组，每个对象包含degree、institution和graduation_year）。
        确保内容针对职位要求进行优化，输出为有效的JSON字符串。
        """
        system_prompt = "你是一位专业的中文简历撰写专家。请始终以有效的JSON格式回复，内容使用中文。"
    else:
        prompt = f"""
        Based on the following personal information:
        {personal_info}

        And the job description:
        {job_description}

        Generate a JSON format resume that best matches the job requirements. 
        The JSON should include the following keys: 
        "name", "contact" (with email, phone, and location), 
        "summary", "skills" (as an array), 
        "experience" (as an array of objects with position, company, duration, and responsibilities), 
        "education" (as an array of objects with degree, institution, and graduation_year).
        Ensure the content is tailored to the job description and the output is a valid JSON string.
        """
        system_prompt = "You are a professional resume writer. Always respond with valid JSON in English."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            n=1,
            temperature=0.7,
        )
        resume_json = completion.choices[0].message.content.strip()
        
        # 确保输出是有效的JSON
        parsed_json = json.loads(resume_json)
        
        # 转换回JSON字符串，确保正确的格式
        return json.dumps(parsed_json, ensure_ascii=False)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Received content: {resume_json}")
        raise ValueError("Generated resume is not in valid JSON format")
    except Exception as e:
        logger.error(f"Error generating resume: {str(e)}")
        raise ValueError(f"Error generating resume: {str(e)}")
