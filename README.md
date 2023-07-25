# <center>XJTU小学期《python编程语言》课程大作业   
**西安交通大学课程大作业社交媒体数据分析，选取微博平台共青团中央账号（user_id:3937348351）推文**   
项目地址[https://github.com/runnerxjtu/pydata_analyze](https://github.com/runnerxjtu/pydata_analyze)
<br>   
   
### 项目结构

>WeiboSpider
>>https://github.com/nghuyong/WeiboSpider
>
>preprocessing
>>
> >json2csv.py
>>pre_handle.py
> 
>analyze
>>LDA
>>> cutword.py
>>>
>>> lda.py
> >
>>vi_merged.py
> 
>essay
> >latex
> 

<br>
<br>

## 数据爬取(WeiboSpider)
本报告爬取共青团中央从 **2019.1.1至2023.7.16** 内所发布所有微博的数据，共**2.5w**余条推文       
参考项目[WeiboSpider](https://github.com/nghuyong/WeiboSpider)，该项目持续维护，在github拥有star数为3.1k，具体实现和使用见WeiboSpider目录下的README文件，感谢作者。

## 数据预处理 (preprocessing)
preprocessing下的json2csv.py将json转化为csv并删除重复行，按照日期降序排列，也可直接修改原项目直接输出csv   
preprocessing下的pre_handle.py删除话题# #及content文本内的无效文本及链接并依据create_at的时间降序排列

## 数据分析可视化(analyze)
分析代码位于analyze目录下，为实现更好可视化交互效果，本项目使用**pyecharts**进行可视化，统计共青团中央在2019-2023.7每年中每日发微次数      
其次，统计了年、月、周、日、时的发文频率差异，样本所有微博发文top200词云，周时日历图   
analyze下的lda将发文内容进行主题分析，先使用cutword.py做分词处理，然后基于分词文件lda.py使用gensim做LDA主题分析，并用pyLDAvis做可视化

## 报告撰写(essay)
本项目使用latex撰写最终分析报告，相关文件位于essay目录下，修改来自[github项目](https://github.com/tsaoyu/WHUT-LaTeX-bachelor)

<br>
<br>

