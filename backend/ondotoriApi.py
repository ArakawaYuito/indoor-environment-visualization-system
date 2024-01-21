"""
ondotoriのwebstrage APIにリクエストする際のrequestを作成
"""
from flask import current_app

def getRequest_prevValue():
    api_key = current_app.config["OT_API_KEY"]
    login_id = current_app.config["OT_LOGIN_ID"]
    login_pass = current_app.config["OT_LOGIN_PASS"]

    #URL指定
    url = "https://api.webstorage.jp/v1/devices/latest-data-rtr500"

    #APIheader作成
    headers = {
        "Host": 'api.webstorage.jp:443',
        "Content-Type": "application/json",
        'X-HTTP-Method-Override':'GET'
    }

    # payload作成
    payload={
        'api-key':api_key,
        'login-id':login_id,
        'login-pass':login_pass,
        'remote-serial':'52C41A95',
        'base-serial':'58580C39'
    }

    return url, headers, payload


def getRequest_currentValue():
    api_key = current_app.config["OT_API_KEY"]
    login_id = current_app.config["OT_LOGIN_ID"]
    login_pass = current_app.config["OT_LOGIN_PASS"]

    #URL指定
    url = "https://api.webstorage.jp/v1/devices/current"

    #APIheader作成
    headers = {
        "Host": 'api.webstorage.jp:443',
        "Content-Type": "application/json",
        'X-HTTP-Method-Override':'GET'
    }

    # payload作成
    payload={
        'api-key':api_key,
        'login-id':login_id,
        'login-pass':login_pass,
    }

    return url, headers, payload
