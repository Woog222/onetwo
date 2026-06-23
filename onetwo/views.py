from rest_framework.decorators import api_view
from rest_framework.response import Response

import datetime

from .utils import (
    get_random_cheering_msg, 
    get_weather_forecast, 
    GREETING_MESSAGES_BY_PERIOD, 
    get_time_greeting, 
    get_which_day,
    get_member_seat_arrangement,
)
import logging



logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def seat_arrangement(request):
    """
    Return the seat arrangement
    """
    seat_arrangement = get_member_seat_arrangement()
    
    text_data = (
        "좌석배치 결과입니다.\n\n"
        + "\n".join([f'{item["name"]}({item["seat_number"]})' for item in seat_arrangement])
        + "\n\n"
        + "아래 좌석배치표를 참고하여 본인의 좌석을 확인해주세요.\n\n"
        + "\n\n"
        + "좌석배치표는 매일 새로운 시드값을 사용하여 생성됩니다. 따라서 매일 좌석배치가 변경됩니다."
    )
    
    
    
    logger.info(f"Seat arrangement called.\ntext_data: {text_data}")
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text_data
                    }
                },
                {
                    "simpleImage": {
                        "imageUrl": "http://175.45.195.166/static_files/divroom_seat.png",
                        "altText": "분임실 좌석 배치도입니다."
                    },
                },
                {
                    "simpleImage": {
                        "imageUrl": "http://175.45.195.166/static_files/hallseat_6023.jpg",
                        "altText": "강당 좌석 배치도입니다."
                    }
                }
            ]
        }
    }
    return Response(data = data)


@api_view(['GET', 'POST'])
def hello(request):
    """
    Return a random cheering message
    """
    
    greeting_msg = get_time_greeting()
    logger.info(f"greeting_msg: {greeting_msg}")
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": greeting_msg
                    }
                }
            ]
        }
    }
    return Response(data = data)

@api_view(['GET', 'POST'])
def enchant_team(request):
    """
    Return an enchanting message for the team
    """
    
    enchanting_msg = get_random_cheering_msg()
    logger.info(f"enchanting_msg: {enchanting_msg}")
    data= {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": enchanting_msg
                    }
                }
            ]
        }
    }
    return Response(data = data)
    
    
@api_view(['GET', 'POST'])
def weather(request):
    """
    Return the weather forecast
    """
    today = datetime.datetime.today()  # 1h ago 
    today = today - datetime.timedelta(hours = 1)
    base_date = today.strftime("%Y%m%d")
    base_time = today.strftime("%H00") # 1H interval time
    
    
    logger.info(f"base_date: {base_date}, base_time: {base_time} for weather forecast called")
    weather_forecast = get_weather_forecast(base_date = base_date, base_time = base_time)
    logger.info(f"weather_forecast received: {weather_forecast}")
    
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": weather_forecast
                    }
                }
            ]
        }
    }
    return Response(data = data)
    
@api_view(['GET', 'POST'])
def calculate(request):
    """
    Calculate the given expression
    """
    
    logger.debug(request.data)
    expression = request.data['action']['params']['expression']
    try:
        result = evaluate_expression(expression)
    except Exception as e:
        result = f"Error: {e}"
        
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }
    return Response(data = data)
                    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@api_view(['GET', 'POST'])
def which_day(request):
    """
    Return the given day of the week
    
    request.data["action"] example:
    {
        'id': '6a369a3fae969d6f764ecae4', 
        'name': 'which_day', 
        'params': {'sys_date': 'sys.date'}, 
        'detailParams': {
            'sys_date': {'groupName': '', 'origin': '26년 7월 5일', 'value': 'sys.date'}
        }, 
        'clientExtra': {}
    }
    """

    
    logger.debug(request.data.keys())
    logger.debug(request.data['action'])
    date_str = request.data['action']['detailParams']['sys_date']['origin']
    
    try:
        day_of_week = get_which_day(date_str = date_str) + "입니다."
    except Exception as e:
        day_of_week = f"Error: {e}"
        
    logger.info(f"day_of_week: {day_of_week}")
        
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": day_of_week
                    }
                }
            ]
        }
    }
    return Response(data = data)