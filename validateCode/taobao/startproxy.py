# -*- coding:UTF-8 -*-
# 第一步运行startproxy.py
# 第二步运行配置了代理的淘宝登录python脚本
from mitmproxy.tools.main import mitmweb
mitmweb(args=['-s', './HttpProxy.py', '-p', '9000', '--web-port', '9020'])