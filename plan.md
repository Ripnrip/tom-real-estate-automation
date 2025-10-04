# AppFolio Automation System - Project Brief

## Overview
Automated property management system using n8n to scrape AppFolio data, analyze financial reports, monitor documents, and send notifications.

## Tech Stack
- **Platform**: n8n (workflow automation)
- **Browser**: BrowserUse / Playwright / Puppeteer (web scraping)
- **Storage**: Local server + Google Drive
- **Format**: Google Sheets + CSV
- **Alerts**: SMS (provider TBD, phone TBD)

## Core Workflows

### 1. Daily Ledger Download
**Trigger**: Manual
- Login to AppFolio via browser automation
- Download ledger report
- Save to local: `/appfolio/ledgers/YYYY-MM-DD/`
- Backup to Google Drive: `/AppFolio/Ledgers/`

### 2. Ledger Analysis
**Trigger**: Auto (after download)
- Parse ledger data into structured format
- Create Google Sheet with columns:
  - Original data (Date, Description, Amount, Category, Property)
  - Analysis (Comments, Patterns, Flags, Details per line item)
- Use AI to categorize and annotate each transaction
- Export CSV to local server

### 3. Trend Analysis
**Trigger**: Auto (after analysis)
- Compare current vs historical data
- Identify patterns in revenue, expenses, maintenance
- Flag anomalies (criteria TBD)
- Add "Trends" tab to Google Sheet

### 4. Document Monitor
**Trigger**: Manual (daily)
- Scrape AppFolio for new documents:
  - Leases
  - PMAs (Property Management Agreements)
  - Work order receipts
- Download new items to organized folders
- Upload to Google Drive
- Track in database/manifest

### 5. SMS Notifications
**Trigger**: Auto (after jobs complete)
- Send summary of completed tasks
- Include new document count
- Share Google Sheets link
- Alert on errors

## Folder Structure

/local/server/appfolio/
├── ledgers/YYYY-MM-DD/
├── analyzed/YYYY-MM-DD.csv
├── leases/
├── pmas/
└── work-orders/

## Implementation Phases
1. ✅ **Setup**: n8n instance + browser automation test
2. 🔨 **Phase 1**: Login + ledger download workflow
3. 🔨 **Phase 2**: Data parsing + Google Sheets generation
4. 🔨 **Phase 3**: AI analysis + trend detection
5. 🔨 **Phase 4**: Document monitoring system
6. 🔨 **Phase 5**: SMS notification integration

## Immediate Tasks
- [ ] Set up n8n environment
- [ ] Test Playwright/Puppeteer with AppFolio login
- [ ] Map AppFolio DOM selectors (login, reports, documents)
- [ ] Create local folder structure
- [ ] Configure Google Drive API in n8n
- [ ] Select SMS provider (Twilio recommended)
- [ ] Define trend analysis criteria
- [ ] Choose phone number for alerts
