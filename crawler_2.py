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
        'symbol': [header_name[0]],
        'izin_code': [header_name[1]],
        'brief_name': [header_name[2]],
        'complete_name': [header_name[3]],
        'col5': [header_name[4]],
        'initial': [header_name[5]],
        'latest': [header_name[6]],
        'last_trans': [header_name[7]],
        'trans_num': [header_name[8]],
        'trans_turnovers': [header_name[9]],
        'trans_values': [header_name[10]],
        'lowest': [header_name[11]],
        'highest': [header_name[12]],
        'yesterday': [header_name[13]],
        'Eps': [header_name[14]],
        'basis_turnovers': [header_name[15]],
        'col17': [header_name[16]],
        'col18': [header_name[17]],
        'gp_code': [header_name[18]],
        'allowed_highestprice': [header_name[19]],
        'allowed_lowestprice': [header_name[20]],
        'all_trans_nums': [header_name[21]],
        'col23': [header_name[22]],
    }

    df = pd.DataFrame(data, columns=[
            'symbol', 'izin_code', 'brief_name', 'complete_name', 'col5',
            'initial', 'latest', 'last_trans', 'trans_num', 'trans_turnovers', 
            'trans_values', 'lowest', 'highest', 'yesterday', 'Eps', 'basis_turnovers',
            'col17', 'col18', 'gp_code', 'allowed_highestprice', 'allowed_lowestprice',
            'all_trans_nums', 'col23'], index=[0])

    df.to_csv('symbols.csv',mode="a", index=True, header=True)
    

    for item in splitted[1:]:
       
        data = { 
            'symbol': [item[0]],
            'izin_code': [item[1]],
            'brief_name': [item[2]],
            'complete_name': [item[3]],
            'col5': [item[4]],
            'initial': [item[5]],
            'latest': [item[6]],
            'last_trans': [item[7]],
            'trans_num': [item[8]],
            'trans_turnovers': [item[9]],
            'trans_values': [item[10]],
            'lowest': [item[11]],
            'highest': [item[12]],
            'yesterday': [item[13]],
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
                'symbol', 'izin_code', 'brief_name', 'complete_name', 'col5',
                'initial', 'latest', 'last_trans', 'trans_num', 'trans_turnovers', 
                'trans_values', 'lowest', 'highest', 'yesterday', 'Eps', 'basis_turnovers',
                'col17', 'col18', 'gp_code', 'allowed_highestprice', 'allowed_lowestprice',
                'all_trans_nums', 'col23'], index=[splitted.index(item)])


        df.to_csv('symbols.csv',mode="a", index = True, header=False)
    