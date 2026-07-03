chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type !== "SCAMSHIELD_COLLECT_PAGE") return false;

  sendResponse({
    page_url: window.location.href,
    page_title: document.title,
    visible_text: document.body?.innerText?.slice(0, 50000) || ""
  });
  return false;
});