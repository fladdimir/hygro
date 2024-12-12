import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import Live from "./components/live/Live.tsx";
import { BrowserRouter, Route, Routes } from "react-router";
import History from "./components/history/History.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Live />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
