import { getApiBaseUrl } from "@/lib/config";
import type { AnalyzeTextRequest, ScamAnalysis } from "@/types/analysis";
import type { HighRiskWarning, HighRiskWarningRequest } from "@/types/notifications";

export class ApiClientError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly requestId?: string
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

export async function analyzeText(payload: AnalyzeTextRequest): Promise<ScamAnalysis> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/analyze/text`, {
    method: "POST",
    credentials: "include",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ...payload,
      content: normalizeUserText(payload.content),
      language: payload.language.trim().toLowerCase()
    })
  });

  if (!response.ok) {
    throw await toApiClientError(response, "Analysis request failed.");
  }

  return response.json() as Promise<ScamAnalysis>;
}

export async function createHighRiskWarning(payload: HighRiskWarningRequest): Promise<HighRiskWarning> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/notifications/high-risk-warning`, {
    method: "POST",
    credentials: "include",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw await toApiClientError(response, "Notification request failed.");
  }

  return response.json() as Promise<HighRiskWarning>;
}


export async function getAnalysisHistory(limit = 50): Promise<ScamAnalysis[]> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/analyze/history?limit=${limit}`, {
    method: "GET",
    credentials: "include",
    cache: "no-store"
  });

  if (!response.ok) {
    throw await toApiClientError(response, "History request failed.");
  }

  return response.json() as Promise<ScamAnalysis[]>;
}
function normalizeUserText(value: string): string {
  return value.replace(/\u0000/g, " ").replace(/\s+/g, " ").trim();
}

async function toApiClientError(response: Response, fallbackMessage: string): Promise<ApiClientError> {
  const requestId = response.headers.get("x-request-id") ?? undefined;
  let message = fallbackMessage;

  try {
    const errorBody = (await response.json()) as { error?: { message?: string } };
    message = errorBody.error?.message ?? message;
  } catch {
    // Keep the safe generic message when the server does not return JSON.
  }

  return new ApiClientError(message, response.status, requestId);
}