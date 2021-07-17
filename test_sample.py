from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as cond
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time


@allure.story('CRUD operations and related verifications on users at http://uitestpractice.com/Students/Index web page')
class TestClass():

    @allure.description('Setup chrome driver')
    @pytest.fixture(autouse=True)
    def driver(self):
        print("\n  initiating chrome driver")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        print("\n  navigate to http://uitestpractice.com/Students/Index")
        driver.get("http://uitestpractice.com/Students/Index")
        print("\n  maximize the window")
        driver.maximize_window()
        driver.implicitly_wait(5)
        yield driver
        print("\n  close the driver")
        driver.close()

    @allure.story('Functional test case 2')  # storydefine user scenarios
    def test_read(self, driver):
        data = self.get_details_of_the_first_student(driver)
        self.click_on_detail_button(driver)
        self.verify_details_of_the_first_student(driver, data)

    @allure.story('Functional test case 3')  # storydefine user scenarios
    def test_update(self, driver):
        print('TODO')

    @allure.story('Functional test case 3')  # storydefine user scenarios
    def test_delete(self, driver):
        print('TODO')

    @allure.title('Create a new user')
    @allure.description('Create a new user and verify that the user exists')
    def test_creation(self, driver):
        first_name = "Isaac"
        last_name = "Newton"
        enrollment_date = "2021.01.01"

        self.click_create_button(driver)
        self.closing_ad(driver)
        self.page_has_loaded(driver)
        self.create_user(driver, first_name, last_name, enrollment_date)
        self.search_for(driver, first_name, last_name)
        self.verify_the_creation_for(driver, first_name, last_name)

    @allure.step('Get the details of the student')
    def get_details_of_the_first_student(self, driver):
        table = driver.find_element_by_css_selector(".table")

        first_name = table.find_elements_by_css_selector("td")[0].text
        print("\n  Get the first name of the student")
        last_name = table.find_elements_by_css_selector("td")[1].text
        print("\n  Get the last name of the student")
        enrollment_date = table.find_elements_by_css_selector("td")[2].text
        print("\n  Get the enrollment date of the student")
        data = [first_name, last_name, enrollment_date]
        return data

    @allure.step('Verify the details of the student')
    def verify_details_of_the_first_student(self, driver, expected_data):
        container_content = driver.find_element_by_css_selector(".container.body-content")
        first = container_content.find_elements_by_css_selector("dd")[0]
        print("\n  Get the fisrt name of the student from the details menu")
        last = container_content.find_elements_by_css_selector("dd")[1]
        print("\n  Get the last name of the student from the details menu")
        date = container_content.find_elements_by_css_selector("dd")[2]
        print("\n  Get the enrollment date of the student from the details menu")
        details_title = container_content.find_element_by_css_selector("h2")
        student_title = container_content.find_element_by_css_selector("h4")
        actual = [first.text, last.text, date.text]
        assert len(actual) == len(expected_data)
        assert all([a == b for a, b in zip(actual, expected_data)])
        if not all([a == b for a, b in zip(actual, expected_data)]):
            raise Exception("The two lists are not equal")
        assert details_title.text == "Details"
        assert student_title.text == "Student"
        print("\n  Details are verified!")

    @allure.step('Click on details button')
    def click_on_detail_button(self, driver):
        details_button = driver.find_element_by_css_selector("table button:nth-child(2)")
        if str.lower(details_button.text) == "details":
            details_button.click()
            print("\n  Details button was clicked")
        else:
            print("\n  Details button does not exist!")

    @allure.step('Verify the creation')
    def verify_the_creation_for(self, driver, first_name, last_name):
        if driver.find_element_by_xpath("//*[contains(@class, 'container body-content')]/div") != None:
            error_msg = driver.find_element_by_xpath("//*[contains(@class, 'container body-content')]/div").text
            raise Exception(error_msg)
        else:
            self.verify_results(first_name, driver.find_element_by_css_selector("table.table td").text)
            self.verify_results(last_name, driver.find_element_by_css_selector("table.table td:nth-child(2)").text)

    @allure.step('Search for the user')
    def search_for(self, driver, first_name, last_name):
        search_data = driver.find_element_by_id("Search_Data")
        search_data.clear()
        search_data.click()
        search_data.send_keys(first_name + " " + last_name)
        print("\n  Search for user: {}.".format(first_name + " " + last_name))
        self.page_has_loaded(driver)
        if driver.find_element_by_css_selector("input.btn").get_attribute("value") == "Find":
            driver.find_element_by_css_selector("input.btn").click()
            print("\n  Find button was clicked")
        else:
            print("\n  There is no Find button")
        self.page_has_loaded(driver)

    @allure.step('Create user')
    def create_user(self, driver, first_name, last_name, date):
        WebDriverWait(driver, 10).until(cond.element_to_be_clickable((By.ID, 'FirstName')))
        first_name_input = driver.find_element_by_id('FirstName')
        first_name_input.send_keys(first_name)
        print("\n  First name: {} was populated.".format(first_name))

        last_name_input = driver.find_element_by_id('LastName')
        last_name_input.send_keys(last_name)
        print("\n  Last name: {} was populated.".format(last_name))

        enrollment_date = driver.find_element_by_id('EnrollmentDate')
        enrollment_date.send_keys(date)
        print("\n  Enrollment Date: {} was populated.".format(date))

        if driver.find_element_by_class_name("btn-default").get_attribute("value") == "Create":
            driver.find_element_by_class_name("btn-default").click()
            print("\n  Create button was clicked")
        else:
            print("\n  There is no Create button")

    @allure.step('Click on create button')
    def click_create_button(self, driver):
        create_new_button = driver.find_element_by_css_selector('button.btn.btn-info')
        create_new_button.click()
        print("\n  Create button was clicked")

    @allure.step('Close the ad')
    def closing_ad(self, driver):
        driver.switch_to.frame("aswift_2")
        driver.switch_to.frame("ad_iframe")

        if len(driver.find_elements_by_id("dismiss-button")) > 0:
            WebDriverWait(driver, 10).until(cond.element_to_be_clickable((By.ID, "dismiss-button")))
            driver.find_element_by_id("dismiss-button").click()
        else:
            driver.refresh()
        print("\n  The ad is closed")

    @allure.step('Verify results')
    def verify_results(self, expected_result, actual_result):
        print("\n  Checking if {} page is equals to {}.".format(expected_result, actual_result))
        if str.lower(actual_result) != expected_result:
            raise Exception("User was not found")
        else:
            return "Username found"

    def page_has_loaded(self, driver):
        print("\n  Checking if {} page is loaded.".format(driver.current_url))
        page_state = driver.execute_script('return document.readyState;')
        if page_state != 'complete':
            time.sleep(5)
