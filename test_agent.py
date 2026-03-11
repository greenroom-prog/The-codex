import asyncio
import os
from dotenv import load_dotenv
from agents.architect import Architect

load_dotenv()

async def main():
    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("ERROR: No API key found in .env file!")
        return
    
    # Create architect and run task
    architect = Architect()
    result = await architect.execute_task("Write a Python function to check if a number is prime")
    print(f"\n✅ RESULT:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
