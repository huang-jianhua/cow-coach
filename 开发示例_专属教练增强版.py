# 专属AI教练增强版 - 二次开发示例
# 基于蜕变式学习理念的深度定制

"""
这个示例展示如何在chatgpt-on-wechat基础上开发一个专属的AI教练系统
主要功能：
1. 个人成长档案管理
2. 学习进度跟踪  
3. 定制化学习计划
4. 情感支持系统
5. 成果展示和激励
"""

# ==================== 1. 自定义Bot类 ====================
# bot/coach/coach_bot.py

from bot.bot import Bot
from bot.session_manager import SessionManager
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf
import json
import datetime
import sqlite3
import os

class CoachBot(Bot):
    """专属AI教练机器人"""
    
    def __init__(self):
        super().__init__()
        self.sessions = SessionManager(CoachSession, model=conf().get("model") or "gpt-3.5-turbo")
        self.db_path = "data/coach.db"
        self.init_database()
        
    def init_database(self):
        """初始化用户档案数据库"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 用户档案表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                goals TEXT,
                learning_style TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # 学习记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                session_date DATE,
                topic TEXT,
                insights TEXT,
                action_items TEXT,
                mood_score INTEGER,
                created_at TIMESTAMP
            )
        ''')
        
        # 成长里程碑表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                title TEXT,
                description TEXT,
                achieved_at TIMESTAMP,
                celebration_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def reply(self, query, context=None):
        try:
            user_id = context.get('session_id', 'default_user')
            
            # 分析用户意图
            intent = self.analyze_intent(query)
            
            if intent == 'profile_setup':
                return self.handle_profile_setup(query, user_id)
            elif intent == 'learning_reflection':
                return self.handle_learning_reflection(query, user_id)
            elif intent == 'progress_check':
                return self.handle_progress_check(user_id)
            elif intent == 'goal_setting':
                return self.handle_goal_setting(query, user_id)
            else:
                # 使用蜕变式学习原理进行常规对话
                return self.handle_coaching_dialogue(query, user_id)
                
        except Exception as e:
            logger.error(f"CoachBot reply error: {e}")
            return Reply(ReplyType.TEXT, "抱歉，我现在有点困惑，让我重新整理一下思路...")
    
    def analyze_intent(self, query):
        """分析用户意图"""
        query_lower = query.lower()
        
        intent_keywords = {
            'profile_setup': ['我是', '我叫', '介绍一下', '第一次'],
            'learning_reflection': ['学会了', '领悟到', '反思', '总结'],
            'progress_check': ['进展', '进度', '成长', '变化'],
            'goal_setting': ['目标', '计划', '想要', '希望']
        }
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        return 'general_coaching'
    
    def handle_profile_setup(self, query, user_id):
        """处理用户档案设置"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已有档案
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
        existing_profile = cursor.fetchone()
        
        if not existing_profile:
            # 创建新档案
            now = datetime.datetime.now()
            cursor.execute('''
                INSERT INTO user_profiles (user_id, name, created_at, updated_at) 
                VALUES (?, ?, ?, ?)
            ''', (user_id, "学习伙伴", now, now))
            conn.commit()
            
            response = """🌟 欢迎来到你的专属AI教练空间！

我是基于蜕变式学习理念训练的AI教练。我相信每个人都有无限的成长潜能，关键是找到适合自己的学习方式。

为了更好地帮助你，我想了解一下：

1. 你希望我怎么称呼你？
2. 你目前最想在哪个方面实现突破？
3. 你的学习风格是怎样的？(比如喜欢理论分析还是实践体验)

请随意分享，我会根据你的情况制定个性化的成长计划。✨"""
        
        else:
            response = """🎯 很高兴再次见到你！

我记得我们之前的对话。如果你想更新个人信息或设定新的成长目标，请告诉我具体的变化。

或者，我们可以直接开始今天的学习对话。你今天想探讨什么话题？"""
        
        conn.close()
        return Reply(ReplyType.TEXT, response)
    
    def handle_learning_reflection(self, query, user_id):
        """处理学习反思"""
        # 引导用户进行深度反思
        reflection_questions = [
            "这个领悟对你来说意味着什么？",
            "你是如何得出这个认识的？",
            "这会如何改变你接下来的行动？",
            "你想如何应用这个新的理解？"
        ]
        
        # 记录学习记录
        self.save_learning_record(user_id, query)
        
        import random
        question = random.choice(reflection_questions)
        
        response = f"""💡 很棒的反思！我能感受到你的成长。

{question}

蜕变式学习的核心就是这种深度的自我觉察。每一次反思都是在为内在的转变播种。继续分享你的想法，让我们一起深入探索。🌱"""
        
        return Reply(ReplyType.TEXT, response)
    
    def handle_progress_check(self, user_id):
        """处理进度检查"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取最近的学习记录
        cursor.execute('''
            SELECT COUNT(*), AVG(mood_score) 
            FROM learning_records 
            WHERE user_id = ? AND session_date >= date('now', '-30 days')
        ''', (user_id,))
        
        result = cursor.fetchone()
        sessions_count = result[0] if result[0] else 0
        avg_mood = result[1] if result[1] else 0
        
        # 获取里程碑
        cursor.execute('''
            SELECT COUNT(*) FROM milestones WHERE user_id = ?
        ''', (user_id,))
        milestones_count = cursor.fetchone()[0]
        
        conn.close()
        
        if sessions_count == 0:
            response = """📊 让我们开始记录你的成长轨迹吧！

目前我还没有足够的数据来分析你的进展。建议我们从以下几个方面开始：

1. 设定一个明确的学习目标
2. 每周进行2-3次深度反思
3. 记录你的学习心得和情感变化

准备好开始这个美好的成长之旅了吗？🚀"""
        else:
            mood_emoji = "😊" if avg_mood >= 8 else "😐" if avg_mood >= 6 else "😔"
            
            response = f"""📈 你的成长数据报告：

✨ 近30天学习会话：{sessions_count} 次
{mood_emoji} 平均心情指数：{avg_mood:.1f}/10
🎯 达成里程碑：{milestones_count} 个

{self.generate_progress_insight(sessions_count, avg_mood, milestones_count)}

继续保持这种积极的学习态度！每一次对话都是成长的种子。🌟"""
        
        return Reply(ReplyType.TEXT, response)
    
    def generate_progress_insight(self, sessions, mood, milestones):
        """生成进度洞察"""
        if sessions >= 20:
            return "🎉 你的学习频率很高，这种持续性是蜕变的关键！"
        elif sessions >= 10:
            return "👍 你正在建立良好的学习习惯，继续保持！"
        else:
            return "💪 增加学习频率会让蜕变更明显，试试每周3次深度对话？"
    
    def save_learning_record(self, user_id, content):
        """保存学习记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.datetime.now()
        cursor.execute('''
            INSERT INTO learning_records 
            (user_id, session_date, topic, insights, created_at) 
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, now.date(), "反思记录", content, now))
        
        conn.commit()
        conn.close()


# ==================== 2. 专属插件系统 ====================
# plugins/coach_toolkit/coach_toolkit.py

import plugins
from plugins import *
from bridge.context import ContextType  
from bridge.reply import Reply, ReplyType
import json
import sqlite3
from datetime import datetime, timedelta

@plugins.register(
    name="coach_toolkit",
    desc="AI教练工具包",
    version="1.0",
    author="专属AI教练",
    desire_priority=150
)
class CoachToolkitPlugin(Plugin):
    
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[CoachToolkit] AI教练工具包已加载")
    
    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT:
            return
            
        content = e_context['context'].content.strip()
        user_id = e_context['context'].kwargs.get('session_id', 'default')
        
        # 命令处理
        if content.startswith("/"):
            command = content[1:].split()[0]
            args = content[1:].split()[1:] if len(content.split()) > 1 else []
            
            if command == "goals":
                reply = self.handle_goals_command(args, user_id)
            elif command == "mood":
                reply = self.handle_mood_command(args, user_id)
            elif command == "insights":
                reply = self.handle_insights_command(user_id)
            elif command == "celebrate":
                reply = self.handle_celebrate_command(args, user_id)
            elif command == "help":
                reply = self.get_help_text()
            else:
                return
                
            e_context['reply'] = Reply(ReplyType.TEXT, reply)
            e_context.action = EventAction.BREAK_PASS
    
    def handle_goals_command(self, args, user_id):
        """处理目标设置命令"""
        if not args:
            return """🎯 目标设置指南：

/goals set "你的目标描述" - 设置新目标
/goals list - 查看当前目标  
/goals update "目标ID" "新描述" - 更新目标
/goals complete "目标ID" - 标记完成

例如：/goals set "30天内掌握Python基础语法" """
        
        action = args[0]
        if action == "set":
            goal_text = " ".join(args[1:]).strip('"')
            return self.set_goal(user_id, goal_text)
        elif action == "list":
            return self.list_goals(user_id)
        # ... 其他goal操作
    
    def handle_mood_command(self, args, user_id):
        """处理心情记录命令"""
        if not args:
            return """😊 心情记录使用说明：

/mood 8 "今天学会了新技能，很有成就感"
/mood check - 查看心情趋势

心情指数范围：1-10分"""
        
        if args[0] == "check":
            return self.check_mood_trend(user_id)
        else:
            try:
                score = int(args[0])
                note = " ".join(args[1:]).strip('"') if len(args) > 1 else ""
                return self.record_mood(user_id, score, note)
            except ValueError:
                return "请输入有效的心情分数（1-10）"
    
    def record_mood(self, user_id, score, note):
        """记录心情"""
        if not 1 <= score <= 10:
            return "心情分数应该在1-10之间"
            
        # 这里应该保存到数据库
        mood_emoji = ["😢", "😔", "😐", "🙂", "😊", "😃", "🎉"][min(score//2, 6)]
        
        return f"""心情记录成功！{mood_emoji}

分数：{score}/10
备注：{note}

记住，情绪是学习过程的重要指标。继续保持觉察！✨"""

    def get_help_text(self, **kwargs):
        return """🛠️ AI教练工具包命令：

📋 目标管理：
/goals set "目标" - 设置目标
/goals list - 查看目标列表

😊 情绪跟踪：  
/mood 8 "心情备注" - 记录心情
/mood check - 查看心情趋势

💡 学习洞察：
/insights - 获取个人学习分析

🎉 庆祝成就：
/celebrate "成就描述" - 记录里程碑

更多功能正在开发中..."""


# ==================== 3. 自定义消息处理器 ====================
# bridge/coach_bridge.py

from bridge.bridge import Bridge
from bridge.reply import Reply, ReplyType
from common.log import logger
import re

class CoachBridge(Bridge):
    """专属教练桥接器"""
    
    def __init__(self):
        super().__init__()
        self.empathy_responses = [
            "我能理解你的感受",
            "这听起来确实是个挑战",
            "你的想法很有价值",
            "我能感受到你的困惑"
        ]
    
    def preprocess_query(self, query, context):
        """预处理用户输入"""
        # 情感检测和共情回应
        if self.detect_negative_emotion(query):
            query = self.add_empathy_response(query)
        
        # 学习术语标准化
        query = self.normalize_learning_terms(query)
        
        return query
    
    def detect_negative_emotion(self, text):
        """检测负面情绪"""
        negative_patterns = [
            r"(困惑|迷茫|不知道|焦虑|担心|害怕)",
            r"(失败|错误|挫折|失望)",
            r"(太难|不行|不会|不懂)"
        ]
        return any(re.search(pattern, text) for pattern in negative_patterns)
    
    def add_empathy_response(self, query):
        """添加共情回应"""
        import random
        empathy = random.choice(self.empathy_responses)
        return f"[内心感受：{empathy}] {query}"
    
    def normalize_learning_terms(self, text):
        """标准化学习术语"""
        replacements = {
            "学不会": "在学习过程中遇到困难",
            "太笨": "学习方式需要调整",
            "没天赋": "还没找到合适的学习路径"
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def postprocess_reply(self, reply, context):
        """后处理AI回复"""
        if reply.type == ReplyType.TEXT:
            # 添加个性化签名
            reply.content += "\n\n💙 你的专属AI教练"
            
            # 添加行动引导
            if "？" not in reply.content:
                reply.content += "\n\n你对此有什么想法呢？"
        
        return reply


# ==================== 4. 启动配置 ====================
# start_coach.py

"""
专属AI教练启动脚本
使用方法：python start_coach.py
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import conf
from common.log import logger
from bot.coach.coach_bot import CoachBot
from bridge.coach_bridge import CoachBridge  
from channel.web.web_channel import WebChannel

def start_coach_system():
    """启动专属AI教练系统"""
    
    # 使用自定义配置
    coach_config = {
        "channel_type": "web",
        "model": "Pro/deepseek-ai/DeepSeek-V3", 
        "character_desc": """你是专属AI教练，基于蜕变式学习理念。
        
核心原则：
1. 蜕变式学习注重内在转变，不只是知识积累
2. 每个人都有独特的学习路径和节奏
3. 情感支持和理性分析同等重要
4. 实践应用比理论记忆更有价值

回应风格：
- 温暖而专业，像朋友一样真诚
- 善于提出启发性问题
- 关注学习者的情感体验
- 提供具体可行的建议""",
        "single_chat_prefix": [""],
        "single_chat_reply_prefix": "",
        "web_port": 9899,
        "debug": True
    }
    
    # 更新配置
    for key, value in coach_config.items():
        conf()[key] = value
    
    logger.info("🚀 启动专属AI教练系统...")
    logger.info("💻 Web界面地址: http://localhost:9899/chat")
    logger.info("🎯 系统基于蜕变式学习理念")
    
    # 启动Web通道
    channel = WebChannel()
    channel.startup()

if __name__ == "__main__":
    start_coach_system()


# ==================== 5. 配置文件 ====================
# config-coach.json

{
  "channel_type": "web",
  "model": "Pro/deepseek-ai/DeepSeek-V3",
  "open_ai_api_key": "YOUR_API_KEY_HERE",
  "open_ai_api_base": "https://api.siliconflow.cn",
  
  "character_desc": "你是基于蜕变式学习核心理念的专属AI教练...",
  
  "single_chat_prefix": [""],
  "single_chat_reply_prefix": "",
  
  "plugins": ["coach_toolkit"],
  "plugin_trigger_prefix": "/",
  
  "web_port": 9899,
  "debug": true,
  
  "coach_settings": {
    "enable_progress_tracking": true,
    "enable_mood_analysis": true,
    "enable_goal_management": true,
    "empathy_level": "high",
    "coaching_style": "transformative_learning"
  }
}

# 使用说明：
# 1. 将以上代码文件放到对应目录
# 2. 配置你的API密钥
# 3. 运行：python start_coach.py
# 4. 访问：http://localhost:9899/chat
# 5. 开始与你的专属AI教练对话！ 