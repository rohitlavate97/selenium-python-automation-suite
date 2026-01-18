class StabilityAnalyzer:

    @staticmethod
    def stability_score(history):
        total = len(history)
        passed = history.count("passed")
        return round((passed / total) * 100, 2) if total else 100
