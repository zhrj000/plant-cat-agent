"""
植物数据库模块
这个模块包含了植物及其对猫毒性信息的数据库
"""

# 定义一个植物数据库字典
# 键是植物的名称（小写）
# 值是一个字典，包含植物的详细信息和毒性状态
PLANT_DATABASE = {
    "绿萝": {
        "name": "绿萝",
        "scientific_name": "Epipremnum aureum",  # 学名
        "toxic_to_cats": True,  # 对猫有毒
        "toxicity_level": "中等",  # 毒性等级
        "symptoms": "口腔刺激、呕吐、吞咽困难",  # 中毒症状
        "toxic_parts": "全株",  # 有毒部位
        "description": "绿萝是非常常见的室内植物，但对猫有毒性"  # 描述
    },
    "吊兰": {
        "name": "吊兰",
        "scientific_name": "Chlorophytum comosum",
        "toxic_to_cats": False,  # 对猫无毒
        "toxicity_level": "无毒",
        "symptoms": "无",
        "toxic_parts": "无",
        "description": "吊兰是对猫完全安全的植物，非常适合有猫的家庭"
    },
    "百合": {
        "name": "百合",
        "scientific_name": "Lilium",
        "toxic_to_cats": True,
        "toxicity_level": "极高",  # 非常危险
        "symptoms": "急性肾衰竭、呕吐、嗜睡、食欲不振",
        "toxic_parts": "花粉、叶子、茎、花（全株都有毒）",
        "description": "百合对猫极度危险，即使是少量摄入也可能致命！"
    },
    "仙人掌": {
        "name": "仙人掌",
        "scientific_name": "Cactaceae",
        "toxic_to_cats": False,
        "toxicity_level": "无毒",
        "symptoms": "可能被刺扎伤",
        "toxic_parts": "刺",
        "description": "仙人掌本身无毒，但要注意刺可能伤害到猫"
    },
    "芦荟": {
        "name": "芦荟",
        "scientific_name": "Aloe vera",
        "toxic_to_cats": True,
        "toxicity_level": "轻微",
        "symptoms": "呕吐、腹泻、嗜睡",
        "toxic_parts": "汁液",
        "description": "芦荟对猫有轻微毒性，不适合放在猫能接触到的地方"
    },
    "虎尾兰": {
        "name": "虎尾兰",
        "scientific_name": "Sansevieria trifasciata",
        "toxic_to_cats": True,
        "toxicity_level": "轻微到中等",
        "symptoms": "恶心、呕吐、腹泻",
        "toxic_parts": "全株",
        "description": "虎尾兰对猫有轻微到中等毒性"
    },
    "薄荷": {
        "name": "薄荷",
        "scientific_name": "Mentha",
        "toxic_to_cats": True,
        "toxicity_level": "轻微",
        "symptoms": "呕吐、腹泻",
        "toxic_parts": "叶子",
        "description": "薄荷对猫有轻微毒性"
    },
    "猫咪草": {
        "name": "猫咪草",
        "scientific_name": "Dactylis glomerata",
        "toxic_to_cats": False,
        "toxicity_level": "无毒",
        "symptoms": "无",
        "toxic_parts": "无",
        "description": "猫咪草是专门为猫种植的，完全安全且对猫有益"
    },
    "文竹": {
        "name": "文竹",
        "scientific_name": "Asparagus setaceus",
        "toxic_to_cats": False,
        "toxicity_level": "无毒",
        "symptoms": "无",
        "toxic_parts": "无",
        "description": "文竹是对猫安全的植物"
    },
    "发财树": {
        "name": "发财树",
        "scientific_name": "Pachira glabra",
        "toxic_to_cats": False,
        "toxicity_level": "无毒",
        "symptoms": "无",
        "toxic_parts": "无",
        "description": "发财树是对猫安全的植物"
    },
    "龟背竹": {
        "name": "龟背竹",
        "scientific_name": "Monstera deliciosa",
        "toxic_to_cats": True,
        "toxicity_level": "中等",
        "symptoms": "口腔刺激、吞咽困难、呕吐",
        "toxic_parts": "全株",
        "description": "龟背竹对猫有毒性"
    },
    "水仙": {
        "name": "水仙",
        "scientific_name": "Narcissus",
        "toxic_to_cats": True,
        "toxicity_level": "高",
        "symptoms": "呕吐、腹泻、腹痛、抽搐",
        "toxic_parts": "鳞茎（根部）",
        "description": "水仙对猫有高毒性，特别是鳞茎部分"
    }
}


def get_plant_info(plant_name):
    """
    根据植物名称获取植物信息

    参数:
        plant_name (str): 植物名称

    返回:
        dict: 如果找到植物则返回植物信息字典，否则返回None
    """
    # 将输入的植物名称转为小写，用于匹配
    plant_name_lower = plant_name.strip().lower()

    # 尝试在数据库中查找植物
    # 先尝试精确匹配
    for db_name, plant_info in PLANT_DATABASE.items():
        if db_name.lower() == plant_name_lower:
            return plant_info

    # 如果没有精确匹配，尝试模糊匹配（包含关系）
    for db_name, plant_info in PLANT_DATABASE.items():
        if plant_name_lower in db_name.lower() or db_name.lower() in plant_name_lower:
            return plant_info

    # 都没找到，返回None
    return None


def get_all_plant_names():
    """
    获取数据库中所有植物的名称列表

    返回:
        list: 植物名称列表
    """
    # 返回所有植物名称的列表
    return list(PLANT_DATABASE.keys())


def get_safe_plants():
    """
    获取所有对猫安全的植物列表

    返回:
        list: 安全植物名称列表
    """
    # 列表推导式：筛选出toxic_to_cats为False的植物
    return [plant_info['name'] for plant_info in PLANT_DATABASE.values() if not plant_info['toxic_to_cats']]


def get_toxic_plants():
    """
    获取所有对猫有毒的植物列表

    返回:
        list: 有毒植物名称列表
    """
    # 列表推导式：筛选出toxic_to_cats为True的植物
    return [plant_info['name'] for plant_info in PLANT_DATABASE.values() if plant_info['toxic_to_cats']]