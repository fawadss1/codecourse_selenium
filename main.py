import csv
import os
import time
import requests
import pyautogui as py
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
# from proxy import get_proxies

# get_proxies()

options = Options()
options.add_experimental_option('detach', True)
# options.add_extension('C:\Program Files (x86)\Internet Download Manager\IDMGCExt.crx')
driver = webdriver.Chrome(options)
driver.maximize_window()
baseUrl = 'https://codecourse.com/'
driver.get(baseUrl)
waitTime = 10

# try:
#     # Closing IDM Tab
#     py.moveTo(468, 12)
#     py.click()
# except:
#     pass


def system_login():
    driver.find_element('xpath', "//nav//div//a[text()='Sign in']").click()
    WebDriverWait(driver, waitTime).until(
        EC.visibility_of_all_elements_located(("xpath", "//div[@id='headlessui-dialog-panel-5']")))
    emailField = driver.find_element("xpath", "//input[@id='login-email']")
    emailField.clear()
    emailField.send_keys("info@suvastutech.com")
    passField = driver.find_element("xpath", "//input[@id='login-password']")
    passField.clear()
    passField.send_keys("Enrgtech@50")
    driver.find_element("xpath", "//div[@id='headlessui-dialog-panel-5']//button").click()


def course_cat():
    driver.get(baseUrl + "subjects")
    courseData = []
    contentLoad = WebDriverWait(driver, waitTime).until(
        EC.presence_of_element_located(
            ("xpath", "//div[@class='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 mt-8 md:mt-16']")))
    if contentLoad:
        cats = driver.find_elements('xpath',
                                    "//div[@class='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 "
                                    "mt-8 md:mt-16']//a")
        for i in cats:
            soup = BeautifulSoup(i.get_attribute('innerHTML'), "html.parser")
            courseName = soup.find("h1").text
            courseLink = i.get_attribute('href')
            courseData.append([courseName, courseLink])
        # Save the Categories data to a CSV file
        with open('csv_Data/cat/cats.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Course Name', 'Course Link'])
            writer.writerows(courseData)
    return courseData


def visit_course():
    catsFile = pd.read_csv('csv_Data/cat/cats.csv')
    name = catsFile['Course Name']
    links = catsFile['Course Link']
    cats = zip(name, links)
    for i, j in cats:
        driver.get(j)
        courseData = []
        try:
            courseTitle = driver.find_element("xpath",
                                              "//h1[@class='text-white text-3xl md:text-4xl font-semibold mt-4']").text
            while True:
                data = driver.find_elements("xpath", "//a[@class='block h-full']")
                for k in data:
                    soup = BeautifulSoup(k.get_attribute('innerHTML'), "html.parser")
                    title = soup.find("h2", class_="mt-2 text-dark-blue leading-snug font-medium").text
                    duration = soup.find("div", class_='whitespace-nowrap').text
                    episodes = soup.find("div", class_="text-xs text-dark-blue opacity-75 flex items-center mr-2").text
                    link = k.get_attribute('href')
                    courseData.append([i, title, duration, episodes, link])
                try:
                    driver.find_element("xpath", "//a[@class='ml-3 relative inline-flex items-center px-4 py-2 border "
                                                 "border-gray-3 text-sm font-medium rounded text-dark-blue bg-white "
                                                 "hover:bg-gray-50']").click()
                    time.sleep(3)
                except Exception as e:
                    break
            # Save the Courses data to a CSV file
            csvFile = f'csv_Data/courses/{courseTitle}.csv'
            with open(csvFile, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Category', 'Titles', 'Duration', 'Episodes', 'Links'])
                writer.writerows(courseData)
            # Save the Courses data to a JSON file
            df = pd.read_csv(csvFile, encoding='unicode_escape')
            df.to_json(f'json_data/{courseTitle}.json')
            print(f"<------{courseTitle} Completed--------->")
        except Exception as e:
            pass


def downloadCourses():
    catsFile = pd.read_csv('csv_Data/courses/Inertia.csv', encoding='unicode_escape')
    category = catsFile['Category']
    title = catsFile['Titles']
    links = catsFile['Links']
    courses = zip(category, title, links)
    for index, (i, j, k) in enumerate(courses):
        driver.get(k)
        time.sleep(1)
        # CLick On First Video Link
        WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located(
            ("xpath", "(//a//div//div//div//h2[contains(@class,'leading-snug')])[1]"))).click()
        courseTitle = f"{index + 1}. {j}"
        path = f"C:\\Users\\muh\\PycharmProjects\\codecourse_selenium\\Video_Lecs\\{i}\\{courseTitle}"
        driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': path})
        limit = 1
        while True:
            try:
                # Click on Download Button
                downloadBtn = WebDriverWait(driver, waitTime).until(
                    EC.visibility_of_element_located(("xpath", "//a[@disabled='false']")))

                # Simulate the keyboard shortcut for opening a link in a new tab
                ActionChains(driver).key_down(Keys.CONTROL).click(downloadBtn).key_up(Keys.CONTROL).perform()
                time.sleep(1)
                # time.sleep(5)
                # py.moveTo(1400, 250)
                # py.click()
                # time.sleep(2)
                # py.moveTo(1400, 255)
                # py.click()
                # time.sleep(2)
            except:
                print(f"({courseTitle}) Don't Have Download Button")
                break

            # Click on Next Button
            nextBtn = WebDriverWait(driver, waitTime).until(
                EC.visibility_of_element_located(("xpath", "(//div[contains(@class,'v-popper "
                                                           "v-popper--theme-tooltip')]//button)[3]")))
            nextBtn.click()
            if nextBtn.get_attribute("disabled") == 'true':
                break


# system_login()
# course_cat()
visit_course()
# downloadCourses()
