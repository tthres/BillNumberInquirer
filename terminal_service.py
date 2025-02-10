from bs4 import BeautifulSoup
import requests
import json

def fetch_terminal_times_second(bill_no, container_no):
    url = "http://e.gznict.com/dorado/view-service"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Origin": "http://e.gznict.com",
        "Referer": "http://e.gznict.com/customerservice.view.InvHist.d",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "Content-Type": "text/xml",
    }

    cookies = {
        "JSESSIONID": "9C385031D16ADCCFAB27371660BCEA7E",
    }

    data = f'''<batch>
    <request type="json"><![CDATA[{{"action":"load-data","dataProvider":"invHistService#getInvHist","supportsEntity":true,"parameter":{{"billNo":"{bill_no}","containerno":"{container_no}","fillingtype":"重"}},"resultDataType":"v:customerservice.view.InvHist$[dtInvHist]","pageSize":50,"pageNo":1,"context":{{}},"loadedDataTypes":["dtInvHist"]}}]]></request>
    </batch>'''

    response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
    
    # 使用 XML 解析器解析响应
    soup = BeautifulSoup(response.text, "lxml-xml")

    # 获取 CDATA 部分
    cdata = soup.find('response').text
    json_data = json.loads(cdata)

    # 提取 terminalintime 和 terminalouttime
    try:
        terminal_in_time = json_data['data']['data'][0]['terminalintime']
        terminal_out_time = json_data['data']['data'][0]['terminalouttime']
        
        # 替换 T 和 Z
        terminal_in_time = terminal_in_time.replace("T", " ").replace("Z", "")
        terminal_out_time = terminal_out_time.replace("T", " ").replace("Z", "")
        
        return terminal_in_time, terminal_out_time
    except (KeyError, IndexError):
        return "", ""  # 返回空值表示未找到