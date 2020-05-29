import tensorflow as tf
import datetime as dt
import matplotlib.pyplot as plt
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
from tensorflow.keras.models import load_model

def init():
    print(tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))
    print(tf.__version__)
    print(tf.keras.__version__)
    print(pd.__version__)

def load_data():
    # 파일 불러오기 예시
    # pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/train.csv')
    # 4319
    print('---------  load_data  ----------')
    data = pd.read_csv('result.csv', encoding='utf-8').set_index('date')
    print(data.shape)
    print(data.head(1))
    print()
    return data

def data_processing(data, target_names):
    print('---------  data_processing  ----------')
    target_name = target_names[0]
    # target_names = [target_name]  # , 'green_pepper'
    shift_steps = 1

    # x_data
    df = data[target_names].shift(1)
    print(df.tail(2))
    x_data = df.values[shift_steps:] # numpy array
    print("x_data Shape:", x_data.shape)
    print()

    # y_data
    df_targets = df[target_name].shift(-shift_steps)
    print(df_targets.tail(2))
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

    # The shape of both input tensors are:
    # [batch_size, sequence_length, num_y_signals].

    # Ignore the "warmup" parts of the sequences
    # by taking slices of the tensors.
    y_true_slice = y_true[:, 50:, :]
    y_pred_slice = y_pred[:, 50:, :]

    # These sliced tensors both have this shape:
    # [batch_size, sequence_length - 50, num_y_signals]

    # Calculat the Mean Squared Error and use it as loss.
    mse = mean(abs(y_true_slice - y_pred_slice) ** 2)

    return mse

def init_model(num_x_y_xtrain):
    model = Sequential()

    model.add(GRU(units=256,
                  return_sequences=True,
                  input_shape=(None, num_x_y_xtrain[0],)))

    model.add(Dense(num_x_y_xtrain[1], activation='sigmoid'))

    optimizer = RMSprop(lr=1e-3)

    model.compile(loss=loss_mse_warmup, optimizer=optimizer)

    model.summary()

    return model

def callback():
    callback_early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
    callback_reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, min_lr=1e-4, patience=0, verbose=1)
    callbacks = [callback_early_stopping, callback_reduce_lr]

    return callbacks

# target_lst = ['아시아종묘', 'green_pepper']

target_lsts = [['아시아종묘', 'green_pepper'],
               ['아세아텍', 'price_egg'],
               ['효성오앤비', 'kospi'],
               ['남해화학', 'price_egg'],
               ['SPC삼립', 'kospi'],
               ['조비', 'price_egg'],
               ['경농', 'green_onion'],
               ['KPX생명과학', 'cabbage1'],
               ['KG케미칼', 'potato'],
               ['농심', 'price_sugar'],
               ['농우바이오', 'kospi'],
               ['동방아그로', 'exchangerate'],
               ['오뚜기', 'onion']]

if __name__ == '__main__':
    for target_lst in target_lsts[:2]:
        print('----------' ,target_lst, '------------')
        # GPU 확인
        init()

        # data_load
        data = load_data()

        # data_processing
        x_train_scaled, x_test_scaled, y_train_scaled, y_test_scaled, num_x_y_xtrain = data_processing(data, target_lst)

        # generator 생성
        generator = batch_generator(batch_size=128, sequence_length=365, num_x_y_xtrain = num_x_y_xtrain)

        # model 생성
        model = init_model(num_x_y_xtrain)

        # callback 설정
        callbacks = callback()
        # validation_data
        validation_data = (np.expand_dims(x_train_scaled, axis=0), np.expand_dims(y_train_scaled, axis=0))

        # model learning
        model.fit(x=generator,
                  epochs=1,
                  steps_per_epoch=100,
                  validation_data=validation_data,
                  callbacks=callbacks)

        model.save('model/' + str(target_lst).replace('\'','') + '.h5')

        del model

    sys.exit()
