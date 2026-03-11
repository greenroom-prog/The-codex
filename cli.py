#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import typer
from rich.console import Console
from dotenv import load_dotenv
from agents.architect import Architect

load_dotenv()
app = typer.Typer()
console = Console()

@app.command()
def run(task: str):
    """Execute a task"""
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env[/red]")
        raise typer.Exit(1)
    
    async def execute():
        architect = Architect()
        result = await architect.execute_task(task=task)
        console.print(f"\n[green]{result}[/green]")
    
    asyncio.run(execute())

if __name__ == "__main__":
    app()
