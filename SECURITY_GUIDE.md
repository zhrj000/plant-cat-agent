# 🔐 API密钥安全配置指南

## ⚠️ 安全问题

### 之前的问题
API密钥硬编码在代码中：
```python
# ❌ 不安全
configure_llm(
    provider="deepseek",
    api_key="sk-c5ba2b0112c7495b8fe4b9714e9cad3b",  # 硬编码
    model="deepseek-chat"
)
```

**风险**：
- ❌ 代码上传到GitHub，密钥泄露
- ❌ 团队协作时，每个人都有自己的密钥
- ❌ 修改密钥需要改代码

---

## ✅ 安全改进

### 新的安全方案

#### 1. 使用.env文件存储密钥

**`.env`** 文件（实际配置，包含真实密钥）：
```
DEEPSEEK_API_KEY=sk-c5ba2b0112c7495b8fe4b9714e9cad3b
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

**`.env.example`** 文件（示例配置，上传到Git）：
```
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

#### 2. 使用.gitignore忽略敏感文件

**`.gitignore`** 文件：
```
# 环境变量和密钥文件
.env
*.key
secrets.json
```

#### 3. 从环境变量读取配置

```python
# ✅ 安全
from dotenv import load_dotenv
load_dotenv()  # 加载.env文件

configure_llm("env")  # 从环境变量读取
```

---

## 📂 文件结构

```
plant_cat_agent/
├── .env                    # 🔐 真实密钥（不上传Git）
├── .env.example            # 📝 示例配置（上传Git）
├── .gitignore              # 🚫 忽略敏感文件
├── visible_agent_secure.py # ✅ 安全版本的Agent
└── requirements.txt        # 📦 依赖（包含python-dotenv）
```

---

## 🚀 使用步骤

### 步骤1：安装依赖

```bash
pip install -r requirements.txt
```

或使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤2：配置API密钥

#### 方法A：使用.env文件（推荐）

```bash
# 1. 复制示例文件
cp .env.example .env

# 2. 编辑.env文件，填入你的真实API密钥
vim .env  # 或使用其他编辑器

# .env文件内容：
# DEEPSEEK_API_KEY=sk-your-actual-api-key-here
```

#### 方法B：使用环境变量

```bash
# macOS/Linux
export DEEPSEEK_API_KEY="sk-your-api-key-here"

# Windows
set DEEPSEEK_API_KEY=sk-your-api-key-here
```

### 步骤3：运行安全版本

```bash
python3 visible_agent_secure.py
```

---

## 📊 对比：之前 vs 现在

### 之前（不安全）

```
visible_agent.py
├── main()
│   └── configure_llm(api_key="sk-...")  # ❌ 硬编码
└── .gitignore  # 没有
```

**问题**：
- ❌ API密钥暴露在代码中
- ❌ 上传Git会泄露密钥
- ❌ 每次修改都要改代码

### 现在（安全）

```
.env（真实密钥，不上传）
├── DEEPSEEK_API_KEY=sk-...

.env.example（示例，上传Git）
├── DEEPSEEK_API_KEY=your-key-here

visible_agent_secure.py
├── main()
│   └── configure_llm("env")  # ✅ 从环境变量读取
└── .gitignore  # ✅ 忽略.env文件
```

**优点**：
- ✅ API密钥不在代码中
- ✅ .env文件不会上传Git
- ✅ 可以轻松切换不同的密钥
- ✅ 团队协作友好

---

## 🔧 配置文件说明

### .env文件格式

```bash
# DeepSeek配置
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx      # 你的API密钥
DEEPSEEK_MODEL=deepseek-chat           # 模型名称
DEEPSEEK_BASE_URL=https://api.deepseek.com  # API地址

# OpenAI配置（可选）
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-3.5-turbo

# Azure配置（可选）
# AZURE_API_KEY=...
# AZURE_ENDPOINT=...
# AZURE_DEPLOYMENT=...
```

### .gitignore文件

```gitignore
# 环境变量和密钥文件（重要！）
.env
*.key
secrets.json
config/api_keys.py
```

---

## 💡 最佳实践

### 1. 不要硬编码密钥

```python
# ❌ 错误
api_key = "sk-c5ba2b0112c7495b8fe4b9714e9cad3b"

# ✅ 正确
import os
api_key = os.getenv("DEEPSEEK_API_KEY")
```

### 2. 使用.gitignore

确保 `.gitignore` 包含：
```
.env
*.key
```

### 3. 提供.env.example

让其他人知道需要配置什么：
```bash
# 复制并填入真实密钥
cp .env.example .env
```

### 4. 检查是否泄露

上传Git前检查：
```bash
# 确认.env不会被上传
git status

# 应该看不到.env文件
```

---

## 🎯 快速开始

### 一键配置

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 创建.env文件
cat > .env << EOF
DEEPSEEK_API_KEY=sk-c5ba2b0112c7495b8fe4b9714e9cad3b
DEEPSEEK_MODEL=deepseek-chat
EOF

# 3. 运行
python3 visible_agent_secure.py
```

---

## 🔍 故障排查

### 问题1：提示"未找到环境变量"

**原因**：没有配置.env文件或环境变量

**解决**：
```bash
# 方法1：创建.env文件
cp .env.example .env
# 然后编辑.env填入密钥

# 方法2：设置环境变量
export DEEPSEEK_API_KEY="your-key"
```

### 问题2：.env文件没有被加载

**原因**：没有安装python-dotenv

**解决**：
```bash
pip install python-dotenv
```

### 问题3：密钥泄露了怎么办？

**解决**：
1. 立即在DeepSeek官网重新生成密钥
2. 更新.env文件
3. 检查Git历史，如果已上传，强制删除历史记录

---

## 📚 相关文件

- **`.env`** - 你的真实密钥（已创建）
- **`.env.example`** - 示例配置
- **`.gitignore`** - 忽略敏感文件
- **`visible_agent_secure.py`** - 安全版本的Agent
- **`requirements.txt`** - 包含python-dotenv依赖

---

## 🎉 安全改进完成！

现在的项目：
- ✅ API密钥不在代码中
- ✅ .env文件不会上传Git
- ✅ 可以轻松切换密钥
- ✅ 符合安全最佳实践

**运行安全版本**：
```bash
python3 visible_agent_secure.py
```

---

**保护你的API密钥！** 🔐
