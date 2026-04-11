import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


def trans_cookies(cookies_str):
    cookies = dict()
    for i in cookies_str.split("; "):
        try:
            cookies[i.split('=')[0]] = '='.join(i.split('=')[1:])
        except:
            continue
    return cookies


def aes_decrypt(data: str, key: str) -> str:
    data = base64.b64decode(data)
    key = key.encode()
    iv = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    res = cipher.decrypt(data)
    res = unpad(res, AES.block_size)
    res = base64.b64decode(res).decode()
    return res

if __name__ == '__main__':
    main_url = 'yJfFUDy4CHSX3wIl576u87pKCQECev/dH+4fi2kklDtez28sSlMqrJEdAGZwkuQCiJdWugMghMYA/HBqsTmisDaiMNOoTUhSCb2LMaGOiqBeNq4wlEMKA3YiQVgUw/BBxCgEWt6ESuxwxyEUFpugAZk97f9dSZXlQsZ9T9PvDQpLnM4vshOnJyInHUJfPHjTR4ZB59VUpwzRESJS1GFEwQusyHZdXETXQTk95WZtetYED1uINfOzMuYZrxDKUV9GlzQxBZXpmIof4cz152JUmwDTWjNSe5TK/kP23O2PD3JX391tyCYx9YdNhLhK26r9x7KxMRVHVESgyMws+Z1XWsTKX6Gy0HTS0GlnpmSonXalA6qbnayYINVeEaGDNWt2ayz3Dd6c6IST8J6OASzJcL2Yab1gT/ubZQ1OR1cW0xRzAwvEkOxtMCOwjsAsGthiq/x8NSOpZ/oBjtHfl2BTRSnpVc47PgP9TvK/vonmZT4bsbFxazAwZJiWomaqKxlEGe+g5XHc1bhSsCtdSrztug=='
    ptk = "683b256f172b46ce88d7f14195f9eaf7"
    print(aes_decrypt(main_url, ptk))