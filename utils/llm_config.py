"""
LLM配置模块
这个模块展示了如何集成真实的LLM（如OpenAI的GPT模型）
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path

# 尝试加载python-dotenv
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("⚠️  python-dotenv未安装，使用手动加载.env文件")


def load_env_file(env_path: Optional[Path] = None) -> bool:
    """
    手动加载.env文件（当python-dotenv不可用时）

    参数:
        env_path (Path): .env文件路径，如果为None则自动查找

    返回:
        bool: 是否成功加载
    """
    if env_path is None:
        # 查找.env文件（从当前目录开始向上查找）
        env_path = Path(__file__).parent.parent / '.env'

    if not env_path.exists():
        print(f"❌ 未找到.env文件: {env_path}")
        return False

    try:
        # 手动解析.env文件
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # 跳过注释和空行
                if not line or line.startswith('#'):
                    continue

                # 解析 KEY=VALUE 格式
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # 移除引号（如果有）
                    if value and value[0] in ('"', "'") and value[-1] == value[0]:
                        value = value[1:-1]

                    # 设置环境变量
                    os.environ[key] = value

        print(f"✅ 已手动加载.env文件: {env_path}")
        return True

    except Exception as e:
        print(f"❌ 加载.env文件失败: {e}")
        return False

class LLMConfig:
    """
    LLM配置类
    用于管理和配置不同的LLM服务
    """

    def __init__(self):
        """
        初始化LLM配置
        """
        # LLM提供商配置
        self.provider = "openai"  # 默认使用OpenAI
        self.api_key = None
        self.model = "gpt-3.5-turbo"  # 默认模型
        self.temperature = 0.7  # 温度参数（控制创造性）
        self.max_tokens = 1000  # 最大token数

    def set_openai_config(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        配置OpenAI

        参数:
            api_key (str): OpenAI的API密钥
            model (str): 模型名称，默认为gpt-3.5-turbo
        """
        self.provider = "openai"
        self.api_key = api_key
        self.model = model

        # 设置环境变量（OpenAI库会自动读取）
        os.environ['OPENAI_API_KEY'] = api_key

        print(f"✅ OpenAI配置完成，使用模型: {model}")

    def set_azure_config(self, api_key: str, endpoint: str, deployment: str):
        """
        配置Azure OpenAI

        参数:
            api_key (str): Azure OpenAI的API密钥
            endpoint (str): Azure OpenAI的端点URL
            deployment (str): 部署的模型名称
        """
        self.provider = "azure"
        self.api_key = api_key
        self.model = deployment
        self.endpoint = endpoint

        # 设置Azure环境变量
        os.environ['OPENAI_API_KEY'] = api_key
        os.environ['OPENAI_API_BASE'] = endpoint
        os.environ['OPENAI_API_TYPE'] = 'azure'
        os.environ['OPENAI_API_VERSION'] = '2023-05-15'

        print(f"✅ Azure OpenAI配置完成，部署: {deployment}")

    def set_deepseek_config(self, api_key: str, model: str = "deepseek-chat", base_url: str = "https://api.deepseek.com"):
        """
        配置DeepSeek

        参数:
            api_key (str): DeepSeek的API密钥
            model (str): 模型名称，默认为deepseek-chat
            base_url (str): API基础URL，默认为https://api.deepseek.com
        """
        self.provider = "deepseek"
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

        # 设置环境变量（OpenAI库会自动读取）
        os.environ['OPENAI_API_KEY'] = api_key
        os.environ['OPENAI_API_BASE'] = base_url

        print(f"✅ DeepSeek配置完成，使用模型: {model}")

    def set_local_model(self, model_path: str):
        """
        配置本地模型（如Llama、ChatGLM等）

        参数:
            model_path (str): 本地模型的路径
        """
        self.provider = "local"
        self.model = model_path

        print(f"✅ 本地模型配置完成，路径: {model_path}")

    def load_from_env(self):
        """
        从环境变量加载配置
        """
        # 先尝试加载.env文件
        if DOTENV_AVAILABLE:
            # 使用python-dotenv加载
            env_file = Path(__file__).parent.parent / '.env'
            if env_file.exists():
                load_dotenv(env_file)
                print(f"✅ 已使用python-dotenv加载.env文件: {env_file}")
        else:
            # 使用手动方法加载
            load_env_file()

        # 检查DeepSeek API密钥
        if 'DEEPSEEK_API_KEY' in os.environ:
            self.api_key = os.environ['DEEPSEEK_API_KEY']
            self.provider = "deepseek"
            self.model = os.environ.get('DEEPSEEK_MODEL', 'deepseek-chat')
            self.base_url = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
            print(f"✅ 从环境变量加载DeepSeek配置完成")
            return True

        # 检查OpenAI API密钥
        elif 'OPENAI_API_KEY' in os.environ:
            self.api_key = os.environ['OPENAI_API_KEY']
            self.provider = "openai"
            if 'OPENAI_MODEL' in os.environ:
                self.model = os.environ['OPENAI_MODEL']
            print(f"✅ 从环境变量加载OpenAI配置完成")
            return True
        else:
            print("⚠️ 未找到环境变量中的API密钥")
            return False

    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置（隐藏敏感信息）

        返回:
            dict: 配置信息
        """
        config = {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        # 不显示完整的API密钥，只显示前4位
        if self.api_key:
            config["api_key"] = f"{self.api_key[:4]}...{self.api_key[-4:]}"

        return config

    def is_configured(self) -> bool:
        """
        检查是否已配置

        返回:
            bool: 是否已配置
        """
        return self.api_key is not None


# 创建全局配置实例
llm_config = LLMConfig()


def configure_llm(provider: str = "openai", **kwargs):
    """
    配置LLM的便捷函数

    参数:
        provider (str): LLM提供商（openai、azure、deepseek、local）
        **kwargs: 其他配置参数

    示例:
        # 配置OpenAI
        configure_llm("openai", api_key="sk-...", model="gpt-3.5-turbo")

        # 配置DeepSeek
        configure_llm("deepseek", api_key="sk-...", model="deepseek-chat")

        # 配置Azure
        configure_llm("azure", api_key="...", endpoint="...", deployment="...")

        # 从环境变量加载
        configure_llm("env")
    """
    global llm_config

    if provider == "env":
        llm_config.load_from_env()
    elif provider == "openai":
        api_key = kwargs.get('api_key')
        model = kwargs.get('model', 'gpt-3.5-turbo')
        if not api_key:
            raise ValueError("OpenAI配置需要api_key参数")
        llm_config.set_openai_config(api_key, model)
    elif provider == "deepseek":
        api_key = kwargs.get('api_key')
        model = kwargs.get('model', 'deepseek-chat')
        base_url = kwargs.get('base_url', 'https://api.deepseek.com')
        if not api_key:
            raise ValueError("DeepSeek配置需要api_key参数")
        llm_config.set_deepseek_config(api_key, model, base_url)
    elif provider == "azure":
        api_key = kwargs.get('api_key')
        endpoint = kwargs.get('endpoint')
        deployment = kwargs.get('deployment')
        if not all([api_key, endpoint, deployment]):
            raise ValueError("Azure配置需要api_key、endpoint和deployment参数")
        llm_config.set_azure_config(api_key, endpoint, deployment)
    elif provider == "local":
        model_path = kwargs.get('model_path')
        if not model_path:
            raise ValueError("本地模型配置需要model_path参数")
        llm_config.set_local_model(model_path)
    else:
        raise ValueError(f"不支持的LLM提供商: {provider}")

    return llm_config


# 使用示例
if __name__ == "__main__":
    """
    使用示例
    """

    print("=" * 60)
    print("LLM配置示例")
    print("=" * 60)

    # 示例1：从环境变量加载
    print("\n示例1：从环境变量加载配置")
    llm_config.load_from_env()

    # 示例2：配置OpenAI（需要真实API密钥）
    print("\n示例2：配置OpenAI")
    print("取消注释下面的代码并填入你的API密钥：")
    print('configure_llm("openai", api_key="sk-your-api-key-here", model="gpt-3.5-turbo")')
    # configure_llm("openai", api_key="sk-your-api-key-here", model="gpt-3.5-turbo")

    # 示例3：查看当前配置
    print("\n示例3：查看当前配置")
    config = llm_config.get_config()
    for key, value in config.items():
        print(f"  {key}: {value}")

    # 示例4：检查是否已配置
    print("\n示例4：检查配置状态")
    if llm_config.is_configured():
        print("  ✅ LLM已配置")
    else:
        print("  ❌ LLM未配置")
        print("  💡 请先配置API密钥或从环境变量加载")

    print("\n" + "=" * 60)
