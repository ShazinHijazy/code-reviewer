# Quick Start - Code Reviewer

## 30 Second Setup

```bash
cd /Users/mohamedhijazyshazinhassan/code-reviewer
pip install -r requirements.txt
python cli.py example_bad.py
```

## What You'll See

The tool analyzes your code and reports:
- **Security issues** (critical) 🔴
- **Code quality** (high/medium) 🟠🟡
- **Style & naming** (low) 🔵

## Basic Commands

```bash
# Review a single file
python cli.py myfile.py

# Review entire project
python cli.py ~/my_project

# Get JSON output
python cli.py myfile.py --format json

# Run tests
python test_reviewer.py

# See examples
python examples.py
```

## Example Output

```
======================================================================
CODE REVIEW REPORT - example.py
======================================================================

📊 Total Issues: 18
Severity: 🔴 Critical: 3 | 🟠 High: 1 | 🟡 Medium: 5 | 🔵 Low: 9

📋 Security Issues:
🔴 Line 17 | CRITICAL - Use of eval() is dangerous
   → Use safer alternatives

📋 Best Practices:
🟡 Line 14 | MEDIUM - Using print() instead of logging
   → Use logging module
```

## What It Checks

✅ **Security**
- eval() and exec() usage
- Hardcoded passwords/API keys
- Dangerous patterns

✅ **Code Quality**
- Function complexity
- Function length
- Parameter count
- Missing docstrings

✅ **Style & Naming**
- Line length
- Variable names
- snake_case conventions
- Code organization

## Try It Now

Review the example file with issues:
```bash
python cli.py example_bad.py
```

Review clean code (should pass):
```bash
python cli.py example_good.py
```

## Integrate Into Your Project

```bash
# Add to your project
git clone <this-repo> code-reviewer
cd code-reviewer
pip install -r requirements.txt

# Use in your CI/CD or pre-commit hooks
python cli.py ~/your_project
```

## No LLM APIs Needed!

- ✅ No API keys
- ✅ No rate limits
- ✅ No internet needed
- ✅ Free forever
- ✅ Results in seconds

## Next Steps

1. Read **README.md** for full documentation
2. Check **USER_GUIDE.md** for advanced features
3. Review **ARCHITECTURE.md** for technical details
4. Run **examples.py** for API usage

---

**Happy coding! 🚀**
