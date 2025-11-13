import os
import shutil
import random
from glob import glob
from tqdm import tqdm

# ========== 配置部分 ==========
RAW_DIR = "data/raw-img"   # Kaggle 原始目录
OUTPUT_DIR = "split_dataset"          # 输出目录，用于训练脚本
SPLIT_RATIOS = (0.7, 0.15, 0.15)  # train / val / test 比例
SEED = 42                         # 随机种子，保证可重复
IMG_EXTENSIONS = (".jpg", ".jpeg", ".png")

random.seed(SEED)

# ========== 创建目标目录结构 ==========
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def make_subdirs(output_dir, classes):
    for split in ["train", "val", "test"]:
        for cls in classes:
            ensure_dir(os.path.join(output_dir, split, cls))

# ========== 主函数 ==========
def split_dataset(raw_dir=RAW_DIR, output_dir=OUTPUT_DIR, ratios=SPLIT_RATIOS):
    assert sum(ratios) == 1.0 or abs(sum(ratios) - 1.0) < 1e-6, "比例之和必须为1"
    classes = sorted([d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))])
    print(f"检测到类别: {classes}")
    make_subdirs(output_dir, classes)

    for cls in classes:
        cls_dir = os.path.join(raw_dir, cls)
        imgs = [f for f in glob(os.path.join(cls_dir, "*")) if f.lower().endswith(IMG_EXTENSIONS)]
        random.shuffle(imgs)

        n_total = len(imgs)
        n_train = int(ratios[0] * n_total)
        n_val = int(ratios[1] * n_total)

        splits = {
            "train": imgs[:n_train],
            "val": imgs[n_train:n_train + n_val],
            "test": imgs[n_train + n_val:]
        }

        print(f"\n[{cls}] 共 {n_total} 张 -> 训练: {len(splits['train'])}, 验证: {len(splits['val'])}, 测试: {len(splits['test'])}")

        # 拷贝文件
        for split, files in splits.items():
            for src_path in tqdm(files, desc=f"{cls}-{split}", leave=False):
                filename = os.path.basename(src_path)
                dst_path = os.path.join(output_dir, split, cls, filename)
                shutil.copy2(src_path, dst_path)

    print(f"\n✅ 数据集整理完成！输出路径：{os.path.abspath(output_dir)}")
    print("目录结构示例：")
    print("dataset/")
    print(" ├── train/cat/xxx.jpg")
    print(" ├── val/cat/xxx.jpg")
    print(" └── test/cat/xxx.jpg")

if __name__ == "__main__":
    split_dataset()
