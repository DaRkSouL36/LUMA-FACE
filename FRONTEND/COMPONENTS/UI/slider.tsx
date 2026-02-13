import { InputHTMLAttributes, forwardRef } from "react";
import { cn } from "./button";

interface SliderProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  valueDisplay?: string | number;
}

const Slider = forwardRef<HTMLInputElement, SliderProps>(
  ({ className, label, valueDisplay, ...props }, ref) => {
    return (
      <div className="w-full space-y-2">
        {(label || valueDisplay) && (
          <div className="flex justify-between text-xs uppercase tracking-wider text-zinc-500 font-bold">
            <span>{label}</span>
            <span>{valueDisplay}</span>
          </div>
        )}
        <input
          type="range"
          ref={ref}
          className={cn(
            "w-full h-2 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-white hover:accent-zinc-300 transition-all focus:outline-none focus:ring-2 focus:ring-white/20",
            className,
          )}
          {...props}
        />
      </div>
    );
  },
);
Slider.displayName = "Slider";
export { Slider };
