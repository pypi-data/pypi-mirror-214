from yplib.index import *
from bs4 import BeautifulSoup
import requests
# from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 有关 http 的工具类

# 解析 html 中的数据
# file_path :   html 文件的路径
# html_data :   html 数据
# selector  :   选择器
def do_parser(file_path=None, html_data='', selector=None):
    if file_path is not None:
        html_str = ''.join(to_list(file_path))
    else:
        if isinstance(html_data, list):
            html_str = ''.join(html_data)
        else:
            html_str = str(html_data)
    return BeautifulSoup(html_str, 'html.parser').select(selector)


# div_list_content = do_parser(r'D:\notepad_file\202306\asfdf.html', selector='table.reference')[4].select('tr')
#
# for i in range(len(div_list_content) - 1):
#     td = div_list_content[i + 1].select('td')
#     num = td[0].text
#     fun_name = td[1].select('a')[0].text
#     fun_desc = td[1].text.replace(fun_name, '')
#     print(f'{num} : {fun_name} , {fun_desc}')


# get 类型的请求
# headers :
# cookie  :
# auth    :
# verify  :
def do_get(url=None,
           headers=None,
           cookie=None,
           auth=None,
           timeout=10,
           verify=False):
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)
    response.encoding = 'utf-8'
    return response.text.strip()

# print(do_get('https://www.runoob.com/?s=sorted'))