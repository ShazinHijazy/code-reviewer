#!/usr/bin/env python3
"""
Integration tests for Code Reviewer UI
Tests the complete workflow
"""

import unittest
import json
import sys

# Import test client
from app import app

class IntegrationTests(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_workflow_1_review_bad_code(self):
        """Test complete workflow: upload bad code"""
        print("\n🧪 Test 1: Review bad code")
        
        bad_code = '''
def poorly_written_function(x, y, z, a, b):
    print("Processing...")
    try:
        result = eval(f"x + {y}")
    except:
        pass
    password = "secret123"
    return result
'''
        
        response = self.client.post('/api/review',
            data=json.dumps({'code': bad_code}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should find multiple issues
        self.assertGreater(data['report']['total_issues'], 3)
        print(f"   ✓ Found {data['report']['total_issues']} issues")
        
        # Should find critical issues
        self.assertGreater(data['report']['by_severity'].get('critical', 0), 0)
        print(f"   ✓ Detected critical issues")
    
    def test_workflow_2_review_good_code(self):
        """Test complete workflow: review good code"""
        print("\n🧪 Test 2: Review good code")
        
        good_code = '''
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of both numbers
    """
    return a + b
'''
        
        response = self.client.post('/api/review',
            data=json.dumps({'code': good_code}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Good code should have few/no issues
        self.assertLessEqual(data['report']['total_issues'], 1)
        print(f"   ✓ Clean code passed with {data['report']['total_issues']} issue(s)")
    
    def test_workflow_3_test_all_api_endpoints(self):
        """Test all available API endpoints"""
        print("\n🧪 Test 3: Test all API endpoints")
        
        # Test index
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("   ✓ Index page loads")
        
        # Test examples
        response = self.client.get('/api/examples')
        self.assertEqual(response.status_code, 200)
        examples = json.loads(response.data)
        self.assertIn('bad_code', examples)
        self.assertIn('good_code', examples)
        print("   ✓ Examples API works")
        
        # Test rules
        response = self.client.get('/api/rules')
        self.assertEqual(response.status_code, 200)
        rules = json.loads(response.data)
        self.assertIn('critical', rules)
        self.assertIn('high', rules)
        self.assertIn('medium', rules)
        self.assertIn('low', rules)
        print("   ✓ Rules API works")
    
    def test_workflow_4_security_detection(self):
        """Test security issue detection"""
        print("\n🧪 Test 4: Security detection")
        
        security_code = '''
password = "admin123"
api_key = "sk_live_123456"
secret_token = "secret123"
result = eval(user_input)
exec(command)
'''
        
        response = self.client.post('/api/review',
            data=json.dumps({'code': security_code}),
            content_type='application/json')
        
        data = json.loads(response.data)
        critical = data['report']['by_severity'].get('critical', 0)
        
        self.assertGreater(critical, 0)
        print(f"   ✓ Detected {critical} critical security issues")
    
    def test_workflow_5_complexity_detection(self):
        """Test complexity detection"""
        print("\n🧪 Test 5: Complexity detection")
        
        complex_code = '''def complex_function(x):
    if x > 0:
        if x > 10:
            if x > 20:
                if x > 30:
                    if x > 40:
                        if x > 50:
                            if x > 60:
                                if x > 70:
                                    if x > 80:
                                        return True
    return False
'''
        
        response = self.client.post('/api/review',
            data=json.dumps({'code': complex_code}),
            content_type='application/json')
        
        data = json.loads(response.data)
        
        # Should detect high complexity
        issues = data['report']['issues']
        complexity_issues = [i for i in issues if 'COMPLEXITY' in i['code']]
        
        self.assertGreater(len(complexity_issues), 0)
        print(f"   ✓ Detected complexity issues")
    
    def test_workflow_6_style_detection(self):
        """Test style detection"""
        print("\n🧪 Test 6: Style detection")
        
        style_code = '''
x = 1; y = 2; z = 3
a = "This is a very long line that exceeds the recommended 100 character limit and should be flagged as a style issue"
def myFunction():
    pass
'''
        
        response = self.client.post('/api/review',
            data=json.dumps({'code': style_code}),
            content_type='application/json')
        
        data = json.loads(response.data)
        
        # Should detect style issues
        self.assertGreater(data['report']['total_issues'], 0)
        print(f"   ✓ Detected {data['report']['total_issues']} style issues")
    
    def test_workflow_7_report_generation(self):
        """Test report generation with statistics"""
        print("\n🧪 Test 7: Report generation")
        
        test_code = '''
def test_function():
    print("test")
    try:
        eval("1+1")
    except:
        pass
'''
        
        response = self.client.post('/api/review',
            data=json.dumps({'code': test_code}),
            content_type='application/json')
        
        data = json.loads(response.data)
        report = data['report']
        
        # Verify report structure
        self.assertIn('filename', report)
        self.assertIn('status', report)
        self.assertIn('total_issues', report)
        self.assertIn('by_severity', report)
        self.assertIn('issues', report)
        
        print(f"   ✓ Report generated with {len(report['issues'])} issues")
        print(f"   ✓ Report format: {report['status']}")

def run_tests():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("CODE REVIEWER - INTEGRATION TESTS")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(IntegrationTests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())
