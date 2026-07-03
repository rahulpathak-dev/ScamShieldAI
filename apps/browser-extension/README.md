# ScamShieldAI Browser Guard

Manifest V3 browser extension scaffold for detecting scam indicators while browsing.

## Flow

1. Popup asks the content script for visible page text.
2. Background service worker sends the page payload to `/api/v1/browser-extension/scan-page`.
3. High-risk results trigger a browser notification.

## Local Setup

1. Start the ScamShieldAI API on `http://localhost:8000`.
2. Open Chrome or Edge extension settings.
3. Enable developer mode.
4. Load `apps/browser-extension` as an unpacked extension.