import json
import os

class AnalyticsEngine:
    FILE = "reports/analytics.json"

    @staticmethod
    def load():
        if os.path.exists(AnalyticsEngine.FILE):
            with open(AnalyticsEngine.FILE, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save(data):
        os.makedirs("reports", exist_ok=True)
        with open(AnalyticsEngine.FILE, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def record(test_name, metric, value):
        data = AnalyticsEngine.load()
        data.setdefault(test_name, {})
        data[test_name][metric] = value
        AnalyticsEngine.save(data)
