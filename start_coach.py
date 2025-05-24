#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
专属AI教练启动脚本
基于蜕变式学习理念

使用方法：
python start_coach.py
"""

import os
import sys
import json
import shutil
from pathlib import Path

def create_coach_config():
    """从模板创建教练专属配置"""
    template_file = "config-coach-template.json"
    
    if not os.path.exists(template_file):
        print(f"❌ 模板文件 {template_file} 不存在")
        print("请确保项目文件完整")
        return None
    
    try:
        with open(template_file, "r", encoding="utf-8") as f:
            coach_config = json.load(f)
        
        # 检查是否需要设置API密钥
        if coach_config.get("open_ai_api_key") == "YOUR_API_KEY_HERE":
            print("⚠️  请先配置你的API密钥！")
            api_key = input("请输入你的OpenAI API密钥: ").strip()
            if api_key:
                coach_config["open_ai_api_key"] = api_key
            else:
                print("❌ 未提供API密钥，无法继续")
                return None
        
        return coach_config
        
    except Exception as e:
        print(f"❌ 读取模板配置失败: {e}")
        return None

def load_or_create_coach_config():
    """加载或创建专属教练配置文件"""
    coach_config_file = "config-coach.json"
    
    if os.path.exists(coach_config_file):
        print(f"✅ 发现专属教练配置文件: {coach_config_file}")
        try:
            with open(coach_config_file, "r", encoding="utf-8") as f:
                coach_config = json.load(f)
            print("✅ 已加载现有专属教练配置")
            return coach_config
        except Exception as e:
            print(f"❌ 读取专属教练配置失败: {e}")
            print("🔄 将创建新的默认配置")
    
    # 创建默认配置
    coach_config = create_coach_config()
    
    # 保存专属配置文件
    with open(coach_config_file, "w", encoding="utf-8") as f:
        json.dump(coach_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已创建专属教练配置文件: {coach_config_file}")
    return coach_config

def backup_original_config():
    """备份原始配置"""
    if os.path.exists("config.json"):
        backup_file = f"config.backup.{int(__import__('time').time())}.json"
        shutil.copy("config.json", backup_file)
        print(f"✅ 已备份原配置为: {backup_file}")
        return backup_file
    return None

def apply_coach_config(coach_config):
    """应用专属教练配置"""
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(coach_config, f, ensure_ascii=False, indent=2)
    print("✅ 已应用专属教练配置到 config.json")

def setup_coach_environment():
    """设置教练环境"""
    # 创建数据目录
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # 确保插件目录存在
    coach_toolkit_dir = "plugins/coach_toolkit"
    if not os.path.exists(coach_toolkit_dir):
        os.makedirs(coach_toolkit_dir, exist_ok=True)
    
    # 确保CoachBot目录存在
    coach_bot_dir = "bot/coach"
    if not os.path.exists(coach_bot_dir):
        os.makedirs(coach_bot_dir, exist_ok=True)
    
    print("✅ 教练环境初始化完成")

def start_coach():
    """启动专属AI教练系统"""
    
    print("🚀 启动专属AI教练增强版系统...")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return
    
    # 检查必要文件
    if not os.path.exists("app.py"):
        print("❌ 未找到app.py文件，请确保在项目根目录运行")
        return
    
    # 检查增强功能文件
    coach_bot_file = "bot/coach/coach_bot.py"
    coach_plugin_file = "plugins/coach_toolkit/coach_toolkit.py"
    
    if not os.path.exists(coach_bot_file):
        print(f"❌ 未找到CoachBot文件: {coach_bot_file}")
        print("请确保已安装增强版功能")
        return
        
    if not os.path.exists(coach_plugin_file):
        print(f"❌ 未找到教练工具包插件: {coach_plugin_file}")
        print("请确保已安装增强版功能")
        return
    
    # 备份原配置
    backup_file = backup_original_config()
    
    # 设置教练环境
    setup_coach_environment()
    
    # 加载或创建专属教练配置
    coach_config = load_or_create_coach_config()
    if not coach_config:
        print("❌ 配置创建失败，无法启动")
        return
    
    # 应用专属教练配置
    apply_coach_config(coach_config)
    
    # 显示启动信息
    print("\n🎯 Keith AI Coach 专属教练增强版")
    print("基于蜕变式学习理念")
    print("-" * 50)
    print("💻 Web界面地址: http://localhost:9899/chat")
    print("📁 专属配置文件: config-coach.json")
    if backup_file:
        print(f"💾 原配置备份: {backup_file}")
    print("-" * 50)
    print("🛠️ 增强功能命令:")
    print("   /goals set \"目标\" - 设置学习目标")
    print("   /goals list - 查看目标列表")
    print("   /mood 8 \"心情\" - 记录心情状态")
    print("   /mood check - 查看心情趋势")
    print("   /insights - 获取学习洞察")
    print("   /celebrate \"成就\" - 庆祝成就")
    print("   /help - 查看完整帮助")
    print("-" * 50)
    print("🌟 核心特色:")
    print("   • 个人成长档案管理")
    print("   • 学习进度智能跟踪")
    print("   • 情绪状态深度分析") 
    print("   • 目标管理与激励")
    print("   • 蜕变式学习指导")
    print("   • 数据驱动的成长洞察")
    print("-" * 50)
    print("💡 配置说明:")
    print("   • 修改 config-coach.json 可自定义专属教练设置")
    print("   • 使用 'python start_coach.py restore' 恢复原配置")
    print("   • 专属教练数据保存在 data/ 目录")
    print("-" * 50)
    print("按 Ctrl+C 停止服务\n")
    
    # 启动主程序
    try:
        import subprocess
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 感谢使用Keith AI Coach增强版！")
        print("期待下次与你的学习对话！")
        print("你的成长数据已安全保存在 data/ 目录中")
        print("专属配置已保存在 config-coach.json 文件中")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        print("请检查依赖是否安装完整: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

def restore_config():
    """恢复原始配置"""
    backup_files = [f for f in os.listdir(".") if f.startswith("config.backup.")]
    if backup_files:
        latest_backup = max(backup_files, key=lambda x: os.path.getctime(x))
        shutil.copy(latest_backup, "config.json")
        print(f"✅ 已恢复配置从: {latest_backup}")
        print("💡 专属教练配置仍保留在 config-coach.json")
    else:
        print("❌ 未找到备份配置文件")

def edit_coach_config():
    """编辑专属教练配置"""
    coach_config_file = "config-coach.json"
    
    if not os.path.exists(coach_config_file):
        print("❌ 专属教练配置文件不存在，正在创建...")
        coach_config = create_coach_config()
        with open(coach_config_file, "w", encoding="utf-8") as f:
            json.dump(coach_config, f, ensure_ascii=False, indent=2)
        print(f"✅ 已创建: {coach_config_file}")
    
    print(f"\n📝 编辑专属教练配置文件: {coach_config_file}")
    print("你可以使用任何文本编辑器修改此文件")
    print("修改后使用 'python start_coach.py' 重新启动即可生效")
    
    # 尝试用系统默认编辑器打开（可选）
    try:
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            subprocess.run(["notepad", coach_config_file])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-e", coach_config_file])
        else:  # Linux
            subprocess.run(["nano", coach_config_file])
    except:
        print(f"请手动打开文件: {coach_config_file}")

def show_usage():
    """显示使用说明"""
    print("""
🎯 Keith AI Coach 专属教练系统

使用方法：
  python start_coach.py          - 启动增强版教练系统
  python start_coach.py restore  - 恢复原始配置
  python start_coach.py edit     - 编辑专属教练配置
  python start_coach.py help     - 显示帮助信息

配置文件：
  config-coach.json              - 专属教练配置文件
  config.json                    - 系统运行配置（自动生成）
  config.backup.*.json           - 原配置备份文件

功能特色：
  ✨ 基于蜕变式学习理念
  📊 个人成长数据追踪
  🎯 智能目标管理
  😊 情绪状态分析
  💡 个性化学习洞察
  🎉 成就庆祝与激励

系统要求：
  • Python 3.7+
  • 已配置的AI模型API密钥
  • 网络连接

更多信息请查看 README.md
""")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "restore":
            restore_config()
        elif sys.argv[1] == "edit":
            edit_coach_config()
        elif sys.argv[1] == "help":
            show_usage()
        else:
            print("❌ 未知参数，使用 'python start_coach.py help' 查看帮助")
    else:
        start_coach() 