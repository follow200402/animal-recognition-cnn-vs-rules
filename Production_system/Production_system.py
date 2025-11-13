"""
动物识别产生式系统 - 基于 Animals-10 数据集
利用 rule_base.py 中定义的规则与知识库进行推理
"""

from rules_base import get_rules, get_all_animals, get_animal_knowledge

# 取出规则
RULES = get_rules()

# ==========================================================
# 推理引擎类
# ==========================================================
class InferenceEngine:
    def __init__(self, rules):
        self.rules = rules
        self.facts = {}  # 当前事实（特征）
        self.derived_facts = {}  # 推理得到的事实

    def add_fact(self, key, value=True):
        """添加事实"""
        self.facts[key] = value

    def match_rule(self, rule):
        """判断当前事实是否满足某条规则"""
        for key, val in rule.conditions.items():
            if key not in self.facts and key not in self.derived_facts:
                return False
            fact_val = self.facts.get(key, self.derived_facts.get(key))
            if fact_val != val:
                return False
        return True

    def infer(self):
        """执行前向推理"""
        applied_rules = []
        updated = True

        while updated:
            updated = False
            for rule in self.rules:
                if rule.rule_id in applied_rules:
                    continue
                if self.match_rule(rule):
                    # 应用规则
                    self.derived_facts.update(rule.conclusion)
                    applied_rules.append(rule.rule_id)
                    print(f"✅ 触发规则 {rule.rule_id}: {rule.description}")
                    updated = True

        return applied_rules

    def get_result(self):
        """输出推理结果"""
        name = self.derived_facts.get("动物名称", "未知动物")
        category = self.derived_facts.get("大类", "")
        subcat = self.derived_facts.get("亚类", "")
        return name, category, subcat


# ==========================================================
# 用户交互界面
# ==========================================================
def interactive_mode():
    print("=== 🧠 动物识别产生式系统（Animals-10） ===\n")

    # 加载所有动物及其特征
    all_animals = get_all_animals()
    print(f"系统知识库包含 {len(all_animals)} 种动物：{', '.join(all_animals)}\n")

    # 提取所有可能的特征
    all_features = set()
    for rule in RULES:
        all_features.update(rule.conditions.keys())
    all_features = sorted(all_features)

    print("可选择的特征：")
    for i, f in enumerate(all_features, 1):
        print(f"{i:2d}: {f}", end="  ")
        if i % 5 == 0:
            print()
    print("\n(请输入特征编号，每行一个，空行结束)\n")

    # 用户输入特征
    engine = InferenceEngine(RULES)
    while True:
        line = input("特征编号: ").strip()
        if not line:
            break
        try:
            idx = int(line)
            if 1 <= idx <= len(all_features):
                feature = all_features[idx - 1]
                engine.add_fact(feature, True)
                print(f"✅ 添加特征: {feature}")
            else:
                print("⚠️ 无效编号")
        except ValueError:
            print("⚠️ 请输入数字编号")

    # 执行推理
    print("\n🧩 开始推理...\n")
    engine.infer()

    # 输出结果
    animal, category, subcat = engine.get_result()
    print("\n🐾 推理结果：")
    print(f"  ➤ 动物名称: {animal}")
    print(f"  ➤ 大类: {category}")
    if subcat:
        print(f"  ➤ 亚类: {subcat}")

    # 如果推理出动物，展示知识
    if animal != "未知动物":
        knowledge = get_animal_knowledge(animal)
        if knowledge:
            print("\n📚 动物知识摘要：")
            print(f"大类: {knowledge.get('大类')}")
            print(f"亚类: {knowledge.get('亚类')}")
            print("特征:", "、".join(knowledge.get("特征", [])))
            print("外观:", "、".join(knowledge.get("外观", [])))
            print("习性:", "、".join(knowledge.get("习性", [])))
    else:
        print("\n❌ 未能推断出动物，请提供更多特征。")


# ==========================================================
# 程序入口
# ==========================================================
if __name__ == "__main__":
    interactive_mode()
