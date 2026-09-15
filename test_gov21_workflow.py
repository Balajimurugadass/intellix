import unittest
from datetime import datetime, timedelta
from app import app
from services.complaint_service import complaint_service
from services.hotspot_service import HotspotService
from config.settings import ADMIN_DEPARTMENT_MAPPING, CATEGORY_DEPARTMENT_MAPPING, PRIORITY_SLA_DAYS

class Gov21WorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_01_citizen_login(self):
        """Step 2: Citizen login with normal email"""
        res = self.client.post('/api/login', json={
            "email": "citizen@example.com",
            "role": "citizen"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['redirect'], '/my-complaints')

    def test_02_admin_login_validation(self):
        """Step 1 & 2: Admin accounts must end in @gov.in and be in approved directory"""
        # Non-gov.in email should be rejected
        res_fail = self.client.post('/api/login', json={
            "email": "hacker@gmail.com",
            "role": "admin"
        })
        self.assertEqual(res_fail.status_code, 403)
        self.assertIn("Access Denied", res_fail.get_json()['error'])

        # Unknown @gov.in email should be rejected
        res_unknown = self.client.post('/api/login', json={
            "email": "unknown.officer@gov.in",
            "role": "admin"
        })
        self.assertEqual(res_unknown.status_code, 403)

        # Approved PWD admin email succeeds
        res_ok = self.client.post('/api/login', json={
            "email": "pwd.admin@gov.in",
            "role": "admin"
        })
        self.assertEqual(res_ok.status_code, 200)
        self.assertTrue(res_ok.get_json()['success'])
        self.assertEqual(res_ok.get_json()['redirect'], '/admin/dashboard')

    def test_03_department_isolation(self):
        """Step 3 & 4: PWD Admin sees ONLY Roads complaints; TWAD Admin sees ONLY Water complaints"""
        # Login as PWD Admin
        with self.client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['admin_profile'] = {
                "name": "PWD Officer",
                "email": "pwd.admin@gov.in",
                "department": "Public Works Department (PWD) – Roads Division",
                "shortDept": "PWD – Roads Division",
                "category": "Roads & Potholes"
            }

        res_pwd = self.client.get('/admin/complaints')
        self.assertEqual(res_pwd.status_code, 200)
        # Should contain PWD tickets, but NOT Water tickets
        self.assertIn(b"GOV-10482", res_pwd.data)
        self.assertNotIn(b"GOV-10483", res_pwd.data)  # Water supply ticket

        # Switch to TWAD Water Admin
        with self.client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['admin_profile'] = {
                "name": "TWAD Officer",
                "email": "water.admin@gov.in",
                "department": "Tamil Nadu Water Supply and Drainage Board (TWAD Board)",
                "shortDept": "TWAD Board",
                "category": "Water Supply"
            }

        res_water = self.client.get('/admin/complaints')
        self.assertEqual(res_water.status_code, 200)
        self.assertIn(b"GOV-10483", res_water.data)  # Water ticket
        self.assertNotIn(b"GOV-10482", res_water.data)  # PWD ticket

    def test_04_sla_calculation(self):
        """Step 7: SLA calculation: High=3 days, Medium=7 days, Low=15 days"""
        # Create High priority ticket
        ticket_high = complaint_service.create_ticket({
            "description": "Critical road pothole",
            "priority": "HIGH",
            "category": "Roads & Potholes"
        })
        added_dt = datetime.strptime(ticket_high['dateAddedDt'], "%Y-%m-%d")
        deadline_dt = datetime.strptime(ticket_high['slaDeadlineDt'], "%Y-%m-%d")
        self.assertEqual((deadline_dt - added_dt).days, 3)

        # Create Medium priority ticket
        ticket_med = complaint_service.create_ticket({
            "description": "Medium road patch",
            "priority": "MEDIUM",
            "category": "Roads & Potholes"
        })
        added_med = datetime.strptime(ticket_med['dateAddedDt'], "%Y-%m-%d")
        deadline_med = datetime.strptime(ticket_med['slaDeadlineDt'], "%Y-%m-%d")
        self.assertEqual((deadline_med - added_med).days, 7)

        # Create Low priority ticket
        ticket_low = complaint_service.create_ticket({
            "description": "Low priority sidewalk",
            "priority": "LOW",
            "category": "Roads & Potholes"
        })
        added_low = datetime.strptime(ticket_low['dateAddedDt'], "%Y-%m-%d")
        deadline_low = datetime.strptime(ticket_low['slaDeadlineDt'], "%Y-%m-%d")
        self.assertEqual((deadline_low - added_low).days, 15)

    def test_05_overdue_and_automatic_escalation(self):
        """Step 8: Overdue complaints automatically marked as OVERDUE and ESCALATED"""
        # GOV-10481 was added 5 days ago with HIGH priority (3-day SLA)
        ticket = complaint_service.get_complaint_by_id("GOV-10481")
        self.assertIsNotNone(ticket)
        self.assertTrue(ticket['isOverdue'])
        self.assertEqual(ticket['slaStatus'], "OVERDUE")
        self.assertEqual(ticket['escalationStatus'], "ESCALATED")
        self.assertIn("SLA EXCEEDED", ticket['escalationNotice'])

    def test_06_resolution_requires_note(self):
        """Step 9 & 10: Marking RESOLVED requires a Resolution Note and sends notification"""
        with self.client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['admin_profile'] = {
                "name": "PWD Officer",
                "email": "pwd.admin@gov.in",
                "department": "Public Works Department (PWD) – Roads Division",
                "shortDept": "PWD – Roads Division"
            }

        # Attempt to resolve WITHOUT note -> should fail
        res_fail = self.client.post('/api/admin/complaints/GOV-10482/status', json={
            "status": "RESOLVED",
            "notes": ""
        })
        self.assertEqual(res_fail.status_code, 400)
        self.assertIn("Resolution Note is mandatory", res_fail.get_json()['error'])

        # Resolve WITH note and photo -> should succeed
        res_ok = self.client.post('/api/admin/complaints/GOV-10482/status', json={
            "status": "RESOLVED",
            "notes": "Asphalt patch completed and roller leveled with road grade.",
            "resolutionPhoto": "https://example.com/photo.jpg"
        })
        self.assertEqual(res_ok.status_code, 200)
        data = res_ok.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['ticket']['status'], "RESOLVED")
        self.assertEqual(data['ticket']['resolutionNote'], "Asphalt patch completed and roller leveled with road grade.")

        # Step 10: Verify citizen received resolution notification
        notifs = complaint_service.get_notifications()
        res_notif = next((n for n in notifs if n.get('ticketId') == 'GOV-10482' and n.get('title') == 'Complaint Resolved'), None)
        self.assertIsNotNone(res_notif)
        self.assertIn("Asphalt patch completed", res_notif['resolutionNote'])

    def test_07_daily_limit_enforcement(self):
        """Step 6: Daily processing limit of 5 complaints"""
        dept = "Tamil Nadu Generation and Distribution Corporation (TANGEDCO)"
        # Reset tracker for test
        complaint_service.department_daily_actions[(dept, complaint_service._today_str())] = ["T1", "T2", "T3", "T4", "T5"]

        stats = complaint_service.get_daily_limit_stats(dept)
        self.assertEqual(stats['processedToday'], 5)
        self.assertEqual(stats['remainingToday'], 0)
        self.assertTrue(stats['limitReached'])

        # Attempting 6th action for TANGEDCO should be blocked by limit
        result = complaint_service.update_complaint_status(
            ticket_id="GOV-10478",
            new_status="RESOLVED",
            admin_email="electricity.admin@gov.in",
            admin_notes="Replaced transformer fuse"
        )
        self.assertFalse(result['success'])
        self.assertTrue(result['limitReached'])
        self.assertIn("Daily processing limit reached", result['error'])

    def test_08_department_scoped_hotspots(self):
        """Step 17: Hotspots are filtered by department"""
        pwd_hotspots = HotspotService.get_hotspots(department="Public Works Department (PWD) – Roads Division")
        self.assertTrue(all(h['department'] == "Public Works Department (PWD) – Roads Division" for h in pwd_hotspots))

        water_hotspots = HotspotService.get_hotspots(department="Tamil Nadu Water Supply and Drainage Board (TWAD Board)")
        self.assertTrue(all(h['department'] == "Tamil Nadu Water Supply and Drainage Board (TWAD Board)" for h in water_hotspots))

if __name__ == '__main__':
    unittest.main()
