import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# open the webpage
driver.get("http://www.instagram.com")

# target username
username = WebDriverWait(
	driver, 10).until(EC.element_to_be_clickable(
		(By.CSS_SELECTOR, "input[name='username']")))

# target Password
password = WebDriverWait(
	driver, 10).until(EC.element_to_be_clickable(
		(By.CSS_SELECTOR, "input[name='password']")))

# enter username and password
username.clear()
username.send_keys("developer_7450")
password.clear()
password.send_keys("3_6HkFWxQS._Ku6")

# target the login button and click it
button = WebDriverWait(
	driver, 2).until(EC.element_to_be_clickable(
		(By.CSS_SELECTOR, "button[type='submit']"))).click()

time.sleep(5)

driver.get("https://www.instagram.com/marketsformakers/followers/")

# driver.find_element_by_partial_link_text("followers").click()

pop_up_window = WebDriverWait(
	driver, 2).until(EC.element_to_be_clickable(
		(By.XPATH, "//div[@class='isgrP']")))

# Scroll till Followers list is there
while True:
	driver.execute_script(
		'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
	pop_up_window)
	time.sleep(1)

driver.quit()
