"use client";

import { ProtectedRoute } from "@/components/auth/protected-route";
import { LogoutButton } from "@/components/auth/logout-button";

export default function AnalystPage() {
  return (
    <ProtectedRoute allowedRoles={["ADMIN", "ANALYST"]}>
      {(user) => (
        <main className="min-h-screen bg-background p-6 text-foreground">
          <div className="mx-auto flex max-w-5xl items-center justify-between border-b pb-4">
            <div>
              <h1 className="text-xl font-semibold">Analyst Workspace</h1>
              <p className="text-sm text-muted-foreground">Signed in as {user.email}</p>
            </div>
            <LogoutButton />
          </div>
        </main>
      )}
    </ProtectedRoute>
  );
}