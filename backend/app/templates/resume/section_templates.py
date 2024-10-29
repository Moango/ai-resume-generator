# 简化的简历结构，移除教育背景部分
RESUME_STRUCTURE = """# {name}
目标职位：{position_name}

## 联系方式
{contact}

## 个人简介
{summary}

## 技能特长
{skills}

## 工作经历
{work_history}

## 项目经验
{work_experience}"""

# 简化的工作经验模板
WORK_EXPERIENCE_TEMPLATE = """### {company} ({period})
#### {position}
**{project}**
- 背景：{background}
- 方案：{solution}
- 职责：{duties}
- 成果：{results}"""

# 添加工作经历模板
WORK_HISTORY_TEMPLATE = """### {position} · {company} · {location}
{period}

{summary}

{highlights}"""

GENERATION_REQUIREMENTS = """
分析要求：
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
