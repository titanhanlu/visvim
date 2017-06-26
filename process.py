#-*-coding:utf-8-*-
from visvim import Visvim
import os,json
import urllib2, time


fileName = "./config"
url = "http://bigota.miwifi.com/xiaoqiang/rom/config"

def getConfig():
    ua = "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    res = "{}"
    status = ""
    try:
        req = urllib2.Request(url)
        if ua:
            req.add_header('User-Agent', ua)
            # req.add_header('Content-Type', "text/xml")
        res_data = urllib2.urlopen(req, timeout=30)
        res = res_data.read()
        status = res_data.getcode()
        # print status
    except urllib2.URLError as e:
        print e.message
        if hasattr(e, 'code'):
            print 'Error code:', e.code
        elif hasattr(e, 'reason'):
            print 'Reason:', e.reason
    return res, status


if __name__ == "__main__":
    if os.path.exists(fileName) != True:
        exit(1)

    try:
        configStr = open(fileName, 'r').read()
    except Exception:
        exit(0)

    # response, status = getConfig()
    # if status != 200:
    #     exit(0)
    # configStr = response

    # print configStr

    configs = json.loads(configStr)
    for config in configs:
        username = config["username"]
        pwd = config["pwd"]
        itemName = config["itemName"]
        color = config["color"]
        size = config["size"]
        t = Visvim(username,pwd,itemName,color,size)
        t.start()
        time.sleep(1)






