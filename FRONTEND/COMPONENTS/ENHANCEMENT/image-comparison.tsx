"use client";

import { useState } from "react";
import { ChevronsLeftRight } from "lucide-react";

interface ImageComparisonProps {
  beforeImage: string; // URL OR BASE64
  afterImage: string; // BASE64
}

export default function ImageComparison({
  beforeImage,
  afterImage,
}: ImageComparisonProps) {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div className="relative w-full aspect-[4/5] md:aspect-video rounded-2xl overflow-hidden border-2 border-border shadow-2xl bg-black select-none group">
      {/* 1. AFTER IMAGE (BACKGROUND LAYER - FULL WIDTH) */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={afterImage}
        alt="RESTORED RESULT"
        className="absolute inset-0 w-full h-full object-contain pointer-events-none"
      />

      {/* LABEL: RESTORED */}
      <div className="absolute top-4 right-4 bg-black/50 backdrop-blur px-3 py-1 rounded text-xs font-bold text-white z-10 pointer-events-none transition-opacity group-hover:opacity-100 opacity-50">
        RESTORED
      </div>

      {/* 2. BEFORE IMAGE (CLIPPED FOREGROUND LAYER) */}
      {/* WE USE CLIP-PATH INSTEAD OF WIDTH SO THE IMAGE ITSELF NEVER RESIZES, ONLY ITS VISIBLE AREA CHANGES */}
      <div
        className="absolute inset-0 w-full h-full"
        style={{
          clipPath: `polygon(0 0, ${sliderPosition}% 0, ${sliderPosition}% 100%, 0 100%)`,
        }}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={beforeImage}
          alt="ORIGINAL INPUT"
          className="absolute inset-0 w-full h-full object-contain pointer-events-none"
        />

        {/* LABEL: ORIGINAL */}
        <div className="absolute top-4 left-4 bg-black/50 backdrop-blur px-3 py-1 rounded text-xs font-bold text-white z-10 pointer-events-none transition-opacity group-hover:opacity-100 opacity-50">
          ORIGINAL
        </div>
      </div>

      {/* 3. SLIDER HANDLE (VISUAL ONLY) */}
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
        className="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-30 m-0 p-0 appearance-none"
      />
    </div>
  );
}
