import json
import os

class FlakyTracker:
    FILE = "reports/flaky_history.json"

    @staticmethod
    def load():
        if os.path.exists(FlakyTracker.FILE):
            with open(FlakyTracker.FILE, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save(data):
        os.makedirs("reports", exist_ok=True)
        with open(FlakyTracker.FILE, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def record(test_name, status):
        data = FlakyTracker.load()
        data.setdefault(test_name, []).append(status)
        FlakyTracker.save(data)

    @staticmethod
    def is_flaky(history):
        return "passed" in history and "failed" in history
