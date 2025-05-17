"""
Technical analyzer that implements various technical analysis methods.
"""
import logging
import numpy as np
from typing import Dict, Any, List, Tuple
from .base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)

class TechnicalAnalyzer(BaseAnalyzer):
    """Technical analysis implementation."""
    
    def __init__(self):
        super().__init__()
        self.required_fields = ['prices', 'volumes', 'timestamps']
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform technical analysis on market data.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Dictionary containing technical analysis results
        """
        if not self._validate_data(data, self.required_fields):
            logger.error(f"Missing required fields for technical analysis: {self.required_fields}")
            return {}
            
        try:
            # Calculate technical indicators
            prices = np.array(data['prices'])
            volumes = np.array(data['volumes'])
            
            # Calculate moving averages
            sma_20 = self._calculate_sma(prices, 20)
            sma_50 = self._calculate_sma(prices, 50)
            ema_20 = self._calculate_ema(prices, 20)
            
            # Calculate RSI
            rsi = self._calculate_rsi(prices)
            
            # Calculate MACD
            macd, signal = self._calculate_macd(prices)
            
            # Calculate Bollinger Bands
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(prices)
            
            # Calculate volume indicators
            obv = self._calculate_obv(prices, volumes)
            
            # Determine trend
            trend = self._determine_trend(prices, sma_20, sma_50)
            
            # Calculate volatility
            volatility = self._calculate_volatility(prices)
            
            # Generate signals
            signals = self._generate_signals(
                prices[-1],
                sma_20[-1],
                sma_50[-1],
                rsi[-1],
                macd[-1],
                signal[-1],
                bb_upper[-1],
                bb_lower[-1]
            )
            
            # Calculate confidence
            confidence_factors = {
                'trend_strength': abs(sma_20[-1] - sma_50[-1]) / sma_50[-1],
                'rsi_signal': 1 - abs(rsi[-1] - 50) / 50,
                'macd_signal': abs(macd[-1] - signal[-1]) / abs(signal[-1]) if signal[-1] != 0 else 0,
                'volatility': 1 - min(volatility, 1)
            }
            
            self.confidence = self._calculate_confidence(confidence_factors)
            
            results = {
                'trend': trend,
                'volatility': volatility,
                'signals': signals,
                'indicators': {
                    'sma_20': sma_20[-1],
                    'sma_50': sma_50[-1],
                    'ema_20': ema_20[-1],
                    'rsi': rsi[-1],
                    'macd': macd[-1],
                    'macd_signal': signal[-1],
                    'bb_upper': bb_upper[-1],
                    'bb_middle': bb_middle[-1],
                    'bb_lower': bb_lower[-1],
                    'obv': obv[-1]
                },
                'confidence': self.confidence
            }
            
            self._log_analysis(results)
            return results
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {str(e)}")
            return {}
    
    def _calculate_sma(self, prices: np.ndarray, period: int) -> np.ndarray:
        """Calculate Simple Moving Average."""
        return np.convolve(prices, np.ones(period)/period, mode='valid')
    
    def _calculate_ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average."""
        return np.convolve(prices, np.exp(-np.arange(period)/period), mode='valid')
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Relative Strength Index."""
        deltas = np.diff(prices)
        gain = np.where(deltas > 0, deltas, 0)
        loss = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.convolve(gain, np.ones(period)/period, mode='valid')
        avg_loss = np.convolve(loss, np.ones(period)/period, mode='valid')
        
        rs = avg_gain / np.where(avg_loss != 0, avg_loss, 1)
        return 100 - (100 / (1 + rs))
    
    def _calculate_macd(self, prices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate MACD and Signal line."""
        ema_12 = self._calculate_ema(prices, 12)
        ema_26 = self._calculate_ema(prices, 26)
        macd = ema_12 - ema_26
        signal = self._calculate_ema(macd, 9)
        return macd, signal
    
    def _calculate_bollinger_bands(self, prices: np.ndarray, period: int = 20, std_dev: float = 2.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate Bollinger Bands."""
        sma = self._calculate_sma(prices, period)
        std = np.std(prices[-period:])
        upper = sma + (std_dev * std)
        lower = sma - (std_dev * std)
        return upper, sma, lower
    
    def _calculate_obv(self, prices: np.ndarray, volumes: np.ndarray) -> np.ndarray:
        """Calculate On-Balance Volume."""
        obv = np.zeros_like(prices)
        obv[0] = volumes[0]
        
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                obv[i] = obv[i-1] + volumes[i]
            elif prices[i] < prices[i-1]:
                obv[i] = obv[i-1] - volumes[i]
            else:
                obv[i] = obv[i-1]
                
        return obv
    
    def _determine_trend(self, prices: np.ndarray, sma_20: np.ndarray, sma_50: np.ndarray) -> str:
        """Determine the current market trend."""
        if len(sma_20) == 0 or len(sma_50) == 0:
            return "unknown"
            
        current_price = prices[-1]
        current_sma20 = sma_20[-1]
        current_sma50 = sma_50[-1]
        
        if current_price > current_sma20 and current_sma20 > current_sma50:
            return "strong_uptrend"
        elif current_price > current_sma20:
            return "uptrend"
        elif current_price < current_sma20 and current_sma20 < current_sma50:
            return "strong_downtrend"
        elif current_price < current_sma20:
            return "downtrend"
        else:
            return "sideways"
    
    def _calculate_volatility(self, prices: np.ndarray, period: int = 20) -> float:
        """Calculate price volatility."""
        returns = np.diff(prices) / prices[:-1]
        return np.std(returns[-period:])
    
    def _generate_signals(self, price: float, sma20: float, sma50: float, rsi: float,
                         macd: float, signal: float, bb_upper: float, bb_lower: float) -> Dict[str, float]:
        """Generate trading signals based on technical indicators."""
        signals = {
            'trend_signal': 0.0,
            'momentum_signal': 0.0,
            'volatility_signal': 0.0,
            'overall_signal': 0.0
        }
        
        # Trend signal
        if price > sma20 and sma20 > sma50:
            signals['trend_signal'] = 1.0
        elif price < sma20 and sma20 < sma50:
            signals['trend_signal'] = -1.0
            
        # Momentum signal
        if rsi > 70:
            signals['momentum_signal'] = -1.0
        elif rsi < 30:
            signals['momentum_signal'] = 1.0
            
        if macd > signal:
            signals['momentum_signal'] += 0.5
        elif macd < signal:
            signals['momentum_signal'] -= 0.5
            
        # Volatility signal
        if price > bb_upper:
            signals['volatility_signal'] = -1.0
        elif price < bb_lower:
            signals['volatility_signal'] = 1.0
            
        # Overall signal
        signals['overall_signal'] = (
            signals['trend_signal'] * 0.4 +
            signals['momentum_signal'] * 0.4 +
            signals['volatility_signal'] * 0.2
        )
        
        return signals 