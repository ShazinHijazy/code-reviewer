#!/usr/bin/env python3
"""
Open-Source LLM Integration Verification Script
Verifies that the migration from paid LLMs to open-source Ollama is complete
"""

import sys
import os

def check_imports():
    """Verify all imports work"""
    print("🔍 Checking imports...")
    try:
        from opensource_llm import OpenSourceLLMHandler, OpenSourceLLMSelector
        print("  ✓ opensource_llm module loaded")
    except ImportError as e:
        print(f"  ❌ Failed to import opensource_llm: {e}")
        return False
    
    try:
        from llm_handler import MultiLLMHandler, LLMProvider
        print("  ✓ llm_handler module loaded")
    except ImportError as e:
        print(f"  ❌ Failed to import llm_handler: {e}")
        return False
    
    try:
        from code_reviewer import CodeReviewer
        print("  ✓ code_reviewer module loaded")
    except ImportError as e:
        print(f"  ❌ Failed to import code_reviewer: {e}")
        return False
    
    return True

def check_llm_handler():
    """Verify LLM handler works"""
    print("\n🔍 Checking LLM Handler...")
    try:
        from llm_handler import MultiLLMHandler
        handler = MultiLLMHandler()
        
        # Check provider status
        status = handler.get_provider_status()
        print(f"  ✓ Handler initialized")
        print(f"  ✓ Active provider: {status['active_provider']}")
        print(f"  ✓ Demo mode enabled: {status['demo_mode_enabled']}")
        
        # Check providers
        providers = status['providers']
        for provider_name, provider_info in providers.items():
            if 'available' in provider_info:
                if provider_info['available']:
                    print(f"  ✓ {provider_name.upper()} available")
                else:
                    print(f"  ℹ {provider_name.upper()} not available (expected if not installed)")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def check_no_paid_apis():
    """Verify paid LLM APIs were removed from active code"""
    print("\n🔍 Verifying paid LLM APIs removed from active code...")
    
    # Read the llm_handler.py to verify no paid API calls
    with open('llm_handler.py', 'r') as f:
        llm_handler_code = f.read()
    
    paid_api_patterns = {
        'anthropic.Anthropic': 'Claude API initialization',
        'openai.ChatCompletion': 'OpenAI API call',
        'genai.GenerativeModel': 'Google Gemini API call',
        'CLAUDE': 'Claude provider enum',
        'OPENAI': 'OpenAI provider enum',
        'GOOGLE': 'Google provider enum',
    }
    
    found_issues = []
    for pattern, description in paid_api_patterns.items():
        if pattern in llm_handler_code:
            found_issues.append(f"    ⚠ Found {pattern} in llm_handler.py ({description})")
    
    # Check environment variables
    if os.getenv('ANTHROPIC_API_KEY'):
        found_issues.append("  ⚠ ANTHROPIC_API_KEY still set in environment")
    else:
        print("  ✓ ANTHROPIC_API_KEY not set")
    
    if os.getenv('OPENAI_API_KEY'):
        found_issues.append("  ⚠ OPENAI_API_KEY still set in environment")
    else:
        print("  ✓ OPENAI_API_KEY not set")
    
    if os.getenv('GOOGLE_API_KEY'):
        found_issues.append("  ⚠ GOOGLE_API_KEY still set in environment")
    else:
        print("  ✓ GOOGLE_API_KEY not set")
    
    # Check llm_handler.py uses opensource_llm
    if 'opensource_llm' in llm_handler_code and 'OpenSourceLLMHandler' in llm_handler_code:
        print("  ✓ llm_handler.py uses opensource_llm module")
    else:
        found_issues.append("  ❌ llm_handler.py doesn't use opensource_llm")
    
    if 'OllamaModel' in llm_handler_code or 'Ollama' in llm_handler_code:
        print("  ✓ Ollama support added to llm_handler.py")
    else:
        found_issues.append("  ⚠ Ollama support not found in llm_handler.py")
    
    # Note about installed libraries
    print("  ℹ Note: Paid API libraries may still be installed as dependencies")
    print("          but are not used in active code - this is OK")
    
    for issue in found_issues:
        print(issue)
    
    return len(found_issues) == 0

def check_demo_mode():
    """Verify demo mode works"""
    print("\n🔍 Checking demo mode fallback...")
    try:
        from llm_handler import MultiLLMHandler
        handler = MultiLLMHandler()
        
        test_code = "for i in range(len(items)):\n    result = result + items[i]"
        refined = handler.refine_code_demo(test_code, "python", [])
        
        if refined and len(refined) > 0:
            print("  ✓ Demo mode refinement works")
            print(f"    Input:  {test_code.split(chr(10))[0][:50]}...")
            print(f"    Output: {refined.split(chr(10))[0][:50]}...")
            return True
        else:
            print("  ❌ Demo mode returned empty result")
            return False
    except Exception as e:
        print(f"  ❌ Error in demo mode: {e}")
        return False

def check_files_exist():
    """Verify all necessary files exist"""
    print("\n🔍 Checking project files...")
    
    required_files = {
        'opensource_llm.py': 'Open-source LLM integration',
        'llm_handler.py': 'LLM handler (open-source)',
        'app.py': 'Flask application',
        'code_reviewer.py': 'Core analysis engine',
        'enhancements.py': 'Enhancement suggestions',
        'templates/index.html': 'Web UI',
        'OLLAMA_SETUP.md': 'Ollama setup guide',
        'OPENSOURCELLLM_MIGRATION.md': 'Migration documentation'
    }
    
    all_exist = True
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print(f"  ✓ {filename}")
        else:
            print(f"  ❌ {filename} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Open-Source LLM Integration Verification")
    print("=" * 60)
    
    os.chdir('/Users/mohamedhijazyshazinhassan/code-reviewer')
    
    checks = [
        ("Imports", check_imports),
        ("LLM Handler", check_llm_handler),
        ("Paid APIs Removed", check_no_paid_apis),
        ("Demo Mode", check_demo_mode),
        ("Project Files", check_files_exist),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ Check '{check_name}' failed with error: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✨ All checks passed! Open-source LLM migration is complete.")
        print("\nNext steps:")
        print("  1. Install Ollama: https://ollama.ai/download")
        print("  2. Start Ollama: ollama serve")
        print("  3. Pull a model: ollama pull mistral")
        print("  4. Start Code Reviewer: python3 app.py")
        print("  5. Open http://127.0.0.1:5002")
        return 0
    else:
        print(f"\n⚠ {total - passed} check(s) failed. Review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
