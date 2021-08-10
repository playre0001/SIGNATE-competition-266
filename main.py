import tensorflow as tf
import numpy as np
import os
import csv
import argparse
import sys

import utils
import config
from preprocess import Preprocess

def CreateNetwork():
    input_num=tf.keras.layers.Input((18,),name="Input_Num")

    layers=[
        tf.keras.layers.Dense(4096,kernel_initializer='he_normal',bias_initializer="random_normal"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.LeakyReLU(),
        tf.keras.layers.Dense(4096,kernel_initializer='he_normal',bias_initializer="random_normal"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.LeakyReLU(),
        tf.keras.layers.Dense(2048,kernel_initializer='he_normal',bias_initializer="random_normal"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.LeakyReLU(),
        tf.keras.layers.Dense(1024,kernel_initializer='he_normal',bias_initializer="random_normal"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.LeakyReLU(),
        tf.keras.layers.Dense(1)
    ]

    x=input_num
    for layer in layers:
        x=layer(x)

    model=tf.keras.Model(inputs=input_num,outputs=x)
    model.compile(optimizer="adagrad",loss=utils.RMSE,metrics=[utils.RMSE])

    return model

def LoadNetwork(model_path):
    if os.path.isfile(model_path):
        return tf.keras.models.load_model(model_path,custom_objects={'RMSE': utils.RMSE})

def Learning(x,y,model,model_path):
    os.makedirs(os.path.dirname(model_path),exist_ok=True)

    mcp=tf.keras.callbacks.ModelCheckpoint(
        filepath=model_path,
        monitor="val_RMSE",
        save_best_only=True
    )

    def Generator(x,y):
        for i in range(len(x)):
            yield x[i],tf.constant([y[i]])

    sep=int(len(x)*config.VALIDATION_SPLIT)

    train=tf.data.Dataset.from_generator(
        Generator,
        args=[x[:sep],y[:sep]],
        output_types=(tf.float32,tf.float32),
        output_shapes=(tf.TensorShape((18,)),tf.TensorShape((1,)))
    )

    valid=tf.data.Dataset.from_generator(
        Generator,
        args=[x[sep:],y[sep:]],
        output_types=(tf.float32,tf.float32),
        output_shapes=(tf.TensorShape((18,)),tf.TensorShape((1,)))
    )

    train=train.shuffle(1000).batch(16)
    valid=valid.shuffle(1000).batch(16)

    history=model.fit(
        train,
        validation_data=valid,
        epochs=100,
        verbose=1,
        callbacks=[mcp]
    )

    return history

def Predict(x,model):
    test=tf.data.Dataset.from_tensor_slices(x)

    test=test.batch(16)

    utils.CSVWrite(model.predict(test))

def ParseArguments(args):
    """
    引数の解析を行う関数

    Args:
        args (sys.args[1:]): プログラムの引数

    Return:
        paser
    """

    #parserの定義
    parser=argparse.ArgumentParser(description="サンプル画像に写った物体の位置検出を行うプログラム")

    #引数の設定
    parser.add_argument("-l","--learning",action="store_true",help="If you want to learning, use this option.")
    parser.add_argument("--modelpath",default=os.path.join(config.MODEL_SAVE_PATH,"DenceOnly.hdf5"),type=str,help="This Network's model file path. This argument will be used by saving and loading.")
    
    #引数の解析
    return parser.parse_args()

def Main(args):
    model_path=args.modelpath

    if args.learning:
        train,_=Preprocess(os.path.join("Data","train.csv"),None)

        model=CreateNetwork()

        Learning(train[2],train[-1][0],model,model_path)
    else:
        train,test=Preprocess(os.path.join("Data","train.csv"),os.path.join("Data","test.csv"))

        model=LoadNetwork(model_path)

        Predict(test[2],model)

if __name__=="__main__":
    Main(ParseArguments(sys.argv[1:]))
