export type SourceType =
  | "sms"
  | "email"
  | "social"
  | "investment_ad"
  | "banking"
  | "chat"
  | "screenshot_ocr"
  | "voice_transcript";

export type AnalyzeTextRequest = {
  content: string;
  source_type: SourceType;
  language: string;
};

export type Evidence = {
  signal: string;
  description: string;
  weight: number;
  matched_terms: string[];
};

export type ScamAnalysis = {
  analysis_id: string;
  source_type: SourceType;
  language: string;
  risk_score: number;
  risk_level: "low" | "medium" | "high" | "critical";
  scam_categories: string[];
  persuasion_strategies: string[];
  evidence: Evidence[];
  recommended_actions: string[];
  created_at: string;
};
