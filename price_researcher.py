from pymongo import MongoClient  # 需要pip安装
import pandas as pd
import datetime
from WechatPoster import WeChat as wx

client = MongoClient('magicapple.cn',8088)
mongo_auth = client.admin
mongo_auth.authenticate('reporter', 'gjysz0816!')
collection = client['commodity_price']
# print(collection.list_collection_names(session=None))

commodity_names=collection.list_collection_names(session=None)
# today=datetime.datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
today=datetime.datetime(2020,12,5)
time_num = 5
days_before_today = (datetime.datetime.today()-datetime.timedelta(days=time_num)).replace(hour=0,minute=0,second=0,microsecond=0)
winxin_text:str=""
# text=[]
for i in commodity_names[:50]:
    newest_record=list(collection[i].find({'datetime':today}))
    days_before_record = list(collection[i].find({'datetime':days_before_today}))
# newest = list(collection.find({'datetime':today}))
    if len(newest_record) == 1:
        newest_price = newest_record[0]['price']
        if type(newest_price) is not float:
            print("error1")
    else:
        print("error2")
    if len(days_before_record) == 1:
        days_before_price = days_before_record[0]['price']
    else:
        print('error3')
    change = round(((newest_price/days_before_price)-1),2)
    # print(change,i)
    percentage = 0.05
    if change >= percentage or change <= -1*percentage:
        name = i
        # print(name)
        # text = (str(today.date()) + ' '+name +'价格为'+ str(newest_price) +'较'+ str(time_num) +'天前'+ str(days_before_today.date())+
        #         '的价格' + str(days_before_price) + '变动为' + str(change) +'.' )
        tmp= (str(today.date()) + ' ' + name + '价格为' + str(newest_price) + '较' + str(time_num) + '天前' + str(
            days_before_today.date()) +
                '的价格' + str(days_before_price) + '变动为' + str(change) + '.\n')
        # text.append(tmp)
        winxin_text+=tmp
# winxin_text = winxin_text.join(text)
# print(winxin_text)
if __name__ == '__main__':
    wx = wx()
    # print(type(winxin_text))
    wx.send_data(winxin_text)
    print('Done')
