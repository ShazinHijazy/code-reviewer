"""
Configuration and extension system for Code Reviewer
"""

from typing import List, Dict, Callable
from dataclasses import dataclass
from enum import Enum

@dataclass
class RuleConfig:
    """Configuration for a review rule"""
    name: str
    enabled: bool = True
    severity_override: str = None  # Override default severity
    skip_patterns: List[str] = None  # Regex patterns to skip

class ReviewerConfig:
    """Configuration for the code reviewer"""
    
    def __init__(self):
        self.max_line_length = 100
        self.max_complexity = 10
        self.max_function_length = 50
        self.max_parameters = 5
        self.enabled_rules = {
            'security': True,
            'complexity': True,
            'documentation': True,
            'naming': True,
            'style': True,
            'best_practices': True,
        }
        self.severity_overrides = {}
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'ReviewerConfig':
        """Load configuration from dictionary"""
        config = cls()
        if 'max_line_length' in config_dict:
            config.max_line_length = config_dict['max_line_length']
        if 'max_complexity' in config_dict:
            config.max_complexity = config_dict['max_complexity']
        if 'enabled_rules' in config_dict:
            config.enabled_rules.update(config_dict['enabled_rules'])
        return config
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary"""
        return {
            'max_line_length': self.max_line_length,
            'max_complexity': self.max_complexity,
            'max_function_length': self.max_function_length,
            'max_parameters': self.max_parameters,
            'enabled_rules': self.enabled_rules,
        }

class CustomRuleRegistry:
    """Registry for custom rules"""
    
    def __init__(self):
        self.pattern_rules: List[Callable] = []
        self.ast_visitors: List[Callable] = []
    
    def register_pattern_rule(self, rule_func: Callable) -> None:
        """Register a pattern-based rule"""
        self.pattern_rules.append(rule_func)
    
    def register_ast_visitor(self, visitor_func: Callable) -> None:
        """Register an AST visitor rule"""
        self.ast_visitors.append(visitor_func)

# Example configuration file format (YAML)
EXAMPLE_CONFIG_YAML = """
# Code Reviewer Configuration

# Maximum line length
max_line_length: 100

# Maximum cyclomatic complexity
max_complexity: 10

# Maximum function length (lines)
max_function_length: 50

# Maximum function parameters
max_parameters: 5

# Enable/disable rule categories
enabled_rules:
  security: true
  complexity: true
  documentation: true
  naming: true
  style: true
  best_practices: true

# Severity overrides for specific rules
severity_overrides:
  PRINT_STATEMENT: low  # Changed from medium to low
  MISSING_DOCSTRING: info  # Changed from low to info

# File patterns to exclude
exclude_patterns:
  - "*/migrations/*"
  - "*/tests/*"
  - "*/venv/*"
"""

# Example Python configuration
EXAMPLE_CONFIG_PYTHON = """
from code_reviewer_config import ReviewerConfig, CustomRuleRegistry
from code_reviewer import CodeIssue, Severity

# Create configuration
config = ReviewerConfig()
config.max_line_length = 120
config.max_complexity = 15
config.enabled_rules['documentation'] = False  # Don't check docstrings

# Create custom rule registry
registry = CustomRuleRegistry()

# Define custom rule
def check_todo_comments(lines, issues):
    '''Custom rule to flag TODO comments'''
    for i, line in enumerate(lines, 1):
        if 'TODO' in line:
            issues.append(CodeIssue(
                line=i,
                column=0,
                severity=Severity.INFO,
                code='TODO_FOUND',
                message='TODO comment found',
                suggestion='Resolve or remove TODO',
                category='TODO'
            ))

# Register custom rule
registry.register_pattern_rule(check_todo_comments)
"""

class ConfigLoader:
    """Load configuration from various formats"""
    
    @staticmethod
    def load_yaml(filepath: str) -> ReviewerConfig:
        """Load configuration from YAML file"""
        try:
            import yaml
            with open(filepath, 'r') as f:
                config_dict = yaml.safe_load(f)
            return ReviewerConfig.from_dict(config_dict)
        except ImportError:
            raise ImportError("PyYAML not installed. Install with: pip install pyyaml")
    
    @staticmethod
    def load_json(filepath: str) -> ReviewerConfig:
        """Load configuration from JSON file"""
        import json
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return ReviewerConfig.from_dict(config_dict)
    
    @staticmethod
    def load_python(filepath: str) -> ReviewerConfig:
        """Load configuration from Python file"""
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.config

if __name__ == "__main__":
    # Show example configurations
    print("Example YAML Configuration:")
    print(EXAMPLE_CONFIG_YAML)
    print("\n" + "="*70 + "\n")
    print("Example Python Configuration:")
    print(EXAMPLE_CONFIG_PYTHON)
