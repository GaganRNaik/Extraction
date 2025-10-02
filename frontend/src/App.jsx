import React from "react";
import { Routes, Route } from "react-router-dom";
// import Topbar from "./components/Topbar";
// import PipelinesList from "./pages/PipelinesList";
import PipelineForm from "./pages/PipelineForm";
// import PipelineDetails from "./pages/PipelineDetails";
// import RunDetails from "./pages/RunDetails";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100">
       {/* <Topbar /> */}
      <main className="max-w-7xl mx-auto py-6"> 
        <Routes>
          {/* <Route path="/" element={<PipelinesList />} /> */}
          <Route path="/create" element={<PipelineForm />} />
          {/* <Route path="/pipelines/:id" element={<PipelineDetails />} />
          <Route path="/runs/:runId" element={<RunDetails />} /> */}
        </Routes>
      </main> 
    </div>
  );
}