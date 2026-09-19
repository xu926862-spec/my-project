import os
from anthropic import Anthropic

class ClaudeClient:
    """满级 Claude 客户端 - 内置总工程师提示词和多模型支持"""
    
    def __init__(self, model="claude-opus-5", system_prompt=None):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY 环境变量未设置")
        
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.conversation_history = []
        
        # 默认系统提示词 - 满级工程师风格
        self.system_prompt = system_prompt or """你是一个满级的全栈工程师和架构师。
你精通：
- 软件架构设计和系统设计
- 多种编程语言和框架
- 云计算、容器化、微服务
- 数据库设计和优化
- DevOps 和基础设施即代码
- 性能优化和安全实践

回答时要：
1. 深度分析问题
2. 给出最佳实践方案
3. 考虑可扩展性和可维护性
4. 提供具体的代码示例和实现建议"""
    
    def send(self, message):
        """发送消息并获取回复"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def set_system_prompt(self, prompt):
        """修改系统提示词"""
        self.system_prompt = prompt
    
    def get_history(self):
        """获取对话历史"""
        return self.conversation_history
