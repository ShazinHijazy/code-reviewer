#!/bin/bash

# Code Reviewer - Production Startup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Code Reviewer - Production Server${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python3 --version

# Install dependencies
echo -e "\n${BLUE}Installing dependencies...${NC}"
pip3 install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Verify modules
echo -e "\n${BLUE}Verifying modules...${NC}"
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from code_reviewer import CodeReviewer
    from enhancements import EnhancementSuggestions
    from llm_handler import MultiLLMHandler
    print('✓ All modules loaded successfully')
except Exception as e:
    print(f'✗ Module load failed: {e}')
    sys.exit(1)
" || exit 1

# Check Ollama (optional)
echo -e "\n${BLUE}Checking for Ollama...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
    OLLAMA_MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; data = json.load(sys.stdin); models = [m['name'].split(':')[0] for m in data.get('models', [])]; print(', '.join(set(models)))" 2>/dev/null || echo "unknown")
    echo -e "${GREEN}  Available models: $OLLAMA_MODELS${NC}"
else
    echo -e "${RED}⚠ Ollama not running (LLM features disabled)${NC}"
    echo -e "  To enable: ollama serve (in another terminal)"
fi

# Display startup info
echo -e "\n${BLUE}Server Configuration:${NC}"
echo -e "  Host: 127.0.0.1"
echo -e "  Port: 5002"
echo -e "  URL: http://127.0.0.1:5002"
echo -e "  Environment: production"

# Start server
echo -e "\n${GREEN}Starting server...${NC}\n"
python3 app.py

echo -e "\n${GREEN}✓ Server stopped${NC}"
