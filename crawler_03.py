# 拉勾网职位信息
from urllib import request, parse

# url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
url = "https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
# 反防爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.92 Safari/537.36 ',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
    'Cookie': "JSESSIONID=ABAAABAABFIAAAC0053654FB4D3E8ABD07B6454EABBE11B; "
              "WEBTJ-ID=20200414194740-17178842f3a765-0b92b7e9b0b92d-87f133f-1350728-17178842f3cac1; "
              "user_trace_token=20200414194740-21b70e4b-955d-498e-bff4-81305c707787; "
              "LGUID=20200414194740-6da52ffe-62ed-4e36-a2a5-31fb61734306; _ga=GA1.2.1543321299.1586864861; "
              "_gid=GA1.2.20031956.1586864861; "
              "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221717884a3aa237-05a77ec6927369-87f133f-1350728"
              "-1717884a3abac5%22%2C%22%24device_id%22%3A%221717884a3aa237-05a77ec6927369-87f133f-1350728"
              "-1717884a3abac5%22%7D; sajssdk_2015_cross_new_user=1; "
              "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1586864862,1586864896; "
              "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1586864896; index_location_city=%E4%B8%8A%E6%B5%B7; "
              "X_MIDDLE_TOKEN=1c1a2e5b7f7ef0370d695605c9150669; _gat=1; "
              "LGSID=20200414204411-0303e230-00f5-4289-a399-1fae3c1a5433; PRE_UTM=; PRE_HOST=cn.bing.com; "
              "PRE_SITE=https%3A%2F%2Fcn.bing.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; "
              "TG-TRACK-CODE=index_search; X_HTTP_TOKEN=f8fed4315e22a34f062868685139dacbe3acb9f947; "
              "LGRID=20200414204420-cf8f44fc-1a18-4494-a609-63c65854f4fc; SEARCH_ID=8619b530762b461fa8e41cd45bfa0dae",
    "Connection": "keep-alive"
}
data = {
    'first': "true",
    "pn": 1,
    "kd": "python"
}
# data需要编码
rep = request.Request(url, headers=headers, data=parse.urlencode(data).encode('utf-8'), method="POST")
res = request.urlopen(rep)
print(res.read().decode('utf-8'))
