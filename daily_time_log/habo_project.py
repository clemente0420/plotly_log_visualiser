
import os
import re
from pprint import pprint
import numpy as np
from scipy import signal
import plotly.offline as py
import plotly.express as px
import plotly.tools as plotly_tools
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

 
interval = 2
average_threshold = 30
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
        print(dictA.keys())
        return dictA

def ThresholdFilter(rawdict,average_threshold):
    DictC = {}
    for key, value in rawdict.items():
        print(key,value[0])
        tem_value = np.array(rawdict[key],dtype = 'float64')
        average_value = np.mean(tem_value)
        if average_value >= average_threshold:
            DictC[key]=value
    return DictC


if __name__ == "__main__":
    TimeLogDict = TextSniffing(TemDict)
    for dirname, filepaths in TimeLogDict.items():
        for ele in filepaths:
            print(ele)
            Entire_Dict.update(TextReader(ele))

    DictC = ThresholdFilter(Entire_Dict, average_threshold)
    
    # TODO 结构调整
    fig = make_subplots(subplot_titles=(list(DictC.keys())), rows=len(DictC), cols=1)
    i = 1
    for key, value in DictC.items():
        x = np.arange(len(DictC[key][0::interval]))


        # fig.append_trace(
        #                 go.Scatter(x=x,
        #                         y=DictC[key][0::interval],
        #                         mode='markers',
        #                         name= '{} (ms)'.format(key),
        #                         marker=dict(size=2, color='#007bbb')
        #                         ),
        #                 row=i,
        #                 col=1)

        fig.add_trace(go.Scatter(x=x, y=signal.savgol_filter(DictC[key][0::interval], 91, 5), # order of fitted polynomial # window size used for filtering 
                                mode='lines',
                                name= '{} (ms)'.format(key),
                                line=dict(color='rgb(55,55,55)', width=2)
                            ),
                            row=i,
                            col=1)
        i += 1
        print(i)
    pprint(list(DictC.keys()))
    fig.update_layout(
        height=2000,
        showlegend=True,
        title_text="<b>FT Time Consuming Visual Analysis</b><br>{}".format(time.strftime("%Y%m%d", time.localtime())),
        template="plotly_white"
    )
    fig.show()
    py.plot(fig, filename = 'FT Time Consuming Analysis_{}.html'.format(time.strftime("%Y-%m-%d", time.localtime())), auto_open=False)



# os.chdir(os.path.join(os.getcwd(),DirName))
# for file in files:
#     if os.path.isfile(file):
#         print(file)


# print("****************************")
# for key,item in dictA.items():
#     print(key)

