"""
Unit tests for the Flask web UI
"""

import unittest
import json
from app import app

class TestWebUI(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_loads(self):
        """Test that main page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Code Reviewer', response.data)
    
    def test_review_api_no_code(self):
        """Test review API with no code"""
        response = self.client.post('/api/review',
            data=json.dumps({'code': ''}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_review_api_good_code(self):
        """Test review API with good code"""
        code = '''def add(a, b):
    """Add two numbers."""
    return a + b
'''
        response = self.client.post('/api/review',
            data=json.dumps({'code': code, 'filename': 'test.py'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('report', data)
    
    def test_review_api_bad_code(self):
        """Test review API detects issues"""
        code = '''
def func():
    print("test")
    try:
        x = eval("1+1")
    except:
        pass
'''
        response = self.client.post('/api/review',
            data=json.dumps({'code': code, 'filename': 'test.py'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['report']['total_issues'], 0)
    
    def test_examples_api(self):
        """Test examples API"""
        response = self.client.get('/api/examples')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('bad_code', data)
        self.assertIn('good_code', data)
    
    def test_rules_api(self):
        """Test rules API"""
        response = self.client.get('/api/rules')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('critical', data)
        self.assertIn('high', data)
        self.assertIn('medium', data)
        self.assertIn('low', data)

if __name__ == '__main__':
    unittest.main()
