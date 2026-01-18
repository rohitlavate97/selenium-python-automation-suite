from pages.login_page import LoginPage

def test_login():
    login = LoginPage()
    login.login("admin", "manager")


# from pages.login_page import LoginPage
# import allure
#
# @allure.epic("Authentication")
# @allure.feature("Login")
# @allure.story("Valid Login")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_login():
#     login = LoginPage()
#     login.login("admin", "manager")
