import copy
import subprocess
import time
import redis
import requests
from airtest.core.android import Android
from contextlib import contextmanager
import functools


class SonicApi:
    def __init__(self, host, user_name, password, redis_connection):
        self.redis = redis.from_url(redis_connection)
        self.host, self.user_name, self.password = host, user_name, password
        self.session = requests.session()

    @property
    def check_token(self):
        sonic_token = self.redis.get("sonic_token")
        return {"SonicToken": sonic_token} if sonic_token else self.get_token()

    def get_token(self):
        url = f"{self.host}/server/api/controller/users/login"
        json = {
            "userName": self.user_name,
            "password": self.password
        }
        try:
            res = self.session.post(url, json=json)
            self.check_response(res)
            sonic_token = res.json()["data"]
        except Exception as e:
            raise Exception("登录接口报错") from e
        else:
            self.redis.set("sonic_token", sonic_token)
            self.redis.expire("sonic_token", 60 * 60 * 24 - 10)
            return {"SonicToken": sonic_token}

    def get_all_devices(self, payload):
        url = f"{self.host}/server/api/controller/devices/list"
        res = self.session.get(url, params=payload, headers=self.check_token)
        self.check_response(res)
        return res.json().get('data').get('content')

    def occupy_device(self, udid):
        url = f"{self.host}/server/api/controller/devices/occupy"
        json = {
            "udId": udid,
            "sasRemotePort": 30000,
            "uia2RemotePort": 30001,
            "sibRemotePort": 30002,
            "wdaServerRemotePort": 30003,
            "wdaMjpegRemotePort": 30004
        }
        res = self.session.post(url, headers=self.check_token, json=json)
        self.check_response(res)
        return res.json().get('data')

    def release_device(self, udid):
        url = f"{self.host}/server/api/controller/devices/release"
        params = {
            "udId": udid
        }
        res = self.session.get(url, headers=self.check_token, params=params)
        self.check_response(res)
        return res.json()

    @staticmethod
    def check_response(response):
        """检查响应的通用方法"""
        if response.status_code != 200:
            raise Exception(f"请求失败，HTTP 状态码: {response.status_code}")
        if response.json().get('code') != 2000:
            raise Exception(f"请求失败，响应码: {response.json().get('code')}, 信息: {response.json().get('message')}")

    @contextmanager
    def device_session(self, udid):
        devices = self.get_all_devices({'page': 1, 'pageSize': 100})
        online_devices = {item.get('udId'): item.get('status') for item in devices}

        if udid not in online_devices or online_devices[udid] != 'ONLINE':
            raise ("设备不在线或不存在。")
            # raise RuntimeError("generator didn't yield")
            return

        try:
            print(f'开始连接设备:{udid}')
            subprocess.run(["adb", "start-server"], check=True)
            time.sleep(3)
            remote = self.occupy_device(udid).get('sas')
            yield remote
        finally:
            print(f'开始释放设备：{udid}')
            time.sleep(3)
            subprocess.run(["adb", "kill-server"], check=True)
            self.release_device(udid)


def with_device_session(sonic_instance, udid):
    def decorator(test_func):
        @functools.wraps(test_func)
        def wrapper(*args, **kwargs):
            with sonic_instance.device_session(udid) as remote:
                if remote:
                    return test_func(remote, *args, **kwargs)

        return wrapper

    return decorator


def airtest_plan(remote):
    remote_copy = copy.deepcopy(remote)
    remote_copy = remote_copy.replace('adb connect', '').strip()

    device = None
    try:
        print(f"开始连接设备: {remote_copy}")
        device = Android(remote_copy)
        apps = device.list_app(third_only=False)
        for app in apps:
            print(app)
    except Exception as e:
        print(f"连接设备时出错: {e}")
    finally:
        if device:
            device.disconnect()  # 假设有 disconnect 方法可用
        print(f"开始释放设备：{remote_copy}")
