import { useState, useEffect } from "react";
import { tradesApi } from "../api/client";
import { Trade, Alert as AlertType, PriceUpdate } from "../types";
import { TradeCard } from "../components/TradeCard";
import { NewTradeForm } from "../components/NewTradeForm";
import { CloseTradeForm } from "../components/CloseTradeForm";
import { AlertBanner } from "../components/AlertBanner";
import { getWebSocketService } from "../services/websocket";
import { Plus, TrendingUp, IndianRupee, Activity } from "lucide-react";

export const Dashboard = () => {
  const [openTrades, setOpenTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewTradeForm, setShowNewTradeForm] = useState(false);
  const [tradeToClose, setTradeToClose] = useState<Trade | null>(null);
  const [prices, setPrices] = useState<Record<string, number>>({});
  const [alerts, setAlerts] = useState<AlertType[]>([]);
  const [winRate, setWinRate] = useState<number | null>(null);

  useEffect(() => {
    loadOpenTrades();
    loadStatistics();

    const wsService = getWebSocketService();
    wsService.connect();

    const priceHandler = (update: PriceUpdate) => {
      setPrices((prev) => ({ ...prev, [update.ticker]: update.price }));
    };

    const alertHandler = (alert: AlertType) => {
      setAlerts((prev) => [...prev, alert]);
      // Auto-dismiss after 10 seconds
      setTimeout(() => {
        setAlerts((prev) => prev.filter((a) => a !== alert));
      }, 10000);
    };

    wsService.onPriceUpdate(priceHandler);
    wsService.onAlert(alertHandler);

    return () => {
      wsService.removePriceHandler(priceHandler);
      wsService.removeAlertHandler(alertHandler);
    };
  }, []);

  useEffect(() => {
    if (openTrades.length > 0) {
      const wsService = getWebSocketService();
      const tickers = openTrades.map((t) => t.ticker);
      wsService.subscribe(tickers);

      // Poll for price updates every 5 seconds as backup
      const intervalId = setInterval(() => {
        fetchInitialPrices(tickers);
      }, 5000);

      return () => clearInterval(intervalId);
    }
  }, [openTrades]);

  const loadOpenTrades = async () => {
    try {
      const trades = await tradesApi.getOpenTrades();
      console.log("Loaded trades:", trades);
      setOpenTrades(trades);

      // Fetch initial prices for all tickers
      await fetchInitialPrices(trades.map((t) => t.ticker));
    } catch (error) {
      console.error("Failed to load trades:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchInitialPrices = async (tickers: string[]) => {
    const uniqueTickers = [...new Set(tickers)];
    const pricePromises = uniqueTickers.map(async (ticker) => {
      try {
        const quote = await tradesApi.getQuote(ticker);
        if (quote.found && quote.price) {
          return { ticker, price: quote.price };
        }
      } catch (error) {
        console.error(`Failed to fetch price for ${ticker}:`, error);
      }
      return null;
    });

    const results = await Promise.all(pricePromises);
    const newPrices: Record<string, number> = {};
    results.forEach((result) => {
      if (result) {
        newPrices[result.ticker] = result.price;
      }
    });
    setPrices((prev) => ({ ...prev, ...newPrices }));
  };

  const loadStatistics = async () => {
    try {
      const stats = await tradesApi.getStatistics();
      setWinRate(stats.win_rate);
    } catch (error) {
      console.error("Failed to load statistics:", error);
    }
  };

  const handleCreateTrade = async (tradeData: any, currentPrice?: number) => {
    try {
      await tradesApi.createTrade(tradeData);

      // If we have the current price from the check, set it immediately
      if (currentPrice && tradeData.ticker) {
        setPrices((prev) => ({ ...prev, [tradeData.ticker]: currentPrice }));
      }

      setShowNewTradeForm(false);
      loadOpenTrades();
    } catch (error) {
      console.error("Failed to create trade:", error);
    }
  };

  const handleCloseTrade = async (closeData: any) => {
    if (!tradeToClose) return;

    console.log("Closing trade:", tradeToClose);
    console.log("Trade ID:", tradeToClose._id);

    if (!tradeToClose._id) {
      console.error("Trade ID is missing!", tradeToClose);
      alert("Error: Trade ID is missing. Please refresh and try again.");
      return;
    }

    try {
      await tradesApi.closeTrade(tradeToClose._id, closeData);
      setTradeToClose(null);
      loadOpenTrades();
    } catch (error) {
      console.error("Failed to close trade:", error);
    }
  };

  const totalUnrealizedPnL = openTrades.reduce((sum, trade) => {
    const currentPrice = prices[trade.ticker];
    if (!currentPrice) return sum;

    const pnl =
      trade.direction === "bullish"
        ? (currentPrice - trade.entryPrice) * trade.size
        : (trade.entryPrice - currentPrice) * trade.size;

    return sum + pnl;
  }, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Alerts */}
      {alerts.map((alert, index) => (
        <AlertBanner
          key={`${alert.trade_id}-${index}`}
          alert={alert}
          onDismiss={() => setAlerts(alerts.filter((_, i) => i !== index))}
        />
      ))}

      {/* Statistics and Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Open Positions</h2>
          <button
            onClick={() => setShowNewTradeForm(true)}
            className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
          >
            <Plus className="w-5 h-5 mr-2" />
            New Trade
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Activity className="w-8 h-8 text-blue-500 mr-3" />
              <div>
                <p className="text-sm text-gray-500">Active Trades</p>
                <p className="text-2xl font-bold text-gray-900">
                  {openTrades.length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <IndianRupee className="w-8 h-8 text-green-500 mr-3" />
              <div>
                <p className="text-sm text-gray-500">Unrealized P&L</p>
                <p
                  className={`text-2xl font-bold ${
                    totalUnrealizedPnL >= 0 ? "text-green-600" : "text-red-600"
                  }`}
                >
                  ₹
                  {totalUnrealizedPnL.toLocaleString("en-IN", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <TrendingUp className="w-8 h-8 text-purple-500 mr-3" />
              <div>
                <p className="text-sm text-gray-500">Win Rate</p>
                <p className="text-2xl font-bold text-gray-900">
                  {winRate !== null ? `${winRate.toFixed(1)}%` : "-"}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Trades Grid */}
        {openTrades.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No open trades</p>
            <p className="text-gray-400 mt-2">
              Create your first trade to get started
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {openTrades.map((trade) => (
              <TradeCard
                key={trade._id}
                trade={trade}
                currentPrice={prices[trade.ticker]}
                onClose={setTradeToClose}
              />
            ))}
          </div>
        )}
      </div>

      {/* Modals */}
      {showNewTradeForm && (
        <NewTradeForm
          onSubmit={handleCreateTrade}
          onCancel={() => setShowNewTradeForm(false)}
        />
      )}

      {tradeToClose && (
        <CloseTradeForm
          trade={tradeToClose}
          onSubmit={handleCloseTrade}
          onCancel={() => setTradeToClose(null)}
        />
      )}
    </div>
  );
};
