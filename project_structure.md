selenium-python-framework/
│
├── config/
│   ├── qa.yaml
│   ├── uat.yaml
│   └── prod.yaml
│
├── core/
│   ├── driver_factory.py
│   ├── base_test.py
│   └── framework_constants.py
│
├── pages/
│   ├── base_page.py
│   └── login_page.py
│
├── utils/
│   ├── config_reader.py
│   ├── selenium_utils.py
│   ├── wait_utils.py
│   ├── screenshot_util.py
│   ├── excel_util.py
│   ├── email_util.py
│   ├── log_util.py
│   └── cleanup_util.py
│
├── listeners/
│   └── pytest_hooks.py
│
├── tests/
│   └── test_login.py
│
├── logs/
├── reports/
├── screenshots/
│
├── docker-compose.yml
├── Jenkinsfile
├── pytest.ini
├── requirements.txt
└── README.md
