class SensorPosition:
    """
    左上を原点、上から下方向をx軸、左から右方向をy軸とし、各軸の変域が0～1の座標空間におけるセンサー設置座標を定義

    リストの各要素の順番はモデルの入力データのカラム、出力結果のカラムの順番に合わせる必要がある。
    """
    # 小文字が変数名に入っているとconfigに追加されない


    # Home Roomのセンサー設置
    """
    入力カラム：Unit2, Unit3, Unit5, Unit6
    出力カラム：Unit1, Unit4, Unit7
    """
    ROOM_HOUSE = {
        # 説明変数として使うセンサの名前とカラムの順番をリストで定義
        'column_input_sensor':[
            "Unit02", 
            "Unit03", 
            "Unit05", 
            "Unit06"
        ],
        'coordinate_input':[
            # 入力センサーの設置座標をモデルの入力のカラムの順番で定義
            [0, 1],         # UNIT2
            [1, 0],         # UNIT3
            [0, 0],         # UNIT5
            [1, 1],         # UNIT6
        ],
        'coordinate_output':[
            # 出力センサーの設置座標をモデルの出力のカラムの順番で定義
            [0.8, 0.8],     # UNIT1 
            [0.5, 0.2],     # UNIT4 
            [0.2, 0.5]      # UNIT7   
        ]
   }

   


