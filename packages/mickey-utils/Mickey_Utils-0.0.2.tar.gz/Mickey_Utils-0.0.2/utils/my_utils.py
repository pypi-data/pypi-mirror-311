import requests
import json
import re
def do_request(url,response_type='jQuery'):
    regex_str = ""
    if response_type == 'jQuery':
        regex_str=r'jQuery\d+_\d+\((.*)\)'
    else:
        regex_str=r'jsonp\d+\((.*)\)'
    return do_request_safe(url,regex_str)


def do_request_safe(url,regex_str):
    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        return parse_response_get_json_str(response.text,regex_str)
def parse_response_get_json_str(response_text,regex_str):
    """
    @param response_text:request返回response.text
    @param regex_str: 解析提取正则式
    @return: 返回JSON字符串 或 NONE
    """
    try:
        # 使用正则表达式匹配JSON字符串
        match = re.search(regex_str, response_text)
        if match:
            # 提取JSON字符串
            json_str = match.group(1)
            # 解析JSON字符串为Python对象
            data = json.loads(json_str)
        return data
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None

if __name__ == '__main__':
    #url = "https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112305578237393100798_1732527679096&fid=f62&po=1&pz=5199&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
    url = "https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery11230746472378215788_1732528889079&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
    data = do_request(url)
    print(data)