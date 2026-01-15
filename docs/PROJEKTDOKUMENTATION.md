# NährWerk - Intelligentes Ernährungsmanagement System

## 📋 Projektübersicht

NährWerk ist ein KI-gestütztes Ernährungsmanagement-System, das dir hilft:
- Gesunde Ernährung zu planen
- Mahlzeiten zu tracken
- Intelligente Einkaufslisten zu erstellen
- Nahrungsmittel per Foto oder Barcode zu erkennen
- Rezepte zu finden und anzupassen
- Saisonale Empfehlungen zu erhalten

## 🏗️ System-Architektur

```
┌─────────────────┐
│  Slack Bot      │  ← Haupt-Interface
│  (Python)       │     
└────────┬────────┘
         │
         ├──────► Mistral AI (Pixtral Large)
         │        └── Bild-Erkennung
         │        └── Chat/Beratung
         │
         ├──────► Supabase
         │        └── PostgreSQL Datenbank
         │        └── File Storage
         │
         ├──────► APIs
         │        ├── Spoonacular (Rezepte)
         │        ├── Open Food Facts (Produkte)
         │        └── SendGrid (E-Mails)
         │
         └──────► Web Dashboard
                  └── Next.js
                  └── Charts & Reports
```

## 🎯 Hauptfeatures

### ✅ **Phase 1 - Foundation (AKTIV)**

1. **Slack Bot Grundfunktionen**
   - ✅ Chat-Interface
   - ✅ Direkt-Nachrichten
   - ✅ Channel-Integration
   - 🔄 Anamnese-Session (IN ARBEIT)

2. **Bilderkennung**
   - ✅ Pixtral Large Integration
   - 🔄 File-Upload Handler
   - ⏳ Nährwert-Analyse aus Fotos

3. **Einkaufslisten**
   - ✅ KI-generierte Listen
   - ⏳ Persistenz in DB
   - ⏳ Marktvergleich

### 🔄 **Phase 2 - Core Features (GEPLANT)**

4. **Nutzerprofile & Tracking**
   - Haushaltsmitglieder-Verwaltung
   - Allergien & Unverträglichkeiten
   - Ernährungsziele
   - Mahlzeiten-Historie

5. **Rezept-Datenbank**
   - Spoonacular API Integration
   - Filter & Suche
   - Schritt-für-Schritt Anleitung
   - Portionsberechnung

6. **Barcode-Scanner**
   - QR/Barcode-Erkennung
   - Open Food Facts Integration
   - Produktvergleich

### ⏳ **Phase 3 - Advanced (ZUKUNFT)**

7. **Web-Dashboard**
   - Visualisierungen
   - Wochenplanung
   - Reports

8. **E-Mail Reports**
   - Wöchentliche Zusammenfassung
   - Einkaufslisten-Versand
   - Motivations-Tipps

9. **Saisonkalender**
   - Deutsche Saisonzeiten
   - Regionale Empfehlungen

## 🗂️ Projekt-Struktur

```
naehrwerk-bot/
├── main.py                 # Slack Bot Hauptdatei
├── requirements.txt        # Python Dependencies
├── README.md              # Projekt-Readme
│
├── docs/                  # Dokumentation
│   ├── PROJEKTDOKUMENTATION.md    # Diese Datei
│   ├── BEDIENUNGSANLEITUNG.md     # User Guide
│   ├── DATABASE_SCHEMA.md         # DB Schema
│   └── API_DOCUMENTATION.md       # API Docs
│
├── database/              # Datenbank
│   ├── schema.sql        # Supabase Schema
│   ├── migrations/       # DB Migrations
│   └── seeds/            # Test-Daten
│
├── bot/                   # Bot Logik
│   ├── handlers/         # Event Handler
│   │   ├── messages.py
│   │   ├── files.py
│   │   └── onboarding.py
│   ├── services/         # Business Logic
│   │   ├── mistral_service.py
│   │   ├── recipe_service.py
│   │   ├── nutrition_service.py
│   │   └── shopping_list_service.py
│   └── utils/            # Hilfsfunktionen
│
├── web/                   # Web Dashboard (Zukunft)
│   ├── app/              # Next.js App
│   ├── components/       # React Components
│   └── public/           # Static Files
│
└── tests/                 # Tests
    ├── test_bot.py
    └── test_services.py
```

## 🚀 Setup & Installation

Siehe: [BEDIENUNGSANLEITUNG.md](./BEDIENUNGSANLEITUNG.md)

## 📊 Datenbank-Schema

Siehe: [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md)

## 🔗 API-Integrationen

### Mistral AI
- **Model:** Pixtral Large
- **Features:** Bilderkennung, Chat, Ernährungsberatung
- **Kosten:** ~0.02€ pro Bild

### Spoonacular
- **Features:** 5.000+ Rezepte, Nährwertberechnung
- **Free Tier:** 150 requests/Tag
- **Kosten:** 0€ oder $19/Monat

### Open Food Facts
- **Features:** 2+ Mio. Produkte
- **Kosten:** Kostenlos (Open Source)

### SendGrid
- **Features:** E-Mail Versand
- **Free Tier:** 100 E-Mails/Tag
- **Kosten:** Kostenlos

## 💰 Kostenübersicht

| Service | Plan | Kosten/Monat |
|---------|------|-------------|
| **Railway** | Hobby | 5€ (bereits bezahlt) |
| **Supabase** | Free | 0€ |
| **Mistral AI** | Pay-per-use | ~5-10€ |
| **Spoonacular** | Free/Paid | 0€ oder 19€ |
| **SendGrid** | Free | 0€ |
| **Total** | | **5-35€** |

## 📅 Roadmap

### ✅ Aktueller Stand (Januar 2026)
- [x] Slack Bot Basic
- [x] Mistral AI Integration
- [x] Pixtral Large Bilderkennung
- [x] Einkaufslisten-Generierung
- [x] GitHub Repository

### 🔄 In Arbeit (Woche 1-2)
- [ ] Supabase Setup
- [ ] Anamnese-Session
- [ ] Nutzerprofile
- [ ] File-Upload vollständig

### ⏳ Geplant (Woche 3-4)
- [ ] Rezept-API Integration
- [ ] Barcode-Scanner
- [ ] Mahlzeiten-Tracking
- [ ] Saisonkalender

### 🎯 Zukunft (Monat 2+)
- [ ] Web Dashboard
- [ ] E-Mail Reports
- [ ] Mobile PWA
- [ ] Preisvergleich

## 🤝 Mitwirken

Dieses Projekt ist privat für Jörg Schürer entwickelt.

## 📝 Lizenz

Privat - Alle Rechte vorbehalten.

## 📧 Support

Bei Fragen: Slack DM an NährWerk Bot
