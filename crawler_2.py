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
symbols = ["43362635835198978","778253364357513","20865316761157979"]
# Symbols csv
market = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0' 
# History
inst_calendar = 'http://www.tsetmc.com/tsev2/data/InstCalendar.aspx?i='

market_rows = get_csv_rows(market, 'MarketWatchInit.csv')
symbols_reformatted = ready_symbols(market_rows)

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
for i in range(len(symbols_reformatted)):
    # Update if exists
    symbol_code = symbols_reformatted[i][0]
    # print(symbols_reformatted[i][1])
    query = { "symbol_code": symbol_code }
    new_values = { "$set": {
        'izin_code': symbols_reformatted[i][1],
        'brief_name': symbols_reformatted[i][2],
        'complete_name': symbols_reformatted[i][3],
        'latest_trans_time': symbols_reformatted[i][4],
        'first_price': symbols_reformatted[i][5],
        'latest_price': symbols_reformatted[i][6],
        'last_trans': symbols_reformatted[i][7],
        'trans_num': symbols_reformatted[i][8],
        'trans_turnovers': symbols_reformatted[i][9],
        'trans_value': symbols_reformatted[i][10],
        'lowest': symbols_reformatted[i][11],
        'highest': symbols_reformatted[i][12],
        'yesterday_price': symbols_reformatted[i][13],
        'Eps': symbols_reformatted[i][14],
        'basis_turnovers': symbols_reformatted[i][15],
        'col17': symbols_reformatted[i][16],
        'col18': symbols_reformatted[i][17],
        'gp_code': symbols_reformatted[i][18],
        'allowed_highestprice': symbols_reformatted[i][19],
        'allowed_lowestprice': symbols_reformatted[i][20],
        'all_trans_nums': symbols_reformatted[i][21],
        'col23': symbols_reformatted[i][22],
    }}
    modified = coll_symbols.update_one(query, new_values)

    # Insert
    if modified.matched_count == 0:
        data = {
            'symbol_code': symbols_reformatted[i][0],
            'izin_code': symbols_reformatted[i][1],
            'brief_name': symbols_reformatted[i][2],
            'complete_name': symbols_reformatted[i][3],
            'latest_trans_time': symbols_reformatted[i][4],
            'first_price': symbols_reformatted[i][5],
            'latest_price': symbols_reformatted[i][6],
            'last_trans': symbols_reformatted[i][7],
            'trans_num': symbols_reformatted[i][8],
            'trans_turnovers': symbols_reformatted[i][9],
            'trans_value': symbols_reformatted[i][10],
            'lowest': symbols_reformatted[i][11],
            'highest': symbols_reformatted[i][12],
            'yesterday_price': symbols_reformatted[i][13],
            'Eps': symbols_reformatted[i][14],
            'basis_turnovers': symbols_reformatted[i][15],
            'col17': symbols_reformatted[i][16],
            'col18': symbols_reformatted[i][17],
            'gp_code': symbols_reformatted[i][18],
            'allowed_highestprice': symbols_reformatted[i][19],
            'allowed_lowestprice': symbols_reformatted[i][20],
            'all_trans_nums': symbols_reformatted[i][21],
            'col23': symbols_reformatted[i][22],
        }
        rs = coll_symbols.insert_one(data)


# Print collection as dataframe
# coll_symbols_cursor = coll_symbols.find()
# df_coll_symbols =  pd.DataFrame(list(coll_symbols_cursor))
# print(coll_symbols.count_documents({}))
# print(df_coll_symbols)


'''
    کد نماد
    symbol_code
    تاریخ جلالی
    jalali_date
    تاریخ میلادی
    gregorian_date
    آخرین قیمت
    last_price
    حجم معاملات
    trans_turnovers
    نشان میدهد که اطلاعات برای ۴ جدول دیگر در آن تاریخ خاص گرفته شده است یا خیر
    is_retrieved
'''

# Transactions Colletion
coll_transactions = db.trading_days
# coll_transactions.drop()
transaction_index = 0
for i in symbols:
    inst = inst_calendar + i
    raw_rows = get_csv_rows(inst, 'InstCalendar.csv')
    reformatted_rows = ready_id(raw_rows, i)
    for row in reformatted_rows:
        gregorian_date  = row[2]
        gregorian_date = gregorian_date[:4] + "-" + gregorian_date[4:6] + "-" + gregorian_date[6:]
        data = {
            '_id': transaction_index, 
            'symbol_code': row[0],
            'jalali_date': row[1],
            'gregorian_date': gregorian_date,
            'last_price': row[3],
            'trans_turnovers': row[4],
            'is_retrieved': row[5],
        }
        query = {'symbol_code': row[0]}
        result = list(coll_transactions.find(query).sort("_id", -1)) #descending
        new_id = coll_transactions.count_documents({})
        # check last record of symbol in db
        if len(result) > 0:
            last_saved_transaction = result[0]
            last_saved_transaction_date = datetime.datetime.strptime((last_saved_transaction.get("gregorian_date", False)), "%Y-%m-%d").date()
            current_item_date = datetime.datetime.strptime(gregorian_date, "%Y-%m-%d").date()
            # add data based on date if its newer then last saved record
            if (last_saved_transaction_date < current_item_date) :
                data["_id"] = new_id
                rs = coll_transactions.insert_one(data)
        # if symbol data wasnt in db
        else:
            data["_id"] = new_id
            rs = coll_transactions.insert_one(data)


        transaction_index += 1

# Bestlimitdata Collection
coll_bestlimitdata = db.bestlimitdata


for i in symbols:
    query = {'symbol_code': i}
    result = list(coll_transactions.find(query, {"_id": 0, "symbol_code": 1, "jalali_date": 1, "is_retrieved": 1 }).sort("_id", -1))
    for item in result[:days]:
        print(item)


