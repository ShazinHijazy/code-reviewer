"""
Unit tests for the Code Reviewer
"""

import unittest
from code_reviewer import CodeReviewer, Severity, CodeIssue

class TestCodeReviewer(unittest.TestCase):
    
    def test_security_eval(self):
        """Test detection of eval() usage"""
        code = """
def calculate():
    result = eval("1 + 1")
    return result
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        # Should have critical issue
        dangerous_issues = [i for i in issues if 'DANGEROUS' in i.code]
        self.assertTrue(len(dangerous_issues) > 0)
    
    def test_hardcoded_secret(self):
        """Test detection of hardcoded secrets"""
        code = """
password = "secret123"
api_key = "sk_test_456"
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        secret_issues = [i for i in issues if 'SECRET' in i.code]
        self.assertEqual(len(secret_issues), 2)
    
    def test_bare_except(self):
        """Test detection of bare except"""
        code = """
try:
    x = 1
except:
    pass
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        bare_except = [i for i in issues if 'BARE_EXCEPT' in i.code]
        self.assertTrue(len(bare_except) > 0)
    
    def test_print_statement(self):
        """Test detection of print statements"""
        code = """
print("Hello, world!")
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        print_issues = [i for i in issues if 'PRINT' in i.code]
        self.assertTrue(len(print_issues) > 0)
    
    def test_missing_docstring(self):
        """Test detection of missing docstrings"""
        code = """
def my_function():
    return 42
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        docstring_issues = [i for i in issues if 'DOCSTRING' in i.code]
        self.assertTrue(len(docstring_issues) > 0)
    
    def test_good_code(self):
        """Test that good code passes"""
        code = """
def add_numbers(a, b):
    '''Add two numbers and return result.'''
    return a + b
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        self.assertEqual(len(issues), 0)
    
    def test_function_complexity(self):
        """Test detection of high complexity"""
        code = """
def complex_function(x):
    if x > 0:
        if x > 10:
            if x > 20:
                if x > 30:
                    if x > 40:
                        if x > 50:
                            if x > 60:
                                if x > 70:
                                    if x > 80:
                                        if x > 90:
                                            return True
    return False
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        complexity_issues = [i for i in issues if 'COMPLEXITY' in i.code]
        self.assertTrue(len(complexity_issues) > 0)
    
    def test_line_too_long(self):
        """Test detection of long lines"""
        code = """
x = "This is a very long line that exceeds the 100 character limit that we recommend for code readability purposes"
"""
        reviewer = CodeReviewer(code)
        issues = reviewer.review()
        
        long_line_issues = [i for i in issues if 'LINE_TOO_LONG' in i.code]
        self.assertTrue(len(long_line_issues) > 0)
    
    def test_report_json(self):
        """Test JSON report generation"""
        code = """
print("test")
"""
        reviewer = CodeReviewer(code, "test.py")
        issues = reviewer.review()
        report = reviewer.get_report()
        
        self.assertEqual(report['filename'], 'test.py')
        self.assertGreater(report['total_issues'], 0)
        self.assertIn('by_severity', report)
        self.assertIn('issues', report)

if __name__ == '__main__':
    unittest.main()
