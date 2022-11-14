import time

def get_current_formatted_time_string():
    
    tm = time.localtime(time.time())

    year    = tm.tm_year
    month   = tm.tm_mon
    day     = tm.tm_mday
    hour    = tm.tm_hour
    minute  = tm.tm_min
    second  = tm.tm_sec

    formatted_time_string = f"{year}년 {month}월 {day}일 {hour}시 {minute}분 {second}초"

    return formatted_time_string