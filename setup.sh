#!/usr/bin/env bash
# setup.sh — interactive first-time setup for the Car Recommendation Bot
set -euo pipefail

echo ""
echo "🚗  Car Recommendation Bot — setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 1. Token ──────────────────────────────────────────────────────────────────
if [ -f ".env" ] && grep -q "^API_TOKEN=." .env 2>/dev/null; then
    echo "✅  .env already contains a token — skipping token prompt."
    echo "    (Delete .env and re-run setup.sh to change the token.)"
else
    echo "Step 1 of 3 — Telegram Bot Token"
    echo ""
    echo "  How to get a token:"
    echo "  1. Open Telegram and search for @BotFather"
    echo "  2. Send /newbot and follow the prompts"
    echo "  3. Copy the token BotFather gives you (looks like 123456789:AAF...)"
    echo ""
    read -rp "  Paste your token here: " TOKEN

    if [ -z "$TOKEN" ]; then
        echo "❌  No token entered. Aborting."
        exit 1
    fi

    cp .env.example .env
    # Replace the placeholder value (works on both Linux and macOS)
    sed -i.bak "s|your_bot_token_here|${TOKEN}|" .env && rm -f .env.bak
    echo "✅  Token saved to .env"
fi

echo ""

# ── 2. Dependencies ───────────────────────────────────────────────────────────
echo "Step 2 of 3 — Installing Python dependencies"
pip install -r requirements.txt
echo "✅  Dependencies installed"

echo ""

# ── 3. Start ──────────────────────────────────────────────────────────────────
echo "Step 3 of 3 — Starting the bot"
echo ""
echo "  Your bot is now running.  Press Ctrl+C to stop it."
echo "  Once running, open Telegram and send /start to your bot."
echo ""

python bot.py
