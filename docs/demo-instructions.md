# Demo Instructions

## Scenario

Demonstrate ScamShieldAI detecting, explaining, and warning about a suspicious financial scam message.

## Setup

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open:

- Web: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`

## Demo Flow

1. Register a user.
2. Log in.
3. Open the analyzer page.
4. Submit this message:

```text
Urgent bank alert: your account is suspended. Verify your OTP now at https://bit.ly/secure-bank or your funds will be locked.
```

5. Show the risk score, scam category, persuasion strategies, evidence, and recommended actions.
6. Show the browser notification warning for a high-risk result.
7. Open the admin dashboard and show scam analytics, threat intelligence, model monitoring, and logs.
8. Open API docs and run the enterprise batch example.
9. Optional: load the browser extension and scan a suspicious webpage.

## Expected Result

The message should be classified as high or critical risk with phishing, banking fraud, urgency, and credential or OTP evidence.