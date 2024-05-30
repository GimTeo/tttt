from index.utils import logger
import datetime

import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
import random, time, os

randomSearch = ["아이스크림", "bts", "동킹콩", "플레이스테이션5", "디아블로", "매니아", "시계", "화장실", "축구", "올림픽", "아이스하키", "초콜렛", "테니스", "시간", "세계시간", "트럭", "날씨",
			"맛집", "서점", "스티커", "안경", "서류가방", "유튜브", "스피커 오른쪽", "모바일 요금제", "친구", "우산"]

randomBlog = [ "https://m.blog.naver.com/blue260260/223438496956",
			"https://m.blog.naver.com/yelin1890/223445565622",
			"https://m.post.naver.com/viewer/postView.naver?volumeNo=37582932&memberNo=15460571&vType=VERTICAL",
			"https://m.blog.naver.com/micahyesung/223430972968",
			"https://in.naver.com/imhana" ]
log = logger.__get_logger(__name__)

referer = ''
def makeTraffic(driver, search, pageIndex, mid) :
      driver.get('https://www.google.com')
      time.sleep(3)
      driver.get('https://m.naver.com')

      time.sleep(3)
      #fakeLikePerson(driver, 2)
      searchAndFind(driver, search, pageIndex, mid)
      clickNum = 0
      for i in range(0,2):
            clickNum += productClick(driver)
      log.info('makeTraffic done. clink num = ' + str(clickNum))
      time.sleep(70)
      if (clickNum > 1): return True
      else: return False

def fakeLikePerson(driver, loopNum):
      for i in range(0, loopNum) : # range(0, 3) -> 0~2 즉 3번
            random.randint(0, len(randomSearch))
            item = driver.find_element(By.CSS_SELECTOR, '#MM_logo > div.sch > section > div > div > form > div.sch_input_wrap')
            ActionChains(driver).click(item).perform()
            time.sleep(3)

            item = driver.find_element(By.ID, 'query')
            makeKey(driver, random.choice(randomSearch))
            time.sleep(3)
            item = driver.find_element(By.CSS_SELECTOR, '#sch_w > div > form > button')
            ActionChains(driver).click(item).perform()
            time.sleep(2.5)

            # Get scroll height
            prev_height = 0
            cur_height = driver.execute_script('return document.documentElement.scrollHeight')
            while prev_height < cur_height:
                  prev_height += 150; 
                  driver.execute_script("window.scrollTo(0,"+ str(prev_height)+");")
                  time.sleep(0.3)
            
            time.sleep(1.5)
            driver.back()
            time.sleep(2)
            if 'm.search.naver' in driver.current_url :
                  driver.back()

      driver.get(random.choice(randomBlog))
      time.sleep(2)
      driver.back()
      time.sleep(1.5)

def searchAndFind(driver, search, pageIndex, mid):
      urlList = []
      item = driver.find_element(By.CSS_SELECTOR, '#MM_logo > div.sch > section > div > div > form > div.sch_input_wrap') #검색창 찾기
      ActionChains(driver).click(item).perform()
      time.sleep(2)
      item = driver.find_element(By.ID, 'query') # 검색창만 떳을때 검색창 찾기
      makeKey(driver, search);
      time.sleep(1.5)
      item = driver.find_element(By.CSS_SELECTOR ,'#sch_w > div > form > button') # 검색버튼 찾기
      ActionChains(driver).move_to_element(item).perform()
      time.sleep(0.9)
      ActionChains(driver).click(item).perform()

      # Get scroll height
      prev_height = 0
      cur_height = 5200
      while prev_height < cur_height:
            prev_height = prev_height + 200; 
            driver.execute_script("window.scrollTo(0,"+ str(prev_height)+");")
            time.sleep(0.3)


      item = driver.find_element(By.CSS_SELECTOR ,'div.mod_more_wrap._more_root') #쇼핑더보기 찾기
      ob = item.find_element(By.CSS_SELECTOR, 'a')
      ActionChains(driver).move_to_element(ob).perform()
      time.sleep(0.9)
      ActionChains(driver).click(ob).perform()
      time.sleep(10)

      findIndex = False
      startIndex = 1
      pageMoveOnlyOnce = False
      if pageIndex > 7:
            startIndex = pageIndex - 3
      log.info("startIndex " + str(startIndex))
      for i in range(startIndex, pageIndex + 1):
            log.info("pageIndex " + str(i))
            # Get scroll height
            prev_height = 0
            cur_height = driver.execute_script('return document.documentElement.scrollHeight')
            while prev_height < cur_height:
                  prev_height = prev_height + 150
                  cur_height = driver.execute_script('return document.documentElement.scrollHeight')
                  driver.execute_script("window.scrollTo(0,"+ str(prev_height)+");")
                  time.sleep(0.32)
            time.sleep(2)
            if startIndex > 7 and pageMoveOnlyOnce == False:
                  pageMoveOnlyOnce = True
                  url = f'https://msearch.shopping.naver.com/search/all?adQuery={search}&frm=MOSCPRO&origQuery={search}&pagingIndex={str(i)}&pagingSize=40&productSet=total&query={search}&sort=rel&viewType=list'
                  driver.get(url)
                  log.info('pageMoveOnlyOnce = ' + str(pageMoveOnlyOnce))
                  time.sleep(2)
                  continue
      
            item = driver.find_element(By.CSS_SELECTOR , 'div[class^=paginator_inner]') #페이지 이동
            indexList = item.find_elements(By.CSS_SELECTOR ,'a')
            
            for e in indexList:
                  if e.get_attribute('text') == str(pageIndex) :
                        findIndex = True
                        ActionChains(driver).move_to_element(e).perform()
                        time.sleep(0.9)
                        ActionChains(driver).click(e).perform()
                        break
            
            if findIndex :
                  break
            else :
                  ActionChains(driver).move_to_element(indexList[4]).perform()
                  time.sleep(0.9)
                  ActionChains(driver).click(indexList[4]).perform()

      if findIndex == False:
            log.error("can not find item")
            raise Exception("can't find item")
      
      time.sleep(3)
      # Get scroll height
      prev_height = 0
      while prev_height < cur_height:
            prev_height = prev_height + 150; 
            cur_height = driver.execute_script('return document.documentElement.scrollHeight')
            driver.execute_script("window.scrollTo(0,"+ str(prev_height)+");")
            time.sleep(0.3)
      time.sleep(3)

      item = driver.find_element(By.CSS_SELECTOR, 'div[class^=listContainer_list]')
      itemList = item.find_elements(By.CSS_SELECTOR, 'div[class^=product_list_item]')
      adItemList = item.find_elements(By.CSS_SELECTOR, 'div[class^=adProduct_list_item]')
      global referer
      for e in itemList :
            ob = e.find_element(By.CSS_SELECTOR, 'a')
            if (mid in ob.get_attribute('href')) :
                  isFindMid = True
                  urlList.append(ob.get_attribute('href'))
                  ActionChains(driver).move_to_element(ob).perform()
                  referer = driver.current_url
                  time.sleep(0.9)
                  driver.request_interceptor = interceptor
                  ActionChains(driver).click(ob).perform()
                  driver.request_interceptor = interceptor
                  time.sleep(0.9)
                  #driver.get(ob.get_attribute('href'))
                  time.sleep(3.7)
                  break
      if isFindMid == False:
            for e in adItemList :
                  ob = e.find_element(By.CSS_SELECTOR, 'a')
                  if (mid in ob.get_attribute('href')) :
                        isFindMid = True
                        urlList.append(ob.get_attribute('href'))
                        ActionChains(driver).move_to_element(ob).perform()
                        referer = driver.current_url
                        time.sleep(0.9)
                        driver.request_interceptor = interceptor
                        ActionChains(driver).click(ob).perform()
                        driver.request_interceptor = interceptor
                        time.sleep(0.9)
                        #driver.get(ob.get_attribute('href'))
                        time.sleep(3.7)
                        break
      if isFindMid == False:
            log.error('can not find product in ' + str(pageIndex))
      for request in driver.requests:
             print(request.headers)
      # Get scroll height
      prev_height = 0
      cur_height = driver.execute_script('return document.documentElement.scrollHeight')
      while prev_height < cur_height:
            prev_height = prev_height + 120
            cur_height = driver.execute_script('return document.documentElement.scrollHeight')
            driver.execute_script("window.scrollTo(0,"+ str(prev_height)+");")
            time.sleep(0.4)
      time.sleep(1.7)

def productClick(driver) :
      clickNum = 0
      try:
            productPageElement = driver.find_element(By.CLASS_NAME, '_2VQFiEzw0j')
            productPageElementList = productPageElement.find_elements(By.CSS_SELECTOR, 'a')
            for product in productPageElementList :
                  ActionChains(driver).move_to_element(product).perform()
                  time.sleep(0.9)
                  ActionChains(driver).click(product).perform()
                  time.sleep(1.3)
                  clickNum +=1
            productPageElementList = driver.find_elements(By.CLASS_NAME, 'bd_3lIMK')
            ActionChains(driver).move_to_element(productPageElementList[len(productPageElementList)-1]).perform()
            time.sleep(1)
            ActionChains(driver).click(productPageElementList[len(productPageElementList)-1]).perform()
            clickNum +=1
            time.sleep(2.3)
            item = driver.find_element(By.CSS_SELECTOR, 'button[class^=bd_2QmR]')
            time.sleep(1)
            ActionChains(driver).click(item).perform()
            clickNum +=1
            time.sleep(1)
      except Exception as e :
            log.info('productClick fail' + str(clickNum))
      finally :
            log.info('productClick done = ' + str(clickNum))
            return clickNum

def makeKey(driver, string):
     for i in range(0, len(string)):
        ActionChains(driver).send_keys(string[i]).perform()
        time.sleep(1.3)

def interceptor(request):
    del request.headers['sec-ch-ua']
    request.headers['sec-ch-ua'] = '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"'
    del request.headers['sec-ch-ua-mobile']
    request.headers['sec-ch-ua-mobile'] = '?1'
    del request.headers['user-agent']
    request.headers['user-agent'] = 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    del request.headers['sec-ch-ua-platform']
    request.headers['sec-ch-ua-platform'] = '"Android"'
    del request.headers['accept-encoding']
    request.headers['accept-encoding'] = 'gzip, deflate, br, zstd'
    del request.headers['accept-language']
    request.headers['accept-language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    del request.headers['referer']
    request.headers['referer'] = referer
    del request.headers['sec-ch-ua-model']
    request.headers['sec-ch-ua-model'] = '"SM-G981B"'
    del request.headers['sec-ch-ua-platform-version']
    request.headers['sec-ch-ua-platform-version'] = '"13"'
    del request.headers['sec-ch-ua-form-factors']
    request.headers['sec-ch-ua-form-factors'] = '"Mobile"'
    print("interceptor success " + referer)
