"""
Tests for the TradingStrategy class.
"""
import pytest
from src.decision.trading_strategy import TradingStrategy

@pytest.fixture
def strategy():
    """Create a TradingStrategy instance for testing."""
    return TradingStrategy()

def test_calculate_parameters(strategy):
    """Test parameter calculation."""
    # Mock market data
    market_data = {
        "price": {
            "price": 100.0,
            "timestamp": "2024-03-20T12:00:00Z"
        },
        "order_book": {
            "bids": [[99.0, 1.0], [98.0, 2.0]],
            "asks": [[101.0, 1.0], [102.0, 2.0]]
        },
        "trades": [
            {"price": 100.0, "size": 1.0, "side": "buy"},
            {"price": 99.5, "size": 2.0, "side": "sell"}
        ]
    }
    
    # Calculate parameters
    params = strategy.calculate_parameters(market_data)
    
    # Verify parameter structure
    assert "bid_spread" in params
    assert "ask_spread" in params
    assert "order_amount" in params
    assert "inventory_skew_enabled" in params
    assert "target_base_pct" in params
    
    # Verify parameter values
    assert 0 < params["bid_spread"] < 0.05
    assert 0 < params["ask_spread"] < 0.05
    assert params["order_amount"] > 0
    assert isinstance(params["inventory_skew_enabled"], bool)
    assert 0 <= params["target_base_pct"] <= 1

def test_position_tracking(strategy):
    """Test position tracking functionality."""
    # Mock trade
    trade = {
        "price": 100.0,
        "size": 1.0,
        "side": "buy"
    }
    
    # Update position
    strategy.update_position(trade)
    
    # Get metrics
    metrics = strategy.get_performance_metrics()
    
    # Verify position tracking
    assert "position_size" in metrics
    assert "realized_pnl" in metrics
    assert "unrealized_pnl" in metrics
    assert metrics["position_size"] == 1.0

def test_risk_management(strategy):
    """Test risk management functionality."""
    # Mock market data with high volatility
    market_data = {
        "price": {
            "price": 100.0,
            "timestamp": "2024-03-20T12:00:00Z"
        },
        "order_book": {
            "bids": [[90.0, 1.0], [80.0, 2.0]],  # Wide spread
            "asks": [[110.0, 1.0], [120.0, 2.0]]
        },
        "trades": [
            {"price": 100.0, "size": 1.0, "side": "buy"},
            {"price": 99.5, "size": 2.0, "side": "sell"}
        ]
    }
    
    # Calculate parameters
    params = strategy.calculate_parameters(market_data)
    
    # Verify risk management
    assert params["bid_spread"] > 0.01  # Increased spread due to volatility
    assert params["order_amount"] < strategy.max_position_size  # Reduced size due to risk

def test_performance_metrics(strategy):
    """Test performance metrics calculation."""
    # Mock trades
    trades = [
        {"price": 100.0, "size": 1.0, "side": "buy"},
        {"price": 101.0, "size": 1.0, "side": "sell"}
    ]
    
    # Update positions
    for trade in trades:
        strategy.update_position(trade)
    
    # Get metrics
    metrics = strategy.get_performance_metrics()
    
    # Verify metrics
    assert "position_size" in metrics
    assert "realized_pnl" in metrics
    assert "unrealized_pnl" in metrics
    assert "win_rate" in metrics
    assert metrics["realized_pnl"] == 1.0  # 101 - 100 = 1
    assert metrics["win_rate"] == 1.0  # One winning trade 