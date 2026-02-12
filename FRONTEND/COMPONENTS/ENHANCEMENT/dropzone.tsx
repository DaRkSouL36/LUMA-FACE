"use client";

import { useCallback, useState } from "react";
import { useDropzone, FileRejection } from "react-dropzone";
import { UploadCloud, FileWarning, Image as ImageIcon } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface DropzoneProps {
  onFileSelect: (file: File) => void;
  isProcessing: boolean;
}

export default function Dropzone({
  onFileSelect,
  isProcessing,
}: DropzoneProps) {
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[], fileRejections: FileRejection[]) => {
      setError(null);

      if (fileRejections.length > 0) {
        const rejection = fileRejections[0];
        if (rejection.errors[0].code === "file-too-large") {
          setError("FILE IS TOO LARGE. MAX SIZE IS 10MB.");
        } else {
          setError("INVALID FILE TYPE. PLEASE UPLOAD JPEG OR PNG.");
        }
        return;
      }

      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
    [onFileSelect],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/jpeg": [],
      "image/png": [],
    },
    maxSize: 10 * 1024 * 1024,
    multiple: false,
    disabled: isProcessing,
  });

  // CRITICAL FIX: EXCLUDE ALL DRAG HANDLERS TO PREVENT CONFLICTS
  // REACT-DROPZONE GIVES HTML DRAG EVENTS, BUT FRAMER MOTION WANTS ANIMATION EVENTS.
  // WE REMOVE THEM SO THEY DON'T CLASH.
  const {
    onDrag,
    onDragEnter,
    onDragLeave,
    onDragOver,
    onDragStart,
    onDragEnd,
    onDrop: onDropProp,
    ...rootProps
  } = getRootProps();

  return (
    <div className="w-full max-w-xl mx-auto">
      {/* WE APPLY THE DRAG EVENTS TO A PLAIN DIV FIRST, 
         THEN WRAP CONTENT IN MOTION IF NEEDED, OR APPLY MOTION PROPS SEPARATELY.
         BUT THE SIMPLEST FIX FOR THIS SPECIFIC ERROR IS TO SPREAD rootProps 
         ON A STANDARD HTML ELEMENT OR CAREFULLY FILTER PROPS.
         
         BETTER APPROACH: USE A STANDARD DIV FOR THE DROPZONE LOGIC
         AND ANIMATE THE CONTENT INSIDE.
      */}

      <div {...getRootProps()} className="outline-none">
        {/* ^^^ USE STANDARD DIV FOR DROPZONE PROPS TO AVOID CONFLICT COMPLETELY */}

        <motion.div
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.98 }}
          className={`
            relative border-2 border-dashed rounded-2xl p-12 transition-colors cursor-pointer
            flex flex-col items-center justify-center text-center gap-4
            ${isDragActive ? "border-primary bg-primary/5" : "border-white/10 hover:border-white/20 hover:bg-white/5"}
            ${isProcessing ? "opacity-50 cursor-not-allowed" : ""}
            ${error ? "border-destructive/50 bg-destructive/5" : ""}
          `}
        >
          <input {...getInputProps()} />

          <AnimatePresence mode="wait">
            {isDragActive ? (
              <motion.div
                key="active"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="text-primary"
              >
                <UploadCloud className="w-16 h-16 mb-4 mx-auto" />
                <p className="text-lg font-medium">DROP THE IMAGE HERE...</p>
              </motion.div>
            ) : (
              <motion.div
                key="idle"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="text-muted-foreground"
              >
                <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-4">
                  {error ? (
                    <FileWarning className="w-8 h-8 text-destructive" />
                  ) : (
                    <ImageIcon className="w-8 h-8 text-white/40" />
                  )}
                </div>

                <p className="text-lg font-medium text-foreground">
                  {error ? (
                    <span className="text-destructive">{error}</span>
                  ) : (
                    "DRAG & DROP YOUR FACE IMAGE HERE"
                  )}
                </p>
                <p className="text-sm mt-2 opacity-60">
                  SUPPORTS JPG, PNG (MAX 10MB)
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
}
