import { WebSocketMessage, PriceUpdate, Alert } from '../types';

type MessageHandler = (message: WebSocketMessage) => void;
type PriceHandler = (update: PriceUpdate) => void;
type AlertHandler = (alert: Alert) => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private messageHandlers: MessageHandler[] = [];
  private priceHandlers: PriceHandler[] = [];
  private alertHandlers: AlertHandler[] = [];
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private userId: string;
  private wsUrl: string;

  constructor(userId: string, baseUrl?: string) {
    this.userId = userId;
    const base = baseUrl || import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';
    this.wsUrl = `${base}/ws/${userId}`;
  }

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      this.ws = new WebSocket(this.wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          
          // Notify all message handlers
          this.messageHandlers.forEach(handler => handler(message));

          // Notify specific handlers
          if (message.type === 'price_update') {
            this.priceHandlers.forEach(handler => handler(message));
          } else if (message.type === 'alert') {
            this.alertHandlers.forEach(handler => handler(message));
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      this.attemptReconnect();
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }

    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectAttempts++;

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
    this.reconnectTimeout = setTimeout(() => {
      this.connect();
    }, delay);
  }

  subscribe(tickers: string[]) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        tickers,
      }));
    } else {
      console.warn('WebSocket not connected. Cannot subscribe.');
    }
  }

  onMessage(handler: MessageHandler) {
    this.messageHandlers.push(handler);
  }

  onPriceUpdate(handler: PriceHandler) {
    this.priceHandlers.push(handler);
  }

  onAlert(handler: AlertHandler) {
    this.alertHandlers.push(handler);
  }

  removeMessageHandler(handler: MessageHandler) {
    this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
  }

  removePriceHandler(handler: PriceHandler) {
    this.priceHandlers = this.priceHandlers.filter(h => h !== handler);
  }

  removeAlertHandler(handler: AlertHandler) {
    this.alertHandlers = this.alertHandlers.filter(h => h !== handler);
  }

  disconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// Singleton instance
let wsService: WebSocketService | null = null;

export const getWebSocketService = (userId: string = 'static_user_id'): WebSocketService => {
  if (!wsService) {
    wsService = new WebSocketService(userId);
  }
  return wsService;
};
