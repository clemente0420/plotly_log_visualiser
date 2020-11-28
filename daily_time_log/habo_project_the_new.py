
import os
import re
from pprint import pprint
import numpy as np
from scipy import signal
import plotly.offline as py
import plotly.tools as plotly_tools
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import pandas as pd
from tabulate import tabulate


interval = 3
average_threshold = 20
TemDict = {}
DictB = {}
Entire_Dict={}


def TextSniffing(TemDict):
    for root, dirs, files in os.walk(".", topdown=True):
        MatchDir = re.match( './time_log', root)
        if MatchDir:
            TemDict[root[2:]] = ["{}/{}".format(root,elemente) for elemente in files]
            #print("{}: {}".format(root[2:],files))
    return TemDict


# def TextReader(filepath):
#     with open(filepath, 'r') as f:
#         line = f.readline()
#         line = line[:-1]
#         dictA={}
#         while line:
#             line = f.readline()
#             a = line.split(' $ ')
#             if a[0] and a[-1][:-4]:
#                 # print(a[0],'    ',a[-1][:-4])
#                 if dictA.get(a[0]):
#                     dictA[a[0]].append(a[-1][:-4])
#                 else:
#                     dictA[a[0]] = [a[-1][:-4]]
#             else:
#                 pass
#         print(dictA.keys())
#         return dictA

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
        return dictA

# def ThresholdFilter(rawDict,average_threshold):
#     DictC = {}
#     for key, value in rawDict.items():
#         #print(key,value[0])
#         for k , v in value.items():
#         # tem_value = np.array(rawDict[key],dtype = 'float64')
#             average_value = np.mean(v)
#             if average_value >= average_threshold:
#                 DictC[k]=value
#     return DictC
def ThresholdFilter(rawDict,average_threshold):
    DictC = {}
    for file_name, file_value_dict in rawDict.items():
        #print(key,value[0])
        for key , value in file_value_dict.items():
        # tem_value = np.array(rawDict[key],dtype = 'float64')
            average_value = np.mean(value)
            if average_value >= average_threshold:
                DictC[file_name][key]= value
    return DictC



def Talulate_Writer(statistics_dict):
    relation_pd = pd.DataFrame(columns=('level','key','average','max_value','min_value','std_value'))
    for key, value in statistics_dict.items():
        if (len(value) == 0):
            continue
       
        tem_value = np.array(statistics_dict[key], dtype= 'float64')
        value_max = max(tem_value)
        value_min = min(tem_value)
        value_std = np.std(tem_value)
        # level = int(key.strip('[').split('::')[0].strip('[').strip(']'))
        level_judge = key.split(' $ ')[0][1]
        if level_judge == "[":
            level = int(key.split(' $ ')[0][2])
        else:
            level = -1
        value_average = np.average(tem_value)
        relation_pd=relation_pd.append(pd.DataFrame({'level':[level], 'key':[key], 'average':[value_average],
                                                        'max_value':[value_max], 'min_value':[value_min],
                                                        'std_value':[value_std]}),
                                                        ignore_index = True,sort = True)
    return relation_pd

def Formater(Talulate_Reader):
    Talulate_Reader.sort_values(by=["level","std_value"],inplace=True,ascending=[True,True])
    Talulate_Reader.set_index('level',inplace=True)
    Talulate_Reader = Talulate_Reader[['key','average','max_value','min_value','std_value']]
    print(tabulate(Talulate_Reader,headers='keys',tablefmt='psql'))
    print('\n')
    return Talulate_Reader['key'].tolist()





if __name__ == "__main__":
    TimeLogDict = TextSniffing(TemDict)
    subplot_titles_list =[]
    for dirname, filepaths in TimeLogDict.items():
        for ele in filepaths:
            print('######## {} ########'.format(ele.split('/')[-1]))
            ele_dict= TextReader(ele)
            if not list(ele_dict.keys()):
                pass
            else:
                Talulate_Reader = Talulate_Writer(ele_dict)
                aa = Formater(Talulate_Reader)
                subplot_titles_list.extend(aa)

            Entire_Dict.update(ele_dict)  #输出完整的 函数:耗时 键值对字典

 
           

    ######################## 绘图 ###########################

    # fig = make_subplots(subplot_titles=(subplot_titles_list), rows=len(subplot_titles_list), cols=1)
    # i = 1
    # for file_name, value_list in Entire_Dict.items():
    #     for key, value in value_list.items():
    #         x = np.arange(len(value_list[key][0::interval]))

    #         fig.append_trace(
    #                         go.Scatter(x=x,
    #                                 y=value_list[key][0::interval],
    #                                 mode='markers',
    #                                 name= '{} (ms)'.format(key),
    #                                 marker=dict(size=2, color='#007bbb')
    #                                 ),
    #                         row=i,
    #                         col=1)

    #         fig.add_trace(go.Scatter(x=x, y=signal.savgol_filter(value_list[key][0::interval], 91, 5), # order of fitted polynomial # window size used for filtering 
    #                                 mode='lines',
    #                                 name= '{} (ms)'.format(key),
    #                                 line=dict(color='rgb(181,73,91)', width=1)
    #                             ),
    #                             row=i,
    #                             col=1)
    #         i += 1


    fig = make_subplots(subplot_titles=(subplot_titles_list), rows=len(subplot_titles_list), cols=1)
    
    i = 1
    for key in subplot_titles_list:
        x = np.arange(len(Entire_Dict[key][0::interval]))

        # fig.append_trace(
        #                 go.Scatter(x=x,
        #                         y=Entire_Dict[key][0::interval],
        #                         mode='markers',
        #                         name= '{} (ms)'.format(key),
        #                         marker=dict(size=2, color='#007bbb')
        #                         ),
        #                 row=i,
        #                 col=1)

        fig.add_trace(go.Scatter(x=x, y=signal.savgol_filter(Entire_Dict[key][0::interval], 91, 5), # order of fitted polynomial # window size used for filtering 
                                mode='lines',
                                name= '{} (ms)'.format(key),
                                line=dict(color='rgb(55,55,55)', width=2)
                            ),
                            row=i,
                            col=1)
        i += 1


    # DictC = ThresholdFilter(Entire_Dict, average_threshold) # 根据阈值过滤  TODO  Entire_Dict 格式变了
    

    fig.update_layout(
        height=10000,
        showlegend=True,
        title_text="<b>FT Time Consuming Visual Analysis</b><br>{}".format(time.strftime("%Y%m%d", time.localtime())),
        template="plotly_white"
    )
    fig.show()
    py.plot(fig, filename = 'FT Time Consuming Analysis_{}.html'.format(time.strftime("%Y-%m-%d", time.localtime())), auto_open=False)

