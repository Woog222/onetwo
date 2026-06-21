from django.test import TestCase
from django.urls import reverse
import datetime, json, random, logging

from .utils import (
    get_random_cheering_msg, 
    CHEERING_MESSAGES_12, 
    get_weather_forecast, 
    time2korean_str, 
    make_weather_summary_text, 
    GREETING_MESSAGES_BY_PERIOD, 
    get_time_greeting, 
    evaluate_expression,
    _eval_arithmetic_node,
    get_which_day,
    )

logger = logging.getLogger(__name__)

class TestUtils(TestCase):  
    def test_get_random_cheering_msg(self):
        result = get_random_cheering_msg()
        self.assertIsInstance(result, str)
        self.assertTrue(result in CHEERING_MESSAGES_12)

    def test_get_which_day(self):
        self.assertEqual(get_which_day(date_str = "2026년 6월 20일"), "토요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 21일"), "일요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 22일"), "월요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 23일"), "화요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 24일"), "수요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 25일"), "목요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 26일"), "금요일")
        

    def test_get_weather_forecast(self):
        
        # too old date
        result = get_weather_forecast(base_date = "20250620", base_time = "1000") # too old date
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.startswith("기상예보 데이터 조회 실패."))
        
        # too future date
        result = get_weather_forecast(base_date = "20500620", base_time = "1000") # too future date
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.startswith("기상예보 데이터 조회 실패."))
        
        # current date
        today = datetime.datetime.today() # 1h ago 
        today = today - datetime.timedelta(hours = 1)
        logger.debug(today)
        base_date = today.strftime("%Y%m%d")
        base_time = today.strftime("%H00")
        result = get_weather_forecast(base_date = base_date, base_time = base_time)
        logger.debug(result)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.startswith(f"{time2korean_str(base_date, base_time)} 기준 기상예보 데이터입니다."))
        
    def test_make_weather_summary_text(self):
        result = make_weather_summary_text(
            fcst_date = "20260620", 
            fcst_time = "1000", 
            t1h_value = "22.0", 
            reh_value = "70", 
            wsd_value = "0.1", 
            rn1_value = "강수없음", 
            sky_value = "1", 
            pty_value = "0"
        )
        result2 = make_weather_summary_text(
            fcst_date="20260621", 
            fcst_time="1230", 
            t1h_value="22.0", 
            reh_value="70", 
            wsd_value="0.1", 
            rn1_value="11.0mm", 
            sky_value="1", 
        pty_value="0")
        self.assertTrue(isinstance(result, str));self.assertTrue(isinstance(result2, str));
        self.assertEqual(result, "2026년 06월 20일 10시 00분 기준 기온 22.0℃, 습도 70%, 풍속 0.1m/s, 강수량 0.0mm, 하늘상태 맑음, 강수형태 없음이 예상됩니다.")
        self.assertEqual(result2, "2026년 06월 21일 12시 30분 기준 기온 22.0℃, 습도 70%, 풍속 0.1m/s, 강수량 11.0mm, 하늘상태 맑음, 강수형태 없음이 예상됩니다.")
        
    def test_time2korean_str(self):
        result = time2korean_str(base_date = "20260620", base_time = "1000")
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.startswith("2026년 06월 20일 10시 00분"))
        
    def test_get_time_greeting(self):
        # dawn  0 ~ 4
        now = datetime.datetime(year = 2026, month = 6, day = 20, hour = 3, minute = 0, second = 0)
        result = get_time_greeting(now = now)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result in GREETING_MESSAGES_BY_PERIOD["dawn"])
        
        # morning 5 ~ 11
        now = datetime.datetime(year = 2026, month = 6, day = 20, hour = 8, minute = 0, second = 0)
        result = get_time_greeting(now = now)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result in GREETING_MESSAGES_BY_PERIOD["morning"])
        
        # noon 12 ~ 13
        now = datetime.datetime(year = 2026, month = 6, day = 20, hour = 12, minute = 0, second = 0)
        result = get_time_greeting(now = now)
        self.assertTrue(isinstance(result, str))
        
        # afternoon 14 ~ 17
        now = datetime.datetime(year = 2026, month = 6, day = 20, hour = 14, minute = 0, second = 0)
        result = get_time_greeting(now = now)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result in GREETING_MESSAGES_BY_PERIOD["afternoon"])
        
        # evening 18 ~ 20
        now = datetime.datetime(year = 2026, month = 6, day = 20, hour = 18, minute = 0, second = 0)
        result = get_time_greeting(now = now)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result in GREETING_MESSAGES_BY_PERIOD["evening"])   
        
        # night 21 ~ 23
        now = datetime.datetime(year = 2026, month = 6, day = 20, hour = 21, minute = 0, second = 0)
        result = get_time_greeting(now = now)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result in GREETING_MESSAGES_BY_PERIOD["night"])

    def test_evaluate_expression(self):
        self.assertEqual(evaluate_expression("11 + 5 * 5 / 3 - 4"), 15.33)
        self.assertEqual(evaluate_expression("2 + 3"), 5)
        self.assertEqual(evaluate_expression("(2 + 3) * 4"), 20)
        self.assertEqual(evaluate_expression("-5 + 10"), 5.00)
        self.assertRaises(ValueError, evaluate_expression, "")
        self.assertRaises(ZeroDivisionError, evaluate_expression, "1 / 0")
        
    def test_get_which_day(self):
        
        # Full formatted date string
        self.assertEqual(get_which_day(date_str = "2026년 6월 20일"), "토요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 21일"), "일요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 22일"), "월요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 23일"), "화요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 24일"), "수요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 25일"), "목요일")
        self.assertEqual(get_which_day(date_str = "2026년 6월 26일"), "금요일")
        
        # Year is not given
        self.assertEqual(get_which_day(date_str = "6월 20일"), "토요일")
        self.assertEqual(get_which_day(date_str = "6월 21일"), "일요일")
        self.assertEqual(get_which_day(date_str = "6월 22일"), "월요일")
        self.assertEqual(get_which_day(date_str = "6월 23일"), "화요일")
        self.assertEqual(get_which_day(date_str = "6월 24일"), "수요일")
        self.assertEqual(get_which_day(date_str = "6월 25일"), "목요일")
        self.assertEqual(get_which_day(date_str = "6월 26일"), "금요일")
        
        # Month is not given -> raise ValueError
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 20일")
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 21일")
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 22일")
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 23일")
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 24일")
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 25일")
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 26일")
        
        # Day is not given -> raise ValueError
        self.assertRaises(ValueError, get_which_day, date_str = "2026년 6월")  
        
        # Year and Month are not given -> raise ValueError
        self.assertRaises(ValueError, get_which_day, date_str = "20일")
        self.assertRaises(ValueError, get_which_day, date_str = "21일")
        self.assertRaises(ValueError, get_which_day, date_str = "22일")
        self.assertRaises(ValueError, get_which_day, date_str = "23일")
        self.assertRaises(ValueError, get_which_day, date_str = "24일")
        self.assertRaises(ValueError, get_which_day, date_str = "25일")
        self.assertRaises(ValueError, get_which_day, date_str = "26일")
        
        # Year and Day are not given -> raise ValueError
        self.assertRaises(ValueError, get_which_day, date_str = "6월")
        
        # utterly invalid date strings -> raise ValueError
        self.assertRaises(ValueError, get_which_day, date_str = "배고프다")
        
        # 오늘 내일 어제 (three exceptional cases)
        today = datetime.datetime.today()
        self.assertEqual(get_which_day(date_str = "오늘"), get_which_day(date_str = today.strftime("%Y년 %m월 %d일")))
        self.assertEqual(get_which_day(date_str = "내일"), get_which_day(date_str = (today + datetime.timedelta(days = 1)).strftime("%Y년 %m월 %d일")))
        self.assertEqual(get_which_day(date_str = "어제"), get_which_day(date_str = (today - datetime.timedelta(days = 1)).strftime("%Y년 %m월 %d일")))