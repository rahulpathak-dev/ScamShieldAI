import type { HighRiskWarning } from "@/types/notifications";

export async function showBrowserWarning(warning: HighRiskWarning): Promise<"sent" | "blocked" | "unsupported"> {
  if (typeof window === "undefined" || !("Notification" in window)) {
    return "unsupported";
  }

  let permission = Notification.permission;
  if (permission === "default") {
    permission = await Notification.requestPermission();
  }

  if (permission !== "granted") {
    return "blocked";
  }

  new Notification(warning.title, {
    body: warning.body,
    tag: "scamshield-high-risk-warning",
    requireInteraction: warning.severity === "critical",
  });

  return "sent";
}