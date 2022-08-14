from time import sleep
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from log import logMain



def scrapingFun(urlList):
    errorflg=0
    asinList=[]
    errorAsin=[]
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    funtime=0
    ###セラーページ分繰り返す###
    for url in urlList:
        ##例外処理
        try:
            driver = webdriver.Chrome(executable_path='./driver/chromedriver',chrome_options=options)
        #起動が掛かるまで待つ
            driver.implicitly_wait(30)
        #セラーページ取得
            driver.get(url)
            driver.find_element_by_xpath("//*[@class='a-link-normal']").click()
            ##セラーページの次へがなくなるまで
            #ページのASINを取得
            pageCount=1
            while True:
                tmpAsinList=driver.find_elements_by_xpath("//*[@class='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16']")
                for tmpAsin in tmpAsinList: 
                    asinList.append(tmpAsin.get_attribute("data-asin"))
                try:
                    if pageCount%100==0:
                        cul=driver.current_url
                        driver.get(cul)
                        sleep(20)
                    pageCount+=1
                    nextButton=driver.find_element_by_link_text("次へ")
                    nextButton.click()
                    sleep(3)
                except NoSuchElementException :
                    break
            logMain.logger.info(str(funtime+1)+"サイト目正常終了")
        except Exception as e:
            errorflg=1
            errorAsin.append(url)
            t = traceback.format_exception_only(type(e), e)
            logMain.logger.error("スクレイピングエラー")
            logMain.logger.error(t)
            logMain.logger.warn(str(funtime+1)+"サイト目異常終了")
            continue
        finally:
            funtime+=1
            driver.quit()
    if errorflg==0:
        logMain.logger.info("スクレイピング正常終了")
    else:
        logMain.logger.warning("スクレイピング異常終了")
    return  asinList,errorAsin
        
 