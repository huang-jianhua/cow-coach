# plugins/coach_toolkit/coach_toolkit.py

import plugins
from plugins import *
from bridge.context import ContextType  
from bridge.reply import Reply, ReplyType
from common.log import logger
import json
import sqlite3
import os
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
        self.db_path = "data/coach.db"
        self.init_database()
        logger.info("[CoachToolkit] AI教练工具包已加载")
    
    def init_database(self):
        """确保数据库存在"""
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
        logger.info("[CoachToolkit] 数据库初始化完成")
    
    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT:
            return
            
        content = e_context['context'].content.strip()
        user_id = e_context['context'].kwargs.get('session_id', 'default')
        
        # 命令处理
        if content.startswith("/"):
            command = content[1:].split()[0]
            args = content[1:].split()[1:] if len(content.split()) > 1 else []
            
            try:
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
            except Exception as e:
                logger.error(f"[CoachToolkit] 命令处理错误: {e}")
                e_context['reply'] = Reply(ReplyType.TEXT, "抱歉，处理命令时出现了问题，请稍后再试。")
                e_context.action = EventAction.BREAK_PASS
    
    def handle_goals_command(self, args, user_id):
        """处理目标设置命令"""
        if not args:
            return """🎯 目标设置指南：

/goals set "你的目标描述" - 设置新目标
/goals list - 查看当前目标  
/goals update [目标ID] "新描述" - 更新目标
/goals complete [目标ID] - 标记完成

例如：/goals set "30天内掌握Python基础语法" """
        
        action = args[0]
        if action == "set":
            goal_text = " ".join(args[1:]).strip('"')
            if not goal_text:
                return "请提供目标描述，例如：/goals set \"学会Python编程\""
            return self.set_goal(user_id, goal_text)
        elif action == "list":
            return self.list_goals(user_id)
        elif action == "update" and len(args) >= 3:
            goal_id = args[1]
            new_text = " ".join(args[2:]).strip('"')
            return self.update_goal(user_id, goal_id, new_text)
        elif action == "complete" and len(args) >= 2:
            goal_id = args[1]
            return self.complete_goal(user_id, goal_id)
        else:
            return "命令格式错误，请输入 /goals 查看帮助。"
    
    def set_goal(self, user_id, goal_text):
        """设置新目标"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now()
            cursor.execute('''
                INSERT INTO goals (user_id, title, description, created_at) 
                VALUES (?, ?, ?, ?)
            ''', (user_id, goal_text[:50], goal_text, now))
            
            goal_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return f"""🎯 目标设置成功！

目标ID: {goal_id}
内容: {goal_text}
创建时间: {now.strftime('%Y-%m-%d %H:%M')}

记住：蜕变式学习注重过程中的内在成长。让我们一步步实现这个目标！✨

使用 /goals list 查看所有目标"""
        
        except Exception as e:
            logger.error(f"设置目标失败: {e}")
            return "设置目标时出现错误，请稍后再试。"
    
    def list_goals(self, user_id):
        """列出用户目标"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, description, status, created_at, completed_at
                FROM goals WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            
            goals = cursor.fetchall()
            conn.close()
            
            if not goals:
                return """📋 你还没有设置任何目标。

使用 /goals set "你的目标" 来设置第一个目标吧！

记住：明确的目标是蜕变的起点。✨"""
            
            response = "📋 你的目标列表：\n\n"
            
            active_goals = []
            completed_goals = []
            
            for goal in goals:
                goal_id, title, description, status, created_at, completed_at = goal
                created_date = datetime.fromisoformat(created_at).strftime('%m-%d')
                
                if status == 'active':
                    active_goals.append(f"🎯 [{goal_id}] {title}\n   📝 {description}\n   📅 {created_date}")
                else:
                    complete_date = datetime.fromisoformat(completed_at).strftime('%m-%d') if completed_at else "未知"
                    completed_goals.append(f"✅ [{goal_id}] {title} (完成于 {complete_date})")
            
            if active_goals:
                response += "🔥 进行中：\n" + "\n\n".join(active_goals) + "\n\n"
            
            if completed_goals:
                response += "🎉 已完成：\n" + "\n".join(completed_goals)
            
            response += f"\n\n💡 使用 /goals complete [ID] 标记完成"
            
            return response
            
        except Exception as e:
            logger.error(f"获取目标列表失败: {e}")
            return "获取目标列表时出现错误，请稍后再试。"
    
    def complete_goal(self, user_id, goal_id):
        """完成目标"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查目标是否存在
            cursor.execute('''
                SELECT title, description FROM goals 
                WHERE id = ? AND user_id = ? AND status = 'active'
            ''', (goal_id, user_id))
            
            goal = cursor.fetchone()
            if not goal:
                conn.close()
                return f"未找到ID为 {goal_id} 的活跃目标。"
            
            title, description = goal
            now = datetime.now()
            
            # 标记完成
            cursor.execute('''
                UPDATE goals SET status = 'completed', completed_at = ?
                WHERE id = ? AND user_id = ?
            ''', (now, goal_id, user_id))
            
            # 添加里程碑
            cursor.execute('''
                INSERT INTO milestones (user_id, title, description, achieved_at, celebration_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, f"完成目标: {title}", description, now, "恭喜你完成了这个重要目标！"))
            
            conn.commit()
            conn.close()
            
            return f"""🎉 恭喜！目标达成！

✅ {title}
📝 {description}
🕐 完成时间: {now.strftime('%Y-%m-%d %H:%M')}

这是一个重要的里程碑！蜕变式学习的精髓就在于这种持续的突破。

你想分享一下完成这个目标后的感受吗？这种内在的体验正是真正成长的标志。✨"""
            
        except Exception as e:
            logger.error(f"完成目标失败: {e}")
            return "标记目标完成时出现错误，请稍后再试。"
    
    def handle_mood_command(self, args, user_id):
        """处理心情记录命令"""
        if not args:
            return """😊 心情记录使用说明：

/mood 8 "今天学会了新技能，很有成就感"
/mood check - 查看心情趋势

心情指数范围：1-10分
记录情绪是自我觉察的重要一步！"""
        
        if args[0] == "check":
            return self.check_mood_trend(user_id)
        else:
            try:
                score = int(args[0])
                note = " ".join(args[1:]).strip('"') if len(args) > 1 else ""
                return self.record_mood(user_id, score, note)
            except ValueError:
                return "请输入有效的心情分数（1-10），例如：/mood 8 \"今天感觉很好\""
    
    def record_mood(self, user_id, score, note):
        """记录心情"""
        if not 1 <= score <= 10:
            return "心情分数应该在1-10之间"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now()
            cursor.execute('''
                INSERT INTO learning_records 
                (user_id, session_date, topic, insights, mood_score, created_at) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, now.date(), "心情记录", note, score, now))
            
            conn.commit()
            conn.close()
            
            mood_emoji = ["😢", "😔", "😟", "😐", "🙂", "😊", "😃", "😄", "😁", "🎉"][score-1]
            
            return f"""心情记录成功！{mood_emoji}

分数：{score}/10
时间：{now.strftime('%Y-%m-%d %H:%M')}
备注：{note}

记住，情绪是学习过程的重要指标。继续保持这种自我觉察！✨

使用 /mood check 查看心情趋势"""
            
        except Exception as e:
            logger.error(f"记录心情失败: {e}")
            return "记录心情时出现错误，请稍后再试。"
    
    def check_mood_trend(self, user_id):
        """检查心情趋势"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取最近30天的心情记录
            cursor.execute('''
                SELECT mood_score, session_date, insights
                FROM learning_records 
                WHERE user_id = ? AND mood_score IS NOT NULL 
                AND session_date >= date('now', '-30 days')
                ORDER BY session_date DESC
                LIMIT 10
            ''', (user_id,))
            
            records = cursor.fetchall()
            
            if not records:
                conn.close()
                return """📊 还没有心情记录

开始记录你的情绪变化吧！使用：
/mood 8 "今天的感受"

情绪跟踪是自我成长的重要工具。✨"""
            
            # 计算平均值和趋势
            scores = [r[0] for r in records]
            avg_score = sum(scores) / len(scores)
            
            recent_3 = scores[:3] if len(scores) >= 3 else scores
            older_3 = scores[-3:] if len(scores) >= 6 else scores[3:] if len(scores) > 3 else []
            
            trend = ""
            if older_3:
                recent_avg = sum(recent_3) / len(recent_3)
                older_avg = sum(older_3) / len(older_3)
                if recent_avg > older_avg + 0.5:
                    trend = "📈 上升趋势 - 很棒！"
                elif recent_avg < older_avg - 0.5:
                    trend = "📉 下降趋势 - 需要关注"
                else:
                    trend = "📊 相对稳定"
            
            mood_emoji = "😊" if avg_score >= 8 else "😐" if avg_score >= 6 else "😔"
            
            response = f"""📊 你的心情趋势分析：

{mood_emoji} 平均心情指数：{avg_score:.1f}/10
📈 趋势：{trend}
📅 记录天数：{len(records)} 天

最近记录："""
            
            for i, (score, date, note) in enumerate(records[:5]):
                mood_emoji = ["😢", "😔", "😟", "😐", "🙂", "😊", "😃", "😄", "😁", "🎉"][score-1]
                response += f"\n{mood_emoji} {score}/10 - {date} {note[:20]}{'...' if len(note) > 20 else ''}"
            
            response += "\n\n💡 持续的情绪觉察是内在成长的基础。继续保持记录！"
            
            conn.close()
            return response
            
        except Exception as e:
            logger.error(f"查看心情趋势失败: {e}")
            return "查看心情趋势时出现错误，请稍后再试。"
    
    def handle_insights_command(self, user_id):
        """处理学习洞察命令"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取用户数据
            cursor.execute('''
                SELECT COUNT(*) FROM learning_records 
                WHERE user_id = ? AND session_date >= date('now', '-30 days')
            ''', (user_id,))
            recent_sessions = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT AVG(mood_score) FROM learning_records 
                WHERE user_id = ? AND mood_score IS NOT NULL
            ''', (user_id,))
            avg_mood = cursor.fetchone()[0] or 0
            
            cursor.execute('''
                SELECT COUNT(*) FROM goals WHERE user_id = ? AND status = 'completed'
            ''', (user_id,))
            completed_goals = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) FROM goals WHERE user_id = ? AND status = 'active'
            ''', (user_id,))
            active_goals = cursor.fetchone()[0]
            
            conn.close()
            
            # 生成个性化洞察
            insights = []
            
            if recent_sessions >= 10:
                insights.append("🔥 你的学习频率很高！这种持续性是蜕变的关键。")
            elif recent_sessions >= 5:
                insights.append("👍 你正在建立良好的学习习惯。")
            else:
                insights.append("💪 试试增加学习频率，每周2-3次深度对话效果更好。")
            
            if avg_mood >= 8:
                insights.append("😊 你的学习状态很积极！情绪是学习质量的重要指标。")
            elif avg_mood >= 6:
                insights.append("😐 情绪状态中等，关注一下是什么影响了你的学习感受。")
            else:
                insights.append("😔 注意情绪状态，可能需要调整学习方式或节奏。")
            
            if completed_goals > 0:
                insights.append(f"🎯 已完成 {completed_goals} 个目标，证明你的执行力很强！")
            
            if active_goals > 0:
                insights.append(f"📋 当前有 {active_goals} 个活跃目标，记得定期回顾进展。")
            
            response = f"""💡 你的个人学习洞察：

📊 数据概览：
• 近30天学习次数：{recent_sessions} 次
• 平均心情指数：{avg_mood:.1f}/10
• 完成目标：{completed_goals} 个
• 进行目标：{active_goals} 个

🎯 个性化建议：
"""
            
            for insight in insights:
                response += f"\n{insight}"
            
            response += """

🌟 蜕变式学习提醒：
真正的成长不仅在于知识的积累，更在于内在的转变。继续保持这种深度的自我觉察和反思！"""
            
            return response
            
        except Exception as e:
            logger.error(f"生成学习洞察失败: {e}")
            return "生成学习洞察时出现错误，请稍后再试。"
    
    def handle_celebrate_command(self, args, user_id):
        """处理庆祝成就命令"""
        if not args:
            return """🎉 庆祝成就使用说明：

/celebrate "我今天学会了新技能"
记录和庆祝每一个成长时刻！"""
        
        achievement = " ".join(args).strip('"')
        if not achievement:
            return "请描述你的成就，例如：/celebrate \"我完成了第一个项目\""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now()
            cursor.execute('''
                INSERT INTO milestones (user_id, title, description, achieved_at, celebration_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, "个人成就", achievement, now, "值得庆祝的成长时刻！"))
            
            conn.commit()
            conn.close()
            
            return f"""🎉 恭喜你的成就！

✨ {achievement}
🕐 时间：{now.strftime('%Y-%m-%d %H:%M')}

每一次成长都值得被看见和庆祝！这种积极的自我认可是持续进步的动力。

记住：蜕变式学习重视过程中的每一个突破，无论大小。继续保持这种成长的觉察！🌟"""
            
        except Exception as e:
            logger.error(f"记录庆祝失败: {e}")
            return "记录成就时出现错误，请稍后再试。"

    def get_help_text(self, **kwargs):
        help_text = """🛠️ AI教练工具包命令：
📋 目标管理：
/goals set "目标描述" - 设置新目标
/goals list - 查看目标列表
/goals complete [ID] - 标记目标完成
😊 情绪跟踪：
/mood 8 "心情备注" - 记录心情(1-10分)
/mood check - 查看心情趋势
💡 学习洞察：
/insights - 获取个人学习分析报告
🎉 庆祝成就：
/celebrate "成就描述" - 记录里程碑时刻
基于蜕变式学习理念，专注于内在成长！✨"""
        return help_text
