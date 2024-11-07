from pathlib import Path
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def find_and_load_env() -> bool:
    """递归向上查找并加载.env文件

    Returns:
        bool: 是否成功找到并加载了.env文件
    """
    current_path = Path.cwd()
    max_levels = 4  # 增加查找层级
    searched_paths = []

    # 首先检查当前文件所在目录
    current_file = Path(__file__)
    current_dir = current_file.parent
    env_paths = [
        current_dir / ".env",
        current_dir.parent / ".env",  # app目录
        current_dir.parent.parent / ".env",  # backend目录
        current_dir.parent.parent.parent / ".env",  # 项目根目录
    ]

    # 检查特定路径
    for env_path in env_paths:
        if env_path.exists() and env_path not in searched_paths:
            logger.info(f"找到.env文件: {env_path}")
            load_dotenv(env_path)
            return True
        searched_paths.append(env_path)

    # 如果特定路径都没找到，则从当前工作目录开始向上查找
    for _ in range(max_levels):
        env_file = current_path / ".env"
        if env_file.exists() and env_file not in searched_paths:
            logger.info(f"找到.env文件: {env_file}")
            load_dotenv(env_file)
            return True
        searched_paths.append(env_file)

        parent = current_path.parent
        if parent == current_path:  # 已经到达根目录
            break
        current_path = parent

    logger.warning(
        f"在以下路径中未找到.env文件:\n" + "\n".join(str(p) for p in searched_paths)
    )
    return False
