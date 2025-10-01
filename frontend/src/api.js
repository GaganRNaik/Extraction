import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const api = axios.create({ baseURL: API_BASE, timeout: 30000 });

export async function listPipelines() {
  const resp = await api.get("/pipelines");
  return resp.data;
}

export async function createPipeline(payload) {
  const resp = await api.post("/pipelines", payload);
  return resp.data;
}

export async function triggerRun(pipelineId) {
  const resp = await api.post(`/pipelines/${pipelineId}/run?async_mode=true`);
  return resp.data;
}

export async function getRun(runId) {
  const resp = await api.get(`/runs/${runId}`);
  return resp.data;
}

export async function getPipeline(pipelineId) {
  const resp = await api.get(`/pipelines`); // backend doesn't have get by id in example
  const all = resp.data;
  return all.find((p) => p.id === pipelineId);
}
