"use client";
import { useState } from "react";
import { ChevronsLeftRight } from "lucide-react";

interface ImageComparisonProps {
  beforeImage: string; // ORIGINAL
  afterImage: string;  // RESTORED
}

export default function ImageComparison({
  beforeImage,
  afterImage,
}: ImageComparisonProps) {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div className="relative w-full aspect-[4/5] md:aspect-video rounded-2xl overflow-hidden border-2 border-border shadow-2xl bg-black select-none group">
      
      {/* 1. ORIGINAL IMAGE (STATIONARY BACKGROUND) */}
      <img
        src={beforeImage}
        alt="ORIGINAL INPUT"
        className="absolute inset-0 w-full h-full object-contain pointer-events-none"
      />

      {/* LABEL: ORIGINAL (Top Left) */}
      <div className="absolute top-4 left-4 bg-black/50 backdrop-blur px-3 py-1 rounded text-xs font-bold text-white z-10 pointer-events-none transition-opacity group-hover:opacity-100 opacity-50 uppercase">
        Original
      </div>

      {/* 2. RESTORED IMAGE (REVEALING FOREGROUND) */}
      <div
        className="absolute inset-0 w-full h-full"
        style={{
          clipPath: `polygon(0 0, ${sliderPosition}% 0, ${sliderPosition}% 100%, 0 100%)`,
        }}
      >
        <img
          src={afterImage}
          alt="RESTORED RESULT"
          className="absolute inset-0 w-full h-full object-contain pointer-events-none"
        />

        {/* LABEL: RESTORED (Top Right - BACK WHERE YOU WANTED IT) */}
        <div className="absolute top-4 right-4 bg-black/50 backdrop-blur px-3 py-1 rounded text-xs font-bold text-white z-10 pointer-events-none transition-opacity group-hover:opacity-100 opacity-50 uppercase">
          Restored
        </div>
      </div>

      {/* 3. SLIDER HANDLE */}
      <div
        className="absolute top-0 bottom-0 w-1 bg-white z-20 shadow-[0_0_10px_rgba(0,0,0,0.5)] pointer-events-none"
        style={{ left: `${sliderPosition}%` }}
      >
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg text-black transition-transform duration-150 ease-in-out">
          <ChevronsLeftRight
            className={`w-4 h-4 transition-transform ${isDragging ? "scale-75" : "scale-100"}`}
          />
        </div>
      </div>

      {/* 4. INVISIBLE SLIDER OVERLAY */}
      <input
        type="range"
        min="0"
        max="100"
        value={sliderPosition}
        onChange={(e) => setSliderPosition(parseInt(e.target.value))}
        onMouseDown={() => setIsDragging(true)}
        onMouseUp={() => setIsDragging(false)}
        onTouchStart={() => setIsDragging(true)}
        onTouchEnd={() => setIsDragging(false)}
        className="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-30 m-0 p-0 appearance-none"
      />
    </div>
  );
}
