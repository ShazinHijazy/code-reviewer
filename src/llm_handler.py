"""
Open-Source LLM Handler
Support for local models via Ollama (LLaMA 2, Mistral, CodeLLaMA)
No API keys required - all models run locally
"""

import os
import json
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List, Any
from opensource_llm import OpenSourceLLMSelector, OpenSourceLLMHandler

class LLMProvider(Enum):
    """Available LLM providers - All open-source and local"""
    OLLAMA = "ollama"
    DEMO = "demo"
    NONE = "none"

@dataclass
class LLMConfig:
    """Configuration for LLM provider"""
    provider: LLMProvider
    model: str = "mistral"
    temperature: float = 0.3
    max_tokens: int = 2000

class MultiLLMHandler:
    """Handles open-source LLM requests via Ollama (no API keys required)"""
    
    def __init__(self):
        """Initialize open-source LLM handler"""
        self.selector = OpenSourceLLMSelector()
        self.handler = self.selector.get_handler()
        self.active_provider = "ollama" if self.handler else "none"
        self.demo_mode = not self.handler
        
        if self.handler:
            print(f"✓ Open-Source LLM Handler initialized")
            print(f"  Provider: {self.handler.provider}")
            print(f"  Model: {self.handler.model}")
            print(f"  Available models: {', '.join(self.handler.models_available) if self.handler.models_available else 'None'}")
        else:
            print("⚠ No open-source LLM provider available")
            print("  Use demo mode or install Ollama: https://ollama.ai")
    
    def refine_code(self, code: str, language: str, issues: List[Dict],
                   enhancement: Optional[Dict] = None, provider: Optional[str] = None) -> str:
        """
        Refine code using local open-source LLM
        
        Args:
            code: Original code to refine
            language: Programming language
            issues: List of detected issues
            enhancement: Specific enhancement to apply
            provider: Preferred provider (uses Ollama if available)
        
        Returns:
            Refined/fixed code
        """
        # Try Ollama first if available
        if self.handler:
            try:
                return self.handler.refine_code(code, language, issues)
            except Exception as e:
                print(f"Ollama error: {str(e)}")
                return self.refine_code_demo(code, language, issues)
        
        # Fallback to demo mode
        return self.refine_code_demo(code, language, issues)
    
    def refine_code_demo(self, code: str, language: str, issues: list = None) -> str:
        """Demo mode refinement using pattern-based improvements (no LLM required)"""
        if issues is None:
            issues = []
        
        refined = code
        
        # Pattern-based refinements
        if language.lower() == 'python':
            # Fix string concatenation in loops
            if 'result = result +' in refined or 'result+=' in refined:
                refined = refined.replace(
                    'for i in range(len(items)):\n    result = result + items[i]',
                    'result = \'\'.join(items)'
                )
            
            # Fix nested loops
            if refined.count('for ') >= 2:
                refined = refined.replace(
                    'for i in range(len(',
                    'for item in '
                )
            
            # Add type hints
            if 'def ' in refined and '->' not in refined:
                lines = refined.split('\n')
                new_lines = []
                for line in lines:
                    if line.strip().startswith('def '):
                        if '(' in line and ')' not in line.split('(')[1]:
                            new_lines.append(line.rstrip(':') + ' -> Any:')
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                refined = '\n'.join(new_lines)
        
        elif language.lower() == 'javascript':
            # Fix var to const/let
            refined = refined.replace('var ', 'const ')
            # Fix string concatenation
            refined = refined.replace("result = result + ", "result += ")
        
        return refined
    
    def get_available_providers(self) -> Dict[str, bool]:
        """Get list of available providers"""
        providers = {}
        all_providers = self.selector.get_all_providers()
        
        for name in all_providers:
            providers[name] = True
        
        providers['demo'] = True  # Demo mode always available
        return providers
    
    def get_active_provider_name(self) -> str:
        """Get name of currently active provider"""
        return self.active_provider
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get detailed status of all providers"""
        status = {
            "active_provider": self.active_provider,
            "demo_mode_enabled": True,
            "providers": {}
        }
        
        # Add Ollama status
        if self.handler:
            status["providers"]["ollama"] = {
                "available": True,
                "model": self.handler.model,
                "models_available": self.handler.models_available
            }
        else:
            status["providers"]["ollama"] = {
                "available": False,
                "error": "Ollama not running. Install from: https://ollama.ai"
            }
        
        # Demo always available
        status["providers"]["demo"] = {
            "available": True,
            "description": "Pattern-based refinement (no LLM required)"
        }
        
        return status
    
    def generate_code_suggestions(self, code: str, language: str, 
                                 issue_types: List[str] = None) -> List[Dict]:
        """
        Generate code improvement suggestions using local LLM
        
        Args:
            code: Code to analyze
            language: Programming language
            issue_types: Types of issues to focus on
        
        Returns:
            List of suggestion dictionaries
        """
        if self.handler:
            try:
                return self.handler.generate_suggestions(code, language)
            except Exception as e:
                print(f"Error generating suggestions: {str(e)}")
                return []
        
        # Return empty list if no LLM available
        return []
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions for local LLM"""
        if self.handler:
            return f"✓ {self.handler.provider.upper()} is ready!"
        
        # Return setup instructions
        return """
🚀 Quick Setup - Open-Source LLM (No API Keys Required!)

1. Install Ollama (Recommended - Easiest):
   https://ollama.ai/download
   
   Or on macOS:
   brew install ollama

2. Start Ollama (in a new terminal):
   ollama serve

3. Pull a model (in another terminal):
   ollama pull mistral        # Fast & good for code (7B)
   ollama pull codellama      # Optimized for code
   ollama pull llama2         # More capable (70B - needs GPU)

4. Code Reviewer will auto-detect and use it!

Available Open-Source Models:
- Mistral 7B (fastest, recommended)
- CodeLLaMA (best for code)
- LLaMA 2 (most capable)
- Orca Mini (lightweight, 3B)
- Neural Chat (conversational)
- Phi (Microsoft lightweight)

All models run locally, no internet required after download!
"""
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of LLM handler"""
        if self.handler:
            return {
                "status": "healthy",
                "provider": self.active_provider,
                "model": self.handler.model,
                "available": self.handler.is_available()
            }
        else:
            return {
                "status": "degraded",
                "provider": "none",
                "warning": "Using demo mode - install Ollama for better results",
                "setup_url": "https://ollama.ai"
            }
