from openai import OpenAI
import os
import logging
from app.utils.env_utils import find_and_load_env

logger = logging.getLogger(__name__)


class OpenAIClient:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            try:
                # 尝试加载环境变量
                if not find_and_load_env():
                    logger.warning("未能找到.env文件，尝试使用系统环境变量")

                # 获取环境变量
                api_key = os.getenv("OPENAI_API_KEY")
                base_url = os.getenv("BASE_URL")

                if not api_key:
                    raise ValueError("未找到OPENAI_API_KEY环境变量")

                cls._client = OpenAI(api_key=api_key, base_url=base_url)
                logger.info("OpenAI客户端初始化成功")

            except Exception as e:
                logger.error(f"OpenAI客户端初始化失败: {str(e)}")
                raise ValueError(f"OpenAI客户端初始化失败: {str(e)}")
        return cls._instance

    @classmethod
    def get_client(cls) -> OpenAI:
        if cls._client is None:
            cls()
        return cls._client
