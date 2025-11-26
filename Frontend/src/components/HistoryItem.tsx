interface Props {
  item: {
    id: number;
    source: string;
    is_dirty: boolean;
    confidence?: number | null;
    notes?: string | null;
    created_at: string;
  };
}

export default function HistoryItem({ item }: Props) {
  return (
    <div className="p-4 bg-white shadow rounded-lg flex gap-4">
      <img
        src={`http://127.0.0.1:8000/image/${item.id}`}
        alt="History"
        className="w-32 h-32 object-cover rounded"
      />

      <div>
        <p className="font-semibold text-lg">
          {item.is_dirty ? "KOTOR ❌" : "BERSIH ✅"}
        </p>
        <p className="text-sm text-slate-700">Sumber: {item.source}</p>
        <p className="text-sm text-slate-700">Waktu: {item.created_at}</p>

        {item.notes && (
          <p className="text-sm text-slate-600 mt-1">Catatan: {item.notes}</p>
        )}
      </div>
    </div>
  );
}
