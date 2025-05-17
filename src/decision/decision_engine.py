"""
Decision engine that combines analysis results to make trading decisions.
"""
import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Configuration
load_dotenv()
logger = logging.getLogger(__name__)

class DecisionEngine:
    def __init__(self):
        # Strategy weights
        self.strategy_weights = {
            'market_making': 0.4,
            'arbitrage': 0.3,
            'liquidity_provision': 0.3
        }
        
        # Initialize strategies
        self.strategies = {
            'market_making': MarketMakingStrategy(),
            'arbitrage': ArbitrageStrategy(),
            'liquidity_provision': LiquidityStrategy()
        }
        
        # Risk parameters
        self.risk_limits = {
            'max_position_size': float(os.getenv("MAX_POSITION_SIZE", "100")),
            'max_drawdown': float(os.getenv("MAX_DRAWDOWN", "0.1")),
            'max_leverage': float(os.getenv("MAX_LEVERAGE", "1.0")),
            'min_liquidity': float(os.getenv("MIN_LIQUIDITY", "10000"))
        }
        
        # Performance tracking
        self.performance_metrics = {
            'total_pnl': 0.0,
            'win_rate': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0
        }
    
    async def make_decision(self, analysis: Dict[str, Any],
                          current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make trading decisions based on analysis and current state.
        """
        try:
            # Evaluate strategies
            strategy_scores = await self._evaluate_strategies(analysis, current_state)
            
            # Select best strategy
            best_strategy = self._select_strategy(strategy_scores)
            
            # Generate actions
            actions = await best_strategy.generate_actions(analysis, current_state)
            
            # Apply risk management
            actions = self._apply_risk_management(actions, current_state)
            
            # Update performance metrics
            self._update_performance_metrics(actions)
            
            return {
                'strategy': best_strategy.name,
                'actions': actions,
                'confidence': strategy_scores[best_strategy.name]['confidence'],
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in decision making: {e}")
            return {}
    
    async def _evaluate_strategies(self, analysis: Dict[str, Any],
                                 current_state: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Evaluate all strategies and return scores."""
        scores = {}
        
        for name, strategy in self.strategies.items():
            # Get strategy evaluation
            evaluation = await strategy.evaluate(analysis, current_state)
            
            # Calculate confidence
            confidence = self._calculate_strategy_confidence(evaluation)
            
            # Apply weight
            weighted_score = evaluation['score'] * self.strategy_weights[name]
            
            scores[name] = {
                'score': weighted_score,
                'confidence': confidence,
                'evaluation': evaluation
            }
        
        return scores
    
    def _select_strategy(self, strategy_scores: Dict[str, Dict[str, float]]) -> Any:
        """Select the best strategy based on scores and confidence."""
        best_strategy = None
        best_score = float('-inf')
        
        for name, scores in strategy_scores.items():
            # Combine score and confidence
            combined_score = scores['score'] * scores['confidence']
            
            if combined_score > best_score:
                best_score = combined_score
                best_strategy = self.strategies[name]
        
        return best_strategy
    
    def _apply_risk_management(self, actions: List[Dict[str, Any]],
                             current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply risk management to actions."""
        managed_actions = []
        
        for action in actions:
            # Check position limits
            if not self._check_position_limits(action, current_state):
                continue
            
            # Check drawdown limits
            if not self._check_drawdown_limits(action, current_state):
                continue
            
            # Check leverage limits
            if not self._check_leverage_limits(action, current_state):
                continue
            
            # Check liquidity requirements
            if not self._check_liquidity_requirements(action, current_state):
                continue
            
            # Add risk management parameters
            action['risk_management'] = self._generate_risk_parameters(action, current_state)
            
            managed_actions.append(action)
        
        return managed_actions
    
    def _update_performance_metrics(self, actions: List[Dict[str, Any]]):
        """Update performance metrics based on actions."""
        for action in actions:
            if 'pnl' in action:
                self.performance_metrics['total_pnl'] += action['pnl']
            
            if 'win' in action:
                self.performance_metrics['win_rate'] = (
                    self.performance_metrics['win_rate'] * 0.9 +  # Decay
                    (1.0 if action['win'] else 0.0) * 0.1  # New result
                )
            
            if 'drawdown' in action:
                self.performance_metrics['max_drawdown'] = max(
                    self.performance_metrics['max_drawdown'],
                    action['drawdown']
                )
    
    def _calculate_strategy_confidence(self, evaluation: Dict[str, Any]) -> float:
        """Calculate confidence in strategy evaluation."""
        confidence_factors = {
            'market_regime': 0.3,
            'trend': 0.2,
            'volatility': 0.2,
            'liquidity': 0.15,
            'risk': 0.15
        }
        
        total_confidence = 0.0
        total_weight = 0.0
        
        for factor, weight in confidence_factors.items():
            if factor in evaluation:
                total_confidence += evaluation[factor] * weight
                total_weight += weight
        
        return total_confidence / total_weight if total_weight > 0 else 0.5
    
    def _check_position_limits(self, action: Dict[str, Any],
                             current_state: Dict[str, Any]) -> bool:
        """Check if action respects position limits."""
        if 'position_size' not in action:
            return True
        
        current_position = current_state.get('position_size', 0)
        new_position = current_position + action['position_size']
        
        return abs(new_position) <= self.risk_limits['max_position_size']
    
    def _check_drawdown_limits(self, action: Dict[str, Any],
                             current_state: Dict[str, Any]) -> bool:
        """Check if action respects drawdown limits."""
        if 'drawdown' not in action:
            return True
        
        return action['drawdown'] <= self.risk_limits['max_drawdown']
    
    def _check_leverage_limits(self, action: Dict[str, Any],
                             current_state: Dict[str, Any]) -> bool:
        """Check if action respects leverage limits."""
        if 'leverage' not in action:
            return True
        
        return action['leverage'] <= self.risk_limits['max_leverage']
    
    def _check_liquidity_requirements(self, action: Dict[str, Any],
                                    current_state: Dict[str, Any]) -> bool:
        """Check if action meets liquidity requirements."""
        if 'liquidity' not in current_state:
            return True
        
        return current_state['liquidity'] >= self.risk_limits['min_liquidity']
    
    def _generate_risk_parameters(self, action: Dict[str, Any],
                                current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk management parameters for action."""
        return {
            'stop_loss': self._calculate_stop_loss(action, current_state),
            'take_profit': self._calculate_take_profit(action, current_state),
            'position_limit': self._calculate_position_limit(action, current_state),
            'leverage_limit': self._calculate_leverage_limit(action, current_state)
        }
    
    def _calculate_stop_loss(self, action: Dict[str, Any],
                           current_state: Dict[str, Any]) -> float:
        """Calculate stop loss level for action."""
        base_price = action.get('price', current_state.get('current_price', 0))
        volatility = current_state.get('volatility', 0)
        
        # Adjust stop loss based on volatility
        stop_loss_pct = 0.02 + (volatility * 0.5)  # Base 2% + volatility adjustment
        
        return base_price * (1 - stop_loss_pct)
    
    def _calculate_take_profit(self, action: Dict[str, Any],
                             current_state: Dict[str, Any]) -> float:
        """Calculate take profit level for action."""
        base_price = action.get('price', current_state.get('current_price', 0))
        volatility = current_state.get('volatility', 0)
        
        # Adjust take profit based on volatility
        take_profit_pct = 0.03 + (volatility * 0.5)  # Base 3% + volatility adjustment
        
        return base_price * (1 + take_profit_pct)
    
    def _calculate_position_limit(self, action: Dict[str, Any],
                                current_state: Dict[str, Any]) -> float:
        """Calculate position limit for action."""
        base_limit = self.risk_limits['max_position_size']
        volatility = current_state.get('volatility', 0)
        
        # Reduce position size in high volatility
        return base_limit * (1 - volatility)
    
    def _calculate_leverage_limit(self, action: Dict[str, Any],
                                current_state: Dict[str, Any]) -> float:
        """Calculate leverage limit for action."""
        base_limit = self.risk_limits['max_leverage']
        volatility = current_state.get('volatility', 0)
        
        # Reduce leverage in high volatility
        return base_limit * (1 - volatility) 