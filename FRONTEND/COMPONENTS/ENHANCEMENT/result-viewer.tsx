"use client";

import { Download, RefreshCw } from "lucide-react";
import { motion } from "framer-motion";
import ImageComparison from "./image-comparison";
import MetricsPanel from "./metrics-card";
import { EnhancementResponse } from "@/TYPES/api";

interface ResultViewerProps {
  originalImage: string; 
  result: EnhancementResponse;
  onReset: () => void;
}

export default function ResultViewer({
  originalImage,
  result,
  onReset,
}: ResultViewerProps) {
  // HELPER TO ENSURE VALID BASE64 SRC
  const getResultSrc = () => {
    if (result.image_base64.startsWith("data:image"))
      return result.image_base64;
    return `data:image/jpeg;base64,${result.image_base64}`;
  };

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = getResultSrc();
    link.download = `RESTORED_FACE_${Date.now()}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8 w-full max-w-5xl mx-auto"
    >
      {/* 1. IMAGE COMPARISON AREA */}
      <div className="w-full">
        <ImageComparison
          beforeImage={originalImage}
          afterImage={getResultSrc()}
        />
      </div>

      {/* 2. METRICS PANEL */}
      <div className="space-y-2">
        <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-widest pl-1">
          RESTORATION ANALYTICS
        </h3>
        <MetricsPanel metrics={result.metrics} />
      </div>

      {/* 3. ACTION BUTTONS */}
      <div className="flex flex-col sm:flex-row gap-4 pt-4 border-t border-border">
        <button
          onClick={handleDownload}
          className="flex-1 bg-white text-black font-bold h-12 rounded-lg flex items-center justify-center gap-2 hover:bg-gray-200 transition-colors uppercase"
        >
          <Download className="w-4 h-4" />
          DOWNLOAD RESULT
        </button>

        <button
          onClick={onReset}
          className="flex-1 bg-transparent border border-white/20 text-white font-bold h-12 rounded-lg flex items-center justify-center gap-2 hover:bg-white/5 transition-colors uppercase"
        >
          <RefreshCw className="w-4 h-4" />
          PROCESS NEW IMAGE
        </button>
      </div>
    </motion.div>
  );
}
