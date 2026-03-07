#!/usr/bin/env python3
"""Telegram bot interface for defensive query parsing."""

from __future__ import annotations

import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from dork_parser import parse_query, to_json


def format_help() -> str:
    return (
        "Send me any search-style query and I will analyze risk signals.\n\n"
        "Commands:\n"
        "/start - welcome\n"
        "/help - show help\n"
        "/analyze <query> - parse a query explicitly"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Defensive Query Parser Bot ready.\n" + format_help())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_help())


async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip()
    if not query:
        await update.message.reply_text("Usage: /analyze <query>")
        return

    result = parse_query(query)
    await update.message.reply_text(f"```json\n{to_json(result)}\n```", parse_mode="Markdown")


async def analyze_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = (update.message.text or "").strip()
    if not query:
        await update.message.reply_text("Empty message mila. Query bhejo.")
        return

    result = parse_query(query)
    await update.message.reply_text(f"```json\n{to_json(result)}\n```", parse_mode="Markdown")


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is required")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyze", analyze_text))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_message))

    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
