import { Crown } from "lucide-react";
import { cn } from "@/lib/utils";

export function LeaderScoreLabel({ className }: { className?: string }) {
  return (
    <p
      className={cn(
        "mb-1 flex items-center gap-1 text-[10px] font-semibold uppercase tracking-wide text-amber-400",
        className
      )}
    >
      <Crown className="h-3 w-3 shrink-0" aria-hidden />
      Arena leader
    </p>
  );
}
