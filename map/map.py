import plotly.graph_objects as go

mapbox_access_token = open(".mapbox_token").read()

fig = go.Figure(
    go.Scattermapbox(
        lat=['30.8817','30.886589'],
        lon=['121.9273','121.928482'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=12,
            color= 'steelblue'
        ),
        name='SR',
        text=['红灯误检','左边半挂卡车识别为小车@海港大道'],
        subplot='mapbox'
    )  
)

fig.add_trace(go.Scattermapbox(
        lat=['30.879454','30.887629'],
        lon=['121.918663','121.932487'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=12,
            color='red',
            opacity=0.7
        ),
        name='DPC',
        text=['follow状态刹车@海事小区东区','overtake三轮车失败，自动朝三轮车行驶 ']
    ))

fig.add_trace(go.Scattermapbox(
        lat=['30.875454','30.867629'],
        lon=['121.917663','121.912487'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=12,
            color='rgb(93,172,129)',
            opacity=0.7
        ),
        name='SYSTEM',
        text=['Rviz卡顿严重','topic信息频率刷新过快']
    ))





fig.update_layout(
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=30.88,
            lon=121.92
        ),
        pitch=0,
        # dark satellite-streets satellite streets
        # style='dark',
        zoom=10,
    )
)

fig.show()
py.plot()