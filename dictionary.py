# -*- coding: utf-8 -*-
import json
import os
import sys
from asyncio.log import logger

from workflow import Workflow3

APP_ID = os.getenv('APP_ID', '').strip()
APP_SECRET = os.getenv('APP_SECRET', '').strip()

def check_language(word):
    import re
    return re.findall(r"[\u4e00-\u9fa5]", word).__len__() == 1


def fetch_data(word):
    from urllib import request
    from urllib import parse

    url = "https://www.mxnzp.com/api/convert/dictionary" \
          + "?content=" + parse.quote(str(word)) \
          + "&app_id=" + APP_ID \
          + "&app_secret=" + APP_SECRET
    logger.info("fetch_data url is %s", url)
    try:
        data = request.urlopen(url).read()
        rt = json.loads(data)
        logger.info("fetch_data success code is %s and msg is %s,", rt.get("code"), rt.get("msg"))
        return rt
    except Exception as e:
        rt = {'code': 500}
        logger.error("fetch_data error error is %s", e)
        return rt


def package_items(wf, rt):
    if rt.get("code") == 500:
        wf.add_item(title="查询失败！", valid=False)
    elif rt.get("code") == 1:
        result = rt.get("data")[0]
        wf.add_item(title=result.get("pinyin"), subtitle="拼音", valid=True)
        wf.add_item(title=result.get("traditional"), subtitle="繁体", valid=True)
        wf.add_item(title=result.get("radicals"), subtitle="偏旁部首", valid=True)
        wf.add_item(title=result.get("strokes"), subtitle="汉字笔画数", valid=True)
        items = result.get("explanation").split("\n\n")
        for item in items:
            wf.add_item(title=item, subtitle="汉字释义", valid=True)
    else:
        wf.add_item(title=rt.get("msg"), subtitle="错误码：" + rt.get("code"), valid=False)


def main(wf):
    word = wf.args[0].strip()
    if check_language(word):
        rt = fetch_data(word)
        package_items(wf, rt)
    else:
        wf.add_item(title="请输入单个汉字！", valid=False)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
