"""Code Reviewer - Professional Code Analysis Tool"""

__version__ = "1.0.0"
__author__ = "Code Reviewer Contributors"
__license__ = "MIT"

from .code_reviewer import CodeReviewer, MultiLanguageAnalyzer, detect_language
from .enhancements import EnhancementSuggestions, EnhancementType
from .llm_handler import MultiLLMHandler, LLMProvider

__all__ = [
    'CodeReviewer',
    'MultiLanguageAnalyzer',
    'detect_language',
    'EnhancementSuggestions',
    'EnhancementType',
    'MultiLLMHandler',
    'LLMProvider',
]
