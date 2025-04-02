import os
import json
import subprocess
from pathlib import Path
import sys
from dotenv import load_dotenv
import argparse

load_dotenv()


def get_claude_config_path() -> Path | None:
    """Get the Claude config directory based on platform."""
    if sys.platform == "win32":
        path = Path(Path.home(), "AppData", "Roaming", "Claude")
    elif sys.platform == "darwin":
        path = Path(Path.home(), "Library", "Application Support", "Claude")
    elif sys.platform.startswith("linux"):
        path = Path(
            os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"), "Claude"
        )
    else:
        return None

    if path.exists():
        return path
    return None


def get_uv_path():
    result = subprocess.run(["which", "uv"], capture_output=True, text=True)
    return result.stdout.strip()


def generate_config():
    repo_dir = Path(__file__).resolve().parent
    server_path = repo_dir / "elevenlabs_mcp" / "server.py"
    uv_path = get_uv_path()
    api_key = os.environ.get("ELEVENLABS_API_KEY")

    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set")

    config = {
        "mcpServers": {
            "ElevenLabs": {
                "command": uv_path,
                "args": [
                    "run",
                    "--directory",
                    str(repo_dir / "elevenlabs_mcp"),
                    "--with",
                    "elevenlabs",
                    "--with",
                    "fastmcp",
                    "--with",
                    "fuzzywuzzy",
                    "--with",
                    "python-Levenshtein",
                    "--with",
                    "python-dotenv",
                    "--with",
                    "python-magic",
                    "--with",
                    "sounddevice",
                    "--with",
                    "soundfile",
                    "fastmcp",
                    "run",
                    str(server_path),
                ],
                "env": {"ELEVENLABS_API_KEY": api_key},
            }
        }
    }

    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print config to screen instead of writing to file",
    )
    args = parser.parse_args()

    config = generate_config()

    if args.print:
        print(json.dumps(config, indent=2))
    else:
        claude_path = get_claude_config_path()
        if claude_path is None:
            raise ValueError("Claude config path not found")
        print("Writing config to", claude_path / "claude_desktop_config.json")
        with open(claude_path / "claude_desktop_config.json", "w") as f:
            json.dump(config, f, indent=2)
