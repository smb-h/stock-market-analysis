from utils import (ready_symbols, get_csv_rows, ready_id, check_tables, get_data)
import pandas as pd
import pymongo
from pymongo.errors import BulkWriteError
from bson.objectid import ObjectId
from bson.son import SON
from bson.code import Code
import datetime, time
import pprint
import re
import json


start = time.time()
# Days
days = int(input("Enter the number of desired past days for retrieving data: "))
# Symbols
symbols = ["43362635835198978", "778253364357513", "20865316761157979"]
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

# Transactions Colletion
coll_transactions = db.trading_days

# Bestlimitdata Collection, shows if the transaction is about buying or selling
coll_bestlimitdata = db.bestlimitdata

# Closingpricedata Collection, shows the general informations for each symbol from the first transcation to last per day
coll_closingpricedata = db.closingpricedata
coll_intradaypricedata = db.intradaypricedata
coll_intratradedata = db.coll_intratradedata

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

# coll_transactions.drop()

for i in symbols:
    inst = inst_calendar + i
    raw_rows = get_csv_rows(inst, 'InstCalendar.csv')
    reformatted_rows = ready_id(raw_rows, i)

    # rows are reversed in order to add rows from the biggest date to the latest saved date in combinition with else*.
    for row in reformatted_rows[ : :-1]:
        gregorian_date  = row[2]
        gregorian_date = gregorian_date[:4] + "-" + gregorian_date[4:6] + "-" + gregorian_date[6:]
        new_id_trans = coll_transactions.count_documents({}) + 1

        data = {
            '_id': new_id_trans, 
            'symbol_code': row[0],
            'jalali_date': row[1],
            'gregorian_date': gregorian_date,
            'last_price': row[3],
            'trans_turnovers': row[4],
            'is_retrieved': row[5],
        }
        query = {'symbol_code': row[0]}
        result = list(coll_transactions.find(query).sort("_id", -1)) #descending

        # if the transaction collection is not empty
        if (len(result) > 0):    
            last_saved_transaction = result[0]
            current_date = last_saved_transaction.get("gregorian_date", False)
            last_saved_transaction_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
            current_item_date = datetime.datetime.strptime(gregorian_date, "%Y-%m-%d").date()

            # add data based on date if its newer than last saved record
            if (last_saved_transaction_date < current_item_date):
                rs = coll_transactions.insert_one(data)

            # *else mentioned in the top, for ending the loop after reaching the first date which is smaller than the latest saved date.
            else:
                break

        # if symbol data wasnt in db
        else:
            rs = coll_transactions.insert_one(data)


for i in symbols:
    query = {'symbol_code': i}
    result = list(coll_transactions.find(query, {"_id": 0, "symbol_code": 1, "gregorian_date": 1, "is_retrieved": 1 }).sort("_id", -1))

    for item in result[:days]:

        symbol_code = item.get("symbol_code")
        gregorian_date = item.get("gregorian_date").replace("-", "")
        is_retrieved = item.get("is_retrieved")
        soup = get_data('i=' + symbol_code + '&d=' + gregorian_date)

        # gregorian_date with dash
        gregorian_date_ = item.get("gregorian_date")


       
        if (is_retrieved ==  0):
        
            # for bestlimitdata collection
            # this collection holds the informations that shows if a transaction type is buying or selling
            # this table indicates صف
            best_limit_data_tags = re.findall(r'BestLimitData=(.+]);', soup)
            best_limit_data_rows = eval(best_limit_data_tags[0])
            new_id_best = coll_bestlimitdata.count_documents({}) + 1

            # rows for bestlimitdata collection
            for row in best_limit_data_rows:

                row[0] = str(row[0])

                if len(row[0]) < 6:
                    row[0] = row[0][0] + ':' + row[0][2:4] + ':' + row[0][4:]
                else:
                    row[0] = row[0][:2] + ':' + row[0][2:4] + ':' + row[0][4:]

                new_id_best += 1

                data = {
                    '_id': new_id_best,
                    'symbol_code': symbol_code, 
                    'gregorian_data': gregorian_date_,
                    'time': row[0],
                    'row_number': row[1],
                    'buying_num': row[2],
                    'buying_turnover': row[3],
                    'buying_price': row[4],
                    'selling_price': row[5],
                    'selling_turnover': row[6],
                    'selling_num': row[7],
                }

                rs = coll_bestlimitdata.insert_one(data)


            # for closingpricedata collection
            # this collection holds the informations that shows general informations about transactions from the beginning of the 
            # day till end of the day 
            closingPriceData_tag = re.findall(r'ClosingPriceData=(.+);',soup)
            c_rows = eval(closingPriceData_tag[0])
            new_id_close = coll_closingpricedata.count_documents({})

            # rows for closingpricedata collection
            for row in c_rows:

                del row[1]
                del row[-2:]
                jalali_date, time_ = row[0].split(" ")

                new_id_close += 1

                data = {
                    '_id': new_id_close, 
                    'symbol_code': symbol_code,
                    'gregorian_date': gregorian_date_,
                    'jalali_date': jalali_date,
                    'time': time_,
                    'last_trans': row[1],
                    "latest_price": row[2],
                    "initial_price": row[3],
                    "yesterday_price": row[4],
                    "highest_price": row[5],
                    "lowest_price": row[6],
                    "trans_num": row[7],
                    "trans_turnovers": row[8],
                    "trans_values": row[9],
                }

                rs = coll_closingpricedata.insert_one(data)


            # for intradaypricedata collection
            # this collection holds information that are stored in a box plot in the crawled website
            intraDayPriceData_tag = re.findall(r'IntraDayPriceData=(.+);',soup)
            intraday_rows = eval(intraDayPriceData_tag[0])
            new_id_intraday = coll_intradaypricedata.count_documents({})

            # rows for intradaypricedata collection
            for row in intraday_rows:
                
                new_id_intraday += 1

                data = {
                    '_id': new_id_intraday, 
                    'symbol_code': symbol_code,
                    'gregorian_date': gregorian_date_,
                    'jalali_date': jalali_date,
                    'time': row[0],
                    'initial_price': row[1],
                    'lowest_price': row[2],
                    'highest_price': row[3],
                    'latest_price': row[4],
                    'turnover': row[5],
                }

                rs = coll_intradaypricedata.insert_one(data)

        
            # for intratradedata collection
            # this collection holds information in the transactions list 
            intraTradeData_tag = re.findall(r'IntraTradeData=(.+);',soup)
            intratrade_rows = eval(intraTradeData_tag[0])
            new_id_intratrade = coll_intratradedata.count_documents({})

            for row in intratrade_rows:
                
                row = row[:-1]
                new_id_intratrade += 1

                data = {
                    '_id': new_id_intratrade, 
                    'symbol_code': symbol_code,
                    'gregorian_date': gregorian_date_,
                    'trans_num': row[0],
                    'time': row[1],
                    'turnovers': row[2],
                    'price': row[3],
                }

                rs = coll_intratradedata.insert_one(data)

        
            # for updating transaction flag
            query = {"symbol_code": symbol_code, "gregorian_date": gregorian_date_}
            new_values = { 
                "$set": {
                    'is_retrieved': 1,
                }
            }           
            modified = coll_transactions.update_one(query, new_values)


# write database as json 
colls_list = [
    coll_symbols,
    coll_transactions,
    coll_bestlimitdata, 
    coll_closingpricedata, 
    coll_intradaypricedata, 
    coll_intratradedata,
]

for collection in colls_list:
    cursor = collection.find({}, {"_id":0})
    file = open("{}.json".format(collection.name), "w")
    file.write('[')
    for document in cursor:
        file.write(json.dumps(document, sort_keys=True, indent=4))
        file.write(',')
    file.write(']')

end = time.time()

print("time elapsed:", end-start)
