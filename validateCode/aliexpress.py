from selenium.webdriver.common.action_chains import ActionChains
import time,random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
https://www.cnblogs.com/zhe-hello/p/10345073.html
第一个 我们定位滑块
第二步 我们就模拟鼠标按住模块
第三步 就是拖动了（这里我们要实现随机的移动 一次就移动一点点）
　　　　　　　　写一个循环  
　　　　　　　　一点点的移动
　　　　　　　　直到拖动到最右边
　　　　　　　　然后每次移动之后 我们截图保存看当前的移动效果
　　　　　　　　最后就可以移动有最右侧了

移除淘宝对selenium的检测：https://www.cnblogs.com/presleyren/p/12936553.html
'''

#配置代理
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Host": "buyertrade.taobao.com",
#     "Accept-Language": "zh-CN",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
#     "Connection": "keep-alive",
#     "referer": "https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm"
# }
options = Options()
# options.add_argument('--proxy-server=http://127.0.0.1:9000')

# chrome 版本 95.0.4638.69                                       # 网上找到 你可以试试
# 这里是你指定浏览器的路径
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
# 设置为开发者模式，避免被识别
options.add_experimental_option('excludeSwitches',['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
# 驱动地址
driver = webdriver.Chrome(executable_path="C:\\Python39\\taobao\\chromedriver_win32\\chromedriver_update.exe",chrome_options=options)
# driver = webdriver.Remote("http://你的ip地址:4444/wd/hub", desired_capabilities)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.get("https://login.aliexpress.com/seller.htm")
driver.maximize_window()

#切 登录iframe
iframe = driver.find_element_by_xpath("//iframe")
driver.switch_to.frame(0)

time.sleep(2)
username = driver.find_element_by_css_selector("input#fm-login-id")
ActionChains(driver).move_to_element(username).click(on_element=username).perform()
for ever in "username":
    time.sleep(random.randint(0,1000)/1000)
    username.send_keys(ever)
time.sleep(random.randint(0,1000)/1000)
pwd = driver.find_element_by_css_selector("input#fm-login-password")
ActionChains(driver).move_to_element(pwd).click(on_element=pwd).perform()
for temp in "password":
    time.sleep(random.randint(0,1000)/1000)
    pwd.send_keys(temp)


# 睡眠等待滑块出来
time.sleep(random.randint(500,1500)/1000)
# iframe = driver.find_element_by_xpath("//*[@id="baxia-dialog-content"]")
# driver.switch_to.frame("baxia-dialog-content")
# try:
#     huakuai = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
#     print("找到滑块元素")
# except:
#     print("没有找到滑块元素")
#     pass
# else:
#     action = ActionChains(driver)
#     # 点击滑块 -> 208px
#     action.click_and_hold(huakuai).perform()
#     # 随机循环的次数自己控制
#     count = random.randint(0,5);
#     for index in range(count):
#         print("index:%d" %index)
#         try:
#             action.move_by_offset(209/count, 0).perform()  # 平行移动鼠标
#             driver.save_screenshot('login-screeshot-i-' + str(index) + '.png')
#         except Exception as e:
#             print(e)
#             break
#         if (index == (count-1)):
#             action.release()
#             time.sleep(1)
#             driver.save_screenshot('login-screeshot-i-' + str(index) + '.png')
#         else:
#             sleeptime = random.randint(0,1000)
#             print("延迟%d毫秒" %sleeptime)
#             time.sleep(sleeptime/1000)
# print("滑块移动完成")

try:
    driver.switch_to.frame("baxia-dialog-content")
    slider = driver.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
    if slider.is_displayed():
        ActionChains(driver).click_and_hold(on_element=slider).perform()
        ActionChains(driver).move_by_offset(xoffset=208, yoffset=0).perform()
        ActionChains(driver).pause(0.5).release().perform()
        print("滑块移动完成")
except:
    print("未获取滑块")
    pass
# try:
#     # 找到滑块
#     slider = driver.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
#     # 判断滑块是否可见
#     if slider.is_displayed():
#         # 点击并且不松开鼠标
#         ActionChains(driver).click_and_hold(on_element=slider).perform()
#         time.sleep(random.randint(0,1000)/1000)
#         # 往右边移动258个位置
#         ActionChains(driver).move_by_offset(xoffset=209, yoffset=0).perform()
#         time.sleep(random.randint(0,1000)/1000)
#         # 松开鼠标
#         ActionChains(driver).pause(0.8).release().perform()
#     else:
#         print("滑块不可见")
# except:
#     print("没有找到滑块")
#     pass
print("滑块移动完成")
# 切回到默认的父页面
# driver.switch_to.default_content()

# driver.switch_to.frame("alibaba-login-box")
loginButton = driver.find_element_by_css_selector("input#fm-login-submit")
loginButton.click()
print("点击登录按钮成功")
driver.switch_to.default_content()

# 第2次滑动
# time.sleep(10)
# # driver.switch_to.frame("baxia-dialog-content")
# # try:
# slider = driver.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
# if slider.is_displayed():
#     ActionChains(driver).click_and_hold(on_element=slider).perform()
#     ActionChains(driver).move_by_offset(xoffset=208, yoffset=0).perform()
#     ActionChains(driver).pause(0.5).release().perform()
#     print("找到滑块")
# else:
#     print("未找到滑块")
# except as e:
#     print("找滑块异常")
#     pass
