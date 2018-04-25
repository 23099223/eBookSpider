import http.client

conn = http.client.HTTPConnection("")

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'connection': "keep-alive",
    'cookie': "mfw_uuid=5adb1597-731e-f463-e420-a5e0422b34a0; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1524307351%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.baidu.com%22%3Bs%3A2%3A%22hp%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1026%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222018-04-21+18%3A42%3A31%22%3B%7D; uva=s%3A264%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222018-04-21%22%3Bs%3A2%3A%22lt%22%3Bi%3A1524307355%3Bs%3A10%3A%22last_refer%22%3Bs%3A137%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dv5C0dH0Y-rIKhf2e30mnqnJJFbNPyHLJd8WENqqrQCcvwrn3yu5oOLdPqYDKmuV-%26wd%3D%26eqid%3Dcb036b7500058428000000035adb158f%22%3Bs%3A5%3A%22rhost%22%3Bs%3A13%3A%22www.baidu.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1524307355%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5adb1597-731e-f463-e420-a5e0422b34a0; UM_distinctid=162e7cc69b7e8-0bcfaab1c1b06a-3b720b58-1fa400-162e7cc69b8407; PHPSESSID=22tm7j5j6odt3ohel6ap3qhat1; __mfwlv=1524378703; __mfwvn=2; CNZZDATA30065558=cnzz_eid%3D1129271189-1524305651-null%26ntime%3D1524375855; __mfwlt=1524378716",
    'host': "www.mafengwo.cn",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "f4a324da-a392-2ced-1b59-566df6d8371d"
}

conn.request("GET", "null", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
