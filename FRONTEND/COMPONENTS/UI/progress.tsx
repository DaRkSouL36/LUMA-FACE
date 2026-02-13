import { HTMLAttributes, forwardRef } from "react";
import { cn } from "./button";

interface ProgressProps extends HTMLAttributes<HTMLDivElement> {
  value: number; // 0 to 100
}

const Progress = forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "relative h-2 w-full overflow-hidden rounded-full bg-zinc-800",
        className,
      )}
      {...props}
    >
      <div
        className="h-full w-full flex-1 bg-white transition-all duration-500 ease-in-out"
        style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
      />
    </div>
  ),
);
Progress.displayName = "Progress";
export { Progress };
