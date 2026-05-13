import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ====== API KEYS (Render pe set karenge) ======
TELEGRAM_TOKEN = os.environ.get("8240194797:AAEz49nJCGeBetTqdcUKKO-NYTevDpsRNqg")
GROQ_API_KEY = os.environ.get("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")

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====== AI FUNCTION ======
def ask_ai(message):
    """Groq AI se jawab lega"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful Indian assistant. Reply in Hinglish (Hindi in Roman script) or English based on user's language. Be friendly and casual."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Bhai kuch error aaya: {str(e)}"

# ====== TELEGRAM COMMANDS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 Namaste bhai! Main AI bot hoon.\n\n"
        "Mujhse kuch bhi pooch lo:\n"
        "• Gyan / Padhai\n"
        "• Coding help\n"
        "• Koi bhi sawaal\n\n"
        "Bas message bhejo!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Commands:\n"
        "/start - Bot shuru\n"
        "/help - Madad\n\n"
        "Bas normal message bhejo, main jawab dunga!"
    )

# ====== MESSAGE HANDLER ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_name = update.effective_user.first_name
    
    logger.info(f"Message from {user_name}: {user_msg}")
    
    # Typing dikhaye
    await update.message.chat.send_action(action="typing")
    
    # AI se jawab
    reply = ask_ai(user_msg)
    
    # Reply bheje
    await update.message.reply_text(reply)

# ====== ERROR HANDLER ======
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("Bhai kuch gadbad ho gayi, dobara try karo!")

# ====== MAIN ======
def main():
    # App create
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    # Chalao
    logger.info("🚀 Bot chal raha hai bhai!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
