import { AlertTriangle, X } from "lucide-react";
import { motion } from "framer-motion";

interface ErrorAlertProps {
  message: string;
  onClose: () => void;
}

export default function ErrorAlert({ message, onClose }: ErrorAlertProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="bg-destructive/10 border border-destructive/50 text-destructive p-4 rounded-lg flex items-center justify-between shadow-lg backdrop-blur-sm"
    >
      <div className="flex items-center gap-3">
        <AlertTriangle className="w-5 h-5" />
        <span className="font-bold tracking-wide text-sm">{message}</span>
      </div>
      <button
        onClick={onClose}
        className="p-1 hover:bg-destructive/20 rounded-full transition-colors"
      >
        <X className="w-4 h-4" />
      </button>
    </motion.div>
  );
}
