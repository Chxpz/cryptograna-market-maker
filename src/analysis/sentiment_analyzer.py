"""
Sentiment analyzer that implements various sentiment analysis methods.
"""
import logging
import numpy as np
from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer

logger = logging.getLogger(__name__)

class SentimentAnalyzer(BaseAnalyzer):
    """Sentiment analysis implementation."""
    
    def __init__(self):
        super().__init__()
        self.required_fields = [
            'social_mentions',
            'news_sentiment',
            'market_sentiment',
            'developer_activity',
            'community_growth'
        ]
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform sentiment analysis on market data.
        
        Args:
            data: Dictionary containing market data
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        if not self._validate_data(data, self.required_fields):
            logger.error(f"Missing required fields for sentiment analysis: {self.required_fields}")
            return {}
            
        try:
            # Extract sentiment data
            social_mentions = data['social_mentions']
            news_sentiment = data['news_sentiment']
            market_sentiment = data['market_sentiment']
            developer_activity = data['developer_activity']
            community_growth = data['community_growth']
            
            # Calculate sentiment scores
            social_score = self._calculate_social_score(social_mentions)
            news_score = self._calculate_news_score(news_sentiment)
            market_score = self._calculate_market_score(market_sentiment)
            developer_score = self._calculate_developer_score(developer_activity)
            community_score = self._calculate_community_score(community_growth)
            
            # Calculate overall sentiment
            overall_sentiment = self._calculate_overall_sentiment(
                social_score,
                news_score,
                market_score,
                developer_score,
                community_score
            )
            
            # Generate signals
            signals = self._generate_signals(
                social_score,
                news_score,
                market_score,
                developer_score,
                community_score,
                overall_sentiment
            )
            
            # Calculate confidence
            confidence_factors = {
                'social_volume': min(len(social_mentions) / 1000, 1),  # Normalize to 1000 mentions
                'news_volume': min(len(news_sentiment) / 100, 1),  # Normalize to 100 news items
                'market_volume': min(len(market_sentiment) / 1000, 1),  # Normalize to 1000 market events
                'developer_activity': min(developer_activity['commits'] / 100, 1),  # Normalize to 100 commits
                'community_growth': min(community_growth['new_members'] / 1000, 1)  # Normalize to 1000 new members
            }
            
            self.confidence = self._calculate_confidence(confidence_factors)
            
            results = {
                'overall_sentiment': overall_sentiment,
                'signals': signals,
                'scores': {
                    'social': social_score,
                    'news': news_score,
                    'market': market_score,
                    'developer': developer_score,
                    'community': community_score
                },
                'confidence': self.confidence
            }
            
            self._log_analysis(results)
            return results
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {}
    
    def _calculate_social_score(self, mentions: List[Dict[str, Any]]) -> float:
        """
        Calculate social media sentiment score.
        
        Args:
            mentions: List of social media mentions with sentiment scores
            
        Returns:
            Social sentiment score between -1 and 1
        """
        if not mentions:
            return 0.0
            
        scores = [mention['sentiment'] for mention in mentions]
        return np.mean(scores)
    
    def _calculate_news_score(self, news: List[Dict[str, Any]]) -> float:
        """
        Calculate news sentiment score.
        
        Args:
            news: List of news items with sentiment scores
            
        Returns:
            News sentiment score between -1 and 1
        """
        if not news:
            return 0.0
            
        scores = [item['sentiment'] for item in news]
        return np.mean(scores)
    
    def _calculate_market_score(self, sentiment: Dict[str, Any]) -> float:
        """
        Calculate market sentiment score.
        
        Args:
            sentiment: Dictionary containing market sentiment indicators
            
        Returns:
            Market sentiment score between -1 and 1
        """
        if not sentiment:
            return 0.0
            
        # Weight different market indicators
        weights = {
            'fear_greed_index': 0.3,
            'market_momentum': 0.3,
            'volatility': 0.2,
            'volume_trend': 0.2
        }
        
        score = 0.0
        for indicator, weight in weights.items():
            if indicator in sentiment:
                score += sentiment[indicator] * weight
                
        return score
    
    def _calculate_developer_score(self, activity: Dict[str, Any]) -> float:
        """
        Calculate developer activity score.
        
        Args:
            activity: Dictionary containing developer activity metrics
            
        Returns:
            Developer activity score between -1 and 1
        """
        if not activity:
            return 0.0
            
        # Weight different developer metrics
        weights = {
            'commits': 0.3,
            'contributors': 0.2,
            'issues': 0.2,
            'pull_requests': 0.3
        }
        
        score = 0.0
        for metric, weight in weights.items():
            if metric in activity:
                # Normalize each metric to a -1 to 1 scale
                normalized_value = min(activity[metric] / 100, 1)  # Assuming 100 is a good baseline
                score += normalized_value * weight
                
        return score
    
    def _calculate_community_score(self, growth: Dict[str, Any]) -> float:
        """
        Calculate community growth score.
        
        Args:
            growth: Dictionary containing community growth metrics
            
        Returns:
            Community growth score between -1 and 1
        """
        if not growth:
            return 0.0
            
        # Weight different community metrics
        weights = {
            'new_members': 0.3,
            'active_members': 0.3,
            'engagement_rate': 0.2,
            'sentiment': 0.2
        }
        
        score = 0.0
        for metric, weight in weights.items():
            if metric in growth:
                # Normalize each metric to a -1 to 1 scale
                normalized_value = min(growth[metric] / 1000, 1)  # Assuming 1000 is a good baseline
                score += normalized_value * weight
                
        return score
    
    def _calculate_overall_sentiment(self, social_score: float, news_score: float,
                                   market_score: float, developer_score: float,
                                   community_score: float) -> str:
        """
        Calculate overall market sentiment.
        
        Args:
            social_score: Social media sentiment score
            news_score: News sentiment score
            market_score: Market sentiment score
            developer_score: Developer activity score
            community_score: Community growth score
            
        Returns:
            Overall sentiment status
        """
        # Weight different sentiment sources
        weights = {
            'social': 0.3,
            'news': 0.2,
            'market': 0.2,
            'developer': 0.15,
            'community': 0.15
        }
        
        scores = {
            'social': social_score,
            'news': news_score,
            'market': market_score,
            'developer': developer_score,
            'community': community_score
        }
        
        # Calculate weighted average
        weighted_sum = sum(scores[source] * weight for source, weight in weights.items())
        
        # Determine sentiment
        if weighted_sum > 0.3:
            return "bullish"
        elif weighted_sum < -0.3:
            return "bearish"
        else:
            return "neutral"
    
    def _generate_signals(self, social_score: float, news_score: float,
                         market_score: float, developer_score: float,
                         community_score: float, overall_sentiment: str) -> Dict[str, float]:
        """
        Generate trading signals based on sentiment analysis.
        
        Args:
            social_score: Social media sentiment score
            news_score: News sentiment score
            market_score: Market sentiment score
            developer_score: Developer activity score
            community_score: Community growth score
            overall_sentiment: Overall sentiment status
            
        Returns:
            Dictionary of trading signals
        """
        signals = {
            'social_signal': 0.0,
            'news_signal': 0.0,
            'market_signal': 0.0,
            'developer_signal': 0.0,
            'community_signal': 0.0,
            'overall_signal': 0.0
        }
        
        # Social signal
        signals['social_signal'] = social_score
        
        # News signal
        signals['news_signal'] = news_score
        
        # Market signal
        signals['market_signal'] = market_score
        
        # Developer signal
        signals['developer_signal'] = developer_score
        
        # Community signal
        signals['community_signal'] = community_score
        
        # Overall signal based on sentiment
        if overall_sentiment == "bullish":
            signals['overall_signal'] = 1.0
        elif overall_sentiment == "bearish":
            signals['overall_signal'] = -1.0
        else:
            signals['overall_signal'] = 0.0
            
        return signals 