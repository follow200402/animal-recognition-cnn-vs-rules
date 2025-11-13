import torch
import torch.nn as nn
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# ======================================================
# 配置部分
# ======================================================
data_dir = "./split_dataset/test"       # 测试集路径（文件夹结构应为 data/test/猫, data/test/狗 ...）
model_path = "./best_resnet50.pth" # 训练保存的模型路径
batch_size = 8
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ======================================================
# 数据预处理
# ======================================================
test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

test_dataset = datasets.ImageFolder(root=data_dir, transform=test_transforms)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

class_names = test_dataset.classes
print("📁 检测到的类别：", class_names)

# ======================================================
# 加载模型
# ======================================================
model = models.resnet50(pretrained=False)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))
model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# ======================================================
# 测试过程
# ======================================================
all_preds = []
all_labels = []
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

        correct += torch.sum(preds == labels).item()
        total += labels.size(0)

# ======================================================
# 结果输出
# ======================================================
accuracy = correct / total
print(f"\n🎯 测试集总体准确率: {accuracy * 100:.2f}%")
print("\n📊 分类详细报告：")
report = classification_report(all_labels, all_preds, target_names=class_names)
print(report)

# 保存分类报告
report_path = "classification_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)

print(f"✅ 分类报告已保存为: {report_path}")
# ======================================================
# 混淆矩阵可视化
# ======================================================
cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel("Predicted Class")
plt.ylabel("True Class")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")  # 保存图像文件
print("✅ 混淆矩阵已保存为 confusion_matrix.png")
