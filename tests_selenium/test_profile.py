import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_update_profile():
    browser = webdriver.Edge()
    try:
      
        browser.get("http://localhost:5000/login")

    
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys("123@gmail.com")
        browser.find_element(By.NAME, "password").send_keys("123456")
        
        submit_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='submit']"))
        )
        submit_btn.click()

     
        WebDriverWait(browser, 10).until(
            EC.url_changes("http://localhost:5000/login")
        )
        print("Login successful, current URL:", browser.current_url)

    
        profile_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Profile"))
        )
        profile_link.click()


        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
        )


        name_input = browser.find_element(By.ID, "name")
        height_input = browser.find_element(By.ID, "height")
        weight_input = browser.find_element(By.ID, "weight")


        name_input.clear()
        name_input.send_keys("New Name")

        height_input.clear()
        height_input.send_keys("180")

        weight_input.clear()
        weight_input.send_keys("75")

  
        save_btn = browser.find_element(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
        save_btn.click()

        time.sleep(2)  


    finally:
        browser.quit()


