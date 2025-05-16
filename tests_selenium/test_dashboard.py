import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def test_view_dashboard_time_filter():
    browser = webdriver.Chrome()

    try:
        
        browser.get("http://localhost:5000/login")
        time.sleep(2)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys("123@gmail.com")
        browser.find_element(By.NAME, "password").send_keys("123456")
        browser.find_element(By.CSS_SELECTOR, "input[type='submit'][name='submit']").click()
        time.sleep(2)

        
        WebDriverWait(browser, 10).until(
            EC.url_contains("/dashboard")
        )

        
        select_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "time-filter"))
        )
        select = Select(select_element)

        
        select.select_by_value("monthly")
        time.sleep(2)
        print("✅ Selected Last 6 Months")

        
        select.select_by_value("daily")
        time.sleep(2)
        print("✅ Selected Last 7 Days")

        

    finally:
        browser.quit()
