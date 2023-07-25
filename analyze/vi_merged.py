import random
import datetime
import pyecharts.options as opts
from pyecharts.charts import Calendar, Page, WordCloud, HeatMap, Bar,Line, Grid
import pandas as pd
import collections
import jieba
import re
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode


def to_weekhour(file, file_colm):
    df = pd.read_csv(file)
    df[file_colm] = pd.to_datetime(df[file_colm])
    hour_week_counts = df.groupby([df[file_colm].dt.hour, df[file_colm].dt.weekday])[file_colm].count()
    result = [[hour, week, count] for (hour, week), count in hour_week_counts.items()]
    result.sort(key=lambda x: x[0])
    return result


def count_word_frequency(csv_file_path, column_name):
    df = pd.read_csv(csv_file_path)
    df[column_name].fillna('', inplace=True)
    content = df[column_name]
    merged_content = ' '.join(content)
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')
    string_data = re.sub(pattern, '', merged_content)
    jieba.suggest_freq('共青团', True)
    jieba.load_userdict('user_words.txt')
    seg_list_exact = jieba.cut(string_data, cut_all=False, HMM=True)  # 分词模式
    object_list = []
    # 去除停用词
    with open('stop_words.txt', 'r', encoding='UTF-8') as meaninglessFile:
        stopwords = set(meaninglessFile.read().split('\n'))
    stopwords.add(' ')
    for word in seg_list_exact:
        if word not in stopwords:
            object_list.append(word)
    word_counts = collections.Counter(object_list)
    for word in list(word_counts.keys()):
        if len(word) == 1:
            del word_counts[word]
    word_counts_top = word_counts.most_common(300)
    return word_counts_top


if __name__ == '__main__':
    df = pd.read_csv('cleaned_text.csv', parse_dates=['created_at'])
    date_counts = df['created_at'].dt.date.value_counts()
    cal_result = [(date, count) for date, count in date_counts.items()]
    page = Page(page_title='共青团中央微博分析')
    for year in range(2019, 2024):
        calendar = (
            Calendar()
            .add("",
                 cal_result,
                 calendar_opts=opts.CalendarOpts(range_=str(year)),
                 daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                 monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),
                 )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"{year} 年每天发微频率"),
                visualmap_opts=opts.VisualMapOpts(
                    max_=55, min_=5, orient="horizontal", is_piecewise=True, pos_top="230px", pos_left="100px",
                ),
            )
        )
        page.add(calendar)
    #绘制转赞评论变化情况
    df = pd.read_csv('cleaned_text.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    timeData = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    repostsData = df['reposts_count'].tolist()
    commentsData = df['comments_count'].tolist()
    attitudesData = df['attitudes_count'].tolist()

    line = (
        Line()
        .add_xaxis(xaxis_data=timeData)
        .add_yaxis(
            series_name="转发",
            y_axis=repostsData,
            linestyle_opts=opts.LineStyleOpts(width=1.5),
        )
        .add_yaxis(
            series_name="评论",
            y_axis=commentsData,
            linestyle_opts=opts.LineStyleOpts(width=1.5),
        )
        .add_yaxis(
            series_name="点赞",
            y_axis=attitudesData,
            linestyle_opts=opts.LineStyleOpts(width=1.5),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, label=opts.LabelOpts(formatter=JsCode("function(params) {return params.value; }"))
                ),
            ),
            yaxis_opts=opts.AxisOpts(name="数量"),
            legend_opts=opts.LegendOpts(pos_top='5%'),
            title_opts=opts.TitleOpts(title="转发、评论、点赞数量随时间变化"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    page.add(line)

    #年、月、周、日、时发微频率
    df = pd.read_csv('cleaned_text.csv', parse_dates=['created_at'])
    dateyear_counts = df['created_at'].dt.year.value_counts()
    datemonth_counts = df['created_at'].dt.month.value_counts()
    dateweek_counts = df['created_at'].dt.weekday.value_counts()
    dateday_counts = df['created_at'].dt.day.value_counts()
    datehour_counts = df['created_at'].dt.hour.value_counts()
    resultyear = [[date, count] for date, count in dateyear_counts.items()]
    resultyear.sort(key=lambda x: x[0])
    resultmonth = [[date, count] for date, count in datemonth_counts.items()]
    resultmonth.sort(key=lambda x: x[0])
    resultweek = [[date, count] for date, count in dateweek_counts.items()]
    resultweek.sort(key=lambda x: x[0])
    resultday = [[date, count] for date, count in dateday_counts.items()]
    resultday.sort(key=lambda x: x[0])
    resulthour = [[date, count] for date, count in datehour_counts.items()]
    resulthour.sort(key=lambda x: x[0])
    c_year = (
        Bar()
        .add_xaxis([i[0] for i in resultyear])
        .add_yaxis("共青团中央", [i[1] for i in resultyear])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每年发微频率"),
            yaxis_opts=opts.AxisOpts(name="次数"),
            xaxis_opts=opts.AxisOpts(name="时间"),
        )

    )

    c_month = (
        Bar()
        .add_xaxis(Faker.months)
        .add_yaxis("共青团中央", [i[1] for i in resultmonth])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每月发微频率"),
            yaxis_opts=opts.AxisOpts(name="次数"),
            xaxis_opts=opts.AxisOpts(name="时间"),
        )

    )
    c_week = (
        Bar()
        .add_xaxis(Faker.week)
        .add_yaxis("共青团中央", [i[1] for i in resultweek])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每周发微频率"),
            yaxis_opts=opts.AxisOpts(name="次数"),
            xaxis_opts=opts.AxisOpts(name="时间"),
        )

    )
    c_day = (
        Bar()
        .add_xaxis([i[0] for i in resultday])
        .add_yaxis("共青团中央", [i[1] for i in resultday])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每天发微频率"),
            yaxis_opts=opts.AxisOpts(name="次数"),
            xaxis_opts=opts.AxisOpts(name="时间"),
        )
    )
    c_hour = (
        Bar()
        .add_xaxis([i[0] for i in resulthour])
        .add_yaxis("共青团中央", [i[1] for i in resulthour])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每小时发微频率"),
            yaxis_opts=opts.AxisOpts(name="次数"),
            xaxis_opts=opts.AxisOpts(name="时间"),
        )

    )
    page.add(c_year, c_month, c_week, c_day, c_hour)
    #词云
    c_wordcloud = (
        WordCloud()
        .add(
            "",
            count_word_frequency('cleaned_text.csv', 'content'),
            word_size_range=[20, 100],
            textstyle_opts=opts.TextStyleOpts(font_family="cursive"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="top200词云"))
    )
    page.add(c_wordcloud)
    #周时热力图
    c_heatmap = (
        HeatMap()
        .add_xaxis(Faker.clock)
        .add_yaxis(
            "发微次数", Faker.week, to_weekhour('cleaned_text.csv', 'created_at'),
            label_opts=opts.LabelOpts(position="middle")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="共青团中央发微周时热力图"),
            visualmap_opts=opts.VisualMapOpts(),
        )
    )
    page.add(c_heatmap)

    page.render("vi_merged.html")
