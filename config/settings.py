import os

# Application Settings
APP_NAME = "CivicRoute AI"
APP_TAGLINE = "Department-Based Government Grievance Management System"
PROJECT_CODE = "GOV-21"
VERSION = "2.0.0-gov21"
SECRET_KEY = os.environ.get("SECRET_KEY", "civicroute_dev_secret_key_2026")

# Central Category -> Official Department Mapping (Section 3)
CATEGORY_DEPARTMENT_MAPPING = {
    "Roads & Potholes": "Public Works Department (PWD) – Roads Division",
    "Water Supply": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
    "Electricity": "Tamil Nadu Generation and Distribution Corporation (TANGEDCO)",
    "Waste Management": "Municipal Corporation – Solid Waste Management Department",
    "Drainage & Sewage": "Municipal Corporation – Sewerage & Drainage Department",
    "Public Transport": "Metropolitan Transport Corporation (MTC) / State Transport Corporation",
    "Street Lighting": "Municipal Corporation – Electrical / Street Lighting Division",
    "Public Safety": "Tamil Nadu Police – Local Police Station",
    "Parks & Public Spaces": "Municipal Corporation – Parks & Open Spaces Department",
    "Government Services": "District Collectorate / District Administration",
    "Noise Pollution": "Tamil Nadu Pollution Control Board (TNPCB) – District Office",
    "Other": "Municipal Corporation – Public Grievance Cell"
}

# Predefined Demo Admin Accounts & Department Mapping (Section 1 & 14)
# Must use official-looking @gov.in email format
ADMIN_DEPARTMENT_MAPPING = {
    "pwd.admin@gov.in": {
        "name": "PWD Roads Division Officer",
        "category": "Roads & Potholes",
        "department": "Public Works Department (PWD) – Roads Division",
        "shortDept": "PWD – Roads Division"
    },
    "water.admin@gov.in": {
        "name": "TWAD Board Assistant Engineer",
        "category": "Water Supply",
        "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
        "shortDept": "TWAD Board"
    },
    "electricity.admin@gov.in": {
        "name": "TANGEDCO Section Superintendent",
        "category": "Electricity",
        "department": "Tamil Nadu Generation and Distribution Corporation (TANGEDCO)",
        "shortDept": "TANGEDCO"
    },
    "municipal.waste.admin@gov.in": {
        "name": "Sanitary Inspector (Solid Waste)",
        "category": "Waste Management",
        "department": "Municipal Corporation – Solid Waste Management Department",
        "shortDept": "Solid Waste Management"
    },
    "municipal.drainage.admin@gov.in": {
        "name": "Drainage & Sewerage In-Charge",
        "category": "Drainage & Sewage",
        "department": "Municipal Corporation – Sewerage & Drainage Department",
        "shortDept": "Sewerage & Drainage"
    },
    "transport.admin@gov.in": {
        "name": "MTC Transit Operations Manager",
        "category": "Public Transport",
        "department": "Metropolitan Transport Corporation (MTC) / State Transport Corporation",
        "shortDept": "MTC / Transport Corp"
    },
    "streetlight.admin@gov.in": {
        "name": "Electrical Division Supervisor",
        "category": "Street Lighting",
        "department": "Municipal Corporation – Electrical / Street Lighting Division",
        "shortDept": "Street Lighting Division"
    },
    "police.admin@gov.in": {
        "name": "Law & Order Duty Officer",
        "category": "Public Safety",
        "department": "Tamil Nadu Police – Local Police Station",
        "shortDept": "TN Police"
    },
    "parks.admin@gov.in": {
        "name": "Horticulture & Parks Officer",
        "category": "Parks & Public Spaces",
        "department": "Municipal Corporation – Parks & Open Spaces Department",
        "shortDept": "Parks & Open Spaces"
    },
    "collectorate.admin@gov.in": {
        "name": "District Revenue / Collectorate Officer",
        "category": "Government Services",
        "department": "District Collectorate / District Administration",
        "shortDept": "District Administration"
    },
    "tnpcb.admin@gov.in": {
        "name": "Pollution Control Environmental Officer",
        "category": "Noise Pollution",
        "department": "Tamil Nadu Pollution Control Board (TNPCB) – District Office",
        "shortDept": "TNPCB District Office"
    },
    "grievance.admin@gov.in": {
        "name": "Chief Public Grievance Officer",
        "category": "Other",
        "department": "Municipal Corporation – Public Grievance Cell",
        "shortDept": "Public Grievance Cell"
    }
}

# SLA Durations (in days) based on Priority (Section 7)
PRIORITY_SLA_DAYS = {
    "HIGH": 3,
    "MEDIUM": 7,
    "LOW": 15
}

# Standard Priority Definitions
PRIORITY_LEVELS = ["HIGH", "MEDIUM", "LOW"]

# Daily Processing Limit per Department Admin (Section 5)
DAILY_PROCESSING_LIMIT = 5

# Escalation Officer Tier
ESCALATION_SUPERVISOR_TITLE = "Department Senior Officer / District Grievance Officer"

# Ticket Lifecycle Stages (Section 9)
TICKET_STATUSES = [
    "SUBMITTED",
    "ASSIGNED",
    "IN PROGRESS",
    "RESOLVED"
]

# Proximity threshold for duplicate complaint detection (in kilometers)
PROXIMITY_THRESHOLD_KM = 0.5

# Default geographic center (Metro Municipal Corporation demo area)
DEFAULT_LATITUDE = 13.0827
DEFAULT_LONGITUDE = 80.2707
DEFAULT_CITY_NAME = "Chennai Metropolitan Area"
