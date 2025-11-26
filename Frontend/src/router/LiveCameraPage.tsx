import { useEffect, useState } from "react";

export default function LiveCameraPage() {
  const [frame, setFrame] = useState<string>("");

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:8000/camera-frame");
      const data = await res.json();

      setFrame("data:image/jpeg;base64," + data.frame);
    }, 200);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Live Camera</h1>
      {frame && <img src={frame} alt="Live Camera" />}
    </div>
  );
}
