# NährWerk - Telegram Migration Plan

**Erstellt am:** 15. Januar 2026, 22:00 CET  
**Status:** Planung  
**Ziel:** Migration von Slack zu Telegram für einfachere Entwicklung und Wartung

---

## 📊 Zusammenfassung

Dieser Plan beschreibt die Migration des NährWerk Ernährungsbot von Slack zu Telegram. Die Analyse hat gezeigt, dass Telegram deutlich einfacher zu implementieren und zu warten ist.

### Hauptvorteile der Migration:
- ✅ **30-40% weniger Code** - Einfachere API
- ✅ **Kein Socket Mode** - Direktes HTTP Polling
- ✅ **Simpleres Setup** - Nur ein Bot-Token nötig
- ✅ **Bessere Performance** bei Bild-Uploads
- ✅ **Leichtgewichtigere Dependencies**

---

## 🔄 Migrations-Phasen

### Phase 1: Vorbereitung (1-2 Stunden)

#### 1.1 Telegram Bot erstellen
- [ ] Bei @BotFather einen neuen Bot registrieren
- [ ] Bot-Token erhalten und sicher speichern
- [ ] Bot-Namen und Beschreibung konfigurieren
- [ ] Bot-Befehle definieren (/start, /help, /meal, etc.)

#### 1.2 Projekt-Setup
- [ ] Neuen Branch `telegram-migration` erstellen
- [ ] `requirements.txt` aktualisieren:
  ```
  python-telegram-bot==20.7
  mistralai==1.2.4
  supabase==2.9.1
  requests
  ```
- [ ] Alte Slack-Dependencies entfernen

---

### Phase 2: Code-Migration (3-4 Stunden)

#### 2.1 Neue Dateistruktur
```
naehrwerk-bot/
├── telegram_bot.py      # Haupt-Bot-Logik (NEU)
├── handlers/            # Event Handler (NEU)
│   ├── __init__.py
│   ├── message.py      # Text-Nachrichten
│   ├── photo.py        # Bild-Uploads
│   └── commands.py     # Bot-Befehle
├── database.py          # Supabase Helper (übernehmen von alt)
├── mistral_client.py    # Mistral AI Helper (übernehmen von alt)
├── dashboard.py         # Flask Dashboard (unverändert)
├── requirements.txt     # Aktualisiert
└── docs/
    ├── PROJEKT_DOKUMENTATION.md
    └── TELEGRAM_MIGRATION_PLAN.md  # Diese Datei
```

#### 2.2 Core-Komponenten migrieren

**`telegram_bot.py` - Haupteinstiegspunkt:**
```python
#!/usr/bin/env python3
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import message, photo, commands
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def main():
    logger.info("🍏 NährWerk Telegram Bot starting...")
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Command Handlers
    app.add_handler(CommandHandler("start", commands.start))
    app.add_handler(CommandHandler("help", commands.help_command))
    app.add_handler(CommandHandler("meal", commands.log_meal))
    
    # Message Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message.handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, photo.handle_photo))
    
    logger.info("✅ Bot running!")
    app.run_polling()

if __name__ == "__main__":
    main()
```

**`handlers/message.py` - Text-Handler:**
```python
from telegram import Update
from telegram.ext import ContextTypes
from mistral_client import get_ai_response
from database import create_or_get_user
import logging

logger = logging.getLogger(__name__)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    logger.info(f"📩 Message from {user_id}: {text}")
    
    # User in DB anlegen/holen
    db_user = create_or_get_user(str(user_id))
    
    # Konversationshistorie verwalten
    if 'conversation' not in context.user_data:
        context.user_data['conversation'] = []
    
    context.user_data['conversation'].append({"role": "user", "content": text})
    
    # AI Response holen
    response = get_ai_response(context.user_data['conversation'])
    context.user_data['conversation'].append({"role": "assistant", "content": response})
    
    await update.message.reply_text(response)
    logger.info("✅ Response sent")
```

**`handlers/photo.py` - Bild-Handler:**
```python
from telegram import Update
from telegram.ext import ContextTypes
import base64
import logging
from mistral_client import get_ai_response_with_image

logger = logging.getLogger(__name__)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"📷 Photo from {user_id}")
    
    # Größtes Foto holen
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    
    # Bild herunterladen
    photo_bytes = await file.download_as_bytearray()
    image_base64 = base64.b64encode(photo_bytes).decode('utf-8')
    
    # AI Analyse
    response = get_ai_response_with_image(image_base64, user_id)
    
    await update.message.reply_text(response)
    logger.info("✅ Image analysis sent")
```

#### 2.3 Datenbank-Layer (unverändert übernehmen)
- [ ] `database.py` aus `main.py` extrahieren
- [ ] Funktionen beibehalten:
  - `create_or_get_user()`
  - `save_meal()`
  - Alle anderen DB-Funktionen

#### 2.4 Mistral AI Client (übernehmen und anpassen)
- [ ] `mistral_client.py` erstellen
- [ ] Functions aus `main.py` übernehmen
- [ ] Anpassungen für Telegram-spezifische User-IDs

---

### Phase 3: Testing (2-3 Stunden)

#### 3.1 Lokale Tests
- [ ] Bot lokal starten: `python telegram_bot.py`
- [ ] Test: Text-Nachrichten senden
- [ ] Test: Bilder senden
- [ ] Test: `/start`, `/help` Befehle
- [ ] Test: Konversationshistorie (mehrere Nachrichten)
- [ ] Test: Mahlzeiten-Logging
- [ ] Test: Datenbankanbindung (Supabase)

#### 3.2 Railway Deployment Test
- [ ] Environment Variables in Railway setzen:
  - `TELEGRAM_BOT_TOKEN`
  - `MISTRAL_API_KEY`
  - `AGENT_ID`
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
- [ ] Start Command ändern: `python telegram_bot.py`
- [ ] Deployment triggern
- [ ] Logs überprüfen
- [ ] Live-Tests durchführen

---

### Phase 4: Produktion (1 Stunde)

#### 4.1 Finales Deployment
- [ ] Branch `telegram-migration` in `main` mergen
- [ ] GitHub Push
- [ ] Railway Auto-Deploy abwarten
- [ ] Production-Tests

#### 4.2 Dokumentation aktualisieren
- [ ] README.md aktualisieren
- [ ] PROJEKT_DOKUMENTATION.md aktualisieren
- [ ] Telegram-spezifische Infos hinzufügen
- [ ] Alte Slack-Referenzen entfernen

#### 4.3 Cleanup
- [ ] Alte Dateien löschen:
  - `main.py` (Slack-Version)
  - Slack-spezifische Imports entfernen
- [ ] Branch `telegram-migration` löschen (optional)

---

## 🔑 Environment Variables

### Zu ändern in Railway:
```bash
# ENTFERNEN:
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# HINZUFÜGEN:
TELEGRAM_BOT_TOKEN=<Bot-Token von @BotFather>

# BEHALTEN:
MISTRAL_API_KEY=...
AGENT_ID=ag_019bc020b7457203aa8c980923d6706e
SUPABASE_URL=https://mtwsrdcpvbilpgzwfbyd.supabase.co
SUPABASE_KEY=...
SUPABASE_SERVICE_KEY=...
```

---

## 📋 Code-Vergleich: Slack vs. Telegram

### Slack (alt) - Komplexer:
```python
# Socket Mode Setup
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_mention(event, say, client):
    user_id = event["user"]
    text = re.sub(r'<@[A-Z0-9]+>', '', event.get("text", "")).strip()
    # ... komplexe Logik

handler = SocketModeHandler(app, SLACK_APP_TOKEN)
handler.start()
```

### Telegram (neu) - Einfacher:
```python
# Direktes Polling
from telegram.ext import Application, MessageHandler, filters

app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    # ... einfache Logik

app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
```

**Ergebnis:** 40% weniger Code, keine WebSocket-Komplexität

---

## ⚠️ Wichtige Hinweise

### User-ID Migration
- **Slack:** User-IDs sind alphanumerisch (z.B. `U0A8RPDLU0M`)
- **Telegram:** User-IDs sind numerisch (z.B. `123456789`)
- **Lösung:** Supabase `users.slack_user_id` → `users.telegram_user_id` umbenennen
  ```sql
  ALTER TABLE users RENAME COLUMN slack_user_id TO telegram_user_id;
  ```

### Bild-Handling
- **Slack:** Komplexer Download mit OAuth-Headers
- **Telegram:** Direkter Download via `get_file()`

### Konversations-Persistenz
- **Slack:** Global Dictionary `conversations = {}`
- **Telegram:** `context.user_data` (pro User isoliert)

---

## 📚 Ressourcen

### Telegram Bot API
- **Offizielle Docs:** https://core.telegram.org/bots/api
- **python-telegram-bot Docs:** https://docs.python-telegram-bot.org/
- **@BotFather:** Bot-Registrierung in Telegram

### Tutorials
- python-telegram-bot Tutorial: https://github.com/python-telegram-bot/python-telegram-bot/wiki

---

## ✅ Checkliste vor Go-Live

- [ ] Alle Tests erfolgreich (lokal + Railway)
- [ ] Environment Variables korrekt gesetzt
- [ ] Datenbank-Migration durchgeführt
- [ ] Dokumentation aktualisiert
- [ ] Alte Slack-App deaktiviert (optional)
- [ ] Team über neue Telegram-Bot informiert

---

## 🎯 Erfolgs-Kriterien

✅ Bot antwortet auf Text-Nachrichten  
✅ Bot analysiert Bilder korrekt  
✅ Konversationshistorie funktioniert  
✅ Datenbank-Logging funktioniert  
✅ Railway Deployment läuft stabil  
✅ Keine kritischen Fehler in Logs

---

**Geschätzte Gesamtdauer:** 7-10 Stunden
**Risiko:** Niedrig - Gut getestete Libraries
**ROI:** Hoch - Deutlich einfachere Wartung

**Nächster Schritt:** Phase 1 starten - Bot bei @BotFather erstellen
