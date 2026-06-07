import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

// Dashboard endpoints
export const getStats = () => api.get("/dashboard/stats").then((r) => r.data);
export const getRiskDistribution = () =>
  api.get("/dashboard/risk-distribution").then((r) => r.data);
//export const getSeverityDist = () =>
 // api.get("/dashboard/severity-distribution").then((r) => r.data);
export const getTopRisky = (limit = 10) =>
  api.get(`/dashboard/top-risky?limit=${limit}`).then((r) => r.data);
export const getRecentActivity = (limit = 15) =>
  api.get(`/dashboard/recent-activity?limit=${limit}`).then((r) => r.data);
export const listAnalyses = (limit = 20, offset = 0) =>
  api
    .get(`/dashboard/analyses?limit=${limit}&offset=${offset}`)
    .then((r) => r.data);
export const getAnalysisDetails = (id) =>
  api.get(`/dashboard/analyses/${id}`).then((r) => r.data);

export default api;
