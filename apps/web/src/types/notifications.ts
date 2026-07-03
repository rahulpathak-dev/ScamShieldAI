export type NotificationChannel = "browser" | "email";

export type HighRiskWarningRequest = {
  analysis_id?: string;
  risk_score: number;
  scam_probability?: number;
  risk_level: string;
  message_excerpt: string;
  reasons: string[];
  recipient_email?: string;
  channels: NotificationChannel[];
};

export type NotificationDelivery = {
  channel: NotificationChannel;
  status: "sent" | "skipped" | "failed";
  detail: string;
};

export type HighRiskWarning = {
  severity: "info" | "warning" | "critical";
  title: string;
  body: string;
  risk_score: number;
  scam_probability: number;
  recommended_actions: string[];
  deliveries: NotificationDelivery[];
};