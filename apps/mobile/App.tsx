import { useState, type ReactNode } from "react";
import { SafeAreaView, ScrollView, Text, TextInput, TouchableOpacity, View } from "react-native";

const API_BASE_URL = "http://localhost:8000";

type AnalysisResult = {
  analysis: {
    risk_score: number;
    risk_level: string;
    scam_categories: string[];
    recommended_actions: string[];
  };
};

export default function App() {
  const [sms, setSms] = useState("");
  const [ocrText, setOcrText] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [status, setStatus] = useState("Ready");

  async function scanSms() {
    setStatus("Scanning SMS");
    setResult(await postScan("/api/v1/mobile/scan-sms", { content: sms, language: "en" }));
    setStatus("Complete");
  }

  async function scanScreenshotText() {
    setStatus("Scanning screenshot text");
    setResult(await postScan("/api/v1/mobile/scan-screenshot", {
      image_base64: "placeholder-image-bytes-for-native-capture",
      ocr_text: ocrText,
      language: "en"
    }));
    setStatus("Complete");
  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#020617" }}>
      <ScrollView contentContainerStyle={{ gap: 16, padding: 20 }}>
        <Text style={{ color: "white", fontSize: 24, fontWeight: "700" }}>ScamShieldAI Mobile</Text>
        <Text style={{ color: "#94a3b8" }}>{status}</Text>

        <Panel title="SMS scanning">
          <TextInput
            multiline
            value={sms}
            onChangeText={setSms}
            placeholder="Paste suspicious SMS"
            placeholderTextColor="#64748b"
            style={inputStyle}
          />
          <ActionButton label="Scan SMS" onPress={scanSms} disabled={sms.trim().length < 3} />
        </Panel>

        <Panel title="Screenshot analysis">
          <TextInput
            multiline
            value={ocrText}
            onChangeText={setOcrText}
            placeholder="OCR text from screenshot"
            placeholderTextColor="#64748b"
            style={inputStyle}
          />
          <ActionButton label="Analyze screenshot" onPress={scanScreenshotText} disabled={ocrText.trim().length < 3} />
        </Panel>

        {result ? (
          <Panel title="Risk result">
            <Text style={{ color: "white", fontSize: 32, fontWeight: "800" }}>{Math.round(result.analysis.risk_score)} / 100</Text>
            <Text style={{ color: "#fca5a5", textTransform: "capitalize" }}>{result.analysis.risk_level}</Text>
            <Text style={{ color: "#cbd5e1" }}>{result.analysis.scam_categories.join(", ") || "No scam category detected"}</Text>
          </Panel>
        ) : null}
      </ScrollView>
    </SafeAreaView>
  );
}

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <View style={{ gap: 10, borderColor: "rgba(255,255,255,0.14)", borderWidth: 1, borderRadius: 8, padding: 14 }}>
      <Text style={{ color: "white", fontWeight: "700" }}>{title}</Text>
      {children}
    </View>
  );
}

function ActionButton({ label, onPress, disabled }: { label: string; onPress: () => void; disabled?: boolean }) {
  return (
    <TouchableOpacity disabled={disabled} onPress={onPress} style={{ backgroundColor: disabled ? "#334155" : "#22d3ee", borderRadius: 6, padding: 12 }}>
      <Text style={{ color: disabled ? "#94a3b8" : "#082f49", fontWeight: "800", textAlign: "center" }}>{label}</Text>
    </TouchableOpacity>
  );
}

async function postScan(path: string, payload: unknown): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error("ScamShieldAI mobile scan failed.");
  }

  return response.json();
}

const inputStyle = {
  minHeight: 120,
  borderColor: "rgba(255,255,255,0.14)",
  borderWidth: 1,
  borderRadius: 6,
  color: "white",
  padding: 10,
  textAlignVertical: "top" as const
};