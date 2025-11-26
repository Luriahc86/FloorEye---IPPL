import { useState } from "react";

interface Props {
  onImageSelected: (file: File) => void;
  onDetect?: () => void; // optional callback jika mau melakukan deteksi dari parent
}

export default function ImageUploader({ onImageSelected, onDetect }: Props) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      onImageSelected(file);
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-white shadow space-y-3">
      <label className="block text-sm font-medium">Pilih Gambar</label>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="w-full"
      />

      <button
        onClick={onDetect}
        disabled={!selectedFile}
        className={`px-4 py-2 rounded-md text-white transition 
          ${selectedFile ? "bg-blue-600 hover:bg-blue-700" : "bg-gray-400 cursor-not-allowed"}
        `}
      >
        Deteksi Gambar
      </button>
    </div>
  );
}
