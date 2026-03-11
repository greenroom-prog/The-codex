import asyncio
import docker
import tempfile
import time
from pathlib import Path
from core.protocol import ToolResult

class CodeExecutor:
    """Sandboxed code execution with proper cleanup"""
    
    def __init__(self, timeout: int = 30, memory_limit: str = "512m"):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.client = None
        self._init_docker()
    
    def _init_docker(self):
        """Initialize Docker client"""
        try:
            self.client = docker.from_env()
            try:
                self.client.images.get("python:3.11-slim")
            except docker.errors.ImageNotFound:
                print("Pulling python:3.11-slim...")
                self.client.images.pull("python:3.11-slim")
        except Exception as e:
            print(f"Warning: Docker not available - {e}")
            self.client = None
    
    async def execute_python(self, code: str, call_id: str, install_packages: list = None) -> ToolResult:
        """Execute Python code with PROPER cleanup"""
        start_time = time.time()
        
        if not self.client:
            return ToolResult(
                call_id=call_id,
                success=False,
                output="",
                error="Docker not available",
                execution_time=0.0
            )
        
        container = None
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                code_file = Path(tmpdir) / "script.py"
                code_file.write_text(code)
                
                cmd_parts = []
                if install_packages:
                    pkg_str = " ".join(install_packages)
                    cmd_parts.append(f"pip install --quiet {pkg_str} &&")
                cmd_parts.append("python /code/script.py")
                command = " ".join(cmd_parts)
                
                # Run with auto_remove=True for cleanup
                container = self.client.containers.run(
                    "python:3.11-slim",
                    command=["sh", "-c", command],
                    volumes={tmpdir: {"bind": "/code", "mode": "ro"}},
                    mem_limit=self.memory_limit,
                    detach=True,
                    remove=False  # Manual removal for better control
                )
                
                # Wait with timeout
                try:
                    result = container.wait(timeout=self.timeout)
                    logs = container.logs().decode("utf-8")
                    execution_time = time.time() - start_time
                    
                    # Clean up container IMMEDIATELY
                    try:
                        container.remove(force=True)
                    except:
                        pass  # Already removed
                    
                    if result["StatusCode"] == 0:
                        return ToolResult(
                            call_id=call_id,
                            success=True,
                            output=logs,
                            execution_time=execution_time
                        )
                    else:
                        return ToolResult(
                            call_id=call_id,
                            success=False,
                            output=logs,
                            error=f"Exit code: {result['StatusCode']}",
                            execution_time=execution_time
                        )
                
                except Exception as e:
                    # Force stop and remove on ANY error
                    if container:
                        try:
                            container.stop(timeout=1)
                            container.remove(force=True)
                        except:
                            pass
                    
                    return ToolResult(
                        call_id=call_id,
                        success=False,
                        output="",
                        error=f"Execution error: {str(e)}",
                        execution_time=time.time() - start_time
                    )
        
        except Exception as e:
            # Final cleanup attempt
            if container:
                try:
                    container.remove(force=True)
                except:
                    pass
            
            return ToolResult(
                call_id=call_id,
                success=False,
                output="",
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def cleanup_all_containers(self):
        """Emergency cleanup - remove all stopped containers"""
        if not self.client:
            return
        
        try:
            # Remove all stopped containers
            for container in self.client.containers.list(all=True, filters={"status": "exited"}):
                try:
                    container.remove(force=True)
                    print(f"Cleaned up container: {container.id[:12]}")
                except:
                    pass
        except Exception as e:
            print(f"Cleanup error: {e}")
