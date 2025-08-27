# ElevenLabs MCP Configuration Guide

This document describes all configurable options for the ElevenLabs MCP server.

## 🔧 Environment Variables

### **Required Configuration**

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ELEVENLABS_API_KEY` | **Required** ElevenLabs API key | None | `sk_abc123...` |

### **File Path Configuration**

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ELEVENLABS_MCP_BASE_PATH` | Primary output directory for generated audio files | `/app/shared` | `/app/output` |
| `SHARED_AUDIO_PATH` | Alternative name for base path (Railway-friendly) | None | `/app/shared` |
| `ELEVENLABS_FALLBACK_DIR` | Fallback directory when no base path set | `~/Desktop` | `/tmp/audio` |

**Path Priority Order:**
1. `ELEVENLABS_MCP_BASE_PATH` (highest priority)
2. `SHARED_AUDIO_PATH` 
3. `/app/shared` (container default)
4. `ELEVENLABS_FALLBACK_DIR` (local fallback)

### **Network Configuration**

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `HOST` | Server bind address | `localhost` | `0.0.0.0` |
| `PORT` | Server port | `3000` | `8080` |
| `RAILWAY_PUBLIC_DOMAIN` | Override Railway domain for URLs | Auto-detected | `myapp.railway.app` |

### **File Management**

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ELEVENLABS_CLEANUP_AGE_HOURS` | Hours before files are auto-deleted | `24` | `48` |
| `ELEVENLABS_CLEANUP_INTERVAL_SECONDS` | Cleanup task run interval | `3600` (1 hour) | `7200` (2 hours) |

### **Voice Configuration**

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ELEVENLABS_DEFAULT_VOICE_ID` | Default voice when none specified | `cgSgspJ2msm6clMCkdW9` | `voice_abc123` |

## 📁 File Path Examples

### **Development (.env)**
```bash
ELEVENLABS_API_KEY=sk_your_api_key_here
ELEVENLABS_MCP_BASE_PATH=/Users/yourname/projects/audio-output
HOST=127.0.0.1
PORT=3002
ELEVENLABS_CLEANUP_AGE_HOURS=12
```

### **Production (Railway)**
```bash
ELEVENLABS_API_KEY=sk_your_api_key_here
# Railway automatically provides:
# PORT=<dynamic>
# HOST=0.0.0.0
# RAILWAY_PUBLIC_DOMAIN=<app-name>.railway.app

# Optional overrides:
ELEVENLABS_CLEANUP_AGE_HOURS=48
ELEVENLABS_CLEANUP_INTERVAL_SECONDS=7200
```

### **Docker Compose**
```yaml
environment:
  - ELEVENLABS_API_KEY=sk_your_api_key_here
  - ELEVENLABS_MCP_BASE_PATH=/app/shared
  - ELEVENLABS_CLEANUP_AGE_HOURS=24
  - HOST=0.0.0.0
  - PORT=3000
volumes:
  - ./audio-files:/app/shared
```

## 🎯 Use Cases

### **High Volume Production**
```bash
# Longer retention, frequent cleanup
ELEVENLABS_CLEANUP_AGE_HOURS=72
ELEVENLABS_CLEANUP_INTERVAL_SECONDS=1800  # 30 minutes
ELEVENLABS_MCP_BASE_PATH=/var/lib/audio-storage
```

### **Development/Testing**
```bash
# Quick cleanup, local paths
ELEVENLABS_CLEANUP_AGE_HOURS=1
ELEVENLABS_CLEANUP_INTERVAL_SECONDS=300   # 5 minutes
ELEVENLABS_MCP_BASE_PATH=./temp-audio
ELEVENLABS_FALLBACK_DIR=./audio-fallback
```

### **Shared Team Environment**
```bash
# Moderate retention, shared storage
ELEVENLABS_CLEANUP_AGE_HOURS=48
ELEVENLABS_MCP_BASE_PATH=/shared/team-audio
ELEVENLABS_DEFAULT_VOICE_ID=team_voice_id
```

## 🔄 Configuration Precedence

1. **Environment Variables** (highest priority)
2. **Command Line Arguments** (for host/port only)
3. **Default Values** (lowest priority)

## 🚀 Dynamic Configuration

Most configuration changes require a server restart. The exception is:
- File cleanup settings are read each time the cleanup task runs
- Voice settings can be overridden per API call

## 🔐 Security Notes

- **Never commit API keys** to version control
- Use Railway/platform environment variables for production
- Restrict file paths to safe directories
- Consider setting conservative cleanup intervals for sensitive data

## 📦 Dependencies

### **Core Dependencies**
- `mcp[cli]>=1.12.0` - Model Context Protocol framework
- `fastmcp>=0.4.1` - FastMCP tools and HTTP server (required for production)
- `elevenlabs>=2.7.1` - ElevenLabs API client
- `fastapi==0.109.2` - Web framework (includes compatible Starlette)
- `uvicorn==0.27.1` - ASGI server

### **Development Dependencies**
Development tools are separate and won't conflict with other projects:
- `pytest` - Testing framework
- `ruff` - Linting and formatting
- `pre-commit` - Git hooks

## 🛠️ Troubleshooting

### **FastMCP Import Errors**
If you get `ModuleNotFoundError: No module named 'fastmcp'`:
1. FastMCP is now a main dependency (not dev-only)
2. Reinstall: `pip install -e .` or `pip install elevenlabs-mcp`
3. For other projects: FastMCP conflicts are resolved

### **Files Not Saving to Expected Directory**
1. Check `ELEVENLABS_MCP_BASE_PATH` is set correctly
2. Verify directory permissions are writable
3. Restart server after environment changes

### **URLs Pointing to Wrong Host/Port**
1. Set `HOST` and `PORT` environment variables
2. For Railway, ensure `RAILWAY_PUBLIC_DOMAIN` is correct
3. Restart server to pick up changes

### **Files Not Being Cleaned Up**
1. Check `ELEVENLABS_CLEANUP_AGE_HOURS` setting
2. Verify cleanup interval with `ELEVENLABS_CLEANUP_INTERVAL_SECONDS`
3. Check server logs for cleanup task errors