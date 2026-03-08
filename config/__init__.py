"""
配置模块（Config）包初始化
这个文件让config目录成为一个Python包
"""

# 导出所有配置模块
from .prompts import Prompts, prompts, get_prompts
from .tools import Tools, tools, get_tools
from .constants import Constants, constants, get_constants
from .agent_config import AgentConfig, agent_config, get_config


# 定义模块导出的内容
__all__ = [
    # Prompts
    'Prompts',
    'prompts',
    'get_prompts',

    # Tools
    'Tools',
    'tools',
    'get_tools',

    # Constants
    'Constants',
    'constants',
    'get_constants',

    # AgentConfig (总配置)
    'AgentConfig',
    'agent_config',
    'get_config'
]


def get_all_configs():
    """
    获取所有配置

    返回:
        dict: 包含所有配置的字典
    """
    return {
        "prompts": get_prompts(),
        "tools": get_tools(),
        "constants": get_constants(),
        "agent_config": get_config()
    }
