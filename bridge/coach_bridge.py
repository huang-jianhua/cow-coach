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
