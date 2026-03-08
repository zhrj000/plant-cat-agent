# LLM配置详细指南

## 🤖 关于LLM配置

### 当前项目说明

我创建的这个demo项目使用的是**基于规则**的AI Agent，不需要LLM也能运行。但为了让你了解如何集成真实的LLM，我提供了完整的配置方案。

---

## 📍 LLM配置在哪里

### 1. 配置文件位置

```
plant_cat_agent/
├── utils/
│   ├── __init__.py           # 工具模块初始化
│   ├── llm_config.py         # 📝 LLM配置模块（核心配置）
│   ├── llm_client.py         # 📝 LLM客户端模块（API调用）
│   └── llm_guide.md          # 📖 本文件：配置指南
```

### 2. 核心配置模块

**`utils/llm_config.py`** - LLM配置
- 支持OpenAI、Azure、本地模型
- 支持从环境变量加载
- 提供便捷的配置函数

**`utils/llm_client.py`** - LLM客户端
- 封装LLM API调用
- 支持模拟响应（无需API密钥）
- 支持多种LLM提供商

---

## 🚀 快速配置步骤

### 方法1：使用环境变量（推荐）

#### 步骤1：设置环境变量

在终端中运行：

```bash
# macOS/Linux
export OPENAI_API_KEY=sk-your-actual-api-key-here
export OPENAI_MODEL=gpt-3.5-turbo

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"
$env:OPENAI_MODEL="gpt-3.5-turbo"

# Windows CMD
set OPENAI_API_KEY=sk-your-actual-api-key-here
set OPENAI_MODEL=gpt-3.5-turbo
```

#### 步骤2：在代码中加载配置

```python
from utils.llm_config import llm_config

# 从环境变量加载
llm_config.load_from_env()

# 创建客户端
from utils.llm_client import LLMClient
client = LLMClient()
```

---

### 方法2：在代码中直接配置

```python
from utils.llm_config import configure_llm

# 配置OpenAI
configure_llm(
    provider="openai",
    api_key="sk-your-actual-api-key-here",
    model="gpt-3.5-turbo"
)

# 创建客户端
from utils.llm_client import LLMClient
client = LLMClient()
```

---

### 方法3：使用配置文件

创建 `.env` 文件：

```bash
# .env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

然后在代码中加载：

```python
from dotenv import load_dotenv
load_dotenv()  # 加载.env文件

from utils.llm_config import llm_config
llm_config.load_from_env()
```

---

## 💡 如何获取API密钥

### OpenAI API密钥

1. 访问 [OpenAI官网](https://openai.com/)
2. 注册账号并登录
3. 进入API管理页面
4. 创建新的API密钥
5. 复制密钥（格式：sk-xxxxxxxx）

**注意**：
- API密钥需要付费使用（新账号有免费额度）
- 请妥善保管密钥，不要泄露
- 不要将密钥提交到GitHub等公开平台

### Azure OpenAI

如果你使用Azure OpenAI，需要：
1. Azure账号
2. 创建OpenAI服务
3. 获取endpoint、API密钥和部署名称

---

## 📖 详细配置示例

### 示例1：基本的OpenAI配置

```python
from utils.llm_config import configure_llm
from utils.llm_client import LLMClient

# 配置OpenAI
configure_llm(
    provider="openai",
    api_key="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx",  # 你的真实API密钥
    model="gpt-3.5-turbo"
)

# 创建客户端
client = LLMClient()

# 调用LLM
messages = [
    {"role": "system", "content": "你是一个植物安全专家。"},
    {"role": "user", "content": "绿萝对猫有毒吗？"}
]

response = client.chat(messages)
print(response)
```

---

### 示例2：从环境变量加载

```python
import os

# 方式1：直接设置环境变量
os.environ['OPENAI_API_KEY'] = 'sk-proj-xxxxxxxxxxxx'
os.environ['OPENAI_MODEL'] = 'gpt-3.5-turbo'

# 方式2：从.env文件加载
from dotenv import load_dotenv
load_dotenv()

# 加载配置
from utils.llm_config import llm_config
llm_config.load_from_env()

# 创建客户端
from utils.llm_client import LLMClient
client = LLMClient()
```

---

### 示例3：使用模拟响应（无需API密钥）

```python
from utils.llm_client import LLMClient

# 不配置API密钥，直接创建客户端
# 系统会自动使用模拟响应
client = LLMClient()

messages = [
    {"role": "user", "content": "绿萝对猫有毒吗？"}
]

response = client.chat(messages)
print(response)
```

---

### 示例4：集成到现有的PlantCatAgent

修改 `plant_cat_agent.py`，添加LLM功能：

```python
from utils.llm_config import llm_config
from utils.llm_client import LLMClient

class PlantCatAgent:
    def __init__(self):
        super().__init__()

        # 初始化LLM客户端
        self.llm_client = LLMClient()

        # 检查是否配置了LLM
        if llm_config.is_configured():
            print("✅ LLM已配置，将使用AI智能分析")
        else:
            print("⚠️ LLM未配置，将使用规则引擎")

    def ask_ai_about_plant(self, plant_name: str) -> str:
        """
        使用AI分析植物

        参数:
            plant_name (str): 植物名称

        返回:
            str: AI的分析结果
        """
        messages = [
            {
                "role": "system",
                "content": "你是一个植物安全专家，专门分析植物对猫的毒性。"
            },
            {
                "role": "user",
                "content": f"请分析{plant_name}对猫的安全性，包括毒性等级、中毒症状和预防建议。"
            }
        ]

        response = self.llm_client.chat(messages)
        return response

# 使用示例
agent = PlantCatAgent()

# 使用AI分析
ai_analysis = agent.ask_ai_about_plant("绿萝")
print(ai_analysis)
```

---

## 🔧 安装依赖

如果要使用真实的LLM，需要安装相关依赖：

```bash
# 安装OpenAI库
pip install openai

# 如果使用.env文件，安装python-dotenv
pip install python-dotenv

# 如果使用Azure，也需要openai库
pip install openai

# 如果要使用本地模型（如Llama）
pip install transformers torch
```

---

## 📝 配置文件模板

### config.py（推荐创建）

在项目根目录创建 `config.py`：

```python
"""
配置文件
集中管理所有配置
"""

import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# LLM配置
LLM_CONFIG = {
    "provider": "openai",  # openai, azure, local
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
    "temperature": 0.7,
    "max_tokens": 1000,
}

# 应用配置
APP_CONFIG = {
    "name": "植物猫咪安全助手",
    "version": "1.0",
    "language": "zh-CN"
}

def get_llm_config():
    """获取LLM配置"""
    return LLM_CONFIG

def is_llm_configured():
    """检查LLM是否配置"""
    return bool(LLM_CONFIG["api_key"])
```

---

## ⚠️ 注意事项

### 1. API密钥安全

- ❌ 不要将API密钥提交到版本控制（Git）
- ❌ 不要在公开代码中硬编码API密钥
- ✅ 使用环境变量或配置文件（记得.gitignore）
- ✅ 使用.env文件并添加到.gitignore

### 2. API使用限制

- OpenAI API有调用限制（每分钟请求数）
- API调用需要付费（新账号有免费额度）
- 注意监控API使用量和费用

### 3. 降级处理

当LLM不可用时，系统应该优雅降级：

```python
def get_plant_advice(plant_name):
    """获取植物建议"""
    try:
        # 尝试使用LLM
        if llm_config.is_configured():
            return ask_llm(plant_name)
        else:
            # 降级到规则引擎
            return ask_rule_engine(plant_name)
    except Exception as e:
        print(f"LLM调用失败，使用规则引擎: {e}")
        return ask_rule_engine(plant_name)
```

---

## 🎯 推荐配置流程

### 对于学习/测试

1. ✅ 使用模拟响应（无需API密钥）
2. ✅ 理解Agent的基本原理
3. ✅ 学习代码结构
4. ✅ 后续再配置真实LLM

### 对于实际应用

1. ✅ 获取OpenAI API密钥
2. ✅ 创建 `.env` 文件保存密钥
3. ✅ 配置环境变量
4. ✅ 测试LLM调用
5. ✅ 添加错误处理和降级逻辑

---

## 💡 常见问题

### Q1: 我不想配置LLM，能运行项目吗？

**A**: 可以！项目默认使用规则引擎，不依赖LLM。LLM是可选的高级功能。

### Q2: LLM API很贵，如何降低成本？

**A**:
- 使用更便宜的模型（gpt-3.5-turbo而不是gpt-4）
- 限制max_tokens参数
- 使用缓存机制
- 只在需要时调用LLM

### Q3: 如何切换不同的LLM提供商？

**A**: 使用 `configure_llm()` 函数：

```python
# 切换到OpenAI
configure_llm("openai", api_key="...")

# 切换到Azure
configure_llm("azure", api_key="...", endpoint="...", deployment="...")

# 切换到本地模型
configure_llm("local", model_path="/path/to/model")
```

### Q4: LLM响应太慢怎么办？

**A**:
- 使用更快的模型（gpt-3.5-turbo比gpt-4快）
- 减少max_tokens
- 使用缓存
- 考虑使用本地模型

---

## 📚 更多资源

### OpenAI官方文档
- [API文档](https://platform.openai.com/docs/api-reference)
- [最佳实践](https://platform.openai.com/docs/guides)

### LangChain（Agent框架）
- [LangChain文档](https://docs.langchain.com/)
- [LangChain中文教程](https://langchain-cn.readthedocs.io/)

---

## 🎉 总结

### LLM配置要点

1. **位置**: `utils/llm_config.py` 和 `utils/llm_client.py`
2. **方式**: 环境变量、代码配置、配置文件
3. **获取**: 从OpenAI官网注册获取API密钥
4. **安全**: 不要泄露API密钥
5. **降级**: 未配置时使用模拟响应

### 学习建议

1. 先用模拟响应理解概念
2. 再配置真实LLM增强功能
3. 注意API成本和安全
4. 优雅处理错误和降级

---

**现在你已经知道在哪里配置LLM了！** 🚀

从 `utils/llm_config.py` 开始，或者直接在代码中使用 `configure_llm()` 函数。

祝你学习愉快！
