import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
def test_register():
    browser = webdriver.Chrome()
    test_email = "user5@example.com"
    try:
 
        browser.get("http://127.0.0.1:5000/register")
        time.sleep(2)


        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )
        time.sleep(1)

  
        browser.find_element(By.NAME, "name").send_keys("User5")
        time.sleep(1)


        browser.find_element(By.NAME, "email").send_keys(test_email)
        time.sleep(1)

     
        browser.find_element(By.NAME, "password").send_keys("TestPass123")
        time.sleep(1)


        browser.find_element(By.NAME, "confirm_password").send_keys("TestPass123")
        time.sleep(1)

  
        select_gender = Select(browser.find_element(By.ID, "gender"))
        select_gender.select_by_visible_text("Female")
        time.sleep(1)

    
        dob_element = browser.find_element(By.ID, "dob")
        browser.execute_script("arguments[0].value = arguments[1]", dob_element, "1995-01-01")
        time.sleep(1)

        browser.find_element(By.ID, "height").send_keys("175")
        time.sleep(1)

   
        browser.find_element(By.ID, "weight").send_keys("70")
        time.sleep(1)

  
        browser.find_element(By.ID, "medical_conditions").send_keys("None")
        time.sleep(1)

        before_url = browser.current_url
 
        submit_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='submit']"))
        )
        submit_btn.click()
        time.sleep(2)


        WebDriverWait(browser, 10).until(
            lambda d: d.current_url != before_url
        )
        print("success", browser.current_url)
        conn = sqlite3.connect('instance/app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (test_email,))
        result = cursor.fetchone()
        conn.close()

        assert result is not None, "Email not found in the database, registration failed!"
    finally:
        browser.quit()
