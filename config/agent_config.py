"""
Agent总配置
整合所有配置模块，提供统一的访问接口
"""

from typing import Dict, Any
from .prompts import Prompts, get_prompts
from .tools import Tools, get_tools
from .constants import Constants, get_constants


class AgentConfig:
    """
    Agent总配置类
    整合prompts、tools、constants三个配置模块
    """

    def __init__(self):
        """
        初始化配置
        """
        # 加载各个配置模块
        self.prompts = get_prompts()
        self.tools = get_tools()
        self.constants = get_constants()

    # ===== 提示词相关方法 =====

    def get_decision_prompt(self, user_input: str) -> str:
        """
        获取决策提示词

        参数:
            user_input (str): 用户输入

        返回:
            str: 格式化后的提示词
        """
        return self.prompts.get_decision_prompt(
            user_input=user_input,
            database_plants=self.constants.DATABASE_PLANTS
        )

    def get_ai_analysis_prompt(self) -> str:
        """获取AI分析提示词"""
        return self.prompts.AI_ANALYSIS_PROMPT

    def get_chat_prompt(self) -> str:
        """获取对话提示词"""
        return self.prompts.CHAT_PROMPT

    # ===== 工具相关方法 =====

    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """获取工具定义"""
        return self.tools.get_tool(tool_name)

    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        """获取所有工具"""
        return self.tools.get_all_tools()

    def get_tool_names(self):
        """获取所有工具名称"""
        return self.tools.get_tool_names()

    # ===== 常量相关方法 =====

    def is_plant_in_database(self, plant_name: str) -> bool:
        """判断植物是否在数据库中"""
        return self.constants.is_plant_in_database(plant_name)

    def get_max_tokens(self) -> int:
        """获取最大token数"""
        return self.constants.get_max_tokens()

    def get_temperature(self) -> float:
        """获取温度参数"""
        return self.constants.get_temperature()

    def should_fallback(self, result: str) -> bool:
        """判断是否应该降级"""
        return self.constants.should_fallback(result)

    def get_fallback_tool(self) -> str:
        """获取降级工具"""
        return self.constants.FALLBACK_RULES["fallback_tool"]

    # ===== 配置信息方法 =====

    def get_agent_info(self) -> Dict[str, Any]:
        """
        获取Agent信息

        返回:
            dict: Agent信息
        """
        return self.constants.AGENT_CONFIG

    def get_config_summary(self) -> str:
        """
        获取配置摘要

        返回:
            str: 配置摘要文本
        """
        summary = f"""
Agent配置摘要：
════════════════════════════════════════

基本信息：
  名称：{self.constants.AGENT_CONFIG['name']}
  版本：{self.constants.AGENT_CONFIG['version']}
  语言：{self.constants.AGENT_CONFIG['language']}

工具配置：
  工具数量：{len(self.tools.get_tool_names())}
  工具列表：{', '.join(self.tools.get_tool_names())}
  免费工具：{', '.join(self.tools.get_free_tools())}
  快速工具：{', '.join(self.tools.get_fast_tools())}

数据库配置：
  植物数量：{len(self.constants.DATABASE_PLANTS)}
  植物列表：{', '.join(self.constants.DATABASE_PLANTS[:5])}...

LLM配置：
  最大token：{self.constants.LLM_PARAMS['max_tokens']}
  温度：{self.constants.LLM_PARAMS['temperature']}

评估配置：
  最小结果长度：{self.constants.EVALUATION_RULES['min_result_length']}
  成功阈值：{self.constants.EVALUATION_RULES['success_threshold']}

降级配置：
  自动降级：{'启用' if self.constants.FALLBACK_RULES['enable_auto_fallback'] else '禁用'}
  降级工具：{self.constants.FALLBACK_RULES['fallback_tool']}

════════════════════════════════════════
        """
        return summary


# 创建全局配置实例
agent_config = AgentConfig()


def get_config() -> AgentConfig:
    """
    获取Agent配置实例

    返回:
        AgentConfig: 配置实例
    """
    return agent_config


# 使用示例
if __name__ == "__main__":
    """使用示例"""
    config = get_config()

    # 1. 获取配置摘要
    print(config.get_config_summary())

    # 2. 获取提示词
    prompt = config.get_decision_prompt("绿萝")
    print("\n决策提示词示例：")
    print(prompt[:200] + "...")

    # 3. 判断植物是否在数据库
    print("\n植物判断：")
    print(f"  绿萝: {config.is_plant_in_database('绿萝')}")
    print(f"  蝴蝶兰: {config.is_plant_in_database('蝴蝶兰')}")

    # 4. 获取工具信息
    print("\n工具列表：")
    for tool_name in config.get_tool_names():
        tool = config.get_tool(tool_name)
        print(f"  {tool_name}: {tool['name']}")
