from multiprocessing import Process
import os
import requests


def task():
    print("PID:", os.getpid())
    response = requests.get("http://13.200.12.138/stats/0000002")
    print("1 Status:", response.status_code)
    print("1 Response:", response.text)


def other_task():
    print("PID:", os.getpid())
    response = requests.post(
        "http://13.200.12.138/shorten",
        json={
            "long_url": "https://www.python-httpx.org/quickstart/new",
            "expires_at": "2026-02-23T18:23:02.234Z"
        }
    )
    print("2 Status:", response.status_code)
    print("2 Response:", response.text)


if __name__ == "__main__":
    p = Process(target=task)
    q = Process(target=other_task)

    p.start()
    q.start()

    # p.join()
    # q.join()

    print("Main process finished")