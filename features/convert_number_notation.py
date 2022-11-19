def get_korean_number_amount(number:int):

    number_notation = {

        "해" : 100000000000000000000,
        "경" : 10000000000000000,
        "조" : 1000000000000,
        "억" : 100000000,
        "만" : 10000,
        "일" : 1
    }    

    number_reading = {}

    for key, values in number_notation.items():
        number_reading.setdefault(str(key), int(number / values))
        number -= int(number / values) * values

    korean_number_string = ""

    number_reading = {k: v for k, v in number_reading.items() if v != 0}
    for key, values in number_reading.items():
        korean_number_string += f"{values}{key}"

    korean_number_string = korean_number_string.replace("일", "")
    return korean_number_string