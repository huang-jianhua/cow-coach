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
import random

class CoachSession:
    """专属教练会话类"""
    def __init__(self, session_id, system_prompt=None):
        self.session_id = session_id
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

class CoachBot(Bot):
    """专属AI教练机器人"""
    
    def __init__(self):
        super().__init__()
        # 使用标准的ChatGPT会话管理
        from bot.chatgpt.chat_gpt_session import ChatGPTSession
        self.sessions = SessionManager(ChatGPTSession, model=conf().get("model") or "gpt-3.5-turbo")
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
        
        # 目标管理表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                title TEXT,
                description TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("[CoachBot] 数据库初始化完成")
        
    def reply(self, query, context=None):
        try:
            user_id = context.get('session_id', 'default_user') if context else 'default_user'
            
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
                return self.handle_coaching_dialogue(query, user_id, context)
                
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
        
        question = random.choice(reflection_questions)
        
        response = f"""💡 很棒的反思！我能感受到你的成长。

{question}

蜕变式学习的核心就是这种深度的自我觉察。每一次反思都是在为内在的转变播种。继续分享你的想法，让我们一起深入探索。🌱"""
        
        return Reply(ReplyType.TEXT, response)
    
    def handle_goal_setting(self, query, user_id):
        """处理目标设置"""
        # 提取目标信息
        goal_text = query
        
        # 保存目标到数据库
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.datetime.now()
        cursor.execute('''
            INSERT INTO goals (user_id, title, description, created_at) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, "新目标", goal_text, now))
        
        conn.commit()
        conn.close()
        
        response = f"""🎯 很好！我听到了你的目标。

让我们一起制定一个实现路径：

1. 你希望在多长时间内达成这个目标？
2. 你认为最大的挑战会是什么？
3. 你已经具备了哪些相关的基础？

记住，蜕变式学习强调的是过程中的内在成长，而不仅仅是结果。让我们一步步来！✨"""
        
        return Reply(ReplyType.TEXT, response)
    
    def handle_coaching_dialogue(self, query, user_id, context):
        """处理常规教练对话"""
        # 使用原有的ChatGPT对话系统，但加入教练特色
        try:
            # 获取或创建会话
            session = self.sessions.session_query(query, context.get('session_id') if context else user_id)
            
            # 这里可以加入更多的教练逻辑处理
            from bot.chatgpt.chat_gpt_bot import ChatGPTBot
            gpt_bot = ChatGPTBot()
            
            # 调用原始的GPT对话，但会使用我们的专属教练persona
            response = gpt_bot.reply(query, context)
            
            return response
            
        except Exception as e:
            logger.error(f"Coaching dialogue error: {e}")
            return Reply(ReplyType.TEXT, "让我们换个角度来思考这个问题...")
    
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
        
        # 获取目标数量
        cursor.execute('''
            SELECT COUNT(*) FROM goals WHERE user_id = ? AND status = 'active'
        ''', (user_id,))
        active_goals = cursor.fetchone()[0]
        
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
📋 活跃目标：{active_goals} 个

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
