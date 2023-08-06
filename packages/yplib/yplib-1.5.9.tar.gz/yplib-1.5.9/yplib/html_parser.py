from yplib.index import *
from bs4 import BeautifulSoup


# 解析 html 中的数据
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
