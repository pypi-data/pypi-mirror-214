import logging
from typing import Any, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from twocaptcha import TwoCaptcha

logger = logging.getLogger('selenium_2captcha_solver')


def solve_recaptchav2(
        two_captcha: TwoCaptcha,
        driver: WebDriver,
        captcha_element: WebElement):
    logger.info("Solving captcha...")
    site_key = captcha_element.get_attribute('data-sitekey')
    text_area = captcha_element.find_element(
        By.ID, "g-recaptcha-response")

    res = _solve_captcha(
        two_captcha.recaptcha,
        sitekey=site_key,
        url=driver.current_url)

    code = res.get('code')
    if code is None:
        raise AttributeError(f"Can't solve captcha. Response text: {res}")
    driver.execute_script("arguments[0].style.display = 'block';", text_area)
    text_area.send_keys(code)
    driver.execute_script("arguments[0].style.display = 'none';", text_area)
    logger.info("Capctha solved")


def _solve_captcha(func, **kwargs) -> Dict[str, Any]:
    '''
    Wrapper just for easy monkeypatch
    '''
    return func(**kwargs)
