"use client";

import { useState } from "react";
import Dropzone from "@/COMPONENTS/ENHANCEMENT/dropzone";
import ResultViewer from "@/COMPONENTS/ENHANCEMENT/result-viewer";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2 } from "lucide-react";
import { EnhancementResponse } from "@/TYPES/api";

// WE WILL IMPLEMENT THE ACTUAL API CALL IN STAGE 10
// FOR NOW, THESE ARE PLACEHOLDERS

export default function EnhancePage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<EnhancementResponse | null>(null);

  const handleFileSelect = async (selectedFile: File) => {
    setFile(selectedFile);
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);

    // MOCK API CALL FOR UI TESTING (REMOVED IN STAGE 10)
    setIsProcessing(true);

    // TODO: STAGE 10 - INSERT API CALL HERE
    // await processImage(selectedFile)
  };

  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setIsProcessing(false);
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-12">
        {/* HEADER - HIDDEN WHEN RESULT IS SHOWN TO SAVE SPACE */}
        {!result && (
          <div className="text-center space-y-4">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-4xl md:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-linear-to-r from-white to-white/60 uppercase"
            >
              RESTORE IDENTITY. PIXEL BY PIXEL.
            </motion.h1>
          </div>
        )}

        {/* LOADING STATE */}
        {isProcessing && !result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center py-20 space-y-4"
          >
            <Loader2 className="w-12 h-12 text-primary animate-spin" />
            <p className="text-xl font-bold uppercase tracking-widest animate-pulse">
              RESTORING FACIAL GEOMETRY...
            </p>
            <p className="text-sm text-muted-foreground uppercase">
              RUNNING GFPGAN + REAL-ESRGAN PIPELINE
            </p>
          </motion.div>
        )}

        {/* UPLOAD STATE */}
        {!isProcessing && !result && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <Dropzone
              onFileSelect={handleFileSelect}
              isProcessing={isProcessing}
            />
          </motion.div>
        )}

        {/* RESULT STATE */}
        <AnimatePresence>
          {result && previewUrl && (
            <ResultViewer
              originalImage={previewUrl}
              result={result}
              onReset={handleReset}
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
