"""
安全版本的Agent
从环境变量或.env文件读取API密钥，不硬编码在代码中
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from utils import LLMClient, llm_config, configure_llm
from config import get_config
from config.prompts import Prompts


class SecureAgent:
    """
    安全版本的Agent
    API密钥从环境变量或.env文件读取
    """

    def __init__(self):
        """
        初始化Agent
        """
        self.name = "植物安全助手"
        self.llm_client = None
        self.config = get_config()
        self.prompts = Prompts()
        self.conversation_history = []

    def setup_llm(self):
        """
        设置LLM（从环境变量加载配置）
        """
        print("⚙️  正在初始化LLM...")

        # 尝试从环境变量加载
        if llm_config.load_from_env():
            print("✅ 从环境变量加载LLM配置成功")
            self.llm_client = LLMClient()
            return True

        # 如果环境变量没有配置
        print("❌ 未找到环境变量配置")
        print("\n💡 请按以下步骤配置：")
        print("   1. 复制 .env.example 为 .env")
        print("   2. 在 .env 文件中填入你的API密钥：")
        print("      DEEPSEEK_API_KEY=your-api-key-here")
        print("   3. 重新运行程序")
        print("\n   或者设置环境变量：")
        print("      export DEEPSEEK_API_KEY=your-api-key-here")
        return False

    def _print_agent_thinking(self, step, content):
        """打印Agent的思考过程"""
        print(f"\n{'='*60}")
        print(f"🤖 Agent思考过程 - 【{step}】")
        print(f"{'='*60}")
        print(content)
        print(f"{'='*60}\n")

    def ask_ai(self, plant_name):
        """
        使用AI分析植物

        参数:
            plant_name (str): 植物名称

        返回:
            str: AI的分析结果
        """
        if not self.llm_client:
            return "❌ LLM未配置"

        try:
            print(f"🤖 正在咨询AI关于【{plant_name}】的信息...")

            messages = [
                {
                    "role": "system",
                    "content": self.prompts.AI_ANALYSIS_PROMPT
                },
                {
                    "role": "user",
                    "content": f"请分析【{plant_name}】对猫的安全性"
                }
            ]

            return self.llm_client.chat(
                messages,
                max_tokens=self.config.get_max_tokens()
            )

        except Exception as e:
            return f"❌ AI分析失败: {e}"

    def run(self):
        """
        运行Agent主循环
        """
        # 先设置LLM
        if not self.setup_llm():
            return

        print("""
╔════════════════════════════════════════╗
║    🤖 植物猫咪安全助手（安全版）       ║
║    API密钥从环境变量读取               ║
╚════════════════════════════════════════╝

💡 使用方法：
   直接输入植物名称，AI会为你分析

   特殊命令：
   help    - 显示帮助
   exit    - 退出程序

✨ 特点：
   - API密钥安全存储在.env文件
   - 不会上传到Git
   - 可以轻松切换不同的API密钥
        """)

        while True:
            try:
                user_input = input("\n👤 你: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 再见！")
                    break

                if user_input.lower() in ['help', '帮助']:
                    print("""
📖 使用说明：
   直接输入植物名称，AI会为你分析其对猫的安全性

   示例：
   - 绿萝
   - 蝴蝶兰
   - 百合
                    """)
                    continue

                # 使用AI分析
                result = self.ask_ai(user_input)
                print(f"\n🤖 AI助手:\n{result}\n")

            except KeyboardInterrupt:
                print("\n\n👋 程序已退出")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}\n")


def main():
    """
    主函数
    """
    # 检查.env文件是否存在
    env_file = Path(__file__).parent / ".env"

    if not env_file.exists():
        print("⚠️  未找到.env文件")
        print("\n📝 请按以下步骤操作：")
        print("   1. 复制 .env.example 为 .env")
        print("      cp .env.example .env")
        print("   2. 编辑 .env 文件，填入你的API密钥")
        print("      DEEPSEEK_API_KEY=your-api-key-here")
        print("   3. 重新运行程序\n")
        return

    # 创建并运行Agent
    agent = SecureAgent()
    agent.run()


if __name__ == "__main__":
    main()
