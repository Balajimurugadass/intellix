import math
from config.settings import PROXIMITY_THRESHOLD_KM

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates great-circle distance between two points in kilometers.
    """
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class DuplicateService:
    @staticmethod
    def find_similar_complaints(description, category, lat, lon, existing_complaints):
        """
        Scans existing active complaints within proximity threshold and category/keyword overlap.
        """
        similar = []
        desc_words = set(description.lower().split())

        for comp in existing_complaints:
            # Check geographical proximity
            comp_lat = float(comp.get("latitude", 0))
            comp_lon = float(comp.get("longitude", 0))
            dist_km = calculate_haversine_distance(lat, lon, comp_lat, comp_lon)

            # Keyword overlap
            existing_desc = comp.get("description", "").lower()
            existing_words = set(existing_desc.split())
            common_words = desc_words.intersection(existing_words)
            # Exclude short stopwords
            meaningful_common = [w for w in common_words if len(w) > 3]

            is_same_category = comp.get("category") == category
            is_close = dist_km <= PROXIMITY_THRESHOLD_KM

            # Match criteria: either same category and close, or strong keyword overlap and close
            if (is_same_category and is_close) or (len(meaningful_common) >= 3 and is_close):
                similar.append({
                    "ticketId": comp["id"],
                    "description": comp["description"],
                    "category": comp.get("category"),
                    "department": comp.get("department"),
                    "location": comp.get("location"),
                    "status": comp.get("status"),
                    "distanceMeters": round(dist_km * 1000),
                    "createdAt": comp.get("createdAt")
                })

        return {
            "found": len(similar) > 0,
            "count": len(similar),
            "approximateArea": similar[0]["location"] if similar else "Current vicinity",
            "commonCategory": category,
            "similarTickets": similar
        }
