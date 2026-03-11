import os
import shutil
from pathlib import Path
from core.protocol import ToolResult
import time

class FileOperations:
    def __init__(self, workspace_root: str = "/tmp/architect_workspace"):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
    
    def _validate_path(self, path: str) -> Path:
        resolved = (self.workspace_root / path).resolve()
        if not str(resolved).startswith(str(self.workspace_root)):
            raise ValueError(f"Path escape attempt: {path}")
        return resolved
    
    async def create_file(self, path: str, content: str, call_id: str, overwrite: bool = False) -> ToolResult:
        start_time = time.time()
        try:
            file_path = self._validate_path(path)
            if file_path.exists() and not overwrite:
                return ToolResult(call_id=call_id, success=False, output="", error=f"File exists: {path}", execution_time=time.time() - start_time)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            return ToolResult(call_id=call_id, success=True, output=f"Created: {path}", execution_time=time.time() - start_time)
        except Exception as e:
            return ToolResult(call_id=call_id, success=False, output="", error=str(e), execution_time=time.time() - start_time)
