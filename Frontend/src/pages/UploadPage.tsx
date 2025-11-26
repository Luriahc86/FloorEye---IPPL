import { useState } from "react";
import ImageUploader from "../components/ImageUploader";
import { detectFromImage } from "../services/detection.service";

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSelectImage = (file: File) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
  };

  const handleDetect = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    try {
      const res = await detectFromImage(selectedFile);
      setResult(res);
    } catch (err: any) {
      setError(err?.detail || "Gagal mendeteksi gambar");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Deteksi dari Upload Gambar</h1>

      <ImageUploader
        onImageSelected={handleSelectImage}
        onDetect={handleDetect}
        loading={loading}
      />

      {error && (
        <p className="p-2 bg-red-100 text-red-700 rounded">{error}</p>
      )}

      {result && (
        <div className="p-4 bg-white rounded shadow border space-y-2">
          <p className="text-sm text-slate-600">
            ID: <span className="font-mono">{result.id}</span>
          </p>

          <p className={`font-semibold ${result.is_dirty ? "text-red-600" : "text-green-600"}`}>
            Status Lantai: {result.is_dirty ? "KOTOR ❌" : "BERSIH ✅"}
          </p>

          {result.notes && (
            <p className="text-sm text-slate-700">Catatan: {result.notes}</p>
          )}
        </div>
      )}
    </div>
  );
}
