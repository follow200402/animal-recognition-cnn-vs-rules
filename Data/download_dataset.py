"""
动物图像数据集下载脚本
支持多种数据源：Kaggle、Google Images、自定义URLs
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import requests
from tqdm import tqdm
import zipfile
import shutil


def download_file(url, dest_path, desc="下载中"):
    """下载文件并显示进度条"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as file, tqdm(
        desc=desc,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)


def download_from_kaggle(dataset_name, download_dir):
    """
    从Kaggle下载数据集
    需要先安装kaggle: pip install kaggle
    需要配置API: 在~/.kaggle/kaggle.json 放置你的API密钥
    """
    print(f"\n正在从 Kaggle 下载数据集: {dataset_name}")
    print("=" * 70)
    
    # 检查kaggle是否已安装
    try:
        import kaggle
        print("✓ Kaggle API 已安装")
    except ImportError:
        print("✗ Kaggle API 未安装")
        print("请运行: pip install kaggle")
        return False
    
    # 检查API密钥
    kaggle_json = Path.home() / '.config' / 'kaggle' / 'kaggle.json'
    if not kaggle_json.exists():
        print("✗ Kaggle API 密钥未配置")
        print("\n请按以下步骤配置:")
        print("1. 登录 https://www.kaggle.com/")
        print("2. 进入 Account -> API -> Create New API Token")
        print("3. 下载 kaggle.json 文件")
        print(f"4. 将文件放置到: {kaggle_json}")
        print(f"5. 运行: chmod 600 {kaggle_json}")
        return False
    
    print(f"✓ API 密钥已配置: {kaggle_json}")
    
    # 创建下载目录
    download_dir = Path(download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)
    
    # 下载数据集
    try:
        print(f"\n开始下载到: {download_dir}")
        subprocess.run([
            'kaggle', 'datasets', 'download',
            '-d', dataset_name,
            '-p', str(download_dir),
            '--unzip'
        ], check=True)
        print("\n✓ 数据集下载成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 下载失败: {e}")
        return False


def download_animals10_dataset():
    """
    下载 Animals-10 数据集
    包含10种动物: 狗、猫、马、蜘蛛、蝴蝶、鸡、绵羊、牛、松鼠、大象
    约28000张图像
    """
    dataset_name = "alessiocorrado99/animals10"
    data_dir = Path(__file__).parent / 'data'
    
    print("\n" + "=" * 70)
    print("Animals-10 数据集下载工具")
    print("=" * 70)
    print(f"数据集: {dataset_name}")
    print("包含类别: 狗、猫、马、蜘蛛、蝴蝶、鸡、绵羊、牛、松鼠、大象")
    print("图像数量: ~28,000张")
    print("=" * 70)
    
    success = download_from_kaggle(dataset_name, data_dir)
    
    if success:
        print("\n后续步骤:")
        print("1. 检查下载的数据: data/raw-img/")
        print("2. 运行数据预处理: python prepare_data.py --process")
        print("3. 开始训练模型: cd cnn_system && python train.py")
    
    return success


def download_animal_dataset_alternative():
    """
    备选方案：下载另一个动物数据集
    Animal Image Dataset (90 Different Animals)
    """
    dataset_name = "iamsouravbanerjee/animal-image-dataset-90-different-animals"
    data_dir = Path(__file__).parent / 'data'
    
    print("\n" + "=" * 70)
    print("Animal Image Dataset (90种动物)")
    print("=" * 70)
    print(f"数据集: {dataset_name}")
    print("包含类别: 90种不同的动物")
    print("=" * 70)
    
    return download_from_kaggle(dataset_name, data_dir)


def download_specific_animals():
    """
    下载项目需要的特定动物数据集
    使用 Caltech Camera Traps 或其他开源数据集
    """
    print("\n正在准备下载特定动物数据...")
    
    # 使用 Animal-10 数据集的一个子集
    # 这里我们尝试下载包含我们需要的动物类别的数据集
    datasets = [
        "alessiocorrado99/animals10",  # 包含常见动物
        "antoreepjana/animals-detection-images-dataset",  # 动物检测数据集
    ]
    
    data_dir = Path(__file__).parent / 'data'
    
    for dataset in datasets:
        print(f"\n尝试下载: {dataset}")
        if download_from_kaggle(dataset, data_dir):
            print(f"✓ 成功下载: {dataset}")
            return True
        else:
            print(f"✗ 跳过: {dataset}")
    
    return False


def setup_kaggle_api():
    """指导用户设置 Kaggle API"""
    print("\n" + "=" * 70)
    print("Kaggle API 配置指南")
    print("=" * 70)
    print("\n步骤 1: 安装 Kaggle API")
    print("运行命令: pip install kaggle")
    
    print("\n步骤 2: 获取 API 密钥")
    print("1. 访问 https://www.kaggle.com/")
    print("2. 登录您的账号（如果没有账号，请先注册）")
    print("3. 点击右上角头像 -> Account")
    print("4. 滚动到 'API' 部分")
    print("5. 点击 'Create New API Token'")
    print("6. 会自动下载 kaggle.json 文件")
    
    print("\n步骤 3: 配置 API 密钥")
    kaggle_dir = Path.home() / '.kaggle'
    print(f"1. 创建目录: mkdir -p {kaggle_dir}")
    print(f"2. 移动文件: mv ~/Downloads/kaggle.json {kaggle_dir}/")
    print(f"3. 设置权限: chmod 600 {kaggle_dir}/kaggle.json")
    
    print("\n步骤 4: 验证安装")
    print("运行命令: kaggle datasets list")
    
    print("\n" + "=" * 70)
    print("配置完成后，重新运行此脚本即可下载数据集")
    print("=" * 70)


def download_from_url(url, dest_dir, filename=None):
    """从指定URL下载文件"""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        filename = url.split('/')[-1]
    
    dest_path = dest_dir / filename
    
    print(f"下载: {url}")
    print(f"保存到: {dest_path}")
    
    try:
        download_file(url, dest_path, desc=filename)
        
        # 如果是压缩文件，自动解压
        if dest_path.suffix in ['.zip', '.tar', '.gz']:
            print(f"解压: {dest_path}")
            if dest_path.suffix == '.zip':
                with zipfile.ZipFile(dest_path, 'r') as zip_ref:
                    zip_ref.extractall(dest_dir)
            print("✓ 解压完成")
            
        return True
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False


def create_sample_dataset():
    """
    创建一个示例数据集结构
    用于测试和演示
    """
    print("\n创建示例数据集结构...")
    
    data_dir = Path(__file__).parent / 'data' / 'images'
    
    # 我们需要的动物类别（与产生式系统对应）
    animals = {
        'cheetah': '猎豹',
        'tiger': '老虎',
        'giraffe': '长颈鹿',
        'zebra': '斑马',
        'ostrich': '鸵鸟',
        'penguin': '企鹅',
        'albatross': '海燕'
    }
    
    for split in ['train', 'test']:
        for eng_name, cn_name in animals.items():
            dir_path = data_dir / split / eng_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # 创建README
            readme = dir_path / 'README.txt'
            readme.write_text(
                f"请将{cn_name}的图像放在这个目录下\n"
                f"支持的格式: .jpg, .jpeg, .png\n"
                f"建议图像数量: {'训练集200+张' if split == 'train' else '测试集50+张'}\n"
            )
    
    print(f"✓ 示例数据集结构已创建: {data_dir}")
    print("\n目录结构:")
    print("data/images/")
    print("  ├── train/")
    print("  │   ├── cheetah/ (猎豹)")
    print("  │   ├── tiger/ (老虎)")
    print("  │   ├── giraffe/ (长颈鹿)")
    print("  │   ├── zebra/ (斑马)")
    print("  │   ├── ostrich/ (鸵鸟)")
    print("  │   ├── penguin/ (企鹅)")
    print("  │   └── albatross/ (海燕)")
    print("  └── test/")
    print("      └── (相同结构)")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='动物数据集下载工具')
    parser.add_argument('--dataset', type=str, default='animals10',
                        choices=['animals10', 'animals90', 'specific', 'sample'],
                        help='选择要下载的数据集')
    parser.add_argument('--setup', action='store_true',
                        help='显示 Kaggle API 配置指南')
    parser.add_argument('--url', type=str,
                        help='从指定URL下载数据集')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_kaggle_api()
        return
    
    if args.url:
        data_dir = Path(__file__).parent / 'data'
        download_from_url(args.url, data_dir)
        return
    
    if args.dataset == 'animals10':
        download_animals10_dataset()
    elif args.dataset == 'animals90':
        download_animal_dataset_alternative()
    elif args.dataset == 'specific':
        download_specific_animals()
    elif args.dataset == 'sample':
        create_sample_dataset()


if __name__ == '__main__':
    # 检查必要的库
    try:
        import requests
        from tqdm import tqdm
    except ImportError:
        print("请先安装必要的库:")
        print("pip install requests tqdm kaggle")
        sys.exit(1)
    
    main()
