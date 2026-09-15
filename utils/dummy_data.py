from datetime import datetime, timedelta

# Default Mock Citizen (Section 1: @gmail.com or normal email)
CURRENT_MOCK_USER = {
    "uid": "usr_citizen_9821a",
    "name": "Demo Citizen",
    "email": "citizen@example.com",
    "phone": "+91 98765 43210",
    "preferredLanguage": "English",
    "defaultLocation": "Ward 4, Anna Nagar, Chennai",
    "latitude": 13.0850,
    "longitude": 80.2101,
    "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
}

# Notification list for Citizen & Admin Demo
INITIAL_NOTIFICATIONS = [
    {
        "id": "notif_001",
        "ticketId": "GOV-10480",
        "title": "Complaint Resolved",
        "message": "Street lighting restoration completed on 2nd Avenue. Resolution Note: Replaced blown ballast capacitor and restored power feed to 5 light poles.",
        "type": "success",
        "timestamp": (datetime.now() - timedelta(hours=3)).strftime("%d %b %Y, %H:%M"),
        "isRead": False,
        "resolutionNote": "Replaced blown ballast capacitor and restored power feed to 5 light poles.",
        "resolutionPhoto": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=600&auto=format&fit=crop&q=80",
        "resolvingDept": "Municipal Corporation – Electrical / Street Lighting Division"
    },
    {
        "id": "notif_002",
        "ticketId": "GOV-10481",
        "title": "SLA Exceeded – Escalated",
        "message": "Complaint GOV-10481 exceeded its 3-day SLA deadline. Automatically escalated to Higher Officer (Department Senior Officer).",
        "type": "warning",
        "timestamp": (datetime.now() - timedelta(hours=12)).strftime("%d %b %Y, %H:%M"),
        "isRead": False
    },
    {
        "id": "notif_003",
        "ticketId": "GOV-10482",
        "title": "Complaint Submitted Successfully",
        "message": "Your complaint regarding road potholes has been registered under ticket GOV-10482 and assigned to PWD – Roads Division.",
        "type": "info",
        "timestamp": (datetime.now() - timedelta(days=1)).strftime("%d %b %Y, %H:%M"),
        "isRead": True
    }
]

# Helper for initial dates
_now = datetime.now()

INITIAL_COMPLAINTS = [
    # 1. PWD Roads - In Progress (Active)
    {
        "complaintId": "GOV-10482",
        "id": "GOV-10482",
        "userId": "usr_citizen_9821a",
        "citizenName": "Demo Citizen",
        "citizenEmail": "citizen@example.com",
        "description": "Road near school has multiple deep potholes. Motorbikes are skidding frequently during peak hours and school drop-off.",
        "category": "Roads & Potholes",
        "department": "Public Works Department (PWD) – Roads Division",
        "location": "School Access Road, Ward 4, Anna Nagar",
        "latitude": 13.0852,
        "longitude": 80.2104,
        "priority": "HIGH",
        "dateAdded": (_now - timedelta(days=1)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now + timedelta(days=2)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now + timedelta(days=2)).strftime("%Y-%m-%d"),
        "status": "IN PROGRESS",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Severe Road Potholes",
                "category": "Roads & Potholes",
                "department": "Public Works Department (PWD) – Roads Division",
                "priority": "HIGH",
                "reason": "Immediate skidding hazard for two-wheelers near school zone."
            }
        ],
        "similarTickets": [],
        "createdAt": (_now - timedelta(days=1)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(hours=4)).strftime("%d %b %Y %H:%M")
    },
    # 2. PWD Roads - Overdue & Escalated! (HIGH priority created 5 days ago; SLA was 3 days)
    {
        "complaintId": "GOV-10481",
        "id": "GOV-10481",
        "userId": "usr_citizen_9821a",
        "citizenName": "Demo Citizen",
        "citizenEmail": "citizen@example.com",
        "description": "Severe asphalt crater on Anna Salai Main Junction corridor causing vehicular axle damage and severe morning traffic bottlenecks.",
        "category": "Roads & Potholes",
        "department": "Public Works Department (PWD) – Roads Division",
        "location": "Anna Salai Junction Corridor, Ward 4",
        "latitude": 13.0850,
        "longitude": 80.2100,
        "priority": "HIGH",
        "dateAdded": (_now - timedelta(days=5)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=5)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now - timedelta(days=2)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now - timedelta(days=2)).strftime("%Y-%m-%d"),
        "status": "ASSIGNED",
        "escalationStatus": "ESCALATED",
        "escalatedDate": (_now - timedelta(days=2)).strftime("%d %b %Y"),
        "escalationReason": "SLA Exceeded (3 days high priority limit). Escalated to Department Senior Officer.",
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1541888946425-d0fbb18086f6?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Major Road Crater",
                "category": "Roads & Potholes",
                "department": "Public Works Department (PWD) – Roads Division",
                "priority": "HIGH",
                "reason": "Severe arterial road surface failure."
            }
        ],
        "similarTickets": [],
        "createdAt": (_now - timedelta(days=5)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(days=2)).strftime("%d %b %Y %H:%M")
    },
    # 3. PWD Roads - Submitted (Pending, logged today)
    {
        "complaintId": "GOV-10485",
        "id": "GOV-10485",
        "userId": "usr_citizen_4412b",
        "citizenName": "Kavitha Raman",
        "citizenEmail": "kavitha.raman@gmail.com",
        "description": "Caved-in storm drain slab creating a gap on the sidewalk on 3rd Avenue, dangerous for pedestrians walking at dusk.",
        "category": "Roads & Potholes",
        "department": "Public Works Department (PWD) – Roads Division",
        "location": "3rd Avenue Sidewalk, Ward 4",
        "latitude": 13.0848,
        "longitude": 80.2095,
        "priority": "MEDIUM",
        "dateAdded": _now.strftime("%d %b %Y"),
        "dateAddedDt": _now.strftime("%Y-%m-%d"),
        "slaDeadline": (_now + timedelta(days=7)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now + timedelta(days=7)).strftime("%Y-%m-%d"),
        "status": "SUBMITTED",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Caved-in Pedestrian Slab",
                "category": "Roads & Potholes",
                "department": "Public Works Department (PWD) – Roads Division",
                "priority": "MEDIUM",
                "reason": "Pedestrian sidewalk hazard."
            }
        ],
        "similarTickets": [],
        "createdAt": _now.strftime("%d %b %Y %H:%M"),
        "updatedAt": _now.strftime("%d %b %Y %H:%M")
    },
    # 4. PWD Roads - Resolved
    {
        "complaintId": "GOV-10476",
        "id": "GOV-10476",
        "userId": "usr_citizen_7719c",
        "citizenName": "Suresh Babu",
        "citizenEmail": "suresh.babu@gmail.com",
        "description": "Loose gravel and damaged bitumen patch after utility trenching on 1st Cross.",
        "category": "Roads & Potholes",
        "department": "Public Works Department (PWD) – Roads Division",
        "location": "1st Cross Street, Ward 4",
        "latitude": 13.0840,
        "longitude": 80.2085,
        "priority": "MEDIUM",
        "dateAdded": (_now - timedelta(days=8)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=8)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now - timedelta(days=1)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "status": "RESOLVED",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": "Hot-mix asphalt patch compacted and leveled with road grade. Debris cleared.",
        "resolutionPhoto": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
        "resolvedDate": (_now - timedelta(days=2)).strftime("%d %b %Y"),
        "resolvedBy": "pwd.admin@gov.in",
        "evidenceUrl": "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Bitumen Road Restoration",
                "category": "Roads & Potholes",
                "department": "Public Works Department (PWD) – Roads Division",
                "priority": "MEDIUM",
                "reason": "Post-trenching road surfacing."
            }
        ],
        "similarTickets": [],
        "createdAt": (_now - timedelta(days=8)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(days=2)).strftime("%d %b %Y %H:%M")
    },
    # 5. TWAD Board (Water Supply) - High Priority Pipeline Burst
    {
        "complaintId": "GOV-10483",
        "id": "GOV-10483",
        "userId": "usr_citizen_9821a",
        "citizenName": "Demo Citizen",
        "citizenEmail": "citizen@example.com",
        "description": "Underground drinking water main pipe fractured. Clean potable water overflowing onto 4th Cross St with zero tap pressure in 50 residential homes.",
        "category": "Water Supply",
        "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
        "location": "4th Cross Street, Sector 2, Anna Nagar",
        "latitude": 13.0861,
        "longitude": 80.2110,
        "priority": "HIGH",
        "dateAdded": (_now - timedelta(days=2)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=2)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now + timedelta(days=1)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now + timedelta(days=1)).strftime("%Y-%m-%d"),
        "status": "IN PROGRESS",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1584467735815-f778f274e296?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Drinking Water Main Burst",
                "category": "Water Supply",
                "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
                "priority": "HIGH",
                "reason": "Continuous potable water loss and domestic outage."
            }
        ],
        "similarTickets": ["GOV-10474"],
        "createdAt": (_now - timedelta(days=2)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(hours=8)).strftime("%d %b %Y %H:%M")
    },
    # 6. TWAD Board - Nearby duplicate
    {
        "complaintId": "GOV-10474",
        "id": "GOV-10474",
        "userId": "usr_citizen_1109f",
        "citizenName": "Deepa Sundar",
        "citizenEmail": "deepa.sundar@gmail.com",
        "description": "Municipal pipeline leak near 4th Cross corner flooding the street.",
        "category": "Water Supply",
        "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
        "location": "4th Cross Street Corner, Sector 2",
        "latitude": 13.0863,
        "longitude": 80.2112,
        "priority": "HIGH",
        "dateAdded": (_now - timedelta(days=3)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=3)).strftime("%Y-%m-%d"),
        "slaDeadline": _now.strftime("%d %b %Y"),
        "slaDeadlineDt": _now.strftime("%Y-%m-%d"),
        "status": "ASSIGNED",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1584467735815-f778f274e296?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Pipeline Leakage",
                "category": "Water Supply",
                "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
                "priority": "HIGH",
                "reason": "Water pipeline leakage."
            }
        ],
        "similarTickets": ["GOV-10483"],
        "createdAt": (_now - timedelta(days=3)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(days=1)).strftime("%d %b %Y %H:%M")
    },
    # 7. TANGEDCO (Electricity)
    {
        "complaintId": "GOV-10478",
        "id": "GOV-10478",
        "userId": "usr_citizen_9011d",
        "citizenName": "Meera Natarajan",
        "citizenEmail": "meera.natarajan@gmail.com",
        "description": "Distribution transformer buzzing loudly with intermittent sparks on Pillar 4B, residential power fluctuating violently.",
        "category": "Electricity",
        "department": "Tamil Nadu Generation and Distribution Corporation (TANGEDCO)",
        "location": "Pillar 4B, Sector 1, Anna Nagar",
        "latitude": 13.0835,
        "longitude": 80.2092,
        "priority": "HIGH",
        "dateAdded": (_now - timedelta(days=1)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now + timedelta(days=2)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now + timedelta(days=2)).strftime("%Y-%m-%d"),
        "status": "IN PROGRESS",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Transformer Sparking & Voltage Surges",
                "category": "Electricity",
                "department": "Tamil Nadu Generation and Distribution Corporation (TANGEDCO)",
                "priority": "HIGH",
                "reason": "Fire hazard and electrical appliance damage risk."
            }
        ],
        "similarTickets": [],
        "createdAt": (_now - timedelta(days=1)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(hours=6)).strftime("%d %b %Y %H:%M")
    },
    # 8. Street Lighting (Municipal Electrical Division) - Resolved
    {
        "complaintId": "GOV-10480",
        "id": "GOV-10480",
        "userId": "usr_citizen_9821a",
        "citizenName": "Demo Citizen",
        "citizenEmail": "citizen@example.com",
        "description": "5 consecutive streetlights non-functional on 2nd Avenue. Area pitch dark after 7 PM.",
        "category": "Street Lighting",
        "department": "Municipal Corporation – Electrical / Street Lighting Division",
        "location": "2nd Avenue, Sector 1, Anna Nagar",
        "latitude": 13.0838,
        "longitude": 80.2090,
        "priority": "MEDIUM",
        "dateAdded": (_now - timedelta(days=4)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=4)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now + timedelta(days=3)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now + timedelta(days=3)).strftime("%Y-%m-%d"),
        "status": "RESOLVED",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": "Replaced blown ballast capacitor and restored power feed to 5 light poles.",
        "resolutionPhoto": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=600&auto=format&fit=crop&q=80",
        "resolvedDate": _now.strftime("%d %b %Y"),
        "resolvedBy": "streetlight.admin@gov.in",
        "evidenceUrl": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Street Lighting Inactive",
                "category": "Street Lighting",
                "department": "Municipal Corporation – Electrical / Street Lighting Division",
                "priority": "MEDIUM",
                "reason": "Street illumination failure."
            }
        ],
        "similarTickets": [],
        "createdAt": (_now - timedelta(days=4)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(hours=3)).strftime("%d %b %Y %H:%M")
    },
    # 9. Waste Management (Solid Waste)
    {
        "complaintId": "GOV-10479",
        "id": "GOV-10479",
        "userId": "usr_citizen_7719c",
        "citizenName": "Suresh Babu",
        "citizenEmail": "suresh.babu@gmail.com",
        "description": "Community garbage dumpster overflowing for 4 days near market square. Stray animals scattering plastic waste.",
        "category": "Waste Management",
        "department": "Municipal Corporation – Solid Waste Management Department",
        "location": "Block C Market Square, Anna Nagar",
        "latitude": 13.0875,
        "longitude": 80.2130,
        "priority": "MEDIUM",
        "dateAdded": (_now - timedelta(days=2)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=2)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now + timedelta(days=5)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now + timedelta(days=5)).strftime("%Y-%m-%d"),
        "status": "ASSIGNED",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1530587191325-3db32d826c18?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Solid Waste Accumulation",
                "category": "Waste Management",
                "department": "Municipal Corporation – Solid Waste Management Department",
                "priority": "MEDIUM",
                "reason": "Dumpster overflow posing environmental health concern."
            }
        ],
        "similarTickets": [],
        "createdAt": (_now - timedelta(days=2)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(days=1)).strftime("%d %b %Y %H:%M")
    },
    # 10. Drainage & Sewage
    {
        "complaintId": "GOV-10472",
        "id": "GOV-10472",
        "userId": "usr_citizen_3120e",
        "citizenName": "Karthik Subramanian",
        "citizenEmail": "karthik.s@gmail.com",
        "description": "Sewer chamber choked causing foul blackwater backflow onto residential street.",
        "category": "Drainage & Sewage",
        "department": "Municipal Corporation – Sewerage & Drainage Department",
        "location": "Cross Lane 4, Ward 4",
        "latitude": 13.0858,
        "longitude": 80.2140,
        "priority": "HIGH",
        "dateAdded": (_now - timedelta(days=1)).strftime("%d %b %Y"),
        "dateAddedDt": (_now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "slaDeadline": (_now + timedelta(days=2)).strftime("%d %b %Y"),
        "slaDeadlineDt": (_now + timedelta(days=2)).strftime("%Y-%m-%d"),
        "status": "SUBMITTED",
        "escalationStatus": "NORMAL",
        "escalatedDate": None,
        "escalationReason": None,
        "resolutionNote": None,
        "resolutionPhoto": None,
        "resolvedDate": None,
        "resolvedBy": None,
        "evidenceUrl": "https://images.unsplash.com/photo-1541888946425-d0fbb18086f6?w=600&auto=format&fit=crop&q=80",
        "issues": [
            {
                "issue": "Sewerage Line Clog & Backflow",
                "category": "Drainage & Sewage",
                "department": "Municipal Corporation – Sewerage & Drainage Department",
                "priority": "HIGH",
                "reason": "Public hygiene threat and sewer backflow."
            }
        ],
        "similarTickets": [],
        "createdAt": (_now - timedelta(days=1)).strftime("%d %b %Y %H:%M"),
        "updatedAt": (_now - timedelta(days=1)).strftime("%d %b %Y %H:%M")
    }
]

# Department Specific Hotspot Clusters (Section 17)
HOTSPOT_DATA = [
    {
        "id": "hotspot_pwd",
        "category": "Roads & Potholes",
        "department": "Public Works Department (PWD) – Roads Division",
        "locationName": "Anna Salai Junction Corridor (Ward 4)",
        "latitude": 13.0851,
        "longitude": 80.2103,
        "complaintCount": 24,
        "severity": "HIGH",
        "description": "Road surface degradation following monsoon rains, leading to traffic bottlenecks and two-wheeler skidding.",
        "trend": "+120% over previous 7-day period",
        "activeTickets": ["GOV-10482", "GOV-10481"]
    },
    {
        "id": "hotspot_twad",
        "category": "Water Supply",
        "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
        "locationName": "Sector 2, Anna Nagar (Ward 4)",
        "latitude": 13.0862,
        "longitude": 80.2111,
        "complaintCount": 37,
        "severity": "CRITICAL",
        "description": "Major underground distribution main fracture causing low pressure across 3 residential blocks.",
        "trend": "+460% over previous 7-day period",
        "activeTickets": ["GOV-10483", "GOV-10474"]
    },
    {
        "id": "hotspot_waste",
        "category": "Waste Management",
        "department": "Municipal Corporation – Solid Waste Management Department",
        "locationName": "Market Square & Commercial Belt",
        "latitude": 13.0876,
        "longitude": 80.2132,
        "complaintCount": 18,
        "severity": "MEDIUM",
        "description": "Commercial waste collection delays during peak vegetable market hours.",
        "trend": "+45% over previous 7-day period",
        "activeTickets": ["GOV-10479"]
    }
]

# Department-Specific Emerging Anomaly Signals (Section 17)
EMERGING_ISSUES = [
    {
        "category": "Roads & Potholes",
        "department": "Public Works Department (PWD) – Roads Division",
        "previousCount": 6,
        "currentCount": 24,
        "percentageIncrease": 300,
        "severity": "HIGH",
        "alertMessage": "Emerging issue detected: Roads & Potholes complaints increased by 300% on Anna Salai Corridor.",
        "recommendation": "Deploy rapid road patch vehicle to Anna Salai signal 3."
    },
    {
        "category": "Water Supply",
        "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
        "previousCount": 5,
        "currentCount": 28,
        "percentageIncrease": 460,
        "severity": "CRITICAL",
        "alertMessage": "Emerging issue detected: Water Supply complaints surged by 460% in Sector 2.",
        "recommendation": "Dispatch rapid engineering audit team to Sector 2 distribution feeder valves."
    }
]
