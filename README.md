# Selenium Python Enterprise Framework

## Features
- PyTest
- Selenium Grid
- Parallel execution
- Page Object Model
- Allure reports
- Retry logic
- Failure screenshots
- Logging
- Docker ready
- Jenkins ready

## Install
pip install -r requirements.txt

## Run
pytest --env=qa --browser=chrome

## Parallel
pytest -n 3

## Allure
allure serve allure-results

## Fully Automatic (Local) Allure report
Create a batch or shell script.
Windows (create run_tests.bat)
python -m pytest -v
allure generate allure-results -o allure-report --clean
allure open allure-report
