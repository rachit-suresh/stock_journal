import axios from 'axios';
import { Trade, TradeCreate, TradeClose, Setup, SetupCreate } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Trades API
export const tradesApi = {
  createTrade: async (trade: TradeCreate): Promise<Trade> => {
    const response = await apiClient.post<Trade>('/api/v1/trades/', trade);
    return response.data;
  },

  getOpenTrades: async (): Promise<Trade[]> => {
    const response = await apiClient.get<Trade[]>('/api/v1/trades/open');
    return response.data;
  },

  getClosedTrades: async (): Promise<Trade[]> => {
    const response = await apiClient.get<Trade[]>('/api/v1/trades/closed');
    return response.data;
  },

  closeTrade: async (tradeId: string, closeData: TradeClose): Promise<Trade> => {
    const response = await apiClient.put<Trade>(`/api/v1/trades/${tradeId}/close`, closeData);
    return response.data;
  },
};

// Setups API
export const setupsApi = {
  createSetup: async (setup: SetupCreate): Promise<Setup> => {
    const response = await apiClient.post<Setup>('/api/v1/setups/', setup);
    return response.data;
  },

  getAllSetups: async (): Promise<Setup[]> => {
    const response = await apiClient.get<Setup[]>('/api/v1/setups/');
    return response.data;
  },
};

export default apiClient;
