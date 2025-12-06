# Contributing to Code Reviewer

Thank you for your interest in contributing to Code Reviewer! We welcome contributions from the community.

## Getting Started

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/yourusername/code-reviewer.git
   cd code-reviewer
   ```

2. **Create a Development Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   python3 -m pip install pytest black flake8 mypy
   ```

## Development Workflow

### Code Style

We follow PEP 8 with some enhancements:

- **Line Length**: 100 characters max
- **Formatting**: Use `black` for automatic formatting
  ```bash
  black src/ app.py
  ```
- **Linting**: Use `flake8` to catch issues
  ```bash
  flake8 src/ app.py
  ```
- **Type Hints**: Use type hints where practical
  ```bash
  mypy src/
  ```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test
python3 tests/test_reviewer.py

# Run with coverage
python3 -m pytest tests/ --cov=src

# Verify migration
python3 tests/verify_migration.py
```

### Making Changes

1. **Modify Code**
   - Follow the existing code style
   - Add type hints to functions
   - Include docstrings for modules and classes

2. **Add Tests**
   - Create tests for new functionality
   - Ensure all tests pass
   - Aim for >80% code coverage

3. **Update Documentation**
   - Update README.md if needed
   - Update docstrings
   - Add comments for complex logic

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "type: brief description
   
   Longer description explaining the change.
   Include why this change was needed."
   ```

### Commit Message Format

Use conventional commits:

```
type(scope): subject

body

footer
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes (formatting, etc)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/changes
- `chore`: Build, CI, dependency updates

**Examples**:
```
feat(analysis): add Rust language support
fix(llm): handle Ollama timeout gracefully
docs: update installation instructions
refactor(ui): reorganize component structure
```

## Project Structure

```
src/
  ├── code_reviewer.py      # Core analysis engine
  ├── enhancements.py       # Enhancement suggestions
  ├── llm_handler.py        # Open-source LLM integration
  ├── opensource_llm.py     # Ollama handler
  ├── mcp_server.py         # Multi-agent coordination
  └── __init__.py

tests/
  ├── test_reviewer.py      # Core tests
  ├── test_integration.py   # Integration tests
  ├── test_ui.py            # UI tests
  └── verify_migration.py   # Verification

docs/
  ├── README.md             # User guide
  ├── ARCHITECTURE.md       # System design
  └── ...

templates/
  └── index.html            # Web UI
```

## Areas for Contribution

### High Priority
- [ ] Add more language support (YAML, HCL, Terraform)
- [ ] Improve error messages
- [ ] Add more enhancement suggestions
- [ ] Performance optimization
- [ ] Better test coverage

### Medium Priority
- [ ] Add more LLM providers (local llama.cpp, Hugging Face)
- [ ] Docker support
- [ ] CI/CD improvements
- [ ] API documentation

### Low Priority
- [ ] UI/UX improvements
- [ ] Dark/light theme toggle
- [ ] Multi-file analysis
- [ ] Integration with IDEs

## Feature Development

### Adding a New Analysis Rule

1. **Edit `src/code_reviewer.py`**:
   ```python
   # Add rule to MultiLanguageAnalyzer class
   def analyze_rule_name(self, code: str) -> List[Dict]:
       """Description of what this rule checks."""
       issues = []
       # Implementation here
       return issues
   ```

2. **Add tests in `tests/test_reviewer.py`**:
   ```python
   def test_rule_name():
       code = "bad code example"
       reviewer = CodeReviewer(code, "file.py")
       reviewer.review()
       assert len(reviewer.issues) > 0
   ```

3. **Document in docstring**:
   ```python
   """
   Check for specific issue.
   
   Returns:
       List of dicts with:
           - rule: Rule name
           - message: Description
           - severity: error/warning/info
           - line: Line number
   """
   ```

### Adding a New Enhancement Category

1. **Edit `src/enhancements.py`**:
   ```python
   # Add to EnhancementType enum
   class EnhancementType(Enum):
       NEW_CATEGORY = "new_category"
   ```

2. **Add suggestion logic**:
   ```python
   def suggest_new_category(self, code: str, language: str) -> List[Dict]:
       """Generate suggestions for new category."""
       suggestions = []
       # Implementation
       return suggestions
   ```

3. **Add tests and documentation**

## Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Error message and traceback
- Minimal code example that reproduces the issue
- Expected behavior vs actual behavior

## Feature Requests

When requesting features:

- Describe the use case
- Explain why it would be useful
- Show example usage
- Suggest implementation approach if possible

## Pull Request Process

1. **Update Your Branch**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run Tests**
   ```bash
   python3 -m pytest tests/ -v
   flake8 src/ app.py
   black src/ app.py --check
   ```

3. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**
   - Use descriptive title
   - Include description of changes
   - Reference related issues
   - Ensure CI passes

5. **Code Review**
   - Address review comments
   - Ensure tests pass
   - Update documentation if needed

6. **Merge**
   - Maintainers will merge when ready
   - Your contribution is now live!

## Code Review Guidelines

We look for:

- ✅ Clear, readable code
- ✅ Proper error handling
- ✅ Test coverage
- ✅ Documentation
- ✅ No breaking changes
- ✅ Performance considerations
- ✅ Security implications

## Questions?

- Check existing GitHub issues
- Read the documentation in `docs/`
- Start a GitHub Discussion
- Email: support@example.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Code Reviewer!** 🚀
