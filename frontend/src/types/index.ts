export interface Trade {
  _id: string;
  ticker: string;
  direction: 'bullish' | 'bearish';
  entryPrice: number;
  stopLoss: number;
  size: number;
  status: 'open' | 'closed';
  entryDate: string;
  exitPrice?: number;
  exitDate?: string;
  marketConditions?: string;
  emotions?: string;
  lessonsLearned?: string;
  result_pnl?: number;
  setup_id?: string;
}

export interface TradeCreate {
  ticker: string;
  direction: 'bullish' | 'bearish';
  entryPrice: number;
  stopLoss: number;
  size: number;
  marketConditions?: string;
  emotions?: string;
  setup_id?: string;
}

export interface TradeClose {
  exitPrice: number;
  lessonsLearned?: string;
}

export interface Setup {
  _id: string;
  name: string;
  notes?: string;
  user_id: string;
}

export interface SetupCreate {
  name: string;
  notes?: string;
}

export interface PriceUpdate {
  type: 'price_update';
  ticker: string;
  price: number;
}

export interface Alert {
  type: 'alert';
  ticker: string;
  trade_id: string;
  message: string;
}

export type WebSocketMessage = PriceUpdate | Alert;
