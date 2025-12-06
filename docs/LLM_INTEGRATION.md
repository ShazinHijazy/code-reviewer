# Code Reviewer - LLM Integration Guide

## 🚀 Features

### Multi-LLM Support
- **Claude 3.5 Sonnet** (Anthropic) - Recommended
- **GPT-4 Turbo** (OpenAI)
- **Gemini 2.0 Flash** (Google)

### LLM Capabilities
1. **Code Refinement** - Fix issues and improve code quality
2. **Code Optimization** - Enhance performance
3. **Multi-Agent Orchestration** - MCP-based agent coordination
4. **Automatic Fallback** - Seamless provider switching on failure

### Integration Points
- REST API endpoints for all LLM operations
- MCP (Model Context Protocol) server for agent management
- Web UI with LLM refinement tab
- Automatic provider detection and fallback logic

## 🔑 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This includes:
- Flask 3.0.0
- anthropic (Claude SDK)
- openai (GPT-4 SDK)
- google-generativeai (Gemini SDK)

### 2. Configure LLM Providers

Set environment variables (choose at least one):

**Claude (Recommended)**
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

**OpenAI**
```bash
export OPENAI_API_KEY='sk-...'
```

**Google Gemini**
```bash
export GOOGLE_API_KEY='AIza...'
```

### 3. Run the Application
```bash
python3 app.py
```

The server will start on `http://localhost:5000`

## 🎯 Usage

### Via Web UI

1. **Input Code**
   - Paste your code in the editor
   - Select language (auto-detected)

2. **Review**
   - Click "Review Code" to find issues

3. **LLM Refine Tab**
   - Select LLM provider (or use Auto)
   - Click "✨ Refine Code with LLM"
   - View original vs. refined code
   - Apply changes or copy to clipboard

### Via API Endpoints

#### 1. Refine Code
```bash
curl -X POST http://localhost:5000/api/refine-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "for i in range(len(items)):\n    result = result + items[i]",
    "language": "python",
    "issues": [...],
    "provider": "claude"
  }'
```

**Response:**
```json
{
  "status": "success",
  "original_code": "...",
  "refined_code": "...",
  "provider": "claude",
  "language": "python",
  "timestamp": "2025-12-06T..."
}
```

#### 2. Get LLM Providers Status
```bash
curl http://localhost:5000/api/llm-providers
```

#### 3. Generate Code Suggestions
```bash
curl -X POST http://localhost:5000/api/code-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "code": "...",
    "language": "python",
    "issue_types": ["performance", "readability"]
  }'
```

#### 4. Get MCP Agents
```bash
curl http://localhost:5000/api/mcp/agents
```

#### 5. Orchestrate Multi-Agent Review
```bash
curl -X POST http://localhost:5000/api/mcp/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "...",
    "language": "python",
    "issues": [...]
  }'
```

## 🏗️ Architecture

### MultiLLMHandler (`llm_handler.py`)
Manages communication with multiple LLM providers:
- Automatic provider detection
- Intelligent fallback system
- Unified interface for all providers
- Code refinement and suggestion generation

### MCPServer (`mcp_server.py`)
Model Context Protocol implementation:
- Agent management and orchestration
- Multi-step workflow execution
- Tool registration and routing
- Request/response handling

### Flask App (`app.py`)
Web server and API:
- 6 new LLM endpoints
- MCP orchestration endpoints
- Automatic initialization on startup
- Error handling and logging

### Web UI (`templates/index.html`)
User interface:
- LLM Refine tab with provider selector
- Side-by-side code comparison
- Real-time refinement
- Copy and apply buttons

## 📊 Supported Languages

- Python, JavaScript, TypeScript, Java, C#
- Go, Rust, Ruby, PHP, Swift
- Kotlin, Groovy, Scala, Objective-C
- Shell (bash, zsh, fish), SQL
- HTML, XML, JSON, YAML, and 20+ more

## 🔄 Fallback Logic

The system implements intelligent fallback:

```
Request for code refinement
    ↓
Try preferred provider (or auto-select best)
    ↓ (if fails)
Try Claude
    ↓ (if fails)
Try OpenAI
    ↓ (if fails)
Try Google
    ↓ (if all fail)
Return original code
```

## 📝 Example Workflow

### Input Code (with issues):
```python
result = ""
for i in range(len(items)):
    result = result + items[i]
```

### Claude Refinement Output:
```python
# More Pythonic approach using join
result = "".join(items)
```

Or with list comprehension:
```python
results = [process(item) for item in items]
```

## 🛠️ Advanced Features

### MCP Workflows
Register custom workflows:
```python
mcp.register_workflow('full_review', [
    {'tool': 'code_refinement', 'agent': 'claude_0', 'priority': 1},
    {'tool': 'security_audit', 'agent': 'claude_0', 'priority': 2},
    {'tool': 'code_optimization', 'agent': 'openai_0', 'priority': 3},
])
```

### Custom Agents
Create agents for specific providers:
```python
agent_id = mcp.create_agent('claude', 'claude-3-5-sonnet-20241022')
```

## 🐛 Troubleshooting

### No LLM Provider Available
- Check API keys are set correctly
- Verify `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY`
- Test with: `python3 -c "import anthropic; print('OK')"`

### API Rate Limits
- The system respects rate limits
- Wait before retrying large batches
- Use fallback providers for load distribution

### Connection Errors
- Verify internet connectivity
- Check firewall/proxy settings
- Review API endpoint status pages

## 📈 Performance

Typical response times:
- Code refinement: 5-15 seconds (depends on code length)
- Suggestions generation: 3-10 seconds
- Multi-agent orchestration: 10-30 seconds

## 🔐 Security

- API keys stored securely (environment variables or ~/.code-reviewer/)
- No code sent to untrusted sources
- Uses official SDKs for all providers
- Automatic HTTPS support via proxy

## 📚 Additional Resources

- Claude API: https://docs.anthropic.com/
- OpenAI API: https://platform.openai.com/docs/
- Google Gemini: https://ai.google.dev/docs
- MCP Spec: https://modelcontextprotocol.io/

## 🤝 Contributing

To add a new LLM provider:

1. Update `MultiLLMHandler` class
2. Add provider check method
3. Implement refinement method
4. Test with sample code
5. Update documentation

---

**Made with ❤️ for better code quality**
