import requests
from jsontools import JsonDiff

def test(host1, host2, url_par, repeats, ignore_rules, ignore_active):
    url1 = host1 + url_par[0]
    url2 = host2 + url_par[0]
    
    result = {
            'A'     : host1,
            'B'     : host2,
            'path'  : url_par[0],
            'params': url_par[1], 
        }

    time1 = 0
    for x in range(repeats):
        resp1 = requests.get(url1, url_par[1])
        time1 += resp1.elapsed.total_seconds()
    time1 /= repeats

    time2 = 0
    for x in range(repeats):
        resp2 = requests.get(url2, url_par[1])
        time2 += resp1.elapsed.total_seconds()
    time2 /= repeats

    """ Compare execution times (see which API is faster)
    """
    diff = round(time1 - time2, 2)
    diff_perc = abs((time1 - time2) / (time1 + time2) * 100)
    same_performance = False
    if diff > 0:
        diff_faster = "B"
    elif diff < 0:
        diff_faster = "A"
    else:
        diff_faster = "="
        same_performance = True
    result['timing'] = {
            'difference'      : diff,
            'faster'          : diff_faster,
            'difference_perc' : diff_perc,
            'status'          : same_performance
        }

    """ Compare HTTP response encodings
    """
    result['http_encoding'] = {
            "A" : str(resp1.encoding), 
            "B" : str(resp2.encoding),
            "status" : (resp1.encoding == resp2.encoding)
        }

    """ Compare HTTP status codes
    """
    result['http_status'] = {
            "A" : str(resp1.status_code),
            "B" : str(resp2.status_code),
            "status" : (resp1.status_code == resp2.status_code)
        }

    jd = JsonDiff(resp1.text, resp2.text)
    jd.ignore_rules_active(ignore_active)
    jd.ignore_rules_set(ignore_rules)
    
    diff = jd.diff()
    
    result['diff'] = {
            'status' : jd.get_equality(),
            'A'      : jd.get_json1(),
            'B'      : jd.get_json2(),
            'output' : diff
        }
    
    result['status'] = (jd.get_equality() 
                        and result['http_status']['status'] 
                        and result['http_encoding']['status'])
    return result