"""
工具（Tools）配置
定义Agent可以使用的所有工具
"""

from typing import Dict, Any, List


class Tools:
    """
    工具配置类
    定义Agent可以使用的所有工具
    """

    # ===== 工具定义 =====

    DEFINITIONS: Dict[str, Dict[str, Any]] = {
        "query_plant_database": {
            "name": "查询植物数据库",
            "description": "查询本地数据库中已知的植物信息（速度快、免费、准确）",
            "parameters": {
                "type": "object",
                "properties": {
                    "plant_name": {
                        "type": "string",
                        "description": "要查询的植物名称"
                    }
                },
                "required": ["plant_name"]
            },
            "usage": "适用于已知植物的高频查询",
            "limitations": "只能查询12种常见植物（绿萝、吊兰、百合等），数据库外的植物无法查询",
            "priority": 1,  # 优先级（数字越小越优先）
            "cost": "free",  # 成本
            "speed": "fast"  # 速度
        },

        "ask_ai_expert": {
            "name": "咨询AI专家",
            "description": "使用DeepSeek AI分析植物信息（知识面广、智能分析、可查询任何植物）",
            "parameters": {
                "type": "object",
                "properties": {
                    "plant_name": {
                        "type": "string",
                        "description": "要分析的植物名称"
                    }
                },
                "required": ["plant_name"]
            },
            "usage": "适用于数据库中没有的植物，或需要AI深度分析的场景",
            "limitations": "需要API调用，速度稍慢，消耗API额度",
            "priority": 2,
            "cost": "paid",
            "speed": "medium"
        },

        "list_safe_plants": {
            "name": "列出安全植物",
            "description": "列出所有对猫安全的植物",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            },
            "usage": "适用于用户想了解有哪些安全植物",
            "limitations": "只显示数据库中的安全植物列表",
            "priority": 1,
            "cost": "free",
            "speed": "fast"
        },

        "chat_with_user": {
            "name": "与用户对话",
            "description": "直接与用户对话，回答一般性问题",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "用户的消息"
                    }
                },
                "required": ["message"]
            },
            "usage": "适用于非植物查询的对话",
            "limitations": "不适用于植物安全性查询",
            "priority": 3,
            "cost": "paid",
            "speed": "medium"
        }
    }

    # ===== 工具名称映射 =====

    TOOL_NAMES = {
        "database": "query_plant_database",
        "db": "query_plant_database",
        "ai": "ask_ai_expert",
        "expert": "ask_ai_expert",
        "list": "list_safe_plants",
        "safe": "list_safe_plants",
        "chat": "chat_with_user"
    }

    @classmethod
    def get_tool(cls, tool_name: str) -> Dict[str, Any]:
        """
        获取工具定义

        参数:
            tool_name (str): 工具名称

        返回:
            dict: 工具定义，如果不存在返回None
        """
        return cls.DEFINITIONS.get(tool_name)

    @classmethod
    def get_all_tools(cls) -> Dict[str, Dict[str, Any]]:
        """
        获取所有工具定义

        返回:
            dict: 所有工具定义
        """
        return cls.DEFINITIONS

    @classmethod
    def get_tool_names(cls) -> List[str]:
        """
        获取所有工具名称

        返回:
            list: 工具名称列表
        """
        return list(cls.DEFINITIONS.keys())

    @classmethod
    def resolve_tool_name(cls, alias: str) -> str:
        """
        解析工具别名到正式名称

        参数:
            alias (str): 工具别名

        返回:
            str: 正式的工具名称
        """
        return cls.TOOL_NAMES.get(alias.lower(), alias)

    @classmethod
    def get_tools_by_priority(cls) -> List[str]:
        """
        按优先级获取工具名称列表

        返回:
            list: 按优先级排序的工具名称
        """
        tools = [(name, info["priority"]) for name, info in cls.DEFINITIONS.items()]
        tools.sort(key=lambda x: x[1])
        return [name for name, _ in tools]

    @classmethod
    def get_free_tools(cls) -> List[str]:
        """
        获取免费的工具列表

        返回:
            list: 免费工具名称
        """
        return [
            name for name, info in cls.DEFINITIONS.items()
            if info.get("cost") == "free"
        ]

    @classmethod
    def get_fast_tools(cls) -> List[str]:
        """
        获取快速的工具列表

        返回:
            list: 快速工具名称
        """
        return [
            name for name, info in cls.DEFINITIONS.items()
            if info.get("speed") == "fast"
        ]


# 创建全局实例
tools = Tools()


def get_tools() -> Tools:
    """获取工具配置"""
    return tools
