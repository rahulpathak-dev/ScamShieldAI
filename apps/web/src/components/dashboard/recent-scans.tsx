import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { StoredScan } from "@/lib/scan-history";

const toneByRisk = {
  low: "success",
  medium: "warning",
  high: "danger",
  critical: "danger"
} as const;

export function RecentScans({ history }: { history: StoredScan[] }) {
  const recent = history.slice(0, 5);

  return (
    <div className="rounded-md border bg-card p-4 shadow-sm">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-semibold">Recent Scans</h3>
          <p className="text-sm text-muted-foreground">Latest submitted messages</p>
        </div>
        <Button asChild variant="outline" size="sm">
          <Link href="/history">View all</Link>
        </Button>
      </div>

      {recent.length ? (
        <div className="grid gap-3">
          {recent.map((scan) => (
            <div key={scan.id} className="rounded-md border p-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-sm font-medium capitalize">{scan.category}</span>
                <Badge tone={toneByRisk[scan.riskLevel]} className="capitalize">
                  {scan.riskLevel}
                </Badge>
              </div>
              <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">{scan.messagePreview}</p>
              <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
                <span>{scan.sourceType.replaceAll("_", " ")}</span>
                <span>{scan.riskScore.toFixed(0)} risk</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-md border border-dashed p-6 text-sm text-muted-foreground">No scans recorded yet.</div>
      )}
    </div>
  );
}