import os
from pathlib import Path
import random, string
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()


def randomname(n):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


secret_key = randomname(8).encode()


class Config:
    # 小文字が変数名に入っているとconfigに追加されない

    # TESTING = False
    #  DEBUG = False
    SECRET_KEY = secret_key

    # ondotori用の設定値
    OT_API_KEY = os.environ.get("OT_API_KEY")
    OT_LOGIN_ID = os.environ.get("OT_LOGIN_ID")
    OT_LOGIN_PASS = os.environ.get("OT_LOGIN_PASS")