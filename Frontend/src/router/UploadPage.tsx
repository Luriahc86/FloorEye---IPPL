import { useState } from "react";

interface DetectResponse {
  dirty: boolean;
}

export default function UploadPage() {
  const [result, setResult] = useState<DetectResponse | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/detect-image", {
      method: "POST",
      body: formData,
    });

    const data: DetectResponse = await res.json();
    setResult(data);
  };

  return (
    <div>
      <h1>Upload Image</h1>
      <input type="file" onChange={handleUpload} />

      {result && (
        <p>
          Hasil Deteksi: {result.dirty ? "🔴 Lantai Kotor" : "🟢 Lantai Bersih"}
        </p>
      )}
    </div>
  );
}
