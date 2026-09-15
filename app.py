import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

from config.settings import (
    APP_NAME, APP_TAGLINE, PROJECT_CODE, VERSION, SECRET_KEY,
    CATEGORY_DEPARTMENT_MAPPING, ADMIN_DEPARTMENT_MAPPING,
    PRIORITY_LEVELS, PRIORITY_SLA_DAYS, TICKET_STATUSES,
    DAILY_PROCESSING_LIMIT, ESCALATION_SUPERVISOR_TITLE,
    DEFAULT_LATITUDE, DEFAULT_LONGITUDE
)
from services.complaint_service import complaint_service
from services.gemini_service import GeminiService
from services.duplicate_service import DuplicateService
from services.hotspot_service import HotspotService

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ================= AUTHENTICATION DECORATORS & HELPERS =================

def get_current_user():
    return session.get("user", complaint_service.get_user_profile())

def get_current_role():
    return session.get("role", "citizen")

def get_admin_profile():
    return session.get("admin_profile")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = get_current_role()
        admin = get_admin_profile()
        if role != "admin" or not admin or not admin.get("email", "").endswith("@gov.in"):
            flash("Unauthorized: Government Admin access requires an approved @gov.in administrative account.", "error")
            return redirect(url_for("admin_login_page"))
        return f(*args, **kwargs)
    return decorated_function

# Context processor for Jinja2 templates
@app.context_processor
def inject_global_vars():
    user = get_current_user()
    role = get_current_role()
    admin_prof = get_admin_profile()
    notifications = complaint_service.get_notifications(citizen_email=user.get("email"))
    unread_count = len([n for n in notifications if not n.get("isRead")])

    return {
        "app_name": APP_NAME,
        "app_tagline": APP_TAGLINE,
        "project_code": PROJECT_CODE,
        "app_version": VERSION,
        "current_user": user,
        "user_role": role,
        "admin_profile": admin_prof,
        "admin_dept_name": admin_prof.get("department") if admin_prof else None,
        "unread_notifications_count": unread_count,
        "categories": list(CATEGORY_DEPARTMENT_MAPPING.keys()),
        "category_dept_mapping": CATEGORY_DEPARTMENT_MAPPING,
        "admin_dept_mapping": ADMIN_DEPARTMENT_MAPPING,
        "priority_levels": PRIORITY_LEVELS,
        "priority_sla_days": PRIORITY_SLA_DAYS,
        "ticket_statuses": TICKET_STATUSES,
        "daily_processing_limit": DAILY_PROCESSING_LIMIT,
        "default_lat": DEFAULT_LATITUDE,
        "default_lon": DEFAULT_LONGITUDE
    }

# ================= PUBLIC & CITIZEN ROUTES =================

@app.route("/")
def index():
    kpis = complaint_service.get_system_kpis()
    hotspots = HotspotService.get_hotspots()
    emerging = HotspotService.get_emerging_issues()
    return render_template("index.html", kpis=kpis, hotspots=hotspots, emerging=emerging)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/admin/login")
def admin_login_page():
    return render_template("admin_login.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    role = data.get("role", "citizen")

    # Section 1: Role-based validation
    if role == "admin" or email.endswith("@gov.in"):
        # Validate format
        if not email.endswith("@gov.in"):
            return jsonify({
                "success": False,
                "error": "Access Denied: Official government administrative accounts must use the official @gov.in domain."
            }), 403

        # Check against approved demo admin accounts
        admin_meta = ADMIN_DEPARTMENT_MAPPING.get(email)
        if not admin_meta:
            return jsonify({
                "success": False,
                "error": f"Email '{email}' has valid @gov.in format, but is not in the approved departmental demo directory."
            }), 403

        session["role"] = "admin"
        session["admin_profile"] = {
            "name": admin_meta["name"],
            "email": email,
            "department": admin_meta["department"],
            "shortDept": admin_meta["shortDept"],
            "category": admin_meta["category"],
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
        }
        return jsonify({"success": True, "redirect": url_for("admin_dashboard")})

    else:
        # Citizen login
        citizen = complaint_service.get_user_profile()
        if email:
            citizen["email"] = email
        session["role"] = "citizen"
        session["user"] = citizen
        session.pop("admin_profile", None)
        return jsonify({"success": True, "redirect": url_for("my_complaints")})

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("index"))

@app.route("/switch-admin/<email>")
def switch_admin(email):
    """Convenient switch helper for demonstrating different department admins in hackathons"""
    admin_meta = ADMIN_DEPARTMENT_MAPPING.get(email)
    if admin_meta:
        session["role"] = "admin"
        session["admin_profile"] = {
            "name": admin_meta["name"],
            "email": email,
            "department": admin_meta["department"],
            "shortDept": admin_meta["shortDept"],
            "category": admin_meta["category"],
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
        }
        flash(f"Switched to {admin_meta['department']} ({email})", "success")
        return redirect(url_for("admin_dashboard"))
    flash("Unknown admin account", "error")
    return redirect(url_for("admin_login_page"))

@app.route("/switch-role/citizen")
def switch_to_citizen():
    session["role"] = "citizen"
    session.pop("admin_profile", None)
    flash("Switched to Citizen Interface.", "info")
    return redirect(url_for("my_complaints"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "preferredLanguage": request.form.get("preferredLanguage", "English"),
            "defaultLocation": request.form.get("defaultLocation", "").strip()
        }
        updated = complaint_service.update_user_profile(data)
        session["user"] = updated
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    user = complaint_service.get_user_profile()
    return render_template("profile.html", user=user)

@app.route("/submit")
def submit_complaint():
    user = complaint_service.get_user_profile()
    return render_template("submit_complaint.html", user=user)

@app.route("/api/analyze-complaint", methods=["POST"])
def analyze_complaint():
    data = request.get_json() or {}
    text = data.get("description", "").strip()
    lat = float(data.get("latitude", DEFAULT_LATITUDE))
    lon = float(data.get("longitude", DEFAULT_LONGITUDE))

    if not text:
        return jsonify({"error": "Please describe your complaint before proceeding."}), 400

    # 1. AI Analysis with 12 official government departments
    ai_result = GeminiService.analyze_complaint(text)

    # 2. Duplicate Detection
    all_complaints = complaint_service.get_all_complaints()
    duplicate_result = DuplicateService.find_similar_complaints(
        description=text,
        category=ai_result["overallCategory"],
        lat=lat,
        lon=lon,
        existing_complaints=all_complaints
    )

    return jsonify({
        "ai": ai_result,
        "duplicates": duplicate_result
    })

@app.route("/confirmation", methods=["GET", "POST"])
def confirmation():
    if request.method == "POST":
        data_json = request.form.get("analysis_payload")
        if not data_json:
            flash("No complaint data received. Please submit again.", "warning")
            return redirect(url_for("submit_complaint"))
        payload = json.loads(data_json)
        return render_template("confirmation.html", payload=payload)
    return redirect(url_for("submit_complaint"))

@app.route("/api/create-ticket", methods=["POST"])
def api_create_ticket():
    data = request.get_json() or {}
    created_ticket = complaint_service.create_ticket(data)
    return jsonify({
        "success": True,
        "ticket": created_ticket,
        "redirect": url_for("my_complaints")
    })

@app.route("/my-complaints")
def my_complaints():
    user = get_current_user()
    status_filter = request.args.get("status", "All")
    search_query = request.args.get("q", "")

    tickets = complaint_service.get_citizen_complaints(
        citizen_email=user.get("email"),
        search=search_query,
        status=status_filter
    )
    return render_template(
        "my_complaints.html",
        tickets=tickets,
        selected_status=status_filter,
        search_query=search_query
    )

@app.route("/complaint/<ticket_id>")
def complaint_detail(ticket_id):
    ticket = complaint_service.get_complaint_by_id(ticket_id)
    if not ticket:
        flash(f"Complaint {ticket_id} was not found.", "error")
        return redirect(url_for("my_complaints"))
    return render_template("complaint_detail.html", ticket=ticket)

@app.route("/notifications")
def notifications_view():
    all_notifs = complaint_service.get_notifications()
    return render_template("notifications.html", notifications=all_notifs)

@app.route("/api/notifications/<notif_id>/read", methods=["POST"])
def mark_notification(notif_id):
    success = complaint_service.mark_notification_read(notif_id)
    return jsonify({"success": success})

# ================= DEPARTMENT-SPECIFIC ADMIN ROUTES =================

@app.route("/admin")
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    admin = get_admin_profile()
    assigned_dept = admin["department"]

    # Section 4: Department-specific KPIs only
    kpis = complaint_service.get_department_kpis(assigned_dept)

    # Section 16: Department complaints sorted by Escalated > High > Medium > Low
    dept_complaints = complaint_service.get_department_complaints(assigned_dept)

    # Section 17: Hotspots & Emerging issues scoped only to this department
    dept_hotspots = HotspotService.get_hotspots(department=assigned_dept)
    dept_emerging = HotspotService.get_emerging_issues(department=assigned_dept)

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        kpis=kpis,
        complaints=dept_complaints,
        hotspots=dept_hotspots,
        emerging=dept_emerging
    )

@app.route("/admin/complaints")
@admin_required
def admin_complaints():
    admin = get_admin_profile()
    assigned_dept = admin["department"]

    search = request.args.get("q", "")
    priority = request.args.get("priority", "All")
    status = request.args.get("status", "All")
    sla_status = request.args.get("sla_status", "All")
    date = request.args.get("date", "")

    # Section 13: Strict backend filtering by admin's assigned department
    complaints = complaint_service.get_department_complaints(
        department=assigned_dept,
        search=search,
        priority=priority,
        status=status,
        sla_status=sla_status,
        date=date
    )

    daily_stats = complaint_service.get_daily_limit_stats(assigned_dept)

    return render_template(
        "admin_complaints.html",
        admin=admin,
        complaints=complaints,
        daily_stats=daily_stats,
        search=search,
        sel_pri=priority,
        sel_status=status,
        sel_sla=sla_status,
        sel_date=date
    )

@app.route("/api/admin/complaints/<ticket_id>/status", methods=["POST"])
@admin_required
def api_update_status(ticket_id):
    admin = get_admin_profile()
    assigned_dept = admin["department"]
    admin_email = admin["email"]

    # Check if ticket belongs to admin's department
    ticket = complaint_service.get_complaint_by_id(ticket_id)
    if not ticket:
        return jsonify({"success": False, "error": "Ticket not found."}), 404

    if ticket.get("department") != assigned_dept:
        return jsonify({
            "success": False,
            "error": "Unauthorized: You can only take administrative action on complaints assigned to your department."
        }), 403

    data = request.get_json() or {}
    new_status = data.get("status")
    notes = data.get("notes", "").strip()
    photo = data.get("resolutionPhoto", "").strip()

    if not new_status or new_status not in TICKET_STATUSES:
        return jsonify({"success": False, "error": "Invalid status value provided."}), 400

    result = complaint_service.update_complaint_status(
        ticket_id=ticket_id,
        new_status=new_status,
        admin_email=admin_email,
        admin_notes=notes,
        resolution_photo=photo
    )

    if not result.get("success"):
        return jsonify(result), 400

    return jsonify(result)

@app.route("/admin/hotspots")
@admin_required
def admin_hotspots():
    admin = get_admin_profile()
    assigned_dept = admin["department"]

    # Section 17: Admin sees only their department's hotspots
    hotspots = HotspotService.get_hotspots(department=assigned_dept)
    emerging = HotspotService.get_emerging_issues(department=assigned_dept)
    dept_complaints = complaint_service.get_department_complaints(department=assigned_dept)
    clusters = HotspotService.analyze_clusters(dept_complaints, department=assigned_dept)

    return render_template(
        "admin_hotspots.html",
        admin=admin,
        hotspots=hotspots,
        emerging=emerging,
        clusters=clusters
    )

# ================= API HEALTH CHECK =================

@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "project": PROJECT_CODE,
        "complaints_count": len(complaint_service.complaints)
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
