"""
Example of well-written code
"""

import logging
from typing import List, Dict, Optional

# Setup logging
logger = logging.getLogger(__name__)

class DataProcessor:
    """Process and transform data efficiently."""
    
    def __init__(self, max_retries: int = 3):
        """Initialize processor with retry configuration."""
        self.max_retries = max_retries
    
    def process_data(self, items: List[Dict]) -> List[Dict]:
        """
        Process a list of data items.
        
        Args:
            items: List of dictionaries to process
            
        Returns:
            List of processed dictionaries
        """
        processed_items = []
        
        for item in items:
            try:
                processed_item = self._transform_item(item)
                processed_items.append(processed_item)
            except ValueError as e:
                logger.error(f"Failed to process item: {e}")
                continue
        
        return processed_items
    
    def _transform_item(self, item: Dict) -> Dict:
        """
        Transform a single item.
        
        Args:
            item: Dictionary to transform
            
        Returns:
            Transformed dictionary
            
        Raises:
            ValueError: If item is invalid
        """
        if not isinstance(item, dict):
            raise ValueError("Item must be a dictionary")
        
        transformed = {
            'id': item.get('id'),
            'name': item.get('name', '').strip(),
            'value': item.get('value', 0)
        }
        
        return transformed
