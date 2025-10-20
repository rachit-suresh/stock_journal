import { Trade } from "../types";
import { TrendingUp, TrendingDown, IndianRupee, Calendar } from "lucide-react";

interface TradeCardProps {
  trade: Trade;
  currentPrice?: number;
  onClose?: (trade: Trade) => void;
}

export const TradeCard = ({ trade, currentPrice, onClose }: TradeCardProps) => {
  const isProfit = trade.result_pnl ? trade.result_pnl > 0 : false;
  const isProfitable = currentPrice
    ? trade.direction === "bullish"
      ? currentPrice > trade.entryPrice
      : currentPrice < trade.entryPrice
    : false;

  const unrealizedPnL = currentPrice
    ? trade.direction === "bullish"
      ? (currentPrice - trade.entryPrice) * trade.size
      : (trade.entryPrice - currentPrice) * trade.size
    : 0;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-2xl font-bold text-gray-900">{trade.ticker}</h3>
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium mt-2 ${
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
        </div>
        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${
            trade.status === "open"
              ? "bg-blue-100 text-blue-800"
              : "bg-gray-100 text-gray-800"
          }`}
        >
          {trade.status.toUpperCase()}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-500">Entry Price</p>
          <p className="text-lg font-semibold text-gray-900">
            ₹
            {trade.entryPrice.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Stop Loss</p>
          <p className="text-lg font-semibold text-red-600">
            ₹
            {trade.stopLoss.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Size</p>
          <p className="text-lg font-semibold text-gray-900">
            {trade.size} shares
          </p>
        </div>
        {trade.status === "open" && (
          <div>
            <p className="text-sm text-gray-500">Current Price</p>
            {currentPrice ? (
              <p
                className={`text-lg font-semibold ${
                  isProfitable ? "text-green-600" : "text-red-600"
                }`}
              >
                ₹
                {currentPrice.toLocaleString("en-IN", {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </p>
            ) : (
              <p className="text-lg font-semibold text-gray-400">N/A</p>
            )}
          </div>
        )}
        {trade.exitPrice && (
          <div>
            <p className="text-sm text-gray-500">Exit Price</p>
            <p className="text-lg font-semibold text-gray-900">
              ₹
              {trade.exitPrice.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </p>
          </div>
        )}
      </div>

      {trade.status === "open" && (
        <div
          className={`p-4 rounded-lg mb-4 ${
            currentPrice
              ? isProfitable
                ? "bg-green-50"
                : "bg-red-50"
              : "bg-gray-50"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              Unrealized P&L
            </span>
            {currentPrice ? (
              <span
                className={`text-xl font-bold flex items-center ${
                  isProfitable ? "text-green-600" : "text-red-600"
                }`}
              >
                <IndianRupee className="w-5 h-5" />
                {unrealizedPnL.toLocaleString("en-IN", {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </span>
            ) : (
              <span className="text-xl font-bold text-gray-400">N/A</span>
            )}
          </div>
        </div>
      )}

      {trade.result_pnl !== undefined && trade.status === "closed" && (
        <div
          className={`p-4 rounded-lg mb-4 ${
            isProfit ? "bg-green-50" : "bg-red-50"
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              Realized P&L
            </span>
            <span
              className={`text-xl font-bold flex items-center ${
                isProfit ? "text-green-600" : "text-red-600"
              }`}
            >
              <IndianRupee className="w-5 h-5" />
              {trade.result_pnl.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </span>
          </div>
        </div>
      )}

      {trade.marketConditions && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700">Market Conditions</p>
          <p className="text-sm text-gray-600 mt-1">{trade.marketConditions}</p>
        </div>
      )}

      {trade.emotions && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700">Emotions</p>
          <p className="text-sm text-gray-600 mt-1">{trade.emotions}</p>
        </div>
      )}

      {trade.lessonsLearned && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700">Lessons Learned</p>
          <p className="text-sm text-gray-600 mt-1">{trade.lessonsLearned}</p>
        </div>
      )}

      <div className="flex items-center text-sm text-gray-500 mt-4">
        <Calendar className="w-4 h-4 mr-2" />
        <span>Entry: {new Date(trade.entryDate).toLocaleDateString()}</span>
        {trade.exitDate && (
          <span className="ml-4">
            Exit: {new Date(trade.exitDate).toLocaleDateString()}
          </span>
        )}
      </div>

      {trade.status === "open" && onClose && (
        <button
          onClick={() => onClose(trade)}
          className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          Close Trade
        </button>
      )}
    </div>
  );
};
