import { useState } from "react";
import CameraViewer from "../components/CameraViewer";
import fileToBase64 from "../utils/fileToBase64";
import { detectFromCameraFrame } from "../services/detection.service";

export default function LiveCameraPage() {
  const [lastResult, setLastResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCapture = async (file: File) => {
    setLoading(true);
    setError(null);

    try {
      const base64 = await fileToBase64(file);
      const res = await detectFromCameraFrame(base64);

      setLastResult(res);
    } catch (err: any) {
      setError("Gagal mendeteksi frame kamera");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-5">
      <h1 className="text-2xl font-semibold">Deteksi dari Kamera</h1>

      <CameraViewer onCapture={handleCapture} />

      {loading && <p className="text-blue-600">Memproses...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {lastResult && (
        <div className="p-4 bg-white border rounded shadow space-y-1">
          <p className="font-semibold">
            {lastResult.is_dirty ? "KOTOR ❌" : "BERSIH ✅"}
          </p>
          <p className="text-xs text-slate-600">
            ID event: {lastResult.id}
          </p>
        </div>
      )}
    </div>
  );
}
