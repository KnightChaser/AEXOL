def get_korean_number_amount(number:int):

    number_notation = {

        "해" : 100000000000000000000,
        "경" : 10000000000000000,
        "조" : 1000000000000,
        "억" : 100000000,
        "만" : 10000,
        "일" : 1
    }    

    original_number = number

    number_reading = {}

    for key, values in number_notation.items():
        number_reading.setdefault(str(key), int(number / values))
        number -= int(number / values) * values

    korean_number_string = ""

    number_reading = {k: v for k, v in number_reading.items() if v != 0}
    for key, values in number_reading.items():
        korean_number_string += f"{values}{key}"

    korean_number_string = korean_number_string.replace("일", "")

    # for negative function
    if original_number < 0:
        korean_number_string = korean_number_string.replace("-", "")
        korean_number_string = "-" + korean_number_string

    return korean_number_string

def approx_SI_prefix_formatter(number):


    number_notation = {

        "T" : 1000000000000,
        "B" : 1000000000,
        "M" : 1000000,
        "K" : 1000
    }

    SI_number_string = ""

    for key, values in number_notation.items():
        if int(number) / values >= 1:
            SI_number_string = f"{round(int(number) / values, 2)}{key}"
            return SI_number_string
            

    return number       # No need to add prefix