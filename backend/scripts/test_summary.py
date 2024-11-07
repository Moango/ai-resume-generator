import sys
import os
import asyncio
from pathlib import Path
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

# 在导入其他模块前先设置环境
from app.utils.env_utils import find_and_load_env

if not find_and_load_env():
    raise EnvironmentError("无法找到或加载.env文件")

from app.services.openai_service import (
    analyze_job_description,
    analyze_personal_info,
    generate_section,
    review_and_improve_section,
)

# 测试用的职位描述
test_job_description = """
【岗位职责】
1、独立完成相关RPA项目方案的设计与实现，包括: 计划、流程、业务影响范围、相关技术选择；

【任职要求】
1、全日制本科及以上学历，计算机及相关专业；
2、拥有RPA或者爬虫工作经验、有RPA项目交付与实施经验，能独立完成业务需求调研；
3、熟练掌握Python、JavaScript等开发语言，良好的代码规范；
4、熟悉HTTP协议、XPath、CSS Path、正则表达式等相关技术；
5、熟悉MySQL、PostgreSQL等常用数据库，能够高效的编写高性能、规范的SQL语句；
6、了解PyAutoGUI、UI Automation、PyWinAuto等自动化框架；

"""

# 测试用的个人信息
test_personal_info = """
个人信息：
姓名：张三
邮箱：zhangsan@example.com
电话：13800138000
地点：北京


"""


async def test_summary_generation():
    """测试个人简介生成功能"""
    try:
        # 验证环境变量
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY环境变量未设置")

        print("开始测试个人简介生成...")
        print("=" * 50)

        # # 1. 分析职位描述和个人信息
        # print("正在分析职位描述和个人信息...")
        # jd_analysis, personal_analysis = await asyncio.gather(
        #     analyze_job_description(test_job_description),
        #     analyze_personal_info(test_personal_info),
        # )

        # 加载测试数据
        test_data_dir = Path(__file__).parent / "test_data"
        with open(test_data_dir / "jd_analysis.json", "r", encoding="utf-8") as f:
            jd_analysis = json.load(f)
        with open(test_data_dir / "personal_analysis.json", "r", encoding="utf-8") as f:
            personal_analysis = json.load(f)

        print("\nJD分析结果:")
        print("-" * 50)
        print(json.dumps(jd_analysis, ensure_ascii=False, indent=2))

        print("\n个人信息分析结果:")
        print("-" * 50)
        print(json.dumps(personal_analysis, ensure_ascii=False, indent=2))

        # 2. 生成个人简介
        print("\n正在生成个人简介...")
        summary = await generate_section("summary", jd_analysis, personal_analysis)

        print("\n生成的个人简介:")
        print("-" * 50)
        print(summary)

        # 3. 审查和改进
    #     print("\n正在进行面试官视角审查...")
    #     review_result = await review_and_improve_section(
    #         "summary", summary, jd_analysis, personal_analysis
    #     )

    #     print("\n审查意见:")
    #     print("-" * 50)
    #     print(review_result["review"])

    #     print("\n改进后的内容:")
    #     print("-" * 50)
    #     print(review_result["improved"])
    #     print("=" * 50)

    #     # 基本验证
    #     assert summary, "个人简介不应为空"
    #     assert len(summary.split("\n")) >= 4, "个人简介应该包含足够的内容"
    #     assert "年" in summary, "应该包含工作年限"
    #     assert not any(
    #         word in summary for word in ["精通", "专家"]
    #     ), "不应使用'精通'、'专家'等主观词"

    #     print("\n✅ 测试通过！")
    #     print("验证项：")
    #     print("- 内容不为空")
    #     print("- 内容充实")
    #     print("- 包含工作年限")
    #     print("- 避免主观词")
    #     print("- 成功完成审查和改进")

    # except AssertionError as e:
    #     print(f"\n❌ 测试失败: {str(e)}")
    except Exception as e:
        print(f"\n❌ 测试出错: {str(e)}")


async def test_summary_competitive():
    """测试简历竞争力"""
    try:
        summary = await generate_section("summary", jd_analysis, personal_analysis)

        # 验证竞争力要素
        assert "RPA项目实施" in summary, "未突出RPA项目经验"
        assert "自动化框架" in summary, "未提及核心技术框架"
        assert "业务流程" in summary, "未体现业务理解能力"
        assert "团队协作" in summary, "未突出团队合作经验"

        print("✅ 竞争力测试通过")
    except Exception as e:
        print(f"❌ 竞争力测试失败: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(test_summary_generation())
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        sys.exit(1)
