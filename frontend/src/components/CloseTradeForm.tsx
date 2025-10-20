import { useState } from "react";
import { Trade, TradeClose } from "../types";
import { X } from "lucide-react";

interface CloseTradeFormProps {
  trade: Trade;
  onSubmit: (closeData: TradeClose) => void;
  onCancel: () => void;
}

export const CloseTradeForm = ({
  trade,
  onSubmit,
  onCancel,
}: CloseTradeFormProps) => {
  const [formData, setFormData] = useState<TradeClose>({
    exitPrice: 0,
    lessonsLearned: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const potentialPnL = (formData.exitPrice - trade.entryPrice) * trade.size;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-lg w-full">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Close Trade: {trade.ticker}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-500">Entry Price</p>
                <p className="font-semibold">
                  ₹
                  {trade.entryPrice.toLocaleString("en-IN", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </p>
              </div>
              <div>
                <p className="text-gray-500">Size</p>
                <p className="font-semibold">{trade.size} shares</p>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Exit Price *
              </label>
              <input
                type="number"
                required
                step="0.01"
                value={formData.exitPrice || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    exitPrice: parseFloat(e.target.value),
                  })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="155.00"
              />
            </div>

            {formData.exitPrice > 0 && (
              <div
                className={`p-4 rounded-lg ${
                  potentialPnL > 0 ? "bg-green-50" : "bg-red-50"
                }`}
              >
                <p className="text-sm text-gray-700 mb-1">Projected P&L</p>
                <p
                  className={`text-2xl font-bold ${
                    potentialPnL > 0 ? "text-green-600" : "text-red-600"
                  }`}
                >
                  ₹
                  {potentialPnL.toLocaleString("en-IN", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </p>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Lessons Learned
              </label>
              <textarea
                value={formData.lessonsLearned}
                onChange={(e) =>
                  setFormData({ ...formData, lessonsLearned: e.target.value })
                }
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="What did you learn from this trade?"
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
                Close Trade
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
