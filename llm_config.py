"""
LLM Configuration Helper
Manages API keys and provider setup for multi-LLM integration
"""

import os
from typing import Dict, Optional
import json

class LLMConfig:
    """Configuration management for LLM providers"""
    
    # Default configuration file location
    CONFIG_FILE = os.path.expanduser("~/.code-reviewer/llm_config.json")
    
    @staticmethod
    def get_api_key(provider: str) -> Optional[str]:
        """Get API key for a specific provider"""
        env_keys = {
            'claude': 'ANTHROPIC_API_KEY',
            'openai': 'OPENAI_API_KEY',
            'google': 'GOOGLE_API_KEY',
        }
        
        env_key = env_keys.get(provider.lower())
        if env_key:
            return os.getenv(env_key)
        
        # Check config file
        try:
            if os.path.exists(LLMConfig.CONFIG_FILE):
                with open(LLMConfig.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get(provider, {}).get('api_key')
        except (json.JSONDecodeError, IOError):
            pass
        
        return None
    
    @staticmethod
    def save_api_key(provider: str, api_key: str) -> bool:
        """Save API key for a provider"""
        try:
            config_dir = os.path.dirname(LLMConfig.CONFIG_FILE)
            os.makedirs(config_dir, exist_ok=True)
            
            config = {}
            if os.path.exists(LLMConfig.CONFIG_FILE):
                try:
                    with open(LLMConfig.CONFIG_FILE, 'r') as f:
                        config = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass
            
            if provider not in config:
                config[provider] = {}
            
            config[provider]['api_key'] = api_key
            
            with open(LLMConfig.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Failed to save API key: {str(e)}")
            return False
    
    @staticmethod
    def get_available_providers() -> Dict[str, bool]:
        """Get list of available providers with their status"""
        providers = {}
        
        # Check each provider
        for provider in ['claude', 'openai', 'google']:
            api_key = LLMConfig.get_api_key(provider)
            providers[provider] = api_key is not None
        
        return providers
    
    @staticmethod
    def get_setup_instructions() -> str:
        """Get setup instructions for users"""
        return """
🚀 LLM Integration Setup Instructions

To enable LLM code refinement features, you need at least one API key:

1. CLAUDE (Recommended):
   - Visit: https://console.anthropic.com/
   - Create API key
   - Set: export ANTHROPIC_API_KEY='your-key'

2. OPENAI (GPT-4):
   - Visit: https://platform.openai.com/api-keys
   - Create API key
   - Set: export OPENAI_API_KEY='your-key'

3. GOOGLE GEMINI:
   - Visit: https://makersuite.google.com/app/apikey
   - Create API key
   - Set: export GOOGLE_API_KEY='your-key'

Alternative (Persistent Storage):
- API keys are automatically saved to ~/.code-reviewer/llm_config.json
- They persist across sessions

After setting up, the application will automatically:
✓ Detect available providers
✓ Use the best available LLM
✓ Implement automatic fallback if one provider fails
✓ Support multi-agent code review orchestration via MCP

To test your setup:
1. Start the application
2. Check the "LLM Refine" tab for provider status
3. Paste code and click "Refine Code with LLM"
"""

if __name__ == '__main__':
    # Print setup instructions
    print(LLMConfig.get_setup_instructions())
    
    # Show available providers
    print("\n📊 Current Provider Status:")
    providers = LLMConfig.get_available_providers()
    for provider, available in providers.items():
        status = "✓ Available" if available else "✗ Not configured"
        print(f"  {provider.upper()}: {status}")
