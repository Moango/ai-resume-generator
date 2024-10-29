import sys
import os
import asyncio
from pathlib import Path
import json

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from app.services.project_service import enhance_project_descriptions

# 测试数据
test_personal_info = """
会flask,django,fastapi等python框架，常用数据库也会，有过AIGC相关经验。
做过多个从0到1的项目，例如无线麦克风管理系统.
无线麦克风管理系统，前端使用vue，后端使用fastapi+sqlite来开发，我主要负责后端开发
"""

async def test_project_enhancement():
    """测试项目描述增强"""
    try:
        print("\n开始测试项目描述增强...")
        print("=" * 50)
        
        # 运行项目增强
        result = await enhance_project_descriptions(test_personal_info)
        
        print("\n1. 原始信息:")
        print("-" * 30)
        print(result["original_info"])
        
        print("\n2. 增强的项目:")
        print("-" * 30)
        for idx, project in enumerate(result["enhanced_projects"], 1):
            print(f"\n项目 {idx}:")
            print(f"名称: {project['project']['name']}")
            print(f"领域: {project['project']['domain']}")
            print(f"缺失信息: {', '.join(project['missing_aspects'])}")
            print("\n分析结果:")
            print(json.dumps(project['analysis'], ensure_ascii=False, indent=2))
            print("\n确认问题:")
            for q in project['questions']:
                print(f"\n{q['type']}:")
                print(f"当前理解: {q['current']}")
                print(f"确认问题: {q['confirm']}")
                print(f"补充要求: {q['details']}")
            print("-" * 30)
        
        print("\n✅ 测试通过！")
        
    except Exception as e:
        print(f"\n❌ 测试出错: {str(e)}")

def main():
    """主函数"""
    print("项目描述增强测试脚本")
    print("版本: 1.0.0")
    print("时间:", import_time := __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("-" * 50)
    
    # 运行测试
    asyncio.run(test_project_enhancement())

if __name__ == "__main__":
    main()
