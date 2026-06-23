import ast
import operator
import requests
import os, random, datetime, logging, re
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Environment variables
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

GREETING_MESSAGES_BY_PERIOD = {
    "dawn": [
        "새벽이네요. 아직 안 잤어요?",
        "이 시간에 만나다니, 우리 꽤 친한 거 맞죠?",
        "새벽이라 좀 고요하네요. 무리하지 마세요.",
        "이른 새벽이에요. 잠깐 쉬어가도 괜찮아요.",
        "새벽인데도 반가워요. 오늘도 편하게 보내요.",
        "새벽 공기가 차갑네요. 따뜻하게 챙기세요.",
        "새벽이 지나면 아침이 올 거예요. 조금만 더 버텨봐요.",
        "새벽에 연락드리네요. 오늘도 잘 부탁해요.",
    ],
    "morning": [
        "좋은 아침이에요! 잘 잤어요?",
        "굿모닝! 오늘도 기분 좋게 시작해요.",
        "아침이에요. 오늘 하루도 힘내요!",
        "상쾌한 아침이네요. 오늘도 재밌게 보내요.",
        "아침부터 반가워요. 오늘 뭐 할 계획이에요?",
        "좋은 아침! 밥은 챙겨 먹었어요?",
        "아침이에요. 오늘도 같이 힘내봐요.",
        "모닝이에요! 오늘 기분은 어때요?",
        "하루의 시작, 오늘도 파이팅이에요!",
        "아침인데 벌써 만나네요. 반가워요.",
    ],
    "noon": [
        "점심 시간이에요. 맛있게 먹었어요?",
        "배고프지 않아요? 점심 꼭 챙겨 먹어요.",
        "점심이에요! 오늘 오전도 수고 많았어요.",
        "맛점이에요. 오후도 같이 버텨봐요.",
        "점심시간이 최고죠. 잠깐 쉬어가요.",
        "점심 뭐 먹었어요? 궁금하네요.",
        "한낮이에요. 오늘도 잘하고 있어요.",
        "점심시간이에요. 맛있는 거 먹었길 바라요.",
    ],
    "afternoon": [
        "오후네요. 좀 졸리지 않아요?",
        "나른한 오후예요. 조금만 더 힘내요!",
        "오후 시간이에요. 오늘도 수고 많아요.",
        "햇살 좋은 오후네요. 오늘 어때요?",
        "오후에도 반가워요. 남은 시간도 같이 가요.",
        "오후엔 커피 한 잔이 딱이죠.",
        "졸릴 때가 왔네요. 물 한 잔 마시고 쉬어가요.",
        "오후 파워 충전은 했어요?",
        "아직 오후예요. 끝까지 잘 해낼 거예요.",
    ],
    "evening": [
        "저녁이에요! 오늘 하루도 고생 많았어요.",
        "퇴근/퇴실했어요? 저녁 맛있게 먹어요.",
        "저녁 시간이네요. 오늘 어땠어요?",
        "하루 마무리 시간이에요. 수고했어요!",
        "저녁이에요. 오늘도 잘 버텨냈네요.",
        "저녁 노을 보고 있어요? 예쁘죠.",
        "저녁인데 뭐 먹을 거예요?",
        "오늘 하루, 정말 고생 많았어요.",
        "저녁 시간이에요. 편하게 쉬어요.",
    ],
    "night": [
        "밤이에요. 오늘도 수고 많았어요.",
        "좋은 밤! 내일 또 만나요.",
        "아직 안 잤어요? 일찍 쉬어요.",
        "밤이 깊어졌네요. 오늘도 고생했어요.",
        "오늘 하루 끝났네요. 푹 쉬어요.",
        "늦은 시간이에요. 무리하지 마세요.",
        "오늘도 재밌었어요. 내일 또 봐요!",
        "자기 전에 한번 더 반가워요.",
        "밤이에요. 좋은 꿈 꾸세요.",
    ],
}

DAY_OF_WEEK = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

_ARITHMETIC_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Member profiles (name)
# 강민우, 고효정, 권승빈, 김동우, 김민철, 김형탁, 손경민, 손예원, 송경준, 오혜원, 이서영, 임도민, 장동건, 정지수, 정현민, 하유주, 허제욱
members = [
    {
        "name": "허제욱",
    },
    {
        "name": "고효정"
    },
    {
        "name": "권승빈"
    },
    {
        "name": "김동우"
    },
    {
        "name": "김민철"
    },
    {
        "name": "김형탁"
    },
    {
        "name": "이서영"
    },
    {
        "name": "손예원"
    },
    {
        "name": "송경준"
    },
    {
        "name": "오혜원"
    },
    {
        "name": "손경민"
    },
    {
        "name": "임도민"
    },
    {
        "name": "장동건"
    },
    {
        "name": "정지수"
    },
    {
        "name": "정현민"
    },
    {
        "name": "하유주"
    },
    {
        "name": "강민우"
    },
]

def _seat_number_shuffle(seed:int):
    """
    Shuffle the list of seat numbers (from 198 to 214) in a deterministic way using the given seed,
    ensuring specific placement rules:
    
    Args:
        seed (int): Seed for the random number generator.
    
    Rules:
        1. Generate a list of numbers from 198 to 214 (inclusive), called shuffled_numbers.
        2. Select two numbers from this list such that their difference is less than or equal to 4,
           and place them at index 0 and index 10 of the shuffled_numbers list.
        3. Place the remaining numbers in the other positions of the list.
        4. Return the shuffled_numbers list.
        
        Most important rule: The result must always be identical for the same seed.
    
    Returns:
        list: The deterministically shuffled list of seat numbers following the above rules.
    """

    shuffled_numbers = list(range(198, 215))
    random.seed(seed)
    while True:
        random.shuffle(shuffled_numbers)
        if abs(shuffled_numbers[0] - shuffled_numbers[10]) <= 4:
            break
    return shuffled_numbers

def get_member_seat_arrangement():
    """
    
    
    Returns:
        list of dicts: {"name" : member_name, "seat_number" : seat_number} 
        E.G. [{"name" : "허제욱", "seat_number" : 211}, {"name" : "고효정", "seat_number" : 212}, ...]
    """
    
    seat_arrangement = []
    # Get a seed : year + month + day
    today = datetime.datetime.today()
    seed = today.year + today.month + today.day
    seat_numbers = _seat_number_shuffle(seed)
    
    member_names = [member["name"] for member in members] # list of strings
    
    for member_name, seat_number in zip(member_names, seat_numbers):
        seat_arrangement.append({
            "name" : member_name,
            "seat_number" : seat_number
        })
        
    logger.info(f"seat_arrangement (seed : {seed}): {seat_arrangement}")
    return seat_arrangement # list of dicts
    





def get_weather_forecast(base_date:str, base_time:str):
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
    - base_time : current time (HHMM, 1H interval time)
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

    Args:
        base_date (str): Current date in YYYYMMDD format
        base_time (str): Current time in HHMM format (1H interval time)
        
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
    logger.debug(f"base_date: {base_date}, base_time: {base_time}")
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
    logger.debug(f"response: {response}")
    data = response.json() # dict
    logger.debug(f"data: {data}")
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


def _get_greeting_period(hour: int) -> str:
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 14:
        return "noon"
    if 14 <= hour < 18:
        return "afternoon"
    if 18 <= hour < 21:
        return "evening"
    if 21 <= hour < 24:
        return "night"
    return "dawn"

def get_time_greeting(now: datetime.datetime | None = None) -> str:
    """
    Returns a random greeting message appropriate for the current time period.

    Args:
        now: The reference datetime. If None, the current time is used.

    Returns:
        str: A greeting message suitable for the time period.
   
    """
    if now is None:
        now = datetime.datetime.now()
        
    logger.info(f"Getting greeting message for now: {now}")
    period = _get_greeting_period(now.hour)
    logger.info(f"Greeting message period: {period}")
    return random.choice(GREETING_MESSAGES_BY_PERIOD[period])





def _eval_arithmetic_node(node: ast.AST) -> float:
    """
    Evaluate an arithmetic expression.

    Args:
        node: The AST node to evaluate.

    Returns:
        float: The result of the evaluation, rounded to 2 decimal places
    """
    if isinstance(node, ast.Expression):
        return _eval_arithmetic_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return round(node.value, 2)
        raise ValueError(f"숫자가 아닌 값입니다: {node.value!r}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ARITHMETIC_OPERATORS:
            raise ValueError(f"지원하지 않는 연산자입니다: {op_type.__name__}")
        left = _eval_arithmetic_node(node.left)
        right = _eval_arithmetic_node(node.right)
        return round(_ARITHMETIC_OPERATORS[op_type](left, right), 2)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ARITHMETIC_OPERATORS:
            raise ValueError(f"지원하지 않는 연산자입니다: {op_type.__name__}")
        return round(_ARITHMETIC_OPERATORS[op_type](_eval_arithmetic_node(node.operand)), 2)
    raise ValueError(f"지원하지 않는 수식입니다: {type(node).__name__}")


def evaluate_expression(expression: str) -> float:
    """
    문자열 산술 수식을 계산합니다. +, -, *, / 와 괄호를 지원합니다.

    Args:
        expression (str): 계산할 수식. 예: "11 + 5 * 5 / 3 - 4"

    Returns:
        float: 계산 결과

    Raises:
        ValueError: 빈 문자열, 잘못된 수식, 지원하지 않는 연산자
        ZeroDivisionError: 0으로 나누기
    """
    if not expression or not expression.strip():
        raise ValueError("수식이 비어 있습니다.")

    tree = ast.parse(expression.strip(), mode="eval")
    return _eval_arithmetic_node(tree)




def get_which_day(date_str:str):
    """ 
    Args:
        date_str (str): Date string in Korean format like "2026년 6월 20일".
            - If the year is not given, use today's year.
            - If month or day is not given, raise an error.
            - Three exceptional cases:"오늘", "내일", "어제" are only allowed.

    Returns:
        str: The day of the week in Korean (e.g., "월요일").
    """
    
    today = datetime.datetime.today()
    
    logger.info(f"Getting which day for date_str: {date_str}")
    
    # Exceptional cases
    if date_str == "오늘":
        return DAY_OF_WEEK[today.weekday()]
    elif date_str == "내일":
        return DAY_OF_WEEK[(today + datetime.timedelta(days = 1)).weekday()]
    elif date_str == "어제":
        return DAY_OF_WEEK[(today - datetime.timedelta(days = 1)).weekday()]
    
    # Normal cases
    year_match = re.search(r"(\d+)년", date_str)
    month_match = re.search(r"(\d+)월", date_str)
    day_match = re.search(r"(\d+)일", date_str)
    if month_match is None or day_match is None:
        raise ValueError("Month or day is not given")
    
    year = today.year if year_match is None else int(year_match.group(1))
    month = int(month_match.group(1))
    day = int(day_match.group(1))
    
    return DAY_OF_WEEK[datetime.datetime(year, month, day).weekday()]











