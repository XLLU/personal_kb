import { API_CONFIG } from "../config/api";

export const apiService = {
  async testConnection() {
    try {
      const response = await fetch("/api/test", {
        method: "GET",
        headers: API_CONFIG.headers,
      });

      if (!response.ok) {
        throw new Error("API connection failed");
      }

      return await response.json();
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },
};
