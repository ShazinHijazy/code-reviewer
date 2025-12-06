"""
Open-Source LLM Handler
Support for local models via Ollama: LLaMA 2, Mistral, CodeLLaMA, Phi
No API keys required - all models run locally
"""

import requests
import json
import subprocess
import time
from typing import Optional, Dict, List, Any
from enum import Enum

class OpenSourceLLMProvider(Enum):
    """Open-source LLM providers"""
    OLLAMA = "ollama"  # Local inference engine
    LOCAL_LLAMACPP = "llamacpp"  # llama.cpp local
    HUGGINGFACE_PIPELINE = "huggingface"  # Hugging Face local pipeline

class OllamaModel(Enum):
    """Available Ollama models"""
    LLAMA2 = "llama2"  # 7B, 13B, 70B
    MISTRAL = "mistral"  # 7B (faster)
    CODELLAMA = "codellama"  # Optimized for code
    NEURAL_CHAT = "neural-chat"  # Conversational
    ORCA_MINI = "orca-mini"  # Lightweight (3B)
    PHI = "phi"  # Microsoft lightweight

class OpenSourceLLMHandler:
    """Handles local open-source LLM inference without API keys"""
    
    def __init__(self, provider: str = "ollama", model: str = "mistral"):
        """
        Initialize open-source LLM handler
        
        Args:
            provider: "ollama", "llamacpp", or "huggingface"
            model: Model name (e.g., "mistral", "llama2", "codellama")
        """
        self.provider = provider
        self.model = model
        self.available = False
        self.error_message = ""
        self.models_available = []
        
        # Check which provider is available
        if provider == "ollama":
            self._check_ollama()
        elif provider == "llamacpp":
            self._check_llamacpp()
        else:
            self._check_huggingface()
    
    def _check_ollama(self):
        """Check if Ollama is installed and running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                self.models_available = [m.get('name', '').split(':')[0] for m in data.get('models', [])]
                self.available = len(self.models_available) > 0
                if not self.available:
                    self.error_message = "Ollama is running but no models installed. Run: ollama pull mistral"
            else:
                self.error_message = "Ollama server not responding"
        except requests.ConnectionError:
            self.error_message = "Ollama not running. Install from: https://ollama.ai and run: ollama serve"
        except Exception as e:
            self.error_message = f"Error checking Ollama: {str(e)}"
    
    def _check_llamacpp(self):
        """Check if llama.cpp is available"""
        try:
            # Try to find llama.cpp executable
            result = subprocess.run(["which", "llama-cli"], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                self.available = True
                self.models_available = ["local_gguf"]
            else:
                self.error_message = "llama.cpp not found. Install from: https://github.com/ggerganov/llama.cpp"
        except Exception as e:
            self.error_message = f"Error checking llama.cpp: {str(e)}"
    
    def _check_huggingface(self):
        """Check if Hugging Face transformers is available"""
        try:
            import transformers
            self.available = True
            self.models_available = ["huggingface_local"]
        except ImportError:
            self.error_message = "Transformers not installed. Run: pip install transformers torch"
        except Exception as e:
            self.error_message = f"Error checking Hugging Face: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if provider is available and ready"""
        return self.available
    
    def get_status(self) -> Dict[str, Any]:
        """Get provider status"""
        return {
            "provider": self.provider,
            "available": self.available,
            "model": self.model,
            "models_available": self.models_available,
            "error": self.error_message if not self.available else None
        }
    
    def refine_code(self, code: str, language: str, issues: List[Dict] = None) -> str:
        """
        Refine code using local open-source LLM
        
        Args:
            code: Code to refine
            language: Programming language
            issues: List of detected issues
        
        Returns:
            Refined code
        """
        if not self.available:
            return code  # Fall back to original if not available
        
        if self.provider == "ollama":
            return self._refine_with_ollama(code, language, issues)
        elif self.provider == "llamacpp":
            return self._refine_with_llamacpp(code, language, issues)
        else:
            return self._refine_with_huggingface(code, language, issues)
    
    def _refine_with_ollama(self, code: str, language: str, issues: List[Dict] = None) -> str:
        """Refine code using Ollama local LLM"""
        try:
            issue_list = ""
            if issues:
                issue_list = "\n\nIssues to fix:\n"
                for issue in issues[:3]:  # Limit to first 3 issues
                    issue_list += f"- {issue.get('message', '')}\n"
            
            prompt = f"""You are an expert code reviewer. Fix and improve this {language} code. 
Keep the response CONCISE and return ONLY the improved code without explanations.

{issue_list}

Code:
```{language}
{code}
```

Improved Code:"""

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,
                    "top_p": 0.9,
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                refined = result.get("response", code).strip()
                
                # Clean up the response
                if "```" in refined:
                    parts = refined.split("```")
                    if len(parts) >= 2:
                        refined = parts[1]
                        if refined.startswith(language):
                            refined = refined[len(language):].lstrip("\n")
                        if "```" in refined:
                            refined = refined.split("```")[0]
                
                return refined.strip() if refined else code
            else:
                return code
        
        except requests.ConnectionError:
            return code
        except Exception as e:
            print(f"Error refining with Ollama: {str(e)}")
            return code
    
    def _refine_with_llamacpp(self, code: str, language: str, issues: List[Dict] = None) -> str:
        """Refine code using llama.cpp local model"""
        # This would require a local GGUF model file
        # For now, return code (user needs to provide model path)
        return code
    
    def _refine_with_huggingface(self, code: str, language: str, issues: List[Dict] = None) -> str:
        """Refine code using Hugging Face local transformers"""
        try:
            from transformers import pipeline
            
            # Use a code-specialized model
            try:
                generator = pipeline(
                    "text-generation",
                    model="Salesforce/codegen-350M-mono",
                    device=0  # GPU if available
                )
            except:
                # Fallback to smaller model
                generator = pipeline(
                    "text-generation",
                    model="gpt2"
                )
            
            prompt = f"Fix and improve this {language} code:\n```{language}\n{code}\n```\nImproved:"
            
            result = generator(prompt, max_length=500, num_return_sequences=1)
            refined = result[0]['generated_text'] if result else code
            
            return refined if refined else code
        
        except Exception as e:
            print(f"Error refining with Hugging Face: {str(e)}")
            return code
    
    def generate_suggestions(self, code: str, language: str) -> List[Dict]:
        """Generate code improvement suggestions using local LLM"""
        if not self.available:
            return []
        
        try:
            prompt = f"""Analyze this {language} code and suggest 3 improvements:

```{language}
{code}
```

Format each suggestion as:
1. [Type]: [Description]
   Current: [show current code pattern]
   Improved: [show improved pattern]"""

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.5,
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                # Parse suggestions (simplified)
                suggestions = []
                for line in text.split('\n'):
                    if line.strip().startswith(('1.', '2.', '3.')):
                        suggestions.append({
                            'type': 'improvement',
                            'description': line.strip()
                        })
                return suggestions
            return []
        
        except Exception as e:
            print(f"Error generating suggestions: {str(e)}")
            return []
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions for this provider"""
        if self.provider == "ollama":
            return """
🚀 Ollama Setup (Recommended - Easiest)

1. Install Ollama:
   - macOS: https://ollama.ai/download/Ollama-darwin.zip
   - Linux: curl https://ollama.ai/install.sh | sh
   - Windows: https://ollama.ai/download/OllamaSetup.exe

2. Start Ollama:
   ollama serve

3. Pull a model (in another terminal):
   # Fast & good for code
   ollama pull mistral
   
   # Optimized for code  
   ollama pull codellama
   
   # Lightweight
   ollama pull orca-mini

4. Code Reviewer will auto-detect and use it!

Available models: LLaMA 2, Mistral, CodeLLaMA, Neural Chat, Phi
"""
        
        elif self.provider == "llamacpp":
            return """
🚀 llama.cpp Setup (Advanced - Fastest)

1. Build llama.cpp:
   git clone https://github.com/ggerganov/llama.cpp
   cd llama.cpp
   make

2. Download a GGUF model:
   wget https://huggingface.co/...model.gguf

3. Set environment variable:
   export LLAMA_CPP_MODEL=/path/to/model.gguf

4. Code Reviewer will use it!
"""
        
        else:
            return """
🚀 Hugging Face Local Setup (Requires GPU for speed)

1. Install Transformers:
   pip install transformers torch

2. Models will auto-download on first use
   (Requires internet for first download only)

3. Code Reviewer will use downloaded model!

Available models: CodeGen, GPT-2, DistilBERT
"""


class OpenSourceLLMSelector:
    """Select best available open-source LLM provider"""
    
    def __init__(self):
        """Initialize and check all providers"""
        self.handlers = {}
        self.best_provider = None
        
        # Try to initialize each provider in priority order
        providers = [
            ("ollama", "mistral"),      # Best balance
            ("llamacpp", "local"),      # Fastest but complex
            ("huggingface", "codegen"), # Requires download
        ]
        
        for provider, model in providers:
            try:
                handler = OpenSourceLLMHandler(provider, model)
                if handler.is_available():
                    self.handlers[provider] = handler
                    if not self.best_provider:
                        self.best_provider = provider
            except:
                pass
    
    def get_best_provider(self) -> Optional[str]:
        """Get best available provider"""
        return self.best_provider
    
    def get_handler(self, provider: str = None) -> Optional[OpenSourceLLMHandler]:
        """Get handler for specific provider or best available"""
        if provider and provider in self.handlers:
            return self.handlers[provider]
        if self.best_provider:
            return self.handlers.get(self.best_provider)
        return None
    
    def get_all_providers(self) -> Dict[str, Dict]:
        """Get status of all providers"""
        return {name: handler.get_status() for name, handler in self.handlers.items()}
    
    def refine_code(self, code: str, language: str, issues: List = None) -> Dict[str, Any]:
        """Refine code using best available provider"""
        handler = self.get_handler()
        if not handler:
            return {"status": "no_provider", "code": code}
        
        refined = handler.refine_code(code, language, issues)
        return {
            "status": "success",
            "code": refined,
            "provider": handler.provider,
            "model": handler.model
        }
