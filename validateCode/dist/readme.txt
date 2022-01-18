===============================================
参数说明
        1.[binary_location]chrome.exe执行路径的地址
        2.[user-data-dir]chrome用户配置的地址->显示插件。地址栏输入chrome://version/查看浏览器信息。注：到User Data就结束了。程序运行过程中要关闭chrome浏览器！！
        3.[executable_path]selenium驱动地址 : https://blog.csdn.net/llbacyal/article/details/78563992
        4.[excel_path]源excel文件目录地址，N行5列.【ASIN 品牌 尺寸 颜色 库存】
"C:\******\Google\Chrome\Application\chrome.exe"
"C:\\Users\\******\\AppData\\Local\\Google\\Chrome\\User Data\\"
"C:\\Python39\\taobao\\chromedriver_win32\\chromedriver_update.exe"
"F:\\*****\\awesome-python-login-model\\validateCode\\ASIN_list.xlsx"
===============================================
在cmd下执行这个命令，后面用空格接上4个参数,根据本地电脑目录修改。
.\amazon_detail.exe "C:\******\chrome.exe" "C:\\Users\\*****\\AppData\\Local\\Google\\Chrome\\User Data\\" "C:\\****\\chromedriver_update.exe" "F:\\*****\\ASIN_list.xlsx"