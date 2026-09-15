# CivicRoute AI – Intelligent Citizen Complaint Routing System
**Hackathon Working Prototype — Phase 1 Deliverable**

CivicRoute AI is an intelligent civic complaint routing system designed to disaggregate multi-issue citizen grievances, assign AI-assisted priorities with explanations, enforce controlled department routing (preventing AI hallucination), detect existing duplicate complaints using spatial proximity, and equip municipal administrators with hotspot and emerging-issue analytics.

---

## Phase 1 Overview

In **Phase 1**, the complete project architecture, responsive civic-tech interface, and modular Flask backend are fully established with realistic in-memory demo data.

### Key Capabilities in Phase 1:
1. **Multi-Issue Extraction & Controlled Routing Simulation**:
   - Accurately splits compound complaints (e.g. *"The road is damaged and street lights are dead"*) into separate sub-issues assigned to the **Road Department** and **Electricity Department**.
   - Enforces a controlled mapping config across 8 municipal departments (Roads, Water Supply, Electricity, Sanitation, Health, Education, Transport, Other).
2. **Duplicate & Proximity Detection**:
   - Scans nearby active complaints within 500m and presents citizens with choices: **"Join Existing Issue"** or **"Create New Separate Complaint"**.
3. **Citizen Experience**:
   - **Google Sign-In Simulation** (`/login`)
   - **Citizen Profile Management** (`/profile`)
   - **Interactive Complaint Submission** (`/submit`) with plain-text input, location coordinates, browser GPS integration, and photo preview.
   - **AI Recommendation & Confirmation View** (`/confirmation`)
   - **Ticket Tracking & Lifecycle Progress** (`/my-complaints`, `/complaint/<id>`)
   - **Configurable SLA Escalation Alert** (*"Pending for 5 days — escalation recommended"*)
   - **In-App Notification Feed** (`/notifications`) with unread counters.
4. **Administrative Console**:
   - **Executive Dashboard** (`/admin`) with real-time KPI metrics and **Chart.js** charts (Category Doughnut & Department Bar Chart).
   - **Filterable Complaints Table** (`/admin/complaints`) with keyword search, multi-dropdown filtering, and status progression modals.
   - **Hotspots Surveillance** (`/admin/hotspots`) showing localized cluster points (*"Water Supply hotspot — 37 complaints"*).
   - **Emerging Anomaly Analytics** (`/admin/analytics`) showing period-over-period surges (*"Water Supply complaints surged +460%"*).

---

## Project Structure

```
civicroute-ai/
├── app.py                      # Flask entrypoint & route controllers
├── requirements.txt            # Python dependencies (Flask, python-dotenv)
├── .env.example                # Template for environment secrets
├── config/
│   ├── __init__.py
│   └── settings.py             # Controlled categories, departments, SLA thresholds
├── services/
│   ├── __init__.py
│   ├── complaint_service.py    # CRUD operations, in-memory store, SLA logic
│   ├── gemini_service.py       # Multi-issue extraction stub (Phase 5 Gemini hook)
│   ├── duplicate_service.py    # Haversine distance & keyword proximity matching
│   └── hotspot_service.py      # Spatial clustering & emerging surges service
├── utils/
│   ├── __init__.py
│   └── dummy_data.py           # Preloaded realistic municipal records & users
├── templates/
│   ├── base.html               # Shared layout, navbar, role switcher, toast container
│   ├── index.html              # Landing portal & live telemetry
│   ├── login.html              # Google sign-in simulation
│   ├── profile.html            # Citizen profile editing
│   ├── submit_complaint.html   # Grievance registration & duplicate modal
│   ├── confirmation.html       # AI preview & sub-issue breakdown
│   ├── my_complaints.html      # Citizen complaint tracker & filters
│   ├── complaint_detail.html   # Detailed ticket view & lifecycle timeline
│   ├── notifications.html      # In-app notification center
│   ├── admin_dashboard.html    # Executive metrics & Chart.js charts
│   ├── admin_complaints.html   # Admin table with filter & status modal
│   ├── admin_hotspots.html     # Hotspot GIS density grid
│   └── admin_analytics.html    # Period-over-period anomaly reports
├── static/
│   ├── css/
│   │   └── style.css           # Modern, responsive civic-tech styling
│   └── js/
│       ├── main.js             # Toast alerts & modal utilities
│       ├── submit.js           # Form handling, GPS geolocation, duplicate triage
│       └── admin.js            # Chart.js initialization & status updates
└── README.md
```

---

## How to Run the Project

### Prerequisites
- Python 3.10+ (Installed at `C:\Users\Balaji M\AppData\Local\Programs\Python\Python312\python.exe`)

### Step 1: Navigate to the Project Directory
```powershell
cd "c:\Users\Balaji M\civicroute-ai"
```

### Step 2: Install Dependencies (Already performed in setup)
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Start the Flask Development Server
```powershell
python app.py
```
Or using full Python binary path:
```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" app.py
```

### Step 4: Access in Your Browser
Open your browser to:
```
http://127.0.0.1:5000
```

---

## What to Test in Phase 1

1. **Role Switcher & Navigation**:
   - Use the **Citizen View / Admin View** toggle in the top header to effortlessly switch between citizen tracking and the municipal administrative console.
2. **Submit a Multi-Issue Complaint**:
   - Go to **Submit Complaint** (`/submit`).
   - Click the quick button **"⚡ Multi-Issue (Road + Streetlights)"** or type:
     *"The road has deep potholes near the school and the street lights have been broken for days."*
   - Click **Analyze & Proceed to Confirmation**.
   - Notice the AI breakdown screen cleanly disaggregating:
     - **Issue 1**: Road Surface Damage & Potholes &rarr; Road Department (High Priority)
     - **Issue 2**: Street Lighting Failure &rarr; Electricity Department (Medium Priority)
3. **Test Duplicate Detection**:
   - Click **"💧 Water Pipeline Burst"** sample and submit.
   - The system will detect existing ticket `CR-2026-001240` within 500m and open the **"Similar Existing Complaints Found"** modal.
   - Test both choices: *"Join Existing Issue"* and *"Create New Separate Complaint"*.
4. **Track Lifecycle & SLA Escalations**:
   - Go to **My Complaints** (`/my-complaints`).
   - Notice ticket `CR-2026-001241` is highlighted with **"⚠️ Escalation Recommended"** (*"Pending for 6 days — escalation recommended"*).
   - Click on any ticket to view the 5-stage timeline tracker (`SUBMITTED` &rarr; `ASSIGNED` &rarr; `IN PROGRESS` &rarr; `RESOLVED` &rarr; `CLOSED`).
5. **Admin Operations & Hotspots**:
   - Switch to **Admin View**.
   - Review live **Chart.js** category doughnut and department workload charts.
   - Filter tickets by department, priority, or status.
   - Click **"Update"** on any ticket to change its status (e.g. from `ASSIGNED` to `IN PROGRESS`), which instantly emits an in-app notification to the citizen.
   - Navigate to **Hotspots** (`/admin/hotspots`) to inspect spatial clusters (e.g. *Water Supply hotspot — 37 complaints*).

---

## Upcoming Phases Roadmap

- **Phase 2 (Next)**: Firebase Google Authentication integration (live Google Sign-In, Firebase user session, UID token verification).
- **Phase 3**: Firebase Firestore cloud database integration.
- **Phase 4**: Full Firestore complaint submission and persistent ticket creation.
- **Phase 5**: Google Gemini API live prompt integration for multi-issue JSON extraction.
- **Phase 6**: Refined prompt engineering for controlled department mapping and priority reasons.
- **Phase 7**: Firestore-backed geospatial duplicate detection.
- **Phase 8**: Persistent complaint tracking, real-time Firestore listeners, in-app notification triggers.
- **Phase 9**: Admin dashboard connected to live Firestore aggregates.
- **Phase 10**: Google Maps Platform JavaScript SDK, interactive markers, and live heatmap layer.
