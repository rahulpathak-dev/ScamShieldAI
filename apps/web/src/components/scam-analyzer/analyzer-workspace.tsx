"use client";

import { AlertTriangle, Bell, Loader2, MailWarning, Send, ShieldAlert } from "lucide-react";
import { FormEvent, useMemo, useState } from "react";

import { analyzeText, ApiClientError, createHighRiskWarning } from "@/lib/api-client";
import { showBrowserWarning } from "@/lib/browser-notifications";
import type { ScamAnalysis, SourceType } from "@/types/analysis";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

const sourceTypes: Array<{ label: string; value: SourceType }> = [
  { label: "SMS", value: "sms" },
  { label: "Email", value: "email" },
  { label: "Social", value: "social" },
  { label: "Investment ad", value: "investment_ad" },
  { label: "Banking", value: "banking" },
  { label: "Chat", value: "chat" },
  { label: "Screenshot OCR", value: "screenshot_ocr" },
  { label: "Voice transcript", value: "voice_transcript" }
];

const riskTone: Record<ScamAnalysis["risk_level"], "neutral" | "success" | "warning" | "danger"> = {
  low: "success",
  medium: "warning",
  high: "danger",
  critical: "danger"
};

export function AnalyzerWorkspace() {
  const [content, setContent] = useState("");
  const [sourceType, setSourceType] = useState<SourceType>("sms");
  const [language, setLanguage] = useState("en");
  const [analysis, setAnalysis] = useState<ScamAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [alertStatus, setAlertStatus] = useState<string | null>(null);
  const [alertEmail, setAlertEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSendingEmailAlert, setIsSendingEmailAlert] = useState(false);

  const canSubmit = content.trim().length >= 3 && !isSubmitting;
  const riskWidth = useMemo(() => `${Math.min(100, analysis?.risk_score ?? 0)}%`, [analysis]);
  const isHighRisk = analysis ? shouldWarn(analysis) : false;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;

    setIsSubmitting(true);
    setError(null);
    setAlertStatus(null);

    try {
      const result = await analyzeText({ content, source_type: sourceType, language });
      setAnalysis(result);

      if (shouldWarn(result)) {
        void sendBrowserWarning(result, content);
      }
    } catch (caught) {
      if (caught instanceof ApiClientError) {
        setError(caught.requestId ? `${caught.message} Request ID: ${caught.requestId}` : caught.message);
      } else {
        setError("Analysis request failed.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  async function sendBrowserWarning(result: ScamAnalysis, rawMessage: string) {
    try {
      const warning = await createHighRiskWarning({
        analysis_id: result.analysis_id,
        risk_score: result.risk_score,
        scam_probability: result.risk_score,
        risk_level: result.risk_level,
        message_excerpt: createExcerpt(rawMessage),
        reasons: createReasons(result),
        channels: ["browser"]
      });
      const browserStatus = await showBrowserWarning(warning);
      setAlertStatus(browserStatus === "sent" ? warning.body : "Browser notification permission is blocked or unavailable.");
    } catch (caught) {
      setAlertStatus(caught instanceof ApiClientError ? caught.message : "Notification request failed.");
    }
  }

  async function handleSendEmailWarning() {
    if (!analysis || !alertEmail.trim()) return;

    setIsSendingEmailAlert(true);
    setAlertStatus(null);

    try {
      const warning = await createHighRiskWarning({
        analysis_id: analysis.analysis_id,
        risk_score: analysis.risk_score,
        scam_probability: analysis.risk_score,
        risk_level: analysis.risk_level,
        message_excerpt: createExcerpt(content),
        reasons: createReasons(analysis),
        recipient_email: alertEmail.trim(),
        channels: ["email"]
      });
      const emailDelivery = warning.deliveries.find((delivery) => delivery.channel === "email");
      setAlertStatus(emailDelivery ? emailDelivery.detail : warning.body);
    } catch (caught) {
      setAlertStatus(caught instanceof ApiClientError ? caught.message : "Email warning request failed.");
    } finally {
      setIsSendingEmailAlert(false);
    }
  }

  return (
    <section className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[minmax(0,0.95fr)_minmax(360px,0.65fr)] lg:px-8">
      <form className="rounded-md border bg-card p-4 shadow-sm" onSubmit={handleSubmit}>
        <div className="mb-4 flex flex-col gap-1">
          <h2 className="text-base font-semibold">Message Analysis</h2>
          <p className="text-sm text-muted-foreground">Manual intake</p>
        </div>

        <div className="grid gap-4 sm:grid-cols-[1fr_140px]">
          <label className="grid gap-2 text-sm font-medium">
            Source
            <select
              className="h-10 rounded-md border bg-background px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              value={sourceType}
              onChange={(event) => setSourceType(event.target.value as SourceType)}
            >
              {sourceTypes.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.label}
                </option>
              ))}
            </select>
          </label>

          <label className="grid gap-2 text-sm font-medium">
            Language
            <input
              className="h-10 rounded-md border bg-background px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              value={language}
              maxLength={16}
              onChange={(event) => setLanguage(event.target.value)}
            />
          </label>
        </div>

        <label className="mt-4 grid gap-2 text-sm font-medium">
          Content
          <Textarea
            value={content}
            maxLength={20000}
            onChange={(event) => setContent(event.target.value)}
            placeholder="Urgent bank alert: verify OTP now or your account will be suspended."
          />
        </label>

        {error ? (
          <div className="mt-4 flex gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-800">
            <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
            <p>{error}</p>
          </div>
        ) : null}

        <div className="mt-4 flex items-center justify-end gap-3">
          <Button type="button" variant="outline" onClick={() => setContent("")} disabled={!content || isSubmitting}>
            Clear
          </Button>
          <Button type="submit" disabled={!canSubmit}>
            {isSubmitting ? (
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            ) : (
              <Send className="h-4 w-4" aria-hidden="true" />
            )}
            Analyze
          </Button>
        </div>
      </form>

      <aside className="rounded-md border bg-card p-4 shadow-sm">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-semibold">Risk Summary</h2>
            <p className="text-sm text-muted-foreground">Latest assessment</p>
          </div>
          <ShieldAlert className="h-5 w-5 text-primary" aria-hidden="true" />
        </div>

        {analysis ? (
          <div className="grid gap-5">
            {isHighRisk ? (
              <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-800">
                <div className="flex items-start gap-2">
                  <Bell className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                  <div>
                    <p className="font-semibold">Warning: This message has {analysis.risk_score.toFixed(0)}% scam probability.</p>
                    <p className="mt-1">High-risk notification generated for this scan.</p>
                  </div>
                </div>
              </div>
            ) : null}

            <div className="grid gap-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Risk score</span>
                <strong>{analysis.risk_score.toFixed(0)} / 100</strong>
              </div>
              <div className="h-3 overflow-hidden rounded-sm bg-muted">
                <div className="h-full bg-primary" style={{ width: riskWidth }} />
              </div>
              <Badge tone={riskTone[analysis.risk_level]} className="w-fit capitalize">
                {analysis.risk_level}
              </Badge>
            </div>

            <ResultGroup title="Scam categories" values={analysis.scam_categories} />
            <ResultGroup title="Persuasion strategies" values={analysis.persuasion_strategies} />

            <div className="grid gap-2">
              <h3 className="text-sm font-semibold">Evidence</h3>
              <div className="grid gap-2">
                {analysis.evidence.slice(0, 4).map((item) => (
                  <div key={`${item.signal}-${item.weight}`} className="rounded-md border p-3">
                    <div className="flex items-center justify-between gap-3 text-sm font-medium">
                      <span>{item.signal}</span>
                      <span>{item.weight}</span>
                    </div>
                    <p className="mt-1 text-sm text-muted-foreground">{item.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {isHighRisk ? (
              <div className="grid gap-3 rounded-md border p-3">
                <div className="flex items-center gap-2 text-sm font-semibold">
                  <MailWarning className="h-4 w-4 text-primary" aria-hidden="true" />
                  Email warning
                </div>
                <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
                  <input
                    className="h-10 rounded-md border bg-background px-3 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    type="email"
                    value={alertEmail}
                    onChange={(event) => setAlertEmail(event.target.value)}
                    placeholder="security-team@example.com"
                  />
                  <Button type="button" onClick={handleSendEmailWarning} disabled={!alertEmail.trim() || isSendingEmailAlert}>
                    {isSendingEmailAlert ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <MailWarning className="h-4 w-4" aria-hidden="true" />}
                    Send
                  </Button>
                </div>
                {alertStatus ? <p className="text-sm text-muted-foreground">{alertStatus}</p> : null}
              </div>
            ) : alertStatus ? (
              <p className="text-sm text-muted-foreground">{alertStatus}</p>
            ) : null}
          </div>
        ) : (
          <div className="rounded-md border border-dashed p-6 text-sm text-muted-foreground">
            No analysis result yet.
          </div>
        )}
      </aside>
    </section>
  );
}

function ResultGroup({ title, values }: { title: string; values: string[] }) {
  return (
    <div className="grid gap-2">
      <h3 className="text-sm font-semibold">{title}</h3>
      <div className="flex flex-wrap gap-2">
        {values.length ? (
          values.map((value) => <Badge key={value}>{value.replaceAll("_", " ")}</Badge>)
        ) : (
          <span className="text-sm text-muted-foreground">None</span>
        )}
      </div>
    </div>
  );
}

function shouldWarn(analysis: ScamAnalysis): boolean {
  return analysis.risk_score >= 71 || analysis.risk_level === "high" || analysis.risk_level === "critical";
}

function createExcerpt(value: string): string {
  const trimmed = value.trim().replace(/\s+/g, " ");
  return trimmed.length > 240 ? `${trimmed.slice(0, 237)}...` : trimmed;
}

function createReasons(analysis: ScamAnalysis): string[] {
  const evidenceReasons = analysis.evidence.slice(0, 3).map((item) => item.description);
  const strategyReasons = analysis.persuasion_strategies.slice(0, 3).map((strategy) => `${strategy.replaceAll("_", " ")} detected`);
  return [...evidenceReasons, ...strategyReasons].slice(0, 5);
}