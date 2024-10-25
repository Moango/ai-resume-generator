# 定制简历生成系统

## 项目概述
基于AI的智能简历定制系统，通过分析用户的个人背景（包括技术栈、项目经验等）以及目标公司的招聘需求，自动生成一份与职位JD高度匹配的专业简历。
![主页面](docs/images/home_page.png)
## 功能需求

1. 用户输入
   - 用户可以自由输入他们认为相关的个人信息（如教育背景、工作经验、技能等）
   - 用户可以以自由文本形式输入目标公司的招聘要求

2. 简历生成
   - 使用OpenAI API处理用户输入并生成定制简历
   - 输出格式为Markdown
   - 支持动态字段和灵活的数据结构

3. 用户界面
   - 单页Web应用
   - 不需要用户注册或登录
   - 不保存或编辑生成的简历
   - 响应式设计，支持移动端和桌面端
   - 支持暗色模式
   - 优雅的加载状态和错误处理

## 技术栈
- 前端：
  - React 18
  - Tailwind CSS 
  - Axios 
- 后端：
  - Python with FastAPI
  - OpenAI API
  - Pydantic 

## 项目架构

1. 前端 (React)
   - 组件结构：
     - App：主应用组件，负责整体布局和状态管理
     - InputForm：用户输入表单，支持个人信息和职位描述输入
     - ResumeDisplay：动态简历显示组件，支持任意JSON结构
   - 特性：
     - 使用 React Hooks 进行状态管理
     - 使用 Tailwind CSS 实现响应式设计
     - 支持优雅的加载状态和错误处理
     - 实现了磨砂玻璃效果和渐变背景
     - 支持暗色模式

2. 后端 (FastAPI)
   - 主要模块：
     - main.py：应用入口点，包含FastAPI应用实例和CORS配置
     - routers/：API路由定义，处理简历生成请求
     - services/：业务逻辑处理，包括OpenAI API集成
     - models/：数据模型定义，使用Pydantic进行验证
   - API端点：
     - POST /api/v1/generate_resume：接收用户输入，返回生成的简历
   - 特性：
     - 完整的错误处理和日志记录
     - 请求验证和响应模型
     - 异步处理支持

3. OpenAI集成
   - 创建专门的服务来处理与OpenAI API的通信
   - 实现提示工程，将用户输入转化为适合OpenAI API的格式
   - 处理API响应并确保输出格式正确

## 已完成的功能
1. ✅ 基础项目结构搭建
2. ✅ 前端界面设计和实现
3. ✅ 后端API开发
4. ✅ OpenAI集成
5. ✅ 响应式设计
6. ✅ 错误处理
7. ✅ 暗色模式支持
8. ✅ 测试用例编写

## 下一步计划
1. 添加更多的简历模板
2. 实现简历导出功能（PDF、Word格式）
3. 优化OpenAI提示工程
4. 添加更多的单元测试
5. 性能优化
6. 部署到生产环境

## 注意事项
- 由于使用OpenAI API，需要考虑API调用的成本和限制
- 确保用户了解他们的输入将被发送到第三方服务（OpenAI）进行处理
- 建议在使用前设置适当的环境变量（OPENAI_API_KEY）

## 本地开发
1. 克隆项目
2. 前端设置：   
```bash
   cd frontend
   npm install
   npm start   
```
3. 后端设置：   
```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload   
   ```
4. 设置环境变量：
   - 创建 `.env` 文件
   - 添加 `OPENAI_API_KEY=your_api_key`

## 测试
- 后端测试：`pytest`
- 前端测试：`npm test`

## 项目进度更新

### 2024-10-23: 优化提示工程
- ✅ 改进 system prompt 和用户 prompt
- ✅ 优化 OpenAI API 参数配置
- ✅ 增强错误处理和日志记录
- ✅ 提升简历生成质量

下一步计划:
1. 添加简历模板支持
2. 实现导出功能
3. 增加更多单元测试
4. 部署到生产环境

### 2024-10-24: 优化OpenAI服务
- ✅ 重构OpenAI服务代码结构
- ✅ 优化提示工程系统设计
- ✅ 改进简历生成质量
- ✅ 强错误处理机制

主要改进：
1. 提示工程系统化
   - 分离system prompt和user prompt
   - 明确的简历结构要求
   - 详细的评估维度指导
   - 数据指标要求具体化

2. 简历生成质量提升
   - 更专业的技能描述分层
   - 更完整的项目经验展示
   - 更具体的数据指标支持
   - 更强的JD匹配度分析

3. 错误处理增强
   - 完整的异常捕获
   - 详细的日志记录
   - 友好的错误提示
   - 异常追踪支持

下一步计划:
1. 优化提示工程      
2. 添加简历模板系统
3. 实现多语言支持
4. 优化响应速度

### 2024-10-25: 实施模板化处理

✅ 完成提示词模板化改造
- 分离系统提示词到独立文件
- 创建简历结构模板
- 优化代码组织结构

主要改进：
1. 提示词管理
   - 创建专门的模板目录
   - 分离系统提示词和简历模板
   - 提高代码可维护性

2. 代码组织优化
   - 模块化设计
   - 清晰的文件结构
   - 便于后续扩展

下一步计划：
1. 实现分步骤生成方案
2. 添加缓存机制
3. 优化提示词内容
4. 实现更多简历模板

## 功能更新
- ✅ 增加目标职位名称输入
- ✅ 优化简历生成逻辑,考虑职位名称因素

### 2024-10-26: 职位名称功能完善
- ✅ 修职位名称参数传递问题
- ✅ 优化简历模板显示职位名称
- ✅ 完善错误处理机制

主要改进：
1. 参数传递优化
   - 完整的职位名称处理流程
   - 强化错误处理机制
   - 改进日志记录

2. 显示优化
   - 简历模板整合职位名称
   - 优化显示格式
   - 提升可读性

下一步计划：
1. 增强职位匹配分析
2. 优化简历模板样式
3. 添加更多自定义选项

### 调试记录
- 修复了RESUME_STRUCTURE未定义的问题
- 确保了所有必要的模板导入
- 验证了模板系统的正常工作

### 2024-10-27: 优化简历生成质量

✅ 完成简历质量提升改造
- 优化提示词系统，增加更详细的指导原则
- 改进数据可信度要求
- 强化技术深度展示
- 完善业务价值描述

主要改进：
1. 提示词优化
   - 添加具体的评估维度
   - 细化数据支撑要求
   - 强化技术描述规范
   - 完善业务价值展示

2. 简历生成质量
   - 更注重技术细节
   - 强调数据可信度
   - 突出业务理解
   - 清晰个人贡献

下一步计划：
1. 添加更多行业特定模板
2. 实现智能数据验证
3. 优化技术描述生成
4. 增强业务价值量化

### 2024-10-27: 优化简历术语和内容

✅ 完成简历术语规范化
- 将"项目经验"改为"项目经历"，使术语更专业准确
- 优化项目经历模板结构
- 完善项目经历生成提示词

主要改进：
1. 术语规范化
   - 统一使用"项目经历"
   - 优化项目描述结构
   - 完善模板格式

2. 内容生成优化
   - 更详细的项目背景描述
   - 更清晰的技术方案说明
   - 更具体的职责描述
   - 更量化的成果展示

下一步计划：
1. 继续优化简历模板
2. 增强项目经历的展示效果
3. 完善技术细节描述
4. 强化成果量化指标

### 2024-10-27: 深化简历生成质量

✅ 完成项目经历生成优化
- 重构项目经历生成提示词
- 增加技术深度要求
- 强化数据可信度验证
- 完善业务价值展示

主要改进：
1. 提示词系统升级
   - 增加具体的技术实现要求
   - 添加数据可信度验证机制
   - 强化业务理解展示
   - 完善项目管理描述

2. 内容质量提升
   - 技术细节更具体
   - 数据指标更可信
   - 业务价值更清晰
   - 个人贡献更突出

3. 模板结构优化
   - 更清晰的项目描述结构
   - 更专业的技术内容展示
   - 更完整的项目管理体现
   - 更强的JD匹配度

下一步计划：
1. 实现智能数据验证机制
2. 添加更多技术场景模板
3. 化业务价值量化方法
4. 增强与JD的匹配分析

### 2024-10-27: 优化简历生成系统

✅ 完成简历生成系统核心优化
- 重构提示词系统，提升通用性
- 增强动态适应能力
- 优化项目经历生成逻辑
- 完善价值展示机制

主要改进：
1. 提示词系统重构
   - 建立通用技术匹配机制
   - 优化项目经历生成逻辑
   - 增强动态适应能力
   - 完善价值展示体系

2. 生成策略优化
   - 智能项目筛选和重组
   - 动态重点调整
   - 深化能力佐证
   - 强化结果导向

下一步计划：
1. 实现智能匹配算法
2. 优化项目筛选机制
3. 增强价值量化能力
4. 完善技术栈分析

### 2024-10-27: 优化简历结构

✅ 完成工作经历与项目经历分离
- 新增工作经历专门模块
- 优化内容组织结构
- 完善生成策略

主要改进：
1. 结构优化
   - 分离工作经历和项目经历
   - 工作经历突出职责和成就
   - 项目经历侧重技术细节
   - 提升简历可读性

2. 内容策略
   - 工作经历引导面试方向
   - 项目经历展示技术实力
   - 避免内容重复
   - 突出核心竞争力

3. 生成逻辑
   - 差异化的内容生成策略
   - 智能的重点分配
   - 合理的篇幅控制
   - 清晰的层次结构

下一步计划：
1. 优化工作经历引导性
2. 增强项目经历技术深度
3. 完善数据可信度验证
4. 提升内容的连贯性
