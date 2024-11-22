import asyncio
import random

import aiofiles
import httpx
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("my_username")
password = os.getenv("password")

async def download_image(img_url: str, img_path: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(img_url)
        if response.status_code == 200:
            async with aiofiles.open(img_path, mode='wb') as file:
                await file.write(response.content)
            print('Success')
        else:
            print('Fail')


async def main(img_url: str, img_path: str) -> None:
    await download_image(img_url, img_path)

driver_path = r'E:\Instagram_image_downloader\chromedriver-win64\chromedriver.exe'

parsing_users = ['zamon.uz', 'realmadrid']


class ImageDownloader:
    def __init__(self, driver_path: str, username: str, password: str, list_of_users: list, image_path: str) -> None:
        self.service = Service(driver_path)
        self.service.start()

        try:
            self.driver = webdriver.Chrome(service=self.service)
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
            self.driver.get('https://www.instagram.com/')
            self.driver.maximize_window()
            user_name = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
            )
            user_name.send_keys(username)
            user_name.send_keys(Keys.ENTER)
            user_password = self.driver.find_element(By.XPATH, '//input[@name="password"]')
            user_password.send_keys(password)
            user_password.send_keys(Keys.ENTER)

            print('Search field clicking')

            search = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//div[@class='x1n2onr6 x6s0dn4 x78zum5'])[4] | (//div[@class='x1n2onr6'])[3]"))
            )
            search.click()
            # time.sleep(1)

            print('Search label clicking')
            search_label = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search input']"))
            )
            random_user = random.choice(list_of_users)
            search_label.send_keys(random_user)
            search_label.send_keys(Keys.ENTER)

            print('Username clicking')
            search_result = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{random_user}']"))
            )
            search_result.click()

            print('Image searching')
            images = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_aagv']/img"))
            )

            print(len(images))
            featured_img = random.choice([i.get_attribute('src') for i in images])
            asyncio.run(main(featured_img, image_path))
            # for img in images:
            #     print(img, '\n', img.get_attribute('src'))
        except Exception as ex:
            print("Error occured: ", ex)

        self.driver.close()
        self.driver.quit()


path = 'image_2.png'

if __name__ == '__main__':

    start = ImageDownloader(driver_path, username, password, parsing_users, path)
