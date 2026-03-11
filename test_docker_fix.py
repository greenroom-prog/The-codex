import asyncio
from tools.code_executor import CodeExecutor

async def test():
    executor = CodeExecutor()
    
    print("🧹 Cleaning up old containers...")
    executor.cleanup_all_containers()
    
    print("\n✅ Testing new executor...")
    code = """
print("Hello from Docker!")
print("Testing: 2 + 2 =", 2 + 2)
"""
    
    result = await executor.execute_python(code, "test")
    
    if result.success:
        print(f"\n✅ SUCCESS!")
        print(f"Output:\n{result.output}")
    else:
        print(f"\n❌ Error: {result.error}")
    
    print("\n🧹 Final cleanup...")
    executor.cleanup_all_containers()
    print("✅ No zombie containers!")

asyncio.run(test())
