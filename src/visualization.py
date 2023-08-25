import plotly.graph_objects as go
from helpers import to_barcode_ext


def make_interval(fig: go.Figure(),
                  bar: list | tuple,
                  i: int,
                  name: str,
                  color1: str,
                  color2: str,
                  color3: str,
                  row: int,
                  col: int) -> None:

    fig.add_trace(go.Scatter(x=[bar[2][0], bar[2][1]], y=[i, i],
                             fill=None,
                             mode='lines',
                             name=name,
                             line_color=color1
                             ), row=row, col=col)
    fig.add_trace(go.Scatter(x=[bar[2][1]], y=[i],
                             fill=None,
                             mode='markers',
                             name=name,
                             marker=dict(color=color2,
                                         size=8,
                                         line=dict(color=color1, width=0.5)
                                         ),
                             showlegend=False), row=row, col=col)
    fig.add_trace(go.Scatter(x=[bar[2][0]], y=[i],
                             fill=None,
                             mode='markers',
                             name=name,
                             marker=dict(color=color3,
                                         size=8,
                                         line=dict(color=color1, width=0.5)
                                         ),
                             showlegend=False), row=row, col=col)


def plot_barcode_LZZ_plotly(fig: go.Figure(), barcode_LZZ: list) -> None:

    d = {'ORD': {'name': 'Type I', 'colors': ['LightSkyBlue', 'white', 'LightSkyBlue']},
         'REL': {'name': 'Type II', 'colors': ['aquamarine', 'aquamarine', 'white']},
         'EP+': {'name': 'Type III', 'colors': ['cornflowerblue', 'cornflowerblue', 'cornflowerblue']},
         'EP-': {'name': 'Type IV', 'colors': ['violet', 'white', 'white']},
         }

    for i, bar in enumerate(barcode_LZZ):
        params = d[bar[0]]
        colors = params['colors']
        make_interval(fig=fig,
                      bar=bar,
                      i=i + 1,
                      name=params['name'],
                      color1=colors[0],
                      color2=colors[1],
                      color3=colors[2],
                      row=1,
                      col=2)

    fig['layout'].update({'showlegend': True})
    fig.update_yaxes(range=(0, len(barcode_LZZ) + 1))


def plot_extended_barcode_plotly(fig: go.Figure(), dgms: list, filt: list) -> None:

    m = sum(list(map(lambda i: len(dgms[i]), range(4))))
    barcode = to_barcode_ext(dgms=dgms)
    filt_max = max(filt)
    length = filt_max - min(filt)

    plot_barcode_plotly(fig, barcode, length)

    fig.add_trace(go.Scatter(x=[filt_max, filt_max], y=[1, m],
                             fill=None,
                             mode='lines',
                             name='ORD|REL',
                             line_color='grey',
                             line=dict(dash='dot'),
                             ))


def plot_barcode_plotly(fig: go.Figure(), barcode: list, filt_length: float) -> go.Figure():

    d = {'ORD': {'name_start': '(I,', 'color': 'LightSkyBlue', 'x_shift': 0, 'y_shift': 0},
         'REL': {'name_start': '(II,', 'color': 'aquamarine', 'x_shift': filt_length, 'y_shift': filt_length},
         'EP+': {'name_start': '(III,', 'color': 'cornflowerblue', 'x_shift': 0, 'y_shift': filt_length},
         'EP-': {'name_start': '(IV,', 'color': 'violet', 'x_shift': filt_length, 'y_shift': 0},
         }

    def plot_bar_dict(bar: dict, i: int, color: str, name: str, x_shift: float, y_shift: float) -> None:
        x = bar["interval"][0] + x_shift
        y = bar["interval"][1] + y_shift
        fig.add_trace(go.Scatter(x=[x, y], y=[i, i],
                                 fill=None,
                                 mode='lines',
                                 name=name,
                                 line_color=color,
                                 showlegend=False
                                 ), row=1, col=1)
        marker = dict(color=color, size=8, line=dict(color=color, width=0.5))
        fig.add_trace(go.Scatter(x=[y], y=[i],
                                 fill=None,
                                 mode='markers',
                                 name=name,
                                 marker=marker,
                                 showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=[x], y=[i],
                                 fill=None,
                                 mode='markers',
                                 name=name,
                                 marker=marker,
                                 showlegend=False), row=1, col=1)

    for i, bar in enumerate(barcode):

        t = bar['type']
        params = d[t]
        plot_bar_dict(bar=bar,
                      i=i + 1,
                      color=params['color'],
                      name=params['name_start'] + str(bar['dimension']) + ')',
                      x_shift=params['x_shift'],
                      y_shift=params['y_shift'])

    fig['layout'].update({
        'showlegend': True,
        'width': 600,
        'height': 500,
    })
    fig.update_layout(xaxis_title="Filtration value", yaxis_title="Topological feature")

    return fig
