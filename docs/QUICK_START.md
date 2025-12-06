# 🚀 Quick Reference - Multi-LLM & MCP Integration

## Installation & Setup (2 minutes)

```bash
# 1. Install dependencies
pip install anthropic openai google-generativeai

# 2. Set API key (choose at least one):
export ANTHROPIC_API_KEY='your-key'           # Claude (recommended)
export OPENAI_API_KEY='your-key'              # GPT-4
export GOOGLE_API_KEY='your-key'              # Gemini

# 3. Run
cd ~/code-reviewer && python3 app.py
```

## Web UI Usage

### Tabs
| Tab | Purpose |
|-----|---------|
| **Issues** | Shows code quality problems |
| **Enhancements** | Improvement suggestions |
| **LLM Refine** | 🆕 AI-powered code refinement |
| **Rules** | Detection rules reference |
| **Info** | Analysis metadata |

### LLM Refine Tab Flow
1. Paste code → Review Code (Issues tab)
2. Go to "LLM Refine" tab
3. Select provider (Auto/Claude/OpenAI/Gemini)
4. Click "✨ Refine Code with LLM"
5. Compare original vs refined
6. Apply changes or copy code

## API Endpoints

### Code Refinement
```bash
curl -X POST http://localhost:5000/api/refine-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your code here",
    "language": "python",
    "issues": [],
    "provider": "claude"
  }'
```

### Check LLM Status
```bash
curl http://localhost:5000/api/llm-providers
```

### Generate Suggestions
```bash
curl -X POST http://localhost:5000/api/code-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your code",
    "language": "python",
    "issue_types": ["performance", "readability"]
  }'
```

### Get MCP Agents
```bash
curl http://localhost:5000/api/mcp/agents
```

### Multi-Agent Code Review
```bash
curl -X POST http://localhost:5000/api/mcp/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your code",
    "language": "python",
    "issues": []
  }'
```

## File Structure

```
code-reviewer/
├── llm_handler.py           # Multi-LLM provider management
├── mcp_server.py            # MCP agent orchestration
├── llm_config.py            # Configuration helper
├── app.py                   # Flask app (6 new endpoints)
├── templates/index.html     # Web UI (LLM Refine tab)
├── LLM_INTEGRATION.md       # Full guide
├── INTEGRATION_SUMMARY.md   # Implementation details
└── requirements.txt         # Dependencies
```

## Supported Providers

| Provider | Model | Status |
|----------|-------|--------|
| Claude | claude-3-5-sonnet-20241022 | ✅ Recommended |
| OpenAI | gpt-4-turbo | ✅ Available |
| Google | gemini-2.0-flash | ✅ Available |

## Fallback Logic

```
User requests refinement
    ↓
Try preferred provider (or auto-select best)
    ↓ (fails)
Try Claude
    ↓ (fails)
Try OpenAI
    ↓ (fails)
Try Google
    ↓ (all fail)
Return original code
```

## Environment Variables

```bash
# Required: At least one API key
ANTHROPIC_API_KEY      # Claude
OPENAI_API_KEY         # OpenAI
GOOGLE_API_KEY         # Google

# Optional
FLASK_DEBUG=1          # Enable debug mode (default: on)
FLASK_PORT=5000        # Server port (default: 5000)
```

## Key Features

✅ **Code Analysis**
- 50+ detection rules
- Multi-language support (30+)
- Static analysis (no LLM needed)

✅ **Code Enhancement**
- 8 improvement categories
- Performance, readability, maintainability, security
- Pattern-based suggestions

✅ **AI Code Refinement** 🆕
- Multi-LLM support
- Automatic fallback
- Side-by-side comparison
- Apply/Copy options

✅ **MCP Orchestration** 🆕
- Multi-agent workflows
- Automatic provider detection
- Extensible tool system
- Request prioritization

## Troubleshooting

**No LLM provider active?**
```bash
# Set an API key
export ANTHROPIC_API_KEY='your-key'
# Restart server
python3 app.py
```

**API key not working?**
```bash
# Verify key format
echo $ANTHROPIC_API_KEY

# Test with Python
python3 -c "import anthropic; print('OK')"
```

**Server won't start?**
```bash
# Kill any existing process
pkill -f "python3 app.py"

# Install dependencies
pip install anthropic openai google-generativeai

# Restart
python3 app.py
```

## Performance Tips

1. **Use Claude** for best quality (but slower)
2. **Use GPT-4** for balanced speed/quality
3. **Use Gemini** for fastest refinement
4. **Auto mode** picks best available provider
5. Check `/api/mcp/agents` to see agent capabilities

## Advanced Usage

### Register Custom Workflow
```python
from mcp_server import MCPAgentOrchestrator

mcp = MCPAgentOrchestrator()
mcp.register_workflow('my_review', [
    {'tool': 'code_refinement', 'agent': 'claude_0', 'priority': 1},
    {'tool': 'security_audit', 'agent': 'claude_0', 'priority': 2},
])
```

### Create Specific Agent
```python
agent_id = mcp.create_agent('claude', 'claude-3-5-sonnet-20241022')
```

### Execute Workflow
```python
result = mcp.execute_workflow('code_review', {
    'code': 'your code',
    'language': 'python'
})
```

## API Response Examples

### Refine Code - Success
```json
{
  "status": "success",
  "original_code": "for i in range(len(items)): result += items[i]",
  "refined_code": "result = ''.join(items)",
  "provider": "claude",
  "language": "python",
  "timestamp": "2025-12-06T10:30:00"
}
```

### LLM Providers
```json
{
  "providers": {
    "claude": true,
    "openai": false,
    "google": false
  },
  "active": "claude",
  "status": "ready"
}
```

### MCP Agents
```json
{
  "agents": [
    {
      "agent_id": "claude_0",
      "provider": "claude",
      "model": "claude-3-5-sonnet-20241022",
      "status": "idle",
      "capabilities": ["code_refinement", "code_optimization", "security_audit"],
      "request_count": 0
    }
  ],
  "total": 1,
  "status": "ready"
}
```

## Supported Languages

Python, JavaScript, TypeScript, Java, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Groovy, Scala, Objective-C, Shell (bash/zsh/fish), SQL, HTML, XML, JSON, YAML, TOML, Dart, R, Lua, Perl, VB.NET, Fortran, Pascal, and more.

---

**For full documentation, see:**
- `LLM_INTEGRATION.md` - Complete guide
- `INTEGRATION_SUMMARY.md` - Architecture details
- Inline code comments

**Status:** ✅ Production Ready

All components tested and integrated. Automatic provider detection and fallback system active.
