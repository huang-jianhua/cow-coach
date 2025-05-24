# 🎯 AI Coach 专属教练系统

基于蜕变式学习理念的智能成长教练系统

## ⚖️ 版权声明

本系统基于开源框架开发，所有原创代码遵循MIT许可证。系统采用通用的蜕变式学习理念，不涉及任何特定个人或机构的专有内容。

## 🚀 快速部署

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/cow-coach.git
cd cow-coach
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥
```bash
# 复制配置模板
cp config-coach-template.json config-coach.json

# 编辑配置文件，替换 YOUR_API_KEY_HERE 为你的真实API密钥
```

### 4. 启动系统
```bash
# 增强版启动（推荐）
python start_coach.py

# 或基础版启动
python app.py
```

## 🔒 安全配置指南

### ⚠️ 重要安全提醒

**绝对不要将包含真实API密钥的配置文件提交到Git！**

### 🛡️ 安全最佳实践

1. **使用环境变量**（推荐）
```bash
# 设置环境变量
export OPENAI_API_KEY="your-real-api-key"
export OPENAI_API_BASE="https://api.siliconflow.cn"

# 或创建 .env 文件（已在.gitignore中排除）
echo "OPENAI_API_KEY=your-real-api-key" > .env
```

2. **本地配置文件**
```bash
# 从模板创建本地配置
cp config-coach-template.json config-coach.json
# 编辑 config-coach.json，替换API密钥
# 此文件已在.gitignore中排除，不会被上传
```

3. **检查敏感信息**
```bash
# 提交前检查是否包含敏感信息
git status
git diff --cached

# 确保以下文件已被忽略：
# - config.json
# - config-coach.json  
# - data/
# - logs/
# - *.env
```

### 📁 项目文件说明

```
cow-coach/
├── config-template.json         # 基础配置模板（安全）
├── config-coach-template.json   # 专属教练配置模板（安全）
├── config.json                  # 运行时配置（被忽略）
├── config-coach.json           # 专属教练配置（被忽略）
├── .env                        # 环境变量文件（被忽略）
├── .gitignore                  # Git忽略规则
└── data/                       # 用户数据目录（被忽略）
```

## 📋 功能特色

### 🎯 核心理念
- **蜕变式学习**：注重内在转变，而非知识堆积
- **个性化路径**：每个人都有独特的学习节奏
- **情感支持**：理性分析与情感关怀并重
- **实践导向**：应用胜过理论记忆

### ✨ 增强功能

#### 📊 个人成长档案管理
- 用户学习历程跟踪
- 个性化成长轨迹记录
- 学习风格识别与适配

#### 🎯 智能目标管理
```
/goals set "30天内掌握Python基础"    # 设置新目标
/goals list                          # 查看目标列表
/goals complete 1                    # 标记目标完成
/goals update 1 "更新目标描述"        # 更新目标
```

#### 😊 情绪状态追踪
```
/mood 8 "今天学会了新技能，很有成就感"  # 记录心情(1-10分)
/mood check                           # 查看心情趋势分析
```

#### 💡 学习洞察分析
```
/insights    # 获取个性化学习报告
```

#### 🎉 成就庆祝系统
```
/celebrate "我完成了第一个Python项目"  # 记录里程碑
```

#### 📈 数据可视化
- 学习频率统计
- 心情变化趋势
- 目标完成率分析
- 成长轨迹图表

## 🛠️ 系统架构

### 📁 项目结构
```
cow-coach/
├── start_coach.py           # 专属教练启动脚本
├── app.py                   # 主应用程序
├── config.json              # 配置文件
├── bot/
│   └── coach/
│       └── coach_bot.py     # 专属教练机器人
├── plugins/
│   └── coach_toolkit/
│       └── coach_toolkit.py # 教练工具包插件
├── data/
│   └── coach.db            # 成长数据库
└── logs/                   # 日志文件
```

### 🗄️ 数据库结构
- **user_profiles**: 用户档案表
- **learning_records**: 学习记录表
- **goals**: 目标管理表
- **milestones**: 成长里程碑表

## 🎨 使用场景

### 💼 职场技能提升
- 设定技能学习目标
- 跟踪学习进度
- 记录应用实践
- 庆祝技能突破

### 📚 学术研究指导
- 论文写作进度管理
- 研究方向探索
- 学术情绪支持
- 成果展示激励

### 🌱 个人成长陪伴
- 自我认知提升
- 生活习惯改变
- 情绪管理指导
- 人际关系改善

## 🔧 技术配置

### 环境要求
- Python 3.7+
- SQLite3 (内置)
- 网络连接

### AI模型配置
```json
{
  "model": "Pro/deepseek-ai/DeepSeek-V3",
  "open_ai_api_base": "https://api.siliconflow.cn",
  "open_ai_api_key": "your-api-key"
}
```

### 插件系统
- 模块化设计，支持功能扩展
- 热插拔机制，无需重启
- 数据驱动的个性化体验

## 📱 Web界面

访问地址：http://localhost:9899/chat

### 界面特色
- 🎨 简洁现代的UI设计
- 📱 响应式布局，支持移动端
- 💬 实时对话体验
- 📊 数据可视化图表
- 🎯 快捷命令面板

## 🔍 命令参考

### 基础对话
- 直接输入文字即可开始对话
- 支持多轮连续对话
- 智能上下文理解

### 系统命令
```bash
/help              # 查看完整帮助
/goals set "目标"   # 设置学习目标  
/goals list        # 查看目标列表
/mood 8 "心情"     # 记录心情状态
/mood check        # 查看心情趋势
/insights          # 获取学习洞察
/celebrate "成就"  # 庆祝成就时刻
```

## 📈 成长数据

### 自动记录
- 对话频率统计
- 学习主题分析
- 情绪变化追踪
- 目标达成率

### 隐私保护
- 本地数据存储
- 用户完全控制
- 支持数据导出
- 可选择性删除

## 🎓 蜕变式学习原理

### 四大支柱
1. **内在转变** - 关注思维模式的改变
2. **个性化路径** - 尊重每个人的独特节奏
3. **情感支持** - 理性分析与感性关怀并重
4. **实践应用** - 知行合一的学习方式

### 核心方法
- 🤔 启发性提问引导深度思考
- 💭 反思总结促进内化吸收  
- 🎯 目标设定激发内在动力
- 🎉 成就庆祝强化正向体验

## 🔄 版本更新

### v2.0 增强版 (当前)
- ✨ 全新的专属教练体验
- 📊 完整的数据追踪系统
- 🎯 智能化目标管理
- 😊 情绪状态深度分析
- 🎉 成就激励机制

### v1.0 基础版
- 💬 基础对话功能
- 🤖 AI教练角色设定
- 🌐 Web界面支持

## 🤝 贡献指南

欢迎提交：
- 🐛 Bug报告
- 💡 功能建议  
- 📝 文档改进
- 🎨 界面优化

## 📞 获取帮助

- 🐛 **报告问题**: 在GitHub仓库创建Issue
- 💡 **功能建议**: 提交Feature Request  
- 📖 **查看文档**: 阅读项目Wiki和README
- 💬 **社区讨论**: 参与GitHub Discussions

---

> 💙 "真正的学习不是知识的堆积，而是内在的蜕变。每一次对话，都是成长的种子。" 
> 
> —— Keith AI Coach

## 🎓 开始你的蜕变之旅

```bash
git clone https://github.com/yourusername/cow-coach.git
cd cow-coach
cp config-coach-template.json config-coach.json
# 编辑config-coach.json配置你的API密钥
python start_coach.py
```

打开浏览器访问：http://localhost:9899/chat

让我们一起开启属于你的成长故事！✨

## 🌟 目标设置功能使用指南

你的AI教练系统现在已经成功启动！以下是目标设置功能的详细使用说明：

### 📋 目标管理命令

#### 1. **查看帮助信息**
```
/help
```
显示所有可用的教练工具命令

#### 2. **设置新目标**
```
/goals set "你的目标描述"
```
**示例：**
- `/goals set "30天内掌握Python基础语法"`
- `/goals set "每周阅读一本专业书籍"`
- `/goals set "提升英语口语表达能力"`

#### 3. **查看目标列表**
```
/goals list
```
显示你的所有目标，包括：
- 🔥 进行中的目标
- ✅ 已完成的目标
- 📅 创建日期

#### 4. **完成目标**
```
/goals complete [目标ID]
```
**示例：**
- `/goals complete 1` （完成ID为1的目标）

#### 5. **更新目标**
```
/goals update [目标ID] "新的目标描述"
```
**示例：**
- `/goals update 1 "45天内精通Python面向对象编程"`

### 🛠️ 其他教练功能

#### 心情记录
```
/mood 8 "今天学习很有收获"
/mood check
```

#### 学习洞察
```
/insights
```

#### 庆祝成就
```
/celebrate "完成了第一个Python项目"
```

### 🌐 访问方式

1. **Web界面**: http://localhost:9899/chat
2. **直接在聊天框中输入上述命令**

### ⚠️ 问题解决

如果遇到"未知插件命令"错误，请检查：

1. **确认系统启动状态**
   ```bash
   netstat -ano | findstr :9899
   ```
   应该看到 LISTENING 状态

2. **重新启动系统**
   ```bash
   python start_coach.py
   ```

3. **检查数据库**
   - 确认 `data/coach.db` 文件存在
   - 文件大小应该大于 0KB

4. **插件配置检查**
   - `plugins/coach_toolkit/__init__.py` 存在
   - `plugins/plugins.json` 中包含 coach_toolkit 配置

### 🎉 系统特色

- ✨ **蜕变式学习理念**: 注重内在转变而非知识堆积
- 📊 **数据驱动成长**: 智能追踪学习进度和情绪变化  
- 🎯 **个性化指导**: 根据你的学习风格提供定制建议
- 💾 **持久化存储**: 所有数据安全保存在本地数据库
- 🌟 **温暖陪伴**: 像朋友一样真诚的AI教练体验

### 🚀 快速开始

1. 确保系统运行中: `python start_coach.py`
2. 打开浏览器访问: http://localhost:9899/chat
3. 输入你的第一个目标: `/goals set "你的第一个成长目标"`
4. 查看目标列表: `/goals list`
5. 开始你的蜕变之旅！✨

---

## 系统架构与配置

### 📁 目录结构
```
cow-coach/
├── start_coach.py          # 专属教练启动脚本
├── config-coach.json       # 专属教练配置文件
├── data/
│   └── coach.db           # 用户数据和学习记录
├── plugins/
│   └── coach_toolkit/     # 教练工具包插件
└── bot/
    └── coach/            # CoachBot核心代码
```

### ⚙️ 配置说明

- **修改配置**: 编辑 `config-coach.json`
- **恢复原配置**: `python start_coach.py restore`
- **编辑配置**: `python start_coach.py edit`
- **查看帮助**: `python start_coach.py help`

### 🔧 技术特性

- **SQLite数据库**: 本地存储，数据安全
- **插件架构**: 模块化功能扩展
- **Web界面**: 现代化聊天体验
- **专属配置**: 独立于原系统的配置管理
- **自动备份**: 原配置文件自动备份

### 💡 开发说明

基于 chatgpt-on-wechat 框架深度定制，实现了：
- 专属的 CoachBot 类
- coach_toolkit 插件
- 蜕变式学习对话逻辑
- 个人成长数据管理
- 情感支持和激励系统

---

*✨ 愿你在这个AI教练的陪伴下，实现真正的蜕变式成长！*

## 🌐 部署到生产环境

### Docker部署（推荐）
```bash
# 构建镜像
docker build -t ai-coach .

# 运行容器（使用环境变量传递API密钥）
docker run -d \
  -e OPENAI_API_KEY="your-api-key" \
  -e OPENAI_API_BASE="https://api.siliconflow.cn" \
  -p 9899:9899 \
  ai-coach
```

### 云平台部署
- **Heroku**: 在设置中配置环境变量
- **Vercel**: 在项目设置中添加环境变量  
- **Railway**: 支持从GitHub直接部署，配置环境变量

### 🔐 生产环境安全建议

1. **使用HTTPS**: 确保生产环境使用SSL证书
2. **限制访问**: 配置防火墙和访问控制
3. **定期更新**: 及时更新依赖和安全补丁
4. **监控日志**: 启用日志监控和异常报警
5. **备份数据**: 定期备份用户数据和配置

## 🔧 开发贡献

### 提交代码前检查清单

- [ ] 确保没有硬编码的API密钥
- [ ] 更新了相应的模板文件
- [ ] 运行了安全检查：`git diff --cached | grep -i "key\|secret"`
- [ ] 测试了配置模板的正确性
- [ ] 更新了文档和README

### 安全审查

```bash
# 检查是否有敏感信息泄露
git log --oneline | head -10
git show --name-only HEAD

# 如果发现敏感信息已提交，立即删除并重写历史
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch config.json' \
--prune-empty --tag-name-filter cat -- --all
```

## 📞 支持与反馈

- 🐛 **Bug报告**: 创建GitHub Issue
- 💡 **功能建议**: 提交Feature Request  
- 📖 **文档改进**: 提交Pull Request
- 💬 **使用咨询**: 查看Wiki或Discussions

**安全问题**: 如发现安全漏洞，请私下联系维护者，不要公开披露。

## 🔒 隐私声明

- **本地存储**: 所有用户数据存储在本地，不上传到外部服务器
- **API调用**: 仅向配置的AI服务提供商发送对话内容  
- **数据控制**: 用户完全控制自己的数据，可随时导出或删除
- **开源透明**: 所有代码开源，欢迎审查和贡献

```bash
git clone https://github.com/yourusername/cow-coach.git
cd cow-coach
cp config-coach-template.json config-coach.json
# 编辑config-coach.json配置你的API密钥
python start_coach.py
```

打开浏览器访问：http://localhost:9899/chat

让我们一起开启属于你的成长故事！✨