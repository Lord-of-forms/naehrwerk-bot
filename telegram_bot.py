import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update, context):
    """Handler für /start Befehl"""
    await update.message.reply_text(
        "Willkommen bei NährWerk 👋\n\n"
        "Ich unterstütze dich bei Ernährung, Rezepten und deinem Coaching.\n\n"
        "Nutze /help um alle verfügbaren Befehle zu sehen."
    )


async def help_command(update, context):
    """Handler für /help Befehl"""
    help_text = (
        "🔹 *Verfügbare Befehle:*\n\n"
        "/start - Begrüßung und Einführung\n"
        "/help - Diese Hilfe anzeigen\n\n"
        "📝 *So nutzt du mich:*\n"
        "• Schreibe mir deine Fragen zur Ernährung\n"
        "• Lade ein Foto deines Essens hoch für eine Analyse\n"
        "• Frage nach Rezeptvorschlägen\n\n"
        "Ich bin für dich da! 💪"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def handle_message(update, context):
    """Handler für Textnachrichten"""
    user_message = update.message.text
    logger.info(f"Received message from {update.effective_user.id}: {user_message}")
    
    await update.message.reply_text(
        "Danke für deine Nachricht! 🙌\n\n"
        "Die intelligente Auswertung mit Mistral AI wird in Kürze aktiviert.\n"
        "Bleib dran!"
    )


async def handle_photo(update, context):
    """Handler für Foto-Uploads"""
    logger.info(f"Received photo from {update.effective_user.id}")
    
    await update.message.reply_text(
        "📸 Foto erhalten!\n\n"
        "Die Bild-Analyse wird bald verfügbar sein.\n"
        "Danke für deine Geduld!"
    )


def main():
    """Hauptfunktion zum Starten des Bots"""
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN ist nicht gesetzt.\n"
            "Bitte setze die Umgebungsvariable oder erstelle eine .env Datei."
        )

    # Bot-Anwendung erstellen
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handler registrieren
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("🚀 NährWerk Telegram Bot wird gestartet...")
    logger.info("Bot läuft im Polling-Modus. Drücke Ctrl+C zum Beenden.")
    
    # Bot starten
    app.run_polling()


if __name__ == "__main__":
    main()
