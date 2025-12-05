# Code Reviewer - User Guide

## Quick Start

### Installation

```bash
cd /Users/mohamedhijazyshazinhassan/code-reviewer
pip install -r requirements.txt
```

### Basic Usage

```bash
# Review a single file
python cli.py mycode.py

# Review entire directory
python cli.py .

# JSON output
python cli.py mycode.py --format json
```

## Complete Rule Reference

### 🔴 CRITICAL Issues

| Rule | Code | Message | Suggestion |
|------|------|---------|-----------|
| Dangerous Functions | DANGEROUS_FUNCTION | eval() or exec() usage | Use safer alternatives |
| Hardcoded Secrets | HARDCODED_SECRET | Credentials in code | Use environment variables |
| Syntax Errors | SYNTAX_ERROR | Invalid Python syntax | Fix syntax errors |

### 🟠 HIGH Issues

| Rule | Code | Message | Suggestion |
|------|------|---------|-----------|
| Bare Except | BARE_EXCEPT | Catches all exceptions | Specify exception type |

### 🟡 MEDIUM Issues

| Rule | Code | Message | Suggestion |
|------|------|---------|-----------|
| High Complexity | HIGH_COMPLEXITY | Cyclomatic complexity > 10 | Break into smaller functions |
| Long Function | LONG_FUNCTION | Function > 50 lines | Split into smaller functions |
| Too Many Parameters | TOO_MANY_PARAMS | Function has > 5 params | Use dataclass/dict |
| Global Variables | GLOBAL_VARIABLE | Module-level mutable state | Use constants/classes |
| Print Statements | PRINT_STATEMENT | Using print() | Use logging module |

### 🔵 LOW Issues

| Rule | Code | Message | Suggestion |
|------|------|---------|-----------|
| Bad Variable Name | BAD_VARIABLE_NAME | Single-letter names | Use descriptive names |
| Invalid Function Name | INVALID_FUNCTION_NAME | Not snake_case | Use snake_case |
| Line Too Long | LINE_TOO_LONG | > 100 characters | Break into multiple lines |
| Multiple Statements | MULTIPLE_STATEMENTS | Multiple ; on one line | One statement per line |
| Missing Docstring | MISSING_DOCSTRING | No documentation | Add docstring |

## Usage Examples

### Example 1: Single File Review

```bash
python cli.py example_bad.py
```

Output shows all issues organized by category with:
- Line number
- Severity level
- Issue code
- Description
- Suggestion for fixing

### Example 2: Batch Directory Review

```bash
python cli.py ~/my_project --extension .py
```

Scans all Python files and shows summary:
- Files with issues
- Total issues count
- Issues by severity

### Example 3: JSON Export

```bash
python cli.py mycode.py --format json > report.json
```

Generate structured report for CI/CD integration:

```json
{
  "filename": "mycode.py",
  "status": "issues_found",
  "total_issues": 5,
  "by_severity": {
    "critical": 1,
    "high": 1,
    "medium": 2,
    "low": 1
  },
  "issues": [...]
}
```

### Example 4: Programmatic Usage

```python
from code_reviewer import CodeReviewer

code = """
def my_function():
    print("hello")
"""

reviewer = CodeReviewer(code, "test.py")
issues = reviewer.review()

for issue in issues:
    print(f"Line {issue.line}: {issue.message}")
    print(f"Fix: {issue.suggestion}")
```

### Example 5: Filter and Process Results

```python
from code_reviewer import CodeReviewer, Severity

reviewer = CodeReviewer(code, "test.py")
issues = reviewer.review()

# Get only critical issues
critical = [i for i in issues if i.severity == Severity.CRITICAL]

# Group by category
by_category = {}
for issue in issues:
    by_category.setdefault(issue.category, []).append(issue)

# Export to JSON
import json
report = reviewer.get_report()
with open('report.json', 'w') as f:
    json.dump(report, f)
```

## Advanced Features

### Configuration

Create a `reviewer_config.json`:

```json
{
  "max_line_length": 120,
  "max_complexity": 15,
  "max_function_length": 100,
  "enabled_rules": {
    "security": true,
    "complexity": true,
    "documentation": false,
    "naming": true
  }
}
```

### Custom Rules

Extend the reviewer with custom rules:

```python
from code_reviewer import CodeAnalyzer, PatternAnalyzer, CodeIssue, Severity

class CustomAnalyzer(PatternAnalyzer):
    def _check_custom_rules(self):
        for i, line in enumerate(self.lines, 1):
            if 'FIXME' in line:
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.MEDIUM,
                    code='FIXME_FOUND',
                    message='FIXME comment found',
                    suggestion='Resolve and remove FIXME',
                    category='TODO'
                ))
```

## Integration Guides

### GitHub Actions

```yaml
- name: Code Review
  run: python cli.py . --format json > review.json
  
- name: Comment PR
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const review = JSON.parse(fs.readFileSync('review.json'));
      // Post comment with issues
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

python cli.py . --format json > /tmp/review.json
if grep -q '"critical"' /tmp/review.json; then
  echo "❌ Critical issues found. Commit rejected."
  exit 1
fi
```

### GitLab CI

```yaml
code_review:
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - python cli.py . --format json > report.json
  artifacts:
    reports:
      sast: report.json
```

## Best Practices

### 1. Security First
- Always fix CRITICAL security issues immediately
- Review all eval() and exec() usage
- Never commit hardcoded credentials

### 2. Code Organization
- Keep functions under 50 lines
- Limit parameters to 5 or fewer
- Use meaningful variable names

### 3. Documentation
- Always include docstrings for public functions/classes
- Add type hints for clarity
- Use descriptive comments for complex logic

### 4. Code Style
- Follow PEP 8 conventions
- Keep lines under 100 characters
- One statement per line

### 5. Testing Integration
- Run reviewer before tests
- Fix issues before committing
- Use in CI/CD pipeline

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'code_reviewer'"

**Solution:** Make sure you're in the correct directory:
```bash
cd /Users/mohamedhijazyshazinhassan/code-reviewer
python cli.py ...
```

### Issue: No issues found but code looks bad

**Solution:** The reviewer looks for specific patterns. Some issues may require:
- Manual code review
- Additional linters (pylint, flake8)
- Custom rules

### Issue: Too many false positives

**Solution:** Configure the reviewer:
- Adjust severity thresholds
- Disable specific rule categories
- Create custom configuration

## Comparison with LLM-Based Reviewers

| Feature | Code Reviewer | LLM APIs |
|---------|---------------|----------|
| Cost | FREE | $$$ |
| Speed | Instant | Slow (network) |
| Privacy | 100% Local | Sends to server |
| Deterministic | Yes | No |
| Rate Limit | None | Yes |
| Context Awareness | Limited | Better |
| Runtime | Fast (seconds) | Variable (minutes) |
| Offline | Yes | No |
| Complex Logic | Limited | Better |

## When to Use This Reviewer

✅ **Good For:**
- Automated security checks
- Code style enforcement
- Quick issue identification
- CI/CD integration
- Local development
- Privacy-sensitive code

❌ **Not Ideal For:**
- Complex architectural reviews
- Business logic analysis
- Design pattern suggestions
- Algorithm optimization

## Performance Metrics

| Metric | Value |
|--------|-------|
| Analysis Speed | ~1000 lines/sec |
| Memory Usage | < 50MB |
| Setup Time | < 1 second |
| Startup Time | < 100ms |

## Getting Help

1. Check the README.md
2. Review examples.py
3. Run test_reviewer.py
4. Check issue suggestions

## Contributing

To extend the reviewer:

1. Add rules to `PatternAnalyzer` or `CodeAnalyzer`
2. Add tests to `test_reviewer.py`
3. Update documentation
4. Submit improvements

---

**Happy Coding! 🚀**
