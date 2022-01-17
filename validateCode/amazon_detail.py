import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

'''
https://blog.csdn.net/weixin_39020133/article/details/105966388
带插件启动：https://www.cnblogs.com/lizm166/p/13207036.html
'''

# 解析商品详情页 返回商品asin、主图地址、标题、价格、评分、评论人数、大类排名、小类排名
def parse_detail(page_source):
    html = pq(page_source)
    attr_list = []

    # 商品标题
    title = html("span#productTitle").text()

    # 详细描述
    li_list = html("ul.a-unordered-list.a-vertical.a-spacing-none li").items()
    li_text_list = []
    for li in li_list:
        li_text_list.append(li.text().strip())

    # 主图
    z_img = html("img#landingImage").attr("data-old-hires")
    if z_img == "":
        z_img = html("img#landingImage").attr("src")

    # 价格
    price = html('span[id*="priceblock"]').text().replace('\xa0', '')

    # 评论数
    review_num = ""
    review_num_list = html("#acrCustomerReviewText").items()
    for rn in review_num_list:
        review_num = rn.text()
        break
    if review_num != "":
        review_num = review_num.split(" ")[0]

    # 排名
    rank1 = ""
    rank2 = ""
    tr_list = html("#productDetails_detailBullets_sections1 tr").items()
    for tr in tr_list:
        if "Rank" in tr("th").text():
            rank1 = tr("td > span > span:nth-child(1)").text().strip()
            rank2 = tr("td > span > span:nth-child(3)").text().strip()
            break
    if rank1 == "":
        first_rank = html("#SalesRank")
        if first_rank("b"):
            rank2 = html("#SalesRank > ul").text().replace("\xa0", "")
            first_rank.remove("b")
            first_rank.remove("ul.zg_hrsr")
            first_rank.remove("style")
            rank1 = first_rank.text()
        else:
            first_rank = html("div.attrG tr#SalesRank > td.value")
            rank2 = html("div.attrG tr#SalesRank > td.value ul.zg_hrsr").text().replace("\xa0", "")
            first_rank.remove("ul.zg_hrsr")
            first_rank.remove("style")
            rank1 = first_rank.text()
    if rank1 == "":
        b_html = BeautifulSoup(page_source, 'lxml')
        tr_list = b_html.select("#productDetails_detailBullets_sections1 tr")
        for tr in tr_list:
            if 'Rank' in tr.th.text:
                rank1_list = tr.select("td > span > span:nth-child(1)")
                if rank1_list:
                    rank1 = rank1_list[0].text.strip()
                rank2_list = tr.select("td > span > span:nth-child(3)")
                if rank2_list:
                    rank2 = rank2_list[0].text.strip()

    rank_regex = re.compile("\d(.*?)\s")
    if rank1 != "":
        rank1 = rank_regex.search(rank1).group()
    if rank2 != "":
        rank2 = rank_regex.search(rank2).group()

    score = html("span[data-hook=rating-out-of-text]").text()
    if score == "":
        try:
            score = list(html("#acrPopover > span.a-declarative > a span").items())[0].text()
        except Exception as e:
            score = ""
    if score != "":
        score = score.split(" ")[0].replace(",", ".")

    asin = ''
    attr_list.append(asin)
    attr_list.append(z_img)
    attr_list.append(title)
    attr_list.append(price)
    attr_list.append(score)
    attr_list.append(int(review_num.strip().replace(',', '')) if review_num else 0)
    attr_list.append(int(rank1.strip().replace(',', '')) if rank1 else 0)
    attr_list.append(rank2)

    return attr_list


# 调用
if __name__ == '__main__':
    options = webdriver.ChromeOptions()

    '''
    参数
        1.[binary_location]chrome.exe执行路径的地址  
        2.[user-data-dir]chrome用户配置的地址->显示插件。地址栏输入chrome://version/查看浏览器信息。注：到User Data就结束了。程序运行过程中要关闭chrome浏览器！！
        3.[executable_path]selenium驱动地址
        4.[excel_path]源excel文件目录地址
    '''
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # 指定这个目录才会打开安装的插件
    options.add_argument("--user-data-dir=" + r"C:\\Users\\****\\AppData\\Local\\Google\\Chrome\\User Data\\")

    options.add_argument('--disable-gpu')
    options.add_argument("disable-web-security")
    options.add_argument('disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(executable_path="C:\\Python39\\taobao\\chromedriver_win32\\chromedriver_update.exe",
                              chrome_options=options)

    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
    row = 2

    excel_path = "F:\\dhq_py_code\\awesome-python-login-model\\validateCode\\ASIN_list.xlsx"
    df = pd.DataFrame(pd.read_excel(excel_path, engine='openpyxl'))
    print(len(df))
    for i in range(0, len(df)):  # 取长度
        asin = df.iloc[i][0]  # iloc函数 模板df.iloc[第几行][第几列]
        brand = df.iloc[i][1]  # iloc函数 模板df.iloc[第几行][第几列]

        url = str.format("https://www.amazon.com/OMYSTYLE-FASHION-Organizer-Handbag-Neverfull/dp/%s" % asin)

        js = 'window.open("' + url + '?language=en_US");'
        driver.execute_script(js)

        # 网页窗口句柄集
        handles = driver.window_handles
        # 进行网页窗口切换
        driver.switch_to.window(handles[-1])

        page_source = driver.page_source
        info_list = parse_detail(driver.page_source)
        info_list.append(driver.current_url)
        # 库存
        stockNum = '0';
        try:
            stock = wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="sellersprite-extension-Inventory-surpluscont"]/div[2]/div[1]/div[2]/span/span'))
            )
            stockNum = stock.text
            time.sleep(2)
        except TimeoutException:
            stockNum = '--'

        # 商品唯一编码{()}
        asin_regex = re.compile('/dp/(.*?)\?')
        asin = asin_regex.findall(driver.current_url)[0]
        info_list[0] = asin
        info_list.append(stockNum)

        print(info_list)

        # 组转excel数据
        # STOCK
        df.loc[i] = [asin, brand, 'size', 'color', stockNum]
        driver.close()
        driver.switch_to.window(handles[0])
    # 保存数据
    DataFrame(df).to_excel('result.xlsx', index=False, header=True)
    print("爬取结束")
