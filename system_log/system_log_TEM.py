
import os
import re
from pprint import pprint
import numpy as np
from scipy import signal
import plotly.figure_factory as ff
import plotly.offline as py
import plotly.express as px
import plotly.tools as plotly_tools
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
import colorsys


 
def TextReader(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = lines[:-1]
        dictCPU={}
        dictMEM={}
        dictTEMP={}
        for line in lines:
            # 时间 2019-07-31 04:24:08
            raw_time = line.split('][')[2].split(',')[0]

            # 资源类型 CPU% Mem% Core_temp
            resource_type = line.split('][')[3].split('] ')[0]

            # 节点 /decision_planning_node
            if line.split('][')[3].split('] ')[1].split(' ')[0][:5] == "/rviz":
                topic_node = line.split('][')[3].split('] ')[1].split(' ')[0] = "/rviz"
            elif line.split('][')[3].split('] ')[1].split(' ')[0][:9] == "/rostopic":
                topic_node = line.split('][')[3].split('] ')[1].split(' ')[0] = "/rostopic"
            elif line.split('][')[3].split('] ')[1].split(' ')[0][:5] == "/play":
                topic_node = line.split('][')[3].split('] ')[1].split(' ')[0] = "/play"
            elif line.split('][')[3].split('] ')[1].split(' ')[0][:16] == "/rqt_gui_py_node":
                topic_node = line.split('][')[3].split('] ')[1].split(' ')[0] = "/rqt_gui_py_node"
            elif line.split('][')[3].split('] ')[1].split(' ')[0][:7] == "/record":
                topic_node = line.split('][')[3].split('] ')[1].split(' ')[0] = "/record"
            else:
                topic_node = line.split('][')[3].split('] ')[1].split(' ')[0]
            # 占用率 0.87%
            occupancy = line.split('][')[3].split('] ')[1].split(' ')[1].strip('%\n')

            if resource_type and resource_type == "CPU%":
                if dictCPU.get(topic_node):
                    dictCPU[topic_node][raw_time] = float(occupancy)
                else:
                    dictCPU[topic_node] = {raw_time:float(occupancy)}

            elif resource_type and resource_type == "Mem%":
                if dictMEM.get(topic_node):
                    dictMEM[topic_node][raw_time] = occupancy
                else:
                    dictMEM[topic_node] = {raw_time:occupancy}

            elif resource_type and resource_type == "Core_temp":
                if dictTEMP.get(topic_node):
                    dictTEMP[topic_node][raw_time] = float(occupancy[:-2])
                else:
                    dictTEMP[topic_node] = {raw_time:float(occupancy[:-2])}
        return dictCPU, dictMEM, dictTEMP



if __name__ == "__main__":
    dictCPU,dictMEM,dictTEMP = TextReader("./system_monitor.log")
    print(list(dictTEMP.keys()))

    # ['/monitor', '/routing', '/rosout', '/ins', '/localization_dispatch_node',
    #  '/control_node', '/rviz', '/system_monitor', '/decision_planning_node', 
    #  '/static_perception', '/canbus', '/localization', '/sensor_fusion', '/lidar_only_freespace']

    # for i in dictTEMP:
    #     pprint(len(dictTEMP[i]))

    # Add histogram data
    x0 = list(dictTEMP["0"].keys())
    x1 = list(dictTEMP["1"].keys())
    y0 = list(dictTEMP["0"].values())
    y1 = list(dictTEMP["1"].values())
    pprint(x1)
    # Group data together

    y_temp =[ list(dictTEMP[key].values()) for key in list(dictTEMP.keys()) ]
    print(y_temp[0])
    x_temp = [ list(dictTEMP[key].keys()) for key in list(dictTEMP.keys()) ]
    print(x_temp[0])
    labels = list(dictTEMP.keys())
    colors = ['rgb({},{},{})'.format(random.randint(0,255),
                                     random.randint(0,255),
                                     random.randint(0,255)) for i in range(100)]

    # hsv_tuples = [(1.0 * x / len(x_temp), 1., 1.) for x in range(len(x_temp))]
    # colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    # colors = list(map(lambda x: 'rgb({},{},{})'.format(int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    # random.seed(0)
    # random.shuffle(colors)
    # random.seed(None)

    print(len(x_temp))
    print(len(y_temp))


    fig = go.Figure()

    # for i in range(len(x_temp)):
    #     fig.add_trace(go.Scatter(
    #         x=x_temp[i],
    #         y=y_temp[i],
    #         name="{}".format(labels[i]),
    #         line=dict(color=colors[i], width=2)
    #         )
    #     )

    for i in range(len(x_temp)):
        fig.add_trace(go.Scatter(
            x=x_temp[i],
            y=y_temp[i],
            name="core {} temp".format(labels[i]),
            line=dict(width=2)
            )
        )


    # 6 5
    # fig.add_trace(go.Scatter(
    #     x=x_temp[5],
    #     y=y_temp[5],
    #     name="{} {}".format(labels[5],'cpu real time'),
    #     line=dict(width=3)
    #     ))

    # # 平均值
    # fig.add_trace(go.Scatter(
    #     x=x_temp[5],
    #     y=[np.mean(y_temp[5])] * len(x_temp[5]),
    #     name="{} {}".format(labels[5],'cpu average'),
    #     line=dict(width=3, dash="dash")
    #     ))

    # fig.add_trace(go.Scatter(
    #     x=x_temp[6],
    #     y=y_temp[6],
    #     name="{} {}".format(labels[6],'cpu real time'),
    #     line=dict(width=3)
    #     ))

    # # 平均值
    # fig.add_trace(go.Scatter(
    #     x=x_temp[6],
    #     y=[np.mean(y_temp[6])] * len(x_temp[6]),
    #     name="{} {}".format(labels[6],'cpu average'),
    #     line=dict(width=3, dash="dash")
    #     ))

    # fig.add_trace(go.Scatter(
    #     x=x_temp[11],
    #     y=y_temp[11],
    #     name="{} {}".format(labels[11],'cpu real time'),
    #     line=dict(width=3)
    #     ))

    # # 平均值
    # fig.add_trace(go.Scatter(
    #     x=x_temp[11],
    #     y=[np.mean(y_temp[11])] * len(x_temp[11]),
    #     name="{} {}".format(labels[11],'cpu average'),
    #     line=dict(width=3, dash="dash")
    #     ))

    # fig.add_trace(go.Scatter(
    #     x=x_temp[13],
    #     y=y_temp[13],
    #     name="{} {}".format(labels[13],'cpu real time'),
    #     line=dict(width=3)
    #     ))

    # # 平均值
    # fig.add_trace(go.Scatter(
    #     x=x_temp[13],
    #     y=[np.mean(y_temp[13])] * len(x_temp[13]),
    #     name="{} {}".format(labels[13],'cpu average'),
    #     line=dict(width=3, dash="dash")
    #     ))




    fig.update_layout(
        title=go.layout.Title(
            text="FT System Monitor",
            font_size=30,
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="x Axis",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="y Axis",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
    )



    fig.update_layout(
        height=1000,
        showlegend=True,
        legend=go.layout.Legend(
        font=dict(
            family="sans-serif",
            size=24,
            color="black"
        ),
    )
    )
    fig.show()
    py.plot(fig, filename = 'system_monitor_{}.html'.format(time.strftime("%Y-%m-%d", time.localtime())), auto_open=False)