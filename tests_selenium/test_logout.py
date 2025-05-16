import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_and_logout():
    browser = webdriver.Chrome()

    try:
        browser.get("http://localhost:5000/login")
        time.sleep(2)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys("123@gmail.com")
        time.sleep(1)

        browser.find_element(By.NAME, "password").send_keys("123456")
        time.sleep(1)

        submit_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='submit']"))
        )
        submit_btn.click()
        time.sleep(2)

        WebDriverWait(browser, 10).until(
            EC.url_changes("http://localhost:5000/login")
        )
        print("Login successful, current URL:", browser.current_url)

      
        logout_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Logout')]"))
        )
        logout_btn.click()
        time.sleep(2)

   
        WebDriverWait(browser, 10).until(
            EC.url_contains("/login")
        )
        print("Logout successful, returned to:", browser.current_url)

    finally:
        browser.quit()
