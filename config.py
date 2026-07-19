"""
Configuration – reads all settings from environment variables.
Loads .env automatically in local development via python-dotenv.
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load .env if it exists (no-op on Railway where vars are set directly)
load_dotenv()


@dataclass
class Config:
    # ── Telegram ──────────────────────────────────────────────────────────────
    TELEGRAM_TOKEN: str = field(
        default_factory=lambda: os.getenv("TELEGRAM_TOKEN", "")
    )
    WEBHOOK_SECRET: str = field(
        default_factory=lambda: os.getenv("WEBHOOK_SECRET", "my-secret-token")
    )

    # ── Gemini AI ──────────────────────────────────────────────────────────────
    GEMINI_API_KEY: str = field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY", "")
    )
    GEMINI_MODEL: str = field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    )

    # ── OpenAI (optional fallback) ─────────────────────────────────────────────
    OPENAI_API_KEY: str = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "")
    )
    OPENAI_MODEL: str = field(
        default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )

    # ── Bot Behaviour ──────────────────────────────────────────────────────────
    BOT_NAME: str = field(
        default_factory=lambda: os.getenv("BOT_NAME", "ISTC AI Assistant")
    )
    MAX_HISTORY: int = field(
        default_factory=lambda: int(os.getenv("MAX_HISTORY", "20"))
    )
    AI_PROVIDER: str = field(
        # "gemini" | "openai"
        default_factory=lambda: os.getenv("AI_PROVIDER", "gemini")
    )

    # ── System Prompt ──────────────────────────────────────────────────────────
    SYSTEM_PROMPT: str = field(
        default_factory=lambda: os.getenv(
            "SYSTEM_PROMPT",
            (
                "You are ISTC AI, a helpful, friendly, and intelligent assistant. "
                "You answer questions clearly and concisely. "
                "You can help with coding, writing, analysis, math, and general knowledge. "
                "Always respond in the same language the user writes in."
            ),
        )
    )

    def __post_init__(self):
        if not self.TELEGRAM_TOKEN:
            raise ValueError("❌ TELEGRAM_TOKEN environment variable is not set!")
        if self.AI_PROVIDER == "gemini" and not self.GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY environment variable is not set!")
        if self.AI_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY environment variable is not set!")
