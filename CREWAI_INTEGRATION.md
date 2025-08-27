# ElevenLabs MCP Server - CrewAI Integration Guide

This enhanced ElevenLabs MCP server now supports **Streamable HTTP transport** for seamless integration with CrewAI and other MCP clients.

## 🚀 Quick Start

### Option 1: CrewAI MCPServerAdapter (Recommended)

```python
from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter

# Configure your deployed ElevenLabs MCP server
elevenlabs_params = {
    "url": "https://your-railway-app.railway.app/mcp",
    "transport": "streamable-http"
}

with MCPServerAdapter(elevenlabs_params) as elevenlabs_tools:
    print(f"Available ElevenLabs tools: {[tool.name for tool in elevenlabs_tools]}")
    
    voice_agent = Agent(
        role="Voice Content Creator",
        goal="Create high-quality audio content using ElevenLabs",
        backstory="An AI specialist in voice synthesis and audio processing",
        tools=elevenlabs_tools,  # All 22 ElevenLabs tools available!
        verbose=True
    )
    
    audio_task = Task(
        description="Convert text to speech: 'Hello from CrewAI with ElevenLabs!'",
        expected_output="Audio file created successfully",
        agent=voice_agent
    )
    
    crew = Crew(agents=[voice_agent], tasks=[audio_task])
    result = crew.kickoff()
```

## 🛠️ Deployment Options

### Railway Deployment (Recommended)

1. **Deploy to Railway:**
   ```bash
   # Your project already includes railway.toml
   # Just deploy using Railway CLI or connect your GitHub repo
   ```

2. **Set Environment Variables:**
   - `ELEVENLABS_API_KEY`: Your ElevenLabs API key
   - `PORT`: Automatically set by Railway (default: 3000)

3. **Configure Shared Volume (if using):**
   - Volume name: `shared-audio-storage`
   - Mount path: `/app/shared`
   - This enables persistent file storage across deployments

4. **Access your server:**
   - Health: `https://your-app.railway.app/health`
   - MCP: `https://your-app.railway.app/mcp`
   - Files: `https://your-app.railway.app/files/filename.mp3`

### Local Development

```bash
# Install dependencies
pip install -e .

# Start with HTTP transport
python -m elevenlabs_mcp --transport http --host 0.0.0.0 --port 3000

# Server available at http://localhost:3000/mcp/
```

## 🔧 Configuration Options

### Command Line

```bash
# Stdio mode (default - for Claude Desktop)
python -m elevenlabs_mcp

# HTTP mode with file serving (for CrewAI and web clients)
python -m elevenlabs_mcp --server --host 0.0.0.0 --port 3000

# Custom host/port
python -m elevenlabs_mcp --server --host 127.0.0.1 --port 8080
```

### Environment Variables

- `ELEVENLABS_API_KEY`: Required ElevenLabs API key
- `HOST`: Override default host (0.0.0.0)
- `PORT`: Override default port (3000)
- `ELEVENLABS_MCP_BASE_PATH`: Override output directory for generated files (defaults to /app/shared in production)
- `SHARED_AUDIO_PATH`: Alternative name for shared volume path (Railway compatible)

## 🎯 Available Tools

Your CrewAI agents will have access to **22 powerful ElevenLabs tools**:

### Text-to-Speech
- `text_to_speech`: Convert text to natural speech (returns HTTP URL for direct playback)
- `text_to_sound_effects`: Generate AI sound effects (returns HTTP URL for direct playback)

### Speech Processing
- `speech_to_text`: Transcribe audio to text
- `speech_to_speech`: Transform voice while preserving emotion (returns HTTP URL for direct playback)

### Voice Management
- `search_voices`: Find voices in the ElevenLabs library
- `get_voice`: Get detailed voice information
- `voice_clone`: Clone voices from audio samples

### Conversational AI
- `create_agent`: Create conversational AI agents
- `list_agents`: Manage your AI agents
- `make_outbound_call`: Automated phone calls

### Audio Tools
- `isolate_audio`: Remove background noise
- `play_audio`: Play audio files

And 10 more advanced tools for professional audio workflows!

## 📡 Protocol Details

### MCP Streamable HTTP Endpoints

The server exposes multiple endpoints:
- **MCP Protocol**: `/mcp` - Standard MCP JSON-RPC 2.0 over HTTP
- **File Serving**: `/files/{filename}` - Direct audio file access for frontend playback
- **Health Check**: `/health` - Service health monitoring
- **Transport**: Streamable HTTP (bidirectional)
- **CORS**: Enabled for frontend access
- **Auto-cleanup**: Files older than 24 hours are automatically removed

### Example MCP Client Usage

```python
import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client

# For direct MCP client access
async def test_mcp_client():
    # Connect to HTTP MCP server
    transport = HttpTransport("http://localhost:3000/mcp")
    
    async with ClientSession(transport) as session:
        await session.initialize()
        
        # List available tools
        tools = await session.list_tools()
        print(f"Available tools: {len(tools)}")
        
        # Call text-to-speech - returns HTTP URL for direct access
        result = await session.call_tool("text_to_speech", {
            "text": "Hello from MCP client!",
            "voice_name": "Adam"
        })
        print(result)  # Contains HTTP URL like: http://host:port/files/tts_Hello_20231201_120000.mp3

asyncio.run(test_mcp_client())
```

### Direct File Serving Flow

```python
# 🎯 New Direct Serving Architecture
# 1. CrewAI calls ElevenLabs MCP tool
crew_result = agent.use_tool("text_to_speech", {"text": "Hello world!"})

# 2. ElevenLabs MCP generates audio and returns URL (not file path)
# Result: "Success. Audio file available at: http://railway-app.railway.app/files/tts_Hello_20231201_120000.mp3"

# 3. CrewAI backend extracts URL and returns to frontend
audio_url = extract_url_from_result(crew_result)

# 4. Frontend plays audio directly from ElevenLabs service
# <audio src="http://railway-app.railway.app/files/tts_Hello_20231201_120000.mp3" controls></audio>
```

## 🔒 Security Notes

- The server runs with CORS enabled for web client access
- Always secure your ElevenLabs API key
- For production deployment, consider adding authentication middleware
- Railway deployment includes built-in HTTPS

## 🚀 Advanced Usage

### Multi-Agent CrewAI Setup

```python
from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter

# Multiple specialized agents with ElevenLabs tools
elevenlabs_params = {
    "url": "https://your-railway-app.railway.app/mcp",
    "transport": "streamable-http"
}

with MCPServerAdapter(elevenlabs_params) as elevenlabs_tools:
    
    # Voice synthesis specialist
    voice_creator = Agent(
        role="Voice Synthesis Specialist",
        goal="Create high-quality voice content",
        backstory="Expert in voice synthesis and audio production",
        tools=[t for t in elevenlabs_tools if 'speech' in t.name],
        verbose=True
    )
    
    # Voice cloning specialist  
    voice_cloner = Agent(
        role="Voice Cloning Expert",
        goal="Clone and manage custom voices",
        backstory="Specialist in voice cloning and voice library management",
        tools=[t for t in elevenlabs_tools if 'voice' in t.name or 'clone' in t.name],
        verbose=True
    )
    
    # Conversational AI specialist
    ai_caller = Agent(
        role="Conversational AI Manager",
        goal="Create and deploy conversational AI agents",
        backstory="Expert in conversational AI and automated calling systems",
        tools=[t for t in elevenlabs_tools if 'agent' in t.name or 'call' in t.name],
        verbose=True
    )
    
    # Define collaborative tasks
    tasks = [
        Task(
            description="Create a professional voice for our AI assistant",
            expected_output="Voice created and configured",
            agent=voice_creator
        ),
        Task(
            description="Clone the CEO's voice for automated responses",
            expected_output="Voice cloned and ready for use",
            agent=voice_cloner
        ),
        Task(
            description="Deploy conversational AI agent with custom voices",
            expected_output="AI agent deployed and tested",
            agent=ai_caller
        )
    ]
    
    crew = Crew(
        agents=[voice_creator, voice_cloner, ai_caller],
        tasks=tasks,
        verbose=True
    )
    
    result = crew.kickoff()
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection refused**: Ensure server is running on correct host/port
2. **Tools not available**: Check ELEVENLABS_API_KEY is set correctly
3. **CrewAI integration fails**: Verify the MCP endpoint URL is accessible

### Debug Mode

```bash
# Enable debug logging
ELEVENLABS_API_KEY=your_key python -m elevenlabs_mcp --transport http --port 3000
```

### Health Check

```bash
# Test server health
curl http://localhost:3000/mcp/

# Should return MCP protocol information
```

## 📚 Resources

- [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- [CrewAI Documentation](https://docs.crewai.com)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/anthropics/modelcontextprotocol)

## 🤝 Contributing

This enhanced server builds on the official ElevenLabs MCP implementation with added Streamable HTTP support for modern AI agent frameworks like CrewAI.

---

**Built for the future of AI agent collaboration! 🚀**