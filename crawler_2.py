from utils import (ready_symbols, get_csv_rows, ready_id, check_tables, get_data)
import pandas as pd
import pymongo 
from pymongo.errors import BulkWriteError
import pprint
from bson.objectid import ObjectId
from bson.son import SON
from bson.code import Code
import datetime


# Days
days = int(input("Enter the number of desired past days for retrieving data: "))
# Symbols
symbols = ["43362635835198978","778253364357513","20865316761157979","44891482026867833"]
# Symbols csv
market = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0' 
# History
inst_calendar = 'http://www.tsetmc.com/tsev2/data/InstCalendar.aspx?i='

market_rows = get_csv_rows(market, 'MarketWatchInit.csv')
symbols_reformated = ready_symbols(market_rows)

# DB client
client = pymongo.MongoClient('localhost', 27017)
# DB
db = client.stock_market

# Symbols Collection
coll_symbols = db.symbols
# Indexing
result = coll_symbols.create_index([('symbol_code', pymongo.ASCENDING)], unique=True)

'''
    کد نماد
    symbol_code
    کد آیذین
    izin_code
    نام کوتاه
    brief_name
    نام کامل
    complete_name
    زمان آخرین معامله
    latest_trans_time
    اولین قیمت
    first_price
    آخرین قیمت
    latest_price
    آخرین معامله
    last_trans
    تعداد معاملات
    trans_num
    حجم معاملات
    trans_turnovers
    ارزش معاملات
    trans_value
    بازه‌ی روز
    lowest
    بازه‌ی روز
    highest
    قیمت دیروز
    yesterday_price
    (درآمد هر سهم (حاصل تقسیم کل درآمد بر تعداد سهم
    Eps
    حجم مبنا
    basis_turnovers
    col17
    col18
    gp_code
    بالاترین قیمت مجاز
    allowed_highestprice
    پائین ترین قیمت مجاز
    allowed_lowestprice
    تعداد سهام
    all_trans_nums
    col23
'''

# insert data into collection
for i in range(len(symbols_reformated)):
    # Update if exists
    symbol_code = symbols_reformated[i][0]
    # print(symbols_reformated[i][1])
    query = { "symbol_code": symbol_code }
    new_values = { "$set": {
        'izin_code': symbols_reformated[i][1],
        'brief_name': symbols_reformated[i][2],
        'complete_name': symbols_reformated[i][3],
        'latest_trans_time': symbols_reformated[i][4],
        'first_price': symbols_reformated[i][5],
        'latest_price': symbols_reformated[i][6],
        'last_trans': symbols_reformated[i][7],
        'trans_num': symbols_reformated[i][8],
        'trans_turnovers': symbols_reformated[i][9],
        'trans_value': symbols_reformated[i][10],
        'lowest': symbols_reformated[i][11],
        'highest': symbols_reformated[i][12],
        'yesterday_price': symbols_reformated[i][13],
        'Eps': symbols_reformated[i][14],
        'basis_turnovers': symbols_reformated[i][15],
        'col17': symbols_reformated[i][16],
        'col18': symbols_reformated[i][17],
        'gp_code': symbols_reformated[i][18],
        'allowed_highestprice': symbols_reformated[i][19],
        'allowed_lowestprice': symbols_reformated[i][20],
        'all_trans_nums': symbols_reformated[i][21],
        'col23': symbols_reformated[i][22],
    }}
    modified = coll_symbols.update_one(query, new_values)

    # Insert
    if modified.matched_count == 0:
        data = {
            'symbol_code': symbols_reformated[i][0],
            'izin_code': symbols_reformated[i][1],
            'brief_name': symbols_reformated[i][2],
            'complete_name': symbols_reformated[i][3],
            'latest_trans_time': symbols_reformated[i][4],
            'first_price': symbols_reformated[i][5],
            'latest_price': symbols_reformated[i][6],
            'last_trans': symbols_reformated[i][7],
            'trans_num': symbols_reformated[i][8],
            'trans_turnovers': symbols_reformated[i][9],
            'trans_value': symbols_reformated[i][10],
            'lowest': symbols_reformated[i][11],
            'highest': symbols_reformated[i][12],
            'yesterday_price': symbols_reformated[i][13],
            'Eps': symbols_reformated[i][14],
            'basis_turnovers': symbols_reformated[i][15],
            'col17': symbols_reformated[i][16],
            'col18': symbols_reformated[i][17],
            'gp_code': symbols_reformated[i][18],
            'allowed_highestprice': symbols_reformated[i][19],
            'allowed_lowestprice': symbols_reformated[i][20],
            'all_trans_nums': symbols_reformated[i][21],
            'col23': symbols_reformated[i][22],
        }
        rs = coll_symbols.insert_one(data)


# Print collection as dataframe
# coll_symbols_cursor = coll_symbols.find()
# df_coll_symbols =  pd.DataFrame(list(coll_symbols_cursor))
# print(coll_symbols.count_documents({}))
# print(df_coll_symbols)


# with open("symbols-date.csv") as file:
        # header_name = symbols_reformated[0]
#      data = { 
#         'symbol': [header_name[0]], # نماد 
#         'jalali_date': [header_name[1]], # کد آیذین
#         'gregorian_date': [header_name[2]], # نام کوتاه
#         'complete_name': [header_name[3]], # نام کامل
#         'latest_trans_time': [header_name[4]], # زمان آخرین معامله
#         'first_price': [header_name[5]], # اولین قیمت
#         'latest_price': [header_name[6]], # آخرین قیمت
#         'last_trans': [header_name[7]], # آخرین معامله
#         'trans_num': [header_name[8]], # تعداد معاملات
#         'trans_turnovers': [header_name[9]], #حجم معاملات
#         'trans_value': [header_name[10]], # ارزش معاملات
#         'lowest': [header_name[11]], # بازه‌ی روز
#         'highest': [header_name[12]], # بازه‌ی روز
#         'yesterday_price': [header_name[13]], # قیمت دیروز
#         'Eps': [header_name[14]], # (درآمد هر سهم (حاصل تقسیم کل درآمد بر تعداد سهم
#         'basis_turnovers': [header_name[15]], # حجم مبنا
#         'col17': [header_name[16]],
#         'col18': [header_name[17]],
#         'gp_code': [header_name[18]],
#         'allowed_highestprice': [header_name[19]], # بالاترین قیمت مجاز
#         'allowed_lowestprice': [header_name[20]], # پائین ترین قیمت مجاز
#         'all_trans_nums': [header_name[21]], # تعداد سهام
#         'col23': [header_name[22]],
#     }



