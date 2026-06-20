import requests
import os, random, datetime
from dotenv import load_dotenv
load_dotenv()


WEATHER_APIKEY = os.getenv("WEATHER_APIKEY")
WEATHER_FORECAST_URL=os.getenv("WEATHER_FORECAST_URL")

CHEERING_MESSAGES_12 = [
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

DAY_OF_WEEK = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]


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

def get_weather_forecast(base_date:str, base_time:str):
    """
    Args:
        base_date (str): Current date in YYYYMMDD format
        base_time (str): Current time in HHMM format (30 minute intervals)
        
    Returns:
        Returns organized Korean weather forecast sentences using the following data:
        T1H : 1-hour temperature forecast (6 hours forecast data)
        RN1 : 1-hour rainfall forecast (6 hours forecast data)
        SKY : 1-hour sky condition forecast (6 hours forecast data)
        PTY : 1-hour precipitation type forecast (6 hours forecast data)
        REH : 1-hour relative humidity forecast (6 hours forecast data)
        WSD : 1-hour wind speed forecast (6 hours forecast data)
        
        Example:
        (base_date and base_time) 2026년 6월 21일 12시 30분에 측정한 단기 기상예보 데이터입니다.
        
        2026년 6월 21일 13시 (using fcstDate and fcstTime) 기온은 22.0℃, 강수량은 11.0mm, 하늘상태는 맑음, 강수형태는 없음, 습도는 70%, 풍속은 0.1m/s 입니다. 
        2026년 6월 21일 14시 (using fcstDate and fcstTime) 기온은 22.0℃, 강수량은 11.0mm, 하늘상태는 맑음, 강수형태는 없음, 습도는 70%, 풍속은 0.1m/s 입니다. 
        ...
    """ 
    response = requests.get(
        url = WEATHER_FORECAST_URL, 
        params={
            "serviceKey": WEATHER_APIKEY,
            "numOfRows": 100,
            "pageNo": 1,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": 69,
            "ny": 113,
        }
    )
    data = response.json() # dict
    resultCode = data["response"]["header"]["resultCode"] # str '00' expected
    
    # Failed to fetch weather data
    if resultCode != '00':
        return f"기상예보 데이터 조회 실패. {data["response"]["header"]["resultMsg"]}"
    

    
    fcst_datas = data["response"]["body"]["items"]["item"] # list
    t1h = [ # 1h temperature forecast data (6 hours forecast data)
        { 
            'fcstDate' : fcst_data['fcstDate'], 
            'fcstTime' : fcst_data['fcstTime'],
            'fcstValue': fcst_data['fcstValue'] # 22.0 (℃)
        } 
        for fcst_data in fcst_datas 
        if fcst_data["category"] == "T1H"
    ]
    
    rn1 = [ # 1h rainfall forecast data (6 hours forecast data)
        { 
            'fcstDate' : fcst_data['fcstDate'], 
            'fcstTime' : fcst_data['fcstTime'],
            'fcstValue': fcst_data['fcstValue'] # "강수없음" OR "11.0mm"
        } 
        for fcst_data in fcst_datas 
        if fcst_data["category"] == "RN1"
    ]
    
    sky = [ # 1h sky forecast data (6 hours forecast data)
        { 
            'fcstDate' : fcst_data['fcstDate'], 
            'fcstTime' : fcst_data['fcstTime'],
            'fcstValue': fcst_data['fcstValue'] # 맑음(1), 구름많음(3), 흐림(4)
        } 
        for fcst_data in fcst_datas 
        if fcst_data["category"] == "SKY"
    ]
    
    pty = [ # 1h precipitation forecast data (6 hours forecast data)
        { 
            'fcstDate' : fcst_data['fcstDate'], 
            'fcstTime' : fcst_data['fcstTime'],
            'fcstValue': fcst_data['fcstValue'] # 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7) 
        } 
        for fcst_data in fcst_datas 
        if fcst_data["category"] == "PTY"
    ]
    
    reh = [ # 1h relative humidity forecast data (6 hours forecast data)
        { 
            'fcstDate' : fcst_data['fcstDate'], 
            'fcstTime' : fcst_data['fcstTime'],
            'fcstValue': fcst_data['fcstValue'] # "70" (%)
        } 
        for fcst_data in fcst_datas 
        if fcst_data["category"] == "REH"
    ]
    
    wsd = [ # 1h wind speed forecast data (6 hours forecast data)
        { 
            'fcstDate' : fcst_data['fcstDate'], 
            'fcstTime' : fcst_data['fcstTime'],
            'fcstValue': fcst_data['fcstValue'] # "0.1" (m/s)
        } 
        for fcst_data in fcst_datas 
        if fcst_data["category"] == "WSD"
    ]
    
    summary_text_list = [
        make_weather_summary_text(
            fcst_date=t1h_data['fcstDate'], 
            fcst_time=t1h_data['fcstTime'], 
            t1h_value=t1h_data['fcstValue'], 
            reh_value=reh_data['fcstValue'], 
            wsd_value=wsd_data['fcstValue'], 
            rn1_value=rn1_data['fcstValue'], 
            sky_value=sky_data['fcstValue'], 
            pty_value=pty_data['fcstValue'])
        for t1h_data, sky_data, pty_data, rn1_data, reh_data, wsd_data in zip(t1h, sky, pty, rn1, reh, wsd)
    ]
    
    return f'{time2korean_str(base_date, base_time)} 기준 기상예보 데이터입니다.\n\n' + '\n'.join(summary_text_list)


    
def make_weather_summary_text(fcst_date:str, fcst_time:str, t1h_value:str, reh_value:str, wsd_value:str, rn1_value:str, sky_value:str, pty_value:str):
    """
    Generate a summary of the weather forecast based on forecast data lists.
    
    Args:
        Every arguments are string data type.
        fcst_date : Forecast date in YYYYMMDD format
        fcst_time : Forecast time in HHMM format (30 minute intervals)
        t1h_value : Temperature forecast data - "22.0" (℃)
        reh_value : Relative humidity forecast data - "70" (%)
        wsd_value : Wind speed forecast data - "0.1" (m/s)
        rn1_value : Rainfall forecast data - "강수없음" OR "11.0mm"
        sky_value : Sky status forecast data - 1: 맑음, 3: 구름많음, 4: 흐림
        pty_value : Precipitation type forecast data - 0: 없음, 1: 비, 2: 비/눈, 3: 눈, 5: 빗방울, 6: 빗방울눈날림, 7: 눈날림
        
        
    Returns:
        str: A summary string describing the weather forecast.
    """

    # Sky codes: 맑음(1), 구름많음(3), 흐림(4)
    sky_text = {
        "1": "맑음",
        "3": "구름많음",
        "4": "흐림"
    }.get(str(sky_value), str(sky_value))

    # PTY codes: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
    pty_text = {
        "0": "없음",
        "1": "비",
        "2": "비/눈",
        "3": "눈",
        "5": "빗방울",
        "6": "빗방울눈날림",
        "7": "눈날림"
    }.get(str(pty_value), str(pty_value))
    
    result_str_list = [f"{time2korean_str(fcst_date, fcst_time)} 기준 "]
    result_str_list.append(f"기온 {t1h_value}℃, ")
    result_str_list.append(f"습도 {reh_value}%, ")
    result_str_list.append(f"풍속 {wsd_value}m/s, ")
    result_str_list.append(f"강수량 {"0.0mm" if rn1_value == "강수없음" else rn1_value}, ")
    result_str_list.append(f"하늘상태 {sky_text}, ")
    result_str_list.append(f"강수형태 {pty_text}")
    result_str_list.append(f"이 예상됩니다.")

    return ''.join(result_str_list)

def time2korean_str(base_date:str, base_time:str):
    """
    Args:
        base_date (str): Current date in YYYYMMDD format
        base_time (str): Current time in HHMM format (30 minute intervals)
        
    Returns:
        str: A string representing the time in the format of "YYYY년 MM월 DD일 HH시 MM분"
    """
    return f"{base_date[:4]}년 {base_date[4:6]}월 {base_date[6:8]}일 {base_time[:2]}시 {base_time[2:4]}분"


def get_random_cheering_msg():
    return random.choice(CHEERING_MESSAGES_12) # str


# def get_which_day(year, month, day):
#     """ 
#     Args:
#         year (int, probably str): year 
#         month (int, probably str): month
#         day (int, probably str): day
        
#     Returns:
#         str: the day of the week
#     """
#     date = datetime.datetime(int(year), int(month), int(day))
#     return DAY_OF_WEEK[date.weekday()] # str 


    





















