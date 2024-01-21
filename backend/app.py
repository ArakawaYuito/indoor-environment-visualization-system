from flask import Flask, render_template, request, session, redirect, jsonify,current_app
import os
import datetime
import pickle
import json
import requests
import json
import numpy as np
from config import config

from ondotoriApi import getRequest_prevValue
from ondotoriApi import getRequest_currentValue
from predict import predict_distribution

from sqlalchemy.orm import sessionmaker
from db import init_db, engine
from db.models import Distribution, ApiLastRequest



app = Flask(__name__)

# アプリケーションの設定
config_name = os.environ.get("CONFIG", "base")
app.config.from_object(config[config_name])

# センサー設置位置の設定ファイルを読み込む
app.config.from_object(config["sensor_position"])

# データベースの初期化
init_db()

# データベース最大保存件数
max_db = 1000

# APIのリクエスト制限対策(秒)
REQ_INTERVAL = 15

# データベースから取り出したSQLAlchemyのオブジェクトを辞書に変換
def getByList(arr):
    res = []
    for item in arr:
        res.append(item.toDict())
    return res

# ondotori api
@app.route("/ondotori/<room>", methods=["GET"])
def get_ondotoriApi(room):
    # requests処理
    url, headers, payload = getRequest_prevValue()
    response = requests.post(url, headers=headers, json=payload)

    # データの抽出　ch1:Co2, ch2:temp, ch3:humid
    dict_response = response.json()
    timeSeries_value_co2 = [data['ch1'] for data in dict_response['data']]
    timeSeries_value_temp = [data['ch2'] for data in dict_response['data']]
    timeSeries_value_humid = [data['ch3'] for data in dict_response['data']]

    # 時間の抽出
    unixtime = [data["unixtime"] for data in dict_response["data"]]
    jst = datetime.timezone(
        datetime.timedelta(hours=9)
    )  # 日本時間（JST, UTC+9）のタイムゾーンオブジェクトを作成
    time_jst = [
        datetime.datetime.fromtimestamp(int(i), jst).strftime("%Y-%m-%dT%H:%M:%S")
        for i in unixtime
    ]  # =>list(各要素は日時の文字列)

    res = {"Co2": timeSeries_value_co2, "temp": timeSeries_value_temp, "humid": timeSeries_value_humid, "time": time_jst}
    return jsonify(res)


# 受け取った温度分布を保存。DB容量を超えている場合は最も古いデータを削除
@app.route("/db/post/distribution/<dt>", methods=["POST"])
def postDist(dt):
    try:
        # JSONデータをリクエストボディから取得
        # 同時にpython用の型（ここではリスト）にデコードされている
        data = request.json
        # リストをjson文字列に変換
        json_data = json.dumps(data)

        # 受け取ったJSONデータを処理
        # ここでdata変数にはJSONデータが格納
        dist = Distribution(date=dt, dist=json_data)
        Session = sessionmaker(bind=engine)
        ses = Session()

        # レコード総数をカウント
        record_count = ses.query(Distribution).count()
        if record_count >= max_db:
            print("レコードを削除します")
            # 削除すべきレコード数
            delete_count = record_count - max_db + 1

            # 古い順に削除するレコードidを取得
            delete_data = ses.query(Distribution.id).order_by(Distribution.id.asc()).limit(delete_count).all()
            for item in delete_data:
                ses.query(Distribution).filter(Distribution.id == item.id).delete()
                ses.commit()

        ses.add(dist)
        ses.commit()
        ses.close()
        return jsonify("ok"), 200

    except Exception as e:
        # エラーが発生した場合の処理
        error_message = str(e)
        return jsonify({"error": error_message}), 400


# 指定された日にデータが保存されているか確認して、保存されている時間をリストで返す
@app.route("/db/distribution/date/<date>", methods=["GET"])
def getDistTime(date):
    try:
        Session = sessionmaker(bind=engine)
        ses = Session()
        res = ses.query(Distribution).filter(Distribution.date.like(f"{date}%")).all()
        ses.close()
        # 取得結果がリスト（複数なのか）どうかを判定する
        if isinstance(res, list):
            res_list = []
            for item in res:
                res_list.append(item.date)
            return jsonify(res_list), 200
        else:
            return jsonify([res.date]), 200

    except Exception as e:
        # エラーが発生した場合の処理
        error_message = str(e)
        return jsonify({"error": error_message}), 400


# 指定された日時の温度分布を返す
@app.route("/db/get/distribution/<datetime>", methods=["GET"])
def getDist(datetime):
    try:
        Session = sessionmaker(bind=engine)
        ses = Session()
        res = ses.query(Distribution).filter(Distribution.date.like(f"{datetime}%")).first()
        ses.close()
        return jsonify(res.dist), 200

    except Exception as e:
        # エラーが発生した場合の処理
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400
    
# 温度/湿度分布を更新する
@app.route("/db/distribution/<room>", methods=["GET"])
def updateDistribution(room):
    # datetimeをdbに保存する際のフォーマット
    s_format = '%Y-%m-%d_%H:%M:%S'

    # 日本時間（JST, UTC+9）のタイムゾーンオブジェクトを作成
    jst = datetime.timezone(
        datetime.timedelta(hours=9)
    )  
    dt_now_jst = datetime.datetime.now(jst)

    try:
        Session = sessionmaker(bind=engine)
        ses = Session()
        latest_req = ses.query(ApiLastRequest).order_by(ApiLastRequest.id.desc()).first()

        time_lag_sec = 999 # 条件分岐を少なくするために大きな値を入れておく
        if latest_req != None:
            latest_req_date = latest_req.date # -> str
            latest_req_date = datetime.datetime.strptime(latest_req_date, s_format ) # -> datetime
            # TZ指定しないとdatetime同士の計算ができない。
            latest_req_date = latest_req_date.replace(tzinfo=jst)

            # 最新のデータとリクエスト時の時間差を計算
            time_lag_sec = (dt_now_jst - latest_req_date).seconds

        if time_lag_sec<REQ_INTERVAL:
            try:
                # 一定時間内なら直近のデータを返す
                latest_data = ses.query(Distribution).order_by(Distribution.id.desc()).first()
                ses.close()   
            except Exception as e:
                print("there is some errors")
                print(e)  

            # tempPredictと出力形式を揃えるためにjsonを一度pythonオブジェクトに戻す
            return jsonify(json.loads(latest_data.dist)), 200
        
        else:
            if room == "House":
                sensor_position = 'ROOM_HOUSE'
                ppm_model_name = 'ppm'
                temp_model_name = 'temp'
                humid_model_name = 'humid'
            elif room == "31A":
                sensor_position = 'ROOM_HOUSE'
                ppm_model_name = 'ppm'
                temp_model_name = 'temp'
                humid_model_name = 'humid'
            elif room == "31B":
                sensor_position = 'ROOM_HOUSE'
                ppm_model_name = 'ppm'
                temp_model_name = 'temp'
                humid_model_name = 'humid'
            elif room == "32A":
                sensor_position = 'ROOM_HOUSE'
                ppm_model_name = 'ppm'
                temp_model_name = 'temp'
                humid_model_name = 'humid'
            elif room == "32B":
                sensor_position = 'ROOM_HOUSE'
                ppm_model_name = 'ppm'
                temp_model_name = 'temp'
                humid_model_name = 'humid'

            #################################################################
            # 四隅の温度センサ値を取得
            #  requests処理
            # url, headers = getHeader()
            # response = requests.get(url,headers=headers)
            try:
                url, headers, payload = getRequest_currentValue()
                response = requests.post(url, headers=headers, json=payload)
                dict_response = response.json()

                # 説明変数として使うセンサのリスト
                sensor_explanatoryVariable = current_app.config[sensor_position]['column_input_sensor']
                # print("column_input_sensor from conf:", sensor_explanatoryVariable)

                # センサーの二酸化炭素データ
                data_ppm = {data["name"]:  data["channel"][0]["value"] for data in dict_response["devices"] if data["name"] in sensor_explanatoryVariable}
                # カラムの順番を揃えてndarrayに変換
                data_ppm = np.array([float(data_ppm[key]) for key in sensor_explanatoryVariable])

                # センサーの温度データ
                data_temp = {data["name"]:  data["channel"][1]["value"] for data in dict_response["devices"] if data["name"] in sensor_explanatoryVariable}
                # カラムの順番を揃えてndarrayに変換
                data_temp = np.array([float(data_temp[key]) for key in sensor_explanatoryVariable])

                # センサーの湿度データ
                data_humid = {data["name"]:  data["channel"][2]["value"] for data in dict_response["devices"] if data["name"] in sensor_explanatoryVariable}
                # カラムの順番を揃えてndarrayに変換
                data_humid = np.array([float(data_humid[key]) for key in sensor_explanatoryVariable])
            except Exception as e:
                print(e)
                print("return latest data")
                try:
                    # 説明変数に文字列'Communication Error'等がある場合は直近のデータを返す
                    latest_data = ses.query(Distribution).order_by(Distribution.id.desc()).first()
                    ses.close()   
                except Exception as e:
                    print("there is some errors")
                    print(e)  
                # tempPredictと出力形式を揃えるためにjsonを一度pythonオブジェクトに戻す
                return jsonify(json.loads(latest_data.dist)), 200
            
            #########################################
            # # デバック用の乱数
            # rng = np.random.default_rng()
            # data_temp = rng.integers(100, size=4)
            # data_humid = rng.integers(100, size=4)
            ################################################################
                
            distribution_temp = predict_distribution(temp_model_name, sensor_position, data_temp) # ->touple(unscaled grid, scaled grid)
            distribution_humid = predict_distribution(humid_model_name, sensor_position, data_humid) # ->touple(unscaled grid, scaled grid)
            distribution_ppm = predict_distribution(ppm_model_name, sensor_position, data_ppm) # ->touple(unscaled grid, scaled grid)

            # apiにリクエストを送信した時間をデータベースに記録
            dt = dt_now_jst.strftime(s_format)
            ALR = ApiLastRequest(date=dt)
            if ses.query(ApiLastRequest).count() >= max_db:
                first_data = ses.query(ApiLastRequest).first()
                ses.delete(first_data)
            ses.add(ALR)
            ses.commit()
            ses.close()

            return jsonify([distribution_temp, distribution_humid, distribution_ppm]), 200 
        #->[[[temp unscaled grid], [temp scaled grid]], [[humid unscaled grid], [humid scaled grid]], [[ppm unscaled grid], [ppm scaled grid]]]
        
    except Exception as e:
        # エラーが発生した場合の処理
        error_message = str(e)
        return jsonify({"error": error_message}), 400
        

