# ================================
# STEP 1: Install Required Software
# ================================

# Install Python 3.10+
# https://www.python.org/downloads/
# ✔ Check "Add Python to PATH"

python --version

# Install PyCharm Community Edition
# https://www.jetbrains.com/pycharm/download/

# (Optional) Install Allure
# Windows:
scoop install allure

# Mac:
brew install allure

allure --version


# ================================
# STEP 2: Create Project in PyCharm
# ================================

# Open PyCharm
# Click New Project
# Name: selenium-python-framework
# Choose: New Virtual Environment
# Click Create


# ================================
# STEP 3: Create Folder Structure
# ================================

selenium-python-framework/
│
├── config
├── core
├── pages
├── utils
├── listeners
├── tests
├── logs
├── reports
├── screenshots
├── videos


# ================================
# STEP 4: Create Python Files
# ================================

# core/
driver_factory.py
base_test.py
framework_constants.py

# utils/
config_reader.py
selenium_utils.py
wait_utils.py
screenshot_util.py
excel_util.py
email_util.py
log_util.py
cleanup_util.py
slack_util.py
video_util.py

# pages/
base_page.py
login_page.py

# listeners/
pytest_hooks.py

# tests/
test_login.py
test_login_excel.py


# ================================
# STEP 5: Create requirements.txt
# ================================

selenium
pytest
pytest-xdist
pytest-rerunfailures
allure-pytest
webdriver-manager
pyyaml
openpyxl
requests


# ================================
# STEP 6: Install Dependencies
# ================================

pip install -r requirements.txt


# ================================
# STEP 7: Create config YAML
# ================================

# config/qa.yaml

URL: "https://online.actitime.com/mstar/login.do"
BROWSER: "chrome"
GRID: false
GRID_URL: "http://localhost:4444/wd/hub"
HEADLESS: false
IMPLICIT_TIMEOUT: 10

EMAIL:
  FROM: "your@gmail.com"
  PASSWORD: "app-password"
  TO: ["a@gmail.com"]


# ================================
# STEP 8: Run Tests
# ================================

pytest --env=qa --browser=chrome


# ================================
# STEP 9: Parallel Execution
# ================================

pytest -n 3


# ================================
# STEP 10: Allure Report
# ================================

allure serve allure-results


# ================================
# STEP 11: Run on Selenium Grid
# ================================

# Start Docker Grid
docker-compose up -d

# Open in browser:
http://localhost:4444/ui

# Update qa.yaml
GRID: true

pytest


# ================================
# STEP 12: How to Write a Test
# ================================

def test_login():
    page = LoginPage()
    page.login("admin", "manager")

#REMOVE PYTHON CACHE (VERY IMPORTANT)
From project root, run:

Git Bash / PyCharm Terminal
rm -rf __pycache__
rm -rf core/__pycache__
rm -rf utils/__pycache__

To run test: python -m pytest -v