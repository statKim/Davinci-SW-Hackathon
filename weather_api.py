﻿import requests

appkey = "키"

# URL
url_days = "https://api2.sktelecom.com/weather/forecast/6days"
url_summary = "https://api2.sktelecom.com/weather/summary"
# 헤더
headers = {'Content-Type': 'application/json; charset=utf-8', 'appKey': appkey}

# 위치정보 : 서울시 송파구 풍납동
params = {"version": "1",
          "lat": "37.53255",
          "lon": "127.10494"
          }


def weather(params):
    response1 = requests.get(url_summary, params=params, headers=headers)
    weather1 = response1.json()

    response2 = requests.get(url_days, params=params, headers=headers)
    weather2 = response2.json()

    # 장소
    # place = weather2['weather']["forecast6days"][0]["grid"]["city"]
    # print(place)

    # 오후6시 기준 구름양
    sky = []
    sky.append(weather1["weather"]["summary"][0]["today"]["sky"]["name"])
    sky.append(weather1["weather"]["summary"][0]["tomorrow"]["sky"]["name"])

    # 일자별 최고기온
    tmax = []
    tmax.append(weather1["weather"]["summary"][0]["today"]["temperature"]["tmax"])
    tmax.append(weather1["weather"]["summary"][0]["tomorrow"]["temperature"]["tmax"])

    # 일자별 최저기온
    tmin = []
    tmin.append(weather1["weather"]["summary"][0]["today"]["temperature"]["tmin"])
    tmin.append(weather1["weather"]["summary"][0]["tomorrow"]["temperature"]["tmin"])
    
    # 2일 ~ 10일의 구름양, 최저,최고기온 append
    for i in range(2, 11, 1):
        sky.append(weather2['weather']["forecast6days"][0]["sky"]["pmName%dday"%i])
        tmax.append(weather2['weather']["forecast6days"][0]["temperature"]["tmax%dday" % i])
        tmin.append(weather2['weather']["forecast6days"][0]["temperature"]["tmin%dday" % i])
    
    # 구름양을 4가지로 분류
    weather = []
    for data in sky:
        if data == "맑음" or data == "구름조금":
            weather.append(1)
        elif data == "구름많음" or data == "흐림":
            weather.append(2)
        elif (data == "흐리고 비" or data == "구름많고 비" or data == "소나기" or data == "비 또는 눈"):
            weather.append(3)
        else:
            weather.append(4)
            
    result = {
        "weather": weather,
        "tmax": tmax,
        "tmin": tmin
    }
    
    return result

# 오늘부터 +10일 까지 총 11개의 데이터

# category 10가지
# 4가지로만 세분화
# 맑음 , 구름조금 : 1
# 구름많음, 흐림 : 2
# 흐리고 비, 구름많고 비, 소나기, 비 또는 눈 : 3
# 구름많고 눈 , 흐리고 눈 : 4