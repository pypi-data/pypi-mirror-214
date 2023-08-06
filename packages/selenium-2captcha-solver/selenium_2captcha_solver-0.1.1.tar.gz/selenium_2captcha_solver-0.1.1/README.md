# Selenium 2CAPTCHA solver

# Usage
```python
from selenium_2captcha_solver import solve_recaptchav2
from twocaptcha import TwoCaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create TwoCaptcha instance
two_captcha = TwoCaptcha(apiKey="2CAPTCHA_API_KEY")

# Create selenium driver instance and open page with captch you need to solve
driver = webdriver.Chrome()
driver.get("https://www.google.com/recaptcha/api2/demo")

# Find recaptcha element
recaptcha_element = driver.find_element(By.CLASS_NAME, 'g-recaptcha')

# Call the solve_recaptchav2
solve_recaptchav2(two_captcha, driver, recaptcha_element)

# And submit your form or anything else
driver.find_element(By.ID, "recaptcha-demo-submit").click()
```
