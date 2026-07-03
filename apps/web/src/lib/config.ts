export function getApiBaseUrl(): string {
  const configuredUrl = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
  return configuredUrl || "http://localhost:8000";
}