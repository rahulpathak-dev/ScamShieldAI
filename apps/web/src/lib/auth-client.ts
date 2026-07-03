import { getApiBaseUrl } from "@/lib/config";
import { ApiClientError } from "@/lib/api-client";
import type { AuthResponse, AuthUser, LoginPayload, RegisterPayload } from "@/types/auth";

async function parseError(response: Response, fallback: string): Promise<never> {
  const requestId = response.headers.get("x-request-id") ?? undefined;
  let message = fallback;

  try {
    const errorBody = (await response.json()) as { error?: { message?: string } };
    message = errorBody.error?.message ?? message;
  } catch {
    // Keep the fallback message when no JSON body is returned.
  }

  throw new ApiClientError(message, response.status, requestId);
}

export async function registerUser(payload: RegisterPayload): Promise<AuthResponse> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/auth/register`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    return parseError(response, "Registration failed.");
  }

  return response.json() as Promise<AuthResponse>;
}

export async function loginUser(payload: LoginPayload): Promise<AuthResponse> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    return parseError(response, "Login failed.");
  }

  return response.json() as Promise<AuthResponse>;
}

export async function fetchCurrentUser(): Promise<AuthUser> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/auth/me`, {
    method: "GET",
    credentials: "include",
    cache: "no-store"
  });

  if (!response.ok) {
    return parseError(response, "Session check failed.");
  }

  return response.json() as Promise<AuthUser>;
}

export async function logoutUser(): Promise<void> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/auth/logout`, {
    method: "POST",
    credentials: "include"
  });

  if (!response.ok) {
    return parseError(response, "Logout failed.");
  }
}