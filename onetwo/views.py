from rest_framework.decorators import api_view
from rest_framework.response import Response

import datetime

from .utils import get_random_cheering_msg, get_weather_forecast, GREETING_MESSAGES_BY_PERIOD, get_time_greeting

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
    today = datetime.datetime.today()
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
                    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @api_view(['GET', 'POST'])
# def which_day(request):
#     """
#     Return the given day of the week
#     """
#     import datetime
    
#     logger.debug(request.data)
#     params = request.data['action']['params']['sys_date_params']
    

#     today = datetime.datetime.today()
#     day = get_which_day(
#         year = params["year"] if params["year"] else today.year, 
#         month = params["month"] if params["month"] else today.month, 
#         day = params["day"] if params["day"] else today.day
#     ) # ex '일요일'

#     data = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": get_which_day() + "입니다." + str(params)
#                     }
#                 }
#             ]
#         }
#     }
#     return Response(data = data)