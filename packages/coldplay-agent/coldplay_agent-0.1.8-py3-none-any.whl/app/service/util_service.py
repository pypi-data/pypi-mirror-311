import configparser
from datetime import datetime, timezone
from functools import partial
import json
import os
from typing import List, Optional
import numpy as np
import requests
from smb.SMBConnection import SMBConnection
import torch
import torch.onnx
import mros
import mros.controller_msgs.msg.JointState
import mros.controller_msgs.msg.JointCmd
import mros.controller_msgs.msg.IMUData
import time
from influxdb_client import InfluxDBClient, Point, WriteOptions

# 从环境变量中读取 SMB 服务器配置信息
SERVER_NAME = os.getenv("SMB_SERVER_NAME")
SHARE_NAME = os.getenv("SMB_SHARE_NAME")
USERNAME = os.getenv("SMB_USERNAME")
PASSWORD = os.getenv("SMB_PASSWORD")
 
class UtilService:
    def load_coldplay_config():
        config_dest = os.path.expanduser('~/.coldplay_config.ini')
        
        if not os.path.exists(config_dest):
            print("Config file not found. Please run coldplayagent-init first.")
            return None
        
        coldplay_config = configparser.ConfigParser()
        coldplay_config.read(config_dest)
        return coldplay_config
    

    # 从环境变量中读取 SMB 服务器配置信息
    SERVER_NAME = "192.168.2.66"
    SHARE_NAME = "software"
    USERNAME = "jenkins"
    PASSWORD = "jenkins#123"

    def list_files(directory_path: str) -> List[str]:
        conn=SMBConnection(USERNAME,PASSWORD,"","",use_ntlm_v2 = True, is_direct_tcp=True)
        result = conn.connect(SERVER_NAME, 445, timeout=60*10) #smb协议默认端口445
        print(f"连接smb成功 {result}")
        files = conn.listPath(SHARE_NAME, f"/{directory_path}")
        file_list = [file.filename for file in files if file.filename not in [".", ".."]]
        
        return file_list

    def download_file(remote_path, local_path):
        conn=SMBConnection(USERNAME,PASSWORD,"","",use_ntlm_v2 = True, is_direct_tcp=True)
        result = conn.connect(SERVER_NAME, 445, timeout=60*10) #smb协议默认端口445
        print(f"连接smb成功 {result}")
        """下载文件"""
        
        with open(local_path, 'wb') as f:
            conn.retrieveFile(SHARE_NAME, remote_path, f)

        conn.close()

        return local_path
    
    def export_policy_as_onnx(model_path, onnx_model_path):
        try:
            # 1. 加载 PyTorch 模型
            # model_path = "your_model.pt"  # 替换为你的模型路径
            # model = torch.load(model_path)
            # loaded_dict = torch.load(model_path)
            model = torch.load(model_path, map_location=torch.device('cpu'))
            # state_dict = torch.load("your_model.pt", map_location=torch.device('cpu'))
            # model.load_state_dict(state_dict)  # 加载参数
            model.eval()  # 切换到评估模式

            # 2. 定义输入张量
            # 假设模型输入是一个形状为 (batch_size, channels, height, width) 的张量
            dummy_input = torch.randn(0, 0, 0, 0)  # 根据实际情况修改

            # 3. 导出为 ONNX 格式
            input_names = ["nn_input"]
            output_names = ["nn_output"]
            # onnx_model_path = "your_model.onnx"
            torch.onnx.export(
                model,                  # 要导出的模型
                dummy_input,            # 模拟输入张量
                onnx_model_path,        # 导出文件名
                verbose=True,
                input_names=input_names,  # 输入节点名称
                output_names=output_names,  # 输出节点名称
                export_params=True,     # 导出模型参数
                opset_version=13,       # ONNX opset 版本 (一般为 11 或更高)
            )
        
        except Exception as e:
            print(f"模型转化失败: {e}")

        print("Exported policy as onnx script to: ", onnx_model_path)

    def download_http_file(file_url, local_file_path):
        # MinIO 文件的完整下载地址
        # file_url = "http://your-minio-server.com/your-bucket-name/path/to/file.txt"

        # 本地保存路径
        # local_file_path = "downloads/file.txt"

        # 确保本地目录存在
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # 下载文件
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # 检查是否有 HTTP 错误

            with open(local_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"文件已保存到本地：{local_file_path}")
        except requests.RequestException as e:
            print(f"下载失败：{e}")
            
    
    def py_subscriber(task_id, stop_event):
        # Initialize the MROS system with the name "PyExampleSubscriber"
        mros.init("PyExampleSubscriber")

        time.sleep(3)

        # print(f"TASK_ID:{task_id}")
        print(f"pub list: {str(mros.getPublishedTopics())}")

        # Choose between spinning or manual message reading
        # Create a subscriber for the topic "controller_msgs" with message type JointState
        # and set the callback function to subscriber_cb
        # subscriber_robot_state_point_foot = mros.subscribe("/RobotStatePointFoot", mros.controller_msgs.msg.JointState, partial(UtilService.subscriber_robot_state_point_foot, task_id=task_id))
        # subscriber_imu_data = mros.subscribe("/ImuData", mros.controller_msgs.msg.IMUData, partial(UtilService.subscriber_imu_data, task_id=task_id))
        # subscriber_robot_cmd_point_foot = mros.subscribe("/RobotCmdPointFoot", mros.controller_msgs.msg.JointCmd, partial(UtilService.subscriber_robot_cmd_point_foot, task_id=task_id))

        # Create a subscriber for the topic "mros_hello" with message type MROSHello
        # but without a callback function

        subscriber_robot_state_point_foot = mros.subscribe("/RobotStatePointFoot", mros.controller_msgs.msg.JointState, None)
        subscriber_imu_data = mros.subscribe("/ImuData", mros.controller_msgs.msg.IMUData, None)
        subscriber_robot_cmd_point_foot = mros.subscribe("/RobotCmdPointFoot", mros.controller_msgs.msg.JointCmd, None)

        # Create a Rate object to control the frequency of the loop (100 Hz)
        rate = mros.Rate(100)

        print("Subscriber started...")
        while not stop_event.is_set():
            # Read the latest message from the subscriber in real-time
            robot_state_point_foot_received_msg = subscriber_robot_state_point_foot.readMsgRT()
            subscriber_imu_data_received_msg = subscriber_imu_data.readMsgRT()
            subscriber_robot_cmd_point_foot_received_msg = subscriber_robot_cmd_point_foot.readMsgRT()

            # Check if a message was received
            if robot_state_point_foot_received_msg != None:
                UtilService.subscriber_robot_state_point_foot(robot_state_point_foot_received_msg, task_id)
            if subscriber_imu_data_received_msg != None:
                UtilService.subscriber_imu_data(subscriber_imu_data_received_msg, task_id)
            if subscriber_robot_cmd_point_foot_received_msg != None:
                UtilService.subscriber_robot_cmd_point_foot(subscriber_robot_cmd_point_foot_received_msg, task_id)

            # Sleep for the specified rate duration to maintain the loop frequency
            rate.sleep()

        # print('%s' % str(subscriber))
        # 使用循环监听消息，支持停止事件
        # print("Subscriber started...")
        # while not stop_event.is_set():  # 如果 stop_event 未触发，继续运行
        #     time.sleep(1)  # 避免过高的 CPU 占用

        print("Stop event received. Shutting down subscriber...")
        # 清理资源
        # mros.shutdown()  # 关闭 MROS 系统
        print("Subscriber stopped.")


    # Callback function that will be called when a new message is received
    def subscriber_robot_state_point_foot(received_msg, task_id):
        # Print the 'hello' field from the received message
        # 查看所有属性
        # print(dir(received_msg))
        # print(type(received_msg))
        # 将消息序列化为字节流
        # serialized = received_msg.serialize()

        # 如果需要可以用 received_msg.deserialize(serialized) 反序列化
        # print(f"Serialized message: {serialized}")

        # 遍历属性并获取值
        
        # print(f"task_id:{task_id}")
        msg_data = UtilService.ros_msg_to_dict(received_msg)
        # attributes = {attr: getattr(received_msg, attr) for attr in dir(received_msg) if not attr.startswith("__")}
        # print('%s' % str(msg_data))
        db_client = UtilService.get_influxdb_client()
        # 使用同步写入模式
        # write_api = db_client.write_api(write_options="asynchronous")
        # 创建写入选项，设置为异步写入
        write_options = WriteOptions(batch_size=1000, flush_interval=10000, write_type="asynchronous")

        # 创建写入 API
        write_api = db_client.write_api(write_options=write_options)

        org = "limx"               # 替换为你的组织名称
        bucket = "coldplay"         # 替换为你的存储桶名称
        # 创建一个数据点
        # print(json.dumps(msg_data))
        # 提取时间 
        # sec = msg_data['header']['stamp']['sec'] 
        # nsec = msg_data['header']['stamp']['nsec']
        # 转换为纳秒级 Unix 时间戳 
        # timestamp_ns = sec * 1_000_000_000 + nsec
        # current_time = datetime.now(timezone.utc).replace(microsecond=int(time.time() * 1e6 % 1e6))
        point = Point("RobotStatePointFoot") \
            .tag("task_id", task_id) \
            .field("value", json.dumps(msg_data))
            # .time(current_time)

        # 将数据点写入到指定的存储桶
        write_api.write(bucket=bucket, org=org, record=point)
        print("Data written successfully!")
        pass

    # Callback function that will be called when a new message is received
    def subscriber_imu_data(received_msg, task_id):
        # Print the 'hello' field from the received message
        # 查看所有属性
        # print(dir(received_msg))
        # print(type(received_msg))
        # 将消息序列化为字节流
        # serialized = received_msg.serialize()

        # 如果需要可以用 received_msg.deserialize(serialized) 反序列化
        # print(f"Serialized message: {serialized}")

        # 遍历属性并获取值
        
        # print(f"task_id:{task_id}")
        msg_data = UtilService.ros_msg_to_dict(received_msg)
        # attributes = {attr: getattr(received_msg, attr) for attr in dir(received_msg) if not attr.startswith("__")}
        # print('%s' % str(msg_data))
        db_client = UtilService.get_influxdb_client()
        # 使用同步写入模式
        # write_api = db_client.write_api(write_options="asynchronous")
        # 创建写入选项，设置为异步写入
        write_options = WriteOptions(batch_size=1000, flush_interval=10000, write_type="asynchronous")

        # 创建写入 API
        write_api = db_client.write_api(write_options=write_options)

        org = "limx"               # 替换为你的组织名称
        bucket = "coldplay"         # 替换为你的存储桶名称
        # 创建一个数据点
        # print(json.dumps(msg_data))
        point = Point("ImuData") \
            .tag("task_id", task_id) \
            .field("value", json.dumps(msg_data))

        # 将数据点写入到指定的存储桶
        write_api.write(bucket=bucket, org=org, record=point)
        print("Data written successfully!")
        pass

    # Callback function that will be called when a new message is received
    def subscriber_robot_cmd_point_foot(received_msg, task_id):
        # Print the 'hello' field from the received message
        # 查看所有属性
        # print(dir(received_msg))
        # print(type(received_msg))
        # 将消息序列化为字节流
        # serialized = received_msg.serialize()

        # 如果需要可以用 received_msg.deserialize(serialized) 反序列化
        # print(f"Serialized message: {serialized}")

        # 遍历属性并获取值
        
        # print(f"task_id:{task_id}")
        msg_data = UtilService.ros_msg_to_dict(received_msg)
        # attributes = {attr: getattr(received_msg, attr) for attr in dir(received_msg) if not attr.startswith("__")}
        # print('%s' % str(msg_data))
        db_client = UtilService.get_influxdb_client()
        # 使用同步写入模式
        # write_api = db_client.write_api(write_options="asynchronous")
        # 创建写入选项，设置为异步写入
        write_options = WriteOptions(batch_size=1000, flush_interval=10000, write_type="asynchronous")

        # 创建写入 API
        write_api = db_client.write_api(write_options=write_options)

        org = "limx"               # 替换为你的组织名称
        bucket = "coldplay"         # 替换为你的存储桶名称
        # 创建一个数据点
        # print(json.dumps(msg_data))
        point = Point("RobotCmdPointFoot") \
            .tag("task_id", task_id) \
            .field("value", json.dumps(msg_data))

        # 将数据点写入到指定的存储桶
        write_api.write(bucket=bucket, org=org, record=point)
        print("Data written successfully!")
        pass

    # def ros_msg_to_dict(msg):
    #     """
    #     递归解析 ROS 消息对象，将其转换为字典。
    #     """
    #     if hasattr(msg, "__slots__"):
    #         # 递归解析 __slots__ 中的字段
    #         return {
    #             slot: UtilService.ros_msg_to_dict(getattr(msg, slot))
    #             for slot in msg.__slots__
    #         }
    #     elif isinstance(msg, (list, tuple)):  
    #         # 如果是列表或元组，递归解析每个元素
    #         return [UtilService.ros_msg_to_dict(item) for item in msg]
    #     elif isinstance(msg, dict):  
    #         # 如果是字典，递归解析键值对
    #         return {key: UtilService.ros_msg_to_dict(value) for key, value in msg.items()}
    #     else:
    #         # 对于其他类型（如基本数据类型），直接返回值
    #         return msg
    def ros_msg_to_dict(msg):
        """
        递归解析 ROS 消息对象，将其转换为字典，并将 numpy.array 转换为普通列表。
        """
        if hasattr(msg, "__slots__"):
            # 递归解析 __slots__ 中的字段
            return {
                slot: UtilService.ros_msg_to_dict(getattr(msg, slot))
                for slot in msg.__slots__
            }
        elif isinstance(msg, (list, tuple)):  
            # 如果是列表或元组，递归解析每个元素
            return [UtilService.ros_msg_to_dict(item) for item in msg]
        elif isinstance(msg, dict):  
            # 如果是字典，递归解析键值对
            return {key: UtilService.ros_msg_to_dict(value) for key, value in msg.items()}
        elif isinstance(msg, np.ndarray):
            # 如果是 numpy.array，转换为列表
            return msg.tolist()
        else:
            # 对于其他类型（如基本数据类型），直接返回值
            return msg


    def get_influxdb_client():
        # 配置 InfluxDB 连接信息
        url = "http://10.0.10.13:8086"  # 替换为你的 InfluxDB 地址
        token = "YRdvbmXgbac5sHx6ZHer4yo9WTTGe8elkRoneCA23B4inLT7vmYje6uvN8BkhWQNGCu0A_Tb2D25W9bJfljtkg=="           # 替换为你的 InfluxDB Token
        org = "limx"               # 替换为你的组织名称
        bucket = "coldplay"         # 替换为你的存储桶名称

        # 初始化 InfluxDB 客户端
        client = InfluxDBClient(url=url, token=token, org=org)
        return client
