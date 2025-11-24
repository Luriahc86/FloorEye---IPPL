interface Props {
  image: string;
  timestamp: string;
}

export default function HistoryItem({ image, timestamp }: Props) {
  return (
    <div className="p-4 bg-white shadow rounded-lg flex gap-4">
      <img
        src={image}
        alt="Detection history"
        className="w-32 h-32 object-cover rounded"
      />
      <div>
        <p className="font-semibold">Waktu: {timestamp}</p>
      </div>
    </div>
  );
}
