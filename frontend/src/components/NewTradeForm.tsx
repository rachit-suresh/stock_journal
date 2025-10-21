import { useState } from "react";
import { TradeCreate } from "../types";
import { tradesApi } from "../api/client";
import { X } from "lucide-react";

interface NewTradeFormProps {
  onSubmit: (trade: TradeCreate, currentPrice?: number) => void;
  onCancel: () => void;
}

export const NewTradeForm = ({ onSubmit, onCancel }: NewTradeFormProps) => {
  const [formData, setFormData] = useState<TradeCreate>({
    ticker: "",
    direction: "bullish",
    entryPrice: 0,
    stopLoss: 0,
    size: 0,
    marketConditions: "",
    emotions: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData, checkedPrice ?? undefined);
  };

  const [checking, setChecking] = useState(false);
  const [checkedPrice, setCheckedPrice] = useState<number | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [tickerValid, setTickerValid] = useState<boolean | null>(null);
  const [warning, setWarning] = useState<string | null>(null);

  const handleCheckTicker = async () => {
    const ticker = formData.ticker.trim().toUpperCase();
    if (!ticker) return;
    setChecking(true);
    setCheckedPrice(null);
    setSuggestions([]);
    setTickerValid(null);
    setWarning(null);
    try {
      const res = await tradesApi.getQuote(ticker);
      if (res.found && res.price_inr) {
        setCheckedPrice(res.price_inr);
        setTickerValid(true);
        setWarning(res.warning || null);
      } else {
        setTickerValid(false);
        setSuggestions(res.suggestions || []);
        setWarning(res.warning || null);
      }
    } catch (err) {
      console.error("Quote check failed", err);
      setTickerValid(false);
    } finally {
      setChecking(false);
    }
  };

  const applySuggestion = (s: string) => {
    setFormData({ ...formData, ticker: s });
    setSuggestions([]);
    // optionally auto-check
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">New Trade</h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ticker Symbol *
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    required
                    value={formData.ticker}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        ticker: e.target.value.toUpperCase(),
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="AAPL or INFY"
                  />
                  <button
                    type="button"
                    onClick={handleCheckTicker}
                    disabled={checking}
                    className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg"
                  >
                    {checking ? "Checking..." : "Check"}
                  </button>
                </div>

                {tickerValid === true && checkedPrice !== null && (
                  <>
                    <div className="mt-2 p-3 bg-green-50 rounded-lg">
                      <p className="text-sm font-medium text-green-800">
                        ✓ Current price: ₹
                        {checkedPrice.toLocaleString("en-IN", {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </p>
                      {formData.entryPrice > 0 && formData.size > 0 && (
                        <p className="text-xs text-green-700 mt-1">
                          {formData.direction === "bullish"
                            ? `If price stays at ₹${checkedPrice.toLocaleString(
                                "en-IN",
                                {
                                  minimumFractionDigits: 2,
                                  maximumFractionDigits: 2,
                                }
                              )}, P&L: ₹${(
                                (checkedPrice - formData.entryPrice) *
                                formData.size
                              ).toLocaleString("en-IN", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })}`
                            : `If price stays at ₹${checkedPrice.toLocaleString(
                                "en-IN",
                                {
                                  minimumFractionDigits: 2,
                                  maximumFractionDigits: 2,
                                }
                              )}, P&L: ₹${(
                                (formData.entryPrice - checkedPrice) *
                                formData.size
                              ).toLocaleString("en-IN", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })}`}
                        </p>
                      )}
                    </div>
                    {warning && (
                      <div className="mt-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-sm text-yellow-800">{warning}</p>
                      </div>
                    )}
                  </>
                )}
                {tickerValid === false && (
                  <div className="mt-2">
                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                      <p className="text-sm font-medium text-red-800">
                        Ticker not found
                      </p>
                      {warning && (
                        <p className="text-xs text-red-600 mt-1">{warning}</p>
                      )}
                    </div>
                    {suggestions.length > 0 && (
                      <div className="mt-2">
                        <p className="text-sm text-gray-600 mb-2">Try these suggestions:</p>
                        <div className="flex flex-wrap gap-2">
                          {suggestions.map((s) => (
                            <button
                              key={s}
                              type="button"
                              onClick={() => applySuggestion(s)}
                              className="px-3 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded-full text-sm font-medium"
                            >
                              {s}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Direction *
                </label>
                <select
                  required
                  value={formData.direction}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      direction: e.target.value as "bullish" | "bearish",
                    })
                  }
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
                  value={formData.entryPrice || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      entryPrice: parseFloat(e.target.value),
                    })
                  }
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
                  value={formData.stopLoss || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      stopLoss: parseFloat(e.target.value),
                    })
                  }
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
                  value={formData.size || ""}
                  onChange={(e) =>
                    setFormData({ ...formData, size: parseInt(e.target.value) })
                  }
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
                onChange={(e) =>
                  setFormData({ ...formData, marketConditions: e.target.value })
                }
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
                onChange={(e) =>
                  setFormData({ ...formData, emotions: e.target.value })
                }
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
