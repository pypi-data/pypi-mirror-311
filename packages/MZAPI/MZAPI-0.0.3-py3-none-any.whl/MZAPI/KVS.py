import hashlib
import json
from datetime import datetime
from threading import Thread

import requests


def generate_log_filename(sdk_name):
    """
    生成日志文件名。

    :param sdk_name: SDK名称。
    :return: 生成的日志文件名和当前时间。
    """
    # 获取当前时间
    now = datetime.now()
    # 格式化时间为 "年-月-日 时：分：秒" 的形式
    formatted_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    json_name = f"{sdk_name}/{formatted_time}.json"
    return json_name, formatted_time


def send_log(sdk_name, json_name, formatted_time):
    """
    发送日志到日志服务器。

    :param sdk_name: SDK名称。
    :param json_name: JSON文件名。
    :param formatted_time: 格式化后的时间
    """
    # 目标URL
    log_url = f"http://xmzsdk.mizhoubaobei.top/MZAPI/{json_name}"
    url = f"http://nodered.glwsq.cn/weixin?to=hwhzrjhbse&body=有人在{formatted_time}使用了接口{sdk_name}，具体日志为{log_url}"
    requests.get(url)


def MD5(json_data):
    json_string = json.dumps(json_data)
    # 计算MD5哈希值
    md5_hash = hashlib.md5(json_string.encode()).hexdigest()
    return md5_hash


class LogHandler:
    def __init__(self):
        """
        初始化LogHandler类。

        """
        self.bucket_name = "xmzsdk"

    def get_ip_location(self):
        """
        获取IP地理位置信息。

        :return: IP地理位置信息的JSON数据。
        """
        url = "https://webapi-pc.meitu.com/common/ip_location"
        response = requests.get(url)
        return response.json()

    def put_content_to_obs(self, log_filename, merged_data):
        url = "https://hwapi.mizhoubaobei.top/rizhi"
        m = {
            "md5": MD5(merged_data),
            "BucketName": "xmzsdk",
            "ObjectKey": f"MZAPI/{log_filename}",
            "json_m": merged_data,
        }
        requests.post(url, json=m)

    def process_log(self, additional_data, sdk_name):
        """
        处理日志，包括获取IP位置信息，合并日志数据，上传到OBS，发送日志通知。

        :param additional_data: 额外的日志数据。
        :param sdk_name: SDK名称。
        """
        log_filename, log_time = generate_log_filename(sdk_name)
        self.put_content_to_obs(log_filename, additional_data)
        send_log(sdk_name, log_filename, log_time)

    def start_process_log(self, additional_data, sdk_name):
        # 使用线程来处理日志
        thread = Thread(target=self.process_log, args=(additional_data, sdk_name))
        thread.start()
