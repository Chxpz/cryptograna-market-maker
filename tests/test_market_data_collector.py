"""
Tests for the MarketDataCollector class.
"""
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.collector.market_data_collector import MarketDataCollector

@pytest.fixture
def collector():
    """Create a MarketDataCollector instance for testing."""
    return MarketDataCollector()

@pytest.mark.asyncio
async def test_collect_market_data(collector):
    """Test market data collection."""
    # Mock API responses
    mock_price_data = {
        "price": 100.0,
        "timestamp": "2024-03-20T12:00:00Z"
    }
    mock_order_book = {
        "bids": [[99.0, 1.0], [98.0, 2.0]],
        "asks": [[101.0, 1.0], [102.0, 2.0]]
    }
    mock_trades = [
        {"price": 100.0, "size": 1.0, "side": "buy"},
        {"price": 99.5, "size": 2.0, "side": "sell"}
    ]
    
    # Mock API calls
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.side_effect = [
            Mock(json=lambda: mock_price_data),
            Mock(json=lambda: mock_order_book),
            Mock(json=lambda: mock_trades)
        ]
        
        # Collect market data
        data = await collector.collect_market_data()
        
        # Verify data structure
        assert "price" in data
        assert "order_book" in data
        assert "trades" in data
        assert data["price"] == mock_price_data
        assert data["order_book"] == mock_order_book
        assert data["trades"] == mock_trades

@pytest.mark.asyncio
async def test_health_check(collector):
    """Test health check functionality."""
    # Mock API responses
    mock_price_data = {"price": 100.0}
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value = Mock(json=lambda: mock_price_data)
        
        # Check health
        health = await collector.health_check()
        
        # Verify health status
        assert health["status"] == "healthy"
        assert "last_update" in health
        assert "errors" in health

@pytest.mark.asyncio
async def test_error_handling(collector):
    """Test error handling and recovery."""
    # Mock API error
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.side_effect = Exception("API Error")
        
        # Attempt to collect data
        data = await collector.collect_market_data()
        
        # Verify error handling
        assert data is not None
        assert "errors" in data
        assert len(data["errors"]) > 0

@pytest.mark.asyncio
async def test_rate_limiting(collector):
    """Test rate limiting functionality."""
    # Mock API responses
    mock_price_data = {"price": 100.0}
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value = Mock(json=lambda: mock_price_data)
        
        # Make multiple requests
        start_time = asyncio.get_event_loop().time()
        for _ in range(3):
            await collector._get_price_data()
        end_time = asyncio.get_event_loop().time()
        
        # Verify rate limiting
        assert end_time - start_time >= 0.1  # 100ms minimum between requests 