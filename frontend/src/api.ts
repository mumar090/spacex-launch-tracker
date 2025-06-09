import axios from "axios";

const BASE_URL = "http://localhost:8000";

export interface Launch {
  id: string;
  name: string;
  date_utc: string;
  success: boolean | null;
  rocket: string;
  launchpad: string;
}

export interface StatisticsResponse {
  success_rate_by_rocket: Record<string, number>;
  launch_count_by_launchpad: Record<string, number>;
  launch_frequency: {
    monthly: Record<string, number>;
    yearly: Record<string, number>;
  };
}

// Fetch all launches
export const fetchLaunches = async (): Promise<Launch[]> => {
  const response = await axios.get(`${BASE_URL}/launches`);
  return response.data.launches;
};

// Fetch statistics
export const fetchStatistics = async (): Promise<StatisticsResponse> => {
  const response = await axios.get(`${BASE_URL}/statistics`);
  return response.data;
};
