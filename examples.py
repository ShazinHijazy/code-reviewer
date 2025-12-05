#!/usr/bin/env python3
"""
Advanced usage examples for the Code Reviewer
"""

from code_reviewer import CodeReviewer, Severity

def example_1_basic_review():
    """Example 1: Basic file review"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Code Review")
    print("="*70)
    
    code = """
def calculate(x, y):
    print("Calculating...")
    try:
        result = eval(f"x + y")
    except:
        result = 0
    return result
"""
    
    reviewer = CodeReviewer(code, "calculate.py")
    issues = reviewer.review()
    
    print(f"\nFound {len(issues)} issues:")
    for issue in issues:
        print(f"  • {issue.severity.value}: {issue.message}")

def example_2_json_export():
    """Example 2: Export results as JSON"""
    print("\n" + "="*70)
    print("EXAMPLE 2: JSON Export")
    print("="*70)
    
    import json
    
    code = """
def bad_function():
    password = "secret"
    print(password)
"""
    
    reviewer = CodeReviewer(code, "secrets.py")
    issues = reviewer.review()
    report = reviewer.get_report()
    
    print("\nJSON Report:")
    print(json.dumps(report, indent=2))

def example_3_filtered_review():
    """Example 3: Review by severity"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Filtered Review (Critical Issues Only)")
    print("="*70)
    
    code = """
def my_func():
    eval("1+1")
    password = "secret"
    print("test")
"""
    
    reviewer = CodeReviewer(code, "filtered.py")
    issues = reviewer.review()
    
    # Filter for critical issues
    critical = [i for i in issues if i.severity == Severity.CRITICAL]
    
    print(f"\nCritical Issues ({len(critical)}):")
    for issue in critical:
        print(f"  Line {issue.line}: {issue.message}")
        print(f"  → {issue.suggestion}")

def example_4_category_grouping():
    """Example 4: Group issues by category"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Issues by Category")
    print("="*70)
    
    code = """
import os
MAX_VAL = 100

def process(x, y, z, a, b):
    try:
        eval(x)
    except:
        pass
    return None
"""
    
    reviewer = CodeReviewer(code, "grouped.py")
    issues = reviewer.review()
    
    # Group by category
    by_category = {}
    for issue in issues:
        if issue.category not in by_category:
            by_category[issue.category] = []
        by_category[issue.category].append(issue)
    
    print("\nIssues by Category:")
    for category, cat_issues in sorted(by_category.items()):
        print(f"\n  {category}: {len(cat_issues)} issue(s)")
        for issue in cat_issues:
            print(f"    - {issue.code}: {issue.message}")

def example_5_custom_analysis():
    """Example 5: Custom analysis of code"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Custom Statistics")
    print("="*70)
    
    code = """
def func1():
    x = 1
    return x

def func2(a, b, c, d, e):
    y = 2
    return y

class MyClass:
    def method(self):
        z = 3
        return z
"""
    
    reviewer = CodeReviewer(code, "stats.py")
    issues = reviewer.review()
    
    # Statistics
    total = len(issues)
    by_severity = {}
    for issue in issues:
        sev = issue.severity.value
        by_severity[sev] = by_severity.get(sev, 0) + 1
    
    print(f"\nCode Statistics:")
    print(f"  Total Issues: {total}")
    print(f"  By Severity: {by_severity}")
    print(f"  Critical: {by_severity.get('critical', 0)}")
    print(f"  High: {by_severity.get('high', 0)}")
    print(f"  Medium: {by_severity.get('medium', 0)}")
    print(f"  Low: {by_severity.get('low', 0)}")

def example_6_compare_codes():
    """Example 6: Compare two versions of code"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Code Comparison")
    print("="*70)
    
    old_code = """
def my_func():
    print("hello")
    try:
        x = eval("1+1")
    except:
        pass
"""
    
    new_code = """
import logging

logger = logging.getLogger(__name__)

def my_func():
    try:
        x = 1 + 1
    except ValueError as e:
        logger.error(f"Error: {e}")
"""
    
    print("\n--- OLD CODE ---")
    reviewer_old = CodeReviewer(old_code, "old.py")
    issues_old = reviewer_old.review()
    print(f"Issues: {len(issues_old)}")
    for issue in issues_old:
        print(f"  • {issue.severity.value}: {issue.code}")
    
    print("\n--- NEW CODE ---")
    reviewer_new = CodeReviewer(new_code, "new.py")
    issues_new = reviewer_new.review()
    print(f"Issues: {len(issues_new)}")
    for issue in issues_new:
        print(f"  • {issue.severity.value}: {issue.code}")
    
    print(f"\n✓ Improvement: {len(issues_old) - len(issues_new)} fewer issues")

def main():
    """Run all examples"""
    examples = [
        example_1_basic_review,
        example_2_json_export,
        example_3_filtered_review,
        example_4_category_grouping,
        example_5_custom_analysis,
        example_6_compare_codes,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
