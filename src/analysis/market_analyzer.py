"""
Market analyzer that combines multiple analysis methods for comprehensive market insights.
"""
import os
import logging
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configuration
load_dotenv()
logger = logging.getLogger(__name__)

class MarketAnalyzer:
    def __init__(self):
        # Analysis weights
        self.weights = {
            'technical': 0.3,
            'fundamental': 0.2,
            'sentiment': 0.15,
            'liquidity': 0.2,
            'risk': 0.15
        }
        
        # Initialize analyzers
        self.analyzers = {
            'technical': TechnicalAnalyzer(),
            'fundamental': FundamentalAnalyzer(),
            'sentiment': SentimentAnalyzer(),
            'liquidity': LiquidityAnalyzer(),
            'risk': RiskAnalyzer()
        }
        
        # Analysis parameters
        self.lookback_periods = {
            'short': timedelta(hours=24),
            'medium': timedelta(days=7),
            'long': timedelta(days=30)
        }
    
    async def analyze_market(self, current_data: Dict[str, Any],
                           historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive market analysis.
        """
        try:
            # Run all analyzers
            analysis_results = await self._run_analyzers(current_data, historical_data)
            
            # Combine results
            combined_analysis = self._combine_analysis(analysis_results)
            
            # Generate signals
            signals = self._generate_signals(combined_analysis)
            
            # Calculate confidence scores
            confidence = self._calculate_confidence(combined_analysis)
            
            return {
                'analysis': combined_analysis,
                'signals': signals,
                'confidence': confidence,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            return {}
    
    async def _run_analyzers(self, current_data: Dict[str, Any],
                            historical_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Run all analyzers concurrently."""
        try:
            # Prepare data for each analyzer
            prepared_data = self._prepare_data(current_data, historical_data)
            
            # Run analyzers
            results = {}
            for name, analyzer in self.analyzers.items():
                results[name] = await analyzer.analyze(prepared_data[name])
            
            return results
            
        except Exception as e:
            logger.error(f"Error running analyzers: {e}")
            return {}
    
    def _prepare_data(self, current_data: Dict[str, Any],
                     historical_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Prepare data for each analyzer."""
        return {
            'technical': self._prepare_technical_data(current_data, historical_data),
            'fundamental': self._prepare_fundamental_data(current_data, historical_data),
            'sentiment': self._prepare_sentiment_data(current_data, historical_data),
            'liquidity': self._prepare_liquidity_data(current_data, historical_data),
            'risk': self._prepare_risk_data(current_data, historical_data)
        }
    
    def _combine_analysis(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Combine results from all analyzers with proper weighting."""
        combined = {
            'market_regime': self._determine_market_regime(analysis_results),
            'trend': self._determine_trend(analysis_results),
            'volatility': self._calculate_combined_volatility(analysis_results),
            'liquidity': self._calculate_combined_liquidity(analysis_results),
            'risk_level': self._calculate_combined_risk(analysis_results),
            'opportunities': self._identify_opportunities(analysis_results)
        }
        
        return combined
    
    def _generate_signals(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading signals based on analysis."""
        signals = {
            'entry': self._generate_entry_signals(analysis),
            'exit': self._generate_exit_signals(analysis),
            'position_size': self._calculate_position_size(analysis),
            'risk_adjustments': self._calculate_risk_adjustments(analysis)
        }
        
        return signals
    
    def _calculate_confidence(self, analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for different aspects of the analysis."""
        return {
            'market_regime': self._calculate_regime_confidence(analysis),
            'trend': self._calculate_trend_confidence(analysis),
            'volatility': self._calculate_volatility_confidence(analysis),
            'liquidity': self._calculate_liquidity_confidence(analysis),
            'risk': self._calculate_risk_confidence(analysis)
        }
    
    def _determine_market_regime(self, analysis_results: Dict[str, Dict[str, Any]]) -> str:
        """Determine current market regime."""
        # Combine signals from different analyzers
        regime_signals = {
            'trending': 0,
            'ranging': 0,
            'volatile': 0,
            'stable': 0
        }
        
        # Weight signals from each analyzer
        for analyzer, results in analysis_results.items():
            weight = self.weights[analyzer]
            if 'regime' in results:
                regime_signals[results['regime']] += weight
        
        # Return dominant regime
        return max(regime_signals.items(), key=lambda x: x[1])[0]
    
    def _determine_trend(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Determine market trend and strength."""
        trend_signals = {
            'direction': 'neutral',
            'strength': 0.0,
            'duration': 'short'
        }
        
        # Combine trend signals
        for analyzer, results in analysis_results.items():
            weight = self.weights[analyzer]
            if 'trend' in results:
                trend_signals['strength'] += results['trend']['strength'] * weight
        
        # Determine direction and duration
        if trend_signals['strength'] > 0.6:
            trend_signals['direction'] = 'bullish'
        elif trend_signals['strength'] < -0.6:
            trend_signals['direction'] = 'bearish'
        
        return trend_signals
    
    def _calculate_combined_volatility(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """Calculate combined volatility metrics."""
        volatility = {
            'current': 0.0,
            'historical': 0.0,
            'forecast': 0.0
        }
        
        # Combine volatility signals
        for analyzer, results in analysis_results.items():
            weight = self.weights[analyzer]
            if 'volatility' in results:
                for key in volatility:
                    if key in results['volatility']:
                        volatility[key] += results['volatility'][key] * weight
        
        return volatility
    
    def _calculate_combined_liquidity(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """Calculate combined liquidity metrics."""
        liquidity = {
            'score': 0.0,
            'depth': 0.0,
            'resilience': 0.0
        }
        
        # Combine liquidity signals
        for analyzer, results in analysis_results.items():
            weight = self.weights[analyzer]
            if 'liquidity' in results:
                for key in liquidity:
                    if key in results['liquidity']:
                        liquidity[key] += results['liquidity'][key] * weight
        
        return liquidity
    
    def _calculate_combined_risk(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """Calculate combined risk metrics."""
        risk = {
            'level': 0.0,
            'exposure': 0.0,
            'limits': {}
        }
        
        # Combine risk signals
        for analyzer, results in analysis_results.items():
            weight = self.weights[analyzer]
            if 'risk' in results:
                for key in risk:
                    if key in results['risk']:
                        if isinstance(results['risk'][key], dict):
                            risk[key].update(results['risk'][key])
                        else:
                            risk[key] += results['risk'][key] * weight
        
        return risk
    
    def _identify_opportunities(self, analysis_results: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify trading opportunities based on analysis."""
        opportunities = []
        
        # Combine opportunity signals
        for analyzer, results in analysis_results.items():
            weight = self.weights[analyzer]
            if 'opportunities' in results:
                for opp in results['opportunities']:
                    opp['confidence'] *= weight
                    opportunities.append(opp)
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x['confidence'], reverse=True)
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def _generate_entry_signals(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate entry signals based on analysis."""
        signals = []
        
        # Generate signals based on market regime
        if analysis['market_regime'] == 'trending':
            signals.extend(self._generate_trend_following_signals(analysis))
        elif analysis['market_regime'] == 'ranging':
            signals.extend(self._generate_range_trading_signals(analysis))
        
        # Add risk management
        signals = self._add_risk_management(signals, analysis)
        
        return signals
    
    def _generate_exit_signals(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate exit signals based on analysis."""
        signals = []
        
        # Generate signals based on market conditions
        if analysis['risk_level'] > 0.7:
            signals.extend(self._generate_risk_reduction_signals(analysis))
        elif analysis['trend']['direction'] == 'neutral':
            signals.extend(self._generate_profit_taking_signals(analysis))
        
        return signals
    
    def _calculate_position_size(self, analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate recommended position sizes based on analysis."""
        base_size = 1.0  # Base position size
        
        # Adjust for market conditions
        size_adjustments = {
            'volatility': 1.0 - (analysis['volatility']['current'] * 0.5),
            'liquidity': analysis['liquidity']['score'],
            'risk': 1.0 - (analysis['risk_level'] * 0.5),
            'confidence': self._calculate_overall_confidence(analysis)
        }
        
        # Calculate final size
        final_size = base_size
        for adjustment in size_adjustments.values():
            final_size *= adjustment
        
        return {
            'base': base_size,
            'adjusted': final_size,
            'adjustments': size_adjustments
        }
    
    def _calculate_risk_adjustments(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk management adjustments."""
        return {
            'stop_loss': self._calculate_stop_loss(analysis),
            'take_profit': self._calculate_take_profit(analysis),
            'position_limits': self._calculate_position_limits(analysis),
            'leverage': self._calculate_leverage(analysis)
        }
    
    def _calculate_overall_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence in the analysis."""
        confidence_scores = analysis.get('confidence', {})
        if not confidence_scores:
            return 0.5  # Default to medium confidence
        
        # Weight different aspects
        weights = {
            'market_regime': 0.3,
            'trend': 0.2,
            'volatility': 0.2,
            'liquidity': 0.15,
            'risk': 0.15
        }
        
        # Calculate weighted average
        total_confidence = 0.0
        total_weight = 0.0
        
        for aspect, weight in weights.items():
            if aspect in confidence_scores:
                total_confidence += confidence_scores[aspect] * weight
                total_weight += weight
        
        return total_confidence / total_weight if total_weight > 0 else 0.5 