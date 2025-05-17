"""
Market analyzer that combines multiple analysis methods for comprehensive market insights.
"""
import os
import logging
import asyncio
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .technical_analyzer import TechnicalAnalyzer
from .fundamental_analyzer import FundamentalAnalyzer
from .sentiment_analyzer import SentimentAnalyzer
from .liquidity_analyzer import LiquidityAnalyzer
from .risk_analyzer import RiskAnalyzer

# Configuration
load_dotenv()
logger = logging.getLogger(__name__)

class MarketAnalyzer:
    """Market analysis implementation that combines multiple analysis methods."""
    
    def __init__(self):
        self.analyzers = {
            'technical': TechnicalAnalyzer(),
            'fundamental': FundamentalAnalyzer(),
            'sentiment': SentimentAnalyzer(),
            'liquidity': LiquidityAnalyzer(),
            'risk': RiskAnalyzer()
        }
        
        # Analysis weights
        self.weights = {
            'technical': 0.3,
            'fundamental': 0.2,
            'sentiment': 0.15,
            'liquidity': 0.2,
            'risk': 0.15
        }
        
        # Analysis parameters
        self.lookback_periods = {
            'short': timedelta(hours=24),
            'medium': timedelta(days=7),
            'long': timedelta(days=30)
        }
    
    async def analyze_market(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive market analysis using all analyzers.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Dictionary containing combined analysis results
        """
        try:
            # Run all analyzers concurrently
            analysis_tasks = []
            for analyzer_name, analyzer in self.analyzers.items():
                analysis_tasks.append(self._run_analyzer(analyzer_name, analyzer, data))
                
            results = await asyncio.gather(*analysis_tasks)
            
            # Combine results
            combined_results = self._combine_results(results)
            
            # Generate signals
            signals = self._generate_signals(combined_results)
            
            # Calculate confidence
            confidence = self._calculate_confidence(combined_results)
            
            final_results = {
                'signals': signals,
                'confidence': confidence,
                'analysis': combined_results
            }
            
            logger.info(f"Market analysis completed with confidence: {confidence}")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in market analysis: {str(e)}")
            return {}
    
    async def _run_analyzer(self, name: str, analyzer: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single analyzer and return its results.
        
        Args:
            name: Name of the analyzer
            analyzer: Analyzer instance
            data: Market data
            
        Returns:
            Dictionary containing analyzer results
        """
        try:
            results = await analyzer.analyze(data)
            return {
                'name': name,
                'results': results,
                'weight': self.weights[name]
            }
        except Exception as e:
            logger.error(f"Error in {name} analysis: {str(e)}")
            return {
                'name': name,
                'results': {},
                'weight': self.weights[name]
            }
    
    def _combine_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine results from all analyzers.
        
        Args:
            results: List of analyzer results
            
        Returns:
            Dictionary containing combined results
        """
        combined = {
            'market_regime': self._determine_market_regime(results),
            'trend': self._determine_trend(results),
            'volatility': self._determine_volatility(results),
            'liquidity': self._determine_liquidity(results),
            'risk': self._determine_risk(results),
            'opportunities': self._identify_opportunities(results)
        }
        
        return combined
    
    def _determine_market_regime(self, results: List[Dict[str, Any]]) -> str:
        """Determine the current market regime."""
        regime_scores = {
            'bullish': 0.0,
            'bearish': 0.0,
            'sideways': 0.0
        }
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                if 'overall_signal' in signals:
                    signal = signals['overall_signal']
                    if signal > 0.3:
                        regime_scores['bullish'] += weight
                    elif signal < -0.3:
                        regime_scores['bearish'] += weight
                    else:
                        regime_scores['sideways'] += weight
        
        return max(regime_scores.items(), key=lambda x: x[1])[0]
    
    def _determine_trend(self, results: List[Dict[str, Any]]) -> str:
        """Determine the current market trend."""
        trend_scores = {
            'strong_uptrend': 0.0,
            'uptrend': 0.0,
            'sideways': 0.0,
            'downtrend': 0.0,
            'strong_downtrend': 0.0
        }
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                if 'trend_signal' in signals:
                    signal = signals['trend_signal']
                    if signal > 0.7:
                        trend_scores['strong_uptrend'] += weight
                    elif signal > 0.3:
                        trend_scores['uptrend'] += weight
                    elif signal < -0.7:
                        trend_scores['strong_downtrend'] += weight
                    elif signal < -0.3:
                        trend_scores['downtrend'] += weight
                    else:
                        trend_scores['sideways'] += weight
        
        return max(trend_scores.items(), key=lambda x: x[1])[0]
    
    def _determine_volatility(self, results: List[Dict[str, Any]]) -> str:
        """Determine the current market volatility."""
        volatility_scores = {
            'low': 0.0,
            'moderate': 0.0,
            'high': 0.0,
            'extreme': 0.0
        }
        
        for result in results:
            if 'results' in result and 'metrics' in result['results']:
                metrics = result['results']['metrics']
                weight = result['weight']
                
                if 'volatility' in metrics:
                    vol = metrics['volatility']
                    if vol > 50:
                        volatility_scores['extreme'] += weight
                    elif vol > 30:
                        volatility_scores['high'] += weight
                    elif vol > 15:
                        volatility_scores['moderate'] += weight
                    else:
                        volatility_scores['low'] += weight
        
        return max(volatility_scores.items(), key=lambda x: x[1])[0]
    
    def _determine_liquidity(self, results: List[Dict[str, Any]]) -> str:
        """Determine the current market liquidity."""
        liquidity_scores = {
            'excellent': 0.0,
            'good': 0.0,
            'moderate': 0.0,
            'poor': 0.0
        }
        
        for result in results:
            if 'results' in result and 'liquidity_health' in result['results']:
                health = result['results']['liquidity_health']
                weight = result['weight']
                liquidity_scores[health] += weight
        
        return max(liquidity_scores.items(), key=lambda x: x[1])[0]
    
    def _determine_risk(self, results: List[Dict[str, Any]]) -> str:
        """Determine the current market risk level."""
        risk_scores = {
            'low': 0.0,
            'moderate': 0.0,
            'high': 0.0,
            'extreme': 0.0
        }
        
        for result in results:
            if 'results' in result and 'risk_level' in result['results']:
                level = result['results']['risk_level']
                weight = result['weight']
                risk_scores[level] += weight
        
        return max(risk_scores.items(), key=lambda x: x[1])[0]
    
    def _identify_opportunities(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify trading opportunities based on analysis results."""
        opportunities = []
        
        # Market making opportunities
        if self._is_market_making_viable(results):
            opportunities.append({
                'type': 'market_making',
                'confidence': self._calculate_opportunity_confidence(results, 'market_making'),
                'parameters': self._get_market_making_parameters(results)
            })
            
        # Arbitrage opportunities
        if self._is_arbitrage_viable(results):
            opportunities.append({
                'type': 'arbitrage',
                'confidence': self._calculate_opportunity_confidence(results, 'arbitrage'),
                'parameters': self._get_arbitrage_parameters(results)
            })
            
        # Liquidity provision opportunities
        if self._is_liquidity_provision_viable(results):
            opportunities.append({
                'type': 'liquidity_provision',
                'confidence': self._calculate_opportunity_confidence(results, 'liquidity_provision'),
                'parameters': self._get_liquidity_provision_parameters(results)
            })
            
        return opportunities
    
    def _is_market_making_viable(self, results: List[Dict[str, Any]]) -> bool:
        """Check if market making is viable."""
        viability_score = 0.0
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                if 'spread_signal' in signals and 'liquidity_signal' in signals:
                    spread_score = (signals['spread_signal'] + 1) / 2  # Normalize to 0-1
                    liquidity_score = (signals['liquidity_signal'] + 1) / 2
                    viability_score += (spread_score * 0.6 + liquidity_score * 0.4) * weight
        
        return viability_score > 0.6
    
    def _is_arbitrage_viable(self, results: List[Dict[str, Any]]) -> bool:
        """Check if arbitrage is viable."""
        viability_score = 0.0
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                if 'price_discrepancy' in signals and 'liquidity_signal' in signals:
                    discrepancy_score = (signals['price_discrepancy'] + 1) / 2
                    liquidity_score = (signals['liquidity_signal'] + 1) / 2
                    viability_score += (discrepancy_score * 0.7 + liquidity_score * 0.3) * weight
        
        return viability_score > 0.6
    
    def _is_liquidity_provision_viable(self, results: List[Dict[str, Any]]) -> bool:
        """Check if liquidity provision is viable."""
        viability_score = 0.0
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                if 'liquidity_signal' in signals and 'risk_signal' in signals:
                    liquidity_score = (signals['liquidity_signal'] + 1) / 2
                    risk_score = (1 - signals['risk_signal']) / 2  # Invert risk signal
                    viability_score += (liquidity_score * 0.6 + risk_score * 0.4) * weight
        
        return viability_score > 0.6
    
    def _calculate_opportunity_confidence(self, results: List[Dict[str, Any]], opportunity_type: str) -> float:
        """Calculate confidence score for a trading opportunity."""
        confidence_factors = {
            'market_making': ['spread_signal', 'liquidity_signal', 'volatility_signal'],
            'arbitrage': ['price_discrepancy', 'liquidity_signal', 'execution_signal'],
            'liquidity_provision': ['liquidity_signal', 'risk_signal', 'market_signal']
        }
        
        if opportunity_type not in confidence_factors:
            return 0.0
            
        confidence = 0.0
        total_weight = 0.0
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                for factor in confidence_factors[opportunity_type]:
                    if factor in signals:
                        signal = (signals[factor] + 1) / 2  # Normalize to 0-1
                        confidence += signal * weight
                        total_weight += weight
        
        return confidence / total_weight if total_weight > 0 else 0.0
    
    def _get_market_making_parameters(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get parameters for market making strategy."""
        parameters = {
            'spread_multiplier': 1.0,
            'position_size': 0.0,
            'rebalance_threshold': 0.2
        }
        
        # Calculate spread multiplier based on volatility
        volatility = self._get_average_volatility(results)
        parameters['spread_multiplier'] = 1.0 + (volatility / 100)
        
        # Calculate position size based on liquidity and risk
        liquidity_score = self._get_liquidity_score(results)
        risk_score = self._get_risk_score(results)
        parameters['position_size'] = min(liquidity_score * (1 - risk_score), 1.0)
        
        # Adjust rebalance threshold based on volatility
        parameters['rebalance_threshold'] = 0.2 * (1 + volatility / 100)
        
        return parameters
    
    def _get_arbitrage_parameters(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get parameters for arbitrage strategy."""
        parameters = {
            'min_profit_threshold': 0.002,
            'max_position_size': 0.0,
            'execution_timeout': 30
        }
        
        # Adjust profit threshold based on volatility and liquidity
        volatility = self._get_average_volatility(results)
        liquidity_score = self._get_liquidity_score(results)
        parameters['min_profit_threshold'] = 0.002 * (1 + volatility / 100) * (1 + (1 - liquidity_score))
        
        # Calculate max position size based on liquidity
        parameters['max_position_size'] = liquidity_score
        
        # Adjust execution timeout based on market conditions
        parameters['execution_timeout'] = 30 * (1 + volatility / 100)
        
        return parameters
    
    def _get_liquidity_provision_parameters(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get parameters for liquidity provision strategy."""
        parameters = {
            'liquidity_amount': 0.0,
            'fee_tier': 'medium',
            'rebalance_threshold': 0.3
        }
        
        # Calculate liquidity amount based on market conditions
        liquidity_score = self._get_liquidity_score(results)
        risk_score = self._get_risk_score(results)
        parameters['liquidity_amount'] = liquidity_score * (1 - risk_score)
        
        # Select fee tier based on volatility
        volatility = self._get_average_volatility(results)
        if volatility > 50:
            parameters['fee_tier'] = 'high'
        elif volatility > 30:
            parameters['fee_tier'] = 'medium'
        else:
            parameters['fee_tier'] = 'low'
        
        # Adjust rebalance threshold based on volatility
        parameters['rebalance_threshold'] = 0.3 * (1 + volatility / 100)
        
        return parameters
    
    def _get_average_volatility(self, results: List[Dict[str, Any]]) -> float:
        """Calculate average volatility from all analyzers."""
        volatility_sum = 0.0
        total_weight = 0.0
        
        for result in results:
            if 'results' in result and 'metrics' in result['results']:
                metrics = result['results']['metrics']
                weight = result['weight']
                
                if 'volatility' in metrics:
                    volatility_sum += metrics['volatility'] * weight
                    total_weight += weight
        
        return volatility_sum / total_weight if total_weight > 0 else 0.0
    
    def _get_liquidity_score(self, results: List[Dict[str, Any]]) -> float:
        """Calculate overall liquidity score."""
        liquidity_sum = 0.0
        total_weight = 0.0
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                if 'liquidity_signal' in signals:
                    liquidity_sum += (signals['liquidity_signal'] + 1) / 2 * weight
                    total_weight += weight
        
        return liquidity_sum / total_weight if total_weight > 0 else 0.0
    
    def _get_risk_score(self, results: List[Dict[str, Any]]) -> float:
        """Calculate overall risk score."""
        risk_sum = 0.0
        total_weight = 0.0
        
        for result in results:
            if 'results' in result and 'signals' in result['results']:
                signals = result['results']['signals']
                weight = result['weight']
                
                if 'risk_signal' in signals:
                    risk_sum += (1 - signals['risk_signal']) / 2 * weight  # Invert risk signal
                    total_weight += weight
        
        return risk_sum / total_weight if total_weight > 0 else 0.0
    
    def _generate_signals(self, results: Dict[str, Any]) -> Dict[str, float]:
        """
        Generate trading signals based on combined analysis results.
        
        Args:
            results: Combined analysis results
            
        Returns:
            Dictionary of trading signals
        """
        signals = {
            'entry_signal': 0.0,
            'exit_signal': 0.0,
            'position_size': 0.0,
            'risk_adjustment': 0.0
        }
        
        # Entry signal based on market regime and trend
        if results['market_regime'] == 'bullish':
            signals['entry_signal'] = 1.0
        elif results['market_regime'] == 'bearish':
            signals['entry_signal'] = -1.0
            
        if results['trend'] in ['strong_uptrend', 'uptrend']:
            signals['entry_signal'] = min(signals['entry_signal'] + 0.5, 1.0)
        elif results['trend'] in ['strong_downtrend', 'downtrend']:
            signals['entry_signal'] = max(signals['entry_signal'] - 0.5, -1.0)
            
        # Exit signal based on risk and volatility
        if results['risk'] in ['high', 'extreme']:
            signals['exit_signal'] = -1.0
        elif results['volatility'] in ['high', 'extreme']:
            signals['exit_signal'] = -0.5
            
        # Position size based on liquidity and risk
        if results['liquidity'] in ['excellent', 'good']:
            signals['position_size'] = 1.0
        elif results['liquidity'] == 'moderate':
            signals['position_size'] = 0.5
        else:
            signals['position_size'] = 0.25
            
        if results['risk'] in ['high', 'extreme']:
            signals['position_size'] *= 0.5
            
        # Risk adjustment based on market conditions
        if results['risk'] == 'extreme':
            signals['risk_adjustment'] = -1.0
        elif results['risk'] == 'high':
            signals['risk_adjustment'] = -0.5
        elif results['risk'] == 'low':
            signals['risk_adjustment'] = 0.5
            
        return signals
    
    def _calculate_confidence(self, results: Dict[str, Any]) -> float:
        """
        Calculate overall confidence in the analysis.
        
        Args:
            results: Combined analysis results
            
        Returns:
            Confidence score between 0 and 1
        """
        confidence_factors = {
            'market_regime': 0.3,
            'trend': 0.2,
            'volatility': 0.15,
            'liquidity': 0.2,
            'risk': 0.15
        }
        
        confidence = 0.0
        for factor, weight in confidence_factors.items():
            if factor in results:
                # Convert categorical values to numerical scores
                if factor == 'market_regime':
                    score = 1.0 if results[factor] in ['bullish', 'bearish'] else 0.5
                elif factor == 'trend':
                    score = 1.0 if 'strong' in results[factor] else 0.7
                elif factor == 'volatility':
                    score = 0.5 if results[factor] in ['high', 'extreme'] else 1.0
                elif factor == 'liquidity':
                    score = 1.0 if results[factor] in ['excellent', 'good'] else 0.5
                elif factor == 'risk':
                    score = 0.5 if results[factor] in ['high', 'extreme'] else 1.0
                else:
                    score = 0.5
                    
                confidence += score * weight
                
        return confidence 