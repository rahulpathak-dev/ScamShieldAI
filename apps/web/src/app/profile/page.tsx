"use client";

import { CalendarClock, KeyRound, Mail, Shield, UserCircle, type LucideIcon } from "lucide-react";

import { ProtectedRoute } from "@/components/auth/protected-route";
import { Badge } from "@/components/ui/badge";
import { PageHeading } from "@/components/workspace/page-heading";
import { WorkspaceShell } from "@/components/workspace/workspace-shell";
import { summarizeHistory } from "@/lib/scan-history";
import { useScanHistory } from "@/hooks/use-scan-history";

export default function ProfilePage() {
  return (
    <ProtectedRoute>
      {(user) => <ProfileContent user={user} />}
    </ProtectedRoute>
  );
}

function ProfileContent({ user }: { user: Parameters<typeof WorkspaceShell>[0]["user"] }) {
  const history = useScanHistory();
  const stats = summarizeHistory(history);

  return (
    <WorkspaceShell user={user}>
      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <PageHeading title="Profile" description="Account, role, and workspace activity" />

        <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
          <div className="rounded-md border bg-card p-5 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-md bg-secondary text-primary">
                <UserCircle className="h-8 w-8" aria-hidden="true" />
              </div>
              <div className="min-w-0">
                <h3 className="truncate text-lg font-semibold">{user.name}</h3>
                <p className="truncate text-sm text-muted-foreground">{user.email}</p>
              </div>
            </div>

            <div className="mt-6 grid gap-3">
              <ProfileRow icon={Mail} label="Email" value={user.email} />
              <ProfileRow icon={Shield} label="Role" value={user.role} />
              <ProfileRow icon={CalendarClock} label="Created" value={new Date(user.created_at).toLocaleDateString()} />
            </div>
          </div>

          <div className="rounded-md border bg-card p-5 shadow-sm">
            <div className="mb-5 flex items-center justify-between gap-3">
              <div>
                <h3 className="text-base font-semibold">Workspace Activity</h3>
                <p className="text-sm text-muted-foreground">Current account summary</p>
              </div>
              <Badge tone={user.is_active ? "success" : "danger"}>{user.is_active ? "Active" : "Inactive"}</Badge>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              <ActivityMetric label="Scans" value={stats.totalScans} />
              <ActivityMetric label="Detections" value={stats.scamDetections} />
              <ActivityMetric label="Average risk" value={`${stats.averageRisk}%`} />
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              <ProfileRow icon={KeyRound} label="Session" value="Secured" />
              <ProfileRow icon={Shield} label="Access" value={user.role} />
            </div>
          </div>
        </div>
      </section>
    </WorkspaceShell>
  );
}

function ProfileRow({ icon: Icon, label, value }: { icon: LucideIcon; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 rounded-md border p-3">
      <Icon className="h-4 w-4 text-primary" aria-hidden="true" />
      <div className="min-w-0">
        <p className="text-xs text-muted-foreground">{label}</p>
        <p className="truncate text-sm font-medium">{value}</p>
      </div>
    </div>
  );
}

function ActivityMetric({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-md border bg-background p-4">
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="mt-2 text-2xl font-semibold">{value}</p>
    </div>
  );
}