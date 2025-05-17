import axios from 'axios';

// Example base URL (adjust as needed)
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Types
export interface SystemSettings {
  maxBots: number;
  maxAllocationPerBot: number;
  updateInterval: number;
  riskLevel: 'low' | 'medium' | 'high';
  autoReinvest: boolean;
  emergencyStop: boolean;
}

export interface SystemLog {
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
}

export interface FundSummary {
  totalBalance: number;
  availableFunds: number;
  allocatedFunds: number;
}

export interface FundTransaction {
  id: string;
  timestamp: string;
  type: 'deposit' | 'withdrawal' | 'transfer';
  amount: number;
  status: 'pending' | 'completed' | 'failed';
  from: string;
  to: string;
}

// API functions
export const getSystemSettings = async (): Promise<SystemSettings> => {
  const res = await axios.get(`${BASE_URL}/admin/settings`);
  return res.data as SystemSettings;
};

export const updateSystemSettings = async (settings: SystemSettings) => {
  return axios.put(`${BASE_URL}/admin/settings`, settings);
};

export const getSystemLogs = async (): Promise<SystemLog[]> => {
  const res = await axios.get(`${BASE_URL}/admin/logs`);
  return res.data as SystemLog[];
};

export const clearSystemLogs = async () => {
  return axios.post(`${BASE_URL}/admin/logs/clear`);
};

export const getFundSummary = async (): Promise<FundSummary> => {
  const res = await axios.get(`${BASE_URL}/admin/funds/summary`);
  return res.data as FundSummary;
};

export const getFundTransactions = async (): Promise<FundTransaction[]> => {
  const res = await axios.get(`${BASE_URL}/admin/funds/transactions`);
  return res.data as FundTransaction[];
};

export const depositFunds = async (amount: number) => {
  return axios.post(`${BASE_URL}/admin/funds/deposit`, { amount });
};

export const withdrawFunds = async (amount: number) => {
  return axios.post(`${BASE_URL}/admin/funds/withdraw`, { amount });
};

export const transferFunds = async (from: string, to: string, amount: number) => {
  return axios.post(`${BASE_URL}/admin/funds/transfer`, { from, to, amount });
}; 