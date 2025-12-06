"""
Code Enhancement Suggestions Engine
Provides actionable suggestions for code improvements, best practices, and design patterns
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class EnhancementType(Enum):
    """Types of code enhancements"""
    PERFORMANCE = "performance"
    READABILITY = "readability"
    MAINTAINABILITY = "maintainability"
    DESIGN_PATTERN = "design_pattern"
    BEST_PRACTICE = "best_practice"
    TESTING = "testing"
    SECURITY = "security"
    OPTIMIZATION = "optimization"


@dataclass
class Enhancement:
    """Represents a code enhancement suggestion"""
    type: EnhancementType
    title: str
    description: str
    current_example: str
    improved_example: str
    impact: str  # HIGH, MEDIUM, LOW
    effort: str  # EASY, MEDIUM, HARD
    priority: int  # 1-10


class EnhancementSuggestions:
    """Generates code enhancement suggestions"""
    
    def __init__(self, code: str, language: str):
        self.code = code
        self.language = language
        self.lines = code.split('\n')
        self.enhancements: List[Enhancement] = []
    
    def analyze(self) -> List[Enhancement]:
        """Generate enhancement suggestions"""
        self._check_performance()
        self._check_readability()
        self._check_maintainability()
        self._check_design_patterns()
        self._check_best_practices()
        self._check_testing()
        return self.enhancements
    
    def _check_performance(self) -> None:
        """Suggest performance improvements"""
        code = self.code.lower()
        
        # Detect inefficient loops
        if self.language == 'python':
            if 'for ' in code and 'append' in code:
                self.enhancements.append(Enhancement(
                    type=EnhancementType.PERFORMANCE,
                    title="Use List Comprehension",
                    description="List comprehensions are faster and more Pythonic than append in loops",
                    current_example="result = []\nfor item in items:\n    result.append(item * 2)",
                    improved_example="result = [item * 2 for item in items]",
                    impact="HIGH",
                    effort="EASY",
                    priority=8
                ))
        
        # Detect string concatenation in loops
        if '+=' in code and ('for ' in code or 'while ' in code):
            lang_name = 'Java' if self.language == 'java' else \
                       'C#' if self.language == 'csharp' else \
                       'Python' if self.language == 'python' else self.language
            
            self.enhancements.append(Enhancement(
                type=EnhancementType.PERFORMANCE,
                title="Avoid String Concatenation in Loops",
                description="String concatenation in loops creates multiple intermediate strings, harming performance",
                current_example="result = ''\nfor item in items:\n    result += item",
                improved_example=f"# Use StringBuilder/StringBuffer in {lang_name}\nresult = []\nfor item in items:\n    result.append(item)\nfinal = ''.join(result)",
                impact="HIGH",
                effort="MEDIUM",
                priority=7
            ))
    
    def _check_readability(self) -> None:
        """Suggest readability improvements"""
        # Detect magic numbers
        magic_numbers = len([l for l in self.lines if re.match(r'.*=\s*\d{3,}', l)])
        if magic_numbers > 0:
            self.enhancements.append(Enhancement(
                type=EnhancementType.READABILITY,
                title="Replace Magic Numbers with Named Constants",
                description="Magic numbers should be extracted into named constants for clarity",
                current_example="if timeout > 30000:\n    handle_timeout()",
                improved_example="MAX_TIMEOUT_MS = 30000\nif timeout > MAX_TIMEOUT_MS:\n    handle_timeout()",
                impact="MEDIUM",
                effort="EASY",
                priority=6
            ))
        
        # Detect nested conditions
        max_nesting = max([len(l) - len(l.lstrip()) for l in self.lines], default=0) // 4
        if max_nesting > 3:
            self.enhancements.append(Enhancement(
                type=EnhancementType.READABILITY,
                title="Reduce Nesting Depth",
                description="Deeply nested code is harder to read. Use early returns or guard clauses",
                current_example="if condition1:\n    if condition2:\n        if condition3:\n            do_work()",
                improved_example="if not condition1:\n    return\nif not condition2:\n    return\nif not condition3:\n    return\ndo_work()",
                impact="HIGH",
                effort="MEDIUM",
                priority=7
            ))
    
    def _check_maintainability(self) -> None:
        """Suggest maintainability improvements"""
        # Detect functions that are too long
        long_functions = 0
        current_func_lines = 0
        for line in self.lines:
            if re.match(r'^\s*(def|function|public|private|protected)\s+\w+', line):
                if current_func_lines > 50:
                    long_functions += 1
                current_func_lines = 0
            else:
                current_func_lines += 1
        
        if long_functions > 0:
            self.enhancements.append(Enhancement(
                type=EnhancementType.MAINTAINABILITY,
                title="Break Down Large Functions",
                description="Functions should be small and focused. Extract logic into separate functions",
                current_example="def process_data(data):\n    # 80+ lines of logic",
                improved_example="def process_data(data):\n    validated = validate_input(data)\n    transformed = transform_data(validated)\n    return save_result(transformed)",
                impact="HIGH",
                effort="HARD",
                priority=8
            ))
        
        # Suggest proper documentation
        if self.language == 'python' and '"""' not in self.code and "'''" not in self.code:
            self.enhancements.append(Enhancement(
                type=EnhancementType.MAINTAINABILITY,
                title="Add Docstrings",
                description="Document functions with docstrings explaining purpose, parameters, and return values",
                current_example="def calculate_sum(a, b):\n    return a + b",
                improved_example='def calculate_sum(a, b):\n    """Calculate sum of two numbers.\n    Args:\n        a: First number\n        b: Second number\n    Returns:\n        Sum of a and b\n    """\n    return a + b',
                impact="MEDIUM",
                effort="EASY",
                priority=5
            ))
    
    def _check_design_patterns(self) -> None:
        """Suggest design pattern usage"""
        # Detect potential factory pattern
        if 'class' in self.code.lower() and 'create' in self.code.lower():
            self.enhancements.append(Enhancement(
                type=EnhancementType.DESIGN_PATTERN,
                title="Consider Factory Pattern",
                description="Use Factory Pattern for object creation when dealing with multiple types",
                current_example="if type == 'A':\n    obj = ClassA()\nelif type == 'B':\n    obj = ClassB()",
                improved_example="class Factory:\n    @staticmethod\n    def create(type):\n        if type == 'A':\n            return ClassA()\n        elif type == 'B':\n            return ClassB()",
                impact="MEDIUM",
                effort="MEDIUM",
                priority=5
            ))
        
        # Detect potential singleton pattern
        if 'global' in self.code.lower() or 'static' in self.code.lower():
            self.enhancements.append(Enhancement(
                type=EnhancementType.DESIGN_PATTERN,
                title="Consider Singleton Pattern",
                description="Use Singleton Pattern instead of global state for resource management",
                current_example="db = None\ndef get_db():\n    global db\n    if db is None:\n        db = Database()",
                improved_example="class Database:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance",
                impact="MEDIUM",
                effort="MEDIUM",
                priority=6
            ))
    
    def _check_best_practices(self) -> None:
        """Suggest best practices"""
        # Suggest error handling
        if 'try' not in self.code.lower() and 'except' not in self.code.lower():
            if self.language in ['python', 'java', 'csharp']:
                self.enhancements.append(Enhancement(
                    type=EnhancementType.BEST_PRACTICE,
                    title="Add Error Handling",
                    description="Wrap potentially failing code in try-except blocks",
                    current_example="result = risky_operation()",
                    improved_example="try:\n    result = risky_operation()\nexcept Exception as e:\n    log_error(e)\n    result = None",
                    impact="HIGH",
                    effort="MEDIUM",
                    priority=9
                ))
        
        # Suggest logging
        if 'print' in self.code.lower() or 'console.log' in self.code.lower():
            self.enhancements.append(Enhancement(
                type=EnhancementType.BEST_PRACTICE,
                title="Use Logging Instead of Print",
                description="Replace print/console.log with proper logging framework for better control",
                current_example="print(f'Processing item {id}')",
                improved_example="import logging\nlogger = logging.getLogger(__name__)\nlogger.info(f'Processing item {id}')",
                impact="MEDIUM",
                effort="EASY",
                priority=6
            ))
        
        # Suggest validation
        if 'def ' in self.code or 'function' in self.code:
            self.enhancements.append(Enhancement(
                type=EnhancementType.BEST_PRACTICE,
                title="Add Input Validation",
                description="Validate function parameters at entry points",
                current_example="def process(data):\n    return data['key']",
                improved_example="def process(data):\n    if not data or 'key' not in data:\n        raise ValueError('Invalid data')\n    return data['key']",
                impact="HIGH",
                effort="EASY",
                priority=8
            ))
    
    def _check_testing(self) -> None:
        """Suggest testing improvements"""
        if 'test' not in self.code.lower():
            self.enhancements.append(Enhancement(
                type=EnhancementType.TESTING,
                title="Add Unit Tests",
                description="Write unit tests for critical functions to ensure reliability",
                current_example="def calculate(a, b):\n    return a + b",
                improved_example="import unittest\nclass TestCalculate(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(calculate(2, 3), 5)\n    def test_negative(self):\n        self.assertEqual(calculate(-1, 1), 0)",
                impact="HIGH",
                effort="MEDIUM",
                priority=8
            ))


import re
