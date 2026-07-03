import logging
import smtplib
from email.message import EmailMessage

from app.application.notification_dto import (
    HighRiskWarningCommand,
    HighRiskWarningDTO,
    NotificationDeliveryDTO,
)
from app.core.config import Settings

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def create_high_risk_warning(self, command: HighRiskWarningCommand) -> HighRiskWarningDTO:
        scam_probability = command.scam_probability if command.scam_probability is not None else command.risk_score
        severity = "critical" if command.risk_score >= self._settings.notification_critical_threshold else "warning"
        title = "Warning: High-risk scam detected"
        body = f"Warning: This message has {scam_probability:.0f}% scam probability."
        actions = [
            "Do not click links, call phone numbers, or reply to the sender.",
            "Do not share OTPs, passwords, banking details, wallet keys, or identity documents.",
            "Report the message to your bank, platform, or security team before taking action.",
        ]

        deliveries: list[NotificationDeliveryDTO] = []
        requested_channels = list(dict.fromkeys(command.channels))

        if "browser" in requested_channels:
            deliveries.append(
                NotificationDeliveryDTO(
                    channel="browser",
                    status="sent",
                    detail="Browser notification payload generated for the client.",
                )
            )

        if "email" in requested_channels:
            deliveries.append(self._send_email(command=command, title=title, body=body, actions=actions))

        return HighRiskWarningDTO(
            severity=severity,
            title=title,
            body=body,
            risk_score=command.risk_score,
            scam_probability=scam_probability,
            recommended_actions=actions,
            deliveries=deliveries,
        )

    def _send_email(
        self,
        command: HighRiskWarningCommand,
        title: str,
        body: str,
        actions: list[str],
    ) -> NotificationDeliveryDTO:
        if command.recipient_email is None:
            return NotificationDeliveryDTO(channel="email", status="skipped", detail="No recipient email was provided.")

        if not self._settings.email_notifications_enabled:
            logger.info("Email notification skipped because email notifications are disabled.")
            return NotificationDeliveryDTO(channel="email", status="skipped", detail="Email notifications are disabled.")

        if not self._settings.smtp_host or not self._settings.notification_from_email:
            logger.warning("Email notification skipped because SMTP settings are incomplete.")
            return NotificationDeliveryDTO(channel="email", status="skipped", detail="SMTP settings are incomplete.")

        message = EmailMessage()
        message["Subject"] = title
        message["From"] = self._settings.notification_from_email
        message["To"] = str(command.recipient_email)
        message.set_content(self._email_body(command=command, body=body, actions=actions))

        try:
            with smtplib.SMTP(self._settings.smtp_host, self._settings.smtp_port, timeout=10) as smtp:
                if self._settings.smtp_use_tls:
                    smtp.starttls()
                if self._settings.smtp_username and self._settings.smtp_password:
                    smtp.login(self._settings.smtp_username, self._settings.smtp_password)
                smtp.send_message(message)
        except Exception as exc:  # pragma: no cover - external SMTP failure path
            logger.exception("Email notification delivery failed.")
            return NotificationDeliveryDTO(channel="email", status="failed", detail=str(exc))

        logger.info("High-risk scam warning email sent.")
        return NotificationDeliveryDTO(channel="email", status="sent", detail="Email warning sent.")

    def _email_body(self, command: HighRiskWarningCommand, body: str, actions: list[str]) -> str:
        reasons = command.reasons or ["High-risk scam indicators were detected."]
        reasons_text = "\n".join(f"- {reason}" for reason in reasons)
        actions_text = "\n".join(f"- {action}" for action in actions)

        return (
            f"{body}\n\n"
            f"Risk level: {command.risk_level}\n"
            f"Risk score: {command.risk_score:.0f}/100\n\n"
            f"Reasons:\n{reasons_text}\n\n"
            f"Recommended actions:\n{actions_text}\n\n"
            "ScamShieldAI"
        )