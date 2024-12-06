from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseModel(ABC):
    """Base class for all models that can be used for preference analysis."""
    
    @abstractmethod
    async def compare_pair(self, option_a: str, option_b: str, num_samples: int = 10) -> Dict[str, int]:
        """
        Compare two options and return counts of preferences.
        
        Args:
            option_a: First option text
            option_b: Second option text
            num_samples: Number of samples to collect
            
        Returns:
            Dict containing counts for each option, e.g., {'A': 7, 'B': 3}
        """
        pass

    @abstractmethod
    async def batch_compare_pairs(self, 
                                pairs: List[tuple[str, str]], 
                                num_samples: int = 10) -> List[Dict[str, int]]:
        """
        Compare multiple pairs of options in batch.
        
        Args:
            pairs: List of (option_a, option_b) tuples
            num_samples: Number of samples per pair
            
        Returns:
            List of preference count dictionaries
        """
        pass