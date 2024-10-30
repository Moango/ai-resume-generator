from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()

class OpenAIClient:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            try:
                cls._client = OpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("BASE_URL")
                )
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                raise ValueError(f"OpenAI客户端初始化失败: {str(e)}")
        return cls._instance

    @classmethod
    def get_client(cls) -> OpenAI:
        if cls._client is None:
            cls()
        return cls._client 