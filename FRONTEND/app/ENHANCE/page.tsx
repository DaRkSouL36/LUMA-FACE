"use client";

import { useState } from "react";
import Dropzone from "@/COMPONENTS/ENHANCEMENT/dropzone";
import ResultViewer from "@/COMPONENTS/ENHANCEMENT/result-viewer";
import ErrorAlert from "@/COMPONENTS/UI/error-alert";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2 } from "lucide-react";
import { EnhancementResponse } from "@/TYPES/api";
import { enhanceImage, getErrorMessage } from "@/LIB/api";

// WE WILL IMPLEMENT THE ACTUAL API CALL IN STAGE 10
// FOR NOW, THESE ARE PLACEHOLDERS

export default function EnhancePage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<EnhancementResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = async (selectedFile: File) => {
    // 1. RESET STATES
    setError(null);
    setFile(selectedFile);
    setResult(null);

    // 2. CREATE LOCAL PREVIEW
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);

    // 3. START PROCESSING
    setIsProcessing(true);

    try {
      // 4. API CALL
      const data = await enhanceImage(selectedFile);

      if (data.success) {
        setResult(data);
      } else {
        setError(data.message.toUpperCase() || "PROCESSING FAILED");
      }
    } catch (err) {
      const msg = getErrorMessage(err);
      setError(msg);
      // OPTIONAL: CLEAR FILE ON ERROR SO USER CAN TRY AGAIN
      // setFile(null)
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    // CLEANUP MEMORY
    if (previewUrl) URL.revokeObjectURL(previewUrl);

    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setIsProcessing(false);
    setError(null);
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* HEADER - VISIBLE ONLY WHEN IDLE */}
        {!result && !isProcessing && (
          <div className="text-center space-y-4">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-4xl md:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-linear-to-r from-white to-white/60 uppercase"
            >
              RESTORE IDENTITY. PIXEL BY PIXEL.
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-sm md:text-base text-muted-foreground max-w-2xl mx-auto uppercase tracking-wide"
            >
              UPLOAD A LOW-QUALITY IMAGE. OUR AI PIPELINE RESTORES DETAILS AND
              UPSCALES BY 4X.
            </motion.p>
          </div>
        )}

        {/* ERROR ALERT */}
        <AnimatePresence>
          {error && (
            <div className="max-w-xl mx-auto w-full">
              <ErrorAlert message={error} onClose={() => setError(null)} />
            </div>
          )}
        </AnimatePresence>

        {/* LOADING STATE */}
        {isProcessing && !result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center py-20 space-y-6"
          >
            <div className="relative">
              <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full" />
              <Loader2 className="w-16 h-16 text-primary animate-spin relative z-10" />
            </div>

            <div className="text-center space-y-2">
              <p className="text-xl font-bold uppercase tracking-widest animate-pulse text-white">
                RESTORING FACIAL GEOMETRY...
              </p>
              <p className="text-xs text-muted-foreground uppercase tracking-widest">
                RUNNING GFPGAN + REAL-ESRGAN PIPELINE
              </p>
            </div>
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
