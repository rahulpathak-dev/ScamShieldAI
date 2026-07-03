"use client";

import { AlertTriangle, Bell, CheckCircle2, Loader2, MailWarning, ScanSearch, Send, ShieldAlert } from "lucide-react";
import { FormEvent, useMemo, useState } from "react";

import { ProtectedRoute } from "@/components/auth/protected-route";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { PageHeading } from "@/components/workspace/page-heading";
import { WorkspaceShell } from "@/components/workspace/workspace-shell";
import { analyzeText, ApiClientError, createHighRiskWarning } from "@/lib/api-client";
import { showBrowserWarning } from "@/lib/browser-notifications";
import { deriveCategory, deriveExplanation, deriveProbability, saveScan, toStoredScan } from "@/lib/scan-history";
import type { ScamAnalysis, SourceType } from "@/types/analysis";

const sourceTypes: Array<{ label: string; value: SourceType }> = [
  { label: "Text / URL", value: "chat" },
  { label: "Email", value: "email" },
  { label: "SMS", value: "sms" },
  { label: "Banking", value: "banking" },
  { label: "Investment ad", value: "investment_ad" },
  { label: "Social", value: "social" }
];

const riskTone: Record<ScamAnalysis["risk_level"], "neutral" | "success" | "warning" | "danger"> = {
  low: "success",
  medium: "warning",
  high: "danger",
  critical: "danger"
};

export default function AnalyzerPage() {
  return (
    <ProtectedRoute>
      {(user) => <AnalyzerContent user={user} />}
    </ProtectedRoute>
  );
}

function AnalyzerContent({ user }: { user: Parameters<typeof WorkspaceShell>[0]["user"] }) {
  const [message, setMessage] = useState("");
  const [sourceType, setSourceType] = useState<SourceType>("chat");
  const [language, setLanguage] = useState("en");
  const [analysis, setAnalysis] = useState<ScamAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [alertStatus, setAlertStatus] = useState<string | null>(null);
  const [alertEmail, setAlertEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSendingEmailAlert, setIsSendingEmailAlert] = useState(false);

  const normalizedMessage = normalizeUserText(message);
  const canSubmit = normalizedMessage.length >= 3 && !isSubmitting;
  const probability = analysis ? deriveProbability(analysis.risk_score) : 0;
  const riskWidth = useMemo(() => `${Math.min(100, analysis?.risk_score ?? 0)}%`, [analysis]);
  const isHighRisk = analysis ? shouldWarn(analysis) : false;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;

    setIsSubmitting(true);
    setError(null);
    setAlertStatus(null);

    try {
      const result = await analyzeText({ content: normalizedMessage, source_type: sourceType, language });
      setAnalysis(result);
      saveScan(toStoredScan(normalizedMessage, result));
      if (shouldWarn(result)) {
        void sendBrowserWarning(result, normalizedMessage);
      }
    } catch (caught) {
      setError(caught instanceof ApiClientError ? caught.message : "Analysis request failed.");
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
        message_excerpt: createExcerpt(normalizedMessage),
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
    <WorkspaceShell user={user}>
      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <PageHeading title="Scam Analyzer" description="Analyze messages, emails, links, and suspicious text for scam risk" />

        <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_420px]">
          <form className="rounded-md border bg-card p-4 shadow-sm" onSubmit={handleSubmit}>
            <div className="mb-4 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-md bg-secondary text-primary">
                <ScanSearch className="h-5 w-5" aria-hidden="true" />
              </div>
              <div>
                <h3 className="text-base font-semibold">Intake</h3>
                <p className="text-sm text-muted-foreground">Message, email, link, or suspicious text</p>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-[1fr_140px]">
              <label className="grid gap-2 text-sm font-medium">
                Type
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
                className="min-h-64"
                value={message}
                maxLength={20000}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Paste a suspicious SMS, email, chat, or URL. Example: Urgent bank alert: verify OTP now to avoid suspension."
              />
            </label>

            {error ? (
              <div className="mt-4 flex gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-800">
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                <p>{error}</p>
              </div>
            ) : null}

            <div className="mt-4 flex items-center justify-end gap-3">
              <Button type="button" variant="outline" onClick={() => setMessage("")} disabled={!message || isSubmitting}>
                Clear
              </Button>
              <Button type="submit" disabled={!canSubmit}>
                {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Send className="h-4 w-4" aria-hidden="true" />}
                Analyze
              </Button>
            </div>
          </form>

          <aside className="rounded-md border bg-card p-4 shadow-sm">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <h3 className="text-base font-semibold">Assessment</h3>
                <p className="text-sm text-muted-foreground">Scam probability and explanation</p>
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
                <div className="rounded-md border p-4">
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <span>Scam probability</span>
                    <span>{probability}%</span>
                  </div>
                  <div className="mt-3 h-3 overflow-hidden rounded-sm bg-muted">
                    <div className="h-full bg-primary" style={{ width: `${probability}%` }} />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-md border p-3">
                    <p className="text-sm text-muted-foreground">Risk score</p>
                    <p className="mt-1 text-2xl font-semibold">{analysis.risk_score.toFixed(0)}</p>
                    <div className="mt-2 h-2 overflow-hidden rounded-sm bg-muted">
                      <div className="h-full bg-primary" style={{ width: riskWidth }} />
                    </div>
                  </div>
                  <div className="rounded-md border p-3">
                    <p className="text-sm text-muted-foreground">Category</p>
                    <p className="mt-1 text-base font-semibold capitalize">{deriveCategory(analysis)}</p>
                    <Badge tone={riskTone[analysis.risk_level]} className="mt-2 capitalize">
                      {analysis.risk_level}
                    </Badge>
                  </div>
                </div>

                <div className="rounded-md border p-4">
                  <div className="mb-2 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-primary" aria-hidden="true" />
                    <h4 className="text-sm font-semibold">Explanation</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">{deriveExplanation(analysis)}</p>
                </div>

                <ResultList title="Persuasion techniques" values={analysis.persuasion_strategies.map(formatLabel)} empty="No strong persuasion pattern detected." />
                <ResultList title="Safety recommendations" values={analysis.recommended_actions} empty="No immediate action required." />

                <div className="grid gap-2">
                  <h4 className="text-sm font-semibold">Evidence</h4>
                  {analysis.evidence.slice(0, 5).map((item) => (
                    <div key={`${item.signal}-${item.weight}`} className="rounded-md border p-3 text-sm">
                      <div className="flex items-center justify-between gap-3 font-medium">
                        <span>{item.signal}</span>
                        <span>{item.weight}</span>
                      </div>
                      <p className="mt-1 text-muted-foreground">{item.description}</p>
                    </div>
                  ))}
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
              <div className="rounded-md border border-dashed p-6 text-sm text-muted-foreground">No assessment yet.</div>
            )}
          </aside>
        </div>
      </section>
    </WorkspaceShell>
  );
}

function ResultList({ title, values, empty }: { title: string; values: string[]; empty: string }) {
  return (
    <div className="rounded-md border p-4">
      <h4 className="text-sm font-semibold">{title}</h4>
      {values.length ? (
        <div className="mt-3 flex flex-wrap gap-2">
          {values.slice(0, 6).map((value) => (
            <Badge key={value}>{value}</Badge>
          ))}
        </div>
      ) : (
        <p className="mt-2 text-sm text-muted-foreground">{empty}</p>
      )}
    </div>
  );
}

function formatLabel(value: string): string {
  return value.replaceAll("_", " ");
}

function normalizeUserText(value: string): string {
  return value.replace(/\u0000/g, " ").replace(/\s+/g, " ").trim();
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