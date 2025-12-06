"""
Web UI for Code Reviewer using Flask
Supports multiple programming languages with enhancements
Integrated with open-source LLM via Ollama
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, render_template, request, jsonify
from code_reviewer import CodeReviewer, Severity, detect_language, MultiLanguageAnalyzer
from enhancements import EnhancementSuggestions, EnhancementType
from llm_handler import MultiLLMHandler, LLMProvider
from mcp_server import MCPAgentOrchestrator, MCPRequest
import json
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize LLM and MCP systems
llm_handler = None
mcp_orchestrator = None

def init_llm_systems():
    """Initialize LLM and MCP systems on startup"""
    global llm_handler, mcp_orchestrator
    
    try:
        llm_handler = MultiLLMHandler()
        print(f"✓ LLM Handler initialized. Active provider: {llm_handler.get_active_provider_name()}")
    except Exception as e:
        print(f"⚠ LLM Handler initialization failed: {str(e)}")
        llm_handler = None
    
    try:
        mcp_orchestrator = MCPAgentOrchestrator()
        
        # Create agents for open-source LLM providers via Ollama
        available_providers = {
            'ollama_mistral': 'ollama/mistral',
            'ollama_codellama': 'ollama/codellama',
        }
        
        for provider, model_spec in available_providers.items():
            try:
                agent_id = mcp_orchestrator.create_agent(provider, model_spec)
                print(f"✓ MCP Agent created: {agent_id} ({model_spec})")
            except Exception as e:
                print(f"⚠ Failed to create {provider} agent: {str(e)}")
        
        # Register default workflows for open-source models
        if mcp_orchestrator.agents:
            first_agent = list(mcp_orchestrator.agents.keys())[0]
            mcp_orchestrator.register_workflow('code_review', [
                {'tool': 'code_refinement', 'agent': first_agent, 'priority': 1},
                {'tool': 'code_optimization', 'agent': first_agent, 'priority': 2},
            ])
        
        agent_count = len(mcp_orchestrator.agents) if mcp_orchestrator.agents else 0
        print(f"✓ MCP Orchestrator initialized with {agent_count} open-source agents")
    except Exception as e:
        print(f"⚠ MCP Orchestrator initialization failed: {str(e)}")
        mcp_orchestrator = None

# Initialize on startup
@app.before_request
def startup():
    """Initialize systems on first request"""
    if llm_handler is None:
        init_llm_systems()



@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/review', methods=['POST'])
def review_code():
    """API endpoint to review code"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        filename = data.get('filename', 'code.py')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Detect language
        language = detect_language(filename, code)
        
        # Run review
        if language == 'python':
            reviewer = CodeReviewer(code, filename)
            reviewer.review()
            report = reviewer.get_report()
        else:
            # Use multi-language analyzer for non-Python code
            analyzer = MultiLanguageAnalyzer(code, language)
            issues = analyzer.analyze()
            
            # Build report
            report = {
                'filename': filename,
                'language': language,
                'status': 'passed' if not issues else 'issues_found',
                'total_issues': len(issues),
                'issues': [
                    {
                        'line': issue.line,
                        'column': issue.column,
                        'severity': issue.severity.value,
                        'code': issue.code,
                        'message': issue.message,
                        'suggestion': issue.suggestion,
                        'category': issue.category
                    }
                    for issue in issues
                ],
                'by_severity': {},
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify({
            'status': 'success',
            'report': report,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/review-file', methods=['POST'])
def review_file():
    """API endpoint to review uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        try:
            code = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return jsonify({'error': 'File must be UTF-8 encoded'}), 400
        
        # Detect language and run review
        filename = file.filename or 'code.txt'
        language = detect_language(filename, code)
        
        if language == 'python':
            reviewer = CodeReviewer(code, filename)
            reviewer.review()
            report = reviewer.get_report()
        else:
            # Use multi-language analyzer
            analyzer = MultiLanguageAnalyzer(code, language)
            issues = analyzer.analyze()
            
            report = {
                'filename': filename,
                'language': language,
                'status': 'passed' if not issues else 'issues_found',
                'total_issues': len(issues),
                'issues': [
                    {
                        'line': issue.line,
                        'column': issue.column,
                        'severity': issue.severity.value,
                        'code': issue.code,
                        'message': issue.message,
                        'suggestion': issue.suggestion,
                        'category': issue.category
                    }
                    for issue in issues
                ]
            }
        
        return jsonify({
            'status': 'success',
            'report': report,
            'filename': filename,
            'language': language,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples')
def get_examples():
    """Get example code snippets"""
    examples = {
        'bad_code': '''def calculate_something(x, y, z, a, b, c, d):
    """Very complex function with too many parameters"""
    print("Processing...")
    
    try:
        result = eval(f"x + y + {z}")
    except:
        result = 0
    
    # Multiple statements on one line
    a = 1; b = 2; c = 3
    
    # Long lines that exceed 100 characters should be split for better readability
    very_long_variable_name = "This is a very long line that exceeds the recommended line length limit"
    
    if result > 10:
        if result > 20:
            if result > 30:
                if result > 40:
                    if result > 50:
                        return result * 2
    
    return result
''',
        'good_code': '''def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b


def process_data(items: list) -> list:
    """
    Process a list of items.
    
    Args:
        items: List of items to process
        
    Returns:
        Processed items
    """
    processed = []
    
    for item in items:
        try:
            if item and isinstance(item, dict):
                processed.append(item)
        except TypeError as e:
            logger.error(f"Error processing item: {e}")
            continue
    
    return processed
'''
    }
    
    return jsonify(examples)

@app.route('/api/rules')
def get_rules():
    """Get list of all review rules"""
    rules = {
        'critical': [
            {
                'code': 'DANGEROUS_FUNCTION',
                'message': 'Use of eval() or exec() is dangerous',
                'suggestion': 'Use safer alternatives or validate input thoroughly'
            },
            {
                'code': 'HARDCODED_SECRET',
                'message': 'Hardcoded secret/credential detected',
                'suggestion': 'Use environment variables or secure config management'
            },
            {
                'code': 'SYNTAX_ERROR',
                'message': 'Syntax Error',
                'suggestion': 'Fix syntax error before reviewing'
            }
        ],
        'high': [
            {
                'code': 'BARE_EXCEPT',
                'message': 'Bare except clause catches all exceptions',
                'suggestion': 'Specify exception type: except Exception: or specific exception'
            }
        ],
        'medium': [
            {
                'code': 'HIGH_COMPLEXITY',
                'message': 'Function has high cyclomatic complexity',
                'suggestion': 'Break into smaller functions'
            },
            {
                'code': 'LONG_FUNCTION',
                'message': 'Function is too long',
                'suggestion': 'Break into smaller, focused functions'
            },
            {
                'code': 'TOO_MANY_PARAMS',
                'message': 'Function has too many parameters',
                'suggestion': 'Use dataclass/dict to group related parameters'
            },
            {
                'code': 'GLOBAL_VARIABLE',
                'message': 'Global variable detected',
                'suggestion': 'Use constants in a class or pass as parameters'
            },
            {
                'code': 'PRINT_STATEMENT',
                'message': 'Using print() for logging',
                'suggestion': 'Use logging module: import logging; logging.info()'
            }
        ],
        'low': [
            {
                'code': 'BAD_VARIABLE_NAME',
                'message': 'Single-letter variable name',
                'suggestion': 'Use meaningful names like count, index, user_id'
            },
            {
                'code': 'INVALID_FUNCTION_NAME',
                'message': 'Function should use snake_case',
                'suggestion': 'Rename to snake_case: my_function instead of myFunction'
            },
            {
                'code': 'LINE_TOO_LONG',
                'message': 'Line is too long (>100 characters)',
                'suggestion': 'Keep lines under 100 characters for readability'
            },
            {
                'code': 'MULTIPLE_STATEMENTS',
                'message': 'Multiple statements on one line',
                'suggestion': 'Put each statement on a separate line'
            },
            {
                'code': 'MISSING_DOCSTRING',
                'message': 'No docstring found',
                'suggestion': 'Add docstring describing purpose, params, and return'
            }
        ]
    }
    
    return jsonify(rules)

@app.route('/api/enhancements', methods=['POST'])
def get_enhancements():
    """Get code enhancement suggestions"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Generate enhancement suggestions
        enhancer = EnhancementSuggestions(code, language)
        enhancements = enhancer.analyze()
        
        return jsonify({
            'status': 'success',
            'language': language,
            'enhancements': [
                {
                    'type': e.type.value,
                    'title': e.title,
                    'description': e.description,
                    'current_example': e.current_example,
                    'improved_example': e.improved_example,
                    'impact': e.impact,
                    'effort': e.effort,
                    'priority': e.priority
                }
                for e in enhancements
            ],
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refine-code', methods=['POST'])
def refine_code():
    """API endpoint to refine code using LLM (with demo fallback)"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        issues = data.get('issues', [])
        enhancement = data.get('enhancement')
        provider = data.get('provider')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Try LLM refinement if available
        refined_code = code
        used_provider = 'none'
        
        if llm_handler and llm_handler.active_provider:
            try:
                refined_code = llm_handler.refine_code(code, language, issues, enhancement, provider)
                used_provider = llm_handler.get_active_provider_name()
            except Exception as e:
                print(f"LLM refinement failed: {str(e)}")
                # Fall back to demo mode
                refined_code = llm_handler.refine_code_demo(code, language, issues)
                used_provider = 'demo'
        else:
            # Use demo mode if no LLM available
            if llm_handler:
                refined_code = llm_handler.refine_code_demo(code, language, issues)
                used_provider = 'demo'
        
        return jsonify({
            'status': 'success',
            'original_code': code,
            'refined_code': refined_code,
            'provider': used_provider,
            'language': language,
            'note': 'Using demo mode - set API keys for LLM features' if used_provider == 'demo' else None,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm-providers', methods=['GET'])
def get_llm_providers():
    """Get available open-source LLM providers"""
    try:
        if not llm_handler:
            return jsonify({
                'providers': {'demo': True},
                'active': 'demo',
                'message': 'Using demo mode - install Ollama for AI-powered features',
                'demo_available': True,
                'setup': llm_handler.get_setup_instructions() if llm_handler else get_ollama_setup()
            })
        
        status = llm_handler.get_provider_status()
        
        return jsonify({
            'providers': status['providers'],
            'active': status['active_provider'],
            'demo_available': True,
            'status': 'ready',
            'message': 'Open-source LLM ready! No API keys required.' if status['active_provider'] == 'ollama' else 'Using demo mode - install Ollama for AI features',
            'setup': llm_handler.get_setup_instructions()
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'demo_available': True}), 500

def get_ollama_setup() -> str:
    """Get Ollama setup instructions"""
    return """
🚀 Quick Setup - Open-Source LLM

1. Install Ollama: https://ollama.ai/download
2. Start Ollama: ollama serve
3. Pull a model: ollama pull mistral
4. Code Reviewer will auto-detect it!
"""

@app.route('/api/code-suggestions', methods=['POST'])
def generate_code_suggestions():
    """Generate multiple code improvement suggestions using LLM"""
    try:
        if not llm_handler or not llm_handler.active_provider:
            return jsonify({'error': 'No LLM provider available'}), 503
        
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        issue_types = data.get('issue_types', [])
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Generate suggestions
        suggestions = llm_handler.generate_code_suggestions(code, language, issue_types)
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions,
            'count': len(suggestions),
            'provider': llm_handler.get_active_provider_name()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/agents', methods=['GET'])
def get_mcp_agents():
    """Get information about MCP agents"""
    try:
        if not mcp_orchestrator:
            return jsonify({
                'agents': [],
                'message': 'MCP Orchestrator not initialized'
            })
        
        agents_info = mcp_orchestrator.get_agents_info()
        
        return jsonify({
            'agents': agents_info,
            'total': len(agents_info),
            'status': 'ready'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/orchestrate', methods=['POST'])
def orchestrate_review():
    """Orchestrate multi-agent code review using MCP"""
    try:
        if not mcp_orchestrator:
            return jsonify({'error': 'MCP Orchestrator not available'}), 503
        
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        issues = data.get('issues', [])
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Run orchestrated review
        results = mcp_orchestrator.orchestrate_code_review(code, language, issues)
        
        return jsonify({
            'status': 'success',
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/workflow', methods=['POST'])
def execute_workflow():
    """Execute a registered MCP workflow"""
    try:
        if not mcp_orchestrator:
            return jsonify({'error': 'MCP Orchestrator not available'}), 503
        
        data = request.get_json()
        workflow_name = data.get('workflow', 'code_review')
        input_data = data.get('data', {})
        
        # Execute workflow
        result = mcp_orchestrator.execute_workflow(workflow_name, input_data)
        
        return jsonify({
            'status': 'success',
            'workflow': workflow_name,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize LLM systems
    init_llm_systems()
    
    # Start Flask app
    app.run(debug=True, port=5002)


