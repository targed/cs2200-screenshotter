import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def run_game(base_url: str, levels: list[tuple[str, int]], driver: webdriver.Chrome, save_file: str, screenshot_prefix: str):
    driver.get(base_url)
    # Load save file
    time.sleep(3)
    hamburger_menu = driver.find_element(By.CSS_SELECTOR, '#menu-btn')
    hamburger_menu.click()

    file_upload_button = driver.find_element(By.CSS_SELECTOR, '[title="Load Progress from JSON"]')
    file_upload_button.click()

    file_input = driver.find_element(By.CSS_SELECTOR, '[type=file]')
    file_input.send_keys(f'{os.getcwd()}/{save_file}')

    file_submit = driver.find_element(By.XPATH, '//*[text()="Load selected file"]')
    file_submit.click()

    # Levels are now loaded, visit each and screenshot

    for level in levels:
        for i in range(level[1]):
            level_idx = i + 1  # Skip the level 0 tutorial
            driver.get(f'{base_url}/world/{level[0]}/level/{level_idx}')
            time.sleep(8)
            driver.save_screenshot(f'screenshots/{screenshot_prefix}_{level[0]}_{i}.png')
            print(f"Saved screenshot {level[0]}/{i}")

    time.sleep(10)


def main():
    if not os.path.isdir('screenshots'):
        os.mkdir('screenshots')

    chrome_driver_path = 'chromedriver.exe'
    service = Service(chrome_driver_path)
    chrome_options = Options()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    nng_url = "https://adam.math.hhu.de/#/g/leanprover-community/nng4"
    nng_levels = [
        ("Tutorial", 8),
        ("Addition", 5),
        ("AdvAddition", 6),
        ("Multiplication", 9),
        ("Implication", 11),
        ("Algorithm", 9),
        ("Power", 10),
        ("LessOrEqual", 11),
        ("AdvMultiplication", 10)
    ]

    stg_url = "https://adam.math.hhu.de/#/g/djvelleman/stg4"
    stg_levels = [
        ("Subset", 6),
        ("Complement", 5),
        ("Intersection", 8),
        ("Union", 6),
        ("Combination", 5),
        ("FamInter", 6),
        ("FamUnion", 7),
        ("FamCombo", 8)
    ]

    logic_url = "https://adam.math.hhu.de/#/g/trequetrum/lean4game-logic"
    logic_levels = [
        ("AndIntro", 8),
        ("AndTactic", 8),
        ("ImpIntro", 9),
        ("ImpTactic", 9),
        ("OrIntro", 8),
        ("OrTactic", 8),
        ("NotIntro", 12),
        ("NotTactic", 12),
        ("IffIntro", 7),
        ("IffTactic", 7)
    ]

    run_game(nng_url, nng_levels, driver, 'nng.json', 'nng')
    run_game(stg_url, stg_levels, driver, 'stg.json', 'stg')
    run_game(logic_url, logic_levels, driver, 'logic.json', 'logic')


if __name__ == "__main__":
    main()
