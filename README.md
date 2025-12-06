# Code Reviewer - Professional Code Analysis Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.0](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Open Source](https://img.shields.io/badge/open-source-success.svg)](https://opensource.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful, open-source code analysis and refinement tool that combines static code analysis with open-source LLM-powered code refinement. Analyze code in 30+ programming languages, get AI suggestions, and refine your code using local, privacy-preserving models.

## ✨ Features

### 🔍 Static Code Analysis
- **30+ Programming Languages**: Python, JavaScript, TypeScript, Java, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, and more
- **50+ Analysis Rules**: Detect code smells, potential bugs, performance issues, and maintainability problems
- **Severity Levels**: Errors, Warnings, and Info categorized for easy prioritization
- **Detailed Reporting**: Line numbers, error messages, and actionable feedback

### 🤖 Open-Source LLM Integration
- **Local Model Support**: Use Ollama to run models locally (Mistral, CodeLLaMA, LLaMA 2)
- **Zero API Keys**: No subscriptions, no rate limits, no cloud dependencies
- **Privacy First**: All code processing happens on your machine
- **Cost Effective**: Free forever, unlimited usage

### ✨ Code Enhancement Suggestions
- **8 Enhancement Categories**: Performance, readability, maintainability, security, concurrency, documentation, patterns, best practices
- **Code Examples**: Before/after examples for each suggestion
- **Language-Specific Tips**: Tailored suggestions for each programming language
- **Actionable Feedback**: Clear, practical improvements

### 🎯 Code Refinement
- **Pattern-Based Demo Mode**: Works instantly without LLM (no setup required)
- **Ollama Integration**: Automatic code refinement using local open-source models
- **Intelligent Fallback**: Seamlessly falls back to demo mode if needed
- **Fast Processing**: 5-30 seconds for code refinement

### 💻 Professional Web UI
- **Modern Design**: Dark theme, intuitive layout, responsive design
- **Real-time Analysis**: See results as you work
- **Tab-based Navigation**: Organize analysis, enhancements, and refined code
- **Code Management**: Copy, download, and manage code easily

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or pip3
- (Optional) Ollama for LLM features

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/code-reviewer.git
cd code-reviewer
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Server**
```bash
python3 app.py
```

4. **Open in Browser**
```
http://127.0.0.1:5002
```

### Setup Ollama (Optional - for LLM Features)

**Install Ollama**:
- macOS: `brew install ollama`
- Linux: `curl https://ollama.ai/install.sh | sh`
- Windows: Download from https://ollama.ai/download

**Start Ollama** (in a new terminal):
```bash
ollama serve
```

**Pull a Model** (in another terminal):
```bash
ollama pull mistral  # Fast & recommended
# OR
ollama pull codellama  # Best for code
```

**Restart Code Reviewer**:
The app will auto-detect Ollama and use it automatically!

## 📁 Project Structure

```
code-reviewer/
├── src/                          # Core application code
│   ├── code_reviewer.py         # Main analysis engine
│   ├── enhancements.py          # Enhancement suggestions
│   ├── llm_handler.py           # Open-source LLM integration
│   ├── opensource_llm.py        # Ollama handler
│   ├── mcp_server.py            # Multi-agent orchestration
│   └── __init__.py
│
├── tests/                        # Test suites
│   ├── test_reviewer.py         # Core functionality tests
│   ├── test_integration.py      # Integration tests
│   ├── test_ui.py               # UI tests
│   └── verify_migration.py      # Migration verification
│
├── docs/                         # Documentation
│   ├── README.md                # User guide
│   ├── ARCHITECTURE.md          # System architecture
│   ├── OLLAMA_SETUP.md          # Ollama setup guide
│   ├── MIGRATION_TECHNICAL.md   # Technical migration details
│   └── ...
│
├── examples/                     # Example code files
│   ├── example_good.py          # Good code example
│   └── example_bad.py           # Bad code example (to review)
│
├── templates/                    # Web UI templates
│   └── index.html               # Main web interface
│
├── app.py                        # Flask application entry point
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🎯 Usage

### Via Web UI

1. **Open the Application**
   - Navigate to http://127.0.0.1:5002

2. **Enter Your Code**
   - Select programming language
   - Paste your code in the editor

3. **Review Code**
   - Click "Review Code" button
   - See analysis results with issues and severity levels

4. **View Enhancements**
   - Click "Enhancements" tab
   - See suggestions with before/after code examples

5. **Refine with LLM**
   - Click "LLM Refine" tab
   - Click "Refine with Open-Source LLM" to get AI-powered suggestions
   - (Requires Ollama to be running)

6. **Download Results**
   - Copy refined code or download as file
   - Use improved code in your project

### Via API

**Analyze Code**:
```bash
curl -X POST http://127.0.0.1:5002/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "for i in range(len(items)):\n    result = result + items[i]",
    "language": "python",
    "filename": "code.py"
  }'
```

**Get Enhancements**:
```bash
curl -X POST http://127.0.0.1:5002/api/enhancements \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your code here",
    "language": "python"
  }'
```

**Refine Code**:
```bash
curl -X POST http://127.0.0.1:5002/api/refine-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "your code here",
    "language": "python",
    "issues": []
  }'
```

**Check LLM Status**:
```bash
curl http://127.0.0.1:5002/api/llm-providers
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 tests/test_reviewer.py

# Run with verbose output
python3 -m pytest tests/ -v

# Verify migration
python3 tests/verify_migration.py
```

## 🛠️ Configuration

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Server Configuration
SERVER_PORT=5002
SERVER_HOST=127.0.0.1

# Ollama Configuration (Optional)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral
```

## 📊 Supported Languages

Python, JavaScript, TypeScript, Java, C#, Go, Rust, Ruby, PHP, C++, Swift, Kotlin, Scala, R, MATLAB, Julia, VB.NET, Objective-C, Lua, Perl, Groovy, Shell, CSS, HTML, SQL, XML, YAML, JSON, Markdown, and more.

## 🚀 Performance

| Operation | Time | Resources |
|-----------|------|-----------|
| Code Analysis | <100ms | Minimal (static) |
| Demo Refinement | ~5ms | Minimal |
| LLM Refinement (CPU) | 20-30s | Standard CPU |
| LLM Refinement (GPU) | 5-10s | GPU recommended |

## 🔐 Security & Privacy

- ✅ **No Cloud Dependencies**: Everything runs locally
- ✅ **Zero Data Collection**: No tracking or logging of code
- ✅ **No API Keys Required**: No external service calls
- ✅ **Open Source**: Code is transparent and auditable
- ✅ **Local Models Only**: All LLM processing on your machine

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

- **Documentation**: See `docs/` folder
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@example.com

## 🎓 Learn More

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Code Analysis Best Practices](https://docs.python.org/3/library/ast.html)

## 🌟 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [Ollama](https://ollama.ai/)
- Open-source LLM models: [Mistral](https://mistral.ai/), [Meta LLaMA](https://www.llama.com/)

---

**Status**: ✅ Production Ready

Made with ❤️ for the developer community
