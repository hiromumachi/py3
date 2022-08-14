import traceback
import data
from log import logMain


#URL取得の関数
def createURLList():
    URLList=[]
    ###指定のシートからurlを取得###
    ##関数で取得##
    tmpURList=data.sellerList.get_worksheet(0).col_values(3,value_render_option='FORMULA')
    checklist=data.sellerList.get_worksheet(0).range(1,1,len(tmpURList),1)
    #取得した関数からurl取得(Listを繰り返す)
    try:
        for check,i in enumerate(tmpURList):
            if not "●" in str(checklist[check]):
                if "HYPERLINK" in i:
                    start=i.find('https')
                    end = i.find(",")
                    extract=i[start:end-1]
                    URLList.append(extract)
                else:
                    continue
            else:
                continue
        logMain.logger.info("URLリスト作成処理正常終了")
        return URLList
    except Exception as e:
        t = traceback.format_exception_only(type(e), e)
        logMain.logger.error("URLリスト作成処理エラー")
        logMain.logger.error(t)
        


#ASINの取得の関数
def createExList():
    logMain.logger.info("除外ASINリスト作成処理実行")
    try:
    #指定のシートから除外ASINを取得
        exList=data.exceptWB1.get_worksheet(0).col_values(1)
        exList=exList+data.exceptWB2.get_worksheet(0).col_values(1)
        exList=exList+data.exceptWB3.get_worksheet(0).col_values(1)
        exList=exList+data.exceptWB4.get_worksheet(0).col_values(1)
        exList=exList+data.exceptWB5.get_worksheet(0).col_values(1)
        exList=exList+data.exceptWB6.get_worksheet(0).col_values(3)
        exList=exList+data.exceptWB7.get_worksheet(0).col_values(3)
        exList=exList+data.exceptWB8.get_worksheet(0).col_values(3)
        exList=exList+data.exceptWB9.get_worksheet(0).col_values(3)
        exList=exList+data.exceptWB10.get_worksheet(0).col_values(3)
        
        logMain.logger.info("除外ASINリスト作成処理正常終了")
        return exList
    except Exception as e:
        t = traceback.format_exception_only(type(e), e)
        logMain.logger.error("除外ASINリスト作成処理エラー")
        logMain.logger.error(t)
        
