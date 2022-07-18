# -*- coding: utf-8 -*-
from asyncio.log import logger
from distutils.log import debug
from nturl2path import url2pathname
import sys
import json
from turtle import title
from workflow import Workflow3

DEFAUTL_KEY = "858fcf4a2de28dbd29cdf53593d00af3"

def check_language(word):
    import re
    return re.findall(r"[\u4e00-\u9fa5]",word).__len__() == 1

def fetch_data(word):
    from urllib import request
    from urllib import parse

    url = "http://v.juhe.cn/xhzd/query"\
        + "?word=" + parse.quote(str(word))\
        + "&key=" + DEFAUTL_KEY
    logger.info("fetch_data url is %s",url)
    try: 
        data = request.urlopen(url).read()
        rt = json.loads(data)
        logger.info("fetch_data succsess reason is %s",rt.get("reason"))
        return rt
    except Exception as e:
        rt = {}
        rt['error_code'] = '500'
        logger.error("fetch_data error error is %s",e)
        return rt

def package_items(wf,rt):
    if rt.get("error_code") == '500':
        wf.add_item(title="查询失败！",valid=False)
    elif rt.get("error_code") == '0':
        result = rt.get("result")
        wf.add_item(title=result.get("pinyin"),subtitle="拼音",valid=True)
    else:
        wf.add_item(title=rt.get("reason"),valid=False)
    
def main(wf):
    word = wf.args[0].strip()
    if check_language(word):
        rt = fetch_data(word)
        package_items(wf,rt)
    else:
        wf.add_item(title="请输入一个汉字！",valid=False)

    wf.send_feedback()
    
if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))