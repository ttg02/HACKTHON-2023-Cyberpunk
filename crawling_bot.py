from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from functionSQL import init, insert_data
import warnings
warnings.filterwarnings('ignore')

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--disable-notifications")
opt.add_argument("--disable-gpu")
opt.add_argument("--headless")
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

url = 'https://www.amazon.com/s?i=specialty-aps&bbn=16225006011&rh=n%3A%2116225006011%2Cn%3A11060451&ref=nav_em__nav_desktop_sa_intl_skin_care_0_2_11_3'

driver = driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = opt)
driver.get(url)

json_star = {1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five'}


def get_comment(list_comments, name_product, star): 
    for comment in list_comments: 
        json = {'category' : "Boy's Fashion", 'sub-category' : 'Clothing', 
                'name_product' : name_product, 'star' : star, 'title' : '', 'comment' : ''}

        json['title'] = comment.find_element(By.CSS_SELECTOR, '[data-hook="review-title"]').text
        json['comment'] = comment.find_element(By.CSS_SELECTOR, '[data-hook="review-body"]').text
        
        insert_data(list(json.values()), conn, cursor)

i = 1 
while True:
    try:
        conn, cursor = init()
        lst = driver.find_elements(By.CLASS_NAME, 'a-section.a-spacing-base')
        print(f'Crawling page {i}')

        for idx, pro in enumerate(lst):
            try:
                name_product = pro.find_element(By.CLASS_NAME, 'a-size-base-plus.a-color-base.a-text-normal').text

                try:
                    product_id = pro.find_element(By.CLASS_NAME, 'a-popover-preload').get_attribute('id')[::-1].split('-')[0][::-1]
                except: 
                    product_id = pro.find_element(By.CLASS_NAME, '''s-widget-container.s-spacing-small.s-widget-
                                                container-height-small.celwidget.slot=MAIN.template=SEARCH_RESULTS.widgetId=search-results_4''')\
                                                    .get_attribute('data-csa-c-item-id').split('.')[-1]

                for star in range(1,6):
                    star_name = json_star[star]

                    url_star = f'https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_{star}?ie=UTF8&filterByStar={star_name}_star&reviewerType=all_reviews#reviews-filter-bar'

                    driver.execute_script("window.open('{}', '_blank');".format(url_star))
                    handles = driver.window_handles
                    new_window = handles[-1]
                    driver.switch_to.window(new_window)

                    # check number comment on pages
                    list_comments = driver.find_elements(By.CLASS_NAME, 'a-section.review.aok-relative')

                    try:
                        while True: 
                            get_comment(list_comments, name_product, star)
                            try: 
                                driver.find_element(By.CLASS_NAME, 'a-last').click()
                                continue
                            except:
                                break
                    except:
                        pass
                    
                    driver.close() 

                    handles = driver.window_handles
                    new_window = handles[0]
                    driver.switch_to.window(new_window)
            except:
                pass
        conn.close()
    except: 
        print(f'No crawling page {i}')
        pass
    
    ## button next_page product 
    try: 
        next_page = driver.find_element(By.XPATH, '//a[contains(@aria-label, "Go to next page")]')
    except: 
        next_page= driver.find_element(By.CLASS_NAME, 's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
    ex
    next_page.click()
    time.sleep(2)
    i += 1 