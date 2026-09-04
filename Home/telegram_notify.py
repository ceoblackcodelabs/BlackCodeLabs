# Home/telegram_notify.py
"""
Telegram notification helper for BlackCodeLabs.

Why this exists: the site owner doesn't monitor an email inbox, but does
watch Telegram. Every contact-form submission is pushed to a Telegram chat
via the Bot API the moment it's saved, so it can be seen immediately —
without making the visitor wait on that network call.

Usage:
    from Home.telegram_notify import notify_new_contact_inquiry
    notify_new_contact_inquiry(inquiry)          # fire in a background thread

Everything here is defensive on purpose: a Telegram outage, bad token, or
network hiccup must never break the contact form for the visitor. Every
failure is caught and logged to the dedicated "telegram" logger
(see logs/telegram.log) instead of raising.
"""
import json
import logging
import threading
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger("telegram")

TELEGRAM_API_BASE = "https://api.telegram.org"
REQUEST_TIMEOUT_SECONDS = 8


def _escape_html(value):
    """Minimal HTML-escaping for Telegram's HTML parse mode."""
    if value is None:
        return ""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def send_telegram_message(text, parse_mode="HTML"):
    """
    Low-level send: posts `text` to the configured Telegram chat.
    Returns True on success, False otherwise. Never raises.
    """
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        logger.info(
            "Telegram not configured (TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID "
            "missing) — skipping notification."
        )
        return False

    url = f"{TELEGRAM_API_BASE}/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8", errors="replace")
            if response.status == 200:
                logger.info("Telegram message sent successfully.")
                return True
            logger.error(
                "Telegram API returned status %s: %s", response.status, body
            )
            return False
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        logger.error("Telegram HTTPError %s: %s", e.code, error_body)
        return False
    except urllib.error.URLError as e:
        logger.error("Telegram URLError (network/timeout): %s", e.reason)
        return False
    except Exception:
        logger.exception("Unexpected error sending Telegram message.")
        return False


def _build_contact_message(inquiry):
    return (
        "\U0001F514 <b>New Contact Inquiry — BlackCodeLabs</b>\n\n"
        f"<b>Name:</b> {_escape_html(inquiry.full_name())}\n"
        f"<b>Email:</b> {_escape_html(inquiry.email)}\n"
        f"<b>Phone:</b> {_escape_html(inquiry.phone or 'Not provided')}\n"
        f"<b>Company:</b> {_escape_html(inquiry.company or 'Not provided')}\n"
        f"<b>Subject:</b> {_escape_html(inquiry.subject)}\n\n"
        f"<b>Message:</b>\n{_escape_html(inquiry.message)}\n\n"
        f"<b>Status:</b> {_escape_html(inquiry.get_status_display())}\n"
        f"<b>IP:</b> {_escape_html(inquiry.ip_address or 'Unknown')}\n"
        f"<b>Received:</b> {inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')} "
        f"(Africa/Nairobi)"
    )


def notify_new_contact_inquiry(inquiry, background=True):
    """
    Send a Telegram alert for a newly-saved ContactInquiry.

    By default this dispatches on a background daemon thread so the HTTP
    response to the visitor is never delayed by a slow/unreachable Telegram
    API — the visitor still gets their "message received" confirmation
    instantly, and the notification lands on your phone a moment later.

    Pass background=False (e.g. in tests / management commands) to send
    synchronously and get the True/False result back directly.
    """
    text = _build_contact_message(inquiry)

    if not background:
        return send_telegram_message(text)

    def _worker():
        send_telegram_message(text)

    thread = threading.Thread(
        target=_worker,
        name=f"telegram-notify-inquiry-{inquiry.pk}",
        daemon=True,
    )
    thread.start()
    return None
