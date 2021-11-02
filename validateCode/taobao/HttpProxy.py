# -*- coding:UTF-8 -*-
# HttpProxy.py
webdriver_js = 'Object.defineProperties(navigator,{webdriver:{get:() => false}});'
def response(flow):
    if "index.js" in flow.request.url:
        flow.response.text = flow.response.text.replace('$cdc_asdjflasutopfhvcZLmcfl_', '看起来是不是很凶 ')

        flow.response.text = webdriver_js + flow.response.text
        print('注入成功')
    if 'um.js' in flow.request.url or '115.js' in flow.request.url:
        # 屏蔽selenium检测
        flow.response.text = flow.response.text + webdriver_js