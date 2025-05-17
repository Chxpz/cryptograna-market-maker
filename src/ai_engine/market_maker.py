"""
Market maker AI that analyzes market data and generates trading recommendations.
"""
import os
import logging
from typing import Dict, Any, List
from datetime import datetime

from ..analysis.market_analyzer import MarketAnalyzer

logger = logging.getLogger(__name__)

class MarketMakerAI:
    """AI-powered market maker that generates trading recommendations."""
    
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.analyzer = MarketAnalyzer()
        
        # Strategy parameters
        self.min_spread = float(os.getenv("MARKET_MAKING_MIN_SPREAD", "0.001"))
        self.max_position = float(os.getenv("MARKET_MAKING_MAX_POSITION", "100"))
        self.rebalance_threshold = float(os.getenv("MARKET_MAKING_REBALANCE_THRESHOLD", "0.2"))
        
        # Risk parameters
        self.max_drawdown = float(os.getenv("MAX_DRAWDOWN", "0.1"))
        self.max_leverage = float(os.getenv("MAX_LEVERAGE", "1.0"))
        self.min_liquidity = float(os.getenv("MIN_LIQUIDITY", "10000"))
        
    async def get_recommendations(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trading recommendations based on market data.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            Dictionary containing trading recommendations
        """
        try:
            # Analyze market conditions
            analysis = await self.analyzer.analyze_market(market_data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(analysis, market_data)
            
            # Apply risk management
            recommendations = self._apply_risk_management(recommendations, analysis)
            
            logger.info(f"Generated recommendations: {recommendations}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_safe_recommendations()
    
    def _generate_recommendations(self, analysis: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading recommendations based on analysis."""
        recommendations = {
            "timestamp": datetime.utcnow().isoformat(),
            "strategy": "market_making",
            "action": "none",
            "parameters": {
                "spread": self.min_spread,
                "position_size": 0.0,
                "rebalance": False
            },
            "confidence": analysis.get("confidence", 0.0)
        }
        
        # Get market signals
        signals = analysis.get("signals", {})
        
        # Determine action based on signals
        if signals.get("entry_signal", 0) > 0.5:
            recommendations["action"] = "enter"
        elif signals.get("exit_signal", 0) < -0.5:
            recommendations["action"] = "exit"
            
        # Adjust parameters based on market conditions
        if recommendations["action"] != "none":
            # Adjust spread based on volatility
            volatility = analysis.get("volatility", "low")
            if volatility == "high":
                recommendations["parameters"]["spread"] *= 1.5
            elif volatility == "extreme":
                recommendations["parameters"]["spread"] *= 2.0
                
            # Adjust position size based on liquidity and risk
            position_size = signals.get("position_size", 0.0)
            recommendations["parameters"]["position_size"] = min(
                position_size * self.max_position,
                self.max_position
            )
            
            # Check if rebalancing is needed
            if abs(signals.get("risk_adjustment", 0)) > self.rebalance_threshold:
                recommendations["parameters"]["rebalance"] = True
                
        return recommendations
    
    def _apply_risk_management(self, recommendations: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply risk management rules to recommendations."""
        # Check market risk
        if analysis.get("risk", "low") in ["high", "extreme"]:
            recommendations["parameters"]["position_size"] *= 0.5
            
        # Check liquidity
        if analysis.get("liquidity", "poor") in ["poor", "moderate"]:
            recommendations["parameters"]["position_size"] *= 0.5
            
        # Check drawdown
        if analysis.get("metrics", {}).get("drawdown", 0) > self.max_drawdown:
            recommendations["action"] = "exit"
            recommendations["parameters"]["position_size"] = 0.0
            
        return recommendations
    
    def _get_safe_recommendations(self) -> Dict[str, Any]:
        """Get safe recommendations when analysis fails."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "strategy": "market_making",
            "action": "none",
            "parameters": {
                "spread": self.min_spread,
                "position_size": 0.0,
                "rebalance": False
            },
            "confidence": 0.0
        } 