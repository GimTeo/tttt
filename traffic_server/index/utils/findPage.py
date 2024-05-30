import time
from index.utils import logger

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def getPageIndex(driver, search, mid) :
    log = logger.__get_logger(__name__)

    processTimeCheck = True;
    startTime = 0
    if (processTimeCheck) :
        startTime = time.time()

    isFindMid = False
    pageindex = 0
    try:
        for i in range(1, 200):
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

            URL = "https://msearch.shopping.naver.com/search/all?adQuery=" + search + "&origQuery=" + search + "&pagingIndex=" + str(i) + "&pagingSize=40&productSet=total&query=" + search + "&sort=rel&timestamp=&viewType=list";
            driver.get(URL);
            time.sleep(5)
            SCROLL_PAUSE_TIME = 0.8
            #print(driver.page_source)

            # Get scroll height
            prev_height = 0
            cur_height = driver.execute_script('return document.documentElement.scrollHeight')
            while prev_height < cur_height:
                    prev_height = prev_height + 250; 
                    cur_height = driver.execute_script('return document.documentElement.scrollHeight')
                    driver.execute_script("window.scrollTo(0,"+ str(prev_height)+");")
                    time.sleep(0.2)
            time.sleep(4);

            item = driver.find_element(By.CSS_SELECTOR, 'div[class^=listContainer_list]')
            list = item.find_elements(By.CSS_SELECTOR, 'div[class^=adProduct_list_item]')
            list2 = item.find_elements(By.CSS_SELECTOR, 'div[class^=product_list_item]')
            for e in list:
                ob = e.find_element(By.CSS_SELECTOR, 'a')
                if mid in ob.get_attribute("href"):
                    isFindMid = True
                    pageindex = i
            if isFindMid == False:
                for e in list2:
                    ob = e.find_element(By.CSS_SELECTOR, 'a')
                    if mid in ob.get_attribute("href"):
                        isFindMid = True
                        pageindex = i
            if isFindMid == True:

                break;
    except Exception as e :
        log.error("page index error ")
        log.error(e)
        driver.quit()
    finally:
        if (processTimeCheck) :
            finishTime = time.time()
            elapsedTime = finishTime - startTime
            log.info("Time of find page index = " + str(elapsedTime))
        if (isFindMid):
            log.info("page index was found = " + str(pageindex))
            return pageindex
        else:
            return -1