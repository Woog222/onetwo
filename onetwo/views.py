from rest_framework.decorators import api_view
from rest_framework.response import Response

import datetime

from .utils import (
    get_random_cheering_msg, get_weather_forecast, GREETING_MESSAGES_BY_PERIOD, get_time_greeting, get_which_day,
)
import logging



logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def hello(request):
    """
    Return a random cheering message
    """
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": get_time_greeting()
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
    data= {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": get_random_cheering_msg()
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
    weather_forecast = get_weather_forecast(base_date = base_date, base_time = base_time)
    
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