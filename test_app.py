import unittest
from app import app
from services.complaint_service import complaint_service

class CivicRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_01_landing_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"CivicRoute", res.data)

    def test_02_login_pages(self):
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Citizen Grievance Portal", res.data)

        res_admin = self.client.get('/admin/login')
        self.assertEqual(res_admin.status_code, 200)
        self.assertIn(b"Departmental Admin Access", res_admin.data)

    def test_03_profile_page(self):
        res = self.client.get('/profile')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Citizen Profile", res.data)

    def test_04_submit_page(self):
        res = self.client.get('/submit')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Register Public Grievance", res.data)

    def test_05_ai_analysis_api_multi_issue(self):
        payload = {
            "description": "Deep potholes on the main road and broken streetlights near the school.",
            "latitude": 13.0852,
            "longitude": 80.2104
        }
        res = self.client.post('/api/analyze-complaint', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['ai']['isAiRecommendation'])
        self.assertGreaterEqual(len(data['ai']['issues']), 2)
        categories = [i['category'] for i in data['ai']['issues']]
        self.assertIn("Roads & Potholes", categories)
        self.assertIn("Street Lighting", categories)

    def test_06_ticket_creation(self):
        payload = {
            "description": "Dangerous pothole at street corner",
            "location": "Ward 4 Corner",
            "latitude": 13.085,
            "longitude": 80.210,
            "category": "Roads & Potholes",
            "priority": "HIGH",
            "issues": [{"issue": "Pothole", "category": "Roads & Potholes", "department": "Public Works Department (PWD) – Roads Division", "priority": "HIGH", "reason": "Hazard"}]
        }
        res = self.client.post('/api/create-ticket', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['ticket']['complaintId'].startswith('GOV-'))

    def test_07_my_complaints(self):
        res = self.client.get('/my-complaints')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"My Registered Grievances", res.data)

    def test_08_admin_views_with_gov_in_auth(self):
        # Authenticate as PWD Admin
        with self.client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['admin_profile'] = {
                "name": "PWD Roads Division Officer",
                "email": "pwd.admin@gov.in",
                "department": "Public Works Department (PWD) – Roads Division",
                "shortDept": "PWD – Roads Division",
                "category": "Roads & Potholes"
            }

        res_dash = self.client.get('/admin')
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn(b"PWD", res_dash.data)

        res_table = self.client.get('/admin/complaints')
        self.assertEqual(res_table.status_code, 200)
        self.assertIn(b"Grievance Registry", res_table.data)

        res_hotspots = self.client.get('/admin/hotspots')
        self.assertEqual(res_hotspots.status_code, 200)

    def test_09_admin_resolution_with_note(self):
        with self.client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['admin_profile'] = {
                "name": "PWD Officer",
                "email": "pwd.admin@gov.in",
                "department": "Public Works Department (PWD) – Roads Division",
                "shortDept": "PWD – Roads Division"
            }

        res = self.client.post('/api/admin/complaints/GOV-10482/status', json={
            "status": "RESOLVED",
            "notes": "Asphalt leveling and compaction completed by PWD road gang."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['ticket']['status'], "RESOLVED")

if __name__ == '__main__':
    unittest.main()
