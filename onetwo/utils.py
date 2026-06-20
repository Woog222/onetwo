import requests
import os
from dotenv import load_dotenv
load_dotenv()

WEATHER_APIKEY = os.getenv("WEATHER_APIKEY")
WEATHER_FORECAST_URL=os.getenv("WEATHER_FORECAST_URL")


"""
Getting weather forecast data from the API

Check it out for more details
-> https://app.notion.com/p/API-383c3adb9bbc805bac7ae675a3573203

URL : WEATHER_FORECAST_URL (from .env file)

request parameters :
- serviceKey : WEATHER_APIKEY (from .env file)
- numOfRows : 100
- pageNo : 1
- dataType : JSON
- base_date : current date (YYYYMMDD)
- base_time : current time (HHMM, 30 minutes interval)
- nx : 69 (Korea National HRD Institute)
- ny : 113 (Korea National HRD Institute)

Response body (JSON) :
- response :
    - header :
        - resultCode : 00 (expected)
        - resultMsg : "NORMAL_SERVICE" (expected)
    - body : 
        - dataType : JSON
        - items : 
            - item : [
                - baseDate : YYYYMMDD
                - baseTime : HHMM
                - category : T1H (RN1, SKY, PTY, VEC, WSD..)
                - fcstDate : YYYYMMDD
                - fcstTime : HHMM
                - fcstValue : (check the document for more details)
            ]
        - pageNo : 1
        - numOfRows : 100
        - totalCount : 100
"""

def get_weather_forecast(base_date:int, base_time:int):
    """
    Args:
        base_date (int): current date (YYYYMMDD)
        base_time (int): current time (HHMM, 30 minutes interval)
        
    Returns:
        dict: weather forecast data 
        {
            T1H : [
                {
                    "fcstDate": YYYYMMDD,
                    "fcstTime": HHMM,
                    "fcstValue": 20.0,
                }, ..
            ],
            SKY : [
                {}
            ]
            
        }
        
    """
    
    url = WEATHER_FORECAST_URL
    params = {
        "serviceKey": WEATHER_APIKEY,
        "numOfRows": 100,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": 69,
        "ny": 113,
    }
    response = requests.get(url, params=params)
    data = response.json() # dict
    resultCode = data["response"]["header"]["resultCode"] # str '00' expected
    
    
    # Failed to fetch weather data
    if resultCode != '00':
        # handling exception (to do)
        pass

    
    fcst_datas = data["response"]["body"]["items"]["item"] # list
    
    
    t1h = [{
        'fcstDate' : fcst_data['fcstDate'], 
        'fcstTime' : fcst_data['fcstTime'],
        'fcstValue': fcst_data['fcstValue']
    } 
        for fcst_data in fcst_datas 
        if fcst_data["category"] == "T1H"
    ]
    
    print(t1h)
    return response.json()

def get_random_cheering_msg():
    import random
    cheering_messages_12 = [
        "12분임 화이팅!!!",
        "12분임 최고!!",
        "VAMOS 12div!!!",
        "12분임 가즈앗!!",
        "원투원투! 12분임 날아오르자!",
        "12분임, 오늘도 뿌셔봅시다!",
        "우리가 누구? 최강 12분임!",
        "12분임 케미 폭발, 오늘도 화이팅!",
        "지치지 않는 열정, 12분임 힘내요!",
        "12분임의 잠재력을 보여줄 시간!",
        "언제나 빛나는 12분임, 화이팅입니다!",
        "12분임과 함께라면 어디든 갈 수 있어!",
        "오늘도 대박 날 12분임 응원합니다!",
        "12분임, 너의 능력을 보여줘!",
        "찰떡궁합 12분임, 오늘도 가보자고!",
        "12분임의 모든 도전을 응원해요!",
        "원투원투! 리듬 맞춰 끝까지 화이팅!",
        "12분임, 오늘도 완벽하게 해낼 거예요!",
        "우리의 노력이 결실을 맺을 12분임!",
        "12분임, 긍정 파워로 가득 채워봐요!",
        "서로 믿고 가는 12분임, 화이팅!",
        "12분임의 멋진 활약을 기대합니다!",
        "끝까지 지치지 마요, 12분임!",
        "12분임, 오늘도 기분 좋게 스타트!",
        "함께라서 든든한 12분임 최고 최고!",
        "12분임, 한 걸음 더 앞으로 가즈아!",
        "우리의 호흡은 100점 만점에 120점!",
        "12분임, 오늘도 멋지게 해내실 거라 믿어요!",
        "언제나 12분임을 무한 응원합니다!",
        "12분임 아자아자 화이팅!!!"
    ]
    return random.choice(cheering_messages_12) # str