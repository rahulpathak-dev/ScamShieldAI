import type { LucideIcon } from "lucide-react";

export function StatCard({ label, value, detail, icon: Icon }: { label: string; value: string; detail: string; icon: LucideIcon }) {
  return (
    <div className="rounded-md border bg-card p-4 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm text-muted-foreground">{label}</p>
          <p className="mt-2 text-3xl font-semibold leading-none">{value}</p>
        </div>
        <div className="flex h-10 w-10 items-center justify-center rounded-md bg-secondary text-primary">
          <Icon className="h-5 w-5" aria-hidden="true" />
        </div>
      </div>
      <p className="mt-4 text-sm text-muted-foreground">{detail}</p>
    </div>
  );
}