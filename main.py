from apscheduler.executors.pool import ThreadPoolExecutor
import traceback
import compare
import scraping
import create_list
import numpy as np
from log import logMain
import datetime
import data
from apscheduler.schedulers.blocking import BlockingScheduler
import sys


def mainFunc():
    try:
        open('./log/log.txt','w')
        today = datetime.datetime.today().strftime("%Y%m%d")
        logMain.logger.info("処理開始")
    except Exception as e:
        t = traceback.format_exception_only(type(e), e)
        logMain.logger.error("初期処理エラー")
        logMain.logger.error(t)
        sys.exit

    if __name__ == '__main__':
        try:
            logMain.logger.info("URLリスト作成処理実行")
            urllist=create_list.createURLList()
        except Exception as e:
            t = traceback.format_exception_only(type(e), e)
            logMain.logger.error("URLリスト作成処理呼び出しエラー")
            logMain.logger.error(t)
            
        try:
            #スクレイピング実行
            logMain.logger.info("スクレイピング1回目実行")
            scrapingResult=scraping.scrapingFun(urllist)
            success=scrapingResult[0]
            errorURL=scrapingResult[1]
            success=list(set(success))
            logMain.logger.info("取得したASIN数"+str(len(success))+"件")
        except Exception as e:
            t = traceback.format_exception_only(type(e), e)
            logMain.logger.error("スクレイピング呼び出しエラー")
            logMain.logger.error(t)
            sys.exit
        if len(errorURL)>0:
            try:
                #スクレイピング実行
                logMain.logger.warning("エラーしたサイト数"+str(len(errorURL))+"件")
                logMain.logger.info("スクレイピング2回目実行")
                scrapingResult2=scraping.scrapingFun(errorURL)
                oldResult=np.array(success)
                newResult=np.array(scrapingResult2[0])
                error2=scrapingResult2[1]
                success=np.hstack((oldResult,newResult))
                success=list(set(success))
                logMain.logger.info("取得したASIN数"+str(len(newResult))+"件")
                logMain.logger.info("重複削除済みASIN数"+str(len(success))+"件")
                logMain.logger.warning("エラーしたサイト数"+str(len(error2))+"件")
            except Exception as e:
                t = traceback.format_exception_only(type(e), e)
                logMain.logger.error("スクレイピング呼び出しエラー2")
                logMain.logger.error(t)
                
        try:   
            #比較実行
            logMain.logger.info("比較処理実行")
            compareResult=compare.compare(success)
            ##書き込み開始
            #書き込み実行
            logMain.logger.info("書き込み実行")
            compare.writeSheet(compareResult)
        except Exception as e:
            t = traceback.format_exception_only(type(e), e)
            logMain.logger.error("ASIN比較処理呼び出しエラー")
            logMain.logger.error(t)
            

        try:
            logMain.logger.info("処理終了")
            #ドライブにログをアップロード
            logMain.logger.info("ログアップロード実行")
            logMain.uploadFileToGoogleDrive("ログ"+today,'./log/log.txt','text/plain',data.credentials)
        except Exception as e:
            t = traceback.format_exception_only(type(e), e)
            logMain.logger.error("ログアップロードエラー")
            logMain.logger.error(t)
           

#毎日決まった時刻に実行
scheduler = BlockingScheduler(executors={'default': ThreadPoolExecutor(1)})
scheduler.add_job(mainFunc,'cron',hour=0, minute=1)
scheduler.add_job(mainFunc,'interval', seconds=3)
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    logMain.logger.error("処理開始エラー")
    scheduler.remove_all_jobs()
    sys.exit








