import asyncio
import os
from dotenv import load_dotenv
from agents.architect import Architect

load_dotenv()

async def main():
    architect = Architect()
    result = await architect.execute_task("Write a function to reverse a string")
    print(f"\n{result}")

asyncio.run(main())
