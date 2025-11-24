import { useEffect, useState } from "react";
import { getHistory } from "../services/history.service";
import HistoryItem from "../components/HistoryItem";

export default function HistoryPage() {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    getHistory().then(setHistory);
  }, []);

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Riwayat Deteksi</h1>
        <p className="text-gray-500 mt-1">
          Daftar hasil deteksi dari upload gambar dan live kamera.
        </p>
      </div>

      {/* If no history */}
      {history.length === 0 && (
        <div className="p-10 text-center bg-white border rounded-xl shadow">
          <p className="text-gray-400">Belum ada riwayat deteksi.</p>
        </div>
      )}

      {/* History list */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {history.map((item, i) => (
          <HistoryItem
            key={i}
            image={item.image}
            timestamp={item.timestamp}
          />
        ))}
      </div>
    </div>
  );
}
