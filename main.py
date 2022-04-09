import sys
import os
import hashlib
import hmac
import base64
import requests
import time


s = requests.Session()
r = s.post('https://user-api.simplybook.me/'
          ,data="{\"jsonrpc\":\"2.0\",\"method\":\"getLocationsList\",\"params\":[true],\"id\":\"064e4ba7-99cc-4947-ac16-fbd7eaa79996\"}"
          ,headers={
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "ko-KR,ko;q=0.9",
            "content-type": "application/json",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "x-company-login": "episode",
            "x-token": "00e7f6649959e3dac813aae4e254755fb62e23c01bfc9ef5532b0bc8dfb32824"
          })

found = False
for site in r.json()['result']:
    if "성수" in r.json()['result'][site]['name']:
        found = True
 
# TODO: 실서비스에서 제거
#found = True

if found:
    print('빈방이 있다')
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    access_key = "uypTk1cTBz6cvjsVdG0x"				# access key id (from portal or Sub Account)
    secret_key = "IjgnXyf0p4o5n52TiKNr9iPGMEDRxRAFqXVaoCv9"				# secret key (from portal or Sub Account)
    secret_key = bytes(secret_key, 'UTF-8')
    
    method = "POST"
    uri = "/sms/v2/services/ncp:sms:kr:252727944722:sms_noti/messages"

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    
    r = s.post('https://sens.apigw.ntruss.com' + uri
          ,json={
            "type":"SMS",
            "contentType":"COMM",
            "countryCode":"82",
            "from":"01025604692",
            "content":"에피소드 성수에 빈방이 떴다!",
            "messages":[
                {
                    "to":"01025604692",
                },
                {
                    "to":"01048581412",
                }
            ],
        }
         ,headers={
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signingKey
          })
    print(r)
    print(r.status_code)
    print(r.json())
