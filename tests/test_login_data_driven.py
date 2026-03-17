import time

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from playwright.sync_api import expect

from utils.data_reader_util import read_json_data, read_csv_data, read_excel_data

# Load/read the data from the test data files

csv_data = read_csv_data("testdata/logindata.csv")
json_data = read_json_data("testdata/logindata.json")
excel_data = read_excel_data("testdata/logindata.xlsx")


@pytest.mark.datadriven
@pytest.mark.parametrize("testName,email,password,expected",
                         excel_data)  # ki rokom data diye test korbo just ei place e change korlei hobe
def test_login_data_driven(page, testName, email, password, expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # login_page.set_email(Config.invalid_email)
    # login_page.set_password(Config.invalid_password)
    # login_page.click_login()

    login_page.login(email, password)
    time.sleep(2)

    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=3000)

    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=3000)
