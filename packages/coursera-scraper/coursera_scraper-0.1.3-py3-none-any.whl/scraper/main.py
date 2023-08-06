from .utils import go_to_course
from .constants import TIME_TO_WAIT
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def scraper(keyword, csv=True):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    url = f'https://www.coursera.org/search?query={keyword}&page=1&index' \
          f'=prod_all_launched_products_term_optimization_skills_test_for_precise_xdp_imprecise_variant'
    driver.get(url)
    driver.implicitly_wait(TIME_TO_WAIT)
    for course in go_to_course(driver, keyword, csv):
        yield course
