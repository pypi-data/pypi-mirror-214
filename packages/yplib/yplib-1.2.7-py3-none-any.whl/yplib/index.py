import json
import os
import uuid
from datetime import datetime
from datetime import timedelta

import xlrd
import xlwt
import time
import re
import random
import hashlib


# 记录日志, 如果是对象会转化为 json
def to_log(a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
           a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    l = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,
         a11, a12, a13, a14, a15, a16, a17, a18, a19, a20]
    d = ''
    for one in l:
        if can_use_json(one):
            o = json.dumps(one)
        else:
            o = str(one)
        if o != '':
            d = d + ' ' + o
    lo = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + d
    print(lo)
    return lo


# 将 log 数据, 写入到文件
def to_log_file(a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
                a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    lo = to_log(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20)
    to_txt([lo], datetime.today().strftime('%Y-%m-%d'), 'log', True, '.log')


# 将 log 数据, 写入到固定文件中
def to_log_txt(file_name, a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
               a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    lo = to_log(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20)
    to_txt([lo], file_name, 'log', True, '.txt')


# 将下划线命名转成驼峰命名
# 例如 : user_id -> userId
# 例如 : USER_ID -> userId
def to_hump(a1=''):
    if a1 == '':
        return a1
    a1 = a1.lower()
    words = a1.split('_')
    r = ""
    for w in words:
        r += w.capitalize()
    return r[0].lower() + r[1:]


def to_hump_more(a1='', a2='', a3='', a4='', a5=''):
    if a1 == '':
        return a1
    elif a2 == '':
        return to_hump(a1)
    elif a3 == '':
        return to_hump(a1), to_hump(a2)
    elif a4 == '':
        return to_hump(a1), to_hump(a2), to_hump(a3)
    elif a5 == '':
        return to_hump(a1), to_hump(a2), to_hump(a3), to_hump(a4)
    return to_hump(a1), to_hump(a2), to_hump(a3), to_hump(a4), to_hump(a5)


# 将驼峰命名转成下划线命名
# 例如 : userId -> user_id
def to_underline(a1=''):
    if a1 == '':
        return a1
    r = ''
    for char in a1:
        if char.isupper():
            r += '_' + char.lower()
        else:
            r += char
    return r


def to_underline_more(a1='', a2='', a3='', a4='', a5=''):
    if a1 == '':
        return a1
    elif a2 == '':
        return to_underline(a1)
    elif a3 == '':
        return to_underline(a1), to_underline(a2)
    elif a4 == '':
        return to_underline(a1), to_underline(a2), to_underline(a3)
    elif a5 == '':
        return to_underline(a1), to_underline(a2), to_underline(a3), to_underline(a4)
    return to_underline(a1), to_underline(a2), to_underline(a3), to_underline(a4), to_underline(a5)


# 是否能用 json
def can_use_json(data):
    if isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set):
        return True
    return False


# 检查文件夹是否存在,不存在,就创建新的
def check_file(file_name):
    if file_name != '' and os.path.exists(file_name) is False:
        os.mkdir(file_name)


# 获得文件名称
def get_file_name(file_name, suffix='.txt'):
    return str(file_name) \
        + '_' + datetime.today().strftime('%Y%m%d_%H%M%S') \
        + '_' + uuid_random()[0:5] \
        + suffix


def do_md5(data='do_md5'):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def do_sha256(data='do_sha256'):
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))
    return h.hexdigest()


def uuid_random(length=32):
    r = uuid.uuid4().hex
    while len(r) < length:
        r += uuid.uuid4().hex
    return r[0:length]


# 去掉 str 中的 非数字字符, 然后, 再转化为 int
def to_int(s):
    if s is None or s == '':
        return 0
    if isinstance(s, float):
        return int(s)
    s = ''.join(filter(lambda ch: ch in '0123456789', str(s)))
    if s == '':
        return 0
    return int(s)


# 去掉 str 中的 非数字字符, 然后, 再转化为 float
def to_float(s):
    if s is None or s == '':
        return 0.0
    s = ''.join(filter(lambda ch: ch in '0123456789.', str(s)))
    if s == '':
        return 0.0
    return float(s)


def to_datetime(s=None, return_str=False):
    if s is None or s == '':
        return datetime.today()
    s = str(s)
    r = datetime.today()
    m_s = {
        "^\\d{4}$": "%Y",
        "^\\d{4}-\\d{1,2}$": "%Y-%m",
        "^\\d{4}-\\d{1,2}-\\d{1,2}$": "%Y-%m-%d",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}$": "%Y-%m-%d %H",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}$": "%Y-%m-%d %H:%M",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}$": "%Y-%m-%d %H:%M:%S",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}.\\d{1,9}$": "%Y-%m-%d %H:%M:%S",
    }
    for m in m_s:
        if re.match(m, s):
            r = datetime.strptime(s.split('.')[0], m_s[m])
    if re.match("^\\d{1,13}$", s):
        s_int = int(s)
        if len(s) > 10:
            s_int = int(s_int / 1000)
        time_arr = time.localtime(s_int)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_arr)
        r = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    if return_str:
        return str(r)
    return r


# 时间加几天
def datetime_add(s=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return to_datetime(s) + timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours,
                                      weeks=weeks)


def to_date(s=None):
    return str(to_datetime(s))[0:10]


def date_add(s=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return str(datetime_add(s=s, days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours,
                            weeks=weeks))[0:10]


# 将 list 中的数据以 json 或者基本类型的形式写入到文件中
# list_data : 数组数据, 也可以不是数组
# file_name : 文件名
# fixed_name : 是否固定文件名
# file_path : 文件路径
def to_txt(list_data, file_name='txt', file_path='txt', fixed_name=False, suffix='.txt'):
    file_name = str(file_name)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    if fixed_name:
        file_name = file_name + suffix
    else:
        file_name = get_file_name(file_name, suffix)
    file_name_path = file_name
    if file_path != '':
        file_name_path = file_path + '/' + file_name
    text_file = open(file_name_path, 'a', encoding='utf-8')
    if isinstance(list_data, list) is False:
        text_file.write(to_str(list_data) + '\n')
    else:
        for one in list_data:
            text_file.write(to_str(one) + '\n')
    text_file.close()
    return file_name_path


# 将 list 中的数据写入到固定的文件中,自己设置文件后缀
def to_txt_data(list_data, file_name='data'):
    return to_txt(list_data, file_name, 'data', True)


def to_str(data):
    if can_use_json(data):
        s = json.dumps(data)
    else:
        s = str(data)
    return s


# 根据json的key排序,用于签名
def sort_by_json_key(data):
    key_list = list()
    for one_data in data:
        key_list.append(one_data)
    key_list.sort()
    result = ''
    for one_data in key_list:
        result += one_data + '=' + data[one_data] + '&'
    if len(result) > 0:
        return result[0: -1]


# 将 txt 文件读取到 list 中, 每一行自动过滤掉行前,行后的空格
def to_list(file_name='a.txt', sheet_index=0):
    if file_name is None or file_name == '' or os.path.exists(file_name) is False:
        return []
    data_list = list()
    # excel 表格解析成 list 数据
    if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
        book = xlrd.open_workbook(file_name)  # 打开一个excel
        sheet = book.sheet_by_index(sheet_index)  # 根据顺序获取sheet
        for i in range(sheet.nrows):  # 0 1 2 3 4 5
            rows = sheet.row_values(i)
            row_data = []
            for j in range(len(rows)):
                row_data.append(str(rows[j]).strip())
            data_list.append(row_data)
        return data_list
    # 普通文件的解析
    file = open(file_name, 'r', encoding='utf-8')
    for line in file.readlines():
        line = line.strip()
        data_list.append(line)
    return data_list


def to_excel(list_data, file_name, file_path='excel'):
    file_name = str(file_name)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 2. 创建Excel工作薄
    w_b = xlwt.Workbook()
    # 3. 添加Excel工作表
    sh = w_b.add_sheet(str(file_name))
    # 4. 写入数据
    # myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')  # 数据格式
    m = 0
    for one_data in list_data:
        n = 0
        if isinstance(one_data, list):
            for one in one_data:
                # mySheet.write(n, m, one)  # 写入A3，数值等于1
                if isinstance(one, dict) or isinstance(one, list):
                    s = json.dumps(one)
                else:
                    s = str(one)
                sh.write(m, n, s)  # 写入A3，数值等于1
                n += 1
        else:
            if can_use_json(one_data):
                s = json.dumps(one_data)
            else:
                s = str(one_data)
            sh.write(m, n, s)  # 写入A3，数值等于1
        m += 1
    # 5. 保存
    # myWorkbook.save('5002200.xls')
    w_b.save(file_path + '/' + get_file_name(file_name, '.xls'))

# print('start')
# to_txt([1,2,3], 'p')
# to_txt_file_name([1,2,3], 'p')
#
#
# li = to_list('D:\code\python3\packaging_tutorial\yplib\data\p_20230612_095450_34779.txt')
#
# to_log()
#
# to_log()
# to_log(1)
# to_log(1, 2)
# to_log(1, 2, [1, 2])
# to_log_file(1, 2, [{'a': 2}])
# to_log_txt('1.txt', 1, 2, [{'a': 2}])
# to_txt([{'a': 2}])
# to_txt_data('yangpu', 1)
# to_txt_data('yangpu1', 1)
# to_txt_data('yangpu12', 1)
#
# x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y_list = json.loads(
#     '[{"name":"Email","data":[120,132,101,134,90,230,210]},{"name":"Union Ads","data":[220,182,191,234,290,330,310]},{"name":"Video Ads","data":[150,232,201,154,190,330,410]},{"name":"Direct","data":[320,332,301,334,390,330,320]},{"name":"Search Engine","data":[820,932,901,934,1290,1330,1320]}]')
#

# # 将 list 转化成 图表的例子
# x_list = []
# y_list = []
# # x 轴有 100 个
# # 100 个横坐标
# for i in range(100):
#     x_list.append(i)
#
# # 有 10 条线
# for i in range(10):  # 0 1 2 3 4 55
#     n = {}
#     n['name'] = str(int(random.uniform(0, 1000)))
#     data = []
#     # 每条线有 100 个纵坐标, 与 x_list 中的对应起来
#     for i in range(100):
#         data.append(int(random.uniform(0, 1000)))
#     n['data'] = data
#     y_list.append(n)
# #
# to_chart(x_list, y_list)
#
# to_txt_data(x_list, 'operate')
# to_txt_data(y_list, 'operate')

# to_log_file(1)
# log_to_file(12)
# log_to_file('yangpu')
# print(str_to_int('yan123gpu'))
# print(str_to_float('yan123gpu'))
# print(str_to_float('yan123g.12pu'))

#
# print(to_hump('user_id'))
# print(to_hump('USER_ID'))
# print(to_hump('userId'))
# print(to_hump('user'))
# print(to_hump(''))

# print(to_hump_more('userId'))

# print(to_underline('userId'))


# print(uuid_random(5))
# print(uuid_random(10))
# print(uuid_random())
# print(uuid_random(32))
# print(uuid_random(64))
# print(uuid_random(128))
# print(uuid_random(127))
# print(uuid_random(129))


# print(to_int('a'))
# print(to_int(2))
# print(to_int(2.2))
# print(to_int(2.2))

# print(to_float('a'))
# print(to_float(2))
# print(to_float(2.2))
# print(to_float(2.24))

# print(to_date('2019-09'))
# print(to_date('2019-09-08'))
# print(to_date('2019-09-08 12'))
# print(to_date('2019-09-08 12:13'))
# print(to_datetime('2019-09-08 12:13:14'))
# print(to_datetime('2019-09-08 12:13:14.789'))
# print(to_datetime(1686537485))
# print(to_datetime(1686537484467))
# print(to_datetime(datetime.today()))
#
# print(do_md5())
# print(do_md5())
# print(do_md5('yangpu'))
# print(do_md5('yangpu12'))
#
# log_msg = ''
# headers = {'Content-Type': 'application/json;charset=utf-8'}
# data = {}
# data['merchantId'] = "merchantId"
# data['currency'] = "IDR"
# data['accType'] = "payout"
# data['version'] = "1.0"
# sign = sort_by_json_key(data)
# print(sign)
# hash = hashlib.sha256()
# hash.update(sign.encode('utf-8'))
# data['sign'] = hash.hexdigest()
#
# print(data)


# print(get_file_data_line(r'D:\notepad_file\202306\fasdfsadfaf.txt', 'payout', from_last=False))

# get_file_data_line(r'D:\notepad_file\202306', 'a')
# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))


# print('end')
