from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

def getHtml(url):
    choise = input('Group or teacher? --> ')
    if choise.lower() == 'group':
        choise = 0
    elif choise.lower() == 'teacher':
        choise = 1
    else:
        print('Error')

    search = input('Input group number or last name and initials of the teacher --> ')
    print('Loading... Please wait...')

    sleepTime = 0

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-in-process-stack-traces")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--output=/dev/null")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Смена user-agent

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver = webdriver.Chrome(f'chromedrivers/chromedriver{version}.exe', options=options)

    try:
        print('Webdriver gets url...')
        driver.get(url)
        sleep(sleepTime)

        groupSelect = Select(driver.find_elements(By.TAG_NAME, 'select')[choise])
        groupSubmitButton = driver.find_elements(By.XPATH, "//input[@type='submit']")[choise]
        groupSelect.select_by_visible_text(search)
        sleep(sleepTime)
        groupSubmitButton.click()
        sleep(sleepTime)

        with open('indexSelenium.html', 'w') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)

    finally:
        print('The webdriver\'s work is finished...\n'
              'html has been uploaded to a file...')
        driver.close()
        driver.quit()
        parseHtml('indexSelenium.html')

def parseHtml(html):
    print('Unloading a file...')
    with open(html, 'r') as file:
        src = file.read()
    print('The parser has started his work...')
    soup = bs(src, 'lxml')
    objOfSearch = soup.find_all('h3')[1].text
    schedule = soup.find_all('b')
    schedule = [x.text for x in schedule]
    print('Result:\n')
    print(f'{objOfSearch}\n')
    [print(x) for x in schedule]
    print('\n')
    getHtml('https://www.rksi.ru/schedule')

def main():
    getHtml('https://www.rksi.ru/schedule')

if __name__ == '__main__':
    main()