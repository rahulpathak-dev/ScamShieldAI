"use client";

import { LogOut } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { logoutUser } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";

export function LogoutButton() {
  const router = useRouter();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  async function handleLogout() {
    setIsLoggingOut(true);
    try {
      await logoutUser();
    } finally {
      router.replace("/login");
      router.refresh();
    }
  }

  return (
    <Button type="button" variant="outline" size="sm" onClick={handleLogout} disabled={isLoggingOut}>
      <LogOut className="h-4 w-4" aria-hidden="true" />
      Sign out
    </Button>
  );
}