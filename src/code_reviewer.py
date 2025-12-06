"""
Code Reviewer - Static Analysis Based Code Review System
Reviews multiple languages without using LLM APIs
Supports: Python, JavaScript, TypeScript, Java, C#, Go, Rust, etc.
"""

import ast
import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum

class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class CodeIssue:
    """Represents a code review issue"""
    line: int
    column: int
    severity: Severity
    code: str
    message: str
    suggestion: str
    category: str

class CodeAnalyzer(ast.NodeVisitor):
    """AST-based code analyzer"""
    
    def __init__(self, code: str, filename: str = ""):
        self.code = code
        self.filename = filename
        self.issues: List[CodeIssue] = []
        self.lines = code.split('\n')
        self.imports = set()
        self.functions = {}
        self.classes = {}
    
    def analyze(self) -> List[CodeIssue]:
        """Run analysis on code"""
        try:
            tree = ast.parse(self.code)
            self.visit(tree)
        except SyntaxError as e:
            self.issues.append(CodeIssue(
                line=e.lineno or 1,
                column=e.offset or 0,
                severity=Severity.CRITICAL,
                code="SYNTAX_ERROR",
                message=f"Syntax Error: {e.msg}",
                suggestion="Fix syntax error before reviewing",
                category="Syntax"
            ))
        
        return self.issues
    
    def visit_Import(self, node: ast.Import) -> None:
        """Check imports"""
        for alias in node.names:
            self.imports.add(alias.name)
            # Check for unused imports later
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check from imports"""
        for alias in node.names:
            self.imports.add(f"{node.module}.{alias.name}")
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Analyze function definitions"""
        self.functions[node.name] = node
        
        # Check function complexity
        complexity = self._calculate_complexity(node)
        if complexity >= 10:
            self.issues.append(CodeIssue(
                line=node.lineno,
                column=0,
                severity=Severity.HIGH,
                code="HIGH_COMPLEXITY",
                message=f"Function '{node.name}' has high cyclomatic complexity: {complexity}",
                suggestion="Consider breaking this function into smaller functions",
                category="Complexity"
            ))
        
        # Check function length
        func_length = len(ast.get_source_segment(self.code, node).split('\n')) if ast.get_source_segment(self.code, node) else 0
        if func_length > 50:
            self.issues.append(CodeIssue(
                line=node.lineno,
                column=0,
                severity=Severity.MEDIUM,
                code="LONG_FUNCTION",
                message=f"Function '{node.name}' is too long ({func_length} lines)",
                suggestion="Consider breaking this function into smaller, more focused functions",
                category="Size"
            ))
        
        # Check for missing docstring
        if not ast.get_docstring(node):
            self.issues.append(CodeIssue(
                line=node.lineno,
                column=0,
                severity=Severity.LOW,
                code="MISSING_DOCSTRING",
                message=f"Function '{node.name}' has no docstring",
                suggestion="Add a docstring describing what the function does, parameters, and return value",
                category="Documentation"
            ))
        
        # Check for too many parameters
        if len(node.args.args) > 5:
            self.issues.append(CodeIssue(
                line=node.lineno,
                column=0,
                severity=Severity.MEDIUM,
                code="TOO_MANY_PARAMS",
                message=f"Function '{node.name}' has too many parameters: {len(node.args.args)}",
                suggestion="Consider refactoring to use a dataclass or dictionary to group related parameters",
                category="Design"
            ))
        
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Analyze class definitions"""
        self.classes[node.name] = node
        
        # Check for missing docstring
        if not ast.get_docstring(node):
            self.issues.append(CodeIssue(
                line=node.lineno,
                column=0,
                severity=Severity.LOW,
                code="MISSING_DOCSTRING",
                message=f"Class '{node.name}' has no docstring",
                suggestion="Add a docstring describing the class purpose and usage",
                category="Documentation"
            ))
        
        self.generic_visit(node)
    
    def visit_For(self, node: ast.For) -> None:
        """Check for inefficient loops"""
        self.generic_visit(node)
    
    def visit_With(self, node: ast.With) -> None:
        """Check context managers"""
        self.generic_visit(node)
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
        return complexity


class PatternAnalyzer:
    """Pattern-based code review"""
    
    def __init__(self, code: str):
        self.code = code
        self.lines = code.split('\n')
        self.issues: List[CodeIssue] = []
    
    def analyze(self) -> List[CodeIssue]:
        """Run pattern-based analysis"""
        self._check_naming_conventions()
        self._check_code_smells()
        self._check_security_issues()
        self._check_best_practices()
        return self.issues
    
    def _check_naming_conventions(self) -> None:
        """Check Python naming conventions"""
        for i, line in enumerate(self.lines, 1):
            # Check for bad variable names
            if re.search(r'\b(x|y|z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w)\s*=', line):
                # Skip loop variables
                if 'for' not in line:
                    self.issues.append(CodeIssue(
                        line=i,
                        column=0,
                        severity=Severity.LOW,
                        code="BAD_VARIABLE_NAME",
                        message="Single-letter variable name is not descriptive",
                        suggestion="Use meaningful variable names (e.g., 'count', 'index', 'user_id')",
                        category="Naming"
                    ))
            
            # Check for snake_case in function names
            func_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
            if func_match:
                func_name = func_match.group(1)
                if re.search(r'[A-Z]', func_name) and not func_name.startswith('_'):
                    self.issues.append(CodeIssue(
                        line=i,
                        column=0,
                        severity=Severity.LOW,
                        code="INVALID_FUNCTION_NAME",
                        message=f"Function '{func_name}' should use snake_case",
                        suggestion="Rename to use snake_case: e.g., 'my_function' instead of 'myFunction'",
                        category="Naming"
                    ))
    
    def _check_code_smells(self) -> None:
        """Check for code smells"""
        for i, line in enumerate(self.lines, 1):
            # Check for bare except
            if re.search(r'except\s*:', line):
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.HIGH,
                    code="BARE_EXCEPT",
                    message="Bare 'except:' clause catches all exceptions including SystemExit",
                    suggestion="Specify the exception type: 'except Exception:' or specific exception",
                    category="Error Handling"
                ))
            
            # Check for print statements (should use logging)
            if re.search(r'\bprint\s*\(', line) and 'debug' not in line.lower():
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.MEDIUM,
                    code="PRINT_STATEMENT",
                    message="Using print() for logging - consider using logging module",
                    suggestion="Use logging module: import logging; logging.info()",
                    category="Best Practice"
                ))
            
            # Check for global variables
            if re.match(r'^[A-Z_][A-Z_0-9]*\s*=', line) and not line.strip().startswith('#'):
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.MEDIUM,
                    code="GLOBAL_VARIABLE",
                    message="Global variable detected",
                    suggestion="Consider using constants in a class or passing values as parameters",
                    category="Design"
                ))
    
    def _check_security_issues(self) -> None:
        """Check for security issues"""
        for i, line in enumerate(self.lines, 1):
            # Check for eval/exec
            if re.search(r'\b(eval|exec)\s*\(', line):
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.CRITICAL,
                    code="DANGEROUS_FUNCTION",
                    message=f"Use of {'eval' if 'eval' in line else 'exec'}() is dangerous",
                    suggestion="Use safer alternatives or validate input thoroughly",
                    category="Security"
                ))
            
            # Check for hardcoded credentials
            if re.search(r'(password|api_key|secret|token)\s*=\s*["\']', line, re.IGNORECASE):
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.CRITICAL,
                    code="HARDCODED_SECRET",
                    message="Hardcoded secret/credential detected",
                    suggestion="Use environment variables or secure config management",
                    category="Security"
                ))
    
    def _check_best_practices(self) -> None:
        """Check for best practices"""
        for i, line in enumerate(self.lines, 1):
            # Check for line length
            if len(line) > 100:
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.LOW,
                    code="LINE_TOO_LONG",
                    message=f"Line is too long ({len(line)} characters)",
                    suggestion="Keep lines under 100 characters for readability",
                    category="Style"
                ))
            
            # Check for multiple statements on one line
            if ';' in line and not line.strip().startswith('#'):
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.LOW,
                    code="MULTIPLE_STATEMENTS",
                    message="Multiple statements on one line",
                    suggestion="Put each statement on a separate line for clarity",
                    category="Style"
                ))


class CodeReviewer:
    """Main code reviewer orchestrator"""
    
    def __init__(self, code: str, filename: str = ""):
        self.code = code
        self.filename = filename
        self.issues: List[CodeIssue] = []
    
    def review(self) -> List[CodeIssue]:
        """Run complete code review"""
        # Run AST analysis
        ast_analyzer = CodeAnalyzer(self.code, self.filename)
        self.issues.extend(ast_analyzer.analyze())
        
        # Run pattern analysis
        pattern_analyzer = PatternAnalyzer(self.code)
        self.issues.extend(pattern_analyzer.analyze())
        
        # Sort by line number
        self.issues.sort(key=lambda x: (x.line, x.column))
        
        return self.issues
    
    def get_report(self) -> Dict:
        """Generate review report"""
        # Count by severity
        severity_count = {}
        for issue in self.issues:
            severity = issue.severity.value
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        return {
            "filename": self.filename,
            "status": "passed" if not self.issues else "issues_found",
            "total_issues": len(self.issues),
            "by_severity": severity_count,
            "issues": [
                {
                    "line": issue.line,
                    "column": issue.column,
                    "severity": issue.severity.value,
                    "code": issue.code,
                    "message": issue.message,
                    "suggestion": issue.suggestion,
                    "category": issue.category
                }
                for issue in self.issues
            ]
        }
    
    def print_report(self) -> None:
        """Print human-readable report"""
        report = self.get_report()
        
        print("\n" + "="*70)
        print(f"CODE REVIEW REPORT - {self.filename}")
        print("="*70)
        
        if report["total_issues"] == 0:
            print("\n✅ No issues found!")
        else:
            print(f"\n📊 Total Issues: {report['total_issues']}")
            print(f"Severity Breakdown: {report['by_severity']}\n")
            
            # Group by category
            by_category = {}
            for issue in self.issues:
                if issue.category not in by_category:
                    by_category[issue.category] = []
                by_category[issue.category].append(issue)
            
            for category, issues in sorted(by_category.items()):
                print(f"\n📋 {category}:")
                print("-" * 70)
                
                for issue in issues:
                    severity_icon = {
                        Severity.CRITICAL: "🔴",
                        Severity.HIGH: "🟠",
                        Severity.MEDIUM: "🟡",
                        Severity.LOW: "🔵",
                        Severity.INFO: "⚪"
                    }
                    
                    print(f"\n{severity_icon.get(issue.severity, '❓')} "
                          f"Line {issue.line} | {issue.severity.value.upper()}")
                    print(f"   Code: {issue.code}")
                    print(f"   Message: {issue.message}")
                    print(f"   Suggestion: {issue.suggestion}")
        
        print("\n" + "="*70 + "\n")


def detect_language(filename: str, code: str) -> str:
    """Detect programming language from filename and code"""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    ext_to_lang = {
        # Python
        'py': 'python',
        'pyw': 'python',
        'pyx': 'python',
        
        # JavaScript & TypeScript
        'js': 'javascript',
        'mjs': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        'jsx': 'javascript',
        
        # Java & JVM
        'java': 'java',
        'kt': 'kotlin',
        'groovy': 'groovy',
        'scala': 'scala',
        
        # C Family
        'c': 'c',
        'h': 'c',
        'cpp': 'cpp',
        'cc': 'cpp',
        'cxx': 'cpp',
        'c++': 'cpp',
        'hpp': 'cpp',
        'h++': 'cpp',
        
        # C#
        'cs': 'csharp',
        
        # Go
        'go': 'go',
        
        # Rust
        'rs': 'rust',
        
        # Ruby
        'rb': 'ruby',
        'erb': 'ruby',
        
        # PHP
        'php': 'php',
        'php3': 'php',
        'php4': 'php',
        'php5': 'php',
        'php7': 'php',
        'phtml': 'php',
        
        # Swift
        'swift': 'swift',
        
        # Objective-C
        'm': 'objc',
        'mm': 'objc',
        
        # Shell
        'sh': 'shell',
        'bash': 'shell',
        'zsh': 'shell',
        'fish': 'shell',
        
        # SQL
        'sql': 'sql',
        
        # Markup
        'html': 'html',
        'htm': 'html',
        'xml': 'xml',
        'json': 'json',
        'yaml': 'yaml',
        'yml': 'yaml',
        'toml': 'toml',
        
        # Other
        'dart': 'dart',
        'go': 'golang',
        'r': 'r',
        'lua': 'lua',
        'pl': 'perl',
        'vb': 'vbnet',
        'f90': 'fortran',
        'pas': 'pascal',
    }
    
    if ext in ext_to_lang:
        return ext_to_lang[ext]
    
    # Fallback to code analysis
    code_lower = code.lower()
    
    if 'def ' in code_lower or 'import ' in code_lower or 'from ' in code_lower:
        return 'python'
    elif 'function ' in code_lower or 'const ' in code_lower or 'let ' in code_lower:
        return 'javascript'
    elif 'public class' in code_lower or 'private class' in code_lower:
        return 'java'
    elif 'func ' in code_lower or 'package ' in code_lower:
        return 'go'
    elif 'fn ' in code_lower or ('let ' in code_lower and 'mut ' in code_lower):
        return 'rust'
    elif 'package;' in code_lower or 'use strict' in code_lower:
        return 'javascript'
    elif '#include' in code_lower or 'using namespace' in code_lower:
        return 'cpp'
    elif '#include' in code_lower and ('int main' in code_lower or 'void main' in code_lower):
        return 'c'
    elif 'class ' in code_lower and ':' in code_lower:
        return 'python'
    
    return 'unknown'



class MultiLanguageAnalyzer:
    """Generic pattern-based analyzer for multiple languages"""
    
    def __init__(self, code: str, language: str):
        self.code = code
        self.language = language
        self.lines = code.split('\n')
        self.issues: List[CodeIssue] = []
    
    def analyze(self) -> List[CodeIssue]:
        """Run generic analysis on code"""
        self._check_generic_issues()
        self._check_complexity_metrics()
        self._check_security_patterns()
        self._check_naming_patterns()
        return self.issues
    
    def _check_generic_issues(self) -> None:
        """Check for generic code issues"""
        for i, line in enumerate(self.lines, 1):
            # Check for TODO/FIXME comments
            if re.search(r'#|//|/\*.*\*/', line):
                if re.search(r'TODO|FIXME|BUG|HACK', line):
                    self.issues.append(CodeIssue(
                        line=i,
                        column=0,
                        severity=Severity.INFO,
                        code="TODO_COMMENT",
                        message="TODO/FIXME comment found in code",
                        suggestion="Address the TODO or remove the comment",
                        category="Code Quality"
                    ))
            
            # Check for debug prints
            if re.search(r'(console\.(log|error|warn)|print\(|println!|System\.out|Debug\.|printf)', line):
                if not re.search(r'logger|LOG|log\.|logging', line):
                    self.issues.append(CodeIssue(
                        line=i,
                        column=0,
                        severity=Severity.LOW,
                        code="DEBUG_OUTPUT",
                        message="Debug output found in code",
                        suggestion="Use a logger instead or remove before production",
                        category="Code Quality"
                    ))
            
            # Check for magic numbers
            if re.search(r'=\s*[0-9]{3,}(?!\d)', line) and 'const' not in line and 'define' not in line:
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.LOW,
                    code="MAGIC_NUMBER",
                    message="Magic number found in code",
                    suggestion="Extract magic number to a named constant",
                    category="Code Quality"
                ))
    
    def _check_complexity_metrics(self) -> None:
        """Check code complexity metrics"""
        for i, line in enumerate(self.lines, 1):
            # Check for deeply nested blocks
            indent = len(line) - len(line.lstrip())
            if indent > 32:  # 8 levels of indentation
                self.issues.append(CodeIssue(
                    line=i,
                    column=indent,
                    severity=Severity.MEDIUM,
                    code="DEEP_NESTING",
                    message="Code is deeply nested",
                    suggestion="Refactor to reduce nesting levels",
                    category="Complexity"
                ))
            
            # Check for long lines
            if len(line) > 120:
                self.issues.append(CodeIssue(
                    line=i,
                    column=120,
                    severity=Severity.LOW,
                    code="LINE_TOO_LONG",
                    message=f"Line is too long ({len(line)} characters)",
                    suggestion="Break line into multiple lines for readability",
                    category="Style"
                ))
    
    def _check_security_patterns(self) -> None:
        """Check for common security issues"""
        for i, line in enumerate(self.lines, 1):
            # Check for hardcoded credentials
            if re.search(r'(password|apikey|secret|token)\s*[:=].*["\']', line, re.IGNORECASE):
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.CRITICAL,
                    code="HARDCODED_SECRET",
                    message="Hardcoded secret found in code",
                    suggestion="Use environment variables or secure vaults",
                    category="Security"
                ))
            
            # Check for SQL injection risks
            if re.search(r'(SELECT|INSERT|UPDATE|DELETE|query|sql).*[\+]|.*f["' + "'" + r']|.*%|.*format', line, re.IGNORECASE):
                if not re.search(r'prepared|parameterized|bind', line, re.IGNORECASE):
                    self.issues.append(CodeIssue(
                        line=i,
                        column=0,
                        severity=Severity.HIGH,
                        code="SQL_INJECTION_RISK",
                        message="Potential SQL injection vulnerability",
                        suggestion="Use parameterized queries or prepared statements",
                        category="Security"
                    ))
            
            # Check for command injection
            if re.search(r'(exec|system|shell|popen|Runtime|Process).*[\+]|.*f["' + "'" + r']|.*format', line, re.IGNORECASE):
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.HIGH,
                    code="COMMAND_INJECTION_RISK",
                    message="Potential command injection vulnerability",
                    suggestion="Avoid string concatenation for command execution",
                    category="Security"
                ))
    
    def _check_naming_patterns(self) -> None:
        """Check naming conventions"""
        for i, line in enumerate(self.lines, 1):
            # Check for single-letter variables (except loop counters)
            if re.search(r'\b[a-z]\s*=', line) and 'for' not in line:
                self.issues.append(CodeIssue(
                    line=i,
                    column=0,
                    severity=Severity.LOW,
                    code="BAD_VARIABLE_NAME",
                    message="Single-letter variable name is unclear",
                    suggestion="Use descriptive variable names",
                    category="Naming"
                ))
