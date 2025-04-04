# Eleven Labs MCP Server

[![Discord](https://badgen.net/badge/black/ElevenLabs/icon?icon=discord&label)](https://discord.gg/elevenlabs)
[![Twitter](https://badgen.net/badge/black/elevenlabsio/icon?icon=twitter&label)](https://x.com/ElevenLabsDevs)
[![PyPI - Format](https://img.shields.io/pypi/format/elevenlabs-mcp)](http://pypi.org/project/elevenlabs-mcp) [![PyPI - Version](https://img.shields.io/pypi/v/elevenlabs-mcp)](https://pypi.org/project/elevenlabs-mcp)


Official Eleven Labs Model Context Protocol (MCP) server that enables interaction with powerful text-to-speech and audio processing APIs. This server allows MCP clients like [Claude Desktop](https://www.anthropic.com/claude), [Cursor](https://www.cursor.so), [Windsurf](https://codeium.com/windsurf), [OpenAI Agents](https://github.com/openai/openai-agents-python) and others to generate speech, clone voices, transcribe audio, and more.

## Quick Start with Claude

1. Get your API key from [Eleven Labs](https://elevenlabs.io/). There is a generous free tier of 10k credits per month.
2. Install `elevenlabs_mcp` module with `pip install elevenlabs-mcp`.
3. Install the MCP server in Claude Desktop by running `python -m elevenlabs_mcp --api-key={{PUT_YOUR_API_KEY_HERE}}`.
4. Restart Claude Desktop.

## Other MCP clients
For other clients like Cursor and Windsurf, run `python -m elevenlabs_mcp --api-key={{PUT_YOUR_API_KEY_HERE}} --print` to get the configuration. Paste it into appropriate configuration directory specified by your MCP client.


That's it! Your MCP client can now interact with Eleven Labs through these tools:

- `text_to_speech`: Convert text to speech using a specified voice
- `voice_clone`: Clone a voice using provided audio files
- `speech_to_text`: Transcribe speech from an audio file
- `text_to_sound_effects`: Generate sound effects from text descriptions
- `isolate_audio`: Isolate audio from a file
- `check_subscription`: Check your Eleven Labs subscription status
- `list_voices`: Get a list of all available voices
- `search_voices`: Search through your voice library for a specific voice
- `get_voice`: Retrieve a specific voice by ID
- `speech_to_speech`: Transform audio from one voice to another using provided audio files
- `text_to_voice`: Design a voice via a text prompt
- `create_voice_from_preview`: Using an ID from `text_to_voice`, save your generated to your library
- `create_agent`: Create a Conversational AI agent
- `list_agents`: Retrieve a list of all available Conversational AI agents
- `get_agent`: Retrieve a specific agent by ID
- `add_knowledge_base_to_agent`: Add knowledge to your Conversational AI agent. Useful for piping LLM deep research into an agent's knowledge base
- `play_audio`: Play audio directly from the client

## Example Usage

Try asking Claude:
- "Can you convert this text to speech using a British accent?"
- "What voices are available for text-to-speech?"
- "Can you transcribe this audio file for me?"
- "Generate some rain sound effects"
- "Play that generated voice clip for me"
- "Generate the voice of a jolly giant"


## Optional features

You can add the `ELEVENLABS_MCP_BASE_PATH` environment variable to the `claude_desktop_config.json` to specify the base path MCP server should look for and output files specified with relative paths.

## Contributing

If you want to contribute or run from source:

1. Clone the repository:
```bash
git clone https://github.com/jacekduszenko/elevenlabs-mcp.git
cd elevenlabs-mcp
```

2. Create a virtual environment and install dependencies [using uv](https://github.com/astral-sh/uv):
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

3. Copy `.env.example` to `.env` and add your ElevenLabs API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

4. Install the server in Claude Desktop: `mcp install server.py`.

5. Debug and test locally with MCP Inspector: `mcp dev server.py`

## Requirements

- Python 3.11 or higher
- Dependencies:
  - mcp>=0.1.0
  - fastapi==0.109.2
  - uvicorn==0.27.1
  - python-dotenv==1.0.1
  - pydantic>=2.6.1
  - httpx==0.28.1
  - elevenlabs>=1.56.0

## Troubleshooting

Logs when running with Claude Desktop can be found at:
- **Windows**: `%APPDATA%\Claude\logs\mcp-server-elevenlabs.log`
- **macOS**: `~/Library/Logs/Claude/mcp-server-elevenlabs.log`

### Timeouts when using certain tools

Certain ElevenLabs API operations like voice design and audio isolation can take a long time to resolve. When using the MCP inspector in dev mode you might get timeout errors, despite the tool completing its intended task.

This shouldn't occur when using a client like Claude.
