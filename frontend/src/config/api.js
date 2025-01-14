// API Key 配置
export const API_CONFIG = {
  headers: {
    "Content-Type": "application/json",
    "X-API-Key": import.meta.env.VITE_DEEPSEEK_API_KEY || "",
  },
};
