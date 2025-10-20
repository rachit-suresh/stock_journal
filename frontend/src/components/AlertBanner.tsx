import { Alert } from '../types';
import { AlertTriangle, X } from 'lucide-react';

interface AlertBannerProps {
  alert: Alert;
  onDismiss: () => void;
}

export const AlertBanner = ({ alert, onDismiss }: AlertBannerProps) => {
  return (
    <div className="fixed top-4 right-4 max-w-md w-full bg-red-50 border-l-4 border-red-500 rounded-lg shadow-lg z-50 animate-slide-in">
      <div className="p-4">
        <div className="flex items-start">
          <AlertTriangle className="w-6 h-6 text-red-500 mr-3 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="text-sm font-medium text-red-800">Stop Loss Alert</h3>
            <p className="mt-1 text-sm text-red-700">{alert.message}</p>
            <p className="mt-2 text-xs text-red-600">Ticker: {alert.ticker}</p>
          </div>
          <button
            onClick={onDismiss}
            className="ml-3 flex-shrink-0 text-red-400 hover:text-red-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};
