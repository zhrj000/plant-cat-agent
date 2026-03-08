"""
LLM客户端模块
这个模块展示了如何调用LLM API
"""

import os
from typing import Optional, List, Dict, Any

class LLMClient:
    """
    LLM客户端类
    用于调用各种LLM服务
    """

    def __init__(self, config=None):
        """
        初始化LLM客户端

        参数:
            config: LLM配置对象
        """
        if config is None:
            from .llm_config import llm_config
            config = llm_config

        self.config = config
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """
        初始化LLM客户端
        """
        if not self.config.is_configured():
            print("⚠️ LLM未配置，将使用模拟响应")
            return

        try:
            if self.config.provider == "openai":
                self._init_openai()
            elif self.config.provider == "deepseek":
                self._init_openai()  # DeepSeek使用OpenAI兼容的API
            elif self.config.provider == "azure":
                self._init_azure()
            elif self.config.provider == "local":
                self._init_local()
        except Exception as e:
            print(f"⚠️ LLM客户端初始化失败: {e}")
            print("💡 将使用模拟响应")

    def _init_openai(self):
        """
        初始化OpenAI客户端（支持新版本API）
        """
        try:
            from openai import OpenAI
            import os

            # 临时禁用代理，避免SOCKS代理问题
            original_env = {}
            proxy_keys = ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY',
                         'http_proxy', 'https_proxy', 'all_proxy']

            # 保存原始代理设置
            for key in proxy_keys:
                if key in os.environ:
                    original_env[key] = os.environ[key]
                    os.environ.pop(key, None)

            try:
                # 如果是DeepSeek，设置base_url
                if hasattr(self.config, 'base_url'):
                    self.client = OpenAI(
                        api_key=self.config.api_key,
                        base_url=self.config.base_url
                    )
                    print(f"✅ DeepSeek客户端初始化成功 (base_url: {self.config.base_url})")
                else:
                    self.client = OpenAI(api_key=self.config.api_key)
                    print("✅ OpenAI客户端初始化成功")

            finally:
                # 恢复原始代理设置
                for key, value in original_env.items():
                    os.environ[key] = value

        except ImportError:
            print("⚠️ 未安装openai库，运行：pip install openai")
        except Exception as e:
            print(f"⚠️ OpenAI初始化失败: {e}")

    def _init_azure(self):
        """
        初始化Azure OpenAI客户端（新版本）
        """
        try:
            from openai import AzureOpenAI

            self.client = AzureOpenAI(
                api_key=self.config.api_key,
                api_version="2023-05-15",
                azure_endpoint=self.config.endpoint
            )
            print("✅ Azure OpenAI客户端初始化成功")
        except ImportError:
            print("⚠️ 未安装openai库，运行：pip install openai")
        except Exception as e:
            print(f"⚠️ Azure OpenAI初始化失败: {e}")

    def _init_local(self):
        """
        初始化本地模型客户端
        """
        # 这里可以集成Transformers等本地模型
        print("✅ 本地模型客户端初始化成功")
        print(f"💡 本地模型支持：Llama、ChatGLM等")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        调用LLM进行对话

        参数:
            messages (list): 消息列表，格式 [{"role": "user", "content": "..."}]
            temperature (float): 温度参数，控制创造性（0-1）
            max_tokens (int): 最大生成token数

        返回:
            str: LLM的响应
        """
        # 使用配置的温度和token数，如果没有传入参数
        temperature = temperature or self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens

        # 如果没有配置LLM，使用模拟响应
        if not self.config.is_configured() or self.client is None:
            return self._mock_response(messages)

        # 调用真实的LLM
        try:
            if self.config.provider in ["openai", "deepseek", "azure"]:
                return self._chat_openai(messages, temperature, max_tokens)
            elif self.config.provider == "local":
                return self._chat_local(messages, temperature, max_tokens)
        except Exception as e:
            print(f"⚠️ LLM调用失败: {e}")
            return self._mock_response(messages)

    def _chat_openai(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """
        调用OpenAI API（新版本）

        参数:
            messages (list): 消息列表
            temperature (float): 温度参数
            max_tokens (int): 最大token数

        返回:
            str: LLM响应
        """
        try:
            # 使用新版本的OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # 提取响应内容
            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ OpenAI API调用失败: {e}")
            raise e

    def _chat_local(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """
        调用本地模型

        参数:
            messages (list): 消息列表
            temperature (float): 温度参数
            max_tokens (int): 最大token数

        返回:
            str: LLM响应
        """
        # 这里可以集成Transformers等本地模型
        # 示例使用伪代码
        return "本地模型响应（需要具体实现）"

    def _mock_response(self, messages: List[Dict]) -> str:
        """
        模拟LLM响应（用于演示）

        参数:
            messages (list): 消息列表

        返回:
            str: 模拟响应
        """
        # 获取最后一条用户消息
        user_message = messages[-1]['content'] if messages else ""

        # 生成简单的模拟响应
        if "绿萝" in user_message:
            return """
根据植物毒性数据库的信息，绿萝对猫确实有一定毒性：

🌿 植物名称：绿萝
☠️ 毒性等级：中等
🏥 中毒症状：口腔刺激、呕吐、吞咽困难
💡 建议：不建议在有猫的家庭种植绿萝

这是基于数据库的查询结果。如需更详细的分析，请配置真实的LLM API。
            """
        elif "安全" in user_message:
            return """
以下是对猫安全的植物推荐：

✅ 吊兰 - 完全安全，易于养护
✅ 仙人掌 - 安全，但要注意刺
✅ 猫咪草 - 专门为猫种植，有益健康
✅ 文竹 - 安全，美观
✅ 发财树 - 安全，寓意好

这些植物即使猫咪啃食也不会中毒，非常适合有猫的家庭。

（这是基于数据库的查询结果。如需AI智能分析，请配置真实的LLM API。）
            """
        else:
            return """
我是植物猫咪安全助手AI Agent！

我可以帮你查询植物对猫的毒性信息：
1. 输入植物名称查询（如"绿萝"、"百合"）
2. 输入"safe"查看安全植物
3. 输入"toxic"查看有毒植物
4. 输入"help"查看帮助

（这是模拟响应。如需真实的AI智能分析，请配置LLM API。）
            """


# 使用示例
if __name__ == "__main__":
    """
    使用示例
    """

    print("=" * 60)
    print("LLM客户端示例")
    print("=" * 60)

    # 示例1：使用模拟响应
    print("\n示例1：使用模拟响应（无需API密钥）")
    client = LLMClient()

    messages = [
        {"role": "system", "content": "你是一个植物安全专家助手。"},
        {"role": "user", "content": "绿萝对猫有毒吗？"}
    ]

    response = client.chat(messages)
    print(f"响应：{response}")

    # 示例2：使用真实OpenAI API（需要API密钥）
    print("\n示例2：使用真实OpenAI API")
    print("首先配置LLM：")
    print('from utils.llm_config import configure_llm')
    print('configure_llm("openai", api_key="sk-your-api-key-here")')
    print("\n然后创建客户端并调用：")
    print('from utils.llm_client import LLMClient')
    print('client = LLMClient()')
    print('response = client.chat(messages)')

    # 示例3：从环境变量加载配置
    print("\n示例3：从环境变量加载配置")
    print("设置环境变量：")
    print("export OPENAI_API_KEY=sk-your-api-key-here")
    print("export OPENAI_MODEL=gpt-3.5-turbo")
    print("\n然后运行：")
    print('from utils.llm_config import llm_config')
    print('llm_config.load_from_env()')
    print('client = LLMClient()')

    print("\n" + "=" * 60)
