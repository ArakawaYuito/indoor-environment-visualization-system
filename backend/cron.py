# 定期実行でDBに分布を保存する

import datetime
import requests

def get_current_time_formatted():
    # 現在の時刻を取得
    now = datetime.datetime.now()
    # 指定されたフォーマットに変換
    formatted_time = now.strftime('%Y-%m-%d_%H:%M:%S')
    
    return formatted_time

""" 分布の更新 """
url = "https://arakawabase.com/api/db/distribution/House"
res_dist = requests.get(url)


""" 受け取った分布をDBにPOST """
current = get_current_time_formatted()
url = f"https://arakawabase.com/api/db/post/distribution/{current}"
# POSTリクエストを送信
response = requests.post(url, json=res_dist.json())