import { useState, useEffect } from "react";
import { tradesApi } from "../api/client";
import { Trade } from "../types";
import { Trash2, TrendingUp, TrendingDown, Calendar } from "lucide-react";

export const History = () => {
  const [closedTrades, setClosedTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadClosedTrades();
  }, []);

  const loadClosedTrades = async () => {
    try {
      const trades = await tradesApi.getClosedTrades();
      setClosedTrades(trades);
    } catch (error) {
      console.error("Failed to load closed trades:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTrade = async (trade: Trade) => {
    if (
      !window.confirm(
        `Are you sure you want to permanently delete the trade for ${trade.ticker}? This action cannot be undone.`
      )
    ) {
      return;
    }

    try {
      await tradesApi.deleteTrade(trade._id);
      setClosedTrades(closedTrades.filter((t) => t._id !== trade._id));
    } catch (error) {
      console.error("Failed to delete trade:", error);
      alert("Failed to delete trade. Please try again.");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Trade History</h1>
          <p className="mt-1 text-sm text-gray-500">
            Review your past trades and analyze performance
          </p>
        </div>

        {closedTrades.length === 0 ? (
          <div className="text-center py-12">
            <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No closed trades yet</p>
            <p className="text-gray-400 mt-2">
              Your trading history will appear here once you close trades
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {closedTrades.map((trade) => (
              <div
                key={trade._id}
                className="bg-white rounded-lg shadow-md overflow-hidden"
              >
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">
                        {trade.ticker}
                      </h3>
                      <div className="flex items-center gap-3 mt-2">
                        <span
                          className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                            trade.direction === "bullish"
                              ? "bg-green-100 text-green-800"
                              : "bg-red-100 text-red-800"
                          }`}
                        >
                          {trade.direction === "bullish" ? (
                            <>
                              <TrendingUp className="w-4 h-4 mr-1" /> Bullish
                            </>
                          ) : (
                            <>
                              <TrendingDown className="w-4 h-4 mr-1" /> Bearish
                            </>
                          )}
                        </span>
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-800">
                          CLOSED
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDeleteTrade(trade)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete trade permanently"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-500">Entry Price</p>
                      <p className="text-lg font-semibold text-gray-900">
                        ${trade.entryPrice.toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Exit Price</p>
                      <p className="text-lg font-semibold text-gray-900">
                        ${trade.exitPrice?.toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Size</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {trade.size} shares
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Stop Loss</p>
                      <p className="text-lg font-semibold text-red-600">
                        ${trade.stopLoss.toFixed(2)}
                      </p>
                    </div>
                  </div>

                  {trade.result_pnl !== undefined && (
                    <div
                      className={`p-4 rounded-lg mb-4 ${
                        trade.result_pnl >= 0 ? "bg-green-50" : "bg-red-50"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">
                          Realized P&L
                        </span>
                        <span
                          className={`text-2xl font-bold ${
                            trade.result_pnl >= 0
                              ? "text-green-600"
                              : "text-red-600"
                          }`}
                        >
                          ${trade.result_pnl.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  )}

                  {trade.marketConditions && (
                    <div className="mb-3">
                      <p className="text-sm font-medium text-gray-700">
                        Market Conditions
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {trade.marketConditions}
                      </p>
                    </div>
                  )}

                  {trade.emotions && (
                    <div className="mb-3">
                      <p className="text-sm font-medium text-gray-700">
                        Emotions
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {trade.emotions}
                      </p>
                    </div>
                  )}

                  {trade.lessonsLearned && (
                    <div className="mb-3">
                      <p className="text-sm font-medium text-gray-700">
                        Lessons Learned
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {trade.lessonsLearned}
                      </p>
                    </div>
                  )}

                  <div className="flex items-center text-sm text-gray-500 mt-4 pt-4 border-t">
                    <Calendar className="w-4 h-4 mr-2" />
                    <span>
                      Entry: {new Date(trade.entryDate).toLocaleDateString()}
                    </span>
                    {trade.exitDate && (
                      <span className="ml-4">
                        Exit: {new Date(trade.exitDate).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
