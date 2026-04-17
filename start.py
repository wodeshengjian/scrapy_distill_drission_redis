#!/usr/bin/env python3
"""
Scrapy Distill Drission Redis - One-click Launcher
"""
import os
import sys
import subprocess
import time


def check_python():
    """检查Python环境"""
    try:
        import sys
        if sys.version_info < (3, 8):
            print("❌ Python版本需要3.8+")
            return False
        print("✅ Python环境正常")
        return True
    except Exception as e:
        print(f"❌ Python检查失败: {e}")
        return False


def check_dependencies():
    """检查依赖"""
    required = ['scrapy', 'drissionpage', 'redis', 'sklearn', 'PyQt5']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg if pkg != 'sklearn' else 'sklearn')
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"⚠️  缺失依赖: {', '.join(missing)}")
        print("正在安装依赖...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'])
            print("✅ 依赖安装完成")
            return True
        except Exception as e:
            print(f"❌ 依赖安装失败: {e}")
            return False
    print("✅ 依赖检查通过")
    return True


def train_model():
    """训练AI模型"""
    model_path = os.path.join('models', 'anti_detect_model.pkl')
    if not os.path.exists(model_path):
        print("⚠️  模型不存在，正在训练...")
        os.chdir('src/train')
        try:
            subprocess.check_call([sys.executable, 'train.py'])
            print("✅ 模型训练完成")
        except Exception as e:
            print(f"❌ 模型训练失败: {e}")
        os.chdir('../..')
    else:
        print("✅ 模型已存在")


def launch_gui():
    """启动图形化界面"""
    print("🚀 启动图形化界面...")
    subprocess.run([sys.executable, '-m', 'src.gui'])


def main():
    """主函数"""
    print("=" * 50)
    print("  Scrapy Distill Drission Redis")
    print("  Distributed Crawler System")
    print("=" * 50)
    print()
    
    if not check_python():
        input("按Enter退出...")
        return
    
    if not check_dependencies():
        input("按Enter退出...")
        return
    
    train_model()
    print()
    
    launch_gui()


if __name__ == '__main__':
    main()