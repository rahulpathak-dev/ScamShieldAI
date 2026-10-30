import type { ScamAnalysis, SourceType } from "@/types/analysis";

const HISTORY_KEY = "scamshield.scanHistory.v1";

export type StoredScan = {
  id: string;
  createdAt: string;
  sourceType: SourceType;
  language: string;
  messagePreview: string;
  probability: number;
  riskScore: number;
  riskLevel: ScamAnalysis["risk_level"];
  category: string;
  explanation: string;
  evidenceCount: number;
};

export function deriveProbability(riskScore: number): number {
  return Math.max(1, Math.min(99, Math.round(riskScore)));
}

export function deriveCategory(analysis: ScamAnalysis): string {
  return analysis.scam_categories[0]?.replaceAll("_", " ") ?? "unknown";
}

export function deriveExplanation(analysis: ScamAnalysis): string {
  const evidence = analysis.evidence[0]?.description;
  if (evidence) return evidence;
  return analysis.risk_level === "low"
    ? "No strong scam indicators were detected in this message."
    : "Multiple scam indicators were detected in the submitted content.";
}

export function toStoredScan(message: string, analysis: ScamAnalysis): StoredScan {
  const compactMessage = message.replace(/\s+/g, " ").trim();
  return {
    id: analysis.analysis_id,
    createdAt: analysis.created_at,
    sourceType: analysis.source_type,
    language: analysis.language,
    messagePreview: compactMessage.length > 140 ? `${compactMessage.slice(0, 140)}...` : compactMessage,
    probability: deriveProbability(analysis.risk_score),
    riskScore: analysis.risk_score,
    riskLevel: analysis.risk_level,
    category: deriveCategory(analysis),
    explanation: deriveExplanation(analysis),
    evidenceCount: analysis.evidence.length
  };
}


export function toStoredScanFromAnalysis(analysis: ScamAnalysis): StoredScan {
  return {
    id: analysis.analysis_id,
    createdAt: analysis.created_at,
    sourceType: analysis.source_type,
    language: analysis.language,
    messagePreview: "Stored securely in database. Message content is hidden for privacy.",
    probability: deriveProbability(analysis.risk_score),
    riskScore: analysis.risk_score,
    riskLevel: analysis.risk_level,
    category: deriveCategory(analysis),
    explanation: deriveExplanation(analysis),
    evidenceCount: analysis.evidence.length
  };
}
export function getScanHistory(): StoredScan[] {
  if (typeof window === "undefined") return [];

  try {
    const raw = window.localStorage.getItem(HISTORY_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as StoredScan[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function saveScan(scan: StoredScan): StoredScan[] {
  const next = [scan, ...getScanHistory().filter((item) => item.id !== scan.id)].slice(0, 50);
  window.localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
  window.dispatchEvent(new Event("scamshield:history-updated"));
  return next;
}

export function clearScanHistory(): void {
  window.localStorage.removeItem(HISTORY_KEY);
  window.dispatchEvent(new Event("scamshield:history-updated"));
}

export function summarizeHistory(history: StoredScan[]) {
  const totalScans = history.length;
  const scamDetections = history.filter((scan) => scan.riskLevel === "high" || scan.riskLevel === "critical").length;
  const averageRisk = totalScans ? Math.round(history.reduce((sum, scan) => sum + scan.riskScore, 0) / totalScans) : 0;
  const criticalScans = history.filter((scan) => scan.riskLevel === "critical").length;
  const mediumOrAbove = history.filter((scan) => scan.riskScore >= 30).length;
  const detectionRate = totalScans ? Math.round((scamDetections / totalScans) * 100) : 0;

  return {
    totalScans,
    scamDetections,
    averageRisk,
    criticalScans,
    mediumOrAbove,
    detectionRate
  };
}