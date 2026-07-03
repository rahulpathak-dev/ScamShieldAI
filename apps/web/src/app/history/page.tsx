"use client";

import { Trash2 } from "lucide-react";
import { useState } from "react";

import { ProtectedRoute } from "@/components/auth/protected-route";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PageHeading } from "@/components/workspace/page-heading";
import { WorkspaceShell } from "@/components/workspace/workspace-shell";
import { clearScanHistory } from "@/lib/scan-history";
import { useScanHistory } from "@/hooks/use-scan-history";

const toneByRisk = {
  low: "success",
  medium: "warning",
  high: "danger",
  critical: "danger"
} as const;

export default function HistoryPage() {
  return (
    <ProtectedRoute>
      {(user) => <HistoryContent user={user} />}
    </ProtectedRoute>
  );
}

function HistoryContent({ user }: { user: Parameters<typeof WorkspaceShell>[0]["user"] }) {
  const history = useScanHistory();
  const [filter, setFilter] = useState("all");
  const filteredHistory = filter === "all" ? history : history.filter((scan) => scan.riskLevel === filter);

  function handleClear() {
    clearScanHistory();
  }

  return (
    <WorkspaceShell user={user}>
      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <PageHeading
          title="History"
          description="Previous scans stored in this browser workspace"
          action={
            <Button type="button" variant="outline" size="sm" onClick={handleClear} disabled={!history.length}>
              <Trash2 className="h-4 w-4" aria-hidden="true" />
              Clear
            </Button>
          }
        />

        <div className="flex flex-wrap gap-2">
          {["all", "low", "medium", "high", "critical"].map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setFilter(item)}
              className={
                filter === item
                  ? "h-9 rounded-md border border-primary bg-primary px-3 text-sm font-medium capitalize text-primary-foreground"
                  : "h-9 rounded-md border bg-card px-3 text-sm font-medium capitalize text-muted-foreground hover:bg-muted hover:text-foreground"
              }
            >
              {item}
            </button>
          ))}
        </div>

        <div className="overflow-hidden rounded-md border bg-card shadow-sm">
          <div className="hidden grid-cols-[160px_110px_120px_1fr_90px] gap-4 border-b bg-muted/60 px-4 py-3 text-sm font-medium text-muted-foreground md:grid">
            <span>Time</span>
            <span>Risk</span>
            <span>Category</span>
            <span>Message</span>
            <span className="text-right">Score</span>
          </div>

          {filteredHistory.length ? (
            <div className="divide-y">
              {filteredHistory.map((scan) => (
                <div key={scan.id} className="grid gap-3 px-4 py-4 md:grid-cols-[160px_110px_120px_1fr_90px] md:items-center md:gap-4">
                  <span className="text-sm text-muted-foreground">{new Date(scan.createdAt).toLocaleString()}</span>
                  <Badge tone={toneByRisk[scan.riskLevel]} className="w-fit capitalize">
                    {scan.riskLevel}
                  </Badge>
                  <span className="text-sm font-medium capitalize">{scan.category}</span>
                  <div>
                    <p className="line-clamp-2 text-sm text-muted-foreground">{scan.messagePreview}</p>
                    <p className="mt-1 text-xs text-muted-foreground">{scan.sourceType.replaceAll("_", " ")} | {scan.evidenceCount} evidence signals</p>
                  </div>
                  <span className="text-left text-sm font-semibold md:text-right">{scan.riskScore.toFixed(0)}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-8 text-sm text-muted-foreground">No matching scans.</div>
          )}
        </div>
      </section>
    </WorkspaceShell>
  );
}