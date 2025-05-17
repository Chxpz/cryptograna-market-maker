"""
Base analyzer class that defines the interface for all market analyzers.
"""
import logging
from typing import Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseAnalyzer(ABC):
    """Base class for all market analyzers."""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.confidence = 0.0
    
    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market data and return results.
        
        Args:
            data: Dictionary containing market data to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        pass
    
    def _calculate_confidence(self, factors: Dict[str, float]) -> float:
        """
        Calculate confidence score based on analysis factors.
        
        Args:
            factors: Dictionary of factors and their weights
            
        Returns:
            Confidence score between 0 and 1
        """
        if not factors:
            return 0.0
            
        total_weight = sum(factors.values())
        if total_weight == 0:
            return 0.0
            
        weighted_sum = sum(score * weight for score, weight in factors.items())
        return weighted_sum / total_weight
    
    def _validate_data(self, data: Dict[str, Any], required_fields: list) -> bool:
        """
        Validate that required fields are present in the data.
        
        Args:
            data: Dictionary containing market data
            required_fields: List of required field names
            
        Returns:
            True if all required fields are present, False otherwise
        """
        return all(field in data for field in required_fields)
    
    def _log_analysis(self, results: Dict[str, Any]):
        """Log analysis results."""
        logger.info(f"{self.name} analysis results: {results}") 