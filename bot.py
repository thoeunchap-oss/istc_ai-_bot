"""
ISTC AI Telegram Bot - Main Entry Point
Deploy on Railway.app
"""
import logging
import os
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from handlers.commands import start, help_command, clear_command, about_command
from handlers.messages import handle_message
from handlers.callbacks import handle_callback
from services import AIService
from config import Config

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    config = Config()

    app = (
        Application.builder()
        .token(config.TELEGRAM_TOKEN)
        .build()
    )

    # ─── Inject AI Service ──────────────────────────────────────────────────────
    app.bot_data["ai_service"] = AIService(config)

    # ─── Command Handlers ───────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("about", about_command))

    # ─── Message Handlers ───────────────────────────────────────────────────────
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ─── Callback Query Handlers ────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("🤖 ISTC AI Bot is starting...")

    # ─── Webhook (Railway) vs Polling (local) ───────────────────────────────────
    webhook_url = os.getenv("WEBHOOK_URL", "")
    port = int(os.getenv("PORT", 8443))

    if webhook_url:
        logger.info(f"🌐 Running in Webhook mode on port {port}")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            secret_token=config.WEBHOOK_SECRET,
            webhook_url=f"{webhook_url}/webhook",
            url_path="/webhook",
        )
    else:
        logger.info("🔄 Running in Polling mode (local development)")
        app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
