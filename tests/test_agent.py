"""
AI Agent 单元测试文件
用于测试Agent的各个功能是否正常工作
"""

import sys
import os

# 添加父目录到Python路径，以便导入项目模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plant_cat_agent import PlantCatAgent
from data import get_plant_info, get_all_plant_names, get_safe_plants, get_toxic_plants


def test_plant_database_query():
    """
    测试数据库查询功能
    """
    print("测试1: 数据库查询功能")

    # 测试查询存在的植物（精确匹配）
    plant_info = get_plant_info("绿萝")
    assert plant_info is not None, "应该能找到绿萝"
    assert plant_info['name'] == "绿萝", "植物名称应该正确"
    assert plant_info['toxic_to_cats'] == True, "绿萝对猫有毒"
    print("   ✅ 精确匹配测试通过")

    # 测试查询存在的植物（模糊匹配）
    plant_info = get_plant_info("吊")
    assert plant_info is not None, "应该能通过模糊匹配找到吊兰"
    assert plant_info['name'] == "吊兰", "模糊匹配应该找到吊兰"
    print("   ✅ 模糊匹配测试通过")

    # 测试查询不存在的植物
    plant_info = get_plant_info("不存在的植物")
    assert plant_info is None, "不应该找到不存在的植物"
    print("   ✅ 不存在植物查询测试通过")


def test_safe_and_toxic_lists():
    """
    测试安全植物和有毒植物列表
    """
    print("\n测试2: 安全植物和有毒植物列表")

    # 获取安全植物列表
    safe_plants = get_safe_plants()
    assert len(safe_plants) > 0, "应该有安全植物"
    assert "吊兰" in safe_plants, "吊兰应该在安全植物列表中"
    assert "绿萝" not in safe_plants, "绿萝不应该在安全植物列表中"
    print(f"   ✅ 安全植物列表测试通过（共{len(safe_plants)}种）")

    # 获取有毒植物列表
    toxic_plants = get_toxic_plants()
    assert len(toxic_plants) > 0, "应该有毒植物"
    assert "绿萝" in toxic_plants, "绿萝应该在有毒植物列表中"
    assert "吊兰" not in toxic_plants, "吊兰不应该在有毒植物列表中"
    print(f"   ✅ 有毒植物列表测试通过（共{len(toxic_plants)}种）")


def test_agent_initialization():
    """
    测试Agent初始化
    """
    print("\n测试3: Agent初始化")

    agent = PlantCatAgent()
    assert agent.name == "植物猫咪安全助手", "Agent名称应该正确"
    assert agent.conversation_history == [], "初始对话历史应该为空"
    print("   ✅ Agent初始化测试通过")


def test_agent_plant_safety_check():
    """
    测试Agent的植物安全性检查功能
    """
    print("\n测试4: Agent植物安全性检查")

    agent = PlantCatAgent()

    # 测试检查有毒植物
    response = agent.check_plant_safety("绿萝")
    assert "警告" in response, "有毒植物的响应应该包含警告"
    assert "绿萝" in response, "响应应该包含植物名称"
    print("   ✅ 有毒植物检查测试通过")

    # 测试检查安全植物
    response = agent.check_plant_safety("吊兰")
    assert "安全" in response, "安全植物的响应应该包含安全"
    assert "吊兰" in response, "响应应该包含植物名称"
    print("   ✅ 安全植物检查测试通过")

    # 测试检查不存在的植物
    response = agent.check_plant_safety("不存在的植物")
    assert "抱歉" in response, "不存在植物的响应应该包含抱歉"
    assert "没有找到" in response, "响应应该提示未找到"
    print("   ✅ 不存在植物检查测试通过")


def test_agent_command_processing():
    """
    测试Agent的命令处理功能
    """
    print("\n测试5: Agent命令处理")

    agent = PlantCatAgent()

    # 测试帮助命令
    response = agent.process_command("help")
    assert "使用说明" in response, "帮助命令应该返回使用说明"
    print("   ✅ 帮助命令测试通过")

    # 测试列表命令
    response = agent.process_command("list")
    assert "所有植物" in response, "列表命令应该返回所有植物"
    print("   ✅ 列表命令测试通过")

    # 测试安全植物命令
    response = agent.process_command("safe")
    assert "安全植物" in response, "安全命令应该返回安全植物"
    print("   ✅ 安全植物命令测试通过")

    # 测试有毒植物命令
    response = agent.process_command("toxic")
    assert "有毒植物" in response, "有毒命令应该返回有毒植物"
    print("   ✅ 有毒植物命令测试通过")

    # 测试历史命令
    response = agent.process_command("history")
    assert "对话历史" in response, "历史命令应该返回对话历史"
    print("   ✅ 历史命令测试通过")

    # 测试退出命令
    response = agent.process_command("exit")
    assert response is None, "退出命令应该返回None"
    print("   ✅ 退出命令测试通过")


def test_conversation_history():
    """
    测试对话历史记录功能
    """
    print("\n测试6: 对话历史记录")

    agent = PlantCatAgent()

    # 初始历史应该为空
    assert len(agent.conversation_history) == 0, "初始历史应该为空"
    print("   ✅ 初始历史为空测试通过")

    # 执行几次查询
    agent.check_plant_safety("绿萝")
    agent.check_plant_safety("吊兰")

    # 检查历史记录
    assert len(agent.conversation_history) == 2, "应该有2条历史记录"
    assert agent.conversation_history[0]['user'] == '绿萝', "第一条记录的用户输入应该是绿萝"
    assert agent.conversation_history[1]['user'] == '吊兰', "第二条记录的用户输入应该是吊兰"
    print("   ✅ 对话历史记录测试通过")


def test_case_insensitive_search():
    """
    测试不区分大小写的搜索
    """
    print("\n测试7: 不区分大小写的搜索")

    # 测试大写查询
    plant_info = get_plant_info("LILY")
    # 注意：因为我们的数据库是中文，所以这个测试应该找不到
    # 如果要支持英文搜索，需要在数据库中添加英文名称

    # 测试中文大小写（中文没有大小写，但可以测试不同格式）
    plant_info = get_plant_info(" 绿萝 ")
    assert plant_info is not None, "应该能去除空格找到植物"
    assert plant_info['name'] == "绿萝", "植物名称应该正确"
    print("   ✅ 空格处理测试通过")


def run_all_tests():
    """
    运行所有测试函数
    """
    print("=" * 60)
    print("🧪 开始运行AI Agent单元测试")
    print("=" * 60)

    try:
        # 依次运行所有测试
        test_plant_database_query()
        test_safe_and_toxic_lists()
        test_agent_initialization()
        test_agent_plant_safety_check()
        test_agent_command_processing()
        test_conversation_history()
        test_case_insensitive_search()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！程序运行正常。")
        print("=" * 60)

        return True

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        print("=" * 60)
        return False

    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        print("=" * 60)
        return False


# 程序入口点
if __name__ == "__main__":
    """
    当直接运行这个测试文件时，执行以下代码
    """
    success = run_all_tests()

    # 根据测试结果设置退出码
    # 0 表示成功，1 表示失败
    sys.exit(0 if success else 1)