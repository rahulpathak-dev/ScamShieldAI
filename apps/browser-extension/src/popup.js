const button = document.getElementById("scan-page");
const result = document.getElementById("result");
const status = document.getElementById("status");

button.addEventListener("click", async () => {
  status.textContent = "Scanning";
  result.textContent = "";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const page = await chrome.tabs.sendMessage(tab.id, { type: "SCAMSHIELD_COLLECT_PAGE" });

  chrome.runtime.sendMessage({ type: "SCAMSHIELD_SCAN_PAGE", payload: page }, (response) => {
    if (!response?.ok) {
      status.textContent = "Error";
      result.textContent = response?.error || "Scan failed.";
      return;
    }

    const analysis = response.result.analysis;
    status.textContent = analysis.risk_level;
    result.innerHTML = `
      <p><strong>${Math.round(analysis.risk_score)} / 100</strong></p>
      <p>${analysis.scam_categories.join(", ") || "No scam category detected"}</p>
    `;
  });
});