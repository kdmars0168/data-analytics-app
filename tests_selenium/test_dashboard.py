import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def test_view_dashboard_time_filter():
    browser = webdriver.Chrome()

    try:
        # Step 1: 登录
        browser.get("http://localhost:5000/login")
        time.sleep(2)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys("123@gmail.com")
        browser.find_element(By.NAME, "password").send_keys("123456")
        browser.find_element(By.CSS_SELECTOR, "input[type='submit'][name='submit']").click()
        time.sleep(2)

        # Step 2: 等待跳转到 dashboard
        WebDriverWait(browser, 10).until(
            EC.url_contains("/dashboard")
        )

        # Step 3: 等待时间过滤器出现
        select_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "time-filter"))
        )
        select = Select(select_element)

        # Step 4: 选择 "Last 6 Months"
        select.select_by_value("monthly")
        time.sleep(2)
        print("✅ Selected Last 6 Months")

        # Step 5: 再选 "Last 7 Days"
        select.select_by_value("daily")
        time.sleep(2)
        print("✅ Selected Last 7 Days")

        # （可选）检查某些数据是否已更新

    finally:
        browser.quit()
