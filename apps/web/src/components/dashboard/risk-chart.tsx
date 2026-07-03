"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { StoredScan } from "@/lib/scan-history";

export function RiskChart({ history }: { history: StoredScan[] }) {
  const data = [
    { level: "Low", count: history.filter((scan) => scan.riskLevel === "low").length },
    { level: "Medium", count: history.filter((scan) => scan.riskLevel === "medium").length },
    { level: "High", count: history.filter((scan) => scan.riskLevel === "high").length },
    { level: "Critical", count: history.filter((scan) => scan.riskLevel === "critical").length }
  ];

  return (
    <div className="h-72 rounded-md border bg-card p-4 shadow-sm">
      <div className="mb-3">
        <h3 className="text-base font-semibold">Risk Distribution</h3>
        <p className="text-sm text-muted-foreground">Grouped by latest local scan history</p>
      </div>
      <ResponsiveContainer width="100%" height="78%">
        <BarChart data={data} margin={{ left: -20, right: 8, top: 8, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="level" tickLine={false} axisLine={false} />
          <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
          <Tooltip cursor={{ fill: "rgba(20, 184, 166, 0.08)" }} />
          <Bar dataKey="count" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}