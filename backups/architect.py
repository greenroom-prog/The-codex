import asyncio
from core.protocol import AgentConfig, AgentRole, ToolType
from agents.base_agent import Agent

class Architect:
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.model = model
        self.role_configs = {
            AgentRole.CODER: {
                "system_prompt": "You are an expert software engineer. Write clean, production-quality code with proper error handling and documentation.",
                "allowed_tools": [ToolType.CODE_EXEC, ToolType.FILE_OPS],
                "temperature": 0.3
            },
        }
    
    async def execute_task(self, task: str) -> str:
        config = AgentConfig(
            role=AgentRole.CODER,
            model=self.model,
            temperature=0.3,
            max_iterations=10,
            allowed_tools=[ToolType.CODE_EXEC, ToolType.FILE_OPS],
            system_prompt=self.role_configs[AgentRole.CODER]["system_prompt"]
        )
        agent = Agent(config)
        print(f"\n🤖 Spawning agent...")
        print(f"📋 Task: {task}\n")
        result = await agent.run(task)
        print(f"\n✅ Agent completed")
        return result

async def main():
    architect = Architect()
    result = await architect.execute_task("Write a Python function that calculates fibonacci numbers")
    print(f"\nResult:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
