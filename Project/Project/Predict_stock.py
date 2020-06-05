import tensorflow as tf
import numpy as np
import pandas as pd
import sys
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, GRU, Embedding
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from tensorflow.keras.backend import square, mean
import time

def init():
    print(tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))
    print(tf.__version__)
    print(tf.keras.__version__)
    print(pd.__version__)

def load_data():
    print('---------  load_data  ----------')
    data = pd.read_csv('result.csv', encoding='utf-8').set_index('date')
    print(data.shape)
    print(data.head(1))
    print()
    return data

def data_processing(data, target_names):
    print('---------  data_processing  ----------')
    target_name = target_names[0]
    shift_steps = 1

    # x_data
    df = data[target_names].shift(1)
    print(df.tail(1))
    x_data = df.values[shift_steps:] # numpy array
    print("x_data Shape:", x_data.shape)
    print()

    # y_data
    df_targets = df[target_name].shift(-shift_steps)
    print(df_targets.tail(1))
    y_data = df_targets.values[shift_steps:].reshape(-1, 1) # numpy array
    print("y_data Shape:", y_data.shape)
    print()

    # train, test split
    num_data = len(x_data)
    train_split = 0.9
    num_train = int(train_split * num_data)
    num_test = num_data - num_train
    print('ALl data : %d, train data : %d, test data : %d' %(num_data, num_train, num_test))
    print()

    x_train = x_data[0:num_train]
    x_test = x_data[num_train:]
    y_train = y_data[0:num_train]
    y_test = y_data[num_train:]

    num_x_y_xtrain = [x_data.shape[1], y_data.shape[1], num_train]

    # Scaled Data
    x_scaler = MinMaxScaler()
    x_train_scaled = x_scaler.fit_transform(x_train)
    x_test_scaled = x_scaler.transform(x_test)

    y_scaler = MinMaxScaler()
    y_train_scaled = y_scaler.fit_transform(y_train)
    y_test_scaled = y_scaler.transform(y_test)

    return x_train_scaled, x_test_scaled, y_train_scaled, y_test_scaled, num_x_y_xtrain

def batch_generator(batch_size, sequence_length, num_x_y_xtrain):
    """
    Generator function for creating random batches of training-data.
    """

    # Infinite loop.
    while True:
        # Allocate a new array for the batch of input-signals.
        x_shape = (batch_size, sequence_length, num_x_y_xtrain[0])
        x_batch = np.zeros(shape=x_shape, dtype=np.float16)

        # Allocate a new array for the batch of output-signals.
        y_shape = (batch_size, sequence_length, num_x_y_xtrain[1])
        y_batch = np.zeros(shape=y_shape, dtype=np.float16)

        # Fill the batch with random sequences of data.
        for i in range(batch_size):
            # Get a random start-index.
            # This points somewhere into the training-data.
            idx = np.random.randint(num_x_y_xtrain[2] - sequence_length)

            # Copy the sequences of data starting at this index.
            x_batch[i] = x_train_scaled[idx:idx + sequence_length]
            y_batch[i] = y_train_scaled[idx:idx + sequence_length]

        yield (x_batch, y_batch)

def loss_mse_warmup(y_true, y_pred):
    """
    Calculate the Mean Squared Error between y_true and y_pred,
    but ignore the beginning "warmup" part of the sequences.

    y_true is the desired output.
    y_pred is the model's output.
    """
    y_true_slice = y_true[:, 50:, :]
    y_pred_slice = y_pred[:, 50:, :]

    # Calculat the Mean Squared Error and use it as loss.
    mse = mean(square(y_true_slice - y_pred_slice))

    return mse

def init_model(num_x_y_xtrain):
    model = Sequential()

    model.add(GRU(units=units,
                  return_sequences=True,
                  input_shape=(None, num_x_y_xtrain[0],)))

    model.add(Dense(num_x_y_xtrain[1], activation='sigmoid'))

    optimizer = RMSprop(lr=learning_rate)

    model.compile(loss=loss_mse_warmup, optimizer=optimizer)

    # model.summary()

    return model

def callback():
    callback_early_stopping = EarlyStopping(monitor='val_loss', patience=patience, verbose=1)
    callback_reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, min_lr=1e-4, patience=0, verbose=1)
    callbacks = [callback_early_stopping, callback_reduce_lr]

    return callbacks

# target_lst = ['아시아종묘', 'green_pepper']

# target_lsts = [['아시아종묘', 'green_pepper'],
#                ['아세아텍', 'price_egg'],
#                ['효성오앤비', 'kospi'],
#                ['남해화학', 'price_egg'],
#                ['SPC삼립', 'kospi'],
#                ['조비', 'price_egg'],
#                ['경농', 'green_onion'],
#                ['KPX생명과학', 'cabbage1'],
#                ['KG케미칼', 'potato'],
#                ['농심', 'price_sugar'],
#                ['농우바이오', 'kospi'],
#                ['동방아그로', 'exchangerate'],
#                ['오뚜기', 'onion']]

batch_size, sequence_length, epochs, units, learning_rate, patience = 256, 65, 100, 512, 1e-2, 10

target_lsts = [['아시아종묘','potato'],['아시아종묘','price_milk'],['아시아종묘','exchangerate'],
               ['조비','carrot'],['조비','price_egg'],['조비','price_milk'],
               ['효성오앤비','carrot'],['효성오앤비','price_milk'],['효성오앤비','kospi'],
               ['경농','green_onion'],['경농','price_egg'],['경농','Dubai'],
               ['남해화학','cabbage1'],['남해화학','exchangerate'],['남해화학','kospi'],
               ['KG케미칼'],['KG케미칼','price_milk'],['KG케미칼','kospi'],
               ['농우바이오','potato'],['농우바이오','exchangerate'],['농우바이오','kospi'],
               ['성보화학','onion'],['성보화학','carrot'],['성보화학','kospi'],
               ['아세아텍'],['아세아텍','price_egg'],['아세아텍','exchangerate'],
               ['동방아그로'],['동방아그로','green_pepper'],['동방아그로','kospi'],
               ['KPX생명과학','potato'],['KPX생명과학','cabbage'],['KPX생명과학','cabbage1'],
               ['SPC삼립','onion'],['SPC삼립','price_sugar'],['SPC삼립','Dubai'],
               ['풀무원','carrot'],['풀무원','price_milk'],['풀무원','price_sugar'],
               ['농심'],['농심','onion'],['농심','price_sugar'],
               ['오뚜기','onion'],['오뚜기','carrot'],['오뚜기','price_egg'],
               ['카프로', 'potato'], ['카프로', 'red_pepper'],['카프로', 'WTI'],
               ['대동공업'], ['대동공업', 'cabbage1'], ['대동공업', 'price_milk'],
               ['남양유업'], ['남양유업', 'green_onion'], ['남양유업', 'exchangerate'],
               ['대한제당'], ['대한제당', 'tomato'],['대한제당', 'WTI'],
               ['조흥'],['조흥', 'price_egg'], ['조흥', 'price_milk'],
               ['빙그레'], ['빙그레', 'cucumber'], ['빙그레', 'exchangerate'],
               ['롯데푸드'],['롯데푸드', 'green_onion'], ['롯데푸드', 'price_milk'],
               ['CJ제일제당', 'price_milk'], ['CJ제일제당', 'price_sugar'],['CJ제일제당', 'exchangerate'],
               ['삼양식품'],['삼양식품', 'price_egg'], ['삼양식품', 'price_milk'],
               ['매일홀딩스', 'price_egg'], ['매일홀딩스', 'price_sugar'], ['매일홀딩스', 'Dubai'],
               ['푸드웰'], ['푸드웰', 'green_pepper'], ['푸드웰', 'red_pepper']]



# BEST

# batch_size=256, sequence_length=100, epochs=100, units=256, RMSprop(lr=1e-3), patience=10
# 420분
# 5 / 0.52

# batch_size=256, sequence_length=65, epochs=100, units=512, RMSprop(lr=1=1e-3), patience=10
# 360 분
# 8 / 0.

# batch_size=256, sequence_length=65, epochs=100, units=512, RMSprop(lr=1=1e-2), patience=10

# batch_size=256, sequence_length=65, epochs=100, units=512, RMSprop(lr=1e-2), patience=10
# 150분
# 13 / 0.49


############################ result model ############################
# batch_size=256, sequence_length=100, epochs=100, units=256, RMSprop(lr=1e-3), patience=10
#batch_size, sequence_length, epochs, units, learning_rate, patience = 256, 100, 100, 256, 1e-3, 10

# target_lsts = [['아시아종묘','potato'],['아시아종묘','price_milk'],['아시아종묘','exchangerate'],
#                ['경농','green_onion'],['경농','price_egg'],['경농','Dubai'],
#                ['성보화학','onion'],['성보화학','carrot'],['성보화학','kospi'],
#                ['아세아텍'],['아세아텍','price_egg'],['아세아텍','exchangerate'],
#                ['동방아그로'],['동방아그로','green_pepper'],['동방아그로','kospi'],
#                ['농심'],['농심','onion'],['농심','price_sugar'],
#                ['카프로', 'potato'], ['카프로', 'red_pepper'],['카프로', 'WTI'],
#                ['남양유업'],['남양유업', 'green_onion'], ['남양유업', 'exchangerate'],
#                ['대한제당'], ['대한제당', 'tomato'],['대한제당', 'WTI'],
#                ['조흥'], ['조흥', 'price_egg'], ['조흥', 'price_milk'],
#                ['롯데푸드'],['롯데푸드', 'green_onion'], ['롯데푸드', 'price_milk'],
#                ['CJ제일제당', 'price_milk'], ['CJ제일제당', 'price_sugar'],['CJ제일제당', 'exchangerate'],
#                ['삼양식품'],['삼양식품', 'price_egg'], ['삼양식품', 'price_milk']]

# # batch_size=256, sequence_length=65, epochs=100, units=512, RMSprop(lr=1=1e-3), patience=10
# batch_size, sequence_length, epochs, units, learning_rate, patience = 256, 65, 100, 512, 1e-3, 10

# target_lsts = [['조비','carrot'],['조비','price_egg'],['조비','price_milk'],
#                ['효성오앤비','carrot'],['효성오앤비','price_milk'],['효성오앤비','kospi'],
#                ['남해화학','cabbage1'],['남해화학','exchangerate'],['남해화학','kospi'],
#                ['KG케미칼'],['KG케미칼','price_milk'],['KG케미칼','kospi'],
#                ['농우바이오','potato'],['농우바이오','exchangerate'],['농우바이오','kospi'],
#                ['KPX생명과학','potato'],['KPX생명과학','cabbage'],['KPX생명과학','cabbage1'],
#                ['SPC삼립','onion'],['SPC삼립','price_sugar'],['SPC삼립','Dubai'],
#                ['풀무원','carrot'],['풀무원','price_milk'],['풀무원','price_sugar'],
#                ['오뚜기','onion'],['오뚜기','carrot'],['오뚜기','price_egg'],
#                ['대동공업'], ['대동공업', 'cabbage1'], ['대동공업', 'price_milk'],
#                ['빙그레'],['빙그레', 'cucumber'], ['빙그레', 'exchangerate'],
#                ['매일홀딩스', 'price_egg'],['매일홀딩스', 'price_sugar'], ['매일홀딩스', 'Dubai'],
#                ['푸드웰'], ['푸드웰', 'green_pepper'], ['푸드웰', 'red_pepper']]



if __name__ == '__main__':
    # GPU 확인
    init()

    # data_load
    data = load_data()
    # callback 설정
    callbacks = callback()

    start = time.time()

    for target_lst in target_lsts:
        print('----------' ,target_lst, '------------')

        # data_processing
        x_train_scaled, x_test_scaled, y_train_scaled, y_test_scaled, num_x_y_xtrain = data_processing(data, target_lst)

        # generator 생성
        generator = batch_generator(batch_size=batch_size, sequence_length=sequence_length, num_x_y_xtrain = num_x_y_xtrain)

        # model 생성
        model = init_model(num_x_y_xtrain)

        # validation_data
        validation_data = (np.expand_dims(x_train_scaled, axis=0), np.expand_dims(y_train_scaled, axis=0))

        # model learning
        model.fit(x=generator,
                  epochs=epochs,
                  steps_per_epoch=100,
                  validation_data=validation_data,
                  callbacks=callbacks)

        model.save('model/' + str(target_lst).replace('\'','') + '.h5')

        del model

    print('소요시간 : ', time.time() - start)
    sys.exit()
