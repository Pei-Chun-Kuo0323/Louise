"""
print('Hello World')
https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M



url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

print(type(response)) # <class 'requests.models.Response'>
res = response.json()
print(type(res))      # <class 'list'>

print(res[0])



def app():
	st.header('特色書店地圖')
	st.metric('Total bookstore', 118)
	county = st.selectbox('請選擇縣市', ['A', 'B', 'C'])
	district = st.multiselect('請選擇區域', ['a', 'b', 'c', 'd'])
"""
import requests
import streamlit as st

def getAllBookstore():
    url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M' # 在這裡輸入目標 url
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res=response.json()# 將 response 轉換成 json 格式
    return res# 回傳值

def getCountyOption(items):
    optionList=[]# 創建一個空的 List 並命名為 optionList
    for item in items:
        name=item['cityName'][0:3]
        # 把 cityname 欄位中的縣市名稱擷取出來 並指定給變數 name
        # hint: 想辦法處理 item['cityName'] 的內容

        # 如果 name 不在 optionList 之中，便把它放入 optionList
        if name in optionList:
            continue
        else:
            optionList.append(name)
        # hint: 使用 if-else 來進行判斷 / 用 append 把東西放入 optionList
    return optionList#注意位置縮排

def getDistrictOption(items, target) ->list:
    optionList = []
    for item in items:
        name = item['cityName']
        if target not in name: continue
        name.strip()
        district = name[5:]
        if len(district) == 0: continue
        if district not in optionList:
            optionList.append(district)
    return optionList


def getSpecificBookstore(items, county):
    specificBookstoreList = []
    for item in items:
        name=item['cityName']
        if county in item['cityName']:
            specificBookstoreList.append(item)
        else:
            continue
	# 如果 name 不是我們選取的 county 則跳過
	# hint: 用 if-else 判斷並用 continue 跳過
    return specificBookstoreList

def getBookstoreInfo(items):
    expanderList = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])# 用 st.write 呈現書店的 Introduction
        expander.subheader('Address')
        expander.write(item['address'])# 用 st.write 呈現書店的 Address
        expander.subheader('Open Time')
        expander.write(item['openTime'])# 用 st.write 呈現書店的 Open Time
        expander.subheader('Email')
        expander.write(item['email']) # 用 st.write 呈現書店的 Email
        # 將該 expander 放到 expanderList 中
    return expanderList


def app():
    bookstorelist = getAllBookstore()# 呼叫 getAllBookstore 函式並將其賦值給變數 bookstoreList
    countyOption=getCountyOption(bookstorelist)# 呼叫 getCountyOption 並將回傳值賦值給變數 countyOption
    st.header('特色書店地圖')
    st.metric('Total bookstore', len(bookstorelist)) # 將 118 替換成書店的數量
    county = st.selectbox('請選擇縣市',countyOption)# .selectbox表示單選拉條
    specificBookstore=getSpecificBookstore(bookstorelist,county)
    districtOption = getDistrictOption(bookstorelist, county)
    district = st.multiselect('請選擇區域', districtOption)#.multiselect表示多選拉條
    getBookstoreInfo(specificBookstore)
    num = len(specificBookstore)
    st.write(f'總共有{num}間書店')



if __name__ == '__main__':
    app()