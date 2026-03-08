# 📋 配置化设计说明

## 🎯 为什么要将Prompt放到配置中？

### 问题：硬编码的Prompt

**之前的代码**（Prompt写死在代码里）：
```python
def _reasoning(self, user_input):
    prompt = f"""你是一个AI Agent的决策中心。
    用户输入：{user_input}
    你可以使用的工具有：
    1. query_plant_database - ...
    2. ask_ai_expert - ...
    ...
    """
    # 使用prompt
```

**缺点**：
- ❌ Prompt太长，代码难读
- ❌ 修改Prompt需要改代码
- ❌ 无法统一管理Prompt
- ❌ 不便于测试和优化

---

### 解决方案：配置化

**现在的代码**（Prompt在配置文件中）：

#### 1. 配置文件 `utils/agent_config.py`
```python
class AgentConfig:
    """所有Prompt都集中管理"""

    DECISION_PROMPT_TEMPLATE = """你是一个AI Agent的决策中心。
    用户输入：{user_input}
    ...
    """

    AI_ANALYSIS_PROMPT = """你是一个专业的植物学专家..."""

    CHAT_PROMPT = "你是一个友好的助手..."

    @classmethod
    def get_decision_prompt(cls, user_input: str) -> str:
        """获取决策提示词"""
        return cls.DECISION_PROMPT_TEMPLATE.format(
            user_input=user_input,
            database_plants="、".join(cls.DATABASE_PLANTS)
        )
```

#### 2. Agent代码变得简洁
```python
def _reasoning(self, user_input):
    # 📌 从配置获取提示词
    prompt = self.config.get_decision_prompt(user_input)

    # 使用prompt
    messages = [{"role": "user", "content": prompt}]
    response = self.llm_client.chat(messages)
```

---

## ✅ 配置化的优点

### 1. 代码更清晰
```python
# 之前：代码里混杂着长长的Prompt
def _reasoning(self, user_input):
    prompt = """...500字的提示词..."""
    # 业务逻辑

# 现在：代码很简洁
def _reasoning(self, user_input):
    prompt = self.config.get_decision_prompt(user_input)  # 一行搞定
    # 业务逻辑
```

### 2. 易于维护
```python
# 修改Prompt：只需要改配置文件
# utils/agent_config.py

DECISION_PROMPT_TEMPLATE = """
你是一个更好的AI Agent...
（修改这里，不用改业务代码）
"""
```

### 3. 统一管理
所有配置集中在一个地方：
- ✅ 工具定义
- ✅ 提示词（Prompt）
- ✅ 数据库植物列表
- ✅ 评估规则
- ✅ 其他参数

### 4. 易于测试
```python
# 测试配置
def test_config():
    assert AgentConfig.DATABASE_PLANTS == [...]
    assert AgentConfig.MAX_TOKENS == 800

    # 测试提示词生成
    prompt = AgentConfig.get_decision_prompt("绿萝")
    assert "绿萝" in prompt
```

### 5. 支持多环境
```python
# 开发环境
DEV_CONFIG = {
    "temperature": 0.9,  # 更有创造性
    "max_tokens": 1000
}

# 生产环境
PROD_CONFIG = {
    "temperature": 0.7,  # 更稳定
    "max_tokens": 800
}
```

---

## 📂 配置文件结构

### `utils/agent_config.py`

```python
class AgentConfig:
    """Agent配置中心"""

    # ===== 1. 工具定义 =====
    TOOLS = {...}

    # ===== 2. 数据 =====
    DATABASE_PLANTS = [...]

    # ===== 3. 提示词（Prompt）=====
    DECISION_PROMPT_TEMPLATE = "..."
    AI_ANALYSIS_PROMPT = "..."
    CHAT_PROMPT = "..."

    # ===== 4. 评估规则 =====
    EVALUATION_RULES = {
        "min_length": 50,
        "success_threshold": 0.7
    }

    # ===== 5. 其他参数 =====
    MAX_TOKENS = 800
    TEMPERATURE = 0.7

    # ===== 方法 =====
    @classmethod
    def get_decision_prompt(cls, user_input):
        """获取格式化的提示词"""
        return cls.DECISION_PROMPT_TEMPLATE.format(...)
```

---

## 🔄 对比：之前 vs 现在

### 之前的代码结构
```
visible_agent.py (500行)
├── _define_tools()      # 工具定义在代码里
├── _reasoning()          # Prompt硬编码在方法里
├── _execute_ask_ai()     # AI提示词硬编码
└── _evaluation()         # 规则散落各处
```

**问题**：
- 配置和业务逻辑混杂
- 修改配置需要改代码
- 代码臃肿难读

### 现在的代码结构
```
utils/
└── agent_config.py       # 📌 所有配置集中管理
    ├── TOOLS
    ├── DATABASE_PLANTS
    ├── DECISION_PROMPT
    ├── AI_ANALYSIS_PROMPT
    ├── EVALUATION_RULES
    └── MAX_TOKENS

main.py (简洁)
├── _reasoning()          # 从配置读取Prompt
├── _execute_ask_ai()     # 从配置读取AI提示词
└── _evaluation()         # 从配置读取规则
```

**优点**：
- ✅ 配置和业务逻辑分离
- ✅ 代码清晰简洁
- ✅ 易于维护和扩展

---

## 🚀 使用方法

### 运行配置化版本

```bash
python3 main.py
```

### 修改配置

编辑 `utils/agent_config.py`：

```python
# 修改工具
TOOLS = {
    "new_tool": {
        "name": "新工具",
        ...
    }
}

# 修改提示词
DECISION_PROMPT_TEMPLATE = """
你是一个更好的AI Agent...
"""

# 修改参数
MAX_TOKENS = 1000  # 增加响应长度
```

### 在代码中使用配置

```python
from utils.agent_config import AgentConfig

# 获取配置
config = AgentConfig()

# 使用工具定义
tools = config.TOOLS

# 使用提示词
prompt = config.get_decision_prompt("绿萝")

# 使用参数
max_tokens = config.MAX_TOKENS
```

---

## 📊 配置项清单

| 配置项 | 类型 | 用途 | 位置 |
|--------|------|------|------|
| TOOLS | dict | 工具定义 | agent_config.py |
| DATABASE_PLANTS | list | 数据库植物列表 | agent_config.py |
| DECISION_PROMPT | str | 决策提示词 | agent_config.py |
| AI_ANALYSIS_PROMPT | str | AI分析提示词 | agent_config.py |
| CHAT_PROMPT | str | 对话提示词 | agent_config.py |
| EVALUATION_RULES | dict | 评估规则 | agent_config.py |
| MAX_TOKENS | int | 最大token数 | agent_config.py |
| TEMPERATURE | float | AI温度 | agent_config.py |

---

## 💡 最佳实践

### 1. 提示词管理
```python
# ✅ 好：集中管理
DECISION_PROMPT = "你是一个AI Agent..."

# ❌ 坏：硬编码
def some_method():
    prompt = "你是一个AI Agent..."
```

### 2. 配置读取
```python
# ✅ 好：通过方法获取
prompt = self.config.get_decision_prompt(user_input)

# ❌ 坏：直接访问属性
prompt = self.config.DECISION_PROMPT.format(...)
```

### 3. 配置更新
```python
# ✅ 好：提供更新方法
from utils.agent_config import update_config
update_config(MAX_TOKENS=1000)

# ❌ 坏：直接修改
AgentConfig.MAX_TOKENS = 1000
```

---

## 🎓 学习要点

### 配置化设计原则

1. **分离关注点** - 配置和业务逻辑分离
2. **集中管理** - 所有配置在一个地方
3. **易于修改** - 修改配置不需要改代码
4. **类型安全** - 配置有明确的类型定义
5. **易于测试** - 配置可以独立测试

### 适用场景

- ✅ Prompt很长或很复杂
- ✅ 需要频繁修改配置
- ✅ 多环境部署（开发、测试、生产）
- ✅ 团队协作（配置和代码分离）

---

## 🎉 总结

**配置化改进**：
- ✅ Prompt从代码移到配置
- ✅ 代码更清晰、更易读
- ✅ 维护更方便
- ✅ 支持多环境

**新版本**：`main.py`
- 使用配置管理
- 代码更简洁
- 更易扩展
- API密钥安全存储

**立即尝试**：
```bash
python3 main.py
```

**配置化让代码更优雅！** 🚀
