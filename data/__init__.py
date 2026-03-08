"""
数据模块初始化文件
这个文件让data目录成为一个Python包
"""

from .plant_database import (
    PLANT_DATABASE,
    get_plant_info,
    get_all_plant_names,
    get_safe_plants,
    get_toxic_plants
)

# 定义模块导出的内容
__all__ = [
    'PLANT_DATABASE',
    'get_plant_info',
    'get_all_plant_names',
    'get_safe_plants',
    'get_toxic_plants'
]