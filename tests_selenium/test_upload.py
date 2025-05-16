import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import os

def test_upload_and_view_dashboard():
    browser = webdriver.Chrome()

    try:
        browser.get("http://localhost:5000/login")
        time.sleep(1)


        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys("123@gmail.com")
        browser.find_element(By.NAME, "password").send_keys("123456")

        browser.find_element(By.CSS_SELECTOR, "input[type='submit'][name='submit']").click()
        time.sleep(2)

        upload_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Upload Data"))
        )
        upload_link.click()
        time.sleep(2)

        relative_path = Path("tests_selenium/uploads/sample.csv")
        absolute_path = os.path.abspath(relative_path)

        # choose the file to upload
        file_input = browser.find_element(By.ID, "file-upload")
        # ✅ Force input visible before interacting (important for hidden file inputs)
        browser.execute_script("arguments[0].classList.remove('hidden')", file_input)
        file_input.send_keys(absolute_path)
        time.sleep(1)

        # click the upload button
        upload_btn = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(@class, 'btn') and contains(@class, 'bg-indigo-600') and normalize-space()='Upload Data']"
    ))
)
        upload_btn.click()

        #  Dashboard 
        dashboard_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Dashboard"))
        )
        dashboard_link.click()
        time.sleep(2)



    finally:
        browser.quit()
