import pymysql
import datetime as dt
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta
from dateutil.parser import parse
import sys
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, GRU, Embedding
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from tensorflow.keras.backend import square, mean

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



if __name__ == '__main__':
    # GPU 확인
    Predict_stock.init()

    # data_load
    data = Predict_stock.load_data()

    # data_processing
    target_lsts = Predict_stock.target_lsts


    for target_lst in target_lsts[:1]:
        x_train_scaled, x_test_scaled, y_train_scaled, y_test_scaled, num_x_y_xtrain = Predict_stock.data_processing(data, target_lst)

        # generator 생성
        generator = Predict_stock.batch_generator(batch_size=256, sequence_length=365, num_x_y_xtrain=num_x_y_xtrain)

        # model 생성
        model = Predict_stock.init_model(num_x_y_xtrain)
        # model 불러오기
        model.load_weights('model/' + str(target_lst).replace('\'', '') + '.h5')

        t, p = pred(model, data[target_lst].shift(1).values[1:], np.array(data[target_lst[0]].values[1:], dtype=np.float).reshape(-1,1))
        # data[target_name]
        # print(t,p)

        del model


    sys.exit()
