"""
Example file with various code issues for testing the reviewer
"""

import os

# Bad: Global variable
MAX_RETRIES = 5

def calculate_something(x, y, z, a, b, c, d):
    """
    Very complex function with too many parameters
    """
    print("Processing...")  # Should use logging
    
    try:
        result = eval(f"x + y + {z}")  # DANGEROUS!
    except:  # Bare except - BAD!
        result = 0
    
    # Line too long warning here - this is a very long line that exceeds the 100 character limit that we recommend for code readability
    
    if result > 10:
        if result > 20:
            if result > 30:
                if result > 40:
                    if result > 50:
                        return result * 2
    
    return result

class DataProcessor:
    # Missing docstring
    
    def process_data(self, data, options, config, settings, params, flags):
        password = "secret123"  # HARDCODED SECRET!
        api_key = "sk_test_123456"  # HARDCODED SECRET!
        
        for x in data:  # Bad variable name
            print(x)
        
        return data

def inefficient_function():
    # Multiple statements on one line (bad)
    a = 1; b = 2; c = 3
    
    # Single letter variable names
    x = 10
    y = 20
    z = x + y
    
    return z
