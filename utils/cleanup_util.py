import shutil
import os

class CleanupUtil:

    @staticmethod
    def clean_dir(path):
        if os.path.exists(path):
            print(f"🧹 Deleting folder: {path}")
            shutil.rmtree(path)
            os.makedirs(path)
            print(f"✅ Recreated folder: {path}")
        else:
            print(f"ℹ️ Folder not found (skipped): {path}")

    @staticmethod
    def clean_all():
        print("🚀 Starting cleanup before test run...")
        for folder in ["logs", "screenshots", "reports", "allure-results", "allure-report"]:
            CleanupUtil.clean_dir(folder)
        print("🎉 Cleanup completed!")
