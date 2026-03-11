import asyncio
from datetime import datetime
from typing import Optional
from core.protocol import AgentConfig, AgentState, Message
from core.llm_engine import LLMEngine
from tools.code_executor import CodeExecutor
from tools.file_ops import FileOperations


class Agent:
    """Core agent with tool execution capabilities"""
    
    def __init__(self, config):
        self.config = config
        self.state = AgentState(config=config)
        self.llm = LLMEngine(config)
        self.code_executor = CodeExecutor()
        self.file_ops = FileOperations()
    
    async def run(self, task: str, max_iterations = None) -> str:
        """Execute agent task - simplified for solid foundation"""
        self.state.status = "thinking"
        
        prompt = f"""Write a complete, working Python program for this task: {task}

Requirements:
- Include all necessary imports
- Add test cases at the end
- Make it production-ready with error handling
- Output ONLY the Python code, nothing else"""
        
        try:
            code = await self.llm.generate(
                messages=[Message(role="user", content=prompt)],
                response_model=None
            )
            
            result = await self.code_executor.execute_python(code=code, call_id="exec")
            
            if result.success:
                return f"✅ SUCCESS!\n\nCode:\n{code}\n\nOutput:\n{result.output}"
            else:
                return f"❌ Error:\n{result.error}\n\nCode was:\n{code}"
                
        except Exception as e:
            return f"Failed: {e}"
