#!/bin/bash
# Setup script for Code Reviewer

echo "🚀 Code Reviewer - Setup"
echo "======================="

# Check Python version
python_version=$(/usr/local/bin/python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
/usr/local/bin/python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment created"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Run tests
echo ""
echo "Running tests..."
/usr/local/bin/python3 test_reviewer.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ All tests passed"
else
    echo "✗ Some tests failed"
    /usr/local/bin/python3 test_reviewer.py
    exit 1
fi

# Show quick demo
echo ""
echo "Quick demo:"
echo "-----------"
/usr/local/bin/python3 cli.py example_bad.py 2>&1 | head -30

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  python cli.py <file.py>          - Review a file"
echo "  python cli.py .                  - Review directory"
echo "  python cli.py <file> --format json - JSON output"
echo ""
echo "Examples:"
echo "  python examples.py               - Run usage examples"
echo "  python test_reviewer.py          - Run tests"
echo ""
