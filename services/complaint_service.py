from datetime import datetime, timedelta
from config.settings import (
    CATEGORY_DEPARTMENT_MAPPING, PRIORITY_SLA_DAYS,
    DAILY_PROCESSING_LIMIT, ESCALATION_SUPERVISOR_TITLE
)
from utils.dummy_data import INITIAL_COMPLAINTS, INITIAL_NOTIFICATIONS, CURRENT_MOCK_USER

class ComplaintService:
    def __init__(self):
        # In-memory storage for prototype
        self.complaints = [dict(c) for c in INITIAL_COMPLAINTS]
        self.notifications = [dict(n) for n in INITIAL_NOTIFICATIONS]
        self.user_profile = dict(CURRENT_MOCK_USER)
        self.ticket_counter = 10486
        self.daily_limit = DAILY_PROCESSING_LIMIT
        # Tracks { (department, YYYY-MM-DD): [complaint_ids] }
        self.department_daily_actions = {}

    def _today_str(self):
        return datetime.now().strftime("%Y-%m-%d")

    def _today_display(self):
        return datetime.now().strftime("%d %b %Y")

    def _enrich_sla_and_escalation(self, comp):
        """
        Calculates SLA deadline adherence and automatic escalation (Section 7 & 8).
        HIGH -> 3 days, MEDIUM -> 7 days, LOW -> 15 days.
        If deadline passed and status is not RESOLVED, automatically marks OVERDUE & ESCALATED.
        """
        c = dict(comp)
        status = c.get("status", "SUBMITTED")
        priority = c.get("priority", "MEDIUM")
        sla_days = PRIORITY_SLA_DAYS.get(priority, 7)

        # Parse date added
        date_added_str = c.get("dateAddedDt")
        if not date_added_str:
            try:
                date_added_dt = datetime.strptime(c.get("dateAdded", self._today_display()), "%d %b %Y")
                date_added_str = date_added_dt.strftime("%Y-%m-%d")
                c["dateAddedDt"] = date_added_str
            except Exception:
                date_added_str = self._today_str()
                c["dateAddedDt"] = date_added_str

        # Calculate SLA deadline if missing
        if not c.get("slaDeadlineDt"):
            date_added_dt = datetime.strptime(date_added_str, "%Y-%m-%d")
            deadline_dt = date_added_dt + timedelta(days=sla_days)
            c["slaDeadlineDt"] = deadline_dt.strftime("%Y-%m-%d")
            c["slaDeadline"] = deadline_dt.strftime("%d %b %Y")

        # Compare with today
        today_dt = datetime.strptime(self._today_str(), "%Y-%m-%d")
        deadline_dt = datetime.strptime(c["slaDeadlineDt"], "%Y-%m-%d")
        days_diff = (deadline_dt - today_dt).days

        if status == "RESOLVED":
            c["slaStatus"] = "RESOLVED"
            c["slaRemainingDays"] = 0
            c["isOverdue"] = False
        elif days_diff < 0:
            # Overdue & Automatic Escalation
            c["slaStatus"] = "OVERDUE"
            c["isOverdue"] = True
            c["slaRemainingDays"] = days_diff  # Negative number indicates days overdue
            c["escalationStatus"] = "ESCALATED"
            if not c.get("escalatedDate"):
                c["escalatedDate"] = c.get("slaDeadline")
            c["escalatedTo"] = ESCALATION_SUPERVISOR_TITLE
            c["escalationNotice"] = f"⚠ SLA EXCEEDED ({abs(days_diff)} days overdue). Automatically escalated to {ESCALATION_SUPERVISOR_TITLE}."
        else:
            c["slaStatus"] = "ON TRACK" if days_diff > 1 else "DUE SOON"
            c["isOverdue"] = False
            c["slaRemainingDays"] = days_diff
            if not c.get("escalationStatus"):
                c["escalationStatus"] = "NORMAL"

        return c

    def get_processed_count_today(self, department):
        """
        Returns number of complaints processed by this department today.
        """
        key = (department, self._today_str())
        return len(self.department_daily_actions.get(key, []))

    def get_daily_limit_stats(self, department):
        """
        Returns today's limit, processed today, and remaining today (Section 5).
        """
        processed = self.get_processed_count_today(department)
        remaining = max(0, self.daily_limit - processed)
        limit_reached = processed >= self.daily_limit

        return {
            "dailyLimit": self.daily_limit,
            "processedToday": processed,
            "remainingToday": remaining,
            "limitReached": limit_reached
        }

    def _sort_key(self, c):
        """
        Sort order required by Section 16:
        1. Escalated / overdue
        2. High priority
        3. Medium priority
        4. Low priority
        """
        # Primary tier: Escalated/Overdue comes first
        is_escalated = 0 if c.get("escalationStatus") == "ESCALATED" or c.get("isOverdue") else 1
        
        # Priority tier: HIGH (0), MEDIUM (1), LOW (2)
        pri_map = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        pri_rank = pri_map.get(c.get("priority", "LOW"), 3)

        # Date tier (newer first)
        date_rank = c.get("dateAddedDt", "")

        return (is_escalated, pri_rank, -int(date_rank.replace("-", "") if date_rank else 0))

    def get_department_complaints(self, department, search=None, priority=None, status=None, sla_status=None, date=None):
        """
        Strict Department Filtering (Section 2 & 13):
        Only returns complaints belonging to the specified department.
        Sorted by Escalated > High > Medium > Low (Section 16).
        """
        # 1. Filter strictly by department in backend
        dept_complaints = [
            self._enrich_sla_and_escalation(c)
            for c in self.complaints
            if c.get("department") == department
        ]

        # 2. Search filter
        if search:
            q = search.lower()
            dept_complaints = [
                c for c in dept_complaints
                if q in c.get("complaintId", "").lower()
                or q in c.get("citizenName", "").lower()
                or q in c.get("citizenEmail", "").lower()
                or q in c.get("description", "").lower()
                or q in c.get("location", "").lower()
                or q in c.get("category", "").lower()
            ]

        # 3. Priority filter
        if priority and priority != "All":
            dept_complaints = [c for c in dept_complaints if c.get("priority") == priority]

        # 4. Status filter
        if status and status != "All":
            dept_complaints = [c for c in dept_complaints if c.get("status") == status]

        # 5. SLA Status filter
        if sla_status and sla_status != "All":
            if sla_status == "OVERDUE":
                dept_complaints = [c for c in dept_complaints if c.get("isOverdue")]
            elif sla_status == "ESCALATED":
                dept_complaints = [c for c in dept_complaints if c.get("escalationStatus") == "ESCALATED"]
            elif sla_status == "ON_TRACK":
                dept_complaints = [c for c in dept_complaints if not c.get("isOverdue") and c.get("status") != "RESOLVED"]

        # 6. Date filter
        if date:
            dept_complaints = [c for c in dept_complaints if c.get("dateAddedDt") == date or c.get("dateAdded") == date]

        # 7. Sort according to Section 16
        dept_complaints.sort(key=self._sort_key)
        return dept_complaints

    def get_citizen_complaints(self, citizen_email=None, search=None, status=None):
        """
        Citizen View (Section 12):
        Citizens see only their own complaints.
        """
        results = [self._enrich_sla_and_escalation(c) for c in self.complaints]

        if citizen_email:
            results = [c for c in results if c.get("citizenEmail") == citizen_email or c.get("userId") == citizen_email]

        if search:
            q = search.lower()
            results = [
                c for c in results
                if q in c.get("complaintId", "").lower()
                or q in c.get("description", "").lower()
                or q in c.get("category", "").lower()
                or q in c.get("department", "").lower()
            ]

        if status and status != "All":
            results = [c for c in results if c.get("status") == status]

        # Sort newest first
        results.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
        return results

    def get_all_complaints(self, search=None, category=None, department=None, priority=None, status=None, user_id=None):
        """General complaint retriever enriched with SLA"""
        results = [self._enrich_sla_and_escalation(c) for c in self.complaints]

        if user_id:
            results = [c for c in results if c.get("userId") == user_id or c.get("citizenEmail") == user_id]
        if department and department != "All":
            results = [c for c in results if c.get("department") == department]
        if category and category != "All":
            results = [c for c in results if c.get("category") == category]
        if priority and priority != "All":
            results = [c for c in results if c.get("priority") == priority]
        if status and status != "All":
            results = [c for c in results if c.get("status") == status]
        if search:
            q = search.lower()
            results = [
                c for c in results
                if q in c.get("complaintId", "").lower()
                or q in c.get("description", "").lower()
                or q in c.get("category", "").lower()
                or q in c.get("department", "").lower()
            ]

        results.sort(key=self._sort_key)
        return results

    def get_complaint_by_id(self, ticket_id):
        for c in self.complaints:
            if c.get("complaintId") == ticket_id or c.get("id") == ticket_id:
                return self._enrich_sla_and_escalation(c)
        return None

    def create_ticket(self, data):
        """
        Creates new ticket with GOV-XXXXX format and calculates SLA deadline (Section 6, 7 & 19).
        """
        complaint_id = f"GOV-{self.ticket_counter}"
        self.ticket_counter += 1

        priority = data.get("priority", "MEDIUM")
        sla_days = PRIORITY_SLA_DAYS.get(priority, 7)

        now_dt = datetime.now()
        date_added = now_dt.strftime("%d %b %Y")
        date_added_dt = now_dt.strftime("%Y-%m-%d")
        deadline_dt = now_dt + timedelta(days=sla_days)
        sla_deadline = deadline_dt.strftime("%d %b %Y")
        sla_deadline_dt = deadline_dt.strftime("%Y-%m-%d")

        category = data.get("category", "Roads & Potholes")
        department = CATEGORY_DEPARTMENT_MAPPING.get(category, data.get("department", "Municipal Corporation – Public Grievance Cell"))

        new_ticket = {
            "complaintId": complaint_id,
            "id": complaint_id,
            "userId": data.get("userId", self.user_profile["uid"]),
            "citizenName": data.get("citizenName", self.user_profile["name"]),
            "citizenEmail": data.get("citizenEmail", self.user_profile["email"]),
            "description": data.get("description", "").strip(),
            "category": category,
            "department": department,
            "location": data.get("location", "Ward 4, Anna Nagar").strip(),
            "latitude": float(data.get("latitude", 13.0850)),
            "longitude": float(data.get("longitude", 80.2101)),
            "priority": priority,
            "dateAdded": date_added,
            "dateAddedDt": date_added_dt,
            "slaDeadline": sla_deadline,
            "slaDeadlineDt": sla_deadline_dt,
            "status": "SUBMITTED",
            "escalationStatus": "NORMAL",
            "escalatedDate": None,
            "escalationReason": None,
            "resolutionNote": None,
            "resolutionPhoto": None,
            "resolvedDate": None,
            "resolvedBy": None,
            "evidenceUrl": data.get("evidenceUrl"),
            "issues": data.get("issues", []),
            "similarTickets": data.get("similarTickets", []),
            "createdAt": now_dt.strftime("%d %b %Y %H:%M"),
            "updatedAt": now_dt.strftime("%d %b %Y %H:%M")
        }

        self.complaints.insert(0, new_ticket)

        # In-app notification for Citizen
        notif = {
            "id": f"notif_{len(self.notifications) + 1:03d}",
            "ticketId": complaint_id,
            "title": "Complaint Submitted Successfully",
            "message": f"Your complaint regarding {category} has been registered under ticket {complaint_id} and assigned to {department}. SLA Deadline: {sla_deadline}.",
            "type": "info",
            "timestamp": now_dt.strftime("%d %b %Y, %H:%M"),
            "isRead": False
        }
        self.notifications.insert(0, notif)

        return self._enrich_sla_and_escalation(new_ticket)

    def update_complaint_status(self, ticket_id, new_status, admin_email, admin_notes=None, resolution_photo=None):
        """
        Admin actions (Section 9, 10 & 11):
        - Enforces daily processing limit of 5.
        - Requires Resolution Note if marking RESOLVED.
        - Allows Resolution Photo.
        - Sends citizen in-app notification upon resolution.
        """
        comp = None
        for c in self.complaints:
            if c.get("complaintId") == ticket_id or c.get("id") == ticket_id:
                comp = c
                break

        if not comp:
            return {"success": False, "error": "Ticket not found"}

        dept = comp.get("department")

        # Check daily processing limit
        key = (dept, self._today_str())
        today_actions = self.department_daily_actions.setdefault(key, [])
        if len(today_actions) >= self.daily_limit and ticket_id not in today_actions:
            return {
                "success": False,
                "error": "Daily processing limit reached. Remaining complaints remain pending for tomorrow.",
                "limitReached": True
            }

        # Validate resolution note requirement (Section 10)
        if new_status == "RESOLVED":
            if not admin_notes or not admin_notes.strip():
                return {"success": False, "error": "A Resolution Note is mandatory before marking a complaint as RESOLVED."}
            
            comp["resolutionNote"] = admin_notes.strip()
            comp["resolutionPhoto"] = resolution_photo or comp.get("evidenceUrl")
            comp["resolvedDate"] = self._today_display()
            comp["resolvedBy"] = admin_email

        comp["status"] = new_status
        now_dt = datetime.now()
        comp["updatedAt"] = now_dt.strftime("%d %b %Y %H:%M")

        # Record daily action
        if ticket_id not in today_actions:
            today_actions.append(ticket_id)

        # Notify Citizen if RESOLVED (Section 11)
        if new_status == "RESOLVED":
            notif = {
                "id": f"notif_{len(self.notifications) + 1:03d}",
                "ticketId": comp["complaintId"],
                "title": "Complaint Resolved",
                "message": f"Your complaint {comp['complaintId']} has been marked as resolved by {dept}. Resolution: {comp['resolutionNote']}",
                "type": "success",
                "timestamp": now_dt.strftime("%d %b %Y, %H:%M"),
                "isRead": False,
                "resolutionNote": comp["resolutionNote"],
                "resolutionPhoto": comp.get("resolutionPhoto"),
                "resolvingDept": dept,
                "resolvedDate": comp["resolvedDate"]
            }
            self.notifications.insert(0, notif)
        else:
            notif = {
                "id": f"notif_{len(self.notifications) + 1:03d}",
                "ticketId": comp["complaintId"],
                "title": f"Complaint Status: {new_status}",
                "message": f"Ticket {comp['complaintId']} has moved to {new_status} by {dept}.",
                "type": "info",
                "timestamp": now_dt.strftime("%d %b %Y, %H:%M"),
                "isRead": False
            }
            self.notifications.insert(0, notif)

        enriched = self._enrich_sla_and_escalation(comp)
        stats = self.get_daily_limit_stats(dept)

        return {
            "success": True,
            "ticket": enriched,
            "dailyStats": stats
        }

    def get_department_kpis(self, department):
        """
        Department-specific stats for Admin Dashboard (Section 4).
        Total, Pending, In Progress, Resolved, Escalated, Today's Complaints.
        """
        dept_tickets = [
            self._enrich_sla_and_escalation(c)
            for c in self.complaints
            if c.get("department") == department
        ]

        today_str = self._today_display()
        today_dt_str = self._today_str()

        total = len(dept_tickets)
        pending = len([c for c in dept_tickets if c.get("status") == "SUBMITTED"])
        in_progress = len([c for c in dept_tickets if c.get("status") in ["ASSIGNED", "IN PROGRESS"]])
        resolved = len([c for c in dept_tickets if c.get("status") == "RESOLVED"])
        escalated = len([c for c in dept_tickets if c.get("escalationStatus") == "ESCALATED" or c.get("isOverdue")])
        today_complaints = len([c for c in dept_tickets if c.get("dateAdded") == today_str or c.get("dateAddedDt") == today_dt_str])

        daily_stats = self.get_daily_limit_stats(department)

        return {
            "department": department,
            "total": total,
            "pending": pending,
            "inProgress": in_progress,
            "resolved": resolved,
            "escalated": escalated,
            "todayComplaints": today_complaints,
            "dailyStats": daily_stats
        }

    def get_system_kpis(self):
        """Global prototype KPIs for landing page"""
        all_enriched = [self._enrich_sla_and_escalation(c) for c in self.complaints]
        total = len(all_enriched)
        high = len([c for c in all_enriched if c.get("priority") == "HIGH"])
        pending = len([c for c in all_enriched if c.get("status") in ["SUBMITTED", "ASSIGNED", "IN PROGRESS"]])
        resolved = len([c for c in all_enriched if c.get("status") == "RESOLVED"])
        escalated = len([c for c in all_enriched if c.get("escalationStatus") == "ESCALATED" or c.get("isOverdue")])
        return {
            "total": total,
            "highPriority": high,
            "pending": pending,
            "resolved": resolved,
            "escalated": escalated
        }

    def get_user_profile(self):
        return self.user_profile

    def update_user_profile(self, data):
        for k in ["name", "email", "phone", "preferredLanguage", "defaultLocation", "latitude", "longitude"]:
            if k in data:
                self.user_profile[k] = data[k]
        return self.user_profile

    def get_notifications(self, citizen_email=None):
        return self.notifications

    def mark_notification_read(self, notif_id):
        for n in self.notifications:
            if n.get("id") == notif_id:
                n["isRead"] = True
                return True
        return False

# Global singleton service
complaint_service = ComplaintService()
