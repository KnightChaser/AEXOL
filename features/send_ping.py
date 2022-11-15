from pythonping import ping


def send_ping(target):
    request_qty = 5
    try:

        response_list = ping(target, count = request_qty)
        
        # 메시지
        if response_list.stats_success_ratio == 1:
            message = "성공(Success)"
        elif 0 < response_list.stats_success_ratio < 1:
            message = "부분 성공(Partial)"
        else:
            message = "실패(Failed)"

        result = {
            "rtt_avg_ms"                : response_list.rtt_avg_ms,
            "rtt_max_ms"                : response_list.rtt_max_ms,
            "rtt_min_ms"                : response_list.rtt_min_ms,
            "packets_sent"              : response_list.stats_packets_sent,
            "packets_returned"          : response_list.stats_packets_returned,
            "success_ratio_percentage"  : response_list.stats_success_ratio * 100,
            "message"                   : message
        }
    except:
        # illegal input detected
        result = "illegal input for ping"
    finally:
        return result