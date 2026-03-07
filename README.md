# Defensive Query Parser (Telegram Bot Controlled)

Ab tool CLI-focused nahi, **Telegram bot controlled** hai.

## What it does

- Query tokenize karta hai (quoted strings supported).
- Operators parse karta hai (`site:`, `filetype:`, `inurl:` etc.).
- Risk signals detect karta hai (password/secret keywords, sensitive file names, `index of`).
- JSON result bhejta hai with `risk_score` and recommendation.

## Setup

1. Python dependency install karo:

```bash
pip install python-telegram-bot==20.7
```

2. Bot token set karo:

```bash
export TELEGRAM_BOT_TOKEN="<your_bot_token>"
```

3. Bot run karo:

```bash
python3 telegram_bot.py
```

## Bot usage

- `/start`
- `/help`
- `/analyze site:example.com filetype:pdf annual report`
- Ya direct koi query text bhejo; bot auto parse karega.

## Run tests

```bash
python3 -m unittest tests_parser.py
```
