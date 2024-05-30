from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from index.utils import findPage
from index.utils import makeTraffic

import time
from index.utils import logger
import datetime

import undetected_chromedriver as uc
import seleniumwire.undetected_chromedriver as uc2

from selenium import webdriver

from seleniumwire import webdriver as wired_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from user_agents import parse
import random, time, os

log = logger.__get_logger(__name__)

# Create your views here.
def make_traffic(request : HttpRequest) :
    try:
        search = request.GET.get('search', '')
        mid = request.GET.get('mid', '')
        log.info("start => search : " + request.GET.get('search', '') + " , mid : " + request.GET.get('mid', ''))
        driver = getUCDriver(False)
        driver.delete_all_cookies()
        time.sleep(3)
        #driver.get('https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html')
        #driver.get('https://antoinevastel.com/bots')
        #time.sleep(5)

        # 3page
        # https://m.smartstore.naver.com/mzkorea/products/8215343094?NaPm=ct%3Dlwdjyrq8%7Cci%3D30d50e503f7c6371f1c3f27325a9dc1f774bddca%7Ctr%3Dslsf%7Csn%3D7504215%7Chk%3Da8a0de7f0c2b99947509f3f8265c4a350bb92cab
        # 82463519569 볼펜  11page
        # 80260846107  연필 1 page
        #index = findPage.getPageIndex(driver, search, mid)
        done = makeTraffic.makeTraffic(driver, '연필', 1, '80260846107')
        #done = makeTraffic.makeTraffic(driver, '볼펜', 1, '82699618371')

        if done == False:
            raise Exception("can't make click num")

    except Exception as e :
        log.error("error")
        print(e)
    finally :
        driver.quit()
        log.info("done")
    return HttpResponse("return this string")

def getUCDriver(headless) :
    options = uc2.ChromeOptions()
    #options = webdriver.ChromeOptions();
    options.add_argument(f"-–disable-blink-features=AutomationControlled")
    options.add_argument(f"--no-sandbox")
    options.add_argument(f"--disable-gpu")
    options.add_argument(f"--disable-infobars")
    #options.add_argument(f"--disable-dev-shm-usage")
    #options.add_argument(f"--single-process")
    options.add_argument(f"--window-size=360,738")
    options.add_argument(f"--ignore-certificate-errors")
    options.add_argument(f"--allow-running-insecure-content")
    options.add_argument(f"--disable-extensions")
    UA = 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    options.add_argument(f"--user-agent={UA}")
    #options.add_argument(f"--sec-ch-ua=\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"")
    #options.add_argument(f"--sec-ch-ua-mobile=?1")
    #options.add_argument(f"--sec-ch-ua-platform=\"Android\"")
    #options.add_argument(f"--upgrade-insecure-requests=1")
    options.add_argument(f"--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
    #options.add_argument(f"--sec-fetch-site=none")
    #options.add_argument(f"--sec-fetch-mode=navigate")
    #options.add_argument(f"--sec-fetch-user=?1")
    #options.add_argument(f"--sec-fetch-dest=document")
    options.add_argument(f"--accept-encoding=gzip, deflate, br, zstd")
    options.add_argument(f"--accept-language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")
    #options.add_experimental_option("useAutomationExtension", False)
    #options.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
    #mobile_emulation = { "deviceName": "Samsung Galaxy S20 Ultra" }
    #options.add_experimental_option("mobileEmulation", mobile_emulation)
    set_device_metrics_override = dict({
                "width": 360,
                "screenWidth": 360,
                "height": 738,
                "screenHeight": 738,
                "deviceScaleFactor": 50,
                "mobile": True,
                "hasTouch ": True
            })
    driver = uc2.Chrome(headless=headless, use_subprocess=True, options=options)
    set_ua_data = make_user_agent(UA, True)
    print(set_ua_data)
    time.sleep(2);
    driver.execute_cdp_cmd("Network.setUserAgentOverride", set_ua_data)
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', set_device_metrics_override)

    #stealth(
    #    driver,
    #    user_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0',
    #    languages = ["ko-KR","ko", "en-US", "en"],
    #    vendor = "Google Inc.",
    #    platform = 'Linux armv81',
    #    webgl_vendor = "Google Inc. (Qualcomm)",
    #    renderer = "ANGEL (Qualcomm, Adreno (TM) 740, OpenGL ES 3.2)",
    #    fix_hairline = True,
    #    run_on_insecure_origins = True,
    #)
    # 스텔스 사용시 ua 관련 정보 없음.. 이유 모름..
    driver.implicitly_wait(5)
    log.info("driver set done")

    return driver

def getDriver(headless) :
    options = webdriver.ChromeOptions();
    #options.add_argument(f"--headless=new")
    #options.add_argument(f"-–disable-blink-features=AutomationControlled")
    options.add_argument(f"--no-sandbox")
    options.add_argument(f"--disable-gpu")
    options.add_argument(f"--window-size=360,738")
    #options.add_argument(f"--ignore-certificate-errors")
    #options.add_argument(f"--allow-running-insecure-content")
    options.add_argument(f"--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    mobile_emulation = { "deviceName": "Samsung Galaxy S20 Ultra" }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = wired_webdriver.Chrome(options=options)
    time.sleep(2);

    stealth(
        driver,
    #    user_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 Edg/124.0.0.0',
    #    languages = ["ko-KR","ko", "en-US", "en"],
    #    vendor = "Google Inc.",
        platform = 'Linux armv81',
        webgl_vendor = "Google Inc. (Qualcomm)",
        renderer = "ANGEL (Qualcomm, Adreno (TM) 740, OpenGL ES 3.2)",
        fix_hairline = True,
    #    run_on_insecure_origins = True,
    )
    # 스텔스 사용시 ua 관련 정보 없음.. 이유 모름..
    driver.implicitly_wait(5)
    log.info("driver set done")

    return driver

def make_user_agent(ua,is_mobile):
    user_agent = parse(ua)
    model = user_agent.device.model
    platform = user_agent.os.family
    platform_version = user_agent.os.version_string + ".0.0"
    version = user_agent.browser.version[0]
    ua_full_version = user_agent.browser.version_string
    architecture = "x86"
    print(platform)
    if is_mobile:
        platform_info = "Linux armv8l"
        architecture= ""
    else: # Window
        platform_info = "Win32"
        model = ""
    RET_USER_AGENT = {
        "appVersion" : ua.replace("Mozilla/", ""),
        "userAgent": ua,
        "platform" : f"{platform_info}",
        "acceptLanguage" : "ko-KR, kr, en-US, en",
        "userAgentMetadata":{
            "brands" : [
                {"brand":" Not A;Brand", "version":"99"},
                {"brand":"Google Chrome", "version":f"{version}"},
                {"brand":"Chromium", "version":f"{version}"}
            ],
            "fullVersion":f"{ua_full_version}",
            "platform" :platform,
            "platformVersion":platform_version,
            "architecture":architecture,
            "model" : model,
            "mobile":is_mobile #True, False
        }
    }
    return RET_USER_AGENT