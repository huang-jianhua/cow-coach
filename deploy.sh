#!/bin/bash

# 阿里云轻量服务器一键部署 chatgpt-on-wechat 脚本
# 使用方法：bash deploy.sh

echo "🚀 开始部署 chatgpt-on-wechat 到阿里云服务器..."

# 更新系统
echo "📦 更新系统软件包..."
sudo apt update -y
sudo apt upgrade -y

# 安装必要软件
echo "🔧 安装必要软件..."
sudo apt install -y git python3 python3-pip python3-venv nginx supervisor curl

# 创建项目目录
echo "📁 创建项目目录..."
sudo mkdir -p /var/www/chatgpt-wechat
cd /var/www/chatgpt-wechat

# 下载项目代码
echo "⬇️ 下载项目代码..."
sudo git clone https://github.com/zhayujie/chatgpt-on-wechat.git .

# 设置目录权限
sudo chown -R $USER:$USER /var/www/chatgpt-wechat

# 创建Python虚拟环境
echo "🐍 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
echo "📚 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 复制配置文件
echo "⚙️ 创建配置文件..."
cp config-template.json config.json

# 创建systemd服务文件
echo "🔄 创建系统服务..."
sudo tee /etc/systemd/system/chatgpt-wechat.service > /dev/null <<EOF
[Unit]
Description=ChatGPT on WeChat
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/chatgpt-wechat
ExecStart=/var/www/chatgpt-wechat/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
sudo systemctl daemon-reload
sudo systemctl enable chatgpt-wechat

# 配置防火墙
echo "🔥 配置防火墙..."
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw --force enable

# 获取服务器IP
SERVER_IP=$(curl -s ifconfig.me)

echo "✅ 部署完成！"
echo ""
echo "🎯 下一步操作："
echo "1. 编辑配置文件：sudo nano /var/www/chatgpt-wechat/config.json"
echo "2. 填入你的API密钥和微信公众号配置"
echo "3. 启动服务：sudo systemctl start chatgpt-wechat"
echo "4. 查看日志：sudo journalctl -u chatgpt-wechat -f"
echo ""
echo "🌐 服务器IP地址：$SERVER_IP"
echo "📝 配置文件位置：/var/www/chatgpt-wechat/config.json"
echo ""
echo "🎉 恭喜！你的AI助手即将上线！" 