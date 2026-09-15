"""
Gemini AI Analysis Service Stub (GOV-21 Department Triage)
Extracts single or multiple issues, mapping strictly to the 12 official government departments.
"""

from config.settings import CATEGORY_DEPARTMENT_MAPPING

class GeminiService:
    @staticmethod
    def analyze_complaint(text):
        text_lower = text.lower()
        detected_issues = []

        keywords_map = {
            "Roads & Potholes": {
                "keywords": ["road", "pothole", "crater", "asphalt", "tar", "skid", "pavement", "footpath", "traffic divider", "bitumen"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Roads & Potholes"],
                "issue_name": "Road Surface Damage & Potholes",
                "default_priority": "HIGH" if any(k in text_lower for k in ["accident", "severe", "crater", "skid", "danger", "school", "hazard"]) else "MEDIUM",
                "reason": "The complaint reports road surface damage and potholes affecting vehicular movement and commuter safety."
            },
            "Street Lighting": {
                "keywords": ["light", "lamp", "dark", "street light", "streetlamp", "lighting", "illumination"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Street Lighting"],
                "issue_name": "Street Lighting Failure",
                "default_priority": "MEDIUM",
                "reason": "The complaint reports non-functioning street lighting creating dark or unsafe nocturnal pedestrian conditions."
            },
            "Water Supply": {
                "keywords": ["water", "pipe", "pipeline", "leak", "leakage", "drinking water", "tap", "pressure", "burst", "water supply"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Water Supply"],
                "issue_name": "Drinking Water Supply Interruption / Pipeline Leak",
                "default_priority": "HIGH" if any(k in text_lower for k in ["burst", "flooding", "days", "drinking", "no water", "outage"]) else "MEDIUM",
                "reason": "The complaint highlights potable water supply disruption or main distribution pipeline fracture."
            },
            "Electricity": {
                "keywords": ["electricity", "spark", "transformer", "wire", "cable", "power", "blackout", "voltage", "tangedco", "fluctuation"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Electricity"],
                "issue_name": "Electrical Grid & Transformer Hazard",
                "default_priority": "HIGH" if any(k in text_lower for k in ["spark", "fire", "shock", "exposed", "explosion"]) else "MEDIUM",
                "reason": "The complaint reports high-voltage distribution fluctuation, transformer sparks, or exposed live conductors."
            },
            "Waste Management": {
                "keywords": ["garbage", "trash", "waste", "dumpster", "bin", "stench", "odor", "smell", "dump", "solid waste"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Waste Management"],
                "issue_name": "Solid Waste Dumpster Overflow",
                "default_priority": "MEDIUM",
                "reason": "Accumulation of community solid waste creating public hygiene and vector hazards."
            },
            "Drainage & Sewage": {
                "keywords": ["drain", "drainage", "sewer", "sewage", "gutter", "manhole", "blackwater", "chamber", "choked"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Drainage & Sewage"],
                "issue_name": "Sewerage Line Clog & Drainage Stoppage",
                "default_priority": "HIGH" if any(k in text_lower for k in ["backflow", "overflow", "stagnant"]) else "MEDIUM",
                "reason": "Sanitary sewer backflow or underground storm-water drain choking."
            },
            "Public Transport": {
                "keywords": ["bus", "shelter", "stop", "mtc", "transport", "bus stand", "depot"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Public Transport"],
                "issue_name": "Public Bus Transit / Shelter Infrastructure Issue",
                "default_priority": "LOW",
                "reason": "Passenger amenity or transit shelter maintenance grievance."
            },
            "Public Safety": {
                "keywords": ["police", "safety", "crime", "harassment", "theft", "patrol", "nuisance", "brawl"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Public Safety"],
                "issue_name": "Public Safety & Law/Order Grievance",
                "default_priority": "HIGH",
                "reason": "Urgent civic safety or security concern requiring local police patrol."
            },
            "Noise Pollution": {
                "keywords": ["noise", "loudspeaker", "decibel", "sound", "horn", "pollution"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Noise Pollution"],
                "issue_name": "Industrial / Commercial Noise Pollution",
                "default_priority": "MEDIUM",
                "reason": "Exceedance of ambient noise thresholds affecting residential zoning."
            },
            "Parks & Public Spaces": {
                "keywords": ["park", "garden", "bench", "tree", "playground", "open space"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Parks & Public Spaces"],
                "issue_name": "Public Park & Recreational Space Maintenance",
                "default_priority": "LOW",
                "reason": "Civic park landscaping or amenity repair."
            },
            "Government Services": {
                "keywords": ["certificate", "revenue", "ration", "collectorate", "portal", "taluk", "officer"],
                "dept": CATEGORY_DEPARTMENT_MAPPING["Government Services"],
                "issue_name": "District Administration / Public Service Grievance",
                "default_priority": "MEDIUM",
                "reason": "Government documentation or administrative service delivery delay."
            }
        }

        for cat, meta in keywords_map.items():
            if any(kw in text_lower for kw in meta["keywords"]):
                detected_issues.append({
                    "issue": meta["issue_name"],
                    "category": cat,
                    "department": meta["dept"],
                    "priority": meta["default_priority"],
                    "reason": meta["reason"]
                })

        # Fallback
        if not detected_issues:
            detected_issues.append({
                "issue": "General Civic Grievance",
                "category": "Other",
                "department": CATEGORY_DEPARTMENT_MAPPING["Other"],
                "priority": "LOW",
                "reason": "General civic grievance requiring inspection and manual triage by municipal administrators."
            })

        primary_issue = detected_issues[0]
        has_high_priority = any(i["priority"] == "HIGH" for i in detected_issues)
        has_med_priority = any(i["priority"] == "MEDIUM" for i in detected_issues)
        overall_priority = "HIGH" if has_high_priority else ("MEDIUM" if has_med_priority else "LOW")

        return {
            "isAiRecommendation": True,
            "disclaimer": "AI predictions are recommendations to assist triage, not official government decisions.",
            "overallCategory": primary_issue["category"],
            "overallDepartment": primary_issue["department"],
            "overallPriority": overall_priority,
            "overallReason": primary_issue["reason"],
            "issues": detected_issues,
            "multipleIssuesDetected": len(detected_issues) > 1
        }
