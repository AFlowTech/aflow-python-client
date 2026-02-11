import os

from aflow_client_python import ASignature
from dotenv import load_dotenv
import requests
import json

load_dotenv(".env")

sig_generator = ASignature()
base_url = os.getenv("AIFLOW_DOMAIN", "")


def sync_department():
    url = f"{base_url}/aflow/api/sys/sync/department"
    payload = {"departments": [
        dict(
            deptId="0",
            deptName="根部门",
            orderNum=1,
            status=1,
        ),
        dict(
            deptId="1",
            deptName="第二个跟部门",
            orderNum=2,
            status=1,
        ),
    ]}

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


def sync_user():
    url = f"{base_url}/aflow/api/sys/sync/user"
    payload = {
      "users": [
        {
          "userId": "11000011111",
          "userName": "张三",
          "realName": "张三",
          "email": "zhangsan@a.com",
          "mobile": "18888888888",
          "deptId": "0",
          "personnelType": 1,
          "directSupervisor": "",
          "status": 1
        }
      ]
    }

    print(json.dumps(payload, ensure_ascii=False))
    headers = {
        "Content-Type": "application/json",
        # 注意，这里对payload dump的时候，不要使用 ensure_ascii=False！
        # 如果appId等变量已经注入到系统变量中，则可以只提供请求体
        "X-A-Signature": sig_generator.create_signature(json.dumps(payload)),
    }

    try:
        print(url)
        ret = requests.post(url, json=payload, headers=headers)
        if ret.status_code == 200:
            return ret.json()
        else:
            print(ret.text)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # print(os.getenv("APP_ID"))
    # print(sync_department())
    print(sync_user())
