"use client";

import { useRouter } from "next/navigation";
import { ReactNode, useEffect, useState } from "react";

import { fetchCurrentUser } from "@/lib/auth-client";
import type { AuthUser, UserRole } from "@/types/auth";

export function ProtectedRoute({
  allowedRoles,
  children
}: {
  allowedRoles?: UserRole[];
  children: (user: AuthUser) => ReactNode;
}) {
  const router = useRouter();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isChecking, setIsChecking] = useState(true);
  const [isForbidden, setIsForbidden] = useState(false);
  const allowedRoleKey = allowedRoles?.join("|") ?? "";

  useEffect(() => {
    let isMounted = true;
    const allowedRoleSet = new Set<UserRole>((allowedRoleKey ? allowedRoleKey.split("|") : []) as UserRole[]);

    fetchCurrentUser()
      .then((currentUser) => {
        if (!isMounted) return;
        if (allowedRoleSet.size && !allowedRoleSet.has(currentUser.role)) {
          setIsForbidden(true);
          return;
        }
        setUser(currentUser);
      })
      .catch(() => {
        router.replace("/login");
      })
      .finally(() => {
        if (isMounted) setIsChecking(false);
      });

    return () => {
      isMounted = false;
    };
  }, [allowedRoleKey, router]);

  if (isChecking) {
    return <div className="p-6 text-sm text-muted-foreground">Checking session...</div>;
  }

  if (isForbidden) {
    return <div className="p-6 text-sm text-red-700">You do not have access to this workspace.</div>;
  }

  if (!user) return null;

  return <>{children(user)}</>;
}