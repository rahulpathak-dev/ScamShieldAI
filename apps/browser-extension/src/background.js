const API_BASE_URL = "http://localhost:8000";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type !== "SCAMSHIELD_SCAN_PAGE") return false;

  scanPage(message.payload)
    .then((result) => {
      const analysis = result.analysis;
      if (analysis.risk_score >= 71 || analysis.risk_level === "high" || analysis.risk_level === "critical") {
        chrome.notifications.create(`scamshield-${analysis.analysis_id}`, {
          type: "basic",
          iconUrl: "icons/icon-128.png",
          title: "ScamShieldAI warning",
          message: `Warning: This page has ${Math.round(analysis.risk_score)}% scam probability.`
        });
      }
      sendResponse({ ok: true, result });
    })
    .catch((error) => sendResponse({ ok: false, error: error.message }));

  return true;
});

async function scanPage(payload) {
  const response = await fetch(`${API_BASE_URL}/api/v1/browser-extension/scan-page`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error("ScamShieldAI page scan failed.");
  }

  return response.json();
}