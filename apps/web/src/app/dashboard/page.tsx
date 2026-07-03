"use client";

import { AlertTriangle, Activity, Radar, ShieldAlert } from "lucide-react";

import { ProtectedRoute } from "@/components/auth/protected-route";
import { RiskChart } from "@/components/dashboard/risk-chart";
import { RecentScans } from "@/components/dashboard/recent-scans";
import { StatCard } from "@/components/dashboard/stat-card";
import { PageHeading } from "@/components/workspace/page-heading";
import { WorkspaceShell } from "@/components/workspace/workspace-shell";
import { summarizeHistory } from "@/lib/scan-history";
import { useScanHistory } from "@/hooks/use-scan-history";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      {(user) => <DashboardContent user={user} />}
    </ProtectedRoute>
  );
}

function DashboardContent({ user }: { user: Parameters<typeof WorkspaceShell>[0]["user"] }) {
  const history = useScanHistory();
  const stats = summarizeHistory(history);

  return (
    <WorkspaceShell user={user}>
      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <PageHeading title="Dashboard" description="Scan volume, detections, and risk posture" />

        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total scans" value={String(stats.totalScans)} detail="Messages analyzed in this browser workspace" icon={Radar} />
          <StatCard label="Scam detections" value={String(stats.scamDetections)} detail={`${stats.detectionRate}% high or critical rate`} icon={ShieldAlert} />
          <StatCard label="Average risk" value={`${stats.averageRisk}%`} detail="Mean risk score across stored scans" icon={Activity} />
          <StatCard label="Critical scans" value={String(stats.criticalScans)} detail={`${stats.mediumOrAbove} scans are medium risk or above`} icon={AlertTriangle} />
        </div>

        <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_420px]">
          <RiskChart history={history} />
          <RecentScans history={history} />
        </div>
      </section>
    </WorkspaceShell>
  );
}