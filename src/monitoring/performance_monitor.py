"""
Performance monitoring and analysis for the trading bot.
"""
import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from prometheus_client import Counter, Gauge, Histogram, Summary

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitors and analyzes trading bot performance."""
    
    def __init__(self):
        # Initialize Prometheus metrics
        self.metrics = {
            # Profitability metrics
            'total_pnl': Counter('bot_total_pnl', 'Total PnL in USD'),
            'win_rate': Gauge('bot_win_rate', 'Win rate percentage'),
            'sharpe_ratio': Gauge('bot_sharpe_ratio', 'Sharpe ratio'),
            'max_drawdown': Gauge('bot_max_drawdown', 'Maximum drawdown percentage'),
            
            # Risk metrics
            'position_size': Gauge('bot_position_size', 'Current position size'),
            'leverage': Gauge('bot_leverage', 'Current leverage'),
            'volatility': Gauge('bot_volatility', 'Current market volatility'),
            
            # Execution metrics
            'order_count': Counter('bot_order_count', 'Total number of orders'),
            'execution_time': Histogram('bot_execution_time', 'Order execution time in seconds'),
            'slippage': Histogram('bot_slippage', 'Order slippage percentage'),
            
            # Market impact metrics
            'spread': Gauge('bot_spread', 'Current market spread'),
            'liquidity': Gauge('bot_liquidity', 'Current market liquidity'),
            'volume': Gauge('bot_volume', 'Current market volume')
        }
        
        # Performance tracking
        self.performance_data = {
            'pnl_history': [],
            'position_history': [],
            'order_history': [],
            'market_data': []
        }
        
        # Analysis parameters
        self.analysis_window = timedelta(days=7)  # Default analysis window
        self.min_trades = 10  # Minimum trades for analysis
        self.risk_free_rate = 0.02  # 2% risk-free rate
    
    def update_metrics(self, data: Dict[str, Any]):
        """Update Prometheus metrics with new data."""
        try:
            # Update profitability metrics
            if 'pnl' in data:
                self.metrics['total_pnl'].inc(data['pnl'])
                self.performance_data['pnl_history'].append({
                    'timestamp': datetime.utcnow(),
                    'value': data['pnl']
                })
            
            if 'win_rate' in data:
                self.metrics['win_rate'].set(data['win_rate'])
            
            # Update risk metrics
            if 'position_size' in data:
                self.metrics['position_size'].set(data['position_size'])
                self.performance_data['position_history'].append({
                    'timestamp': datetime.utcnow(),
                    'value': data['position_size']
                })
            
            if 'leverage' in data:
                self.metrics['leverage'].set(data['leverage'])
            
            if 'volatility' in data:
                self.metrics['volatility'].set(data['volatility'])
            
            # Update execution metrics
            if 'order_executed' in data:
                self.metrics['order_count'].inc()
                self.performance_data['order_history'].append({
                    'timestamp': datetime.utcnow(),
                    'order': data['order_executed']
                })
            
            if 'execution_time' in data:
                self.metrics['execution_time'].observe(data['execution_time'])
            
            if 'slippage' in data:
                self.metrics['slippage'].observe(data['slippage'])
            
            # Update market impact metrics
            if 'spread' in data:
                self.metrics['spread'].set(data['spread'])
            
            if 'liquidity' in data:
                self.metrics['liquidity'].set(data['liquidity'])
            
            if 'volume' in data:
                self.metrics['volume'].set(data['volume'])
            
            # Store market data
            self.performance_data['market_data'].append({
                'timestamp': datetime.utcnow(),
                'data': data
            })
            
            # Clean up old data
            self._cleanup_old_data()
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze bot performance and generate insights."""
        try:
            # Get data within analysis window
            window_start = datetime.utcnow() - self.analysis_window
            pnl_data = [d for d in self.performance_data['pnl_history'] 
                       if d['timestamp'] >= window_start]
            position_data = [d for d in self.performance_data['position_history']
                           if d['timestamp'] >= window_start]
            order_data = [d for d in self.performance_data['order_history']
                         if d['timestamp'] >= window_start]
            
            if len(order_data) < self.min_trades:
                return {
                    'status': 'insufficient_data',
                    'message': f'Need at least {self.min_trades} trades for analysis'
                }
            
            # Calculate performance metrics
            total_pnl = sum(d['value'] for d in pnl_data)
            win_rate = self._calculate_win_rate(order_data)
            sharpe_ratio = self._calculate_sharpe_ratio(pnl_data)
            max_drawdown = self._calculate_max_drawdown(pnl_data)
            
            # Calculate risk metrics
            avg_position = np.mean([d['value'] for d in position_data])
            position_volatility = np.std([d['value'] for d in position_data])
            
            # Calculate execution metrics
            avg_execution_time = self._calculate_avg_execution_time(order_data)
            avg_slippage = self._calculate_avg_slippage(order_data)
            
            # Generate insights
            insights = self._generate_insights({
                'total_pnl': total_pnl,
                'win_rate': win_rate,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'avg_position': avg_position,
                'position_volatility': position_volatility,
                'avg_execution_time': avg_execution_time,
                'avg_slippage': avg_slippage
            })
            
            return {
                'status': 'success',
                'metrics': {
                    'total_pnl': total_pnl,
                    'win_rate': win_rate,
                    'sharpe_ratio': sharpe_ratio,
                    'max_drawdown': max_drawdown,
                    'avg_position': avg_position,
                    'position_volatility': position_volatility,
                    'avg_execution_time': avg_execution_time,
                    'avg_slippage': avg_slippage
                },
                'insights': insights
            }
            
        except Exception as e:
            logger.error(f"Error analyzing performance: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _cleanup_old_data(self):
        """Clean up data older than analysis window."""
        window_start = datetime.utcnow() - self.analysis_window
        
        for key in self.performance_data:
            self.performance_data[key] = [
                d for d in self.performance_data[key]
                if d['timestamp'] >= window_start
            ]
    
    def _calculate_win_rate(self, order_data: List[Dict[str, Any]]) -> float:
        """Calculate win rate from order history."""
        if not order_data:
            return 0.0
        
        winning_trades = sum(1 for d in order_data if d['order'].get('pnl', 0) > 0)
        return winning_trades / len(order_data)
    
    def _calculate_sharpe_ratio(self, pnl_data: List[Dict[str, Any]]) -> float:
        """Calculate Sharpe ratio from PnL history."""
        if len(pnl_data) < 2:
            return 0.0
        
        returns = [d['value'] for d in pnl_data]
        excess_returns = np.array(returns) - self.risk_free_rate/252  # Daily risk-free rate
        
        if len(excess_returns) == 0 or np.std(excess_returns) == 0:
            return 0.0
        
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)  # Annualized
    
    def _calculate_max_drawdown(self, pnl_data: List[Dict[str, Any]]) -> float:
        """Calculate maximum drawdown from PnL history."""
        if not pnl_data:
            return 0.0
        
        cumulative_pnl = np.cumsum([d['value'] for d in pnl_data])
        max_drawdown = 0.0
        peak = cumulative_pnl[0]
        
        for pnl in cumulative_pnl:
            if pnl > peak:
                peak = pnl
            drawdown = (peak - pnl) / peak if peak > 0 else 0
            max_drawdown = max(max_drawdown, drawdown)
        
        return max_drawdown
    
    def _calculate_avg_execution_time(self, order_data: List[Dict[str, Any]]) -> float:
        """Calculate average execution time from order history."""
        if not order_data:
            return 0.0
        
        execution_times = [
            d['order'].get('execution_time', 0)
            for d in order_data
            if 'execution_time' in d['order']
        ]
        
        return np.mean(execution_times) if execution_times else 0.0
    
    def _calculate_avg_slippage(self, order_data: List[Dict[str, Any]]) -> float:
        """Calculate average slippage from order history."""
        if not order_data:
            return 0.0
        
        slippages = [
            d['order'].get('slippage', 0)
            for d in order_data
            if 'slippage' in d['order']
        ]
        
        return np.mean(slippages) if slippages else 0.0
    
    def _generate_insights(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate insights from performance metrics."""
        insights = []
        
        # PnL insights
        if metrics['total_pnl'] < 0:
            insights.append({
                'type': 'warning',
                'message': 'Bot is currently operating at a loss',
                'suggestion': 'Review strategy parameters and market conditions'
            })
        
        # Win rate insights
        if metrics['win_rate'] < 0.4:
            insights.append({
                'type': 'warning',
                'message': 'Low win rate detected',
                'suggestion': 'Consider adjusting entry/exit criteria'
            })
        
        # Risk insights
        if metrics['max_drawdown'] > 0.1:  # 10% drawdown
            insights.append({
                'type': 'warning',
                'message': 'High maximum drawdown detected',
                'suggestion': 'Implement stricter risk management'
            })
        
        if metrics['position_volatility'] > metrics['avg_position'] * 0.5:
            insights.append({
                'type': 'warning',
                'message': 'High position volatility detected',
                'suggestion': 'Consider reducing position size variability'
            })
        
        # Execution insights
        if metrics['avg_execution_time'] > 1.0:  # 1 second
            insights.append({
                'type': 'warning',
                'message': 'Slow execution times detected',
                'suggestion': 'Optimize order execution process'
            })
        
        if metrics['avg_slippage'] > 0.001:  # 0.1%
            insights.append({
                'type': 'warning',
                'message': 'High slippage detected',
                'suggestion': 'Consider using more conservative order sizes'
            })
        
        # Positive insights
        if metrics['sharpe_ratio'] > 2.0:
            insights.append({
                'type': 'success',
                'message': 'Good risk-adjusted returns',
                'suggestion': 'Consider increasing position sizes'
            })
        
        if metrics['win_rate'] > 0.6:
            insights.append({
                'type': 'success',
                'message': 'High win rate achieved',
                'suggestion': 'Strategy is performing well'
            })
        
        return insights 