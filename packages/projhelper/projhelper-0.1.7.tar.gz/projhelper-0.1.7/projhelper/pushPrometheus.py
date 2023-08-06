# -*- coding: utf-8 -*-
""" 
@File    : pushPrometheus
@Time    : 22/12/19 9:23
@Author  : jianhua.ou
"""

import requests

def push_metric(data_list, pushgateway_url, url_param):
    # concat url
    try:
        url = f"{pushgateway_url}/job/{url_param['job']}"
    except KeyError:
        raise ("url_param mast has key 'job'  and data_list mast has key 'name' and value ")
    for key in url_param:
        if key != 'job':
            url = f"{url}/{key}/{url_param[key]}"

    # concat data
    data = ""
    for dic in data_list:
        try:
            name = dic['name']
            value = dic['value']
        except KeyError:
            raise ("data_list mast has key 'name' and value ")

        tag = ""
        for key in dic:
            if key not in ['name', 'value']:
                tag = f'{tag}, {key}="{dic[key]}" '
        tag = tag.replace(',', '{', 1) + '}'
        data = f"{data} {name}{tag} {value}\n"
    print(f'data:{data}')
    # if len(data)>0:
    # 中文需要转成UTF-8才能发送
    response = requests.post(url, data=data.encode("UTF-8"), headers=None)

    if response.status_code == 200:
        print("sucessfully push to {}".format(url))
        return True
    else:
        print(response.text)
    return False


if __name__ == '__main__':
    # 获取告警信息 .要有name value
    data_list = [{'name': 'key1', 'value': 35.24, 'date': 'profit'},
                 {'name': 'key2', 'value': 23.78, 'detector': 'cost-by-channel', 'date': 'other_fees'}]
    url_param = {"job": "lookout_checker", "project": "dds"}
    pushgateway_url = "http://prometheus:9091/metrics"
    push_metric(data_list, pushgateway_url, url_param)
