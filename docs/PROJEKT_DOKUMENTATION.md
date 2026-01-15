# NährWerk - Projekt Dokumentation

**Erstellt am:** 15. Januar 2026  
**Status:** Aktiv, Private Repository  
**GitHub Repository:** https://github.com/Lord-of-forms/naehrwerk-bot (🔒 Private)

---

## 📋 Projektübersicht

**NährWerk** ist ein intelligenter Slack-Bot für Ernährungsberatung, der Mistral AI nutzt, um personalisierte Ernährungsempfehlungen und Einkaufslisten zu erstellen. Das System besteht aus einem Slack-Bot und einem Web-Dashboard zur Verwaltung von Benutzerdaten.

### Kernfunktionen
- ✅ KI-gestützte Ernährungsberatung über Slack
- ✅ Automatische Mahlzeitenprotokollierung
- ✅ Haushaltsverwaltung (Mitglieder, Allergien, Vorlieben)
- ✅ Intelligente Einkaufslisten-Generierung
- ✅ Bevorzugte Supermärkte und Produktempfehlungen
- ✅ Web-Dashboard zur Datenvisualisierung
- ✅ Rezeptvorschläge und Lieblingsrezepte

---

## 🔐 Zugangsdaten & Schlüssel

### Slack App
- **App Name:** NährWerk
- **App ID:** A0A8RPDLU0M
- **Workspace:** Jörg Schürer Slack (T070X6X7K61)
- **Konfiguration:** https://api.slack.com/apps/A0A8RPDLU0M
- **Environment Variables:**
  - `SLACK_BOT_TOKEN` - Bot User OAuth Token (in Railway gesetzt)
  - `SLACK_APP_TOKEN` - App-Level Token für Socket Mode (in Railway gesetzt)

### Mistral AI
- **Konsole:** https://console.mistral.ai/
- **Agent ID:** ag_019bc020b7457203aa8c980923d6706e
- **Playground:** https://console.mistral.ai/build/playground?agentId=ag_019bc020b7457203aa8c980923d6706e
- **Environment Variable:**
  - `MISTRAL_API_KEY` - API Key für Mistral AI (in Railway gesetzt)
  - `AGENT_ID` - Agent ID (in Railway gesetzt)

### Supabase (Datenbank)
- **Projekt Name:** naehrwerk
- **Projekt ID:** mtwsrdcpvbilpgzwfbyd
- **Dashboard:** https://supabase.com/dashboard/project/mtwsrdcpvbilpgzwfbyd
- **API Settings:** https://supabase.com/dashboard/project/mtwsrdcpvbilpgzwfbyd/settings/api-keys
- **Environment Variables:**
  - `SUPABASE_URL` - https://mtwsrdcpvbilpgzwfbyd.supabase.co
  - `SUPABASE_KEY` - Anon/Public Key (für client-seitige Operationen)
  - `SUPABASE_SERVICE_KEY` - Service Role Key (für server-seitige Operationen)

**⚠️ Wichtig:** RLS (Row Level Security) ist für folgende Tabellen **DEAKTIVIERT**:
- `users`
- `meals`
- `household_members`
- `shopping_lists`
- `shopping_list_items`
- `products`

### Railway (Hosting)
- **Projekt:** tender-charisma
- **Projekt ID:** 2d1c1e9f-4fed-414c-8a63-b01b1ba29f3e
- **Dashboard:** https://railway.com/project/2d1c1e9f-4fed-414c-8a63-b01b1ba29f3e
- **Service Name:** naehrwerk-bot
- **Production URL:** https://naehrwerk-bot-production.up.railway.app
- **Environment:** production
- **Start Command:** `python dashboard.py` (Dashboard) / `python bot.py` (Bot)
- **Port:** 5000

---

## 🗄️ Datenbankstruktur (Supabase)

### Tabelle: `users`
- `id` (bigint, PK) - Auto-increment User ID
- `slack_user_id` (text, unique) - Slack User ID
- `slack_name` (text) - Slack Display Name
- `created_at` (timestamp) - Erstellungsdatum

### Tabelle: `household_members`
- `id` (bigint, PK)
- `user_id` (bigint, FK → users)
- `name` (text) - Name des Haushaltsmitglieds
- `age` (int) - Alter
- `gender` (text) - Geschlecht
- `activity_level` (text) - Aktivitätslevel
- `health_conditions` (text) - Gesundheitszustände
- `allergies` (text) - Allergien
- `dietary_preferences` (text) - Ernährungspräferenzen
- `created_at` (timestamp)

### Tabelle: `meals`
- `id` (bigint, PK)
- `user_id` (bigint, FK → users)
- `meal_description` (text) - Mahlzeitenbeschreibung
- `meal_type` (text) - Frühstück, Mittagessen, Abendessen, Snack
- `created_at` (timestamp)

### Tabelle: `shopping_lists`
- `id` (bigint, PK)
- `user_id` (bigint, FK → users)
- `created_at` (timestamp)

### Tabelle: `shopping_list_items`
- `id` (bigint, PK)
- `shopping_list_id` (bigint, FK → shopping_lists)
- `item_name` (text) - Produktname
- `quantity` (text) - Menge
- `unit` (text) - Einheit (kg, Stück, etc.)
- `category` (text) - Kategorie (Obst, Gemüse, etc.)

### Tabelle: `preferred_markets`
- `id` (bigint, PK)
- `user_id` (bigint, FK → users)
- `market_name` (text) - Supermarktname
- `created_at` (timestamp)

### Tabelle: `products`
- `id` (bigint, PK)
- `name` (text) - Produktname
- `category` (text) - Kategorie
- `description` (text) - Beschreibung
- `created_at` (timestamp)

### Tabelle: `favorite_recipes`
- `id` (bigint, PK)
- `user_id` (bigint, FK → users)
- `recipe_name` (text) - Rezeptname
- `recipe_description` (text) - Rezeptbeschreibung
- `ingredients` (text) - Zutaten
- `created_at` (timestamp)

---

## 📂 Projektstruktur

```
naehrwerk-bot/
├── bot.py                          # Hauptbot-Logik (Slack Socket Mode)
├── dashboard.py                    # Flask Web-Dashboard
├── main.py                         # Legacy/Alternativer Entry Point
├── requirements.txt                # Python Dependencies
├── templates/                      # HTML Templates für Dashboard
│   ├── index.html                 # Benutzerübersicht
│   └── user_dashboard.html        # Einzelbenutzer-Dashboard
├── docs/                           # Dokumentation
│   └── PROJEKT_DOKUMENTATION.md   # Diese Datei
└── README.md                       # Projekt-README
```

---

## 🔧 Verwendete Technologien & Services

### Backend
- **Python 3.13.11**
- **slack-bolt** - Slack Bot Framework (Socket Mode)
- **Flask 3.1.0** - Web Framework für Dashboard
- **Supabase Python Client** - Datenbankzugriff
- **Mistral AI SDK** - KI-Integration

### Frontend (Dashboard)
- **Jinja2 Templates** - HTML Templating
- **CSS** - Responsive Design mit Gradient-Styling

### Infrastruktur
- **Railway** - PaaS für Deployment
- **Supabase** - PostgreSQL Datenbank (Backend as a Service)
- **Mistral AI** - Large Language Model Agent
- **Slack** - Messaging Platform & API
- **GitHub** - Version Control (Private Repository)

---

## 🚀 Deployment & Betrieb

### Railway Konfiguration

**Environment Variables (alle in Railway gesetzt):**
```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
MISTRAL_API_KEY=...
AGENT_ID=ag_019bc020b7457203aa8c980923d6706e
SUPABASE_URL=https://mtwsrdcpvbilpgzwfbyd.supabase.co
SUPABASE_KEY=... (Anon Key)
SUPABASE_SERVICE_KEY=sb_secret_2PmpdgZqjspz29vp02vqeO_XRivco43
```

**Start Command:**
- Bot: `python bot.py`
- Dashboard: `python dashboard.py`

**Port:** 5000

**Region:** Europe West 4 (Drams 3g)

### Deployment-Prozess
1. Code-Änderungen in GitHub pushen
2. Railway erkennt automatisch Änderungen (GitHub Integration)
3. Neues Deployment wird automatisch gestartet
4. Service läuft nach erfolgreichem Build

---

## 🔗 Wichtige Links

### Entwicklung & Administration
- **GitHub Repo:** https://github.com/Lord-of-forms/naehrwerk-bot
- **Railway Dashboard:** https://railway.com/project/2d1c1e9f-4fed-414c-8a63-b01b1ba29f3e
- **Supabase Dashboard:** https://supabase.com/dashboard/project/mtwsrdcpvbilpgzwfbyd
- **Mistral AI Console:** https://console.mistral.ai/
- **Slack API Dashboard:** https://api.slack.com/apps/A0A8RPDLU0M

### Produktiv-URLs
- **Dashboard:** https://naehrwerk-bot-production.up.railway.app
- **Slack Workspace:** Jörg Schürer Slack

---

## 📝 Wichtige Hinweise

### Sicherheit
- ✅ Repository ist auf **Private** gesetzt
- ✅ Alle API-Keys sind als Environment Variables in Railway gespeichert
- ✅ RLS in Supabase ist für Haupttabellen deaktiviert (Server-seitiger Zugriff)
- ⚠️ NIEMALS API-Keys oder Secrets im Code committen!

### Bekannte Probleme & Lösungen
- **Problem:** Dashboard zeigt "Invalid API key" → **Lösung:** `SUPABASE_SERVICE_KEY` statt `SUPABASE_KEY` in `dashboard.py` verwenden
- **Problem:** Keine Daten trotz korrektem Key → **Lösung:** RLS in Supabase deaktivieren
- **Problem:** 502 Bad Gateway → **Lösung:** Railway Logs prüfen, Service neu starten

### Nächste Schritte / TODOs
- [ ] Dashboard läuft aktuell nicht (502 Error) - weitere Fehleranalyse notwendig
- [ ] RLS-Policies für Produktiv-Umgebung definieren (aktuell deaktiviert)
- [ ] Monitoring & Logging verbessern
- [ ] Backup-Strategie für Supabase-Datenbank
- [ ] Tests für Bot-Funktionen schreiben

---

## 📞 Support & Kontakt

**Entwickler:** Lord-of-forms  
**GitHub:** https://github.com/Lord-of-forms  
**Slack Workspace:** Jörg Schürer Slack

---

**Letzte Aktualisierung:** 15. Januar 2026, 15:00 CET
