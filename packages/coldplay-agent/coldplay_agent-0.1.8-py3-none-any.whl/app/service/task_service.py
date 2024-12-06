# app/service/task_service.py

import json
import os
import re
import shlex
import subprocess
import threading
import time
from urllib.parse import quote, urlparse, urlunparse
from app.service.curl_service import CurlService
from app.service.thread_manage import ThreadManager
from app.service.util_service import UtilService
from pathlib import Path

thread_manager = ThreadManager()
class TaskService:
    @staticmethod
    def task_run(data):
        """
        处理任务运行逻辑
        """
        print(f"data: {data}")  # 打印传入的数据，便于调试
        
        #回传状态数据
        CurlService.update_task_status(data['task_id'],"3")
        # 执行脚本文件
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        task_type = data['task_type'] 
        match task_type:
            case '1':#仿真训练模式
                code_type = data['code_type']
                conda_env = data['conda_env']
                version_type = data['version_type']
                version_name = data['version_name']
                run_params = data['run_params']  # 获取脚本的运行参数
                match code_type: 
                    case '1':#上传文件方式
                        # 构建项目URL
                        project_url = data['code_url']
                        project_file_uri = data['code_file_uri'] 
                        task_id = data['task_id']
                        urdf_path = data['urdf_path']
                        hparams_path = data['hparams_path']
                        hp_down_fileurl = data['hp_down_fileurl']
                        hp_file_name = data['hp_file_name']
                        
                        
                        # 获取脚本的执行URL和脚本名称
                        script_run_url = data['script_run_url']  # 获取脚本的运行URL
                        script_name = data['script_name']  # 获取脚本的名称
                        
                        # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
                        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
                        
                        print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")  # 打印项目URL和脚本URL，便于调试
                        
                        # 使用shlex.quote来安全处理字符串，避免命令注入
                        # project_url = shlex.quote(project_url)  
                        script_run_url_new = shlex.quote(script_run_url_new)

                        # 获取当前文件的绝对路径
                        current_file = Path(__file__).resolve()  
                        
                        # 获取项目根目录的app目录，假设项目目录在当前文件的上级目录
                        project_app_root = current_file.parent.parent  
                        
                        # 使用subprocess.Popen 让命令在后台执行，避免阻塞主线程
                        # 使用subprocess.Popen执行shell脚本，传入项目URL和脚本运行的URL作为参数
                        # process = subprocess.Popen(["bash", f"{project_app_root}/scripts/run_task.sh", project_url, script_run_url_new, project_file_uri, task_id, code_type, version_type, version_name, run_params, conda_env]) 
                        config = {
                            "project_url": project_url,
                            "script_run_url_new": script_run_url_new,
                            "project_file_uri": project_file_uri,
                            "task_id": task_id,
                            "code_type": code_type,
                            "version_type": version_type,
                            "version_name": version_name,
                            "run_params": run_params,
                            "conda_env": conda_env,
                            "hparams_path": hparams_path,
                            "hp_down_fileurl": hp_down_fileurl,
                            "hp_file_name": hp_file_name
                        }

                        params_config = os.path.expanduser('~/.run_params_config.json')
                        print(f"params_config:{params_config}")
                        with open(params_config, "w") as f:
                            json.dump(config, f)
                        process = subprocess.Popen(["bash",  f"{project_app_root}/scripts/run_task.sh", params_config])
                    case '2':#git方式
                        # 构建项目URL
                        project_url = data['code_url']
                        git_source = TaskService.check_git_source(project_url)
                        project_file_uri = data['code_file_uri'] 
                        task_id = data['task_id']
                        print(f"project_url:{project_url}")  # 打印项目URL和脚本URL，便于调试
                        # 使用正则表达式从完整URL中提取REPO_URL部分
                        repo_url = re.sub(r"https://", "", project_url)
                        if data['is_open'] == "2":
                            match git_source:
                                case 'GitHub':
                                    project_url = f"https://{data['github_name']}:{data['github_token']}@{repo_url}"
                                case 'GitLab':
                                    project_url = f"https://{data['gitlab_name']}:{data['gitlab_token']}@{repo_url}"
                                case 'Unknown':
                                    project_url = f"https://{data['gitlab_name']}:{data['gitlab_token']}@{repo_url}"
                        else:
                            project_url = f"https://{repo_url}"

                        
                        # 获取脚本的执行URL和脚本名称
                        script_run_url = data['script_run_url']  # 获取脚本的运行URL
                        script_name = data['script_name']  # 获取脚本的名称
                        
                        # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
                        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
                        
                        print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")  # 打印项目URL和脚本URL，便于调试
                        
                        # 使用shlex.quote来安全处理字符串，避免命令注入
                        # project_url = shlex.quote(project_url)  
                        script_run_url_new = shlex.quote(script_run_url_new)

                        # 获取当前文件的绝对路径
                        current_file = Path(__file__).resolve()  
                        
                        # 获取项目根目录的app目录，假设项目目录在当前文件的上级目录
                        project_app_root = current_file.parent.parent  
                        
                        # 使用subprocess.Popen 让命令在后台执行，避免阻塞主线程
                        # 使用subprocess.Popen执行shell脚本，传入项目URL和脚本运行的URL作为参数
                        process = subprocess.Popen(["bash", f"{project_app_root}/scripts/run_task.sh", project_url, script_run_url_new, project_file_uri, task_id, code_type, version_type, version_name, run_params, conda_env])  
        
            case '2':#仿真验证模式
                task_id = data['task_id']
                verify_code_type = data['verify_code_type']#仿真验证代码方式 0 官方示例， 1 本地上传， 2 部署版本
                operating_verify_env = data['operating_verify_env']#仿真验证环境 1 gazebo ， 2 MuJoCo
                robot_type = data['robot_type']
                visual_tools = data['visual_tools']
                code_file_uri = data['code_file_uri']
                code_url = data['code_url']
                start_script = data['start_script']
                policy_source = data['policy_source']
                police_info = data['police_info']
                police_local_path = str(Path.home() / "coldplay/limx_ws/police")
                # 遍历处理police_info
                if police_info:
                    for item in police_info:
                        policyUri = item['policyUri']
                        policyUriReal = urlparse(policyUri)
                        policyName = policyUriReal.path.split("/")[-1]
                        policyNameWithoutExt, policyNameExt = os.path.splitext(policyName)
                        # 下载policy文件
                        localfile_path = f"{police_local_path}/{policyName}"
                        UtilService.download_http_file(policyUri,localfile_path)
                        #onnx转化 涉及到非标准的网络模型，本期不做转化
                        # if policyNameExt == ".pt":
                        #     onnxModelPath = f"{police_local_path}/{policyNameWithoutExt}.onnx"
                        #     UtilService.export_policy_as_onnx(localfile_path,onnxModelPath)
                        
                police_info = json.dumps(police_info)

                #如果是代码是部署版本，则下载smb的部署文件
                # if verify_code_type == '2':
                #     file_path = code_url
                #     # 设置 rgz_path 为 $HOME 下的 coldplay/limx_ws 目录
                #     rgz_path = str(Path.home() / "coldplay/limx_ws")
                    
                #     # 确保目录存在，如果不存在则创建
                #     Path(rgz_path).mkdir(parents=True, exist_ok=True) 
                    # file_rgz = UtilService.download_file(file_path, rgz_path)

                # 获取当前文件的绝对路径
                current_file = Path(__file__).resolve()  
                
                # 获取项目根目录的app目录，假设项目目录在当前文件的上级目录
                project_app_root = current_file.parent.parent  
                print(f"police_info：{police_info}")  # 打印执行成功的消息
                
                process = subprocess.Popen(["bash", f"{project_app_root}/scripts/run_verify_task.sh", task_id, verify_code_type, code_url, start_script, policy_source, operating_verify_env, robot_type, visual_tools, police_info])
                
                # 等待子进程完成
                process.wait()
                # 如果任务需要订阅线程,使用多线程启动订阅
                stop_event = threading.Event()
                subscriber_thread = threading.Thread(target=UtilService.py_subscriber, args=(task_id, stop_event))
                subscriber_thread.daemon = True # 主线程退出时自动结束
                subscriber_thread.start()

                # 注册线程到管理器
                thread_manager.add_thread(task_id, subscriber_thread, stop_event)


        print(f"执行成功")  # 打印执行成功的消息
        
        return True  # 返回True表示任务执行成功
    
    @staticmethod
    def check_git_source(repo_url):
        if "github.com" in repo_url:
            return "GitHub"
        elif "gitlab.com" in repo_url:
            return "GitLab"
        else:
            return "Unknown"
    
    @staticmethod
    def task_stop(data):
        """
        处理任务终止逻辑
        """
        print(f"stop run")

        task_type = data['task_type'] 
        task_id = data['task_id']
        # 执行脚本文件
        # 使用 subprocess.Popen 让命令在后台执行
        # 获取当前文件所在路径
        current_file = Path(__file__).resolve()
        # 获取项目根目录app目录
        project_app_root = current_file.parent.parent  # 假设项目目录在上级
        match task_type:
            case '1':#仿真训练模式

                # 获取脚本的执行URL和脚本名称
                script_run_url = data['script_run_url']  # 获取脚本的运行URL
                script_name = data['script_name']  # 获取脚本的名称
                run_params = data['run_params'] 
                
                # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
                script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
                subprocess.Popen(["bash", f"{project_app_root}/scripts/stop_task.sh", script_run_url_new, task_id, run_params])

            case '2':#仿真验证模式
                verify_code_type = data['verify_code_type']
                operating_verify_env = data['operating_verify_env']
                robot_type = data['robot_type']
                visual_tools = data['visual_tools']
                code_file_uri = data['code_file_uri']
                code_url = data['code_url']
                start_script = data['start_script']
                policy_source = data['policy_source']
                subprocess.Popen(["bash", f"{project_app_root}/scripts/stop_verify_task.sh", task_id, operating_verify_env, verify_code_type])

        # 停止订阅线程
        if thread_manager.has_thread(task_id):
            print(f"停止订阅线程{task_id}")
            thread_manager.stop_thread(task_id)

        #回传状态数据
        CurlService.update_task_status(data['task_id'],'6')
        print(f"执行成功")

        return True
    

    @staticmethod
    def task_pause(data):
        """
        处理任务暂停逻辑
        """
        print(f"pause run")
        # 执行脚本文件
        # 使用 subprocess.Popen 让命令在后台执行
        # 获取当前文件所在路径
        current_file = Path(__file__).resolve()

        # 获取脚本的执行URL和脚本名称
        script_run_url = data['script_run_url']  # 获取脚本的运行URL
        script_name = data['script_name']  # 获取脚本的名称
        task_id = data['task_id']
        run_params = data['run_params'] 
        
        # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
        # 获取项目根目录app目录
        project_app_root = current_file.parent.parent  # 假设项目目录在上级
        subprocess.Popen(["bash", f"{project_app_root}/scripts/stop_task.sh", script_run_url_new, task_id, run_params])
        #回传状态数据
        CurlService.update_task_status(data['task_id'],'4')
        print(f"执行成功")

        return True
    
    @staticmethod
    def task_restart(data):
        """
        处理任务继续运行逻辑
        """
        print(f"data: {data}")  # 打印传入的数据，便于调试
        
        # 执行脚本文件
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        load_run = data['load_run']
        checkpoint = data['checkpoint']
        conda_env = data['conda_env']

        # 构建项目URL
        project_url = data['code_url']
        task_id = data['task_id']
        
        
        # 获取脚本的执行URL和脚本名称
        script_run_url = data['script_run_url']  # 获取脚本的运行URL
        script_name = data['script_name']  # 获取脚本的名称
        
        # 构建完整的脚本运行URL，去掉多余的斜杠并拼接脚本名称
        script_run_url_new = f"{script_run_url.strip('/')}/{script_name}"
        
        print(f"project_url:{project_url} script_run_url_new:{script_run_url_new}")  # 打印项目URL和脚本URL，便于调试
        
        # 使用shlex.quote来安全处理字符串，避免命令注入
        # project_url = shlex.quote(project_url)  
        script_run_url_new = shlex.quote(script_run_url_new)

        # 获取当前文件的绝对路径
        current_file = Path(__file__).resolve()  
        
        # 获取项目根目录的app目录，假设项目目录在当前文件的上级目录
        project_app_root = current_file.parent.parent  
        
        # 使用subprocess.Popen 让命令在后台执行，避免阻塞主线程
        # 使用subprocess.Popen执行shell脚本，传入项目URL和脚本运行的URL作为参数
        process = subprocess.Popen(["bash", f"{project_app_root}/scripts/rerun_task.sh", script_run_url_new, task_id, load_run, checkpoint, conda_env]) 
           
        #回传状态数据
        CurlService.update_task_status(data['task_id'],"3")
        
        print(f"执行成功")  # 打印执行成功的消息
        
        return True  # 返回True表示任务执行成功
    