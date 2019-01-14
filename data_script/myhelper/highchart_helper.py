import pandas as pd
import json
import numpy as np


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class Highchart_Helper(object):
    def __init__(self, df):
        self.df = df
        self.col = "Class_Name"
        self.ycol = "Training_StartM"

    def get_chart_stack(self, series_data, xAxis_data, title="堆疊圖", *args, **kwargs):
        stackcol = {
            'chart': {
                'type': 'column'
            },
            'title': {
                'text': title
            },
            'xAxis': {
                'categories': xAxis_data
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': '數量'
                },
                'stackLabels': {
                    'enabled': True,
                    'style': {
                        'fontWeight': 'bold',
                        'color': 'gray'
                    }
                }
            },
            'legend': {
                'reversed': True
            },
            'tooltip': {
                'headerFormat': '<b>{point.x}</b><br/>',
                'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal',
                    'dataLabels': {
                        'enabled': True,
                        'color': 'white'
                    }
                }
            },
            'series': series_data
        }

        return stackcol

    def get_chart_bar(self, yAxis_data, xAxis_data, title='水平長條圖', *args, **kwargs):
        bar = {'chart': {'renderTo': 'my-chart', 'type': 'bar'},
               'legend': {'enabled': True},
               'series': [{'data': yAxis_data,
                           'name': '課程數量',
                           'yAxis': 0}],
               'title': {'text': title},
               'xAxis': {'categories': xAxis_data},
               'yAxis': [{}]}

        return bar

    def get_chart_pie(self, series_data, title='圓餅圖', *args, **kwargs):
        pie = {'chart': {
            'plotBackgroundColor': None,
            'plotBorderWidth': None,
            'plotShadow': False,
            'type': 'pie'
        },
            'title': {
                'text': title
            },
            'tooltip': {
                'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            'plotOptions': {
                'pie': {
                    'allowPointSelect': True,
                    'cursor': 'pointer',
                    'dataLabels': {
                        'enabled': True,
                        'format': '<b>{point.name}</b>: {point.percentage:.1f} %',

                    }
                }
            },
            'series': [{
                'name': 'Brands',
                'colorByPoint': True,
                'data': series_data
            }]}

        return pie

    def get_bar_data(self, col):
        # dfcc = self.df['Class_Name'].value_counts()[:10]
        dfcc = self.df[col].value_counts()[:10]

        xAxis_data = dfcc.keys().tolist()
        dfcc = dfcc.reset_index()  # 重設索引
        yAxis_data = dfcc.values.tolist()
        data = {"yAxis_data": yAxis_data, "xAxis_data": xAxis_data}
        return data

    def get_pie_data(self, col):
        dfcc = self.df[col].value_counts()[:10]
        dfcc = dfcc.reset_index()
        dfcc_list = dfcc.values.tolist()  # 轉為列表 [['LINQ 新一代統一資料存取技術', 8],..]
        series_data = list(map((lambda x: {'name': x[0], 'y': x[1]}), dfcc_list))
        data = {"series_data": series_data}
        return data

    # 水平堆疊圖
    def get_stack_data(self, col, ycol):
        list1 = list(self.df[col].value_counts()[:10].index)  # TOP10 list
        dfiii_Class10 = self.df[self.df[col].map(lambda x: x in list1)]  # match list1 courses
        df = dfiii_Class10.groupby([col, ycol]).size().unstack()
        # df.where((dfiii_Class10.notnull(dfiii_Class10)), None)
        df1 = df.where((pd.notnull(df)), None)
        dfc_stack = df1.to_dict()

        t = []
        values = []
        for k, v in dfc_stack.items():
            t.append(str(k))
            keys = list(v.keys())
            values.append(list(v.values()))

        values = [list(i) for i in zip(*values)]
        series = [{'name': k, 'data': v} for v, k in zip(values, keys)]
        print(t)
        data = {"xAxis_data": t, "series_data": series}

        return data

    def ret_chart(self):
        data = {
            "stack": json.dumps(self.get_chart_stack(**self.get_stack_data(self.col, self.ycol)), cls=MyEncoder),
            "bar": json.dumps(self.get_chart_bar(**self.get_bar_data(self.col))),
            'pie': json.dumps(self.get_chart_pie(**self.get_pie_data(self.col)))
        }

        return data
