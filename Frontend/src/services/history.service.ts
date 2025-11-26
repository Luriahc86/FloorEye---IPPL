import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export interface HistoryItem {
  id: number;
  source: "upload" | "camera";
  is_dirty: boolean;
  confidence?: number | null;
  notes?: string | null;
  created_at: string;
}

export async function getHistory(limit = 50, offset = 0): Promise<HistoryItem[]> {
  const res = await axios.get(`${API_BASE}/history`, {
    params: { limit, offset },
  });
  return res.data;
}

export function getImageUrl(id: number) {
  return `${API_BASE}/image/${id}`;
}
