import os
from pathlib import Path
from mcp.types import CallToolResult, TextContent


def make_error(error_text: str) -> CallToolResult:
    return CallToolResult(
        isError=True,
        content=[TextContent(type="text", text=error_text)],
    )


def is_file_writeable(path: Path) -> bool:
    if path.exists():
        return os.access(path, os.W_OK)
    parent_dir = path.parent
    return os.access(parent_dir, os.W_OK)
