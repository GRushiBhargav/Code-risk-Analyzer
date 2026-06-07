import "./App.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import AnalysisDetail from "./pages/AnalysisDetail";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-slate-100">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analysis/:id" element={<AnalysisDetail />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
