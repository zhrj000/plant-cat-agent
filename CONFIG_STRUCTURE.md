# 📂 配置目录结构说明

## 🎯 设计理念

将配置细化为不同的文件，每个文件负责一类配置：
- **职责分离** - 每个配置文件职责清晰
- **易于维护** - 修改某个配置只需要改一个文件
- **便于测试** - 每个配置模块可独立测试
- **模块化** - 配置模块化，易于扩展

---

## 📁 目录结构

```
config/
├── __init__.py          # 配置包初始化
├── prompts.py           # 📝 提示词配置
├── tools.py             # 🛠️ 工具定义
├── constants.py         # 🔢 常量和参数
└── agent_config.py      # 📋 总配置（整合）
```

---

## 📝 1. prompts.py - 提示词配置

### 职责
管理所有LLM的提示词（Prompt）

### 内容
```python
class Prompts:
    # 决策提示词
    DECISION_PROMPT_TEMPLATE = "..."

    # AI分析提示词
    AI_ANALYSIS_PROMPT = "..."

    # 对话提示词
    CHAT_PROMPT = "..."

    # 系统角色提示词
    SYSTEM_ROLES = {...}
```

### 使用方法
```python
from config import get_prompts

prompts = get_prompts()

# 获取决策提示词
decision_prompt = prompts.get_decision_prompt(
    user_input="绿萝",
    database_plants=["绿萝", "吊兰", ...]
)

# 获取AI分析提示词
ai_prompt = prompts.AI_ANALYSIS_PROMPT
```

### 优点
- ✅ 所有Prompt集中管理
- ✅ 易于修改和优化
- ✅ 便于A/B测试不同Prompt

---

## 🛠️ 2. tools.py - 工具定义

### 职责
定义Agent可以使用的所有工具

### 内容
```python
class Tools:
    # 工具定义
    DEFINITIONS = {
        "query_plant_database": {
            "name": "查询植物数据库",
            "description": "...",
            "parameters": {...},
            "usage": "...",
            "limitations": "...",
            "priority": 1,
            "cost": "free",
            "speed": "fast"
        },
        "ask_ai_expert": {...},
        "list_safe_plants": {...},
        "chat_with_user": {...}
    }

    # 工具别名映射
    TOOL_NAMES = {...}
```

### 使用方法
```python
from config import get_tools

tools = get_tools()

# 获取单个工具
tool = tools.get_tool("query_plant_database")

# 获取所有工具
all_tools = tools.get_all_tools()

# 按优先级获取工具
priority_tools = tools.get_tools_by_priority()

# 获取免费工具
free_tools = tools.get_free_tools()

# 获取快速工具
fast_tools = tools.get_fast_tools()
```

### 优点
- ✅ 工具定义集中管理
- ✅ 支持工具优先级
- ✅ 支持成本和速度分类
- ✅ 支持别名映射

---

## 🔢 3. constants.py - 常量配置

### 职责
定义所有常量、参数和规则

### 内容
```python
class Constants:
    # 数据库植物列表
    DATABASE_PLANTS = [...]

    # LLM参数
    LLM_PARAMS = {
        "max_tokens": 800,
        "temperature": 0.7,
        ...
    }

    # 评估规则
    EVALUATION_RULES = {
        "min_result_length": 50,
        "success_threshold": 0.7,
        ...
    }

    # Agent配置
    AGENT_CONFIG = {...}

    # 文本模板
    TEMPLATES = {...}

    # 降级规则
    FALLBACK_RULES = {...}
```

### 使用方法
```python
from config import get_constants

constants = get_constants()

# 判断植物是否在数据库
is_in_db = constants.is_plant_in_database("绿萝")

# 获取LLM参数
max_tokens = constants.get_max_tokens()
temperature = constants.get_temperature()

# 判断是否应该降级
should_fallback = constants.should_fallback(result)

# 获取文本模板
welcome_msg = constants.get_template("welcome")
```

### 优点
- ✅ 所有常量集中管理
- ✅ 易于修改参数
- ✅ 支持多种规则配置

---

## 📋 4. agent_config.py - 总配置

### 职责
整合所有配置模块，提供统一的访问接口

### 内容
```python
class AgentConfig:
    def __init__(self):
        self.prompts = get_prompts()
        self.tools = get_tools()
        self.constants = get_constants()

    # 提供统一的访问方法
    def get_decision_prompt(self, user_input):
        return self.prompts.get_decision_prompt(...)

    def get_tool(self, tool_name):
        return self.tools.get_tool(tool_name)

    def is_plant_in_database(self, plant_name):
        return self.constants.is_plant_in_database(plant_name)
```

### 使用方法
```python
from config import get_config

config = get_config()

# 统一的接口访问所有配置
prompt = config.get_decision_prompt("绿萝")
tool = config.get_tool("ask_ai_expert")
is_in_db = config.is_plant_in_database("蝴蝶兰")
max_tokens = config.get_max_tokens()

# 获取配置摘要
summary = config.get_config_summary()
print(summary)
```

### 优点
- ✅ 统一的访问接口
- ✅ 简化使用
- ✅ 提供配置摘要

---

## 🔄 配置文件之间的关系

```
config/
│
├── prompts.py ────┐
├── tools.py ──────┤
├── constants.py ──┤
│                  │
└──────────────────┼──> agent_config.py (整合)
                       │
                       └──> Agent使用
```

### 层次结构

1. **底层配置**：prompts.py、tools.py、constants.py（各自独立）
2. **整合层**：agent_config.py（整合底层配置）
3. **使用层**：Agent通过agent_config访问所有配置

---

## 📊 对比：之前 vs 现在

### 之前（单文件配置）

```
utils/
└── agent_config.py  # 所有配置都在一个文件
```

**问题**：
- ❌ 文件过长（500+行）
- ❌ 职责不清晰
- ❌ 难以定位配置

### 现在（多文件配置）

```
config/
├── prompts.py       # 100行 - 只管提示词
├── tools.py         # 150行 - 只管工具
├── constants.py     # 120行 - 只管常量
└── agent_config.py  # 80行 - 整合配置
```

**优点**：
- ✅ 每个文件职责单一
- ✅ 易于定位和修改
- ✅ 便于团队协作

---

## 💡 最佳实践

### 1. 修改Prompt
```bash
# 编辑 config/prompts.py
vim config/prompts.py

# 找到对应的Prompt并修改
DECISION_PROMPT_TEMPLATE = "新的提示词..."
```

### 2. 添加新工具
```python
# 在 config/tools.py 中添加
DEFINITIONS = {
    ...,
    "new_tool": {
        "name": "新工具",
        "description": "...",
        ...
    }
}
```

### 3. 修改参数
```python
# 在 config/constants.py 中修改
LLM_PARAMS = {
    "max_tokens": 1000,  # 增加token数
    "temperature": 0.8,  # 调高温度
    ...
}
```

### 4. 添加新常量
```python
# 在 config/constants.py 中添加
NEW_CONSTANT = "新常量"
```

---

## 🎯 使用建议

### 简单使用
```python
from config import get_config

config = get_config()
# 使用统一的接口
```

### 高级使用
```python
from config import get_prompts, get_tools, get_constants

# 分别访问各个配置模块
prompts = get_prompts()
tools = get_tools()
constants = get_constants()
```

---

## 📈 扩展性

### 添加新的配置模块

例如添加 `database.py`：

```python
# config/database.py
class Database:
    CONNECTION_STRING = "..."
    PLANTS_COLLECTION = "plants"
    ...

# config/__init__.py
from .database import Database, database, get_database
```

---

## 🎉 总结

### 配置结构
- ✅ **prompts.py** - 管理所有提示词
- ✅ **tools.py** - 管理工具定义
- ✅ **constants.py** - 管理常量和参数
- ✅ **agent_config.py** - 整合所有配置

### 优点
- ✅ 职责清晰
- ✅ 易于维护
- ✅ 便于扩展
- ✅ 易于测试

### 使用
```python
from config import get_config

config = get_config()
prompt = config.get_decision_prompt("绿萝")
```

---

**配置细化，代码更优雅！** 🚀
