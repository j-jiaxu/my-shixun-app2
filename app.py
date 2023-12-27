# -*- coding: utf-8 -*-
import streamlit as st
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["Helvetica"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
import jieba 
import re  
from collections import Counter 
import csv
from pyecharts import options as opts 
from pyecharts.charts import *
import streamlit_echarts as ste
import math
import pandas as pd
from pyecharts.globals import ThemeType 
#############################################################################################################

# 获取html文本
def get_html(url):
    response=requests.get(url)
    # 获取编码方式
    response.encoding = 'utf-8'
    return response.text

# 查找body标签中的数据
def get_data(html):
    soup=BeautifulSoup(html, 'html.parser')
    a_tags=soup.find('body')
    return a_tags

# 将body标签中的数据写到txt文件中
def get_txt(a_tags):
    a_tags_ls=a_tags.replace("\n"," ")
    # 以utf-8编码写入txt文件
    with open(f'words.txt','w',encoding='utf-8') as f:
        f.write(a_tags_ls)
    return 'words.txt'

# 读取txt文件并进行分词
def a_tags_read(a_tags_txt):
    # 读取文本文件  
    with open(a_tags_txt, 'r',encoding='utf-8') as f:  
        text = f.read()
    # 去除文本中的空格  
    text = re.sub(r'\s+', '', text)  
    # 去除文本中的标点符号  
    text = re.sub(r'[^\w\s]', '', text)  # 使用正则表达式去除标点符号

    # 对文本分词,统计词频
    words = jieba.lcut(text)  # 使用jieba分词  
    word_counts = Counter(words)  # 使用Counter统计词频

    # 过滤长度为1或者词频为1的词
    filtered_word_counts = {word: count for word, count in word_counts.items() if len(word) > 1 and count > 1}

    return filtered_word_counts  #返回分词结果

# 将分词结果写入CSV文件
def a_tags_csv(word_counts):
    # 以写的方式打开CSV文件
    with open('words1.csv', 'w', encoding='utf-8', newline='') as csvfile:  
        writer = csv.writer(csvfile)  
        writer.writerow(['Word', 'Counts'])  # 写入CSV文件的标题行  
        for word, counts in word_counts.items():
            if len(word)>1 and counts>1:
                writer.writerow([word, counts])  # 写入CSV文件中的每一行数据

# 获取词频最高的前20个词
def a_tags_top(word_counts):
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))
    # 取出前20个
    word_count = dict(list(sorted_word_counts.items())[:20])
    return word_count
##############################################################################################################
def common():
    st.title('Web Scraping and Visualization App')
    # 输入URL
    url = st.text_input('Enter the URL:')

    if url:
        # 获取html文本
        html=get_html(url)
        # 获取数据
        a_tags=get_data(html)
        # 生成txt文本
        a_tags_txt=get_txt(a_tags.text)
        # 将词放入csv文件
        word_counts=a_tags_read(a_tags_txt)
        a_tags_csv(word_counts)
        return word_counts
    
###################################绘制图形###########################################################################
# 绘制折线图
def plot_line_chart(word_count):
    # 创建对象
    line_chart = Line()
    # 添加x轴坐标
    line_chart.add_xaxis(list(word_count.keys()))
    # 添加y轴坐标，不显示数据
    line_chart.add_yaxis("", list(word_count.values()), label_opts=opts.LabelOpts(is_show=False))
    # 设置全局选项，包括标题等
    line_chart.set_global_opts(title_opts=opts.TitleOpts(title="折线图"))
    ste.st_pyecharts(line_chart)

# 饼图
def plot_pie_chart(word_count):
    # 创建对象
    pie_chart = Pie()
    # 添加键值对
    pie_chart.add("", list(zip(list(word_count.keys()), list(word_count.values()))))
    ste.st_pyecharts(pie_chart)
    st.write("饼图")

# 柱状图
def plot_bar_chart(word_count):
    # 创建Bar()对象
    bar_chart = Bar()
    # 添加x轴坐标
    bar_chart.add_xaxis(list(word_count.keys()))
    # 添加y轴坐标，不显示数据
    bar_chart.add_yaxis("", list(word_count.values()), label_opts=opts.LabelOpts(is_show=False))
    # 设置全局选项，包括标题等
    bar_chart.set_global_opts(title_opts=opts.TitleOpts(title="柱形图"))
    ste.st_pyecharts(bar_chart)

# 散点图
def plot_scatter_chart(word_count):
    if st.button("Re-run"):
        # 创建Scatter对象
        scatter_chart = Scatter()
        # 添加x轴坐标
        scatter_chart.add_xaxis(list(word_count.keys()))
        # 添加y轴坐标
        scatter_chart.add_yaxis("", list(word_count.values()),label_opts=opts.LabelOpts(is_show=False))
        # 设置全局选项，包括标题等
        scatter_chart.set_global_opts(title_opts=opts.TitleOpts(title="散点图"))
        ste.st_pyecharts(scatter_chart)

# 面积图
def plot_plotly_chart(word_count):
   # 创建一个 Line 图表对象，使用init_opts参数初始化图表，设置其主题为LIGHT-明亮
   mianji_chart = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
   # 添加X轴数据
   mianji_chart.add_xaxis(list(word_count.keys()))
   # 使用list(word_count.values())作为Y轴的数据点，数据线是平滑的，不是折线，在折线下方填充颜色以创建面积图，并设置填充的不透明度为0.5
   mianji_chart.add_yaxis("", list(word_count.values()), is_smooth=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.5))  
   mianji_chart.set_global_opts(title_opts=opts.TitleOpts(title="面积图")) 
   ste.st_pyecharts(mianji_chart) 

# 雷达图
def plot_leida_chart(word_count):
    # 转换为列表形式  
    words = list(word_count.keys())  
    counts = list(word_count.values())  
      
    # 创建Radar对象  
    radar_chart = Radar()  
      
    # 添加schema，设置最大值和指标名称  
    radar_chart.add_schema(schema=[opts.RadarIndicatorItem(name=word, max_=max_value) for word, max_value in zip(words, counts)]  )  
      
    # 添加数据点，这里我们使用counts作为数据点，并通过'o'标记它们  
    data = [counts]  
    radar_chart.add("", data, label_opts=opts.LabelOpts(is_show=False),   
                   linestyle_opts=opts.LineStyleOpts(color="red", width=2),   
                   areastyle_opts=opts.AreaStyleOpts(color=0.1))  
    # 设置全局选项，包括标题等 
    radar_chart.set_global_opts(title_opts=opts.TitleOpts(title="雷达图"))  
    ste.st_pyecharts(radar_chart)

    

# 漏斗图
def plot_ld_charts(word_count):
    # 创建Funnel对象
    wf = Funnel()
    st.write("漏斗图")
    # 将字典中的键值对添加到图表中
    wf.add('',[list(z) for z in zip(word_count.keys(), word_count.values())])
    ste.st_pyecharts(wf)
##############################################################################################################
# 词云
def plot_ciyun_chart(word_count,shape_mask):
    plt.title('词云图')
    # 将字典转为列表的形式
    ls=list(word_count.items())
    # 创建一个WordCloud类实例
    wordcloud = (  
        WordCloud()  
    .add("", ls, word_size_range=[30, 30+len(word_count)],shape=shape_mask)  
    .set_global_opts(title_opts=opts.TitleOpts(title="词云图")))

    # 保存为html文件
    wordcloud.render("wordcloud.html")

     # 读取 HTML 文件内容
    with open('wordcloud.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    # 在页面中显示 HTML 内容
    st.components.v1.html(html_content, height=500,width=900)

##############################################################################################################
# 显示词频
def get_word():
    word_counts=common()
   
    # 输出CSV文件
    if word_counts:
        # 将字典转换成列表
        data = [{'Word': key, 'Count': value} for key, value in word_counts.items()]
        df = pd.DataFrame(data)
        st.write('词频：')
        # 使用st.table()函数显示表格
        st.table(df)

# 可视化
def Visualization():
    #侧边栏选项
    list_baidu_project= ['折线图', '饼图', '柱形图','面积图','散点图','雷达图','漏斗图']
    selected_option = st.sidebar.selectbox("type",list_baidu_project)

    word_counts=common()

    if word_counts:
        # 获得词频最高的20个词
        word_count=a_tags_top(word_counts)
        # 根据侧边栏选择显示不同的内容
        if selected_option == "折线图":
            plot_line_chart(word_count)
        elif selected_option == "饼图":
            plot_pie_chart(word_count)
        elif selected_option == "柱形图":
            plot_bar_chart(word_count)
        elif selected_option == "面积图":
            plot_plotly_chart(word_count)
        elif selected_option == "散点图":
            plot_scatter_chart(word_count)
        elif selected_option == "漏斗图":
            plot_ld_charts(word_count)
        elif selected_option == "雷达图":
            plot_leida_chart(word_count)

    
# 词云
def ciyun():
    word_counts=common()
    
    # 读取多个形状图片
    shape_images = {'circle','rect','roundRect','triangle','diamond','pinwheel','snowflake','heart','star'}
    shape_mask = st.sidebar.selectbox("shape",shape_images)

    if word_counts:
        # 获得词频最高的20个词
        word_count=a_tags_top(word_counts)
        plot_ciyun_chart(word_count,shape_mask)

##############################################################################################################


def main():
    # 创建侧边栏选项来切换页面
    page = st.sidebar.radio("page", ("word_count", "Visualization","ciyun"))

    if page=="word_count":
        get_word()
    elif page=="Visualization":
        Visualization()
    elif page=="ciyun":
        ciyun()

if __name__=='__main__':
    main()
