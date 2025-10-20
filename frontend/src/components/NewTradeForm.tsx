import { useState } from 'react';
import { TradeCreate } from '../types';
import { X } from 'lucide-react';

interface NewTradeFormProps {
  onSubmit: (trade: TradeCreate) => void;
  onCancel: () => void;
}

export const NewTradeForm = ({ onSubmit, onCancel }: NewTradeFormProps) => {
  const [formData, setFormData] = useState<TradeCreate>({
    ticker: '',
    direction: 'bullish',
    entryPrice: 0,
    stopLoss: 0,
    size: 0,
    marketConditions: '',
    emotions: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">New Trade</h2>
            <button onClick={onCancel} className="text-gray-400 hover:text-gray-600">
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ticker Symbol *
                </label>
                <input
                  type="text"
                  required
                  value={formData.ticker}
                  onChange={(e) => setFormData({ ...formData, ticker: e.target.value.toUpperCase() })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="AAPL"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Direction *
                </label>
                <select
                  required
                  value={formData.direction}
                  onChange={(e) => setFormData({ ...formData, direction: e.target.value as 'bullish' | 'bearish' })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="bullish">Bullish</option>
                  <option value="bearish">Bearish</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Entry Price *
                </label>
                <input
                  type="number"
                  required
                  step="0.01"
                  value={formData.entryPrice || ''}
                  onChange={(e) => setFormData({ ...formData, entryPrice: parseFloat(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="150.00"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Stop Loss *
                </label>
                <input
                  type="number"
                  required
                  step="0.01"
                  value={formData.stopLoss || ''}
                  onChange={(e) => setFormData({ ...formData, stopLoss: parseFloat(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="148.00"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Size (Shares) *
                </label>
                <input
                  type="number"
                  required
                  value={formData.size || ''}
                  onChange={(e) => setFormData({ ...formData, size: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="100"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Market Conditions
              </label>
              <textarea
                value={formData.marketConditions}
                onChange={(e) => setFormData({ ...formData, marketConditions: e.target.value })}
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Describe market conditions, support/resistance levels, etc."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Emotional State
              </label>
              <input
                type="text"
                value={formData.emotions}
                onChange={(e) => setFormData({ ...formData, emotions: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Confident, anxious, etc."
              />
            </div>

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={onCancel}
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
              >
                Create Trade
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
