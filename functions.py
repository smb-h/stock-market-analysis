from peewee import *
from bs4 import BeautifulSoup
import os,requests,re


def ready_to_insert(row):
    splitted_row = row.split(',')
    if len(splitted_row) == 8:
        for i in range(15):
            splitted_row.append('')
    return splitted_row

def ready_signs(rows):
    ''' parameters = rows that are gotten from csv file as list
        returns = a list of rows that are ready to be saved '''
    splitted_row = list()
    for items in rows:
        for row in items:
            splitted_row.append(ready_to_insert(row))
    return splitted_row

def get_csv(url,name):
    ''' parameters = url of the csv file to download
        returns = a list of csv file rows '''
    rows = list()
    try:
        r = requests.get(url)
        pwd = os.getcwd()
        with open (os.path.join(pwd , name), 'wb') as file:
            file.write(r.content)
    except:
        if (not os. path. isfile(name)):
            print("something went wrong,couldn't download the file...")
    finally:
        if name == 'MarketWatchInit.csv':
            with open(name) as handle:
                info = handle.read()
            infos = info.split('@')
            for item in infos[2:-1]:
                rows.append(item.split(';'))
            return rows
        else:
            with open ('InstCalendar.csv') as handle:
                file = handle.read()
            rows = file.split(';')
            return rows
            
def ready_id(rows,i):
    ''' parameters = a list of rows gotten from csv file, i as string
        returns = a list of rows that are ready to be inserted to db i_d table '''
    new_rows = list()
    for row in rows:
        items = row.split(',')
        row = (i,) + tuple(items) + (0,)
        if len(row) == 6:
            new_rows.append(row)
    return new_rows            

def check_tables(db,table_name):
    ''' parameters = db connection object, table name as string
        returns = True if table doesnt exist in db '''
    tables = list(db.get_tables())
    if table_name not in tables:
        return True
    else:
        return False
    
def get_data(id):
    ''' parameters = i=izincode&d=date as string
        returns = cleaned string of source code '''
    url = 'http://cdn.tsetmc.com/Loader.aspx?ParTree=15131P&' + id
    page = requests.get(url)
    soup = str(BeautifulSoup(page.text, 'html.parser'))
    return soup

