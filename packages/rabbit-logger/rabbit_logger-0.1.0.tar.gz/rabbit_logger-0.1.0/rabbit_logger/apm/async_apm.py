import datetime
import functools
import inspect
import json
import time
from uuid import uuid4

import psutil
from aio_pika import Message, connect


class AsyncAPMHandler:
    def __init__(
        self, rabbit_host="localhost", rabbit_port=5672, rabbit_user="", rabbit_password="", server_name="python"
    ):
        self.host = rabbit_host
        self.port = rabbit_port
        self.user = rabbit_user
        self.password = rabbit_password
        self.server_name = server_name
        self.queue = "apm"
        self.exchange = ""
        self.connection = None
        self.channel = None

    async def connect(self):
        try:
            self.connection = await connect(host=self.host, port=self.port, login=self.user, password=self.password)
            self.channel = await self.connection.channel()
            await self.channel.declare_queue(self.queue, durable=True)
        except Exception as e:
            raise RuntimeError(f"AsyncAPMHandler initialization failed: {e}")

    async def send_apm_data(self, data):
        if not self.channel:
            raise RuntimeError("AsyncAPMHandler is not initialized properly.")
        try:
            message = Message(json.dumps(data).encode(), delivery_mode=2)
            await self.channel.default_exchange.publish(message, routing_key=self.queue)
        except Exception as e:
            raise RuntimeError(f"Failed to send APM data: {e}")

    def apm(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            func_name = func.__name__
            func_path = inspect.getsourcefile(func)

            # Начало измерений
            cpu_usage_start = psutil.cpu_percent(interval=None)
            process = psutil.Process()
            ram_start = process.memory_info().rss
            start_time = time.time()

            # Вызов функции
            result = func(*args, **kwargs)

            # Конец измерений
            end_time = time.time()
            cpu_usage_end = psutil.cpu_percent(interval=None)
            ram_end = process.memory_info().rss

            # Вычисления
            exec_time = end_time - start_time
            cpu_time = cpu_usage_end - cpu_usage_start
            cpu_time = cpu_time if cpu_time > 0 else 0.1
            ram_used = ram_end - ram_start
            ram_used = ram_used if ram_used > 0 else 1

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                data = {
                    "uuid": str(uuid4()),
                    "created_dt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "func_path": func_path,
                    "func_name": func_name,
                    "exec_time": exec_time,
                    "cpu_used": cpu_time,
                    "ram_used": ram_used,
                    "server_name": self.server_name,
                }
                await self.send_apm_data(data)
            return result

        return wrapper

    async def close(self):
        if self.connection:
            try:
                await self.connection.close()
            except Exception as e:
                raise RuntimeError(f"Failed to close connection: {e}")
