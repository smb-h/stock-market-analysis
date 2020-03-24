from peewee import *
from functions import *


db = SqliteDatabase('stocks.db')
class BaseModel(Model): 
    class Meta:
        database = db

class plotting(BaseModel):
    i = CharField()
    m_date = CharField()
    opening_price = FloatField()
    closing_price = FloatField()

class Signs(BaseModel):
    i = CharField()
    izin_code = CharField()
    brief_name = CharField()
    complete_name = CharField()
    col5 = CharField()
    initial = CharField()
    latest = CharField()
    last_trans = CharField()
    trans_num = CharField()
    trans_turnovers = CharField()
    trans_values = CharField()
    lowest = CharField()
    highest = CharField()
    yesterday = CharField()
    Eps = CharField()
    basis_turnovers = CharField()
    col17 = CharField()
    col18 = CharField()
    gp_code = CharField()
    allowed_hp = CharField()
    allowed_lp = CharField()
    all_trans_nums = CharField()
    col23 = CharField()

class i_d(BaseModel):
    i = CharField()
    s_date = DateField()
    m_date = CharField()
    last_price = CharField()
    trans_turnovers = CharField()
    flag = CharField()

class BestLimitData(BaseModel):
    i = CharField()
    m_date = CharField()
    time  = TimeField()
    row = CharField()
    buying_num = CharField()
    buying_turnover = CharField()
    buying_price = CharField()
    selling_price = CharField()
    selling_turnover = CharField()
    people_num = CharField()

class ClosingPriceData(BaseModel):
        i = CharField()
        m_date = CharField()
        date = DateTimeField()
        last_trans = CharField() 
        latest_price = CharField()
        initial_price = CharField()
        yesterday_price = CharField()
        highest_price = CharField()
        lowest_price = CharField()
        trans_num = CharField()
        trans_turnovers = CharField()
        trans_values = CharField()

class IntraTradeData(BaseModel):
    i = CharField()
    m_date = CharField()
    trans_num = CharField()
    time = TimeField() 
    turnover = CharField()
    price = CharField()

class IntraDayPriceData(BaseModel):
    number = IntegerField(primary_key=True)
    i = CharField()
    m_date = CharField()
    time = TimeField() 
    initial_price = CharField() 
    lowest_price = CharField()
    highest_price = CharField()
    latest_price = CharField()
    Turnover = CharField()

db.connect()
count = 0
num = int(input("Enter the number of desired past days for retrieving data:"))
the_4_i = ["43362635835198978","778253364357513","20865316761157979","44891482026867833"]
market = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0'
instcalendar = 'http://www.tsetmc.com/tsev2/data/InstCalendar.aspx?i='
m_rows = get_csv(market,'MarketWatchInit.csv')
splitted = ready_signs(m_rows)

# checking if signs table exists, if not it will be created
if check_tables(db,'signs'):
    db.create_tables([Signs])
    for item in splitted:
        Signs.create(i = item[0],izin_code = item[1],brief_name = item [2],complete_name = item[3],col5 = item[4],\
            initial = item[5],latest = item[6],last_trans = item[7],trans_num = item[8],trans_turnovers = item[9],\
            trans_values = item[10],lowest = item[11],highest = item[12],yesterday = item[13],Eps = item[14],\
            basis_turnovers = item[15],col17 = item[16],col18 = item[17],gp_code = item[18],allowed_hp = item[19],\
            allowed_lp = item[20],all_trans_nums = item[21],col23 = item[22])
else:
    rows = Signs.select(Signs.id)
    for item,row in zip(splitted,rows):
        Signs.update(i = item[0],izin_code = item[1],brief_name = item [2],complete_name = item[3],col5 = item[4],\
            initial = item[5],latest = item[6],last_trans = item[7],trans_num = item[8],trans_turnovers = item[9],\
            trans_values = item[10],lowest = item[11],highest = item[12],yesterday = item[13],Eps = item[14],\
            basis_turnovers = item[15],col17 = item[16],col18 = item[17],gp_code = item[18],allowed_hp = item[19],\
            allowed_lp = item[20],all_trans_nums = item[21],col23 = item[22]).where(Signs.id == row.id)

if check_tables(db,'i_d'):
    db.create_tables([i_d])
    for i in the_4_i:
        inst = instcalendar + i
        i_rows = get_csv(inst,'InstCalendar.csv')
        ready_rows = ready_id(i_rows,i)
        for row in ready_rows:
            i_d.create(i = row[0],s_date = row[1],m_date = row[2],last_price = row[3],trans_turnovers = row[4],\
            flag = row[5])
else:
    rows = i_d.select(i_d.id)
    for i in the_4_i:
        inst = instcalendar + i
        i_rows = get_csv(inst,'InstCalendar.csv')
        ready_rows = ready_id(i_rows,i)
        for ready_row,row in zip(ready_rows,rows):
            i_d.update(i = ready_row[0],s_date = ready_row[1],m_date = ready_row[2],last_price = ready_row[3],\
            trans_turnovers = ready_row[4],flag = ready_row[5]).where(i_d.id == row.id)

for i in the_4_i:
    i_date = i_d.select(i_d.i,i_d.m_date,i_d.flag).where(i_d.i == i)
    
    for i_and_date in i_date[-num : ]:      # loop through desired days
        print("Retrieving data...")
        working_i = i_and_date.i
        date = i_and_date.m_date
        flag = i_and_date.flag
        soup = get_data('i=' + working_i + '&d=' + date)    # getting source code
        if flag == "0":
            print("Saving data...")
            # getting tags if weren't gotten before
            if check_tables(db,"ClosingPriceData"):
                db.create_tables([ClosingPriceData])
            ClosingPriceData_tag = re.findall(r'ClosingPriceData=(.+);',soup)
            C_rows = eval(ClosingPriceData_tag[0])
            db.create_tables([ClosingPriceData])
            for row in C_rows:
                del row[1]
                del row[-2:]
                ClosingPriceData.create(i = working_i,m_date = date,date = row[0],last_trans = row[1],\
                latest_price = row[2],initial_price = row[3],yesterday_price = row[4],highest_price = row[5],\
                lowest_price = row[6],trans_num = row[7],trans_turnovers = row[8],trans_values = row[9])

            if check_tables(db,"IntraDayPriceData"):
                db.create_tables([IntraDayPriceData])
            else:
                num = IntraDayPriceData.select(IntraDayPriceData.max(IntraDayPriceData.number))
                count = num[0].number + 1
                print(count)
            IntraDayPriceData_tag = re.findall(r'IntraDayPriceData=(.+);',soup)
            Intraday_rows = eval(IntraDayPriceData_tag[0])
            for row in Intraday_rows:
                IntraDayPriceData.create(number = count,i = working_i,m_date = date,time = row[0],initial_price = row[1],\
                lowest_price = row[2],highest_price = row[3],latest_price = row[4],Turnover = row[5])
                count += 1

            if check_tables(db,"IntraTradeData"):
                db.create_tables([IntraTradeData])
            IntraTradeData_tag = re.findall(r'IntraTradeData=(.+);',soup)
            Intratrade_rows = eval(IntraTradeData_tag[0])
            for row in Intratrade_rows:
                row = row[:-1]
                IntraTradeData.create(i = working_i,m_date = date,trans_num = row[0],time = row[1],\
                turnover = row[2],price = row[3])

            if check_tables(db,"BestLimitData"):
                db.create_tables([BestLimitData])
            BestLimitData_tag = re.findall(r'BestLimitData=(.+]);',soup)
            Best_rows = eval(BestLimitData_tag[0])
            for row in Best_rows:
                row[0] = str(row[0])
                if len(row[0]) < 6:
                    row[0] = row[0][0] + ':' + row[0][2:4] + ':' + row[0][4:]
                else:
                    row[0] = row[0][:2] + ':' + row[0][2:4] + ':' + row[0][4:]
                    BestLimitData.create(i = working_i,m_date = date,time = row[0],row = row[1],\
                    buying_num = row[2],buying_turnover = row[3],buying_price = row[4],selling_price = row[5],\
                    selling_turnover = row[6],people_num = row[7])
            i_d.update(flag = "1" ).where((i_d.i == working_i) & (i_d.m_date == date)).execute()   

for i in the_4_i:
    if check_tables(db,"plotting"):
        db.create_tables([plotting])
    i_date = IntraDayPriceData.select(IntraDayPriceData.m_date).where(IntraDayPriceData.i == i)
    days = {row.m_date for row in i_date}
    for day in days:
        opening = IntraDayPriceData.select(IntraDayPriceData.initial_price).where(IntraDayPriceData.i == i, \
        IntraDayPriceData.m_date == day).limit(1)
        print([item.initial_price for item in opening])
        closing = IntraDayPriceData.select(IntraDayPriceData.latest_price).where(IntraDayPriceData.i == i,\
        IntraDayPriceData.m_date == day).order_by(IntraDayPriceData.number.desc()).limit(1)
        plotting.create(i = i,m_date = day,opening_price = opening[0].initial_price,closing_price = closing[0].latest_price)

print('Done =)')
