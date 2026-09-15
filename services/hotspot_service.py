from utils.dummy_data import HOTSPOT_DATA, EMERGING_ISSUES

class HotspotService:
    @staticmethod
    def get_hotspots(department=None):
        """
        Returns spatial clusters of high-volume complaints.
        Section 17: Admin sees only hotspot information relevant to their department.
        """
        if department and department != "All":
            return [h for h in HOTSPOT_DATA if h.get("department") == department]
        return HOTSPOT_DATA

    @staticmethod
    def get_emerging_issues(department=None):
        """
        Returns period-over-period complaint surges.
        Section 17: Admin sees only emerging issues relevant to their department.
        """
        if department and department != "All":
            return [e for e in EMERGING_ISSUES if e.get("department") == department]
        return EMERGING_ISSUES

    @staticmethod
    def analyze_clusters(complaints, department=None):
        """
        Groups complaints by latitude/longitude approximation (rounded to 3 decimal places ~100m)
        and category to highlight localized spikes.
        """
        if department and department != "All":
            complaints = [c for c in complaints if c.get("department") == department]

        clusters = {}
        for c in complaints:
            lat = round(float(c.get("latitude", 0)), 3)
            lon = round(float(c.get("longitude", 0)), 3)
            cat = c.get("category", "General")
            key = f"{cat}@{lat},{lon}"

            if key not in clusters:
                clusters[key] = {
                    "category": cat,
                    "department": c.get("department"),
                    "latitude": lat,
                    "longitude": lon,
                    "locationName": c.get("location"),
                    "count": 0,
                    "tickets": []
                }
            clusters[key]["count"] += 1
            clusters[key]["tickets"].append(c.get("complaintId", c.get("id")))

        result = list(clusters.values())
        result.sort(key=lambda x: x["count"], reverse=True)
        return result
