import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { Outlet } from "react-router-dom";

export default function MainLayout() {
  return (
    <div className="flex h-screen w-full">
      {/* Sidebar Kiri */}
      <Sidebar />

      {/* Konten Kanan */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar />

        <main className="p-6 overflow-y-auto flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
