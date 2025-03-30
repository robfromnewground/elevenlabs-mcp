import os
from pathlib import Path
from typing import Optional
from datetime import datetime


class ElevenLabsMcpError(Exception):
    pass


def make_error(error_text: str):
    raise ElevenLabsMcpError(error_text)


def is_file_writeable(path: Path) -> bool:
    if path.exists():
        return os.access(path, os.W_OK)
    parent_dir = path.parent
    return os.access(parent_dir, os.W_OK)


def make_output_file(tool: str, text: str, output_path: Path) -> Path:
    output_file_name = f"{tool}_{text[:5].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    return output_path / output_file_name


def make_output_path(output_directory: str, base_path: Optional[str] = None) -> Path:
    output_path = None
    if output_directory == "":
        output_path = Path.home() / "Desktop"
    elif not os.path.isabs(output_directory) and not base_path:
        make_error(
            "Output directory must be an absolute path if ELEVENLABS_MCP_BASE_PATH is not set"
        )
    elif not os.path.isabs(output_directory) and base_path:
        output_path = Path(os.path.expanduser(base_path)) / Path(output_directory)
    else:
        output_path = Path(os.path.expanduser(output_directory))
    if not is_file_writeable(output_path):
        make_error(f"Directory ({output_path}) is not writeable")
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
