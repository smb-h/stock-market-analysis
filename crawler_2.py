from functions import *
import pandas as pd


num = int(input("Enter the number of desired past days for retrieving data:"))
the_4_i = ["43362635835198978","778253364357513","20865316761157979","44891482026867833"]
#signs csv
market = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0' 
instcalendar = 'http://www.tsetmc.com/tsev2/data/InstCalendar.aspx?i='
m_rows = get_csv(market,'MarketWatchInit.csv')
splitted = ready_signs(m_rows)

with open("symbols.csv",'w') as file:

    header_name = splitted[0]

    data = { 
        'symbol': [header_name[0]], # نماد 
        'izin_code': [header_name[1]], # کد آیذین
        'brief_name': [header_name[2]], # نام کوتاه
        'complete_name': [header_name[3]], # نام کامل
        'latest_trans_time': [header_name[4]], # زمان آخرین معامله
        'first_price': [header_name[5]], # اولین قیمت
        'latest_price': [header_name[6]], # آخرین قیمت
        'last_trans': [header_name[7]], # آخرین معامله
        'trans_num': [header_name[8]], # تعداد معاملات
        'trans_turnovers': [header_name[9]], #حجم معاملات
        'trans_value': [header_name[10]], # ارزش معاملات
        'lowest': [header_name[11]], # بازه‌ی روز
        'highest': [header_name[12]], # بازه‌ی روز
        'yesterday_price': [header_name[13]], # قیمت دیروز
        'Eps': [header_name[14]], # (درآمد هر سهم (حاصل تقسیم کل درآمد بر تعداد سهم
        'basis_turnovers': [header_name[15]], # حجم مبنا
        'col17': [header_name[16]],
        'col18': [header_name[17]],
        'gp_code': [header_name[18]],
        'allowed_highestprice': [header_name[19]], # بالاترین قیمت مجاز
        'allowed_lowestprice': [header_name[20]], # پائین ترین قیمت مجاز
        'all_trans_nums': [header_name[21]], # تعداد سهام
        'col23': [header_name[22]],
    }

    df = pd.DataFrame(data, columns=[
            'symbol', 'izin_code', 'brief_name', 'complete_name', 'latest_trans_time',
            'first_price', 'latest_price', 'last_trans', 'trans_num', 'trans_turnovers', 
            'trans_value', 'lowest', 'highest', 'yesterday_price', 'Eps', 'basis_turnovers',
            'col17', 'col18', 'gp_code', 'allowed_highestprice', 'allowed_lowestprice',
            'all_trans_nums', 'col23'], index=[0])

    df.to_csv('symbols.csv',mode="a", index=True, header=True)
    

    for item in splitted[1:]:
       
        data = { 
            'symbol': [item[0]],
            'izin_code': [item[1]],
            'brief_name': [item[2]],
            'complete_name': [item[3]],
            'latest_trans_time': [item[4]],
            'first_price': [item[5]],
            'latest_price': [item[6]],
            'last_trans': [item[7]],
            'trans_num': [item[8]],
            'trans_turnovers': [item[9]],
            'trans_value': [item[10]],
            'lowest': [item[11]],
            'highest': [item[12]],
            'yesterday_price': [item[13]],
            'Eps': [item[14]],
            'basis_turnovers': [item[15]],
            'col17': [item[16]],
            'col18': [item[17]],
            'gp_code': [item[18]],
            'allowed_highestprice': [item[19]],
            'allowed_lowestprice': [item[20]],
            'all_trans_nums': [item[21]],
            'col23': [item[22]],
        }
    
        df = pd.DataFrame(data, columns=[
                'symbol', 'izin_code', 'brief_name', 'complete_name', 'latest_trans_time',
                'first_price', 'latest_price', 'last_trans', 'trans_num', 'trans_turnovers', 
                'trans_value', 'lowest', 'highest', 'yesterday_price', 'Eps', 'basis_turnovers',
                'col17', 'col18', 'gp_code', 'allowed_highestprice', 'allowed_lowestprice',
                'all_trans_nums', 'col23'], index=[splitted.index(item)])


        df.to_csv('symbols.csv',mode="a", index = True, header=False)
    

with open("symbols-date.csv") as file:

     data = { 
        'symbol': [header_name[0]], # نماد 
        'jalali_date': [header_name[1]], # کد آیذین
        'gregorian_date': [header_name[2]], # نام کوتاه
        'complete_name': [header_name[3]], # نام کامل
        'latest_trans_time': [header_name[4]], # زمان آخرین معامله
        'first_price': [header_name[5]], # اولین قیمت
        'latest_price': [header_name[6]], # آخرین قیمت
        'last_trans': [header_name[7]], # آخرین معامله
        'trans_num': [header_name[8]], # تعداد معاملات
        'trans_turnovers': [header_name[9]], #حجم معاملات
        'trans_value': [header_name[10]], # ارزش معاملات
        'lowest': [header_name[11]], # بازه‌ی روز
        'highest': [header_name[12]], # بازه‌ی روز
        'yesterday_price': [header_name[13]], # قیمت دیروز
        'Eps': [header_name[14]], # (درآمد هر سهم (حاصل تقسیم کل درآمد بر تعداد سهم
        'basis_turnovers': [header_name[15]], # حجم مبنا
        'col17': [header_name[16]],
        'col18': [header_name[17]],
        'gp_code': [header_name[18]],
        'allowed_highestprice': [header_name[19]], # بالاترین قیمت مجاز
        'allowed_lowestprice': [header_name[20]], # پائین ترین قیمت مجاز
        'all_trans_nums': [header_name[21]], # تعداد سهام
        'col23': [header_name[22]],
    }



