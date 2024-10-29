import sys
import os
import asyncio
from pathlib import Path
import json

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from app.services.openai_service import (
    analyze_job_description,
    analyze_personal_info,
    generate_section,
    review_and_improve_section,
    review_section
)

# 测试用的职位描述
test_job_description = """
职位名称：RPA开发工程师
【岗位职责】
1、独立完成相关RPA项目方案的设计与实现，包括: 计划、流程、业务影响范围、相关技术选择；
2、负责客户侧的RPA项目实施，对接客户信息化系统；
3、可编写与抽象出可重复使用的组件或模块，提高开发效率；
4、后续负责RPA平台的设计与开发工作
【任职要求】
1、全日制本科及以上学历，计算机及相关专业；
2、拥有RPA或者爬虫工作经验、有RPA项目交付与实施经验，能独立完成业务需求调研；
3、熟练掌握Python、JavaScript等开发语言，良好的代码规范；
4、熟悉HTTP协议、XPath、CSS Path、正则表达式等相关技术；
5、熟悉MySQL、PostgreSQL等常用数据库，能够高效的编写高性能、规范的SQL语句；
6、了解PyAutoGUI、UI Automation、PyWinAuto等自动化框架；
7、了解主流的UiPath、影刀、艺赛旗等RPA产品特性
8、熟悉设计模式，良好的代码规范；
9、善于沟通和逻辑表达，有较强的分析与解决问题能力；
10、能接受短期出差客户现场沟通与开发

工作地点：广州
"""

# 测试用的个人信息
test_personal_info = """
个人信息：
姓名：张三
邮箱：zhangsan@example.com
电话：13800138000
地点：上海

技术背景：
- 3年Python开发经验
- 3年RPA开发经验，熟悉影刀RPA
- 精通网页自动化和数据解析
- 有过爬虫项目经历
- 具备自动化测试和数据分析能力
- 有过多个从0到1的项目开发经验
- 开发过办公自动化项目，具体是通过Python实现办公自动化
"""

async def test_work_history_generation():
    """测试工作经历生成"""
    try:
        print("\n开始测试工作经历生成...")
        print("=" * 50)
        
        # 1. 分析职位描述
        print("\n1. 分析职位描述...")
        jd_analysis = await analyze_job_description(test_job_description)
        print("职位分析结果:")
        print("-" * 30)
        print(json.dumps(jd_analysis, ensure_ascii=False, indent=2))
        
        # 2. 分析个人信息
        print("\n2. 分析个人信息...")
        personal_analysis = await analyze_personal_info(test_personal_info)
        print("个人信息分析结果:")
        print("-" * 30)
        print(json.dumps(personal_analysis, ensure_ascii=False, indent=2))
        
        # 3. 生成工作经历
        print("\n3. 生成工作经历...")
        work_history = await generate_section(
            "work_history",
            jd_analysis,
            personal_analysis
        )
        
        print("\n生成的工作经历内容:")
        print("-" * 50)
        print(work_history)
        print("=" * 50)
        
        # 4. 面试官视角审查并改进
        print("\n4. 面试官视角审查并改进...")
        review_result = await review_and_improve_section(
            "work_history", 
            work_history,
            jd_analysis,
            personal_analysis
        )
        
        print("\n审查意见:")
        print("-" * 50)
        print(review_result["review"])
        
        print("\n改进后的内容:")
        print("-" * 50)
        print(review_result["improved"])
        print("=" * 50)
        
        # 基本验证
        assert work_history, "工作经历不应为空"
        assert "·" in work_history, "应包含职位和公司分隔符"
        assert len(work_history.split("\n")) > 5, "工作经历内容应该足够详细"
        
        print("\n✅ 测试通过！")
        print("验证项：")
        print("- 内容不为空")
        print("- 格式正确")
        print("- 内容详细")
        print("- 成功完成审查和改进")
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {str(e)}")
    except Exception as e:
        print(f"\n❌ 测试出错: {str(e)}")

def main():
    """主函数"""
    print("工作经历生成测试脚本")
    print("版本: 1.0.0")
    print("时间:", import_time := __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("-" * 50)
    
    # 运行测试
    asyncio.run(test_work_history_generation())

if __name__ == "__main__":
    main()
