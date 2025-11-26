src/services/detection.service.ts
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export async function detectFromImage(file: File, notes?: string) {
  const formData = new FormData();
  formData.append("file", file);
  if (notes) formData.append("notes", notes);

  const res = await axios.post(`${API_BASE}/detect/image`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
}

export async function detectFromCameraFrame(imageBase64: string, notes?: string) {
  const res = await axios.post(`${API_BASE}/detect/frame`, {
    image_base64: imageBase64,
    notes,
  });

  return res.data;
}
