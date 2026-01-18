import pytest
from pages.login_page import LoginPage
from utils.excel_util import ExcelUtil

data = ExcelUtil.get_test_data("ValidLogin")

@pytest.mark.parametrize("username,password,expected_title", data)
def test_login_excel(username, password, expected_title):
    login = LoginPage()
    login.login(username, password)

    assert expected_title in login.driver.title
