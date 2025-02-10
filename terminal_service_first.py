import requests
import time

def fetch_dates(container_number=None, bill_of_lading=None):
    url = 'http://eportal.goct.com.cn/Inquire/ContainerInfo/GetContainerInfo/'

    # 生成当前时间的时间戳（毫秒）
    current_timestamp = int(time.time() * 1000)
    
    # 如果提供了提单号，则通过提单号查询
    if bill_of_lading:
        params_bol = {
            '_dc': current_timestamp,
            'action': 'read',
            'sCntrNo': bill_of_lading,  # 使用提单号查询
            'type': 'M.Bl_No',
            'page': 1,
            'start': 0,
            'limit': 25
        }
        
        # 请求头设置
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Referer': 'http://eportal.goct.com.cn/Inquire/ContainerInfo/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # 发送请求
        response_bol = requests.get(url, headers=headers, params=params_bol, verify=False)
        data_bol = response_bol.json()
        
        # 检查提单号查询结果
        if data_bol['data']:
            # 提单号查询到数据，返回到达和离开日期
            entry = data_bol['data'][0]
            return entry['IN_TMNL_DATE'], entry['OUT_DATE']

    # 如果通过提单号未查询到数据，则通过柜号查询
    if container_number:
        params_container = {
            '_dc': current_timestamp,
            'action': 'read',
            'sCntrNo': container_number,  # 使用柜号查询
            'type': 'M.CNTR_NO',
            'page': 1,
            'start': 0,
            'limit': 25
        }
        
        # 发送请求
        response_container = requests.get(url, headers=headers, params=params_container, verify=False)
        data_container = response_container.json()
        
        # 遍历通过柜号查询的数据
        for entry in data_container['data']:
            # 如果找到与提单号匹配的数据
            if entry.get('BL_NO') == bill_of_lading:
                return entry['IN_TMNL_DATE'], entry['OUT_DATE']
    
    # 如果都没有找到，返回 None
    return None, None

# 使用示例
# container_no = "MNBU4128328"  # 曹号
# bill_no = "D05823111"  # 提单号

# in_date, out_date = fetch_dates(container_number=container_no, bill_of_lading=bill_no)

# if in_date and out_date:
#     print(f"到达日期: {in_date}")
#     print(f"离开日期: {out_date}")
# else:
#     print("未找到相关数据。")