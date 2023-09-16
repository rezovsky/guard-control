from selenium import webdriver


class Telegram:
    def get_images(self, groups, base_url):
        driver = webdriver.Chrome()

        for group in groups:
            # Открываем веб-страницу с HTML таблицей
            driver.get(f"{base_url}/group/{group}")

            # Создаем скриншот страницы
            driver.save_screenshot('table_screenshot.png')


        driver.quit()
        return
