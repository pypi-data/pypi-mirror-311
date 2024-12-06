# 创建一个全局线程管理器
from threading import Lock

class ThreadManager:
    _threads = {}
    _lock = Lock()

    @classmethod
    def add_thread(cls, task_id, thread, stop_event):
        with cls._lock:
            cls._threads[task_id] = (thread, stop_event)

    @classmethod
    def stop_thread(cls, task_id):
        with cls._lock:
            if task_id in cls._threads:
                thread, stop_event = cls._threads.pop(task_id)
                stop_event.set()  # 通知线程停止
                thread.join()  # 等待线程退出
                print(f"Thread for task_id={task_id} stopped successfully.")

    @classmethod
    def has_thread(cls, task_id):
        with cls._lock:
            return task_id in cls._threads
