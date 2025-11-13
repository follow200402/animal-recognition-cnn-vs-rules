import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from tqdm import tqdm
import matplotlib.pyplot as plt

# ================================
# 1️⃣ 基本配置
# ================================
data_dir = "split_dataset"   # 数据集路径
num_classes = 10
batch_size = 8
num_epochs = 15
learning_rate = 1e-3
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ================================
# 2️⃣ 数据增强与加载
# ================================
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

train_dataset = datasets.ImageFolder(os.path.join(data_dir, "train"), transform=train_transforms)
val_dataset = datasets.ImageFolder(os.path.join(data_dir, "val"), transform=val_transforms)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

print(f"训练样本数: {len(train_dataset)}")
print(f"验证样本数: {len(val_dataset)}")
print(f"类别: {train_dataset.classes}")

# ================================
# 3️⃣ 模型定义 (ResNet50)
# ================================
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
in_features = model.fc.in_features
model.fc = nn.Linear(in_features, num_classes)
model = model.to(device)

# ================================
# 4️⃣ 损失函数与优化器
# ================================
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# ================================
# 5️⃣ 训练与验证
# ================================
train_losses, val_losses = [], []
train_accs, val_accs = [], []
best_val_acc = 0.0
best_epoch = 0

for epoch in range(num_epochs):
    print(f"\nEpoch [{epoch+1}/{num_epochs}]")
    model.train()
    train_loss, correct, total = 0.0, 0, 0

    for images, labels in tqdm(train_loader, desc="Training"):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    train_acc = 100 * correct / total
    train_loss = train_loss / total
    train_losses.append(train_loss)
    train_accs.append(train_acc)

    # 验证
    model.eval()
    val_loss, val_correct, val_total = 0.0, 0, 0

    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc="Validating"):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            val_total += labels.size(0)
            val_correct += predicted.eq(labels).sum().item()

    val_acc = 100 * val_correct / val_total
    val_loss = val_loss / val_total
    val_losses.append(val_loss)
    val_accs.append(val_acc)

    print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
    print(f"Val   Loss: {val_loss:.4f} | Val   Acc: {val_acc:.2f}%")

    # 保存最佳模型
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        best_epoch = epoch
        torch.save(model.state_dict(), "best_resnet50.pth")
        print("✅ 保存最佳模型！")

    scheduler.step()

print(f"\n🎯 训练完成！最佳验证准确率: {best_val_acc:.2f}% (Epoch {best_epoch+1})")

# ================================
# 6️⃣ 绘制训练曲线 + 标注最优点
# ================================
plt.figure(figsize=(12, 5))

# ---- Loss 曲线 ----
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss', marker='o')
plt.plot(val_losses, label='Val Loss', marker='o')
plt.axvline(x=best_epoch, color='r', linestyle='--', label=f'Best Epoch ({best_epoch+1})')
plt.scatter(best_epoch, val_losses[best_epoch], color='red', s=60, zorder=5)
plt.text(best_epoch, val_losses[best_epoch] + 0.01,
         f'Best={val_losses[best_epoch]:.3f}', color='red', fontsize=9)
plt.title('Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# ---- Accuracy 曲线 ----
plt.subplot(1, 2, 2)
plt.plot(train_accs, label='Train Acc', marker='o')
plt.plot(val_accs, label='Val Acc', marker='o')
plt.axvline(x=best_epoch, color='r', linestyle='--', label=f'Best Epoch ({best_epoch+1})')
plt.scatter(best_epoch, val_accs[best_epoch], color='red', s=60, zorder=5)
plt.text(best_epoch, val_accs[best_epoch] + 0.5,
         f'Best={val_accs[best_epoch]:.2f}%', color='red', fontsize=9)
plt.title('Accuracy Curve')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.legend()

plt.tight_layout()
plt.savefig('training_curves_annotated.png', dpi=300)
plt.show()

print("📈 已保存带标注的训练曲线：training_curves_annotated.png")
