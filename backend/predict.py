import numpy as np
from scipy.interpolate import griddata
import mlflow
import math
import os

from flask import current_app


# MLflowのModel Registryに接続
remote_server_uri = "http://160.251.202.211:5000/"
mlflow.set_tracking_uri(remote_server_uri)

# 2次元配列の線形補間を行う関数
def linear_interpolate(coordinates, values):
    """
    coordinates:既知の値の座標のリスト
    values:coordinatesの各座標に対応する値
    ======================================
    grid_Z:実際の値の表示に使うグリッド
    scaled_grid_z:可視化した際に分布の違いがわかりやすくなるようにスケールしたグリッド
    """
    # メッシュの定義、複素数でステップ指定するとメッシュの分割数になる
    grid_x, grid_y = np.mgrid[0:1:10j, 0:1:10j]  # 50x50のメッシュ

    # griddataを使用して、既知の値をもとに2Dメッシュを線形補間
    grid_z = griddata(coordinates, values, (grid_x, grid_y), method='linear') # -> 2D ndarray

    # 全体の最小値と最大値を計算
    min_val = np.min(grid_z)
    max_val = np.max(grid_z)

    # 全体でMinMaxスケーリング
    scaled_grid_z = (grid_z - min_val) / (max_val - min_val)

    return grid_z, scaled_grid_z


# 出力した2次元配列をapexchartのデータフォーマットに変換
def convert_data(row):
    data_list=[]
    for index, val in enumerate(row.tolist(), 1):
        temp={'x':index,'y':round(val, 2)}
        data_list.append(temp)
    return data_list

def convert(res, type):
    converted_res=list(map(convert_data, res)) # -> list
    num_row = len(converted_res)
    formatted_data = [
        {
            'name':type,
            'data': converted_res[(num_row-1)-i]
        }
        for i in range(num_row)
    ]

    return formatted_data


# 温度を予測する
def predict_distribution(model_name, sensor_position, x):
    """
    x:説明変数 1D ndarray
    """
    # 使用するモデルの選択(MLflow上のエイリアスでモデルを変更できる)
    alias = 'champion'
    try:
        # 予測モデルの読み込み
        model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}_model@{alias}")
        # 標準化用のscalerの読み込み
        scaler = mlflow.sklearn.load_model(model_uri=f"models:/{model_name}_scaler@{alias}")
    except Exception as e:
        print("there is some errors in loading model")
        print(e)

    # 標準化
    try:
        scaled_x = scaler.transform(x[np.newaxis, :]) # バッチ軸がないとエラーになるので追加
    except Exception as e:
        print("there is some errors in scaling value")
        print(e)
    
    # 予測
    try:
        # 予測値のカラムとセンサーの対応関係はconfigのsensor_position.py参照
        pred = model.predict(scaled_x) # -> 2D ndarray
    except Exception as e:
        print("there is some errors")
        print(e)

    # all_pointsとall_valuesの各要素が対応するようにする
    list_coordinate_input = current_app.config[sensor_position]['coordinate_input'] # -> list
    list_coordinate_output = current_app.config[sensor_position]['coordinate_output'] # -> list
    all_coordinates = list_coordinate_input + list_coordinate_output # -> list

    list_value_input = x.tolist()
    list_value_output = pred.tolist()[0]
    all_values = list_value_input + list_value_output # -> list

    # 既知の値をもとに2次元のメッシュを線形補完
    grid_z, scaled_grid_z = linear_interpolate(all_coordinates, all_values)

    return convert(grid_z, model_name), convert(scaled_grid_z, model_name)