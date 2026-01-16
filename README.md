# naehrwerk-bot
Slack Bot für Ernährungsberatung mit Mistral AI

## 🚀 Setup

### Telegram Bot erstellen

1. In Telegram @BotFather öffnen
2. `/newbot` ausführen
3. Botname und Username vergeben
4. `TELEGRAM_BOT_TOKEN` vom BotFather erhalten und sichern

### Umgebungsvariablen setzen

1. Kopiere `.env.example` zu `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fülle die Werte in `.env` aus:
   - `TELEGRAM_BOT_TOKEN`: Dein Telegram Bot Token
   - `MISTRAL_API_KEY`: Dein Mistral AI API Key
   - `SUPABASE_URL`: Deine Supabase URL
   - `SUPABASE_KEY`: Dein Supabase Service Key

### Installation

```bash
# Dependencies installieren
pip install -r requirements.txt

# Telegram Bot starten
python telegram_bot.py
```

### Deployment auf Railway

1. Setze die Umgebungsvariablen in Railway:
   - `TELEGRAM_BOT_TOKEN`
   - `MISTRAL_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

2. Start-Befehl: `python telegram_bot.py`

## 📱 Nutzung

- `/start` - Begrüßung und Einführung
- `/help` - Hilfe anzeigen
- Sende Textnachrichten für Ernährungsberatung
- Lade Fotos deines Essens hoch für Analyse
