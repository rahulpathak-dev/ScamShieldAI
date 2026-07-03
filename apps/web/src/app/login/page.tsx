"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import { AuthCard } from "@/components/auth/auth-card";
import { Button } from "@/components/ui/button";
import { loginUser } from "@/lib/auth-client";
import { ApiClientError } from "@/lib/api-client";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await loginUser({ email, password });
      router.replace("/dashboard");
      router.refresh();
    } catch (caught) {
      setError(caught instanceof ApiClientError ? caught.message : "Login failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard title="Sign in" subtitle="ScamShieldAI secure access">
      <form className="grid gap-4" onSubmit={handleSubmit}>
        <label className="grid gap-2 text-sm font-medium">
          Email
          <input
            className="h-10 rounded-md border bg-background px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            type="email"
            value={email}
            autoComplete="email"
            required
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>
        <label className="grid gap-2 text-sm font-medium">
          Password
          <input
            className="h-10 rounded-md border bg-background px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            type="password"
            value={password}
            autoComplete="current-password"
            required
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>

        {error ? <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-800">{error}</div> : null}

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Signing in..." : "Sign in"}
        </Button>
      </form>

      <p className="mt-5 text-sm text-muted-foreground">
        New to ScamShieldAI? <Link className="font-medium text-primary" href="/register">Create an account</Link>
      </p>
    </AuthCard>
  );
}