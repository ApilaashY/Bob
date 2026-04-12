import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def close_popups(driver):
    """Closes all windows except the currently active one."""
    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(main_window)

def findandget(movieName: str):

    driver = webdriver.Chrome()

    driver.get(f"https://einthusan.tv/movie/results/?lang=tamil&query={movieName}")

    # Check if we need to accept cookies
    
    if (driver.find_element(By.ID, "qc-cmp2-ui").is_displayed()):
        driver.find_element(By.XPATH, "//div[@class='qc-cmp2-summary-buttons']/button[3]").click()

    # Get the url
    url = driver.find_element(By.XPATH, "//section[@id='UIMovieSummary']/ul[1]/li[1]/div[1]/a[1]").get_attribute("href")

    # Open downloader
    # driver.close()
    driver.get("https://www.savethevideo.com/einthusan-tv-downloader")

    print(url)

    # Enter the url
    inputField = driver.find_element(By.XPATH, "//input[@class='block w-full py-3 text-base rounded-md placeholder-gray-500 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:flex-1 border-gray-300']")
    for char in url:
        inputField.send_keys(char)
        sleep(0.025)
    driver.find_element(By.XPATH, "//button[@class='flex items-center justify-center rounded-md shadow-sm border focus:outline-none relative bg-gray-800 hover:bg-gray-900 border-transparent focus:ring-gray-500 focus:ring-2 focus:ring-offset-2 px-6 py-3 text-base text-white mt-3 sm:mt-0 w-full sm:w-auto sm:ml-3']").click()
    
    close_popups(driver)
    
    sleep(3)

    print(driver.find_element(By.XPATH, "//div[@class='react-tabs__tab-panel react-tabs__tab-panel--selected']"))


    input()
    