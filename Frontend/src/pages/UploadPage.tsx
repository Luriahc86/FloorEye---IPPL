import { useState } from "react";
import ImageUploader from "../components/ImageUploader";
import { uploadImage } from "../services/detection.service";

export default function UploadPage() {
  const [preview, setPreview] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    const url = URL.createObjectURL(file);
    setPreview(url);

    await uploadImage(file);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Upload Gambar</h1>

      <ImageUploader onImageSelected={handleUpload} />

      {preview && (
        <img
          src={preview}
          className="mt-4 w-64 h-64 object-cover rounded shadow"
        />
      )}
    </div>
  );
}
