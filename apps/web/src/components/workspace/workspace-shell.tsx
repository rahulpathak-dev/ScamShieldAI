"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, History, Radar, ShieldCheck, UserCircle } from "lucide-react";
import type { ReactNode } from "react";

import { LogoutButton } from "@/components/auth/logout-button";
import type { AuthUser } from "@/types/auth";
import { cn } from "@/lib/utils";

const navigation = [
  { href: "/dashboard", label: "Dashboard", icon: Activity },
  { href: "/analyzer", label: "Analyzer", icon: Radar },
  { href: "/history", label: "History", icon: History },
  { href: "/profile", label: "Profile", icon: UserCircle }
];

export function WorkspaceShell({ user, children }: { user: AuthUser; children: ReactNode }) {
  const pathname = usePathname();

  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-20 border-b bg-card/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground shadow-sm">
                <ShieldCheck className="h-5 w-5" aria-hidden="true" />
              </div>
              <div>
                <h1 className="text-lg font-semibold leading-6">ScamShieldAI</h1>
                <p className="text-sm text-muted-foreground">{user.role} workspace</p>
              </div>
            </div>
            <div className="lg:hidden">
              <LogoutButton />
            </div>
          </div>

          <nav className="flex gap-2 overflow-x-auto">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "inline-flex h-10 shrink-0 items-center gap-2 rounded-md border px-3 text-sm font-medium transition-colors",
                    isActive
                      ? "border-primary bg-primary text-primary-foreground"
                      : "border-border bg-background text-muted-foreground hover:bg-muted hover:text-foreground"
                  )}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {item.label}
                </Link>
              );
            })}
          </nav>

          <div className="hidden items-center gap-3 lg:flex">
            <span className="max-w-64 truncate text-sm text-muted-foreground">{user.email}</span>
            <LogoutButton />
          </div>
        </div>
      </header>
      {children}
    </main>
  );
}