export async function getHistory() {
  const res = await fetch("http://localhost:5000/history");
  return res.json();
}
