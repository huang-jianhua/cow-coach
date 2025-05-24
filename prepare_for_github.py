#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub上传准备脚本
用于清理敏感信息，准备项目上传
"""

import os
import shutil
import json
import glob
from pathlib import Path

def clean_sensitive_files():
    """清理敏感文件"""
    print("🧹 清理敏感文件...")
    
    # 要删除的敏感文件
    sensitive_files = [
        "config.json",
        "config-coach.json", 
        "config.backup.*.json",
        ".env",
        "*.log"
    ]
    
    # 要删除的敏感目录
    sensitive_dirs = [
        "data/",
        "logs/",
        "__pycache__/",
        "*.egg-info/",
        ".venv/",
        "venv/"
    ]
    
    removed_files = []
    
    # 删除敏感文件
    for pattern in sensitive_files:
        for file_path in glob.glob(pattern):
            if os.path.exists(file_path):
                os.remove(file_path)
                removed_files.append(file_path)
                print(f"   ✅ 删除文件: {file_path}")
    
    # 删除敏感目录
    for pattern in sensitive_dirs:
        for dir_path in glob.glob(pattern):
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
                removed_files.append(dir_path)
                print(f"   ✅ 删除目录: {dir_path}")
    
    if not removed_files:
        print("   ✅ 没有发现敏感文件")
    
    return removed_files

def check_api_keys_in_files():
    """检查文件中是否包含API密钥"""
    print("🔍 检查文件中的API密钥...")
    
    # 敏感关键词
    sensitive_patterns = [
        "sk-",  # OpenAI API key prefix
        "api_key",
        "secret",
        "password",
        "token"
    ]
    
    # 要检查的文件类型
    check_extensions = [".py", ".json", ".md", ".txt", ".yml", ".yaml"]
    
    warnings = []
    
    for root, dirs, files in os.walk("."):
        # 跳过git目录
        if ".git" in dirs:
            dirs.remove(".git")
        
        for file in files:
            if any(file.endswith(ext) for ext in check_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        
                        for pattern in sensitive_patterns:
                            if pattern in content and "your_api_key" not in content and "template" not in file_path:
                                warnings.append(f"⚠️  {file_path} 可能包含敏感信息: {pattern}")
                except Exception:
                    continue
    
    if warnings:
        print("   发现潜在敏感信息:")
        for warning in warnings:
            print(f"   {warning}")
        return False
    else:
        print("   ✅ 未发现敏感信息")
        return True

def create_gitignore():
    """确保.gitignore文件正确"""
    print("📝 检查.gitignore文件...")
    
    if os.path.exists(".gitignore"):
        print("   ✅ .gitignore文件已存在")
    else:
        print("   ❌ 缺少.gitignore文件")
        return False
    
    return True

def verify_templates():
    """验证模板文件是否存在且安全"""
    print("📋 验证配置模板...")
    
    templates = [
        "config-template.json",
        "config-coach-template.json"
    ]
    
    all_good = True
    
    for template in templates:
        if os.path.exists(template):
            try:
                with open(template, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # 检查是否包含真实API密钥
                api_key = config.get("open_ai_api_key", "")
                if api_key and not api_key.startswith("YOUR_"):
                    print(f"   ⚠️  {template} 包含真实API密钥")
                    all_good = False
                else:
                    print(f"   ✅ {template} 安全")
            except Exception as e:
                print(f"   ❌ {template} 读取失败: {e}")
                all_good = False
        else:
            print(f"   ❌ 缺少模板文件: {template}")
            all_good = False
    
    return all_good

def create_env_example():
    """创建环境变量示例文件"""
    print("🔧 创建环境变量示例...")
    
    env_example_content = """# AI Coach 环境变量配置示例
# 复制此文件为 .env 并填入真实值

# OpenAI API配置
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=https://api.siliconflow.cn

# Web服务配置
WEB_PORT=9899
DEBUG=true

# 可选：其他AI服务配置
# CLAUDE_API_KEY=your-claude-api-key
# ZHIPU_API_KEY=your-zhipu-api-key
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_example_content)
    
    print("   ✅ 创建 .env.example 文件")

def main():
    """主函数"""
    print("🚀 准备项目上传到GitHub...")
    print("=" * 50)
    
    # 1. 清理敏感文件
    removed_files = clean_sensitive_files()
    print()
    
    # 2. 检查文件中的API密钥
    api_check_passed = check_api_keys_in_files()
    print()
    
    # 3. 验证.gitignore
    gitignore_ok = create_gitignore()
    print()
    
    # 4. 验证模板文件
    templates_ok = verify_templates()
    print()
    
    # 5. 创建环境变量示例
    create_env_example()
    print()
    
    # 总结
    print("📊 准备结果:")
    print(f"   • 清理文件: {len(removed_files)} 个")
    print(f"   • API密钥检查: {'✅ 通过' if api_check_passed else '❌ 失败'}")
    print(f"   • .gitignore: {'✅ 正常' if gitignore_ok else '❌ 异常'}")
    print(f"   • 配置模板: {'✅ 安全' if templates_ok else '❌ 有问题'}")
    
    if api_check_passed and gitignore_ok and templates_ok:
        print("\n🎉 项目已准备好上传到GitHub！")
        print("\n📋 下一步操作:")
        print("   1. git add .")
        print("   2. git commit -m '初始提交: AI教练系统'")
        print("   3. git remote add origin https://github.com/yourusername/cow-coach.git")
        print("   4. git push -u origin main")
        print("\n⚠️  上传前再次确认:")
        print("   git status  # 查看将要提交的文件")
        print("   git diff --cached | grep -i 'key\\|secret'  # 最后检查")
    else:
        print("\n❌ 发现问题，请先解决后再上传！")
    
    print("\n💡 记住：用户需要自己配置API密钥才能使用系统")

if __name__ == "__main__":
    main() 