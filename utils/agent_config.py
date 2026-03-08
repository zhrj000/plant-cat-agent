"""
Agent配置模块
定义Agent的提示词（Prompt）、工具定义、决策规则
"""

from typing import Dict, Any


class AgentConfig:
    """
    Agent配置类
    集中管理所有配置信息
    """

    # ===== 工具定义 =====

    TOOLS: Dict[str, Dict[str, Any]] = {
        "query_plant_database": {
            "name": "查询植物数据库",
            "description": "查询本地数据库中已知的植物信息（速度快、免费、准确）",
            "parameters": ["植物名称"],
            "usage": "适用于已知植物的高频查询",
            "limitations": "只能查询12种常见植物（绿萝、吊兰、百合等），数据库外的植物无法查询"
        },
        "ask_ai_expert": {
            "name": "咨询AI专家",
            "description": "使用DeepSeek AI分析植物信息（知识面广、智能分析、可查询任何植物）",
            "parameters": ["植物名称"],
            "usage": "适用于数据库中没有的植物，或需要AI深度分析的场景",
            "limitations": "需要API调用，速度稍慢，消耗API额度"
        },
        "list_safe_plants": {
            "name": "列出安全植物",
            "description": "列出所有对猫安全的植物",
            "parameters": [],
            "usage": "适用于用户想了解有哪些安全植物",
            "limitations": "只显示数据库中的安全植物列表"
        },
        "chat_with_user": {
            "name": "与用户对话",
            "description": "直接与用户对话，回答一般性问题",
            "parameters": ["用户问题"],
            "usage": "适用于非植物查询的对话",
            "limitations": "不适用于植物安全性查询"
        }
    }

    # ===== 数据库中的植物列表 =====

    DATABASE_PLANTS = [
        "绿萝", "吊兰", "百合", "仙人掌",
        "芦荟", "虎尾兰", "薄荷", "猫咪草",
        "文竹", "发财树", "龟背竹", "水仙"
    ]

    # ===== LLM决策提示词 =====

    DECISION_PROMPT_TEMPLATE = """你是一个AI Agent的决策中心。

用户输入：{user_input}

你可以使用的工具有：

1. query_plant_database - 查询本地植物数据库
   - 描述：查询已知植物信息（速度快、免费、准确）
   - 限制：只能查询12种常见植物（{database_plants}）
   - 适用：这12种植物的高频查询

2. ask_ai_expert - 咨询AI专家
   - 描述：使用AI分析任何植物（知识面广、智能）
   - 限制：需要API调用，稍慢
   - 适用：数据库中没有的植物（如蝴蝶兰、玫瑰、茉莉等）

3. list_safe_plants - 列出安全植物
   - 适用：用户想了解所有安全植物

4. chat_with_user - 与用户对话
   - 适用：一般性对话

重要提示：
- 如果用户输入的植物不在数据库12种植物中，应该选择 ask_ai_expert
- 如果不确定植物是否在数据库中，优先选择 ask_ai_expert

请分析用户意图，决定：
1. 用户想做什么？
2. 应该使用哪个工具？
3. 为什么选择这个工具？

请用简洁的JSON格式回答：
{{
    "intent": "用户意图",
    "tool": "选择的工具名称",
    "reason": "选择理由（说明为什么选择这个工具）"
}}"""

    # ===== AI分析提示词 =====

    AI_ANALYSIS_PROMPT = """你是一个专业的植物学和宠物护理专家。

你的任务是分析各种植物对猫的安全性，请按照以下格式回答：

🌿 植物名称：[植物名]
⚠️ 对猫的安全性：[安全/有毒/轻微毒性等]
🏥 中毒症状：[如果有毒，说明症状]
💡 养护建议：[给养猫家庭的建议]
📝 详细说明：[详细介绍这种植物]

请用简洁、专业但易懂的语言回答，不要太长。"""

    # ===== 对话提示词 =====

    CHAT_PROMPT = "你是一个友好的植物安全专家助手，专门帮助用户了解植物对猫的安全性。"

    # ===== 评估规则 =====

    EVALUATION_RULES = {
        "min_length": 50,  # 最小结果长度
        "success_threshold": 0.7  # 成功阈值
    }

    # ===== 其他配置 =====

    MAX_TOKENS = 800  # AI响应的最大token数
    TEMPERATURE = 0.7  # AI响应的温度

    @classmethod
    def get_decision_prompt(cls, user_input: str) -> str:
        """
        获取决策提示词

        参数:
            user_input (str): 用户输入

        返回:
            str: 格式化后的提示词
        """
        return cls.DECISION_PROMPT_TEMPLATE.format(
            user_input=user_input,
            database_plants="、".join(cls.DATABASE_PLANTS)
        )

    @classmethod
    def get_tool_info(cls, tool_name: str) -> Dict[str, Any]:
        """
        获取工具信息

        参数:
            tool_name (str): 工具名称

        返回:
            dict: 工具信息，如果不存在返回None
        """
        return cls.TOOLS.get(tool_name)

    @classmethod
    def is_plant_in_database(cls, plant_name: str) -> bool:
        """
        判断植物是否在数据库中

        参数:
            plant_name (str): 植物名称

        返回:
            bool: 是否在数据库中
        """
        return plant_name in cls.DATABASE_PLANTS


# 创建全局配置实例
agent_config = AgentConfig()


def get_config() -> AgentConfig:
    """
    获取Agent配置

    返回:
        AgentConfig: 配置实例
    """
    return agent_config


def update_config(**kwargs):
    """
    更新Agent配置

    参数:
        **kwargs: 要更新的配置项
    """
    for key, value in kwargs.items():
        if hasattr(agent_config, key):
            setattr(agent_config, key, value)


# 使用示例
if __name__ == "__main__":
    """使用示例"""
    print("=" * 60)
    print("Agent配置示例")
    print("=" * 60)

    # 1. 查看所有工具
    print("\n1. 所有工具：")
    for tool_name, tool_info in AgentConfig.TOOLS.items():
        print(f"   {tool_name}: {tool_info['name']}")
        print(f"      {tool_info['description']}")

    # 2. 查看数据库植物
    print("\n2. 数据库中的植物：")
    print(f"   {', '.join(AgentConfig.DATABASE_PLANTS)}")

    # 3. 生成决策提示词
    print("\n3. 决策提示词示例：")
    prompt = AgentConfig.get_decision_prompt("绿萝")
    print(prompt[:200] + "...")

    # 4. 判断植物是否在数据库
    print("\n4. 植物判断：")
    test_plants = ["绿萝", "蝴蝶兰", "百合"]
    for plant in test_plants:
        in_db = AgentConfig.is_plant_in_database(plant)
        status = "✅ 在数据库中" if in_db else "❌ 不在数据库中"
        print(f"   {plant}: {status}")

    print("\n" + "=" * 60)
