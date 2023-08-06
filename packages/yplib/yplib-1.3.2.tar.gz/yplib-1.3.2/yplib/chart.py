from yplib.chart_html import *
from yplib.index import *


# 将 html 中的占位符 替换成数据
# 并且 导出 生成后的 html 文件
def insert_data_to_chart(html_data='',
                         name=None,
                         x_list=None,
                         y_list=None,
                         legend=None,
                         series=None,
                         smooth=0):
    p_list = [
        'chart_name', 'name', 'x_list', 'y_list', 'legend', 'series', 'smooth'
    ]
    p_data_list = [
        name, name, x_list, y_list, legend, series, smooth
    ]
    for index in range(len(p_list)):
        one_p = p_list[index]
        one_data = p_data_list[index]
        if one_data is None:
            continue
        one_p = f'-{one_p}-'
        if one_p in html_data:
            html_data = html_data.replace(one_p, str(one_data))
    to_txt(list_data=[html_data],
           file_name=str(name),
           file_path='html',
           fixed_name=False,
           suffix='.html')
    # current_path = os.path.abspath(__file__)
    # html_list = open(current_path[0:current_path.find('__init__')] + 'line-stack-temp.html', 'r', encoding='utf-8').readlines()


# 将数据整理成折线图
#  x轴数据 : x_list = [
#       ['x轴的数据', 'line1', 'line2', 'line3'],
#       ['2020-01-01', 120, 132, 101],
#       ['2020-01-02', 100, 102, 131],
#       ['2020-01-03', 123, 165, 157],
#       ['2020-01-04', 126, 109, 189],
#       ['2020-01-05', 150, 156, 128],
#       ['2020-01-06', 178, 134, 140],
#       ['2020-01-07', 157, 148, 161],
#  ]
#  --- 以上这种情况,当 y_list 为空的时候,就说明有可能是这种情况
#  --- 以上这种情况,数据与 excel 中的数据对齐
#  --- 以下是第二种情况的 api
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#             {
#                 name: 'Email',
#                 hide: False,
#                 smooth: True,
#                 data: [120, 132, 101, 134, 90, 230, 210],
#             },
#             {
#                 name: 'Union Ads',
#                 hide: 0,
#                 smooth: False,
#                 data: [220, 182, 191, 234, 290, 330, 310],
#             },
#             {
#                 name: 'Video Ads',
#                 hide: True,
#                 data: [150, 232, 201, 154, 190, 330, 410],
#             },
#             {
#                 name: 'Direct',
#                 data: [320, 332, 301, 334, 390, 330, 320],
#             },
#             {
#                 name: 'Search Engine',
#                 data: [820, 932, 901, 934, 1290, 1330, 1320],
#             },
#         ]
#  name : 文件名称,折线图的名称
#  name_raw : 用原始的名字,不用带上属性 line_stack
def to_chart(x_list, y_list=None, name=None, name_raw=False):
    if y_list is None:
        list_data = x_list
        x_list = []
        y_list = []
        index = 0
        for line_one in list_data:
            if index > 0:
                x_list.append(line_one[0])
            # 第一行数据
            if index == 0:
                for y in range(len(line_one) - 1):
                    y_list.append({'name': line_one[y + 1], 'data': []})
            # 第二行开始的数据
            if index > 0:
                for y in range(len(line_one) - 1):
                    y_list[y]['data'].append(line_one[y + 1])
            index += 1
    legend_data = []
    legend_selected = {}
    for y_one in y_list:
        legend_data.append(y_one['name'])
        if 'hide' in y_one:
            legend_selected[y_one['name']] = 0
    legend = "data : " + str(legend_data) + ", selected : " + str(legend_selected)
    # {
    #     name: 'Email',
    #     type: 'line',
    #     stack: 'Total',
    #     data: [120, 132, 101, 134, 90, 230, 210],
    # }
    series = []
    for y_one in y_list:
        y_one['type'] = 'line'
        y_one['stack'] = 'Total'
        if 'smooth' in y_one:
            y_one['name'] = 1
        series.append(y_one)

    if name_raw is False:
        name = 'line_stack' if name is None else name + '_line_stack'
    insert_data_to_chart(html_data=line_stack_html(),
                         name=name,
                         x_list=x_list,
                         legend=legend,
                         series=series)


# 将数据整理成折线图
# 一条折线
# 数据 : data_list = [
#             ['2020-01-01', 132],
#             ['2021-01-01', 181],
#             ['2022-01-01', 147]
#         ]
# x_index : x 轴数据的下标
# y_index : y 轴数据的下标
# smooth : 曲线是否平滑
def to_chart_one(list_data, name=None, is_area=False, x_index=0, y_index=1, smooth=False):
    x_list = []
    y_list = []
    name = 'line' if name is None else name + '_line'
    for d_one in list_data:
        x_list.append(d_one[x_index])
        y_list.append(d_one[y_index])
    if is_area:
        sm = 1 if smooth else 0
        name += '_area'
        if smooth:
            name += '_smooth'
        insert_data_to_chart(html_data=line_area_html(),
                             name=name,
                             x_list=x_list,
                             y_list=y_list,
                             smooth=sm)
    else:
        sm = 0
        if smooth:
            sm = 1
            name += '_smooth'
        to_chart(x_list, [{'name': name, 'data': y_list, 'smooth': sm}], name=name, name_raw=True)


# legend_data.append(y_one['name'])
#     if 'hide' in y_one:
#         legend_selected[y_one['name']] = 0
# legend = "data : " + str(legend_data) + ", selected : " + str(legend_selected)
# # {
# #     name: 'Email',
# #     type: 'line',
# #     stack: 'Total',
# #     data: [120, 132, 101, 134, 90, 230, 210],
# # }
# series = []
# for y_one in y_list:
#     y_one['type'] = 'line'
#     y_one['stack'] = 'Total'
#     series.append(y_one)
#
# insert_data_to_chart(html_data=line_stack_html(),
#                      name=name,
#                      x_list=x_list,
#                      legend=legend,
#                      series=series)


# 将数据整理成饼状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
def to_chart_pie(list_data, name=None, name_index=0, value_index=1):
    x_list = []
    name = 'pie' if name is None else name + '_pie'
    if isinstance(list_data[0], list):
        for one_data in list_data:
            x_list.append({'name': one_data[name_index], 'value': one_data[value_index]})
    else:
        for one_data in list_data:
            # 有多余的属性,就只保留这两个
            x_list.append({'name': one_data['name'], 'value': one_data['value']})
    insert_data_to_chart(html_data=pie_html(),
                         name=name,
                         x_list=x_list)


# 将数据整理成柱状图
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
# 或者
# 数据 : data = [
#        {x: "Search Engine", y: 1048 },
#        {x: "Direct", y: 735 },
#        {x: "Email", y:580 },
#        {x: "Union Ads", y:484 },
#        {x: "Video Ads", y:300 }
#       }]
def to_chart_bar(list_data, name=None, x_index=0, y_index=1):
    x_list = []
    y_list = []
    name = 'bar' if name is None else name + '_bar'
    for one in list_data:
        if isinstance(one, list):
            x_list.append(one[x_index])
            y_list.append(one[y_index])
        else:
            x_list.append(one['x'])
            y_list.append(one['y'])

    insert_data_to_chart(html_data=bar_html(),
                         name=name,
                         x_list=x_list,
                         y_list=y_list)


# data = []
# # for i in range(10):
# #     data.append([uuid_random(), int(random.uniform(0, 1000))])
# for i in range(10000):
#     one = {}
#     one['x'] = uuid_random()
#     one['y'] = int(random.uniform(0, 1000))
#     data.append(one)
#
# to_chart_bar(data)

#
#
# data = []
# # for i in range(10):
# #     data.append([uuid_random(), int(random.uniform(0, 1000))])
# for i in range(10):
#     data.append([random_uuid(), int(random.uniform(0, 1000))])
#
# to_chart_pie(data)
# to_chart_pie(data, 'yp')

# x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y_list = json.loads(
#     '[{"name":"Email","data":[120,132,101,134,90,230,210]},{"name":"Union Ads","data":[220,182,191,234,290,330,310]},{"name":"Video Ads","data":[150,232,201,154,190,330,410]},{"name":"Direct","data":[320,332,301,334,390,330,320]},{"name":"Search Engine","data":[820,932,901,934,1290,1330,1320]}]')
#

# # # 将 list 转化成 图表的例子
# x_list = []
# y_list = []
# # # x 轴有 100 个
# # # 100 个横坐标
# for i in range(100):
#     x_list.append(i)
# #
# # 有 10 条线
# for i in range(1):  # 0 1 2 3 4 55
#     n = {}
#     n['name'] = str(int(random.uniform(0, 1000)))
#     data = []
#     # 每条线有 100 个纵坐标, 与 x_list 中的对应起来
#     for i in range(100):
#         data.append(int(random.uniform(0, 1000)))
#     n['data'] = data
#     # n['hide'] = '1'
#     y_list.append(n)
# #
# to_chart(x_list, y_list)
#
#
# data_list = []
# for i in range(100):
#     data_list.append([i, int(random.uniform(0, 1000))])
#
# to_chart_one(data_list, name='yp')
# to_chart_one(data_list, name='yp', smooth=True)
# to_chart_one(data_list, name='yp', is_area=True)
# to_chart_one(data_list, name='yp', is_area=True, smooth=True)
#
# data_list =
#
# to_chart(data_list)

# to_chart(to_list(r'C:\Users\yangpu\Desktop\study\12.xls'))

#
# print('end')
