"use client";

import { useMemo, useState, type ReactNode } from "react";
import {
  Activity,
  BarChart3,
  BrainCircuit,
  DatabaseZap,
  FileClock,
  Filter,
  Gauge,
  Globe2,
  LockKeyhole,
  Search,
  ShieldAlert,
  Users,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { LogoutButton } from "@/components/auth/logout-button";
import { ProtectedRoute } from "@/components/auth/protected-route";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const tabs = [
  { id: "overview", label: "Overview", icon: BarChart3 },
  { id: "users", label: "Users", icon: Users },
  { id: "threats", label: "Threat Intel", icon: DatabaseZap },
  { id: "models", label: "Models", icon: BrainCircuit },
  { id: "logs", label: "Logs", icon: FileClock },
] as const;

type AdminTab = (typeof tabs)[number]["id"];

const summaryStats = [
  {
    label: "Total users",
    value: "12,840",
    change: "+8.2%",
    icon: Users,
    tone: "text-cyan-700",
  },
  {
    label: "Scam detections",
    value: "48,219",
    change: "+14.7%",
    icon: ShieldAlert,
    tone: "text-rose-700",
  },
  {
    label: "Active threats",
    value: "1,428",
    change: "+6.1%",
    icon: Globe2,
    tone: "text-amber-700",
  },
  {
    label: "Model F1 score",
    value: "94.8%",
    change: "+1.9%",
    icon: Gauge,
    tone: "text-emerald-700",
  },
];

const scamCategories = [
  { name: "Phishing", value: 34, color: "#0f766e" },
  { name: "Investment", value: 22, color: "#d97706" },
  { name: "Crypto", value: 18, color: "#dc2626" },
  { name: "Romance", value: 12, color: "#2563eb" },
  { name: "Job", value: 8, color: "#7c3aed" },
  { name: "Lottery", value: 6, color: "#475569" },
];

const attackTrends = [
  { day: "Mon", phishing: 122, investment: 74, crypto: 58 },
  { day: "Tue", phishing: 148, investment: 82, crypto: 66 },
  { day: "Wed", phishing: 133, investment: 93, crypto: 71 },
  { day: "Thu", phishing: 171, investment: 105, crypto: 88 },
  { day: "Fri", phishing: 196, investment: 118, crypto: 104 },
  { day: "Sat", phishing: 162, investment: 109, crypto: 97 },
  { day: "Sun", phishing: 184, investment: 121, crypto: 111 },
];

const riskDistribution = [
  { level: "Safe", count: 18420 },
  { level: "Suspicious", count: 21360 },
  { level: "Dangerous", count: 8440 },
];

const users = [
  { name: "Aarav Sharma", email: "aarav@example.com", role: "USER", status: "Active", scans: 124, risk: "Medium" },
  { name: "Maya Chen", email: "maya.chen@example.com", role: "ANALYST", status: "Active", scans: 641, risk: "Low" },
  { name: "Rohan Mehta", email: "rohan@example.com", role: "USER", status: "Review", scans: 38, risk: "High" },
  { name: "Nia Patel", email: "nia.patel@example.com", role: "ADMIN", status: "Active", scans: 214, risk: "Low" },
  { name: "Ethan Brooks", email: "ethan@example.com", role: "USER", status: "Locked", scans: 9, risk: "High" },
];

const threatIntel = [
  { type: "URL", indicator: "secure-bank-verify.example", severity: "Critical", confidence: "98%", lastSeen: "12 min ago" },
  { type: "Phone", indicator: "+1 202 555 0148", severity: "High", confidence: "91%", lastSeen: "27 min ago" },
  { type: "Keyword", indicator: "wallet recovery fee", severity: "Medium", confidence: "83%", lastSeen: "1 hr ago" },
  { type: "URL", indicator: "crypto-airdrop-claim.example", severity: "High", confidence: "94%", lastSeen: "2 hrs ago" },
  { type: "Sender", indicator: "support@banking-alert.example", severity: "Critical", confidence: "97%", lastSeen: "3 hrs ago" },
];

const modelMetrics = [
  { model: "ScamShield TF-IDF LR", accuracy: 91.2, precision: 90.4, recall: 88.7, f1: 89.5, status: "Stable" },
  { model: "ScamShield SVM", accuracy: 92.8, precision: 93.1, recall: 89.8, f1: 91.4, status: "Stable" },
  { model: "ScamShield BERT", accuracy: 95.3, precision: 94.7, recall: 95.1, f1: 94.9, status: "Primary" },
  { model: "Persuasion Classifier", accuracy: 89.6, precision: 88.9, recall: 86.4, f1: 87.6, status: "Watch" },
];

const logs = [
  { time: "10:48:22", level: "Info", event: "Threat database sync completed", actor: "system", ip: "10.0.2.14" },
  { time: "10:41:09", level: "Warn", event: "High-risk scan burst detected", actor: "risk-engine", ip: "10.0.4.22" },
  { time: "10:36:51", level: "Info", event: "Admin user exported report", actor: "nia.patel@example.com", ip: "203.0.113.42" },
  { time: "10:21:33", level: "Error", event: "Model registry latency threshold exceeded", actor: "model-monitor", ip: "10.0.8.19" },
  { time: "10:12:18", level: "Info", event: "Analyst added malicious URL indicator", actor: "maya.chen@example.com", ip: "198.51.100.16" },
];

const roleTone = {
  ADMIN: "danger",
  ANALYST: "warning",
  USER: "neutral",
} as const;

const statusTone = {
  Active: "success",
  Review: "warning",
  Locked: "danger",
  Stable: "success",
  Primary: "success",
  Watch: "warning",
} as const;

const severityTone = {
  Critical: "danger",
  High: "danger",
  Medium: "warning",
  Low: "success",
} as const;

const logTone = {
  Info: "neutral",
  Warn: "warning",
  Error: "danger",
} as const;

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<AdminTab>("overview");

  const dangerousShare = useMemo(() => {
    const total = riskDistribution.reduce((sum, item) => sum + item.count, 0);
    const dangerous = riskDistribution.find((item) => item.level === "Dangerous")?.count ?? 0;
    return Math.round((dangerous / total) * 100);
  }, []);

  return (
    <ProtectedRoute allowedRoles={["ADMIN"]}>
      {(user) => (
        <main className="min-h-screen bg-slate-950 text-slate-100">
          <div className="border-b border-white/10 bg-slate-950/95">
            <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-5 sm:px-6 lg:px-8">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-lg border border-cyan-400/30 bg-cyan-400/10">
                    <LockKeyhole className="h-5 w-5 text-cyan-200" aria-hidden="true" />
                  </div>
                  <div>
                    <h1 className="text-xl font-semibold tracking-normal text-white sm:text-2xl">ScamShieldAI Admin</h1>
                    <p className="text-sm text-slate-400">Signed in as {user.email}</p>
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <Button variant="secondary" className="border-white/10 bg-white/10 text-white hover:bg-white/15">
                    <Filter className="mr-2 h-4 w-4" aria-hidden="true" />
                    Last 7 days
                  </Button>
                  <LogoutButton />
                </div>
              </div>

              <nav className="flex gap-2 overflow-x-auto pb-1" aria-label="Admin sections">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  const selected = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      type="button"
                      onClick={() => setActiveTab(tab.id)}
                      className={cn(
                        "flex h-10 shrink-0 items-center gap-2 rounded-lg border px-3 text-sm font-medium transition",
                        selected
                          ? "border-cyan-300/60 bg-cyan-300/15 text-cyan-100"
                          : "border-white/10 bg-white/[0.03] text-slate-300 hover:border-white/20 hover:bg-white/[0.07]",
                      )}
                    >
                      <Icon className="h-4 w-4" aria-hidden="true" />
                      {tab.label}
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>

          <div className="mx-auto max-w-7xl space-y-6 px-4 py-6 sm:px-6 lg:px-8">
            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {summaryStats.map((stat) => {
                const Icon = stat.icon;
                return (
                  <div key={stat.label} className="rounded-lg border border-white/10 bg-white/[0.04] p-4 shadow-sm shadow-black/20">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <p className="text-sm text-slate-400">{stat.label}</p>
                        <p className="mt-2 text-2xl font-semibold text-white">{stat.value}</p>
                      </div>
                      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/10">
                        <Icon className={cn("h-5 w-5", stat.tone)} aria-hidden="true" />
                      </div>
                    </div>
                    <p className="mt-3 text-xs text-emerald-300">{stat.change} from previous window</p>
                  </div>
                );
              })}
            </section>

            {activeTab === "overview" && <OverviewSection dangerousShare={dangerousShare} />}
            {activeTab === "users" && <UsersSection />}
            {activeTab === "threats" && <ThreatIntelSection />}
            {activeTab === "models" && <ModelMonitoringSection />}
            {activeTab === "logs" && <LogsSection />}
          </div>
        </main>
      )}
    </ProtectedRoute>
  );
}

function OverviewSection({ dangerousShare }: { dangerousShare: number }) {
  return (
    <section className="grid gap-6 xl:grid-cols-[1.35fr_0.9fr]">
      <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
        <div className="mb-4 flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-base font-semibold text-white">Attack trends</h2>
            <p className="text-sm text-slate-400">Weekly scam volume by leading category</p>
          </div>
          <Badge tone="danger">{dangerousShare}% dangerous</Badge>
        </div>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={attackTrends} margin={{ top: 10, right: 12, left: -12, bottom: 0 }}>
              <CartesianGrid stroke="rgba(148, 163, 184, 0.16)" vertical={false} />
              <XAxis dataKey="day" stroke="#94a3b8" tickLine={false} axisLine={false} />
              <YAxis stroke="#94a3b8" tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8 }} />
              <Legend />
              <Line type="monotone" dataKey="phishing" stroke="#22d3ee" strokeWidth={3} dot={false} />
              <Line type="monotone" dataKey="investment" stroke="#f59e0b" strokeWidth={3} dot={false} />
              <Line type="monotone" dataKey="crypto" stroke="#fb7185" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
        <h2 className="text-base font-semibold text-white">Scam categories</h2>
        <p className="text-sm text-slate-400">Distribution across confirmed detections</p>
        <div className="mt-4 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={scamCategories} dataKey="value" nameKey="name" innerRadius={62} outerRadius={106} paddingAngle={3}>
                {scamCategories.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8 }} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="rounded-lg border border-white/10 bg-white/[0.04] p-4 xl:col-span-2">
        <h2 className="text-base font-semibold text-white">Risk distribution</h2>
        <p className="text-sm text-slate-400">Scan outcomes grouped by scoring band</p>
        <div className="mt-4 h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={riskDistribution} margin={{ top: 10, right: 12, left: -12, bottom: 0 }}>
              <CartesianGrid stroke="rgba(148, 163, 184, 0.16)" vertical={false} />
              <XAxis dataKey="level" stroke="#94a3b8" tickLine={false} axisLine={false} />
              <YAxis stroke="#94a3b8" tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8 }} />
              <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                <Cell fill="#10b981" />
                <Cell fill="#f59e0b" />
                <Cell fill="#ef4444" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  );
}

function UsersSection() {
  return (
    <section className="rounded-lg border border-white/10 bg-white/[0.04]">
      <div className="flex flex-col gap-3 border-b border-white/10 p-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-base font-semibold text-white">User management</h2>
          <p className="text-sm text-slate-400">Accounts, roles, status, and investigation posture</p>
        </div>
        <div className="flex min-w-0 items-center gap-2 rounded-lg border border-white/10 bg-slate-950/60 px-3 py-2 text-sm text-slate-400 md:w-72">
          <Search className="h-4 w-4 shrink-0" aria-hidden="true" />
          <span className="truncate">Search users</span>
        </div>
      </div>
      <ResponsiveTable>
        <thead>
          <tr className="text-left text-xs uppercase tracking-wide text-slate-500">
            <th className="px-4 py-3 font-medium">User</th>
            <th className="px-4 py-3 font-medium">Role</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Scans</th>
            <th className="px-4 py-3 font-medium">Risk</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/10">
          {users.map((item) => (
            <tr key={item.email} className="text-sm text-slate-200">
              <td className="px-4 py-4">
                <div className="font-medium text-white">{item.name}</div>
                <div className="text-xs text-slate-400">{item.email}</div>
              </td>
              <td className="px-4 py-4"><Badge tone={roleTone[item.role as keyof typeof roleTone]}>{item.role}</Badge></td>
              <td className="px-4 py-4"><Badge tone={statusTone[item.status as keyof typeof statusTone]}>{item.status}</Badge></td>
              <td className="px-4 py-4">{item.scans}</td>
              <td className="px-4 py-4">{item.risk}</td>
            </tr>
          ))}
        </tbody>
      </ResponsiveTable>
    </section>
  );
}

function ThreatIntelSection() {
  return (
    <section className="rounded-lg border border-white/10 bg-white/[0.04]">
      <div className="flex flex-col gap-3 border-b border-white/10 p-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-base font-semibold text-white">Threat intelligence</h2>
          <p className="text-sm text-slate-400">Malicious URLs, phone numbers, sender identities, and campaign keywords</p>
        </div>
        <Button className="bg-cyan-500 text-slate-950 hover:bg-cyan-400">
          <DatabaseZap className="mr-2 h-4 w-4" aria-hidden="true" />
          Add indicator
        </Button>
      </div>
      <ResponsiveTable>
        <thead>
          <tr className="text-left text-xs uppercase tracking-wide text-slate-500">
            <th className="px-4 py-3 font-medium">Type</th>
            <th className="px-4 py-3 font-medium">Indicator</th>
            <th className="px-4 py-3 font-medium">Severity</th>
            <th className="px-4 py-3 font-medium">Confidence</th>
            <th className="px-4 py-3 font-medium">Last seen</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/10">
          {threatIntel.map((item) => (
            <tr key={`${item.type}-${item.indicator}`} className="text-sm text-slate-200">
              <td className="px-4 py-4">{item.type}</td>
              <td className="px-4 py-4 font-mono text-xs text-cyan-100">{item.indicator}</td>
              <td className="px-4 py-4"><Badge tone={severityTone[item.severity as keyof typeof severityTone]}>{item.severity}</Badge></td>
              <td className="px-4 py-4">{item.confidence}</td>
              <td className="px-4 py-4 text-slate-400">{item.lastSeen}</td>
            </tr>
          ))}
        </tbody>
      </ResponsiveTable>
    </section>
  );
}

function ModelMonitoringSection() {
  return (
    <section className="grid gap-6 lg:grid-cols-2">
      {modelMetrics.map((model) => (
        <div key={model.model} className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-base font-semibold text-white">{model.model}</h2>
              <p className="text-sm text-slate-400">Accuracy, precision, recall, and F1 monitoring</p>
            </div>
            <Badge tone={statusTone[model.status as keyof typeof statusTone]}>{model.status}</Badge>
          </div>
          <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Metric label="Accuracy" value={model.accuracy} />
            <Metric label="Precision" value={model.precision} />
            <Metric label="Recall" value={model.recall} />
            <Metric label="F1" value={model.f1} />
          </div>
        </div>
      ))}
    </section>
  );
}

function LogsSection() {
  return (
    <section className="rounded-lg border border-white/10 bg-white/[0.04]">
      <div className="flex items-center gap-3 border-b border-white/10 p-4">
        <Activity className="h-5 w-5 text-cyan-200" aria-hidden="true" />
        <div>
          <h2 className="text-base font-semibold text-white">System logs</h2>
          <p className="text-sm text-slate-400">Security, model, analyst, and platform events</p>
        </div>
      </div>
      <ResponsiveTable>
        <thead>
          <tr className="text-left text-xs uppercase tracking-wide text-slate-500">
            <th className="px-4 py-3 font-medium">Time</th>
            <th className="px-4 py-3 font-medium">Level</th>
            <th className="px-4 py-3 font-medium">Event</th>
            <th className="px-4 py-3 font-medium">Actor</th>
            <th className="px-4 py-3 font-medium">IP</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/10">
          {logs.map((item) => (
            <tr key={`${item.time}-${item.event}`} className="text-sm text-slate-200">
              <td className="px-4 py-4 font-mono text-xs text-slate-400">{item.time}</td>
              <td className="px-4 py-4"><Badge tone={logTone[item.level as keyof typeof logTone]}>{item.level}</Badge></td>
              <td className="px-4 py-4">{item.event}</td>
              <td className="px-4 py-4 text-slate-400">{item.actor}</td>
              <td className="px-4 py-4 font-mono text-xs text-slate-400">{item.ip}</td>
            </tr>
          ))}
        </tbody>
      </ResponsiveTable>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg border border-white/10 bg-slate-950/50 p-3">
      <div className="flex items-center justify-between text-xs text-slate-400">
        <span>{label}</span>
        <span>{value.toFixed(1)}%</span>
      </div>
      <div className="mt-3 h-2 rounded-full bg-white/10">
        <div className="h-2 rounded-full bg-cyan-400" style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function ResponsiveTable({ children }: { children: ReactNode }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-[760px] w-full">{children}</table>
    </div>
  );
}