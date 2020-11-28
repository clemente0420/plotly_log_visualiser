
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import re
from pprint import pprint
import numpy as np
import time 

TemDict = {"last_week":{},"this_week":{}}

def TextSniffing(TemDict):
    for root, dirs, files in os.walk(".", topdown=True):
        MatchDir = re.match( './', root)
        # 匹配 & 过滤文件为空的目录
        if MatchDir and files:
            # print("aaaa {}".format(root))
            TemDict[root[2:11]].update( { root[12:]:["{}/{}".format(root,elemente) for elemente in files] } )
    return TemDict



def TextReader(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = lines[:-1]
        dictA={}
        for line in lines:
            a = line.split(' $ ')
            if a[0] and a[-1][:-4]:
                # print(a[0],'    ',a[-1][:-4])
                if dictA.get(a[0]):
                    dictA[a[0]].append(a[-1][:-4])
                else:
                    dictA[a[0]] = [a[-1][:-4]]
            else:
                pass
        # print(dictA.keys())
        # {module:[value, ...]}
        return dictA


# 示例
# >>> one={'a': [1, 2], 'c': [5, 6], 'b': [3, 4]}
# >>> two={'a': [2.4, 3.4], 'c': [5.6, 7.6], 'b': [3.5, 4.5]}
# >>> three={'a': 1.2, 'c': 3.4, 'b': 2.3}
# >>> {key: value + two[key] + [three[key]] for key, value in one.iteritems()}
# {'a': [1, 2, 2.4, 3.4, 1.2], 'c': [5, 6, 5.6, 7.6, 3.4], 'b': [3, 4, 3.5, 4.5, 2.3]}


def WeekSeparate(TemDict, last_week_List, this_week_List):
    for week, spec_date_dict in TemDict.items():
        for spec_date, files_list in spec_date_dict.items():
            # print(len(files_list))
            for file_path in files_list:
                if file_path[2:11] == "last_week":
                    last_week_List.append(TextReader(file_path))
                elif file_path[2:11] == "this_week":
                    this_week_List.append(TextReader(file_path))


def Pretreatment(data_list):
    dictA = {}
    for elemente_dict in data_list:
        for key in elemente_dict:
            if key in dictA:
                dictA[key].extend(elemente_dict[key])
            else:
                dictA[key] = elemente_dict[key]
    return dictA



def data_processing(data_dict):
    for key ,value in data_dict.items():
        tem_value = np.array(data_dict[key],dtype = 'float64')
        data_dict[key] = [np.mean(tem_value),np.std(tem_value)]
    # 返回{module:[均值，标准差], ...}
    return data_dict
    

def dict_merge(Adict,Bdict):
    final_dict = { key:[] for key in Adict.keys() & Bdict.keys() }
    for key in final_dict:
        final_dict[key].extend(Adict[key])
        final_dict[key].extend(Bdict[key])
    return final_dict

def list_factory(data):
    x_list= []
    last_y_list=[]
    this_y_list =[]
    for key in data:
        # print(data[key])
        x_list.append(key)
        last_y_list.append(data[key][0])
        this_y_list.append(data[key][2])
    return x_list, last_y_list, this_y_list

last_week_List = [] # 每一个txt文本解析后的{module:[value, ...]} 有多少天就有多少个dict
this_week_List = [] # 每一个txt文本解析后的{module:[value, ...]}

TimeLogDict = TextSniffing(TemDict)
pprint(TimeLogDict)
WeekSeparate(TimeLogDict,  last_week_List,  this_week_List)


last_week_Dict =Pretreatment(last_week_List)
this_week_Dict =Pretreatment(this_week_List)

last_week_stat_describe= data_processing(last_week_Dict)
this_week_stat_describe= data_processing(this_week_Dict)
# pprint(last_week_stat_describe)
# print("\n")
# pprint(this_week_stat_describe)

data = dict_merge(last_week_stat_describe, this_week_stat_describe)

print(len(data))
x,y1,y2 = list_factory(data)
# x 为 模块函数名
# y1 上一周的特征结果
# y2 这周的特征结果




# import numpy as np
# a = {"a":[10,20],"b":[22,33]}
# for key ,value in a.items():
#     a[key] = [np.mean(a[key]),np.std(a[key])]

# print(a)

# dic1 = {'A': [25,11], 'B': 41, 'C': 32}
# dic2 = {'A': [21,22], 'd': 12, 'C': 62}
# print(dic1.keys() & dic2.keys())
# result = {}
# for key in (dic1.keys() & dic2.keys()):
#     if key in dic1:
#         result.setdefault(key, []).append(dic1[key])
#     if key in dic2:
#         result.setdefault(key, []).append(dic2[key])

# print (result)

# Creating two subplots
fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=True, vertical_spacing=0.001)





difference_y_net = list(map(lambda x: (x[0]-x[1]), zip(y2, y1)))
print(max(difference_y_net))
print(sorted(difference_y_net)[-2])
print(x[difference_y_net.index(max(difference_y_net))])
# print(len(x))
# print("dddddddddddddddddddddddd")
# pprint(difference_y_net)
# print(len(difference_y_net))
fig.append_trace(go.Bar(
    x= difference_y_net,
    y= x,
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),
    name='2019年08月第4周同比增减 (ms)',
    orientation='h',
), 1, 1)


# fig.append_trace(go.Bar(
#     x=2*y_saving,
#     y=x,
#     marker=dict(
#         color='rgba(150, 171, 96, 0.6)',
#         line=dict(
#             color='rgba(150, 171, 96, 1.0)',
#             width=1),
#     ),
#     name='20190821 条形占比',
#     orientation='h',
# ), 1, 1)



fig.append_trace(go.Scatter(
    x=y1, y=x,
    mode='lines+markers',
    line_color='rgb(128, 0, 128)',
    name='2019年08月第3周平均 (ms)',
), 1, 2)

fig.append_trace(go.Scatter(
    x=y2, y=x,
    mode='lines+markers',
    line_color='rgb(255, 165, 0)',
    name='2019年08月第4周平均 (ms)',
), 1, 2)



# difference_net = list(map(lambda x: (x[0]* x[1]) ,zip(difference_y_net, y1)))
# rising_module = x[difference_net.index(max(difference_net))]
# rising_rate = difference_y_net[difference_net.index(max(difference_net))]


positive_rising_module = x[difference_y_net.index(max(difference_y_net))]
# rising_rate = difference_y_net[difference_net.index(max(difference_net))]
negative_rising_module = x[difference_y_net.index(min(difference_y_net))]
fig.update_layout(
    title="<b>{} 各模块函数耗时平均 (ms)</b><br><br>值得关注的模块<b><br>'{}',均次增加耗时<b>{:.1f}ms</b><br><b>'{}'</b>,均次耗时减少<b>{:.1f}ms</b>"\
        .format("2019年08月第3周至第4周",positive_rising_module,max(difference_y_net),negative_rising_module, min(difference_y_net)),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.95],
    ),
    yaxis2=dict(
        showgrid=False,
        showline=True,
        showticklabels=False,
        linecolor='rgba(102, 102, 102, 0.8)',
        linewidth=2,
        domain=[0, 0.95],
    ),
    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.42],
    ),
    xaxis2=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.47, 1],
        side='top',
        dtick=2500,
    ),
    legend=dict(x=0.605, y=1.038, font_size=14),
    margin=dict(l=30, r=20, t=70, b=70),
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
    autosize=False,
    width=1800,
    height=1200,
)

annotations = []

y_s = np.round(difference_y_net, decimals=4)
y_nw = np.rint(y1)

# Adding labels
for ydn, yd, xd in zip(y_nw, y_s, x):
    # labeling the scatter savings
    annotations.append(dict(xref='x2', yref='y2',
                            y=xd, x=ydn,
                            text='{:,}'.format(ydn) + 'ms',
                            font=dict(family='Arial', size=12,
                                      color='rgb(128, 0, 128)'),
                            showarrow=False))
    # labeling the bar net worth
    annotations.append(dict(xref='x1', yref='y1',
                            y=xd, x=yd+0.4,
                            # text=str(yd * 100) + '%',
                            text=str(yd) + 'ms',
                            font=dict(family='Arial', size=12,
                                      color='rgb(50, 171, 96)'),
                            showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper',
                        x=-0.2, y=-0.109,
                        text='OECD "' +
                             '(2015), Household savings (indicator), ' +
                             'Household net worth (indicator). doi: ' +
                             '10.1787/cfc6f499-en (Accessed on 05 June 2015)',
                        font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                        showarrow=False))

fig.update_layout(annotations=annotations,
                  template="plotly_white")

fig.show()

