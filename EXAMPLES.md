# 使用示例和演示

## 🎬 完整使用演示

### 场景1：新手养猫，想养植物

```
用户：我刚开始养猫，想在家里养点植物，听说绿萝很好养，能养吗？

Agent交互：
👤 请输入植物名称或命令: 绿萝

⚠️ 警告：【绿萝】对猫有中等毒性！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌿 学名: Epipremnum aureum
📝 描述: 绿萝是非常常见的室内植物，但对猫有毒性
☠️ 毒性等级: 中等
🏥 中毒症状: 口腔刺激、呕吐、吞咽困难
🍃 有毒部位: 全株
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 建议:
   1. ❌ 不要在有猫的家庭种植此植物
   2. 如果猫误食，立即带去兽医处
   3. 将现有植物移到猫无法接触的地方
   4. 建议选择对猫安全的替代植物

用户：那有什么植物是对猫安全的呢？

👤 请输入植物名称或命令: safe

✅ 对猫安全的植物推荐:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌿 吊兰
   吊兰是对猫完全安全的植物，非常适合有猫的家庭

🌿 仙人掌
   仙人掌是对猫完全安全的植物，但要注意刺可能伤害到猫

🌿 猫咪草
   猫咪草是专门为猫种植的，完全安全且对猫有益

🌿 文竹
   文竹是对猫安全的植物

🌿 发财树
   发财树是对猫安全的植物

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 共 5 种安全植物
```

---

### 场景2：发现家里有百合花

```
用户：我家里刚买了一束百合花，听说对猫不好？

👤 请输入植物名称或命令: 百合

⚠️ 警告：【百合】对猫有极高毒性！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌿 学名: Lilium
📝 描述: 百合对猫极度危险，即使是少量摄入也可能致命！
☠️ 毒性等级: 极高
🏥 中毒症状: 急性肾衰竭、呕吐、嗜睡、食欲不振
🍃 有毒部位: 花粉、叶子、茎、花（全株都有毒）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 建议:
   1. ❌ 不要在有猫的家庭种植此植物
   2. 如果猫误食，立即带去兽医处
   3. 将现有植物移到猫无法接触的地方
   4. 建议选择对猫安全的替代植物

用户：天哪，太危险了！我赶紧把花扔掉！
```

---

### 场景3：批量检查植物清单

```
用户：我想查看数据库里所有的植物

👤 请输入植物名称或命令: list

📋 数据库中的所有植物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 对猫安全的植物:
   ✅ 仙人掌
   ✅ 吊兰
   ✅ 发财树
   ✅ 吊兰
   ✅ 文竹
   ✅ 猫咪草

⚠️ 对猫有毒的植物:
   ⚠️ 百合
   ⚠️ 虎尾兰
   ⚠️ 水仙
   ⚠️ 绿萝
   ⚠️ 龟背竹
   ⚠️ 芦荟
   ⚠️ 薄荷

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 统计: 共 12 种植物（安全: 5 种，有毒: 7 种）
```

---

### 场景4：查看对话历史

```
用户：我刚才都查询了哪些植物？

👤 请输入植物名称或命令: history

📝 对话历史记录:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第 1 次对话】2026-03-08 10:30:15
👤 用户: 绿萝
🤖 Agent: ⚠️ 警告：【绿萝】对猫有中等毒性！...

【第 2 次对话】2026-03-08 10:31:22
👤 用户: safe
🤖 Agent: ✅ 对猫安全的植物推荐:...

【第 3 次对话】2026-03-08 10:35:45
👤 用户: 百合
🤖 Agent: ⚠️ 警告：【百合】对猫有极高毒性！...

【第 4 次对话】2026-03-08 10:40:10
👤 用户: list
🤖 Agent: 📋 数据库中的所有植物:...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎓 编程学习示例

### 示例1：查询不存在的植物

```python
# 在 Python 交互式环境中
>>> from plant_cat_agent import PlantCatAgent
>>> agent = PlantCatAgent()
>>> result = agent.check_plant_safety("不存在的植物")
>>> print(result)

❌ 抱歉，数据库中没有找到【不存在的植物】的信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 建议:
   1. 检查植物名称是否正确
   2. 输入"list"查看所有可用植物
   3. 输入"safe"查看所有对猫安全的植物
```

### 示例2：获取安全植物列表

```python
>>> from data import get_safe_plants
>>> safe_plants = get_safe_plants()
>>> print(safe_plants)

['吊兰', '仙人掌', '猫咪草', '文竹', '发财树']
```

### 示例3：检查特定植物

```python
>>> from data import get_plant_info
>>> plant = get_plant_info("绿萝")
>>> print(plant['toxic_to_cats'])

True
>>> print(plant['toxicity_level'])

中等
```

---

## 🔧 代码修改示例

### 示例1：修改输出颜色

在 `plant_cat_agent.py` 中修改：

```python
# 原来的代码
response = f"⚠️ 警告：【{plant_info['name']}】对猫有{plant_info['toxicity_level']}毒性！"

# 修改为（增加颜色标识）
response = f"🔴 危险：【{plant_info['name']}】对猫有{plant_info['toxicity_level']}毒性！"
```

### 示例2：添加新植物

在 `data/plant_database.py` 中添加：

```python
PLANT_DATABASE = {
    # ... 其他植物

    "玫瑰": {
        "name": "玫瑰",
        "scientific_name": "Rosa",
        "toxic_to_cats": False,
        "toxicity_level": "无毒",
        "symptoms": "可能被刺扎伤",
        "toxic_parts": "刺",
        "description": "玫瑰对猫无毒，但要注意刺可能伤害到猫"
    },
}
```

### 示例3：添加新的命令

在 `plant_cat_agent.py` 的 `process_command` 方法中添加：

```python
def process_command(self, command):
    # ... 现有命令处理

    elif command_lower in ['rose', '玫瑰']:
        # 新增：推荐玫瑰作为替代植物
        response = """
🌹 玫瑰推荐:
玫瑰是对猫无毒的美丽植物，但要注意：
- 避免猫被刺扎伤
- 定期修剪和护理
        """

    # ... 其他命令
```

---

## 🧪 测试示例

### 运行所有测试

```bash
$ python tests/test_agent.py

============================================================
🧪 开始运行AI Agent单元测试
============================================================
测试1: 数据库查询功能
   ✅ 精确匹配测试通过
   ✅ 模糊匹配测试通过
   ✅ 不存在植物查询测试通过

测试2: 安全植物和有毒植物列表
   ✅ 安全植物列表测试通过（共5种）
   ✅ 有毒植物列表测试通过（共7种）

...

============================================================
✅ 所有测试通过！程序运行正常。
============================================================
```

### 单独测试某个功能

```python
# 在 Python 交互式环境中测试
>>> from data import get_plant_info
>>> plant = get_plant_info("百合")
>>> assert plant['toxic_to_cats'] == True
>>> assert plant['toxicity_level'] == "极高"
>>> print("测试通过！")
测试通过！
```

---

## 📊 数据统计示例

### 统计各类植物数量

```python
from data import PLANT_DATABASE

# 统计有毒和无毒植物
toxic_count = sum(1 for plant in PLANT_DATABASE.values() if plant['toxic_to_cats'])
safe_count = len(PLANT_DATABASE) - toxic_count

print(f"总植物数: {len(PLANT_DATABASE)}")
print(f"有毒植物: {toxic_count}")
print(f"安全植物: {safe_count}")
print(f"有毒比例: {toxic_count/len(PLANT_DATABASE)*100:.1f}%")
```

输出：
```
总植物数: 12
有毒植物: 7
安全植物: 5
有毒比例: 58.3%
```

---

## 🎯 实际应用场景

### 场景1：宠物店老板

```python
# 宠物店老板的查询清单
plants_to_check = ["绿萝", "吊兰", "百合", "发财树", "虎尾兰"]

from plant_cat_agent import PlantCatAgent
agent = PlantCatAgent()

for plant in plants_to_check:
    print(agent.check_plant_safety(plant))
    print("\n" + "="*50 + "\n")
```

### 场景2：家庭装修顾问

```python
# 根据房间类型推荐植物
def recommend_plants_for_room(room_type):
    from data import get_safe_plants
    safe_plants = get_safe_plants()

    if room_type == "客厅":
        return ["发财树", "文竹"]  # 大型植物
    elif room_type == "卧室":
        return ["吊兰", "仙人掌"]  # 小型植物
    else:
        return safe_plants  # 返回所有安全植物

print("客厅推荐植物:", recommend_plants_for_room("客厅"))
print("卧室推荐植物:", recommend_plants_for_room("卧室"))
```

---

## 💡 高级使用技巧

### 技巧1：批量查询并生成报告

```python
def generate_safety_report(plant_list):
    from data import get_plant_info

    report = "📋 植物安全性报告\n"
    report += "=" * 50 + "\n\n"

    for plant_name in plant_list:
        plant = get_plant_info(plant_name)
        if plant:
            status = "❌ 有毒" if plant['toxic_to_cats'] else "✅ 安全"
            report += f"{status} {plant_name}: {plant['description']}\n"
        else:
            report += f"⚠️ 未找到: {plant_name}\n"

    return report

print(generate_safety_report(["绿萝", "吊兰", "玫瑰", "百合"]))
```

### 技巧2：保存对话历史

```python
def save_conversation_to_file(agent, filename="conversation_history.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for conv in agent.conversation_history:
            f.write(f"时间: {conv['timestamp']}\n")
            f.write(f"用户: {conv['user']}\n")
            f.write(f"Agent: {conv['agent'][:100]}...\n")
            f.write("-" * 50 + "\n\n")

# 使用
agent = PlantCatAgent()
agent.check_plant_safety("绿萝")
save_conversation_to_file(agent)
```

---

## 🎨 自定义输出格式示例

### 创建简单的HTML报告

```python
def create_html_report(plant_name):
    from data import get_plant_info

    plant = get_plant_info(plant_name)
    if not plant:
        return "<html><body><h1>未找到植物</h1></body></html>"

    status_color = "red" if plant['toxic_to_cats'] else "green"
    status_text = "有毒" if plant['toxic_to_cats'] else "安全"

    html = f"""
    <html>
    <head>
        <title>{plant_name} 毒性报告</title>
    </head>
    <body>
        <h1 style="color: {status_color}">{status_text}</h1>
        <p><strong>学名:</strong> {plant['scientific_name']}</p>
        <p><strong>毒性等级:</strong> {plant['toxicity_level']}</p>
        <p><strong>中毒症状:</strong> {plant['symptoms']}</p>
        <p><strong>描述:</strong> {plant['description']}</p>
    </body>
    </html>
    """

    return html

# 使用
print(create_html_report("绿萝"))
```

---

## 🚀 扩展项目示例

### 示例1：添加多语言支持

```python
# 在 data/plant_database.py 中添加
PLANT_DATABASE = {
    "绿萝": {
        # ... 中文信息
        "name_en": "Pothos",  # 英文名
        "description_en": "Pothos is toxic to cats"
    },
}

# 修改查询函数支持英文
def get_plant_info(plant_name):
    # 支持中文和英文查询
    # ... 实现逻辑
```

### 示例2：添加用户评分系统

```python
# 保存用户偏好
class PlantCatAgent:
    def __init__(self):
        self.user_preferences = {}  # 用户偏好字典

    def rate_plant(self, plant_name, rating):
        """用户对植物评分（1-5分）"""
        self.user_preferences[plant_name] = rating
        return f"已记录：{plant_name} 评分 {rating} 分"

    def get_recommended_plants(self):
        """获取用户评分高的植物"""
        if not self.user_preferences:
            return "暂无评分记录"

        # 按评分排序
        sorted_plants = sorted(
            self.user_preferences.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return "推荐植物：\n" + "\n".join(
            f"⭐ {plant} - {rating}分"
            for plant, rating in sorted_plants[:5]
        )
```

---

## 📝 总结

这些示例展示了如何：
1. ✅ 使用Agent进行日常查询
2. ✅ 通过代码调用Agent功能
3. ✅ 修改和扩展Agent
4. ✅ 编写测试验证功能
5. ✅ 创建实际应用

希望这些示例能帮助你更好地理解和使用这个AI Agent项目！

继续探索，发挥你的创意！🎉
