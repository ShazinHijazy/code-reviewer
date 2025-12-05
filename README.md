# Code Reviewer - Static Analysis Based Code Review

A Python code reviewer that performs comprehensive code analysis **without using LLM APIs**. It uses AST parsing, pattern matching, and built-in rules to identify issues, suggest improvements, and enforce best practices.

## Features

✅ **No LLM Dependencies** - Pure Python static analysis
✅ **AST-Based Analysis** - Deep code structure analysis
✅ **Pattern Matching** - Regex-based code smell detection
✅ **Security Checks** - Identifies common security issues
✅ **Multiple Output Formats** - Text and JSON reports
✅ **Batch Processing** - Review entire directories
✅ **Categorized Issues** - Organized by type (Security, Performance, Style, etc.)

## What It Checks

### Code Quality
- Function complexity (cyclomatic complexity)
- Function length and parameter count
- Class and function documentation
- Variable naming conventions
- Code organization

### Security Issues
- `eval()` and `exec()` usage
- Hardcoded secrets and credentials
- Dangerous imports

### Best Practices
- Bare except clauses
- Print statements (should use logging)
- Global variables
- Line length
- Multiple statements per line

### Style & Naming
- Snake_case conventions
- Single-letter variable names
- Long lines (>100 chars)
- Missing docstrings

## Installation

```bash
cd /Users/mohamedhijazyshazinhassan/code-reviewer
pip install -r requirements.txt
```

## Usage

### Review a Single File

```bash
python cli.py example_bad.py
```

### Review a Directory

```bash
python cli.py .
```

### JSON Output

```bash
python cli.py example_bad.py --format json
```

### Specific File Extension

```bash
python cli.py . --extension .py
```

## Example Output

```
======================================================================
CODE REVIEW REPORT - example_bad.py
======================================================================

📊 Total Issues: 12
Severity Breakdown: {'high': 3, 'medium': 4, 'low': 5}

📋 Security:
----------------------------------------------------------------------

🔴 Line 17 | CRITICAL
   Code: DANGEROUS_FUNCTION
   Message: Use of eval() is dangerous
   Suggestion: Use safer alternatives or validate input thoroughly

🔴 Line 25 | CRITICAL
   Code: HARDCODED_SECRET
   Message: Hardcoded secret/credential detected
   Suggestion: Use environment variables or secure config management

📋 Error Handling:
----------------------------------------------------------------------

🟠 Line 16 | HIGH
   Code: BARE_EXCEPT
   Message: Bare 'except:' clause catches all exceptions
   Suggestion: Specify the exception type

... more issues ...

======================================================================
```

## API Usage

```python
from code_reviewer import CodeReviewer

# Review code
code = """
def my_function(x, y, z):
    print("Hello")
    try:
        return eval(x + y)
    except:
        pass
"""

reviewer = CodeReviewer(code, "example.py")
issues = reviewer.review()

# Print report
reviewer.print_report()

# Get structured report
report = reviewer.get_report()
print(report)
```

## Severity Levels

- 🔴 **CRITICAL** - Major issues that must be fixed (security, syntax)
- 🟠 **HIGH** - Important issues that should be fixed soon
- 🟡 **MEDIUM** - Moderate issues affecting code quality
- 🔵 **LOW** - Minor issues for code improvement
- ⚪ **INFO** - Informational suggestions

## Rules Categories

| Category | Examples |
|----------|----------|
| **Syntax** | Syntax errors |
| **Security** | eval(), hardcoded secrets |
| **Performance** | High complexity, inefficient patterns |
| **Design** | Too many parameters, global variables |
| **Error Handling** | Bare except, missing error handling |
| **Documentation** | Missing docstrings |
| **Style** | Line length, naming conventions |
| **Best Practice** | Print statements, code organization |

## Extensibility

You can extend the reviewer by:

1. **Adding custom rules** in `PatternAnalyzer._check_*` methods
2. **Adding AST visitors** in `CodeAnalyzer.visit_*` methods
3. **Creating custom analyzers** inheriting from the base classes

## Example Customization

```python
# Create custom analyzer
class CustomAnalyzer(PatternAnalyzer):
    def _check_custom_rules(self):
        for i, line in enumerate(self.lines, 1):
            if 'TODO' in line:
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.INFO,
                    code="TODO_FOUND",
                    message="TODO comment found",
                    suggestion="Resolve or remove TODO",
                    category="TODO"
                ))
```

## Limitations

- Only analyzes Python 3 code
- Pattern-based checks may have false positives/negatives
- Cannot detect runtime errors
- Does not execute code
- Limited context awareness compared to LLMs

## Advantages Over LLM-Based Reviewers

- ✅ No API costs
- ✅ Instant results (no network latency)
- ✅ Privacy (code stays local)
- ✅ Deterministic and reproducible
- ✅ No rate limiting
- ✅ Transparent rules and logic
- ✅ Offline functionality

## Future Enhancements

- [ ] Multi-language support (JavaScript, Go, Rust)
- [ ] Custom rule configuration
- [ ] GitHub integration
- [ ] Pre-commit hooks
- [ ] IDE plugins
- [ ] Performance profiling
- [ ] Duplicate code detection
- [ ] Dependencies analysis

## License

MIT

## Contributing

Feel free to add more rules and improvements!
