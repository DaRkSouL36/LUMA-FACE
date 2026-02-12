"use client";

import { useState } from "react";
import Dropzone from "@/COMPONENTS/ENHANCEMENT/dropzone";
import { motion } from "framer-motion";
// NEXT STAGE: IMPORT ResultViewer

export default function EnhancePage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
    // CREATE LOCAL PREVIEW URL
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);

    // TODO: TRIGGER UPLOAD AUTOMATICALLY OR WAIT FOR BUTTON CLICK
    // FOR NOW, WE JUST SET STATE
  };

  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
    setIsProcessing(false); // RESOLVES UNUSED VARIABLE WARNING
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-12">
        {/* HEADER */}
        <div className="text-center space-y-4">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-linear-to-r from-white to-white/60"
          >
            RESTORE IDENTITY. PIXEL BY PIXEL.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-lg text-muted-foreground max-w-2xl mx-auto"
          >
            UPLOAD A LOW-QUALITY, BLURRY, OR OLD FACE IMAGE. OUR AI PIPELINE
            WILL RESTORE DETAILS AND UPSCALE IT BY 4X.
          </motion.p>
        </div>

        {/* UPLOAD AREA */}
        {!file && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Dropzone
              onFileSelect={handleFileSelect}
              isProcessing={isProcessing}
            />
          </motion.div>
        )}

        {/* PREVIEW STATE (TEMPORARY PLACEHOLDER FOR STAGE 9) */}
        {file && previewUrl && (
          <div className="text-center text-green-400">
            FILE SELECTED: {file.name} (READY FOR STAGE 9 INTEGRATION)
            <br />
            <button
              onClick={handleReset}
              className="mt-4 px-4 py-2 bg-white/10 rounded hover:bg-white/20"
            >
              CANCEL / UPLOAD NEW
            </button>
          </div>
        )}
      </div>
    </div>
  );
}