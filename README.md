![export](https://github.com/user-attachments/assets/ee379feb-348d-48e7-899c-134f7f7cd74f)

<div class="title-block" style="text-align: center;" align="center">

  [![Discord Community](https://img.shields.io/badge/discord-@elevenlabs-000000.svg?style=for-the-badge&logo=discord&labelColor=000)](https://discord.gg/elevenlabs)
  [![Twitter](https://img.shields.io/badge/Twitter-@elevenlabsio-000000.svg?style=for-the-badge&logo=twitter&labelColor=000)](https://x.com/ElevenLabsDevs)
  [![PyPI](https://img.shields.io/badge/PyPI-elevenlabs--mcp-000000.svg?style=for-the-badge&logo=pypi&labelColor=000)](https://pypi.org/project/elevenlabs-mcp)
  [![Tests](https://img.shields.io/badge/tests-passing-000000.svg?style=for-the-badge&logo=github&labelColor=000)](https://github.com/elevenlabs/elevenlabs-mcp-server/actions/workflows/test.yml)

</div>


<p align="center">
  Official ElevenLabs Model Context Protocol (MCP) server that enables interaction with powerful Text to Speech and audio processing APIs. This server allows MCP clients like <a href="https://www.anthropic.com/claude">Claude Desktop</a>, <a href="https://www.cursor.so">Cursor</a>, <a href="https://codeium.com/windsurf">Windsurf</a>, <a href="https://github.com/openai/openai-agents-python">OpenAI Agents</a> and others to generate speech, clone voices, transcribe audio, and more.
</p>

## Quick Start with Claude

1. Get your API key from [ElevenLabs](https://elevenlabs.io/). There is a free tier with 10k credits per month.
2. Install `elevenlabs_mcp` module with `pip install elevenlabs-mcp`.
3. Install the MCP server in Claude Desktop by running `python -m elevenlabs_mcp --api-key={{PUT_YOUR_API_KEY_HERE}}`.
4. Restart Claude Desktop.

If you're using Windows, you will have to enable "Developer Mode" in Claude Desktop to use the MCP server. Click "Help" in the hamburger menu in the top left and select "Enable Developer Mode".

## Other MCP clients

For other clients like Cursor and Windsurf, run `python -m elevenlabs_mcp --api-key={{PUT_YOUR_API_KEY_HERE}} --print` to get the configuration. Paste it into appropriate configuration directory specified by your MCP client.

That's it! Your MCP client can now interact with ElevenLabs through these tools:

- `text_to_speech`: Convert text to speech using a specified voice
- `voice_clone`: Clone a voice using provided audio files
- `speech_to_text`: Transcribe speech from an audio file
- `text_to_sound_effects`: Generate sound effects from text descriptions
- `isolate_audio`: Isolate audio from a file
- `check_subscription`: Check your ElevenLabs subscription status
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
- `make_outbound_call` - Make an outbound call via Twilio using an ElevenLabs agent
- `list_phone_numbers` - List all phone numbers associated with your ElevenLabs account

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
git clone https://github.com/elevenlabs/elevenlabs-mcp-server
cd elevenlabs-mcp-server
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

4. Run the tests to make sure everything is working:

```bash
./test.sh
# Or with options
./test.sh --verbose --fail-fast
```

5. Install the server in Claude Desktop: `mcp install elevenlabs_mcp/server.py`

6. Debug and test locally with MCP Inspector: `mcp dev elevenlabs_mcp/server.py`

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
