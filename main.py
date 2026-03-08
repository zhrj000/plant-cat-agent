"""
完整展示AI Agent思考过程的版本
展示：感知 → 思考 → 决策 → 行动 → 评估
"""

import sys
import os
import time
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from utils import LLMClient, llm_config, configure_llm
from config import get_config
from config.prompts import Prompts
from config.tools import Tools


class ThinkingAgent:
    """
    完整展示AI Agent思考过程的版本
    展示：感知 → 思考 → 决策 → 行动 → 评估
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

    def _print_step(self, step_number, step_name, content):
        """
        打印Agent思考步骤

        参数:
            step_number (int): 步骤编号
            step_name (str): 步骤名称
            content (str): 步骤内容
        """
        step_names = {
            1: "感知",
            2: "思考",
            3: "决策",
            4: "行动",
            5: "评估"
        }

        emojis = {
            1: "📥",
            2: "🧠",
            3: "🎯",
            4: "⚡",
            5: "📊"
        }

        step_name_zh = step_names.get(step_number, step_name)
        emoji = emojis.get(step_number, "🤖")

        print(f"\n{'='*60}")
        print(f"{emoji} Agent思考过程 - 【第{step_number}步：{step_name_zh}】")
        print(f"{'='*60}")
        print(content)
        print(f"{'='*60}\n")

    def _perception(self, user_input):
        """
        第1步：感知 - 接收用户输入
        """
        self._print_step(1, "感知", f"📥 接收到用户输入：{user_input}")
        return user_input

    def _reasoning(self, user_input):
        """
        第2步：思考 - LLM分析用户意图并选择工具
        """
        self._print_step(2, "思考", "🧠 LLM正在分析用户意图...")

        # 构建工具描述
        tools_description = ""
        for tool_name, tool_info in Tools.DEFINITIONS.items():
            tools_description += f"{tool_name} - {tool_info['name']}（优先级：{tool_info['priority']}，成本：{tool_info['cost']}，速度：{tool_info['speed']}）\n"

        # 构建决策提示词
        # 需要数据库植物列表，这里使用一个示例列表
        database_plants = ["绿萝", "百合", "吊兰", "芦荟", "猫草", "薄荷", "蜘蛛草", "仙人掌",
                          "常春藤", "杜鹃花", "水仙", "郁金香"]

        decision_prompt = self.prompts.get_decision_prompt(
            user_input=user_input,
            database_plants=database_plants
        )

        # 在提示词中添加工具描述
        decision_prompt += f"\n\n可用工具详情：\n{tools_description}"

        # 显示发送给LLM的提示词（前200字符）
        prompt_preview = decision_prompt[:200] + "..." if len(decision_prompt) > 200 else decision_prompt
        print(f"📤 发送给LLM的提示词（预览）：\n{prompt_preview}\n")

        messages = [{"role": "user", "content": decision_prompt}]

        # 调用LLM进行决策
        try:
            response = self.llm_client.chat(messages, max_tokens=200)
            self._print_step(2, "思考", f"💭 LLM分析结果：\n{response}")
            return response
        except Exception as e:
            self._print_step(2, "思考", f"❌ LLM分析失败：{e}")
            return None

    def _decision(self, reasoning_result):
        """
        第3步：决策 - 解析LLM的选择，决定使用哪个工具
        """
        self._print_step(3, "决策", "🎯 正在解析LLM的选择...")

        # 从LLM响应中提取工具选择
        selected_tool = None
        parsed_intent = "未知意图"
        parsed_reason = "未解析到原因"

        # 尝试解析JSON格式的响应
        if reasoning_result:
            # 尝试查找JSON格式
            import json
            try:
                # 查找JSON部分
                start_idx = reasoning_result.find('{')
                end_idx = reasoning_result.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = reasoning_result[start_idx:end_idx]
                    parsed_data = json.loads(json_str)
                    selected_tool = parsed_data.get("tool")
                    parsed_intent = parsed_data.get("intent", "未知意图")
                    parsed_reason = parsed_data.get("reason", "未解析到原因")

                    print(f"📋 解析到的JSON数据：")
                    print(f"   意图: {parsed_intent}")
                    print(f"   工具: {selected_tool}")
                    print(f"   原因: {parsed_reason}")
            except (json.JSONDecodeError, ValueError):
                # 如果不是JSON格式，使用简单的文本匹配
                print(f"📝 LLM响应不是标准JSON格式，使用文本匹配...")
                for tool_name in Tools.DEFINITIONS.keys():
                    if tool_name in reasoning_result.lower():
                        selected_tool = tool_name
                        break

                # 尝试提取意图和原因
                if "intent" in reasoning_result.lower():
                    lines = reasoning_result.split('\n')
                    for line in lines:
                        if "intent" in line.lower():
                            parsed_intent = line.split(':')[-1].strip()
                        if "reason" in line.lower():
                            parsed_reason = line.split(':')[-1].strip()

        if selected_tool:
            tool_info = Tools.DEFINITIONS[selected_tool]
            self._print_step(3, "决策", f"✅ 决策：使用【{tool_info['name']}】工具\n\n📋 解析结果：\n   用户意图：{parsed_intent}\n   选择工具：{selected_tool}\n   选择原因：{parsed_reason}")
            return selected_tool
        else:
            # 默认使用AI专家工具
            self._print_step(3, "决策", f"⚠️  无法确定工具，默认使用【AI专家】工具\n\n📋 解析结果：\n   用户意图：{parsed_intent}\n   选择工具：ask_ai_expert（默认）\n   选择原因：无法解析LLM响应")
            return "ask_ai_expert"

    def _action(self, selected_tool, user_input):
        """
        第4步：行动 - 执行选定的工具
        """
        tool_info = Tools.DEFINITIONS.get(selected_tool, Tools.DEFINITIONS["ask_ai_expert"])
        self._print_step(4, "行动", f"⚡ 正在执行工具：【{tool_info['name']}】")

        print(f"🔧 工具详情：")
        print(f"   名称: {tool_info['name']}")
        print(f"   描述: {tool_info.get('description', '无描述')}")
        print(f"   优先级: {tool_info['priority']}")
        print(f"   成本: {tool_info['cost']}")
        print(f"   速度: {tool_info['speed']}")
        print(f"   输入参数: {user_input}")

        try:
            if selected_tool == "ask_ai_expert":
                print(f"🤖 调用AI专家分析植物：{user_input}")
                result = self._execute_ask_ai(user_input)
            elif selected_tool == "query_plant_database":
                print(f"📊 查询植物数据库：{user_input}")
                result = self._execute_query_database(user_input)
            elif selected_tool == "list_safe_plants":
                print(f"🌿 列出所有对猫安全的植物")
                result = self._execute_list_safe_plants()
            elif selected_tool == "chat_with_user":
                print(f"💬 与用户对话：{user_input}")
                result = self._execute_chat(user_input)
            else:
                result = "❌ 未知工具"

            # 显示完整结果
            print(f"\n📄 工具执行结果：")
            print(f"{'─'*40}")
            print(result)
            print(f"{'─'*40}")

            self._print_step(4, "行动", f"✅ 工具执行完成\n\n📊 执行摘要：\n   工具：{tool_info['name']}\n   输入：{user_input}\n   状态：成功完成")
            return result

        except Exception as e:
            error_msg = f"❌ 工具执行失败：{e}"
            print(f"\n❌ 错误信息：{e}")
            self._print_step(4, "行动", f"❌ 工具执行失败\n\n📊 执行摘要：\n   工具：{tool_info['name']}\n   输入：{user_input}\n   状态：失败\n   错误：{e}")
            return error_msg

    def _evaluation(self, action_result):
        """
        第5步：评估 - 判断任务是否完成
        """
        self._print_step(5, "评估", "📊 正在评估任务完成情况...")

        print(f"📈 评估标准：")
        print(f"   1. 结果不为空")
        print(f"   2. 结果不以错误标记开头（❌）")
        print(f"   3. 结果长度合理（> 10字符）")

        # 详细的评估逻辑
        evaluation_details = []

        # 检查1：结果是否为空
        if not action_result:
            evaluation_details.append("❌ 结果为空")
            is_valid = False
        else:
            evaluation_details.append("✅ 结果不为空")

            # 检查2：是否以错误标记开头
            if action_result.startswith("❌"):
                evaluation_details.append("❌ 结果包含错误标记")
                is_valid = False
            else:
                evaluation_details.append("✅ 结果无错误标记")

                # 检查3：结果长度是否合理
                if len(action_result) < 10:
                    evaluation_details.append("⚠️  结果可能过短")
                    is_valid = True  # 仍然认为是有效的，只是可能不完整
                else:
                    evaluation_details.append("✅ 结果长度合理")
                    is_valid = True

        # 显示评估详情
        print(f"\n📋 评估详情：")
        for detail in evaluation_details:
            print(f"   {detail}")

        # 计算评估分数（简单示例）
        total_checks = len(evaluation_details)
        passed_checks = sum(1 for d in evaluation_details if d.startswith("✅"))
        score = passed_checks / total_checks if total_checks > 0 else 0

        if is_valid:
            self._print_step(5, "评估", f"✅ 任务状态：完成\n\n📊 评估报告：\n   评估分数：{score:.0%} ({passed_checks}/{total_checks})\n   总体结论：任务成功完成\n   建议：结果有效，可以返回给用户")
            return True
        else:
            self._print_step(5, "评估", f"⚠️  任务状态：未完成\n\n📊 评估报告：\n   评估分数：{score:.0%} ({passed_checks}/{total_checks})\n   总体结论：任务失败或结果无效\n   建议：需要重新执行或使用其他工具")
            return False

    def _execute_ask_ai(self, plant_name):
        """
        执行AI专家工具
        """
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

        return self.llm_client.chat(messages, max_tokens=self.config.get_max_tokens())

    def _execute_query_database(self, plant_name):
        """
        执行查询数据库工具（模拟）
        """
        # 模拟数据库查询
        database_plants = {
            "绿萝": "❌ 有毒 - 含有草酸钙结晶，会引起口腔刺激和呕吐",
            "百合": "❌ 剧毒 - 所有部分都对猫有毒，会引起肾衰竭",
            "芦荟": "❌ 有毒 - 会引起呕吐、腹泻",
            "吊兰": "✅ 安全 - 对猫无毒，可以安全种植",
            "猫草": "✅ 安全 - 专门为猫种植的草，有助于消化",
            "薄荷": "✅ 安全 - 猫薄荷对猫有吸引力且安全",
            "蜘蛛草": "✅ 安全 - 对猫无毒，容易养护",
            "仙人掌": "⚠️  小心 - 物理伤害风险，但通常无毒"
        }

        if plant_name in database_plants:
            return f"📊 数据库查询结果：\n【{plant_name}】{database_plants[plant_name]}"
        else:
            return f"❌ 数据库中未找到【{plant_name}】的信息，请使用AI专家工具"

    def _execute_list_safe_plants(self):
        """
        执行列出安全植物工具
        """
        safe_plants = [
            "吊兰", "猫草", "薄荷", "蜘蛛草", "波士顿蕨",
            "非洲紫罗兰", "迷迭香", "百里香", "罗勒"
        ]

        return f"🌿 对猫安全的植物列表：\n" + "\n".join([f"  ✅ {plant}" for plant in safe_plants])

    def _execute_chat(self, user_input):
        """
        执行对话工具
        """
        messages = [
            {
                "role": "system",
                "content": self.prompts.CHAT_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        return self.llm_client.chat(messages, max_tokens=300)

    def process_user_input(self, user_input):
        """
        处理用户输入的完整流程
        """
        print(f"\n👤 你: {user_input}")

        # 第1步：感知
        perceived_input = self._perception(user_input)

        # 第2步：思考
        reasoning_result = self._reasoning(perceived_input)

        # 第3步：决策
        selected_tool = self._decision(reasoning_result)

        # 第4步：行动
        action_result = self._action(selected_tool, perceived_input)

        # 第5步：评估
        evaluation_result = self._evaluation(action_result)

        # 显示最终结果
        print(f"\n{'='*60}")
        print(f"📝 最终回答：")
        print(f"{'='*60}")
        print(action_result)
        print(f"{'='*60}\n")

        return action_result

    def run(self):
        """
        运行Agent主循环
        """
        # 先设置LLM
        if not self.setup_llm():
            return

        print("""
╔════════════════════════════════════════════════════════════════╗
║    🤖 植物猫咪安全助手 - 完整思考过程版                       ║
║    展示：感知 → 思考 → 决策 → 行动 → 评估                     ║
╚════════════════════════════════════════════════════════════════╝

💡 使用方法：
   直接输入植物名称，观察Agent如何一步步思考、决策、执行！

   特殊命令：
   help    - 显示帮助
   exit    - 退出程序

✨ 特点：
   - 完整展示AI Agent的5步思考过程
   - API密钥安全存储在.env文件
   - 可以观察LLM如何选择工具
   - 学习AI Agent的工作原理
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
   输入植物名称，观察Agent的完整思考过程：

   示例：
   - 绿萝
   - 蝴蝶兰
   - 百合
   - 哪些植物对猫安全？

   Agent会展示：
   1. 📥 感知 - 接收输入
   2. 🧠 思考 - LLM分析意图
   3. 🎯 决策 - 选择工具
   4. ⚡ 行动 - 执行工具
   5. 📊 评估 - 判断完成
                    """)
                    continue

                # 处理用户输入
                self.process_user_input(user_input)

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
    agent = ThinkingAgent()
    agent.run()


if __name__ == "__main__":
    main()