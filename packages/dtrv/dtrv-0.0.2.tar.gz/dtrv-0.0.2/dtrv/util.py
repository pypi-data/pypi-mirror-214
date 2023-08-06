import dtrv
import pandas as pd
import datetime
import pytz
import time

def default_vault_host() -> str:
    """
    获取全局变量 vault_host
    :return:
    """
    if dtrv.vault_host is not None:
        return dtrv.vault_host
    return ""

def default_vault_token() -> str:
    """
    获取全局变量 vault_token
    :return:
    """
    if dtrv.vault_token is not None:
        return dtrv.vault_token
    return ""

def set_vault_timestamp(data) -> bool:
    """
    修改全局变量 vault_timestamp
    :param data:
    :return:
    """
    try:
        dtrv.vault_token_timestamp = data
        return True
    except:
        return False

def string_formatting_timestamp(TZtime):
    """
    字符串 "2023-06-20T08:20:39.560493845Z" 格式化时间戳
    :param TZtime:
    :return:
    """
    origin_date_str = TZtime
    _time_object = pd.to_datetime(origin_date_str)
    # return datetime.datetime.fromtimestamp(_time_object.timestamp(), pytz.timezone(_time_object.tz.zone)).strftime("%Y-%m-%d %H:%M:%S")
    return int(time.mktime(datetime.datetime.fromtimestamp(_time_object.timestamp(), pytz.timezone(_time_object.tz.zone)).timetuple()))

def calculate_hours_for_both_timestamps(compareTime, newTime=None, tz='UTC'):
    """
    比较两个时间戳，并得到差的小时数
    :param compareTime:
    :param newTime:
    :param tz:
    :return:
    """
    if newTime:
        return "{:.1f}".format((compareTime - newTime) / 60 / 60)
    else:
        nowTime = datetime.datetime.now(pytz.timezone(tz))
        nowTimeUnix = int(time.mktime(nowTime.timetuple()))
        return "{:.1f}".format((compareTime - nowTimeUnix) / 60 / 60)