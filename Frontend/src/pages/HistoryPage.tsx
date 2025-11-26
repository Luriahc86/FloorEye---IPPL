import { useEffect, useState } from "react";
import axios from "axios";
import HistoryItem from "../components/HistoryItem";

interface HistoryType {
  id: number;
  source: string;
  is_dirty: boolean;
  confidence?: number | null;
  notes?: string | null;
  created_at: string;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);
    const res = await axios.get("http://127.0.0.1:8000/history");
    setHistory(res.data);
    setLoading(false);
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">Riwayat Deteksi</h1>

      {loading && <p>Loading...</p>}

      {!loading && history.length === 0 && (
        <p className="text-slate-500">Belum ada data.</p>
      )}

      <div className="space-y-3">
        {history.map((item) => (
          <HistoryItem key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}
