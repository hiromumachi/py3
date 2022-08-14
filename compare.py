import traceback
import create_list
import data
import pandas as pd
from gspread_dataframe import set_with_dataframe
from log import logMain


def compare(List):
    exList = create_list.createExList()
    asinList=List
    necessarilyAsin=[]
    try:
        for asin in asinList:
            if asin in exList:
                continue
            else:
                necessarilyAsin.append(asin)
        logMain.logger.info("書き出したASIN"+str(len(necessarilyAsin))+"件")
        logMain.logger.info("除外したASIN"+str(len(asinList)-len(necessarilyAsin))+"件")
        logMain.logger.info("比較処理正常終了")
        return necessarilyAsin
    except Exception as e:
        t = traceback.format_exception_only(type(e), e)
        logMain.logger.error("比較処理エラー")
        logMain.logger.error(t)
        

def writeSheet(asinList):
    try:
        data.resultWB.worksheet("ASINリスト").clear
        df=pd.DataFrame(asinList,columns=["ASIN"])
        set_with_dataframe(data.resultWB.worksheet("ASINリスト"),df,include_column_header=False)
        logMain.logger.info("書き込み完了")
    except Exception as e:
        t = traceback.format_exception_only(type(e), e)
        logMain.logger.error("書き込みエラー")
        logMain.logger.error(t)
        