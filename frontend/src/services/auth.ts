/**
 * Authentication service for managing JWT tokens and user sessions
 */

const TOKEN_KEY = "trading_journal_token";
const USER_KEY = "trading_journal_user";

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
  email?: string;
}

export interface User {
  user_id: string;
  username: string;
  email?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  private baseUrl = "https://stock-journal-api-8u38.onrender.com";

  /**
   * Get the stored JWT token
   */
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * Store the JWT token
   */
  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  }

  /**
   * Remove the JWT token
   */
  removeToken(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  /**
   * Get the stored user info
   */
  getUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * Store the user info
   */
  setUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  /**
   * Register a new user
   */
  async register(
    username: string,
    password: string,
    email?: string
  ): Promise<User> {
    const response = await fetch(`${this.baseUrl}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password, email }),
    });

    if (!response.ok) {
      const error = await response
        .json()
        .catch(() => ({ detail: "Registration failed" }));
      throw new Error(error.detail || "Registration failed");
    }

    const data: AuthResponse = await response.json();
    this.setToken(data.access_token);

    // Fetch user info
    const user = await this.fetchUserInfo();
    this.setUser(user);

    return user;
  }

  /**
   * Login with username and password
   */
  async login(username: string, password: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const error = await response
        .json()
        .catch(() => ({ detail: "Login failed" }));
      throw new Error(error.detail || "Login failed");
    }

    const data: AuthResponse = await response.json();
    this.setToken(data.access_token);

    // Fetch user info
    const user = await this.fetchUserInfo();
    this.setUser(user);

    return user;
  }

  /**
   * Fetch current user information
   */
  async fetchUserInfo(): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error("No token available");
    }

    const response = await fetch(`${this.baseUrl}/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        this.removeToken();
        throw new Error("Session expired. Please login again.");
      }
      throw new Error("Failed to fetch user info");
    }

    return await response.json();
  }

  /**
   * Logout the current user
   */
  logout(): void {
    this.removeToken();
  }
}

export const authService = new AuthService();
