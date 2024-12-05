import asyncio
import json
import socket
import click
import websockets
import psutil
import time
import threading
hostname = socket.gethostname()


def get_user_process_names():
    # 获取当前用户的用户名
    current_user = psutil.Process().username()

    # 获取所有进程
    processes = psutil.process_iter(['pid', 'name', 'username'])

    # 过滤出当前用户的进程名
    user_process_names = [proc.name() for proc in processes if proc.username() == current_user]

    return user_process_names
async def init():
    url = "ws://114.236.93.153:8083/iov/websocket/dual?topic=test_devices"
    async with websockets.connect(url) as websocket:
        while True:
            await websocket.send(json.dumps({"hostname": hostname, "process_names": get_user_process_names()}))
            try:
                data = await asyncio.wait_for(websocket.recv(), timeout=5)
                if data=="ack":
                    break
            except Exception as e:
                continue

        await connect()


async def connect():
    url = "ws://114.236.93.153:8083/iov/websocket/dual?topic=" + hostname
    async with websockets.connect(url) as websocket:
        receive_data = await websocket.recv()
        await websocket.send("ack")
        receive_data = json.loads(receive_data)
        process_name = receive_data.get("process_name")
        print("process_name:", process_name)
        t=threading.Thread(target=collect_and_push_metrics, args=(process_name,websocket))
        t.start()
        t.join()

def collect_and_push_metrics(process_name, websocket):

    async def send_data(data):
        await websocket.send(json.dumps(data))

    while True:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.name() == process_name:
                while True:
                    cpu_percent_per_cpu = psutil.cpu_percent(interval=1, percpu=True)
                    load_avg = psutil.getloadavg()
                    cpu_percent_total = sum(cpu_percent_per_cpu) / len(cpu_percent_per_cpu)
                    # 获取总内存
                    total_memory = psutil.virtual_memory().total
                    # 获取可用内存
                    available_memory = psutil.virtual_memory().available
                    # 获取内存使用率
                    memory_percent = psutil.virtual_memory().percent
                    network_io = psutil.net_io_counters()
                    data = {
                        "cpu_percent_per_cpu": cpu_percent_per_cpu,
                        "load_avg": load_avg,
                        "cpu_percent_total": cpu_percent_total,
                        "total_memory": total_memory,
                        "available_memory": available_memory,
                        "memory_percent": memory_percent,
                        "network_io": network_io,
                        "process_cpu_percent": proc.cpu_percent(),
                        "process_memory_percent": proc.memory_percent(memtype="rss"),
                    }
                    asyncio.run(send_data(data))

                    time.sleep(1)
@click.command()
def main():
    asyncio.run(init())

if __name__ == '__main__':
    main()
    # connect()
