# 数据分析项目（城市人口分析与预测）

__数据来源：__ CCF大数据与计算智能大赛2023年赛题数据集
网盘链接：https://pan.baidu.com/s/1j6th-e5McM3zgAV8zAM2dQ?pwd=es2y
> 做一次赛题练一练，看看最近数据挖掘学的怎么样，看看还有哪些不足

## 分析思路

![image](https://github.com/user-attachments/assets/0294aa57-1b4a-4268-b639-a14ddefe8ef6)

打算先做A题看一下，主要就是检验一下近段时间的学习成果

---
# 数据预处理
## 文件合并
> 首先因为数据分散在多个数据文件，先进行合并方便后续操作，由于文件较少，所以直接打开文件查看即可

通过直接观察可以了解到excel数据文件中大部分数据文件可以直接用于合并，但是生活水平和就业信息两个数据文件中存在多个表格，而且生活水平和工资水平都是非平衡面板数据，都需要进行处理

### 个别文件处理
> 参考文档
https://blog.csdn.net/weixin_43392794/article/details/129452041
https://blog.csdn.net/SeizeeveryDay/article/details/114696467
```python
# 用于转换个别非面板数据并将excel中多个sheet合并
import pandas as pd
# 非面板数据转面板数据
# 修改工资水平.xlsx
df = pd.read_excel(r'路径\工资水平.xlsx')
list1 = []
for index in range(0, df.shape[0]):
    year = df.at[index, 'averageWage']
    for city in range(1,41):
        City = 'city' + str(city)
        averageWage = df.at[index, City]
        list1.append([City, year.replace('年', ''), averageWage])

df1 = pd.DataFrame(list1)
df1 = df1.rename(columns={0: '城市名称', 1: '年份', 2: 'averageWage'})
print(df1)
df1.to_excel(r'路径\工资水平.xlsx', index=False)


# 多个sheet表合并
# 修改就业信息.xlsx
dfs = pd.read_excel(r'路径\就业信息.xlsx', sheet_name=None)
keys = list(dfs.keys())
# print(keys)
result = pd.DataFrame({'年份':[],'城市名称':[]})
num = 1
for i in keys:
    df = dfs[i]
    num += 1
    result = pd.merge(result, df, on=['年份', '城市名称'], how='outer', suffixes=('_left', '_right'))
print(f'循环合并后的数据如下：\n{result}')
result.to_excel(r'路径\就业信息.xlsx', index=False, freeze_panes=(1,0))

# 非面板转面板并合并多个sheet表
# 修改生活水平.xlsx
dfs = pd.read_excel(r'路径\生活水平.xlsx', sheet_name=None,header=1)
keys = list(dfs.keys())
# print(keys)
result = pd.DataFrame({'年份':[],'城市名称':[]})
num = 1
tag = ['','disposableIcome','consumptionExpenditures','towner_ ConsumptionExpenditures','rural_ConsumptionExpenditures','towner_disposableIcome','rural_disposableIcome']
data_list = []
for i in keys:
    list1 = []
    df = dfs[i]
    for index in range(0, df.shape[0]):
        city = df.at[index, '城市名称']
        for year in range(2011, 2023):
            try:
                n = df.at[index, year]
                list1.append([city, year, n])
            except KeyError:
                pass
    df1 = pd.DataFrame(list1)
    df1 = df1.rename(columns={0: '城市名称', 1: '年份', 2: tag[num]})
    data_list.append(df1)
    num += 1
    result = pd.merge(result, df1, on=['年份', '城市名称'], how='outer', suffixes=('_left', '_right'))
print(f'循环合并后的数据如下：\n{result}')
result.to_excel(r'路径\生活水平.xlsx', index=False, freeze_panes=(1,0))
```
pd.merge中suffixes参数用于处理两个DataFrame中存在相同名称的列的情况
> 部分修改后效果

![image](https://github.com/user-attachments/assets/9aa013ff-2881-458f-9de2-b74bdab807ac)

![image](https://github.com/user-attachments/assets/276e3dcf-205f-445d-9f34-d1fbbf69a5fb)

### 批量修改文件名称
完成文档处理后，为方便合并、汇总数据，这里选择批量修改文件名称
> 参考文档
https://blog.csdn.net/Yao_June/article/details/92416562
```python
# 用于修改文件名称，可以作为模板保存并根据需要修改
import os

# 文件夹路径
path = os.path.abspath(r'对应路径\A赛数据 - 副本')
# 文件后缀
filename_extenstion = '.xlsx'
# 汇总后的列名
new_filename = ['data_1', 'data_2', 'data_3', 'data_4', 'data_5', 'data_6', 'data_7']

count = 0
for filename in os.listdir(path):
    # 按.xlsx后缀匹配
    if os.path.splitext(filename)[1] == filename_extenstion:
        t = os.path.splitext(filename)[0]
        # 拼接.xlsx后缀，生成完整文件名
        os.rename(os.path.join(path,t + filename_extenstion),os.path.join(path,new_filename[count] + filename_extenstion))
        count += 1
```

splitext 是 Python 中 os.path 模块提供的一个函数，用于将文件路径分割成文件名和扩展名两部分。具体来说，os.path.splitext(path) 返回一个元组，包含路径 path 的文件名和扩展名两部分。
上面代码中：
os.path.splitext(filename)[0]返回文件名
os.path.splitext(filename)[1]返回拓展名
https://blog.csdn.net/qq_45058745/article/details/131611308

os.rename()方法语法格式如下：os.rename(src, dst)
参数解释
- src – 要修改的目录名
- dst – 修改后的目录名
https://blog.csdn.net/wowocpp/article/details/79460407

_运行前_

![image](https://github.com/user-attachments/assets/29ad06db-af14-47d7-922d-42bbc365c42d)

_运行后_

![image](https://github.com/user-attachments/assets/a015368f-c16e-4c6b-9eed-c9dea90273e8)

### 合并
参考了[数据分析项目（旅游行业数据分析）](https://github.com/Hyh996/data_analyse/tree/main/%E6%97%85%E6%B8%B8%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90)的方式对文件进行合并，从整体层面了解数据集情况
```python
import pandas as pd

# 合并数据文件（简单粗暴的合并）
dir = r"对应路径\A赛数据 - 副本"
result = pd.DataFrame({'年份':[],'城市名称':[]})
for i in range(1, 8):
    path = f"{dir}\\data_{i}.xlsx"
    data = pd.read_excel(path)
    result = pd.merge(result, data, on=['年份', '城市名称'], how='outer', suffixes=('_left', '_right'))
print(result)

# 保存清洗后的数据 csv
result.to_csv(r'对应路径\城市人口分析与预测数据汇总.csv', index=False)
```
这里在简单合并后就输出看一下整体表格

![image](https://github.com/user-attachments/assets/bb0c23fb-8fea-4232-bfd2-3edcd2da458c)

不过参考题目要求“给定多个城市近几年的人口数据，包括年龄、职业、收入等特征，分析每个城市的特点和规律”可以先不做处理分析各个城市的特征

通过观察发现年龄结构数据只有2000、2010、2020三年时间的数据，存在大量数据缺失，此外2000年与2022年数据同样存在大量缺失，而生活水平数据从2011年开始

![image](https://github.com/user-attachments/assets/b91ee607-b658-44bc-ab16-c7f3f3c52b67)


---
# 各城市分析（数据观察）
粗略分析各个城市的特征
## 字段说明
> 直接整理自题目要求中的截图

|文件名|文件内容|字段|
|----|----|----|
|人口规模.xlsx|城市人口规模信息|pr_Population -- 常住人口规模|
|||r_Population -- 户籍人口规模|
|城镇化率.xlsx|城市的城镇化率|urbanizationRate -- 城镇化率|
|年龄结构.xlsx|城市人口的年龄结构|0-14 -- 0-14 岁人口规模|
|||15-64 -- 城市15-64岁人口规模|
|||65+ -- 城市65岁及以上人口规模|
|人口密度.xlsx|城市的人口密度|populationDensity -- 人口密度|
|就业信息.xlsx|城市的就业情况|unemploymentRate -- 失业率|
|||employeesNumber -- 从业人员数|
|||newlyEmployedPeople -- 城镇新增就业人员数|
|||threeIndustriesEmployed -- 三次产业就业人员数|
|工资水平.xlsx|城市就业人员的工资水平|averageWage -- 职工平均工资|
|||umpu_averageWage -- 城镇非私营单位平均工资|
|人民生活水平.xlsx|城市人民生活水平指标|disposableIcome -- 人均可支配收入|
|||consumptionExpenditures -- 人均消费支出|
|||towner_ConsumptionExpenditures-- 城镇居民消费支出|
|||rural_ConsumptionExpenditures --农村居民消费支出|
|||towner_disposableIcome -- 城镇居民人均可支配收入|
|||rural_disposableIcome -- 农村居民人均可支配收入|

## 具体分析
为方便起见本处直接是直接将合并好的数据导入power BI来绘制图表并分析
### 各城市城镇化率对比

|字段|
|----|
|urbanizationRate -- 城镇化率|

_字段设置_

![image](https://github.com/user-attachments/assets/f049f9b7-bb8b-4de0-87b0-8bb3abba1e4e)

得出 _各城市城镇化率折线图_

![image](https://github.com/user-attachments/assets/ad428c17-2ec5-4957-bfe0-d05abe6e8f3c)

城市25、31、33城镇化率高，但城市25和33有骤降现象，后续分析可能要关注一下以便分析原因，城市35和9城镇化率低
后面的设置基本一致，都是年份放X轴，城市名称放图例，如何根据要看的标签放Y轴

### 各城市工资水平对比
|字段||
|----|----|
|averageWage -- 职工平均工资|umpu_averageWage -- 城镇非私营单位平均工资|

_职工平均工资折线图_

![image](https://github.com/user-attachments/assets/1689e060-47c0-4dbc-9358-3b9e07829f35)

城市25和城市33职工平均工资高，其他城市都差不多，总体而言各个城市是职工平均工资维持在逐年上涨的趋势中

### 各城市就业信息对比

|字段||
|----|----|
|unemploymentRate -- 失业率|newlyEmployedPeople -- 城镇新增就业人员数|
|employeesNumber -- 从业人员数|threeIndustriesEmployed -- 三次产业就业人员数|

_失业率柱状图_

![image](https://github.com/user-attachments/assets/134bf9d6-dac5-47fd-be13-bcec3daee569)

通过与绘制图表的交互，城市31和城市25失业率较大，城市31失业率最高在2002年甚至高达12%，不过随着时间发展失业率都逐年降低，最终稳定在4%以下
_从业人员数折线图_

![image](https://github.com/user-attachments/assets/cb665bc3-9b20-4b50-84ad-2f86d6189f30)

城市3和城市17保持逐年上涨的趋势，而城市32和城市25在2020年却出现骤降，其他则维持在一个较为稳定的状态

_第一产业就业人员数丝带图_

![image](https://github.com/user-attachments/assets/62cab6c8-b0a1-4963-ad5a-7cb074c30d3e)

城市15第一产业就业人员数变化波动大，城市35第一产业就业人员数则基本保持在第一；2007-2009年期间总体而言各个城市占比都有所下降，但城市9在该段时间内占比有明显上升，在2009后又不断下降

_第二产业就业人员数丝带图_

![image](https://github.com/user-attachments/assets/87cc5d14-0409-41a4-aa90-a9467cd5919f)

城市33、25、3、5四个最高，尽管其中2012、2015、2020年城市33和城市25的总量有所变化，但总体来看城市33第二产业就业人数最多

_第三产业就业人员数丝带图_

![image](https://github.com/user-attachments/assets/7097edd4-d0e1-4ff3-859b-80b729bf78c7)

总体来看，第三产业的就业人数是不断增多的，其中城市3和17发展迅速，分别在2014、2015年陆续超越原来的第三产业就业人员数第一城市33成为第一第二

基于以上产业就业人员数丝带图，城市35第一产业可能比较发达，城市25和城市5第二产业比较突出，城市17第三产业发展迅速，城市3和城市33二、三产业都有所兼顾

### 各城市年龄结构对比

|字段|15-64 -- 城市15-64岁人口规模|
|----|-----|
|0-14 -- 0-14 岁人口规模|65+ -- 城市65岁及以上人口规模|

_各城市年龄结构树状图_

![image](https://github.com/user-attachments/assets/37e4cf19-044d-4a19-b965-42dec7f9a775)

通过对图表的观察可以了解到基本所有城市都是15-64岁人口最多，其中大部分城市65+与0-14岁人口规模数量相近，同时通过图表可以了解到城市33、17、25、3都是人口规模较大的城市。此外，进一步观察还发现靠近左下侧的城市3、6、24中0-14岁人口规模相对大于65+，人口结构相对年轻化

### 各城市人口规模对比

|字段||
|----|----|
|pr_Population -- 常住人口规模|r_Population -- 户籍人口规模|

_常住人口&户籍人口折线图_

![image](https://github.com/user-attachments/assets/d8fe7d77-e4e9-48b5-b4d5-b54db00f074f)

常住人口与户籍人口基本保持相近变化趋势，值得注意的是通过数据观察可以发现人口规模在2006年又明显断层，可能是许多城市数据的缺失，后续可能要对该部分进行处理避免影响模型。此外，2002年城市31有较为突兀的波动，如果后续模型预测效果不理想可能要将其考虑为异常值进行处理

### 各城市人口密度对比

|字段|
|----|
|populationDensity -- 人口密度|

_人口密度堆积面积图_

![image](https://github.com/user-attachments/assets/e5e6bf18-8b07-4026-aaad-dac718717330)

通过图表观察，人口密度总体呈上升趋势，说明人口密度随时间不断增大。其中，城市3的堆积面积最大，在众多城市中人口密度最大

### 各城市生活水平对比

|字段||
|----|----|
|disposableIcome -- 人均可支配收入|rural_ConsumptionExpenditures --农村居民消费支出|
|consumptionExpenditures -- 人均消费支出|towner_disposableIcome -- 城镇居民人均可支配收入|
|towner_ConsumptionExpenditures-- 城镇居民消费支出|rural_disposableIcome -- 农村居民人均可支配收入|

_人均可支配收入&人均消费支出折线图_

![image](https://github.com/user-attachments/assets/5f772d11-9d96-48d4-938d-820db8a64140)

人均可支配收入折线图中除城市25和城市33基本都保持上升趋势，而城市25和城市33在20年人均可支配收入下降明显。人均消费支出折线图中，大部分城市人均消费基本维持在一定水平，但城市21在2021年有突兀上升，需要进一步验证是否是异常值导致

_使用筛选器剔除城市21后_

![image](https://github.com/user-attachments/assets/8b437e04-159e-449c-b034-a096bda5cbbe)


人均消费支出折线图在去除城市21后变化趋势与人均可支配收入折线图基本一致，人均消费支出同样除城市25和城市33保持上升趋势，可以确定城市21中2022的值比较极端，对图表影响大

_城乡人均可支配收入&人均消费支出对比_
> 上方两张图对应人均可支配收入，下方两张图对应人均消费支出。左边为城市，右边为农村

![image](https://github.com/user-attachments/assets/d7c6cf38-8a6e-4370-ba7c-143bda3255a5)

通过观察总体上无论消费还是可支配收入都呈上升趋势，其中城市25同样突出，在2020年有明显变化，结合前面分析，可以判断城市25是一个城镇化程度高并且收入较高的城市，第二产业就业人数多，工业较发达，同时其人均可支配收入与人均消费支出与工资水平变动基本一致

## 报告
>就直接用上面的内容偷懒做了一份简单的报告

![image](https://github.com/user-attachments/assets/9dab30ec-779e-4e06-a06b-af93d47de4ef)

![image](https://github.com/user-attachments/assets/7de54bb4-362c-4892-ab84-b1b99d528970)

![image](https://github.com/user-attachments/assets/ff67b9f3-369d-47e9-ba9a-c64de4415886)

![image](https://github.com/user-attachments/assets/80f4f63b-721e-4540-9e75-3b9225bd644c)


---
# 建模预测
> 开始预测前有必要厘清要预测的内容

__总人口的基本定义__
- 统计意义上的总人口，又称人口总数，是指一定时点、一定地域范围内所有的有生命活动的个人的总和。它不分性别，不分年龄，不分民族，只要是有独立的生命活动就包含在人口总数之内。总人口是人口统计中最基本的指标，是计算人口构成和人口再生产诸多指标的基础，也是反映一个国家人口资源的重要指标。
- 总人口通常使用常住人口的口径。常住人口为国际上进行人口普查和人口调查时常用的统计口径之一，是指经常居住在某一地区的人口。目前在中国，常住人口是指实际经常居住在某地区半年以上的人口。主要包括：居住在本乡镇街道且户口在本乡镇街道或户口待定的人；居住在本乡镇街道且离开户口登记地所在的乡镇街道半年以上的人；户口在本乡镇街道且外出不满半年或在境外工作学习的人。
- 总人口随人口的出生、死亡、迁入、迁出的变动而变动。中国总人口的变动主要来源于人口的自然变动，通常用人口自然增长率来反映。人口自然增长率是指一年内人口自然增长数与年平均总人数之比，通常用千分数表示。它是用于说明人口自然增长的水平和速度的综合性指标。
- 人口自然增长率＝人口出生率－人口死亡率
——国家统计局

## 预处理
筛选和城市人口直接相关的常住人口处理并保存，用于初步直接预测
> 总人口通常使用常住人口的口径，由此适合将常住人口拿来先构建一个简单的模型直接预测
```python
import pandas as pd
# 筛选和城市人口直接相关的数据处理并保存，用于初步直接预测
df = pd.read_csv(r'对应路径\城市人口分析与预测汇总.csv')
# 筛选出常住人口数据
result = df[['年份','城市名称','常住人口（万人）']]
# 检查属性
# df.info()
# 检查是否存在空值
# print(df.isnull().sum())
# 缺失值处理：直接删除缺失值所在行，并重置索引
result.dropna(axis=0, inplace=True)
result.reset_index(drop=True, inplace=True)
# 修改城市名称，将city1转为1
# 创建一个映射字典，将城市名称映射到一个唯一的数字
city_mapping = {city: i + 1 for i, city in enumerate(result['城市名称'].unique())}
# 使用映射字典替换城市名称
result['城市名称'] = result['城市名称'].map(city_mapping)
# 检查
print(result)
# 输出csv
result.to_csv(r'对应路径\城市人口分析与预测常住人口数据.csv', index=False)
```
关于该部分预处理内容可以翻看笔记[数据预处理](https://github.com/Hyh996/data_analyse/blob/main/%E7%9B%B8%E5%85%B3%E6%95%B4%E7%90%86/%E6%95%B0%E6%8D%AE%E9%A2%84%E5%A4%84%E7%90%86/README.md)，有更详尽的说明
筛选数据完整度最高的2015-2021年剔除年龄结构数据处理并保存，用于构建特征工程后再预测
```python
import pandas as pd
# 筛选数据完整度最高的2015-2021年剔除年龄结构数据处理并保存，用于构建特征工程后再预测
# 筛选数据完整度最高的2015-2021年
years_to_filter = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
filtered_df = df[df['年份'].isin(years_to_filter)]
# 剔除年龄结构数据
df_dropped = filtered_df.drop(columns=['0-14','15-64','65+'])
# 定义一个函数来合并列值
def combine_values(x):
    return [val for val in x if pd.notna(val)]
# 应用函数并使用agg进行分组合并
result = df_dropped.groupby(['年份', '城市名称']).agg(combine_values).reset_index()
# 将结果转换为单个值
for col in ['employeesNumber','towner_disposableIcome']:
    result[col] = result[col].apply(lambda x: x[0] if x else None)
# 缺失值处理：直接删除缺失值所在行，并重置索引
result.dropna(axis=0, inplace=True)
result.reset_index(drop=True, inplace=True)
# 修改城市名称，将city1转为1
# 创建一个映射字典，将城市名称映射到一个唯一的数字
city_mapping = {city: i + 1 for i, city in enumerate(result['城市名称'].unique())}
# 使用映射字典替换城市名称
result['城市名称'] = result['城市名称'].map(city_mapping)
# 检查
print(result)
# 输出csv
result.to_csv(r'对应路径\2015-2021年人口规模预测数据集.csv', index=False)
```
这个部分本来是考虑搭建特征工程或引入外部变量可能会用到所以写的，但实际上并没有完成特征工程的搭建，也就没有用到

---
## 初步直接预测
### 完整代码
```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings

# 忽略报错（主程序中mean_squared_error会导致报错，但并不影响程序运行，为了输出简洁的结果，这里采取直接忽略报错的方式）
warnings.filterwarnings('ignore',category=Warning)

# 指定默认字体，'SimHei'为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 加载数据
data = pd.read_csv(r'对应路径\城市人口分析与预测常住人口数据.csv')

# 创建列表（方便后续结果写入）
data_to_append = []

# 按照城市分组
grouped = data.groupby('城市名称')

# 遍历每个城市
for city, group_data in grouped:
    # 将人口数据转换为时间序列
    population_series = group_data.set_index('年份')['常住人口（万人）']

    # 平稳性检测
    adf_test = adfuller(population_series)
    print(f'\nCity: {city}')
    print('ADF Statistic: %f' % adf_test[0])
    print('p-value: %f' % adf_test[1])

    # 差分
    population_diff = population_series.diff().dropna()
    adf_test_diff = adfuller(population_diff)
    print('ADF Statistic (diff): %f' % adf_test_diff[0])
    print('p-value (diff): %f' % adf_test_diff[1])

    # # ACF和PACF图
    # plot_acf(population_diff, lags=14)
    # plot_pacf(population_diff, lags=6, method='ywm')
    # plt.show()

    # 模型定阶
    p = q = d = 0
    for i in range(5):
        for j in range(5):
            for k in range(5):
                try:
                    model = ARIMA(data, order=(i, d, j))
                    results = model.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        p, d, q = i, d, j
                except:
                    continue

    # 分割数据集,80%的数据用于训练，20%用于测试
    split_ratio = 0.8
    train_size = int(len(population_series) * split_ratio)
    train, test = population_series[0:train_size], population_series[train_size:]

    # 模型拟合
    model = ARIMA(train, order=(p, d, q))
    results = model.fit()
    # # 模型检验
    # results.plot_diagnostics(figsize=(21, 12))
    # plt.show()
    # 预测
    forecast = results.forecast(steps=len(test))
    # 计算预测值和真实值之间的MSE和RMSE
    mse = mean_squared_error(test, forecast)
    score =1/(1+mse)
    print(f'MSE: {mse}')
    print(f'评估得分: {score}')

    # 使用模型预测2023年的人口
    # 模型拟合
    model = ARIMA(population_series, order=(p, d, q))
    results = model.fit()
    # 预测
    forecast = results.forecast(steps=1).iloc[0]
    print(f'2023年预测值: {forecast}')
    # 结果统一写入列表
    end_result = []
    end_result.append(city)
    end_result.append("2023")
    end_result.append(forecast)
    data_to_append.append(end_result)

df = pd.DataFrame({'city_id':[],'year':[],'pred':[]})
new_data = pd.DataFrame(data_to_append, columns=['city_id','year','pred'])
df = df._append(new_data, ignore_index=True)
# 转换数据类型
df['city_id'] = df['city_id'].astype(str)
df['year'] = df['year'].astype(np.int64)
# 检查属性
df.info()
print(df)
# # 导出
df.to_csv(r'对应路径\submission.csv', index=False)
```
### 拆解
#### 代码参考
> 虽然已经改的面目全非，不过确实是基于这一篇文章为基础写的代码
https://blog.csdn.net/bigorsmallorlarge/article/details/141860662

#### 前期准备
> 导入要用或可能要用的库，如何就是要处理绘图的字体问题（后面有设计绘图内容），还有导入数据
```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings

# 忽略报错（主程序中mean_squared_error会导致报错，但并不影响程序运行，为了输出简洁的结果，这里采取直接忽略报错的方式）
warnings.filterwarnings('ignore',category=Warning)
# 指定默认字体，'SimHei'为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据
data = pd.read_csv(r'对应路径\城市人口分析与预测常住人口数据.csv')
# 创建列表（方便后续结果写入）
data_to_append = []
```
这里多加了一个忽略报错的功能主要是在后面模型预测那里有不影响代码运行的报错，无关紧要的报错有点影响结果的输出，就干脆在这里设置了一个忽略
```python
https://blog.csdn.net/low5252/article/details/109334695
warnings.filterwarnings(action, message='', category=Warning, module='', lineno=0, append=False)
```
- action 为以下值：

|值|处理方式|
|----|----|
"error"|将匹配警告转换为异常
"ignore"|忽略匹配的警告
"always"|始终输出匹配的警告
"default"|对于同样的警告只输出第一次出现的警告
"module"|在一个模块中只输出第一次出现的警告
"once"|输出第一次出现的警告,而不考虑它们的位置

- message 是包含正则表达式的字符串，警告消息的开始必须匹配，不区分大小写
- category 是一个警告类型（必须是 Warning 的子类）

|类|描述|
|----|----|
Warning|所有警告类别类的基类，它是 Exception 的子类
UserWarning|函数 warn() 的默认类别
DeprecationWarning |用于已弃用功能的警告（默认被忽略）
SyntaxWarning|用于可疑语法的警告
RuntimeWarning|用于有关可疑运行时功能的警告
FutureWarning|对于未来特性更改的警告
PendingDeprecationWarning|对于未来会被弃用的功能的警告（默认将被忽略）
ImportWarning|导入模块过程中触发的警告（默认被忽略）
UnicodeWarning|与 Unicode 相关的警告
BytesWarning|与 bytes 和 bytearray 相关的警告 (Python3)
ResourceWarning |与资源使用相关的警告(Python3)

- module 是包含模块名称的正则表达式字符串，区分大小写
- lineno 是一个整数，警告发生的行号，为 0 则匹配所有行号
#### 模型主体
这里因为要分析多个城市，而我目前就时间序列模型比较熟悉，但ARIMA模型并不能很好的分析面板数据，所以这里我主要的思路就是通过按照城市分组，然后分别进行预测
##### 分组
```python
# 按照城市分组
grouped = data.groupby('城市名称')

# 遍历每个城市
for city, group_data in grouped:
    # 将人口数据转换为时间序列
    population_series = group_data.set_index('年份')['常住人口（万人）']
```
##### 检验
> 这里就设计了平稳性检验、差分、ACF图和PACF图几个部分，就是走一遍过程，其他的模型我也还不太会就算这里真有问题我也暂时没有其他选择，就是练一下流程

_这个地方做的不好（本来是打算做特征工程的时候一起改进的），忘记处理P值了，问题蛮大的_
```python
    # 平稳性检测
    adf_test = adfuller(population_series)
    print(f'\nCity: {city}')
    print('ADF Statistic: %f' % adf_test[0])
    print('p-value: %f' % adf_test[1])
```
> 下面差分这个部分放到后面优化再用，初步分析并没有用上，不过查看结果的时候也可以看看为后续优化做准备
```python
    # 差分（剔除周期性因素）
    population_diff = population_series.diff().dropna()
    adf_test_diff = adfuller(population_diff)
    print('ADF Statistic (diff): %f' % adf_test_diff[0])
    print('p-value (diff): %f' % adf_test_diff[1])
```
```python
# # ACF和PACF图
    # plot_acf(population_diff, lags=14)
    # plot_pacf(population_diff, lags=6, method='ywm')
    # plt.show()
```
这里的ACF和PACF图绘制有点问题，每个城市绘制时lags值有不同，就前面几个都有些时14，有些15，这里想着要是全部绘制出来估计挺麻烦的，就没有继续花时间处理
##### 确定参数(p, d, q)
> 因为打算用的是ARIMA，而每个城市使用模型拟合的参数肯定是不同的，正常情况下是按照前面检测部分通过ADF检验确定d，通过ACF和PACF图分别确定p和q，但是这里很难通过这种方式实现

这里是设计了循环来找参数，不能说一定是找到最好的参数，但起码相对来说肯定好过全部预测都用同一组参数
```python
    # 模型定阶
    p = q = d = 0
    for i in range(5):
        for j in range(5):
            for k in range(5):
                try:
                    model = ARIMA(data, order=(i, d, j))
                    results = model.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        p, d, q = i, d, j
                except:
                    continue
```
##### 分割训练集
这里分割训练集之所以设置在循环里面，主要就是都以城市分组了，就肯定不能用整个数据集来训练模型（当然这个是我个人想法，不好说会不会导致预测效果不好，因为怎么做了用于预测的数据量大幅减少，很可能导致模型预测效果不好）
```python
    # 分割数据集,80%的数据用于训练，20%用于测试
    split_ratio = 0.8
    train_size = int(len(population_series) * split_ratio)
    train, test = population_series[0:train_size], population_series[train_size:]
```
##### 拟合
```python
    # 模型拟合
    model = ARIMA(train, order=(p, d, q))
    results = model.fit()
```
##### 模型检验
```python
    # # 模型检验
    # results.plot_diagnostics(figsize=(21, 12))
    # plt.show()
```

![image](https://github.com/user-attachments/assets/e90d6de0-257d-4531-abad-b66842034f2c)


调用plot_diagnostics()方法时，它会生成四个诊断图：
1. __标准化残差：__ 显示模型残差的图表，理想情况下应该随机分布在零周围，没有明显的模式。
2. __直方图：__ 残差的直方图，用于检查残差的分布是否接近正态分布。
3. __正态Q-Q图：__ 用于检查残差是否具有正态分布的图形。如果残差是正态分布的，那么图中的点应该大致沿着45度线排列。
4. __自相关图：__ 残差的自相关图，用于检查残差中是否存在自相关性。理想情况下，所有的自相关都应该接近于零，并且置信区间（通常以蓝色阴影表示）应该包含零。
> 通过检查这些图形，可以评估模型的拟合质量。如果残差不是随机的、正态分布的，或者存在自相关性，那么可能需要重新考虑模型的选择和参数。

##### 评估
> 是用测试集来初步评估的模型效果，主要是看看参数选定的效果
```
    # 预测评估
    forecast = results.forecast(steps=len(test))
    # 计算预测值和真实值之间的MSE和RMSE
    mse = mean_squared_error(test, forecast)
    score =1/(1+mse)
    print(f'MSE: {mse}')
    print(f'评估得分: {score}')
```
##### 预测
这里使用各个城市完整的人口数据population_series来再次拟合主要就是根据确定下来的参数再次去训练预测（不过这样的话前面评估的效果就只能用于参考了，该次预测结果的效果不能得到保障）
```python
    # 使用模型预测2023年的人口
    # 模型拟合
    model = ARIMA(population_series, order=(p, d, q))
    results = model.fit()
    # 预测
    forecast = results.forecast(steps=1).iloc[0]
    print(f'2023年预测值: {forecast}')
    # 结果统一写入列表
    end_result = []
    end_result.append(city)
    end_result.append("2023")
    end_result.append(forecast)
    data_to_append.append(end_result)
```
_部分输出结果截图_

![image](https://github.com/user-attachments/assets/d8242093-fccd-41ad-9517-dfe2a7f2435e)

通过结果结合前面的检验图可以判断这个初步的预测效果并不算好，大部分的预测MSE都比较高，也导致得分较低（尽管该得分反映的是初次预测的效果，不完全就是再次预测的效果，但一定程度上也可以佐证推断再次拟合的预测效果也并不理想），还是要进一步优化

> 均方误差（mean-square error, MSE）是反映估计量与被估计量之间差异程度的一种度量。均方误差是评价点估计的最一般的标准，自然，我们希望估计的均方误差越小越好
——百度百科

__另外，直接使用forecast = results.forecast(steps=1)会返回Series对象：__
```python
21 584.809519
dtype: float64
```
使用.iloc通过位置索引来访问Series或DataFrame中的元素，而不考虑实际的索引值，可以解决这个问题。
输出：584.809519

_输出结果_
```python
df = pd.DataFrame({'city_id':[],'year':[],'pred':[]})
new_data = pd.DataFrame(data_to_append, columns=['city_id','year','pred'])
df = df._append(new_data, ignore_index=True)
# 转换数据类型
df['city_id'] = df['city_id'].astype(str)
df['year'] = df['year'].astype(np.int64)
# 检查属性
df.info()
print(df)
# 导出
df.to_csv(r'对应路径\submission.csv', index=False)
```
_部分截图_
|||
|----|----|
![image](https://github.com/user-attachments/assets/6b889af0-d90e-4221-9513-7d6e7c83e80b) | ![image](https://github.com/user-attachments/assets/2f34baca-c5e3-45af-a90e-06c2eb7ab2cd)

## 优化后再预测
### 优化思路参考
https://blog.csdn.net/qq_38016957/article/details/89501981
> 这篇有具体的优化过程，不过主要可能优化在参数的遍历部分，还有一些绘图的参考

[arima模型如何改进](https://wenku.csdn.net/answer/148p7yqoo8#:~:text=%E6%94%B9%E8%BF%9Barima%E7%AE%97%E6%B3%95%E6%A8%A1%E5%9E%8B%201%20%E5%A2%9E%E5%8A%A0%E5%A4%96%E9%83%A8%E5%8F%98%E9%87%8F%EF%BC%9AARIMA%E6%A8%A1%E5%9E%8B%E5%8F%AA%E8%83%BD%E8%80%83%E8%99%91%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E5%86%85%E9%83%A8%E7%9A%84%E5%9B%A0%E7%B4%A0%EF%BC%8C%E8%80%8C%E5%A4%96%E9%83%A8%E5%9B%A0%E7%B4%A0%EF%BC%88%E5%A6%82%E5%A4%A9%E6%B0%94%E3%80%81%E7%BB%8F%E6%B5%8E%E6%8C%87%E6%A0%87%E7%AD%89%EF%BC%89%E4%B9%9F%E4%BC%9A%E5%BD%B1%E5%93%8D%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E7%9A%84%E5%8F%98%E5%8C%96%E3%80%82%20%E5%9B%A0%E6%AD%A4%EF%BC%8C%E5%8F%AF%E4%BB%A5%E5%B0%86%E5%A4%96%E9%83%A8%E5%8F%98%E9%87%8F%E5%8A%A0%E5%85%A5ARIMA%E6%A8%A1%E5%9E%8B%E4%B8%AD%EF%BC%8C%E4%BB%A5%E6%8F%90%E9%AB%98%E9%A2%84%E6%B5%8B%E7%B2%BE%E5%BA%A6%E3%80%82%202%20%E8%80%83%E8%99%91%E5%AD%A3%E8%8A%82%E6%80%A7%E5%9B%A0%E7%B4%A0%EF%BC%9AARIMA%E6%A8%A1%E5%9E%8B%E9%80%9A%E5%B8%B8%E5%8F%AA%E8%80%83%E8%99%91%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E7%9A%84%E8%B6%8B%E5%8A%BF%E5%92%8C%E5%BE%AA%E7%8E%AF%E6%80%A7%EF%BC%8C%E8%80%8C%E5%BF%BD%E7%95%A5%E4%BA%86%E5%AD%A3%E8%8A%82%E6%80%A7%E5%9B%A0%E7%B4%A0%E3%80%82%20%E5%9B%A0%E6%AD%A4%EF%BC%8C%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E5%AD%A3%E8%8A%82%E6%80%A7ARIMA%E6%A8%A1%E5%9E%8B%EF%BC%88SARIMA%EF%BC%89%E6%88%96%E5%AD%A3%E8%8A%82%E6%80%A7%E8%87%AA%E5%9B%9E%E5%BD%92%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E6%A8%A1%E5%9E%8B%EF%BC%88SARMA%EF%BC%89%E6%9D%A5%E8%80%83%E8%99%91%E5%AD%A3%E8%8A%82%E6%80%A7%E5%9B%A0%E7%B4%A0%EF%BC%8C%E4%BB%A5%E6%8F%90%E9%AB%98%E9%A2%84%E6%B5%8B%E7%B2%BE%E5%BA%A6%E3%80%82,3%20%E4%BC%98%E5%8C%96%E5%8F%82%E6%95%B0%E9%80%89%E6%8B%A9%EF%BC%9AARIMA%E6%A8%A1%E5%9E%8B%E9%9C%80%E8%A6%81%E9%80%89%E6%8B%A9%E8%87%AA%E5%9B%9E%E5%BD%92%E9%A1%B9%E3%80%81%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E9%A1%B9%E5%92%8C%E5%B7%AE%E5%88%86%E9%A1%B9%E7%9A%84%E9%98%B6%E6%95%B0%E3%80%82%20...%204%20%E5%BC%95%E5%85%A5%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E7%AE%97%E6%B3%95%EF%BC%9AARIMA%E6%A8%A1%E5%9E%8B%E6%98%AF%E4%B8%80%E7%A7%8D%E4%BC%A0%E7%BB%9F%E7%9A%84%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E9%A2%84%E6%B5%8B%E7%AE%97%E6%B3%95%EF%BC%8C%E8%80%8C%E9%9A%8F%E7%9D%80%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E6%8A%80%E6%9C%AF%E7%9A%84%E5%8F%91%E5%B1%95%EF%BC%8C%E5%8F%AF%E4%BB%A5%E8%80%83%E8%99%91%E4%BD%BF%E7%94%A8%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E3%80%81%E5%86%B3%E7%AD%96%E6%A0%91%E7%AD%89%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E7%AE%97%E6%B3%95%E6%9D%A5%E8%BF%9B%E8%A1%8C%E9%A2%84%E6%B5%8B%EF%BC%8C%E4%BB%A5%E6%8F%90%E9%AB%98%E9%A2%84%E6%B5%8B%E7%B2%BE%E5%BA%A6%E3%80%82%205%20%E6%95%B0%E6%8D%AE%E9%A2%84%E5%A4%84%E7%90%86%EF%BC%9AARIMA%E6%A8%A1%E5%9E%8B%E5%AF%B9%E6%95%B0%E6%8D%AE%E7%9A%84%E5%B9%B3%E7%A8%B3%E6%80%A7%E8%A6%81%E6%B1%82%E5%BE%88%E9%AB%98%EF%BC%8C%E5%9B%A0%E6%AD%A4%E9%9C%80%E8%A6%81%E5%AF%B9%E5%8E%9F%E5%A7%8B%E6%95%B0%E6%8D%AE%E8%BF%9B%E8%A1%8C%E5%B9%B3%E7%A8%B3%E5%8C%96%E5%A4%84%E7%90%86%E3%80%82%20)
> 这篇文章有优化思路的列举

![image](https://github.com/user-attachments/assets/27a88119-5706-4cbe-b294-6f4abbf70c95)

https://blog.csdn.net/qq_49384023/article/details/136943259
> 这篇文章参数选取是通过网络搜索或随机搜索实现的，而且还有预警机制，值得参考

https://zhuanlan.zhihu.com/p/49746642
> 这个链接主要是里面提及的auto_arima，可以自动选取参数，有必要试试

![image](https://github.com/user-attachments/assets/9c33065a-4a65-4447-ab53-2440a4d4bd65)

https://blog.csdn.net/wzk4869/article/details/126371600
> 构建特征工程的重要参考

### 大致优化思路
根据参考文章，主要确定了以下三个优化方向：
[x] __参数确定：__ 改进、优化参数(p, d, q)的穷举方法，或者改用auto arima作替代，看看哪一种方式更好
[] __引入外部变量：__ 通过构建特征工程，将其他可能影响人口的数据引入参与到预测中
[x] __滚动预测：__ 通过每次都使用新观测值重新拟合来动态预测
> （暂时作为一个考虑方向，不过优化还是以前两个为主）

与初步预测重复的部分不再赘述，主要是将改进过或添加的内容拿出来，通过前后对比看看改动的实际效果再整合
#### 参数确定
##### 只修改循环步长
```python
# 模型定阶
p = q = d = 0
for i in np.arange(0,4.1,0.1):
    for j in np.arange(0,4.1,0.1):
        for k in np.arange(0,4.1,0.1):
            try:
                model = ARIMA(data, order=(i, d, j))
                results = model.fit()
                if results.aic < min_aic:
                    min_aic = results.aic
                    p, d, q = i, d, j
            except:
                continue
```
|初步预测版输出|修改后输出|
|----|----|
![image](https://github.com/user-attachments/assets/6cb4790a-521e-4598-936f-a07bbff6febf) | ![image](https://github.com/user-attachments/assets/aaddc9f8-c76b-4e72-8d53-620d01671a20)

可以看到前后基本没有变动，不排除可能对个别城市的预测有优化，但从输出截图中的几个城市来看可以推断就算有用估计影响也不算大，后续不考虑该优化方式
> 这个地方也没有更好的修改想法，原先算法练习确实练习效果一般般，是一个薄弱点，后续需要花时间去针对性强化

##### 改用auto_arima作替代
```python
# 模型拟合
from pmdarima import auto_arima
model = auto_arima(train)
# 按照参考的文章auto_arima是不需要拟合的，拟合反而报错
forecast = model.predict(n_periods=len(test))
# 计算预测值和真实值之间的MSE和RMSE
mse = mean_squared_error(test, forecast)
score =1/(1+mse)
print(f'MSE: {mse}')
print(f'评估得分: {score}')

# 使用模型预测2023年的人口
# 模型拟合
model = auto_arima(population_series)
# 预测
forecast = model.predict(n_periods=1).iloc[0]
print(f'2023年预测值: {forecast}')
```
|初步预测版输出|修改后输出|
|----|----|
![image](https://github.com/user-attachments/assets/29715686-9f84-4645-afa4-044a53a5933f) | ![image](https://github.com/user-attachments/assets/d59a89a5-32bd-4a39-bbe2-f195db0713d7)

直接改用auto_arima模型就发现预测效果有明显提升，得分全部都有改善，说明改用auto_arima模型来确定参数(p, d, q)的方式优于原先的穷举方式，可以纳入后续模型优化
> 这个修改中用的pmdarima库和原先找的参考的文章中使用的库不一样，原先找到的文章里面的库好像不能按照文章里提到的from pyramid.arima import auto_arima调用方式使用auto_arima模型，本来是要找pyramid库的源文档看的，不过检索的时候发现这个pmdarima库也可以使用auto_arima模型，就直接改用这个库了

_新参考：_
https://blog.51cto.com/u_16213365/9389326

#### 特征工程
这个部分尝试了很久都还是没有很好的效果，而且标准化处理等还有报错没有解决。问题很大，很有必要专门重点训练一遍。另外就是模型的选择本身也有问题，这个题目并没有月份、日等的特征，所掌握的一些简单的特征工程也用不上
#### 滚动预测
```python
# 模型拟合
forecasts = []
train_segment = train
# 滚动预测
for t in range(len(train), len(train) + len(test)):
    model = ARIMA(train_segment, order=(p, d, q))
    results = model.fit()
    forecast = results.forecast(steps=1)
    train_segment._append(forecast)
    # 存储预测结果
    forecasts.append(forecast)
# 将预测结果转换为数组
forecast = np.array(forecasts)

# 计算预测值和真实值之间的MSE和RMSE
mse = mean_squared_error(test, forecast)
score = 1/(1+mse)
print(f'MSE: {mse}')
print(f'评估得分: {score}')


# 使用模型预测2023年的人口
train_segment = population_series
# 滚动预测
for t in range(len(population_series) - 1):
    # 建立模型
    model = ARIMA(train_segment, order=(p, d, q))
    results = model.fit()
    forecast = results.forecast(steps=1)
    train_segment._append(forecast)
# 打印预测结果
print(f'2023年预测值: {forecast.iloc[0]}')
```
|初步预测版输出|修改后输出|
![image](https://github.com/user-attachments/assets/50eb49ed-7c32-4da1-9ff2-bb85ab5a5b8c) | ![image](https://github.com/user-attachments/assets/8e299e33-9924-4bfa-9765-e06421d66460)

改动之后好像还是没有改善，动态预测和原先静态预测效果一样，暂时不确定这么改动有没有问题先放在这里。滚动预测就先不纳入模型的优化中


### 完整代码（改用auto_arima作替代）
```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
from pmdarima import auto_arima

warnings.filterwarnings('ignore',category=Warning)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data = pd.read_csv(r'C:\Users\86198\Desktop\城市人口分析与预测\城市人口分析与预测常住人口数据.csv')
# 创建列表（方便后续结果写入）
data_to_append = []
grouped = data.groupby('城市名称')
for city, group_data in grouped:
    population_series = group_data.set_index('年份')['常住人口（万人）']
    adf_test = adfuller(population_series)
    print(f'\nCity: {city}')
    print('ADF Statistic: %f' % adf_test[0])
    print('p-value: %f' % adf_test[1])
    split_ratio = 0.8
    train_size = int(len(population_series) * split_ratio)
    train, test = population_series[0:train_size], population_series[train_size:]
    # 模型拟合
    model = auto_arima(train)
    # 按照参考的文章auto_arima是不需要拟合的，拟合反而报错
    forecast = model.predict(n_periods=len(test))
    mse = mean_squared_error(test, forecast)
    score =1/(1+mse)
    print(f'MSE: {mse}')
    print(f'评估得分: {score}')
    # 使用模型预测2023年的人口
    model = auto_arima(population_series)
    forecast = model.predict(n_periods=1).iloc[0]
    print(f'2023年预测值: {forecast}')
    end_result = []
    end_result.append(city)
    end_result.append("2023")
    end_result.append(forecast)
    data_to_append.append(end_result)

df = pd.DataFrame({'city_id':[],'year':[],'pred':[]})
new_data = pd.DataFrame(data_to_append, columns=['city_id','year','pred'])
df = df._append(new_data, ignore_index=True)
df['city_id'] = df['city_id'].astype(str)
df['year'] = df['year'].astype(np.int64)
df.info()
print(df)
# 导出
df.to_csv(r'对应路径\城市人口分析与预测\submission(优化后).csv', index=False)
```
---
# 简单复盘
勉勉强强完成这次练习，总体来看不算满意，不过毕竟数据挖掘就学了一个星期，做成这样也还说得过去，只完成了最基本的预测，特征工程根本无从下手，边学边用磕磕碰碰完成了这次的项目（并没有达到一开始的目标，个人感觉算是失败的），还是有很多需要改进的地方，后续要沉淀一段时间好好吸收消化这次的练习。后续的学习也是，要提上日程
__不足__
_本次项目不足之处总结如下：_
- [数据预处理](https://github.com/Hyh996/data_analyse/blob/main/%E7%9B%B8%E5%85%B3%E6%95%B4%E7%90%86/%E6%95%B0%E6%8D%AE%E9%A2%84%E5%A4%84%E7%90%86/README.md)还要继续补充，不仅是数据的预处理，文件的处理也很有必要整理一下，都是可复用的功能，整理出来可以节省很多时间
- 在确定参数部分就发现原来算法是真的要练的，以前三天打鱼两天晒网的练，现在就要再回头补，挺痛苦的，等这个项目做完，真的很有必要补一下算法
- 目前数据挖掘的学习还是比较粗浅的，这一次实战就发现哪怕是相对来说比较了解的时间序列分析其实都还有很多不明白的地方和疏漏，而且前面检验的部分其实做的不好，本来是想着做特征工程的时候好好把差分、平滑一起搞的，结果就是特征工程都搞的焦头烂额还没有做出来。而且目前了解的模型还是太少了，这个项目其实不应该用时间序列来预测的，毕竟有多个变量，完全就是强行附会，预测效果很差
- 特征工程要重点关注，之前学的哪些内容太浅显了，特征工程部分甚至可以说根本没有学明白，除了B站的教程有必要用Kaggle的题目什么的辅助一下
- 还是着急了，应该先多看、分解多几个别人的项目之后再练习的，有太多没有注意到的地方了
