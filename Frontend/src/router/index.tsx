import { createBrowserRouter } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

import UploadPage from "../pages/UploadPage";
import LiveCameraPage from "../pages/LiveCameraPage";
import HistoryPage from "../pages/HistoryPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { path: "", element: <UploadPage /> },
      { path: "upload", element: <UploadPage /> },
      { path: "live", element: <LiveCameraPage /> },
      { path: "history", element: <HistoryPage /> },
    ],
  },
]);

export default router;
