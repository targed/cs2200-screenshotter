import os
import time
import requests
import zipfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def load_save_file(base_url: str, driver: webdriver.Chrome, save_file: str):
    driver.get(base_url)
    
    time.sleep(3)
    # Finds the hamburger menu button using its CSS selector (#menu-btn) and clicks it to open the menu.
    hamburger_menu = driver.find_element(By.CSS_SELECTOR, '#menu-btn')
    hamburger_menu.click()
    
    # Finds the file upload button using its CSS selector ([title="Load Progress from JSON"]) and clicks it to open the file upload dialog.
    file_upload_button = driver.find_element(By.CSS_SELECTOR, '[title="Load Progress from JSON"]')
    file_upload_button.click()
    
    # Finds the file input element using its CSS selector ([type=file]) and sends the path of the save file to it. This simulates selecting a file for upload.
    file_input = driver.find_element(By.CSS_SELECTOR, '[type=file]')
    file_input.send_keys(f'{os.getcwd()}/{save_file}')

    # Finds the submit button using its XPath (//*[text()="Load selected file"]) and clicks it to load the selected save file.
    file_submit = driver.find_element(By.XPATH, '//*[text()="Load selected file"]')
    file_submit.click()

def set_slider_to_none(base_url: str, driver: webdriver.Chrome):
    driver.get(base_url)
    
    # Wait for the page to load and the slider to be present
    wait = WebDriverWait(driver, 20)
    slider = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.MuiSlider-root')))
    
    # Debugging: Print the page source to check if the element is present
    # print(driver.page_source)
    
    # Find the 'none' label element
    none_label = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'MuiSlider-markLabel') and text()='none']")))
    
    # Calculate the position to click (slightly above the 'none' label)
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(none_label, 0, -5).click().perform()
    
    # Wait for the change to take effect
    time.sleep(2)
    
    # Verify the change
    input_element = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Game Rules"]')
    value = input_element.get_attribute('aria-valuenow')
    
    if value == '0':
        print("Successfully set slider to 'none'")
    else:
        print(f"Failed to set slider to 'none'. Current value: {value}")
        
def download_and_extract_chromedriver():
    # Check if chromedriver.exe or chromedriver-win64 folder
    if os.path.isfile('chromedriver.exe') or os.path.isdir('chromedriver-win64'):
        print("ChromeDriver already downloaded and extracted.")
        return
    
    # URL for the ChromeDriver zip file
    url = 'https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.119/win64/chromedriver-win64.zip'
    
    # Download the zip file
    response = requests.get(url)
    zip_path = 'chromedriver-win64.zip'
    
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()
    
    # Move the chromedriver.exe to the current directory
    extracted_dir = 'chromedriver-win64'
    chromedriver_path = os.path.join(extracted_dir, 'chromedriver.exe')
    os.rename(chromedriver_path, 'chromedriver.exe')
    
    # Clean up the zip file and extracted directory
    os.remove(zip_path)
    shutil.rmtree(extracted_dir)
    
    print("ChromeDriver downloaded and extracted successfully.")
        

def run_game(base_url: str, levels: list[tuple[str, int]], driver: webdriver.Chrome, save_file: str, screenshot_prefix: str):
    
    load_save_file(base_url, driver, save_file)
    
    # Go to each of the worlds and set the rules slider to none
    set_slider_to_none(base_url, driver)

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
    download_and_extract_chromedriver()
    
    if not os.path.isdir('screenshots'):
        os.mkdir('screenshots')

    chrome_driver_path = 'chromedriver.exe'
    service = Service(chrome_driver_path)
    chrome_options = Options()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    nng_url = "https://adam.math.hhu.de/#/g/leanprover-community/nng4"
    nng_levels = [
        # ("Tutorial", 8),
        # ("Addition", 5),
        # ("AdvAddition", 6),
        # ("Multiplication", 9),
        # ("Implication", 11),
        # ("Algorithm", 9),
        ("Power", 10),
        # ("LessOrEqual", 11),
        # ("AdvMultiplication", 10)
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

    run_game(nng_url, nng_levels, driver, './json-files/nng.json', 'nng')
    # run_game(stg_url, stg_levels, driver, './json-files/stg.json', 'stg')
    # run_game(logic_url, logic_levels, driver, './json-files/logic.json', 'logic')


if __name__ == "__main__":
    main()
