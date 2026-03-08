# 🤖 植物猫咪安全助手 - AI Agent 完整思考过程版

一个完全展示AI Agent 5步工作流程的教学项目

---

## 🎯 项目特色

### ✨ 完整可视化Agent思考过程

Agent会展示完整的5步思考过程：

1. **📥 感知** - Agent接收用户输入
2. **🧠 思考** - LLM分析用户意图并选择工具
3. **🎯 决策** - Agent解析LLM的选择，决定使用哪个工具
4. **⚡ 行动** - Agent执行选定的工具
5. **📊 评估** - Agent判断任务是否完成

### 🔐 安全特性

- ✅ API密钥存储在 `.env` 文件中
- ✅ 不会上传到 Git 仓库
- ✅ 符合安全最佳实践
- ✅ 自动处理代理问题

### 🤖 智能工具选择

Agent会根据植物类型智能选择工具：
- **数据库查询**：适用于12种常见植物（绿萝、百合等）
- **AI专家分析**：适用于数据库外的植物（蝴蝶兰、玫瑰等）
- **安全植物列表**：列出所有对猫安全的植物
- **对话模式**：一般性对话

---

## 🚀 快速开始

### 步骤1：安装依赖

```bash
# 推荐使用国内镜像加速
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤2：配置API密钥

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 DeepSeek API 密钥
# DEEPSEEK_API_KEY=your-api-key-here
```

### 步骤3：运行Agent

```bash
python3 main.py
```

详细配置说明请查看：[SECURITY_GUIDE.md](SECURITY_GUIDE.md)

---

## 🎯 项目特色

### ✨ 完整可视化Agent思考过程

- 📥 **感知** - Agent接收用户输入
- 🧠 **思考** - LLM分析用户意图
- 🎯 **决策** - Agent选择工具
- ⚡ **行动** - Agent执行工具
- 📊 **评估** - Agent判断任务完成

---

## 🤖 Agent工作流程

```
用户输入
    ↓
【感知】接收输入
    ↓
【思考】LLM分析意图
    ↓
【决策】选择工具
    ↓
【行动】执行工具
    ↓
【评估】判断完成
    ↓
返回结果
```

---

## 🛠️ 可用工具

### 1. query_plant_database - 查询植物数据库
- 优点：快、准、免费
- 限制：只能查12种植物
- 适用：已知植物的高频查询

### 2. ask_ai_expert - 咨询AI专家
- 优点：知识面广、智能
- 限制：需要API调用
- 适用：数据库外的植物

### 3. list_safe_plants - 列出安全植物
- 适用：查看所有安全植物

### 4. chat_with_user - 与用户对话
- 适用：一般性对话

---

## 📖 更多文档

- [QUICKSTART.md](QUICKSTART.md) - 快速入门指南
- [EXAMPLES.md](EXAMPLES.md) - 详细使用示例
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 学习路线图
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明

---

## 🎉 立即开始！

```bash
python3 main.py
```

**观察Agent如何一步步思考、决策、执行！** 🤖

---

## 📚 更多文档

- [SECURITY_GUIDE.md](SECURITY_GUIDE.md) - API密钥安全配置指南
- [QUICKSTART.md](QUICKSTART.md) - 快速入门指南
- [EXAMPLES.md](EXAMPLES.md) - 详细使用示例
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 学习路线图
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明
