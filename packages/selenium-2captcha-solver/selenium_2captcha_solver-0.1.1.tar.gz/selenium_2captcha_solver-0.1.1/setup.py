# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selenium_2captcha_solver']

package_data = \
{'': ['*']}

install_requires = \
['2captcha-python>=1.2.0,<2.0.0', 'selenium>=4.10.0,<5.0.0']

setup_kwargs = {
    'name': 'selenium-2captcha-solver',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Selenium 2CAPTCHA solver\n\n# Usage\n```python\nfrom selenium_2captcha_solver import solve_recaptchav2\nfrom twocaptcha import TwoCaptcha\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\n\n# Create TwoCaptcha instance\ntwo_captcha = TwoCaptcha(apiKey="2CAPTCHA_API_KEY")\n\n# Create selenium driver instance and open page with captch you need to solve\ndriver = webdriver.Chrome()\ndriver.get("https://www.google.com/recaptcha/api2/demo")\n\n# Find recaptcha element\nrecaptcha_element = driver.find_element(By.CLASS_NAME, \'g-recaptcha\')\n\n# Call the solve_recaptchav2\nsolve_recaptchav2(two_captcha, driver, recaptcha_element)\n\n# And submit your form or anything else\ndriver.find_element(By.ID, "recaptcha-demo-submit").click()\n```\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
