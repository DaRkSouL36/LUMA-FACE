"use client";

import { Activity, Fingerprint, Layers, Zap } from "lucide-react";
import { EnhancementMetrics } from "@/TYPES/api";

interface MetricsPanelProps {
  metrics: EnhancementMetrics;
}

export default function MetricsPanel({ metrics }: MetricsPanelProps) {
  // HELPER TO DETERMINE COLOR BASED ON QUALITY THRESHOLDS
  const getScoreColor = (
    value: number,
    type: "psnr" | "ssim" | "lpips" | "identity",
  ) => {
    // SIMPLE THRESHOLDING FOR VISUAL FEEDBACK
    if (type === "psnr")
      return value > 30
        ? "text-green-400"
        : value > 25
          ? "text-yellow-400"
          : "text-red-400";
    if (type === "ssim")
      return value > 0.8
        ? "text-green-400"
        : value > 0.7
          ? "text-yellow-400"
          : "text-red-400";
    if (type === "lpips")
      return value < 0.3
        ? "text-green-400"
        : value < 0.5
          ? "text-yellow-400"
          : "text-red-400";
    if (type === "identity")
      return value > 0.6
        ? "text-green-400"
        : value > 0.4
          ? "text-yellow-400"
          : "text-red-400";
    return "text-white";
  };

  const items = [
    {
      label: "PSNR (DB)",
      value: metrics.psnr.toFixed(2),
      icon: Zap,
      color: getScoreColor(metrics.psnr, "psnr"),
      desc: "SIGNAL FIDELITY",
    },
    {
      label: "SSIM",
      value: metrics.ssim.toFixed(3),
      icon: Layers,
      color: getScoreColor(metrics.ssim, "ssim"),
      desc: "STRUCTURAL SIMILARITY",
    },
    {
      label: "LPIPS",
      value: metrics.lpips.toFixed(3),
      icon: Activity,
      color: getScoreColor(metrics.lpips, "lpips"),
      desc: "PERCEPTUAL ERROR",
    },
    {
      label: "IDENTITY",
      value: metrics.identity_score.toFixed(3),
      icon: Fingerprint,
      color: getScoreColor(metrics.identity_score, "identity"),
      desc: "FACE VERIFICATION",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full">
      {items.map((item, idx) => (
        <div
          key={idx}
          className="bg-card border border-border p-4 rounded-xl flex flex-col items-center text-center space-y-2 hover:bg-white/5 transition-colors"
        >
          <div className="p-2 bg-white/5 rounded-full mb-1">
            <item.icon className="w-5 h-5 text-muted-foreground" />
          </div>
          <span className="text-xs font-bold text-muted-foreground tracking-wider">
            {item.label}
          </span>
          <span className={`text-2xl font-mono font-bold ${item.color}`}>
            {item.value}
          </span>
          <span className="text-[10px] text-white/40 uppercase">
            {item.desc}
          </span>
        </div>
      ))}
    </div>
  );
}
