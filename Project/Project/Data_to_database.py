import pymysql
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sys

import Predict_stock

def pred(model, pred_x_data, y_true):
    '''
    수익률 계산을 위한 실제 주식값, 예측 주식값 생성
    '''
    x_scaler = MinMaxScaler()
    y_scaler = MinMaxScaler()

    pred_x_train_scaled = x_scaler.fit_transform(pred_x_data)
    pred_x = np.expand_dims(pred_x_train_scaled, axis=0)
    pred = model.predict(pred_x)

    y_true_scaled = y_scaler.fit_transform(y_true)
    pred_rescaled = y_scaler.inverse_transform(pred[0])
    pred = pred_rescaled[:, 0].astype(np.int)

    return y_true, pred

def create_DB_data(data, target_lst):
    print('---------   create DB data --------')
    target_name = target_lst[0]

    # date
    date = np.array((data[target_lst].reset_index()['date'][1:])).reshape(-1, 1)

    print(date.shape)

    # com_name
    com_name = np.array([target_name for _ in range(len(date))]).reshape(-1, 1)
    # com_code
    com_code = np.array(['000001' for _ in range(len(date))]).reshape(-1, 1)
    # tod_price
    tod_price = np.array(data[target_name])[1:].reshape(-1, 1)

    print(tod_price.shape)

    # tod_status
    tod_status = np.array([0 for _ in range(len(date))]).reshape(-1, 1)
    sub = tod_price[1:] - tod_price[:-1]
    for idx, value in enumerate(sub):
        if value > 0:
            tod_status[idx + 1] = 1
        elif value < 0:
            tod_status[idx + 1] = -1

    # tom_price
    tom_price = np.array(data[target_name])[1:]
    tom_price[1:] += p[1:] - p[:-1]
    tom_price = tom_price.reshape(-1, 1)

    # tom_status
    # 오늘 종가로부터 상향, 하향, 유지
    tom_status = np.array([0 for _ in range(len(date))]).reshape(-1, 1)
    for idx, value in enumerate(tom_price - tod_price):
        if value > 0:
            tom_status[idx] = 1
        elif value < 0:
            tom_status[idx] = -1

    # match_status
    # 작일 예측 여부 확인
    match_status = np.array([True for _ in range(len(date))]).reshape(-1, 1)
    for idx, value in enumerate(tom_status[:-1] == tod_status[1:]):
        match_status[idx + 1] = value

    # price_error
    # 작일 예측값 - 금일 종가의 절댓값
    price_error = np.array([0 for _ in range(len(date))]).reshape(-1, 1)
    for idx, value in enumerate(tom_price[:-1] - tod_price[1:]):
        price_error[idx + 1] = abs(value)

    # return
    # 금일 수익률
    # 작일 tom_status > 0 => (금일 tod_price) - (작일 tod_price) 만큼 수익 발생
    # 작일 tom_status <= 0 => 수익 없음
    returns = np.array([1.0 for _ in range(len(date))]).reshape(-1, 1)

    for idx, value in enumerate(tom_status[:-1]):
        if value == 1:
            returns[idx] += (tod_price[idx + 1] - tod_price[idx]) / tod_price[idx]
    returns = np.round(returns, 3)

    DB_data = pd.DataFrame(np.concatenate(
        [com_name, com_code, date, tod_price, tod_status, tom_price, tom_status, match_status, price_error, returns],
        axis=1), columns=['com_name', 'com_code', 'date', 'tod_price', 'tod_status', 'tom_price', 'tom_status',
                          'match_status', 'price_error', 'return'])
    # com_name,date,tod_price,tod_status,tom_price,tom_status,match_status,price_error,returns

    print(DB_data.tail())
    # print(np.prod(returns[-50:-1]))
    # print(match_status[-50:-1].mean())

    return DB_data

def db_to_database(DB_data):
    print('---------   db_to_database --------')
    conn = pymysql.connect(host='192.168.1.23', user='root', password='1231',
                               db='bms_test', charset='utf8')

    curs = conn.cursor()

    sql = "delete from stock_predict where com_name = %s"
    curs.execute(sql, DB_data['com_name'][0])

    sql = '''INSERT INTO stock_predict VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

    # print(DB_data.head().values)
    for data in DB_data.values:
        curs.execute(sql, (tuple(data)))

    conn.commit()

def find_final_lst(lsts):

    # print(lsts)

    idx = 0
    final_lsts = []
    name,accuracy,returns  = '', 0, 0

    for lst in lsts:
        print(lst)
        if stock_lsts[idx] in lst[0]:
            if accuracy < lst[1]:
                name, accuracy, returns = lst
            elif accuracy == lst[1] and returns < lst[2]:
                name, accuracy, returns = lst
        else:
            final_lsts.append([name, accuracy, returns])
            name, accuracy, returns = '', 0, 0
            idx += 1
            if accuracy < lst[1]:
                name, accuracy, returns = lst
            elif accuracy == lst[1] and returns < lst[2]:
                name, accuracy, returns = lst

    final_lsts.append([name, accuracy, returns])

    return final_lsts

stock_lsts = ['아시아종묘', '조비', '효성오앤비', '경농', '남해화학',
              'KG케미칼', '농우바이오', '성보화학', '아세아텍', '동방아그로',
              'KPX생명과학', 'SPC삼립', '풀무원', '농심', '오뚜기',
              '카프로', '대동공업','남양유업', '대한제당', '조흥',
              '빙그레', '롯데푸드', 'CJ제일제당', '삼양식품', '매일홀딩스',
              '푸드웰']

# stock_lsts = ['카프로','대동공업','서울식품','남양유업','대한제당',
#               '조흥','빙그레','롯데푸드','CJ제일제당','삼양식품',
#               '매일홀딩스','동서','푸드웰']


if __name__ == '__main__':
    # GPU 확인
    Predict_stock.init()

    # data_load
    data = Predict_stock.load_data()

    print(data.tail())

    # data_processing
    target_lsts = Predict_stock.target_lsts

    predict_result = []

    # 모든 모델 성능 확인
    for target_lst in target_lsts:
        print('--------', target_lst, '--------')
        x_train_scaled, x_test_scaled, y_train_scaled, y_test_scaled, num_x_y_xtrain = Predict_stock.data_processing(data, target_lst)

        # model 생성
        model = Predict_stock.init_model(num_x_y_xtrain)
        # model 불러오기
        model.load_weights('model/' + str(target_lst).replace('\'', '') + '.h5')

        t, p = pred(model, data[target_lst].shift(1).values[1:], np.array(data[target_lst[0]].values[1:], dtype=np.float).reshape(-1,1))

        DB_data = create_DB_data(data, target_lst)

        print(DB_data.tail(3))

        predict_result.append([str(target_lst), DB_data.match_status[-65:].mean(), np.prod(DB_data['return'][-65:])])

        # db_to_database(DB_data)

        del model


    final_lsts = find_final_lst(predict_result)

    # data_load
    data = Predict_stock.load_data()

    for lst, a, b in final_lsts:
        lst = lst.split('\'')
        if lst[1] == lst[-2]: target_lst = [lst[1]]
        else: target_lst = [lst[1], lst[-2]]

        print('--------', target_lst, '--------')

        x_train_scaled, x_test_scaled, y_train_scaled, y_test_scaled, num_x_y_xtrain = Predict_stock.data_processing(data, target_lst)

        # model 생성
        model = Predict_stock.init_model(num_x_y_xtrain)
        # model 불러오기
        model.load_weights('model/' + str(target_lst).replace('\'', '') + '.h5')

        t, p = pred(model, data[target_lst].shift(1).values[1:], np.array(data[target_lst[0]].values[1:], dtype=np.float).reshape(-1, 1))

        print(len(t), len(p))

        DB_data = create_DB_data(data, target_lst)

        db_to_database(DB_data)

        del model


    sys.exit()
