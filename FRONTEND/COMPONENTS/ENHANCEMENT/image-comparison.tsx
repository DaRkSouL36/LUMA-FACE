"use client";

import { useState } from "react";
import { ChevronsLeftRight } from "lucide-react";

interface ImageComparisonProps {
  beforeImage: string; // URL or Base64
  afterImage: string; // Base64
}

export default function ImageComparison({
  beforeImage,
  afterImage,
}: ImageComparisonProps) {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div className="relative w-full aspect-[4/5] md:aspect-video rounded-2xl overflow-hidden border-2 border-border shadow-2xl bg-black">
      {/* 1. AFTER IMAGE (BACKGROUND LAYER) */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={afterImage}
        alt="Restored Result"
        className="absolute top-0 left-0 w-full h-full object-contain"
      />

      {/* LABEL: RESTORED */}
      <div className="absolute top-4 right-4 bg-black/50 backdrop-blur px-3 py-1 rounded text-xs font-bold text-white z-10 pointer-events-none">
        RESTORED
      </div>

      {/* 2. BEFORE IMAGE (CLIPPED FOREGROUND LAYER) */}
      <div
        className="absolute top-0 left-0 h-full overflow-hidden"
        style={{ width: `${sliderPosition}%` }}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={beforeImage}
          alt="Original Input"
          className="absolute top-0 left-0 w-full h-full max-w-none object-contain"
          // WE MUST SET WIDTH TO THE PARENT CONTAINER WIDTH TO MAINTAIN ASPECT RATIO
          // THIS IS TRICKY IN CSS, BUT object-contain HELPS
          style={{ width: "100vw", maxWidth: "100%" }}
        />

        {/* LABEL: ORIGINAL */}
        <div className="absolute top-4 left-4 bg-black/50 backdrop-blur px-3 py-1 rounded text-xs font-bold text-white z-10 pointer-events-none">
          ORIGINAL
        </div>
      </div>

      {/* 3. SLIDER HANDLE (VISUAL ONLY) */}
      <div
        className="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize z-20 shadow-[0_0_10px_rgba(0,0,0,0.5)]"
        style={{ left: `${sliderPosition}%` }}
      >
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg text-black">
          <ChevronsLeftRight className="w-4 h-4" />
        </div>
      </div>

      {/* 4. INTERACTIVE RANGE INPUT (INVISIBLE OVERLAY) */}
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
        className="absolute top-0 left-0 w-full h-full opacity-0 cursor-ew-resize z-30 m-0 p-0 appearance-none"
      />
    </div>
  );
}
