"""
常量（Constants）配置
定义所有常量、参数和规则
"""

from typing import Dict, Any, List


class Constants:
    """
    常量配置类
    定义所有常量、参数和规则
    """

    # ===== 数据库植物列表 =====

    DATABASE_PLANTS: List[str] = [
        "绿萝", "吊兰", "百合", "仙人掌",
        "芦荟", "虎尾兰", "薄荷", "猫咪草",
        "文竹", "发财树", "龟背竹", "水仙"
    ]

    # ===== LLM参数 =====

    LLM_PARAMS = {
        "max_tokens": 800,          # AI响应的最大token数
        "temperature": 0.7,         # AI响应的温度（0-1，越高越随机）
        "top_p": 0.9,               # 核采样参数
        "frequency_penalty": 0,     # 频率惩罚
        "presence_penalty": 0       # 存在惩罚
    }

    # ===== 评估规则 =====

    EVALUATION_RULES: Dict[str, Any] = {
        "min_result_length": 50,    # 最小结果长度（字符）
        "success_threshold": 0.7,   # 成功阈值（0-1）
        "max_retries": 2,           # 最大重试次数
        "timeout": 30               # 超时时间（秒）
    }

    # ===== Agent配置 =====

    AGENT_CONFIG = {
        "name": "植物猫咪安全助手",
        "version": "2.0",
        "language": "zh-CN",
        "max_history": 100          # 最大历史记录数
    }

    # ===== 文本模板 =====

    TEMPLATES = {
        "welcome": """
╔════════════════════════════════════════╗
║    🤖 AI Agent 思考过程可视化           ║
║    展示Agent如何一步步完成任务          ║
╚════════════════════════════════════════╝
        """,
        "goodbye": "\n👋 再见！感谢使用！\n",
        "error": "\n❌ 发生错误: {error}\n",
        "thinking": "🧠 正在思考...",
        "executing": "⚡ 正在执行..."
    }

    # ===== 日志配置 =====

    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "agent.log"
    }

    # ===== 降级规则 =====

    FALLBACK_RULES = {
        "enable_auto_fallback": True,        # 启用自动降级
        "fallback_on_keywords": [            # 触发降级的关键词
            "未找到", "没有", "不存在", "错误", "失败"
        ],
        "fallback_tool": "ask_ai_expert"     # 降级到的工具
    }

    # ===== 性能配置 =====

    PERFORMANCE_CONFIG = {
        "cache_enabled": True,               # 启用缓存
        "cache_ttl": 3600,                   # 缓存时间（秒）
        "concurrent_requests": 5             # 并发请求数
    }

    @classmethod
    def get_max_tokens(cls) -> int:
        """获取最大token数"""
        return cls.LLM_PARAMS["max_tokens"]

    @classmethod
    def get_temperature(cls) -> float:
        """获取温度参数"""
        return cls.LLM_PARAMS["temperature"]

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

    @classmethod
    def get_evaluation_rule(cls, rule_name: str) -> Any:
        """
        获取评估规则

        参数:
            rule_name (str): 规则名称

        返回:
            规则值
        """
        return cls.EVALUATION_RULES.get(rule_name)

    @classmethod
    def get_template(cls, template_name: str) -> str:
        """
        获取文本模板

        参数:
            template_name (str): 模板名称

        返回:
            str: 模板内容
        """
        return cls.TEMPLATES.get(template_name, "")

    @classmethod
    def should_fallback(cls, result: str) -> bool:
        """
        判断是否应该触发降级

        参数:
            result (str): 执行结果

        返回:
            bool: 是否应该降级
        """
        if not cls.FALLBACK_RULES["enable_auto_fallback"]:
            return False

        keywords = cls.FALLBACK_RULES["fallback_on_keywords"]
        return any(keyword in result for keyword in keywords)


# 创建全局实例
constants = Constants()


def get_constants() -> Constants:
    """获取常量配置"""
    return constants
