import React from 'react';

// Mock data for the order book
const mockOrderBook = {
  asks: [
    { price: 98.75, amount: 1.23, total: 121.46 },
    { price: 98.70, amount: 2.15, total: 212.21 },
    { price: 98.65, amount: 3.45, total: 340.34 },
    { price: 98.60, amount: 1.89, total: 186.35 },
    { price: 98.55, amount: 2.67, total: 263.13 },
  ],
  bids: [
    { price: 98.45, amount: 1.56, total: 153.58 },
    { price: 98.40, amount: 2.34, total: 230.26 },
    { price: 98.35, amount: 3.12, total: 306.85 },
    { price: 98.30, amount: 1.78, total: 174.97 },
    { price: 98.25, amount: 2.45, total: 240.71 },
  ],
};

const OrderBook: React.FC = () => {
  return (
    <div className="terminal-card">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-terminal-accent">Order Book</h2>
        <div className="flex space-x-2">
          <button className="terminal-button text-sm">Refresh</button>
          <button className="terminal-button text-sm">Auto-Update</button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Asks (Sell Orders) */}
        <div>
          <h3 className="text-sm font-medium text-terminal-error mb-2">Asks</h3>
          <div className="overflow-x-auto">
            <table className="terminal-table">
              <thead>
                <tr>
                  <th>Price</th>
                  <th>Amount</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {mockOrderBook.asks.map((ask, index) => (
                  <tr key={`ask-${index}`} className="text-terminal-error hover:bg-terminal-hover">
                    <td>${ask.price.toFixed(2)}</td>
                    <td>{ask.amount.toFixed(2)}</td>
                    <td>${ask.total.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Bids (Buy Orders) */}
        <div>
          <h3 className="text-sm font-medium text-terminal-success mb-2">Bids</h3>
          <div className="overflow-x-auto">
            <table className="terminal-table">
              <thead>
                <tr>
                  <th>Price</th>
                  <th>Amount</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {mockOrderBook.bids.map((bid, index) => (
                  <tr key={`bid-${index}`} className="text-terminal-success hover:bg-terminal-hover">
                    <td>${bid.price.toFixed(2)}</td>
                    <td>{bid.amount.toFixed(2)}</td>
                    <td>${bid.total.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Spread Information */}
      <div className="mt-4 pt-4 border-t border-terminal-border">
        <div className="grid grid-cols-3 gap-4">
          <div className="terminal-card terminal-glow">
            <span className="text-sm text-gray-400">Spread</span>
            <p className="text-lg font-semibold text-terminal-warning">0.30%</p>
          </div>
          <div className="terminal-card terminal-glow">
            <span className="text-sm text-gray-400">Last Price</span>
            <p className="text-lg font-semibold">$98.45</p>
          </div>
          <div className="terminal-card terminal-glow">
            <span className="text-sm text-gray-400">24h Change</span>
            <p className="text-lg font-semibold text-terminal-success">+2.34%</p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-4 pt-4 border-t border-terminal-border">
        <div className="flex justify-between items-center">
          <div className="flex space-x-2">
            <button className="terminal-button">Place Buy Order</button>
            <button className="terminal-button">Place Sell Order</button>
          </div>
          <div className="flex space-x-2">
            <button className="terminal-button-danger">Cancel All</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderBook; 