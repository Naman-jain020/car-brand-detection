import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_and_store_images(group_url, save_dir, limit=30):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)  # Ensure chromedriver is in your PATH

    driver.get(group_url)
    time.sleep(5)  # Wait for page to load

    # Scroll to load images
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        # Break if no new content or enough images found
        if new_height == last_height or len(driver.find_elements(By.TAG_NAME, 'img')) >= limit:
            break
        last_height = new_height

    img_elements = driver.find_elements(By.TAG_NAME, 'img')
    count = 0
    for img in img_elements:
        if count >= limit:
            break
        src = img.get_attribute('src')
        if src and src.startswith('http') and ('staticflickr.com' in src or 'live.staticflickr.com' in src):
            try:
                img_data = requests.get(src).content
                ext = os.path.splitext(src)[1].split('?')[0]
                if ext.lower() not in ['.jpg', '.jpeg', '.png']:
                    ext = '.jpg'
                img_path = os.path.join(save_dir, f'img_{count}{ext}')
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                count += 1
            except Exception:
                continue

    driver.quit()
    return count
