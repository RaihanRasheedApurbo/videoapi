import requests


def main():

    BASE = "http://127.0.0.1:5000/"
    data = [
        {"likes": 78, "name": "joe", "views": 1000},
        {"likes": 10000, "name": "how to make rest api", "views": 80000},
        {"likes": 35, "name": "tim", "views": 2000},
    ]

    # for i in range(len(data)):
    #     response = requests.put(BASE + "video/" + str(i), data[i])
    #     print(response.json())

    # input()
    response = requests.get(BASE + "video/2")
    print(response)
    print(response.json())
