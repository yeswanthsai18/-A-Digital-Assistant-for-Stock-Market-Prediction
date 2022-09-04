#============================================================================================Import Libraries
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
#=============================================================================================Ignore Warnings
import warnings
warnings.filterwarnings("ignore")
#============================================================================================Global Variables
webpage_list = []
webpage_url = "https://www.tickertape.in/stocks?filter="
webpage_dirs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'others']
stock_symbol = []
stock_name = []
stock_industry = []
stock_market_cap = []
stock_risk_level = []
stock_ticker_url = []
opinion = []
#===========================================================================================Process Functions
def urlToMarkup(url) -> object:
    html_data = bs(requests.get(url).content)
    return html_data

def writeCSV(data , file_name) -> None:
    data_obj = pd.DataFrame(data) 
    data_obj.to_csv(file_name, index = False) 
#===============================================================================================Main Function
def main() -> None:    
    global webpage_list
    global webpage_url
    global webpage_dirs
    global stock_symbol
    global stock_name
    global stock_industry
    global stock_market_cap
    global stock_risk_level
    global stock_ticker_url
    global opinion
    for i in range(len(webpage_dirs)):
        url = webpage_url + webpage_dirs[i]
        markup_data = urlToMarkup(url)
        if(webpage_dirs[i] not in ['i', 's', 'others']):
            anchor_tags = markup_data.find_all("a", {'class':'jsx-1528870203'})
        else:
            anchor_tags = markup_data.find_all("a")
        for tag in anchor_tags:
            try:
                path_url = "https://www.tickertape.in" + tag.get('href') + "?checklist=basic"
                if(path_url not in webpage_list and '/stocks/' in path_url):
                    webpage_list.append(path_url)
            except:
                pass
            finally:
                pass
    for url in webpage_list:
        web_data = urlToMarkup(url)
        try:
            icr = web_data.find_all("span", {'class':['jsx-1803365110','stock-label-title']})
        except:
            icr.append('N/A')
            
        string = ""
        for w in icr:
            string += w.text
        
        #-----------------------------------------------symbol------------------------------------------------
        try:
            stock_symbol.append(web_data.find("span", {'class':['text-light']}).text)
        except:
            stock_symbol.append('N/A')
        #------------------------------------------------name-------------------------------------------------
        try:
            stock_name.append(web_data.find("h1", {'class':'stock-name'}).text)
        except :
            stock_name.append('N/A')
        #----------------------------------------------industry-----------------------------------------------        
        try:
            if(len(icr[0].text)>2):
                stock_industry.append(icr[0].text)
            else:
                stock_industry.append("N/A")
        except:
            stock_industry.append("N/A")
        #---------------------------------------------market cap----------------------------------------------
        if('Smallcap' in string):
            stock_market_cap.append('Smallcap')
        elif('Midcap' in string):
            stock_market_cap.append('Midcap')
        elif('Largecap' in string):
            stock_market_cap.append('Largecap')
        else:
            stock_market_cap.append('nocap')        
        #---------------------------------------------risk level----------------------------------------------
        if('Low Risk' in string):
            stock_risk_level.append('Low Risk')
        elif('Moderate Risk' in string):
            stock_risk_level.append('Moderate Risk')
        else:
            stock_risk_level.append('High Risk')
        #------------------------------------------stock ticker url-------------------------------------------
        stock_ticker_url.append(url)
        #----------------------------------------------opinion------------------------------------------------
        try:
            score = web_data.find("span", {'class':['percBuyReco-value','jsx-215274026']}).text
            score = score.replace("%", "")
            score = int(score)
            if(score>=65):
                opinion.append("good")
            else:
                opinion.append("bad")
        except:
            opinion.append("bad")
        #-----------------------------------------------------------------------------------------------------
        
    data = {'stock_symbol':stock_symbol,
            'stock_name':stock_name,
            'stock_industry':stock_industry,
            'stock_market_cap':stock_market_cap,
            'stock_risk_level':stock_risk_level,
            'opinion':opinion,
            'stock_ticker_url':stock_ticker_url}
    
    writeCSV(data, 'stockDataset_v1.csv')

if __name__ == "__main__": 
    main()