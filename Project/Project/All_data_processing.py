import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import math
from random import *
from dateutil.parser import parse
warnings.filterwarnings("ignore")

plt.style.use('ggplot')

start = '20140801'  # '20110101'
end = '20200530'

# 평일 날짜만 추출
dt_index = pd.DataFrame(pd.date_range(start=start, end=end, freq='B')).rename(columns={0: 'date'})

def drop_duplicates(data):
    return data.reset_index().drop_duplicates(['date']).set_index('date')

def processing_potato_price(data):
    # print("======= data processing start ===========")
    # print(data.shape)
    # 중복값 제거
    data = data.drop_duplicates()

    # before, now / string to int
    data['before'] = data['before'].apply(lambda x: int(x.replace(',', '')))
    data['now'] = data['now'].apply(lambda x: int(x.replace(',', '')))

    # name 통합
    data['name'] = data['name'].apply(lambda x: x.replace('감자(수미)', '감자 수미').replace('감자(대지마)', '감자 대지'))

    # 감자 수미 or 감자 대지 선택
    string = '감자 수미'  # 감자 수미 or 감자 대지
    subdata = data[data['name'] == '감자 대지']
    data = data[data['name'] == string]

    # 20110101-20191231 인덱스 설정
    data['date'] = data['date'].apply(lambda x: parse(str(x)))
    data = pd.merge(dt_index, data, how='left', on='date').set_index('date')

    # 원하는 날짜 index와 결합
    subdata['date'] = subdata['date'].apply(lambda x: parse(str(x)))
    subdata = pd.merge(dt_index, subdata, how='left', on='date').set_index('date')

    # name 통일
    data['name'] = string

    # null 값 채우기
    # 1) 0값을 null값으로
    def zero_to_nan(data):
        if math.isnan(data):
            return data
        elif data == 0:
            return np.nan
        else:
            return data

    data['before'] = data['before'].apply(zero_to_nan)
    data['now'] = data['now'].apply(zero_to_nan)

    # 2) now가 null 값일 때 다음날 before값이 존재할 때
    random_value = 10
    data['Fill_value'] = data.shift(-1)['before']
    data['now'] = data[['now', 'Fill_value']].apply(lambda x: x['Fill_value'] if math.isnan(x['now']) else x['now'],
                                                    axis=1)

    # 3) 2014-04-01 ~ 2015-04-40 수미 감자 null 값을 대지 감자 price로 대체
    data['sub_now'] = subdata['now']
    data['tmp_date'] = data.index

    def fill_null_to_sub_now(data):
        if str(data['tmp_date']) > '2014-03-31' and str(data['tmp_date']) <= '2015-04-30':
            return data['sub_now']
        else:
            return data['now']

    data['now'] = data[['now', 'tmp_date', 'sub_now']].apply(fill_null_to_sub_now, axis=1)

    # 4) 이전 날의 값으로 null값 대체
    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    # 불필요한 columns drop
    data.drop(['name', 'before', 'Fill_value', 'sub_now', 'tmp_date'], axis=1, inplace=True)
    data.rename(columns={'now': 'potato'}, inplace=True)
    # print(data.head())
    # print(data.isnull().sum().sum())
    data = drop_duplicates(data)

    print(data.tail(3))
    # print("======= data processing finish ===========")
    print()
    return data

def processing_Exchange_Rate(data):
    # 20110101부터 정렬
    data = data[::-1]
    # format datetime으로 변경
    data['날짜'] = data['날짜'].apply(lambda x: parse(x[:4] + x[6:8] + x[10:12]))
    # 20110101-20191231 인덱스 설정
    data = pd.merge(dt_index, data, how='left', left_on='date', right_on='날짜').set_index('date')
    # print('전처리 전 null 갯수 : {}'.format(data['종가'].isnull().sum()))
    # type 변경 str -> float
    data['종가'] = data['종가'].apply(lambda x: x if x is np.nan else float(x.replace(',', '')))
    data['오픈'] = data['오픈'].apply(lambda x: x if x is np.nan else float(x.replace(',', '')))

    # 주말 Null값 채우기

    # 일요일 : 월요일 오픈 가격으로 대체
    data['Fill_value'] = data.shift(-1)['오픈']
    data['종가'] = data[['종가', 'Fill_value']].apply(lambda x: x['Fill_value'] if math.isnan(x['종가']) else x['종가'], axis=1)
    # print('전처리 후 null 갯수 : {}'.format(data['종가'].isnull().sum()))

    # 토요일 : 금요일 종가 + random value
    random_value = 1
    data['Fill_value'] = data.shift(1)['종가']
    data['종가'] = data[['종가', 'Fill_value']].apply(
        lambda x: x['Fill_value'] + uniform(-random_value, random_value) if math.isnan(x['종가']) else x['종가'], axis=1)

    data.drop(['날짜', '오픈', '고가', '저가', '변동 %', 'Fill_value'], axis=1, inplace=True)

    # print('전처리 후 null 갯수 : {}'.format(data['종가'].isnull().sum()))
    data.rename(columns={'종가': 'Exchange_Rate'}, inplace=True)

    data = data.fillna(method='bfill')

    data = drop_duplicates(data)
    print(data.tail(3))
    print()
    return data

def processing_KOSPI(data):
    # 20110101부터 정렬
    data = data[::-1]

    # format datetime으로 변경
    data['날짜'] = data['날짜'].apply(lambda x: parse(x[:4] + x[6:8] + x[10:12]))

    # 20110101-20191231 인덱스 설정
    data = pd.merge(dt_index, data, how='left', left_on='date', right_on='날짜').set_index('date')
    # type 변경 str -> float
    data['종가'] = data['종가'].apply(lambda x: x if x is np.nan else float(x.replace(',', '')))
    data['오픈'] = data['오픈'].apply(lambda x: x if x is np.nan else float(x.replace(',', '')))

    # 주말 Null값 채우기

    # 일요일 : 월요일 오픈 가격으로 대체
    data['Fill_value'] = data.shift(-1)['오픈']
    data['종가'] = data[['종가', 'Fill_value']].apply(lambda x: x['Fill_value'] if math.isnan(x['종가']) else x['종가'], axis=1)

    random_value = 1
    data['Fill_value'] = data.shift(1)['종가']
    data['종가'] = data[['종가', 'Fill_value']].apply(
        lambda x: x['Fill_value'] + uniform(-random_value, random_value) if math.isnan(x['종가']) else x['종가'], axis=1)

    pd.set_option('display.float_format', '{:.2f}'.format)  # 항상 float 형식으로

    data.drop(['날짜', '오픈', '고가', '저가', '거래량', '변동 %', 'Fill_value'], axis=1, inplace=True)
    data.rename(columns={'종가': 'KOSPI'}, inplace=True)

    data = data.fillna(method='bfill')

    data = drop_duplicates(data)
    print(data.tail(3))
    print()
    return data

def load_crops_data(sql):
    # print("======= data loading start ===========")
    conn = pymysql.connect(host='192.168.1.23', user='root', password='1231',
                           db='bms_test', charset='utf8')
    curs = conn.cursor()
    curs.execute(sql)
    rows = curs.fetchall()
    # print("{}개의 데이터 로딩".format(len(rows)))
    data = pd.DataFrame(rows, columns=['name', 'now', 'before', 'date'])

    return data

def load_potato_price():
    sql = """
    SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date`
    FROM tbl_item WHERE tbl_item.`date` > '2011-01-01' and tbl_item.`품목` LIKE CONCAT('%' ,'%감자','%') 
    ORDER BY tbl_item.date ASC 
    """
    return load_crops_data(sql)

def load_tomato_price():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item  
    WHERE tbl_item.`품목` LIKE '방울토마토%'
    """
    return load_crops_data(sql)

def load_green_pepper():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item  
    WHERE tbl_item.`품목` IN ('풋고추(일반)', '풋고추')
    """
    return load_crops_data(sql)

def load_red_pepper():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item 
    WHERE tbl_item.`품목` IN ('풋고추(청양계)', '청양계풋고추')
    """
    return load_crops_data(sql)

def load_cabbage():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item 
    WHERE tbl_item.`품목` LIKE '배추%'
    """
    return load_crops_data(sql)

def load_cabbage1():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item 
    WHERE tbl_item.`품목` LIKE '양배추'
    """
    return load_crops_data(sql)

def load_onion():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item 
    WHERE tbl_item.`품목` LIKE '양파'
    """
    return load_crops_data(sql)

def load_carrot():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item 
    WHERE tbl_item.`품목` LIKE '당근'
    """
    return load_crops_data(sql)

def load_green_onion():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item 
    WHERE tbl_item.`품목` LIKE '대파%'
    """
    return load_crops_data(sql)

def load_cucumber():
    sql = """SELECT tbl_item.`품목`, tbl_item.`당일`, tbl_item.`전일`, tbl_item.`date` FROM tbl_item 
    WHERE tbl_item.`품목` LIKE '%백다다기%'
    """
    return load_crops_data(sql)

def processing_data(data, name):
    data['now'] = data['now'].apply(lambda x: int(x.replace(',', '')))
    data['before'] = data['before'].apply(lambda x: int(x.replace(',', '')))
    data['date'] = data['date'].apply(lambda x: parse(str(x)))

    data = pd.merge(dt_index, data, how='left', left_on='date', right_on='date').set_index('date')

    # fill null value
    def zero_to_nan(data):
        if math.isnan(data):
            return data
        elif data == 0:
            return np.nan
        else:
            return data

    data['before'] = data['before'].apply(zero_to_nan)
    data['now'] = data['now'].apply(zero_to_nan)

    data['Fill_value'] = data.shift(-1)['before']
    data['now'] = data[['now', 'Fill_value']].apply(lambda x: x['Fill_value'] if math.isnan(x['now']) else x['now'],
                                                    axis=1)

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill').rename(columns={'now': name})

    data.drop(['name', 'before', 'Fill_value'], axis=1, inplace=True)

    data = drop_duplicates(data)

    print(data.tail(3))
    print()
    return data

def load_data_bms_test(sql):
    # print("======= data loading start ===========")
    conn = pymysql.connect(host='192.168.1.23', user='root', password='1231',
                           db='bms_test', charset='utf8')
    curs = conn.cursor()
    curs.execute(sql)
    rows = curs.fetchall()
    # print("{}개의 데이터 로딩".format(len(rows)))
    data = pd.DataFrame(rows)  # , columns=['name','now','before','date'])
    # print(data.head(3))
    # print("======= data loading finish ===========")
    # print()
    return data

def processing_stock_data(col_name):
    sql = 'SELECT DATE, price_closing FROM stock_day WHERE com_name LIKE \'' + col_name + '\' and DATE > \'2011-01-01\''

    data = load_data_bms_test(sql)

    data = data.rename(columns={0: 'date', 1: col_name})
    data['date'] = data['date'].apply(lambda x: parse(str(x)))
    # data[col_name] = data[col_name].apply(lambda x : int(x.replace(',','')))

    data = pd.merge(dt_index, data, how='left', left_on='date', right_on='date')  # .set_index('date')

    data = data.fillna(method='ffill').set_index('date')

    print(data.tail(3))
    print()

    return data

def processing_exchangerate_kospi_egg_milk_sugar(table_name):
    if table_name in ['exchangerate', 'kospi']:
        sql = 'SELECT DATE, price_closing FROM ' + table_name
    elif table_name in ['price_egg', 'price_milk']:
        sql = 'SELECT DATE, price FROM ' + table_name
    elif table_name in ['price_sugar']:
        sql = 'SELECT date, price_closing FROM price_sugar'

    data = load_data_bms_test(sql)
    data = data.rename(columns={0: 'date', 1: table_name}).drop_duplicates(['date'])
    data['date'] = data['date'].apply(lambda x: parse(str(x)))
    if table_name in ['exchangerate', 'kospi', 'price_sugar']:
        data[table_name] = data[table_name].apply(lambda x: float(x.replace(',', '')))
    elif table_name in ['price_egg', 'price_milk']:
        data[table_name] = data[table_name].apply(lambda x: int(x.replace(',', '')))

    data = pd.merge(dt_index, data, how='left', left_on='date', right_on='date').set_index('date')

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    print(data.tail(3))
    print()
    return data

def processing_oil_price():
    sql = 'SELECT * FROM price_oil'

    data = load_data_bms_test(sql).replace('-', np.nan)

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    data = data.rename(columns={0: 'date', 1: 'Dubai', 2: 'Brent', 3: 'WTI'})
    data['date'] = data['date'].apply(lambda x: parse(str(x)))
    data = pd.merge(dt_index, data, how='left', left_on='date', right_on='date').set_index('date')

    data = data.apply(pd.to_numeric, errors='coerce')

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    print(data.tail(3))
    print()
    return data


def cor_to_database(data):
    conn = pymysql.connect(host='192.168.1.23', user='root', password='1231',
                           db='bms_test', charset='utf8')


    curs = conn.cursor()
    sql = "delete from stock_corr"
    curs.execute(sql)


    sql = '''INSERT INTO stock_corr VALUES (%s,%s,%s)'''

    data = data.corr().loc[:'푸드웰', :'푸드웰']
    for i in data.index:
        for j in data.columns:
            if data[i][j] != 1:
                curs.execute(sql, tuple([i, j, float(data[i][j])]))
                # print(tuple([i, j, data[i][j]]))
    conn.commit()

if __name__ == "__main__":
    print('==========감자 가격 전처리=============')
    potato_price = processing_potato_price(load_potato_price())

    print('========방울토마토 가격 전처리==========')
    tomato_price = processing_data(load_tomato_price(), 'tomato')

    print('==========풋고추 가격 전처리============')
    green_pepper_price = processing_data(load_green_pepper(), 'green_pepper')

    print('==========청양고추 가격 전처리============')
    red_pepper_price = processing_data(load_red_pepper(), 'red_pepper')

    print('==========배추 가격 전처리============')
    cabbage_price = processing_data(load_cabbage(), 'cabbage')

    print('=========양배추 가격 전처리============')
    cabbage1_price = processing_data(load_cabbage1(), 'cabbage1')

    print('=========양파 가격 전처리============')
    onion_price = processing_data(load_onion(), 'onion')

    print('=========당근 가격 전처리============')
    carrot_price = processing_data(load_carrot(), 'carrot')

    print('=========대파 가격 전처리============')
    green_onion_price = processing_data(load_green_onion(), 'green_onion')

    print('=========오이 가격 전처리============')
    cucumber_price = processing_data(load_cucumber(), 'cucumber')

    print('=========계란 가격 전처리============')
    egg_price = processing_exchangerate_kospi_egg_milk_sugar('price_egg')

    print('=========우유 가격 전처리============')
    milk_price = processing_exchangerate_kospi_egg_milk_sugar('price_milk')

    print('============설탕 가격 전처리==============')
    sugar_price = processing_exchangerate_kospi_egg_milk_sugar('price_sugar')

    print('============환율 전처리================')
    Exchange_Rate = processing_exchangerate_kospi_egg_milk_sugar('exchangerate')

    print('============코스피 전처리==============')
    KOSPI = processing_exchangerate_kospi_egg_milk_sugar('kospi')

    print('============원유 가격 전처리==============')
    oil_price = processing_oil_price()

    print('=========아시아종묘 주식 전처리============')
    Stock_Asia = processing_stock_data('아시아종묘')

    print('==============조비 주식 전처리==============')
    stock_Jobi = processing_stock_data('조비')

    print('==========효성오앤비 주식 전처리==========')
    stock_Hyosung = processing_stock_data('효성오앤비')

    print('==========경농 주식 전처리==========')
    stock_Farming = processing_stock_data('경농')

    print('==========남해화학 주식 전처리==========')
    stock_Namhae_Chemical = processing_stock_data('남해화학')

    print('==========KG케미칼 주식 전처리==========')
    stock_KGChemical = processing_stock_data('KG케미칼')

    print('==========농우바이오 주식 전처리==========')
    stock_Nongwoo_Bio = processing_stock_data('농우바이오')

    print('==========성보화학 주식 전처리==========')
    stock_Sungbo_Chemical = processing_stock_data('성보화학')

    print('==========아세아텍 주식 전처리==========')
    stock_Asia_Tech = processing_stock_data('아세아텍')

    print('==========동방아그로 주식 전처리==========')
    stock_Eastern_Agro = processing_stock_data('동방아그로')

    print('==========KPX생명과학 주식 전처리==========')
    stock_KPX = processing_stock_data('KPX생명과학')

    print('==========SPC삼립 주식 전처리==========')
    stock_SPC = processing_stock_data('SPC삼립')

    print('==========풀무원 주식 전처리==========')
    stock_Pulmuone = processing_stock_data('풀무원')

    print('==========농심 주식 전처리==========')
    stock_Nongshim = processing_stock_data('농심')

    print('==========오뚜기 주식 전처리==========')
    stock_Ottogi = processing_stock_data('오뚜기')

    print('==========오리온 주식 전처리==========')
    stock_Orion = processing_stock_data('오리온')

    print('==========해태제과 주식 전처리==========')
    stock_Haitai = processing_stock_data('해태제과')

    print('==========롯데제과 주식 전처리==========')
    stock_Lotte = processing_stock_data('롯데제과')

    print('==========카프로 주식 전처리==========')
    stock_Capro = processing_stock_data('카프로')

    print('==========대동공업 주식 전처리==========')
    stock_Daedong = processing_stock_data('대동공업')

    print('==========서울식품 주식 전처리==========')
    stock_Seoulfood = processing_stock_data('서울식품')

    print('==========남양유업 주식 전처리==========')
    stock_Namyang = processing_stock_data('남양유업')

    print('==========대한제당 주식 전처리==========')
    stock_TS = processing_stock_data('대한제당')

    print('==========조흥 주식 전처리==========')
    stock_Choheung = processing_stock_data('조흥')

    print('==========빙그레 주식 전처리==========')
    stock_Bing = processing_stock_data('빙그레')

    print('==========롯데푸드 주식 전처리==========')
    stock_Lottefood = processing_stock_data('롯데푸드')

    print('==========CJ제일제당 주식 전처리==========')
    stock_CJ = processing_stock_data('CJ제일제당')

    print('==========삼양식품 주식 전처리==========')
    stock_Samyang = processing_stock_data('삼양식품')

    print('==========매일홀딩스 주식 전처리==========')
    stock_Maeil = processing_stock_data('매일홀딩스')

    print('==========푸드웰 주식 전처리==========')
    stock_Foodwell = processing_stock_data('푸드웰')

    print('================전처리 끝===============')

    result_data = pd.concat([Stock_Asia, stock_Jobi, stock_Hyosung, stock_Farming, stock_Namhae_Chemical,
                             stock_KGChemical, stock_Nongwoo_Bio, stock_Sungbo_Chemical, stock_Asia_Tech,
                             stock_Eastern_Agro,
                             stock_KPX, stock_SPC, stock_Pulmuone, stock_Nongshim, stock_Ottogi,
                             stock_Capro, stock_Daedong, stock_Seoulfood, stock_Namyang, stock_TS,
                             stock_Choheung, stock_Bing, stock_Lottefood, stock_CJ, stock_Samyang,
                             stock_Maeil, stock_Foodwell,
                             potato_price, tomato_price, green_pepper_price, red_pepper_price, cabbage_price,
                             cabbage1_price, onion_price, carrot_price, green_onion_price, cucumber_price,
                             egg_price, milk_price, sugar_price, Exchange_Rate, KOSPI, oil_price], axis=1)
    result_data.to_csv('result.csv', encoding='utf-8')

    # 상관관계 DB 입력
    cor_to_database(result_data)

    # result_data.corr().loc['potato':, '아시아종묘':].style.background_gradient(cmap='summer_r')