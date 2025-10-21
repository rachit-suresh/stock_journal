import axios from "axios";
import { Trade, TradeCreate, TradeClose, Setup, SetupCreate } from "../types";
import { authService } from "../services/auth";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "https://stock-journal-api-8u38.onrender.com";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add JWT token to all requests
apiClient.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle 401 errors (redirect to login)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      authService.logout();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Trades API
export const tradesApi = {
  createTrade: async (trade: TradeCreate): Promise<Trade> => {
    const response = await apiClient.post<Trade>("/api/v1/trades/", trade);
    return response.data;
  },

  getOpenTrades: async (): Promise<Trade[]> => {
    const response = await apiClient.get<Trade[]>("/api/v1/trades/open");
    return response.data;
  },

  getClosedTrades: async (): Promise<Trade[]> => {
    const response = await apiClient.get<Trade[]>("/api/v1/trades/closed");
    return response.data;
  },

  closeTrade: async (
    tradeId: string,
    closeData: TradeClose
  ): Promise<Trade> => {
    const response = await apiClient.put<Trade>(
      `/api/v1/trades/${tradeId}/close`,
      closeData
    );
    return response.data;
  },

  deleteTrade: async (tradeId: string): Promise<void> => {
    await apiClient.delete(`/api/v1/trades/${tradeId}`);
  },

  getStatistics: async (): Promise<{
    total_closed_trades: number;
    winning_trades: number;
    losing_trades: number;
    breakeven_trades: number;
    win_rate: number;
    total_pnl: number;
  }> => {
    const response = await apiClient.get("/api/v1/trades/statistics");
    return response.data;
  },
  getQuote: async (
    ticker: string
  ): Promise<{
    found: boolean;
    price: number | null;
    price_inr: number | null;
    price_usd: number | null;
    exchange_rate: number;
    suggestions: string[];
    warning?: string | null;
    is_adr?: boolean;
  }> => {
    const response = await apiClient.get(`/api/v1/trades/quotes/${ticker}`);
    return response.data;
  },
};

// Setups API
export const setupsApi = {
  createSetup: async (setup: SetupCreate): Promise<Setup> => {
    const response = await apiClient.post<Setup>("/api/v1/setups/", setup);
    return response.data;
  },

  getAllSetups: async (): Promise<Setup[]> => {
    const response = await apiClient.get<Setup[]>("/api/v1/setups/");
    return response.data;
  },
};

export default apiClient;
