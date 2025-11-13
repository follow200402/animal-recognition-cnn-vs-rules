"""
产生式规则定义模块 - Animals-10 版本
定义动物识别的规则集合，适配 Kaggle Animals-10 数据集
"""

class Rule:
    """产生式规则类"""
    def __init__(self, rule_id, conditions, conclusion, description=""):
        self.rule_id = rule_id
        self.conditions = conditions  # 条件列表
        self.conclusion = conclusion  # 结论字典 {属性: 值}
        self.description = description
    
    def __repr__(self):
        return f"Rule {self.rule_id}: {self.description}"


# 定义所有规则 - 适配 Animals-10 数据集（10种动物）
RULES = [
    # 一级分类规则：区分大类
    
    # R1-R4: 哺乳动物识别
    Rule(
        rule_id="R1",
        conditions={"有毛发": True},
        conclusion={"大类": "哺乳动物"},
        description="若该动物有毛发，那么它是哺乳动物"
    ),
    Rule(
        rule_id="R2",
        conditions={"能产乳": True},
        conclusion={"大类": "哺乳动物"},
        description="若该动物能产乳，那么它是哺乳动物"
    ),
    Rule(
        rule_id="R3",
        conditions={"四条腿": True, "温血": True, "胎生": True},
        conclusion={"大类": "哺乳动物"},
        description="若该动物四条腿、温血、胎生，那么它是哺乳动物"
    ),
    
    # R5-R7: 鸟类识别
    Rule(
        rule_id="R5",
        conditions={"有羽毛": True},
        conclusion={"大类": "鸟类"},
        description="若该动物有羽毛，那么它是鸟类"
    ),
    Rule(
        rule_id="R6",
        conditions={"能生蛋": True, "有喙": True},
        conclusion={"大类": "鸟类"},
        description="若该动物能生蛋、有喙，那么它是鸟类"
    ),
    
    # R8-R9: 昆虫识别
    Rule(
        rule_id="R8",
        conditions={"有外骨骼": True, "六条腿": True},
        conclusion={"大类": "昆虫"},
        description="若该动物有外骨骼、六条腿，那么它是昆虫"
    ),
    
    # R10-R11: 节肢动物识别
    Rule(
        rule_id="R10",
        conditions={"有外骨骼": True, "八条腿": True},
        conclusion={"大类": "节肢动物", "亚类": "蛛形纲"},
        description="若该动物有外骨骼、八条腿，那么它是蛛形纲节肢动物"
    ),
    
    # 二级分类规则：哺乳动物细分
    
    # R12-R14: 宠物类
    Rule(
        rule_id="R12",
        conditions={"大类": "哺乳动物", "驯化": True, "吠叫": True, "忠诚": True},
        conclusion={"亚类": "犬科", "动物名称": "狗"},
        description="若是哺乳动物，能吠叫、忠诚、被驯化，那么它是狗"
    ),
    Rule(
        rule_id="R13",
        conditions={"大类": "哺乳动物", "驯化": True, "喵叫": True, "爱干净": True},
        conclusion={"亚类": "猫科", "动物名称": "猫"},
        description="若是哺乳动物，能喵叫、爱干净、被驯化，那么它是猫"
    ),
    
    # R15-R17: 农场动物
    Rule(
        rule_id="R15",
        conditions={"大类": "哺乳动物", "长有蹄": True, "能骑乘": True, "有鬃毛": True},
        conclusion={"亚类": "马科", "动物名称": "马"},
        description="若是哺乳动物，有蹄、能骑乘、有鬃毛，那么它是马"
    ),
    Rule(
        rule_id="R16",
        conditions={"大类": "哺乳动物", "长有蹄": True, "产奶": True, "有角": True},
        conclusion={"亚类": "牛科", "动物名称": "牛"},
        description="若是哺乳动物，有蹄、产奶、有角，那么它是牛"
    ),
    Rule(
        rule_id="R17",
        conditions={"大类": "哺乳动物", "长有蹄": True, "有羊毛": True, "温顺": True},
        conclusion={"亚类": "羊科", "动物名称": "羊"},
        description="若是哺乳动物，有蹄、有羊毛、温顺，那么它是羊"
    ),
    
    # R18-R20: 野生动物
    Rule(
        rule_id="R18",
        conditions={"大类": "哺乳动物", "体型巨大": True, "长鼻子": True, "长象牙": True},
        conclusion={"亚类": "象科", "动物名称": "大象"},
        description="若是哺乳动物，体型巨大、长鼻子、长象牙，那么它是大象"
    ),
    Rule(
        rule_id="R19",
        conditions={"大类": "哺乳动物", "体型小": True, "蓬松尾巴": True, "爬树": True, "吃坚果": True},
        conclusion={"亚类": "松鼠科", "动物名称": "松鼠"},
        description="若是哺乳动物，体型小、蓬松尾巴、爬树、吃坚果，那么它是松鼠"
    ),
    
    # 三级分类规则：鸟类细分
    
    # R21: 家禽
    Rule(
        rule_id="R21",
        conditions={"大类": "鸟类", "驯化": True, "下蛋": True, "咯咯叫": True},
        conclusion={"亚类": "家禽", "动物名称": "鸡"},
        description="若是鸟类，被驯化、下蛋、咯咯叫，那么它是鸡"
    ),
    
    # 四级分类规则：昆虫细分
    
    # R22-R23: 蝴蝶
    Rule(
        rule_id="R22",
        conditions={"大类": "昆虫", "有翅膀": True, "色彩鲜艳": True, "采花蜜": True},
        conclusion={"亚类": "鳞翅目", "动物名称": "蝴蝶"},
        description="若是昆虫，有翅膀、色彩鲜艳、采花蜜，那么它是蝴蝶"
    ),
    Rule(
        rule_id="R23",
        conditions={"大类": "昆虫", "有四个翅膀": True, "有触角": True, "经历蛹期": True},
        conclusion={"亚类": "鳞翅目", "动物名称": "蝴蝶"},
        description="若是昆虫，四个翅膀、有触角、经历蛹期，那么它是蝴蝶"
    ),
    
    # 五级分类规则：节肢动物细分
    
    # R24-R25: 蜘蛛
    Rule(
        rule_id="R24",
        conditions={"大类": "节肢动物", "亚类": "蛛形纲", "会织网": True},
        conclusion={"动物名称": "蜘蛛"},
        description="若是蛛形纲节肢动物，会织网，那么它是蜘蛛"
    ),
    Rule(
        rule_id="R25",
        conditions={"八条腿": True, "会织网": True, "捕食昆虫": True},
        conclusion={"大类": "节肢动物", "亚类": "蛛形纲", "动物名称": "蜘蛛"},
        description="若有八条腿、会织网、捕食昆虫，那么它是蜘蛛"
    ),
    
    # 额外的辅助规则（基于外观特征）
    
    # R26-R35: 基于颜色和体型的辅助规则
    Rule(
        rule_id="R26",
        conditions={"毛发颜色": "棕色", "中等体型": True, "忠诚": True},
        conclusion={"动物名称": "狗"},
        description="基于外观：棕色毛发、中等体型、忠诚 -> 狗"
    ),
    Rule(
        rule_id="R27",
        conditions={"毛发颜色": "灰色", "体型小": True, "独立性强": True},
        conclusion={"动物名称": "猫"},
        description="基于外观：灰色毛发、小体型、独立 -> 猫"
    ),
    Rule(
        rule_id="R28",
        conditions={"毛发颜色": "棕色", "有鬃毛": True, "体型大": True},
        conclusion={"动物名称": "马"},
        description="基于外观：棕色、有鬃毛、大体型 -> 马"
    ),
    Rule(
        rule_id="R29",
        conditions={"有黑白花纹": True, "体型大": True, "产奶": True},
        conclusion={"动物名称": "牛"},
        description="基于外观：黑白花纹、大体型、产奶 -> 牛"
    ),
    Rule(
        rule_id="R30",
        conditions={"毛发颜色": "白色", "毛茸茸": True, "温顺": True},
        conclusion={"动物名称": "羊"},
        description="基于外观：白色、毛茸茸、温顺 -> 羊"
    ),
    Rule(
        rule_id="R31",
        conditions={"颜色": "灰色", "体型巨大": True, "长鼻子": True},
        conclusion={"动物名称": "大象"},
        description="基于外观：灰色、巨大、长鼻子 -> 大象"
    ),
    Rule(
        rule_id="R32",
        conditions={"翅膀颜色": "多彩", "体型小": True, "飞行": True},
        conclusion={"动物名称": "蝴蝶"},
        description="基于外观：多彩翅膀、小体型、飞行 -> 蝴蝶"
    ),
    Rule(
        rule_id="R33",
        conditions={"羽毛颜色": "白色或棕色", "下蛋": True, "咯咯叫": True},
        conclusion={"动物名称": "鸡"},
        description="基于外观：白/棕色羽毛、下蛋、咯咯叫 -> 鸡"
    ),
    Rule(
        rule_id="R34",
        conditions={"颜色": "黑色或棕色", "八条腿": True, "小体型": True},
        conclusion={"动物名称": "蜘蛛"},
        description="基于外观：黑/棕色、八条腿、小体型 -> 蜘蛛"
    ),
    Rule(
        rule_id="R35",
        conditions={"毛发颜色": "灰色或棕色", "蓬松尾巴": True, "爬树": True},
        conclusion={"动物名称": "松鼠"},
        description="基于外观：灰/棕色、蓬松尾巴、爬树 -> 松鼠"
    ),
]


# 动物知识库模板
ANIMAL_KNOWLEDGE_BASE = {
    "狗": {
        "大类": "哺乳动物",
        "亚类": "犬科",
        "特征": ["有毛发", "四条腿", "温血", "胎生", "驯化", "吠叫", "忠诚"],
        "外观": ["中等体型", "毛发颜色多样"],
        "习性": ["社交性强", "保护领地", "嗅觉灵敏"]
    },
    "猫": {
        "大类": "哺乳动物",
        "亚类": "猫科",
        "特征": ["有毛发", "四条腿", "温血", "胎生", "驯化", "喵叫", "爱干净"],
        "外观": ["体型小", "柔软毛发", "灵活"],
        "习性": ["独立性强", "夜行性", "捕鼠"]
    },
    "马": {
        "大类": "哺乳动物",
        "亚类": "马科",
        "特征": ["有毛发", "四条腿", "温血", "长有蹄", "能骑乘", "有鬃毛"],
        "外观": ["体型大", "棕色或黑色", "长腿"],
        "习性": ["奔跑快", "群居", "食草"]
    },
    "牛": {
        "大类": "哺乳动物",
        "亚类": "牛科",
        "特征": ["有毛发", "四条腿", "温血", "长有蹄", "产奶", "有角"],
        "外观": ["体型大", "多为黑白花纹", "强壮"],
        "习性": ["反刍", "温顺", "食草"]
    },
    "羊": {
        "大类": "哺乳动物",
        "亚类": "羊科",
        "特征": ["有毛发", "四条腿", "温血", "长有蹄", "有羊毛", "温顺"],
        "外观": ["体型中等", "白色毛茸茸", "卷曲羊毛"],
        "习性": ["群居", "食草", "产毛"]
    },
    "大象": {
        "大类": "哺乳动物",
        "亚类": "象科",
        "特征": ["有毛发", "四条腿", "温血", "体型巨大", "长鼻子", "长象牙"],
        "外观": ["灰色", "巨大耳朵", "厚皮肤"],
        "习性": ["智商高", "群居", "记忆力强"]
    },
    "松鼠": {
        "大类": "哺乳动物",
        "亚类": "松鼠科",
        "特征": ["有毛发", "四条腿", "温血", "体型小", "蓬松尾巴", "爬树", "吃坚果"],
        "外观": ["灰色或棕色", "大尾巴", "敏捷"],
        "习性": ["储存食物", "跳跃", "树栖"]
    },
    "蝴蝶": {
        "大类": "昆虫",
        "亚类": "鳞翅目",
        "特征": ["有外骨骼", "六条腿", "有四个翅膀", "色彩鲜艳", "采花蜜", "有触角", "经历蛹期"],
        "外观": ["多彩翅膀", "体型小", "轻盈"],
        "习性": ["飞行", "传粉", "变态发育"]
    },
    "鸡": {
        "大类": "鸟类",
        "亚类": "家禽",
        "特征": ["有羽毛", "能生蛋", "有喙", "驯化", "下蛋", "咯咯叫"],
        "外观": ["白色或棕色羽毛", "红色鸡冠", "中等体型"],
        "习性": ["地面觅食", "群居", "产蛋"]
    },
    "蜘蛛": {
        "大类": "节肢动物",
        "亚类": "蛛形纲",
        "特征": ["有外骨骼", "八条腿", "会织网", "捕食昆虫"],
        "外观": ["黑色或棕色", "小体型", "多只眼睛"],
        "习性": ["织网", "捕食", "独居"]
    }
}


def get_rules():
    """获取所有规则"""
    return RULES


def get_animal_knowledge(animal_name):
    """获取特定动物的知识"""
    return ANIMAL_KNOWLEDGE_BASE.get(animal_name, {})


def get_all_animals():
    """获取所有动物名称"""
    return list(ANIMAL_KNOWLEDGE_BASE.keys())
