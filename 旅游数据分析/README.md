# 数据分析项目（旅游行业数据分析）

> 该项目数据基于国家统计局数据（旅游部分20年数据）

__对应数据网盘链接：__
https://pan.baidu.com/s/1lR9tp4rf_33Sm4xEPPo7Iw?pwd=2egt

## 分析思路

![image](https://github.com/user-attachments/assets/2b655177-72cb-4b69-8061-04bd9bb574a3)

---

## 数据预处理
### 项目完整代码
> 数据预处理主要就是基于数据预处理（1.3）直接套的模板，还加入了合并文件、转置和排序的处理

```python
import pandas as pd
from sqlalchemy import create_engine

# 合并数据文件（因为文件就5个，就直接简单粗暴合并了）
dir = r"C:\Users\86198\Desktop\旅游数据"
data_list = []
for i in range(1, 6):
    path = f"{dir}\\data_{i}.xls"
    data = pd.read_excel(path,header=2)
    data_list.append(data)
data = pd.concat(data_list)

# 预处理
# 检查是否存在空值
# print(data.isnull().sum())
# 后面处理空值时发现18年之后大量指标存在空值，只能处理掉
data.drop(['2023年', '2022年','2021年','2020年','2019年'], axis=1, inplace=True)
# 缺失值处理：直接删除缺失值所在行，并重置索引
data.dropna(axis=0, inplace=True)
data.reset_index(drop=True, inplace=True)
# 转置
# 转置前先设置好列索引
data.set_index('指标', inplace=True)
# 转置并将转置后的行标签转为第一列
data = data.T.rename_axis("年份").reset_index()
# 按照年份排序
data = data.sort_values(by='年份')
# 输出检查结果
print(data)

# 保存清洗后的数据 csv
data.to_csv(r'C:\Users\86198\Desktop\旅游数据汇总.csv', index=False)
# 保存数据进数据库
# engine = create_engine('mysql://用户名:密码@地址:端口号/数据库名称?charset=utf8')
# data.to_sql('要保存的名称', con=engine, index=False, if_exists='append')
```

输出结果

![image](https://github.com/user-attachments/assets/2d3921ee-85d0-4529-a94a-a5afb6292da6)


这里有点可惜，本来是想直接分析20年的不过18年后有挺多指标的数值是缺失的，就只好删掉了
> 这个项目的数据很少，所以就没有安排数据库操作

---

## 具体分析
### 项目完整代码
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 指定默认字体，'SimHei'为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv(r'C:\Users\86198\Desktop\旅游数据汇总.csv')
# print(df)

# 总体情况分析
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制国内旅游总花费折线图
plt.subplot(2, 2, 1)
# 这里需要才用choose把需要的指标的筛选出来，尝试过所有要的指标一次性筛选出来放在最前面，会直接报错，暂时还没有找到解决办法
choose = df[['年份', '国内旅游总花费(亿元)']] 
plt.plot(choose['年份'], choose['国内旅游总花费(亿元)'], label='国内旅游总花费', color='r')
plt.legend(loc='upper left')
plt.title('国内旅游总花费折线图')
# 绘制国际旅游外汇收入折线图
plt.subplot(2, 2, 2)
choose = df[['年份', '国际旅游外汇收入(百万美元)']]
plt.plot(choose['年份'], choose['国际旅游外汇收入(百万美元)'], label='国际旅游外汇收入', color='g')
plt.legend(loc='upper left')
plt.title('国际旅游外汇收入折线图')
# 绘制旅行社数折线图
plt.subplot(2, 2, 3)
choose = df[['年份', '旅行社数(个)']]
plt.plot(choose['年份'], choose['旅行社数(个)'], label='旅行社数', color='c')
plt.legend(loc='upper left')
plt.title('旅行社数折线图')
# 绘制星级饭店总数折线图
plt.subplot(2, 2, 4)
choose = df[['年份', '星级饭店总数(个)']]
plt.plot(choose['年份'], choose['星级饭店总数(个)'], label='星级饭店总数', color='y')
plt.title('星级饭店总数折线图')
plt.legend(loc='upper left')
plt.show()

# 游客分析
# 绘制过夜游客占比变化图
# 创建一个图形和两个y轴
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()   # 创建共享相同的x轴的副坐标系
# 计算过夜游客与入境游客比值
choose = df[['年份', '入境游客(万人次)', '入境过夜游客(万人次)']]
df['过夜游客与入境游客比值'] = choose['入境过夜游客(万人次)'] / choose['入境游客(万人次)']
ax1.bar(choose['年份'], df['过夜游客与入境游客比值'], label='过夜游客与入境游客比值')
ax1.set_ylim(0.4, 0.5)
ax2.plot(choose['年份'], choose['入境游客(万人次)'], label='入境游客', color='g', marker='o', ls='-.')
ax2.plot(choose['年份'], choose['入境过夜游客(万人次)'], label='入境过夜游客', color='r', marker='o', ls='--')
fig.legend(loc='upper left')
plt.title('过夜游客占比变化图')
plt.show()

# 分析入境游客构成情况
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制入境游客构成总体情况图
plt.subplot(2, 2, 1)
choose = df[['年份', '入境游客(万人次)', '外国人入境游客(万人次)', '港澳同胞入境游客(万人次)', '台湾同胞入境游客(万人次)']]
plt.plot(choose['年份'], choose['入境游客(万人次)'], label='入境游客', color='g', marker='o', ls='-.')
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
x_3 = [i+bar_width*2 for i in x_1]
plt.bar(x_1, choose['外国人入境游客(万人次)'], width=bar_width, label='外国人入境游客', color='b')
plt.bar(x_2, choose['港澳同胞入境游客(万人次)'], width=bar_width, label='港澳同胞入境游客', color='y')
plt.bar(x_3, choose['台湾同胞入境游客(万人次)'], width=bar_width, label='台湾同胞入境游客', color='g')
plt.legend(loc='upper left')
plt.title('入境游客构成总体情况图')
# 绘制外国人入境游客数量变化折线图
plt.subplot(2, 2, 2)
choose = df[['年份', '外国人入境游客(万人次)']]
plt.plot(choose['年份'], choose['外国人入境游客(万人次)'], label='外国人入境游客', color='b')
plt.legend(loc='upper left')
plt.title('外国人入境游客数量变化折线图')
# 绘制港澳同胞入境游客数量变化折线图
plt.subplot(2, 2, 3)
choose = df[['年份', '港澳同胞入境游客(万人次)']]
plt.plot(choose['年份'], choose['港澳同胞入境游客(万人次)'], label='港澳同胞入境游客', color='y')
plt.legend(loc='upper left')
plt.title('港澳同胞入境游客数量变化折线图')
# 绘制台湾同胞入境游客数量变化折线图
plt.subplot(2, 2, 4)
choose = df[['年份', '台湾同胞入境游客(万人次)']]
plt.plot(choose['年份'], choose['台湾同胞入境游客(万人次)'], label='台湾同胞入境游客', color='g')
plt.legend(loc='upper left')
plt.title('台湾同胞入境游客数量变化折线图')
plt.show()

# 游客出入境对比分析
# 绘制游客出入境情况图
choose = df[['年份', '入境游客(万人次)', '国内居民出境人数(万人次)', '国内居民因私出境人数(万人次)']]
plt.plot(choose['年份'], choose['入境游客(万人次)'], label='入境游客', color='g')
plt.plot(choose['年份'], choose['国内居民出境人数(万人次)'], label='出境游客', color='y')
plt.plot(choose['年份'], choose['国内居民因私出境人数(万人次)'], label='因私出境游客', color='c',marker='o', ls='--')
plt.legend(loc='upper left')
plt.title('入境游客构成总体情况图')
plt.show()

# 国内游客情况分析（城镇乡村游客对比分析）
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制国内旅游总花费折线图
plt.subplot(2, 2, 1)
choose = df[['年份', '国内旅游总花费(亿元)']]
plt.plot(choose['年份'], choose['国内旅游总花费(亿元)'], label='国内旅游总花费', color='g')
plt.legend(loc='upper left')
plt.title('国内旅游总花费折线图')
# 绘制国内城乡游客数对比图
plt.subplot(2, 2, 2)
choose = df[['年份', '城镇居民国内游客(百万人次)', '农村居民国内游客(百万人次)', '国内游客(百万人次)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['城镇居民国内游客(百万人次)'], width=bar_width, label='城镇居民国内游客数', color='c')
plt.bar(x_2, choose['农村居民国内游客(百万人次)'], width=bar_width, label='农村居民国内游客数', color='y')
plt.plot(choose['年份'], choose['国内游客(百万人次)'], label='国内游客数')
plt.legend(loc='upper left')
plt.title('国内城乡游客数对比图')
# 绘制国内城乡游客总花费对比图
plt.subplot(2, 2, 3)
choose = df[['年份', '城镇居民国内旅游总花费(亿元)', '农村居民国内旅游总花费(亿元)', '国内旅游总花费(亿元)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['城镇居民国内旅游总花费(亿元)'], width=bar_width, label='城镇居民国内旅游总花费', color='orange')
plt.bar(x_2, choose['农村居民国内旅游总花费(亿元)'], width=bar_width, label='农村居民国内旅游总花费', color='tan')
plt.plot(choose['年份'], choose['国内旅游总花费(亿元)'], label='国内旅游总花费')
plt.legend(loc='upper left')
plt.title('国内城乡游客总花费对比图')
# 绘制国内城乡游客人均花费对比图
plt.subplot(2, 2, 4)
choose = df[['年份', '城镇居民国内旅游人均花费(元)', '农村居民国内旅游人均花费(元)', '国内旅游人均花费(元)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['城镇居民国内旅游人均花费(元)'], width=bar_width, label='城镇居民国内旅游人均花费', color='pink')
plt.bar(x_2, choose['农村居民国内旅游人均花费(元)'], width=bar_width, label='农村居民国内旅游人均花费', color='lightgreen')
plt.plot(choose['年份'], choose['国内旅游人均花费(元)'], label='国内旅游人均花费')
plt.legend(loc='upper left')
plt.title('国内城乡游客人均花费对比图')
plt.show()

# 国外游客分析
# 国外游客总体情况
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制外国人入境游客人数与国际旅游外汇收入双折线图
plt.subplot(2, 2, 1)
choose = df[['年份', '外国人入境游客(万人次)', '国际旅游收入(亿美元)']]
plt.plot(choose['年份'], choose['外国人入境游客(万人次)'], label='外国人入境游客人数', color='g')
plt.plot(choose['年份'], choose['国际旅游收入(亿美元)'], label='国际旅游收入', color='gold')
plt.legend(loc='upper left')
plt.title('外国人入境游客人数与国际旅游外汇收入双折线图')
# 绘制男性外国人入境游客人数柱状图
plt.subplot(2, 2, 2)
choose = df[['年份', '男性外国人入境游客(万人次)']]
plt.bar(choose['年份'], choose['男性外国人入境游客(万人次)'], label='男性外国人入境游客人数', color='blue')
plt.legend(loc='upper left')
plt.title('男性外国人入境游客人数柱状图')
# 绘制女性外国人入境游客人数柱状图
plt.subplot(2, 2, 3)
choose = df[['年份', '女性外国人入境游客(万人次)']]
plt.bar(choose['年份'], choose['女性外国人入境游客(万人次)'], label='女性外国人入境游客人数', color='pink')
plt.legend(loc='upper left')
plt.title('女性外国人入境游客人数柱状图')
# 绘制男女性外国人入境游客人数对比柱状图
plt.subplot(2, 2, 4)
choose = df[['年份', '男性外国人入境游客(万人次)', '女性外国人入境游客(万人次)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['男性外国人入境游客(万人次)'], width=bar_width, label='男性外国人入境游客人数', color='blue')
plt.bar(x_2, choose['女性外国人入境游客(万人次)'], width=bar_width, label='女性外国人入境游客人数', color='pink')
plt.legend(loc='upper left')
plt.title('男女性外国人入境游客人数柱状图')
plt.show()

# 绘制国际旅游收入方式折线图&堆积面积图（往下三张图基本同理（偷懒），这个可以直接单独摘出来当堆积图的模板）
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
choose = df[['年份', '长途交通国际旅游外汇收入(亿美元)', '民航国际旅游外汇收入(亿美元)', '铁路国际旅游外汇收入(亿美元)',
     '汽车国际旅游外汇收入(亿美元)', '轮船国际旅游外汇收入(亿美元)', '游览国际旅游外汇收入(亿美元)', '住宿国际旅游外汇收入(亿美元)',
     '餐饮国际旅游外汇收入(亿美元)', '商品销售国际旅游外汇收入(亿美元)', '娱乐国际旅游外汇收入(亿美元)', '邮电通讯国际旅游外汇收入(亿美元)',
     '市内交通国际旅游外汇收入(亿美元)', '其他服务国际旅游外汇收入(亿美元)']
]
count = 0
# 从第二列开始遍历每一列
for column in choose.columns[1:]:
    # 使用numpy生成随机颜色
    color = np.random.rand(3,)  # 生成RGB颜色，范围在0到1之间
    # 绘制面积堆积图
    plt.subplot(2, 1, 1)
    plt.stackplot(choose['年份'], choose[column], labels=column, color=color, baseline='zero')
    plt.title('国际旅游收入方式堆积面积图')
    plt.legend(loc='upper left')
    # 这里多绘制一张折线图是为了将所有情况都看清楚
    plt.subplot(2, 1, 2)
    plt.plot(choose['年份'], choose[column], label=column, color=color)
    plt.title('国际旅游收入方式折线图')
    plt.legend(loc='upper left')
    count += choose[column]
plt.show()

# 绘制各年龄段情况折线图&堆积面积图
plt.figure(figsize=(14, 14), dpi=100)
choose = df[['年份', '14岁以下外国人入境游客(万人次)', '15-24岁外国人入境游客(万人次)',
     '25-44岁外国人入境游客(万人次)', '45-64岁外国人入境游客(万人次)', '65岁以上外国人入境游客(万人次)']
]
count = 0
for column in choose.columns[1:]:
    color = np.random.rand(3,)
    plt.subplot(2, 1, 1)
    plt.stackplot(choose['年份'], choose[column], labels=column, color=color, baseline='zero')
    plt.title('各年龄段情况堆积面积图')
    plt.legend(loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(choose['年份'], choose[column], label=column, color=color)
    plt.title('各年龄段情况折线图')
    plt.legend(loc='upper left')
    count += choose[column]
plt.show()

# 绘制入境目的折线图&堆积面积图
plt.figure(figsize=(14, 14), dpi=100)
choose = df[['年份', '会议/商务外国人入境游客(万人次)',
             '观光休闲外国人入境游客(万人次)', '探亲访友外国人入境游客(万人次)',
             '服务员工外国人入境游客(万人次)', '其他外国人入境游客(万人次)']
]
count = 0
for column in choose.columns[1:]:
    color = np.random.rand(3,)
    plt.subplot(2, 1, 1)
    plt.stackplot(choose['年份'], choose[column], labels=column, color=color, baseline='zero')
    plt.title('入境目的堆积面积图')
    plt.legend(loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(choose['年份'], choose[column], label=column, color=color)
    plt.title('入境目的折线图')
    plt.legend(loc='upper left')
    count += choose[column]
plt.show()

# 绘制入境游客国家情况折线图&堆积面积图
plt.figure(figsize=(14, 14), dpi=100)
choose = df[['年份', '亚洲入境游客(万人次)', '朝鲜入境游客(万人次)', '印度入境游客(万人次)', '印度尼西亚入境游客(万人次)', '日本入境游客(万人次)',
             '马来西亚入境游客(万人次)', '蒙古入境游客(万人次)', '菲律宾入境游客(万人次)', '新加坡入境游客(万人次)', '韩国入境游客(万人次)', '泰国入境游客(万人次)',
             '非洲入境游客(万人次)', '欧洲入境游客(万人次)', '英国入境游客(万人次)', '德国入境游客(万人次)', '法国入境游客(万人次)', '意大利入境游客(万人次)',
             '荷兰入境游客(万人次)', '葡萄牙入境游客(万人次)', '瑞典入境游客(万人次)', '瑞士入境游客(万人次)', '俄罗斯入境游客(万人次)', '拉丁美洲入境游客(万人次)',
             '北美洲入境游客(万人次)', '加拿大入境游客(万人次)', '美国入境游客(万人次)', '大洋洲及太平洋岛屿入境游客(万人次)', '澳大利亚入境游客(万人次)',
             '新西兰入境游客(万人次)', '其他国家入境游客(万人次)']
]
count = 0
for column in choose.columns[1:]:
    color = np.random.rand(3,)
    plt.subplot(2, 1, 1)
    plt.stackplot(choose['年份'], choose[column], labels=column, color=color, baseline='zero')
    plt.title('入境游客国家情况堆积面积图')
    plt.legend(loc='upper left')
    plt.subplot(2, 1, 2)
    plt.plot(choose['年份'], choose[column], label=column, color=color)
    plt.title('入境游客国家情况折线图')
    plt.legend(loc='upper left')
    count += choose[column]
plt.show()
```

## 拆解分析
### 前期准备
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns   # 这个项目没有用到seaborn

# 指定默认字体，'SimHei'为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 导入csv
df = pd.read_csv(r'C:\Users\86198\Desktop\旅游数据汇总.csv')
# 检查导入结果
# print(df)
```

这个就没有什么好解释的，那个字体那里就根据电脑有的字体换名字就行

### 总体情况分析
```python
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制国内旅游总花费折线图
plt.subplot(2, 2, 1)
# 这里需要才用choose把需要的指标的筛选出来，尝试过所有要的指标一次性筛选出来放在最前面，会直接报错，暂时还没有找到解决办法
choose = df[['年份', '国内旅游总花费(亿元)']] 
plt.plot(choose['年份'], choose['国内旅游总花费(亿元)'], label='国内旅游总花费', color='r')
plt.legend(loc='upper left')
plt.title('国内旅游总花费折线图')
# 绘制国际旅游外汇收入折线图
plt.subplot(2, 2, 2)
choose = df[['年份', '国际旅游外汇收入(百万美元)']]
plt.plot(choose['年份'], choose['国际旅游外汇收入(百万美元)'], label='国际旅游外汇收入', color='g')
plt.legend(loc='upper left')
plt.title('国际旅游外汇收入折线图')
# 绘制旅行社数折线图
plt.subplot(2, 2, 3)
choose = df[['年份', '旅行社数(个)']]
plt.plot(choose['年份'], choose['旅行社数(个)'], label='旅行社数', color='c')
plt.legend(loc='upper left')
plt.title('旅行社数折线图')
# 绘制星级饭店总数折线图
plt.subplot(2, 2, 4)
choose = df[['年份', '星级饭店总数(个)']]
plt.plot(choose['年份'], choose['星级饭店总数(个)'], label='星级饭店总数', color='y')
plt.title('星级饭店总数折线图')
plt.legend(loc='upper left')
plt.show()
```

这里是通过subplot来设置子图，从而让四张图放一起

plot和后面用到的bar还有stackplot都是第一个放x轴，第二个放y轴，然后再后面按照自己想法加内容，像颜色，图例名称这些（这种上网搜一搜就有）

_以plot为例_

这里是直接百度就可以找到的文章,其中就介绍了plot的具体用法

[参考文档](https://blog.csdn.net/m0_46478042/article/details/137197294)

```python
plt.plot(x, y, fmt, **kwargs)
```

- x：表示X轴上的数据点，通常是一个列表、数组或一维序列，用于指定数据点的水平位置。
- y：表示Y轴上的数据点，通常也是一个列表、数组或一维序列，用于指定数据点的垂直位置。
- fmt：是一个可选的格式字符串，用于指定线条的样式、标记和颜色。例如，‘ro-’ 表示红色圆点线条。
- **kwargs：是一系列可选参数，用于进一步自定义线条的属性，如线宽、标记大小、标签等。

__以下是一些常用参数和用法：__

> 通过例如color='r'/color='red'/marker='o'的方式使用

- __样式参数（fmt）：__ 格式字符串可以包含一个字符来指定颜色，一个字符来指定标记样式，以及一个字符来指定线条样式。例如，‘r-’ 表示红色实线，‘bo–’ 表示蓝色圆点虚线。
- __线条样式（linestyle）:__ 使用linestyle参数可以指定线条的样式，如实线（‘-’）、虚线（‘–’）、点划线（‘-.’）等。
- __标记样式（marker）：__ 使用marker参数可以指定数据点的标记样式，如圆点（‘o’）、方块（‘s’）、星号（‘*’）等。
- __线条颜色（color）：__ 使用color参数可以指定线条的颜色，可以使用颜色名称（如’red’）、缩写（如’r’）或十六进制颜色码（如’#FF5733’）。
- __线宽（linewidth）：__ 使用linewidth参数可以指定线条的宽度，以数字表示。
- 标记大小（markersize）： 使用markersize参数可以指定标记的大小，以数字表示。
- __图例标签（label）：__ 使用label参数可以为线条指定标签，用于创建图例。
- __其他属性：__ 还有许多其他属性可用于自定义线图，如透明度、渐变、线型、阴影等。

输出结果

![image](https://github.com/user-attachments/assets/23c95ab4-6bff-4a77-983d-6633eb148d9d)

总体上看旅游业至少在18年前都是在不断发展的，不过有点奇怪的是星级饭店的数量在09年前同旅游发展趋势不断增长，而10年后却不断减少。

__根据部分检索资料:__ 2009年之后，一方面随着饭店行业面临较为严峻的市场形势，集中表现在经营 __成本上升__ 、市场 __竞争激烈__ 等方面，同时更多消费者不再愿承担星级酒店 __高昂消费__ ，导致一部分星级饭店被淘汰。另一方面省级文化和旅游行政等相关部门的 __审核__ 更为 __严格__ ，同样致使该情况

参考资料：
https://www.huaon.com/channel/trend/758566.html
https://www.163.com/dy/article/HU0TN9VD0552BL5C.html

### 游客分析
#### 绘制过夜游客占比变化图

> 因为数值相差比较大，所以就设置了一个x轴的副坐标系

```python
# 创建一个图形和两个y轴
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()   # 创建共享相同的x轴的副坐标系
# 计算过夜游客与入境游客比值
choose = df[['年份', '入境游客(万人次)', '入境过夜游客(万人次)']]
df['过夜游客与入境游客比值'] = choose['入境过夜游客(万人次)'] / choose['入境游客(万人次)']
ax1.bar(choose['年份'], df['过夜游客与入境游客比值'], label='过夜游客与入境游客比值')
ax1.set_ylim(0.4, 0.5)
ax2.plot(choose['年份'], choose['入境游客(万人次)'], label='入境游客', color='g', marker='o', ls='-.')
ax2.plot(choose['年份'], choose['入境过夜游客(万人次)'], label='入境过夜游客', color='r', marker='o', ls='--')
fig.legend(loc='upper left')
plt.title('过夜游客占比变化图')
plt.show()
```

输出结果

![image](https://github.com/user-attachments/assets/b70ce874-d906-44c2-b83b-c0cf2ae5540f)

从图可见入境以及入境过夜游客同旅游业发展趋势不断增长，同时根据比值可视化的柱状图可以发现，入境过夜游客在入境游客中的占比总体呈上升趋势

#### 分析入境游客构成情况

> 这里其实本来是打算只绘制一张的，不过这样的话就不能看出港澳和台湾来客的变动，所以就把分开的折线图也给不上来了
```python
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制入境游客构成总体情况图
plt.subplot(2, 2, 1)
choose = df[['年份', '入境游客(万人次)', '外国人入境游客(万人次)', '港澳同胞入境游客(万人次)', '台湾同胞入境游客(万人次)']]
plt.plot(choose['年份'], choose['入境游客(万人次)'], label='入境游客', color='g', marker='o', ls='-.')
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
x_3 = [i+bar_width*2 for i in x_1]
plt.bar(x_1, choose['外国人入境游客(万人次)'], width=bar_width, label='外国人入境游客', color='b')
plt.bar(x_2, choose['港澳同胞入境游客(万人次)'], width=bar_width, label='港澳同胞入境游客', color='y')
plt.bar(x_3, choose['台湾同胞入境游客(万人次)'], width=bar_width, label='台湾同胞入境游客', color='g')
plt.legend(loc='upper left')
plt.title('入境游客构成总体情况图')
# 绘制外国人入境游客数量变化折线图
plt.subplot(2, 2, 2)
choose = df[['年份', '外国人入境游客(万人次)']]
plt.plot(choose['年份'], choose['外国人入境游客(万人次)'], label='外国人入境游客', color='b')
plt.legend(loc='upper left')
plt.title('外国人入境游客数量变化折线图')
# 绘制港澳同胞入境游客数量变化折线图
plt.subplot(2, 2, 3)
choose = df[['年份', '港澳同胞入境游客(万人次)']]
plt.plot(choose['年份'], choose['港澳同胞入境游客(万人次)'], label='港澳同胞入境游客', color='y')
plt.legend(loc='upper left')
plt.title('港澳同胞入境游客数量变化折线图')
# 绘制台湾同胞入境游客数量变化折线图
plt.subplot(2, 2, 4)
choose = df[['年份', '台湾同胞入境游客(万人次)']]
plt.plot(choose['年份'], choose['台湾同胞入境游客(万人次)'], label='台湾同胞入境游客', color='g')
plt.legend(loc='upper left')
plt.title('台湾同胞入境游客数量变化折线图')
plt.show()
```

输出结果

![image](https://github.com/user-attachments/assets/e11ac456-9617-4b0f-affb-a78f69b8681c)

从第一张图看，入境游客以港澳游客为主，外国入境游客次之，而台湾入境游客占比相对较小。进一步分开观察各入境游客波动 _（线条颜色分别为：蓝外国，黄港澳，绿台湾）_ 可以了解总体上的波动同旅游业增长趋势。不过值得注意的是，外国游客在07-09年有明显下降，这可能与08年次贷危机紧密相关；而港澳11-14年来客有明显下降根据进一步检索可能与香港“占中”运动存在关联。
> “占中”这个词语，在香港有两种阐述。第一种“占中”发生在2011年10月至2012年9月。彼时，部分香港市民响应美国占领华尔街运动，齐聚中环，占领汇丰总行大厦地下广场，反对金融霸权。而第二种“占中”由香港大学法律学院副教授戴耀廷等人于2013年1月发起。戴鼓励香港市民和民间领袖，以事先张扬的形式，实行“违法”、“非暴力”地占领中环行动，主要是围绕香港特首的选举问题。
https://m.thepaper.cn/newsDetail_forward_1252417

#### 游客出入境对比分析
```python
# 绘制游客出入境情况图
choose = df[['年份', '入境游客(万人次)', '国内居民出境人数(万人次)', '国内居民因私出境人数(万人次)']]
plt.plot(choose['年份'], choose['入境游客(万人次)'], label='入境游客', color='g')
plt.plot(choose['年份'], choose['国内居民出境人数(万人次)'], label='出境游客', color='y')
plt.plot(choose['年份'], choose['国内居民因私出境人数(万人次)'], label='因私出境游客', color='c',marker='o', ls='--')
plt.legend(loc='upper left')
plt.title('入境游客构成总体情况图')
plt.show()
```

输出结果

![image](https://github.com/user-attachments/assets/b2b96883-fc9e-4784-97a0-a9b762013cb5)

这张图就可以了解到，入境游客相比于出境游客维持在一定数量，而出境游客随着我国逐年发展、富强，数量快速增长并在16-17年左右出境游客数超过入境游客数，并且其中绝大多数出境游客属于因私出境。

#### 国内游客情况分析（城镇乡村游客对比分析）
```python
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制国内旅游总花费折线图（这张图其实是凑数的，毕竟只绘制三张图空一块的话看着难受）
plt.subplot(2, 2, 1)
choose = df[['年份', '国内旅游总花费(亿元)']]
plt.plot(choose['年份'], choose['国内旅游总花费(亿元)'], label='国内旅游总花费', color='g')
plt.legend(loc='upper left')
plt.title('国内旅游总花费折线图')
# 绘制国内城乡游客数对比图
plt.subplot(2, 2, 2)
choose = df[['年份', '城镇居民国内游客(百万人次)', '农村居民国内游客(百万人次)', '国内游客(百万人次)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['城镇居民国内游客(百万人次)'], width=bar_width, label='城镇居民国内游客数', color='c')
plt.bar(x_2, choose['农村居民国内游客(百万人次)'], width=bar_width, label='农村居民国内游客数', color='y')
plt.plot(choose['年份'], choose['国内游客(百万人次)'], label='国内游客数')
plt.legend(loc='upper left')
plt.title('国内城乡游客数对比图')
# 绘制国内城乡游客总花费对比图
plt.subplot(2, 2, 3)
choose = df[['年份', '城镇居民国内旅游总花费(亿元)', '农村居民国内旅游总花费(亿元)', '国内旅游总花费(亿元)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['城镇居民国内旅游总花费(亿元)'], width=bar_width, label='城镇居民国内旅游总花费', color='orange')
plt.bar(x_2, choose['农村居民国内旅游总花费(亿元)'], width=bar_width, label='农村居民国内旅游总花费', color='tan')
plt.plot(choose['年份'], choose['国内旅游总花费(亿元)'], label='国内旅游总花费')
plt.legend(loc='upper left')
plt.title('国内城乡游客总花费对比图')
# 绘制国内城乡游客人均花费对比图
plt.subplot(2, 2, 4)
choose = df[['年份', '城镇居民国内旅游人均花费(元)', '农村居民国内旅游人均花费(元)', '国内旅游人均花费(元)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['城镇居民国内旅游人均花费(元)'], width=bar_width, label='城镇居民国内旅游人均花费', color='pink')
plt.bar(x_2, choose['农村居民国内旅游人均花费(元)'], width=bar_width, label='农村居民国内旅游人均花费', color='lightgreen')
plt.plot(choose['年份'], choose['国内旅游人均花费(元)'], label='国内旅游人均花费')
plt.legend(loc='upper left')
plt.title('国内城乡游客人均花费对比图')
plt.show()
```

输出结果

![image](https://github.com/user-attachments/assets/a7910096-dd4a-467a-90df-cb94fcdd3fc2)

- 这张图主要是城乡对比，也可以发现不论是城镇还是乡村，游客数都在不断增长，符合旅游业发展趋势，同时城镇相比于乡村游客数量以及花费明显更多。

- 当然，进一步观察还可以发现11、12年左右乡村游客人均花费明显增长，目前暂时没有找到突然增长的原因
> （可能与20世纪80年代中期以来，中国政府开始有组织、有计划、大规模地开展农村扶贫开发，先后制定实施的《国家八七扶贫攻坚计划》 (1994—2000年)、《中国农村扶贫开发纲要 (2001—2010年)》有关，乡村居民收入的提高促进了花费的提高，当然如果只是这样的话按理不应该在11、12年左右有怎么明显的增长，原因有待考究）

#### 国外游客分析
##### 国外游客总体情况
```python
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
# 绘制外国人入境游客人数与国际旅游外汇收入双折线图
plt.subplot(2, 2, 1)
choose = df[['年份', '外国人入境游客(万人次)', '国际旅游收入(亿美元)']]
plt.plot(choose['年份'], choose['外国人入境游客(万人次)'], label='外国人入境游客人数', color='g')
plt.plot(choose['年份'], choose['国际旅游收入(亿美元)'], label='国际旅游收入', color='gold')
plt.legend(loc='upper left')
plt.title('外国人入境游客人数与国际旅游外汇收入双折线图')
# 绘制男性外国人入境游客人数柱状图
plt.subplot(2, 2, 2)
choose = df[['年份', '男性外国人入境游客(万人次)']]
plt.bar(choose['年份'], choose['男性外国人入境游客(万人次)'], label='男性外国人入境游客人数', color='blue')
plt.legend(loc='upper left')
plt.title('男性外国人入境游客人数柱状图')
# 绘制女性外国人入境游客人数柱状图
plt.subplot(2, 2, 3)
choose = df[['年份', '女性外国人入境游客(万人次)']]
plt.bar(choose['年份'], choose['女性外国人入境游客(万人次)'], label='女性外国人入境游客人数', color='pink')
plt.legend(loc='upper left')
plt.title('女性外国人入境游客人数柱状图')
# 绘制男女性外国人入境游客人数对比柱状图
plt.subplot(2, 2, 4)
choose = df[['年份', '男性外国人入境游客(万人次)', '女性外国人入境游客(万人次)']]
bar_width = 0.2
a = choose['年份']
x_1 = list(range(len(a)))
x_2 = [i+bar_width for i in x_1]
plt.bar(x_1, choose['男性外国人入境游客(万人次)'], width=bar_width, label='男性外国人入境游客人数', color='blue')
plt.bar(x_2, choose['女性外国人入境游客(万人次)'], width=bar_width, label='女性外国人入境游客人数', color='pink')
plt.legend(loc='upper left')
plt.title('男女性外国人入境游客人数柱状图')
plt.show()
```

输出结果

![image](https://github.com/user-attachments/assets/e8497cf4-ea3f-4179-8ed2-74de8fc099ff)

这里看国外入境游客男女情况，拆开来看男女入境游客的增长趋势基本一致，整体上呈增长趋势，当然16年前总体而言数量维持在一定水平，而16年后出现突增，当然在网络检索后，这个变化可能并不具备分析意义

> （根据网络资料2015年以后，“国际旅游收入”补充完善了停留时间为3-12个月的入境游客花费和游客在华短期旅居的花费，与往期不可比。）

##### 绘制国际旅游收入方式折线图&堆积面积图
- 因为后面三张图的原理基本是一致的，所以就只拿第一张解释一下
> 大部分绘图操作基本没有什么好说的，不过在循环那里要特别注意是从年份下一个开始，所以要加[1:]
```python
# 设置画布大小像素点
plt.figure(figsize=(14, 14), dpi=100)
choose = df[['年份', '长途交通国际旅游外汇收入(亿美元)', '民航国际旅游外汇收入(亿美元)', '铁路国际旅游外汇收入(亿美元)',
     '汽车国际旅游外汇收入(亿美元)', '轮船国际旅游外汇收入(亿美元)', '游览国际旅游外汇收入(亿美元)', '住宿国际旅游外汇收入(亿美元)',
     '餐饮国际旅游外汇收入(亿美元)', '商品销售国际旅游外汇收入(亿美元)', '娱乐国际旅游外汇收入(亿美元)', '邮电通讯国际旅游外汇收入(亿美元)',
     '市内交通国际旅游外汇收入(亿美元)', '其他服务国际旅游外汇收入(亿美元)']
]
count = 0
# 从第二列开始遍历每一列（有很多个指标，一个个绘图肯定不现实，在这里就搞一个循环）
for column in choose.columns[1:]:
    # 使用numpy生成随机颜色（生成RGB颜色，范围在0到1之间）
    color = np.random.rand(3,)  
    # 绘制面积堆积图
    plt.subplot(2, 1, 1)
    plt.stackplot(choose['年份'], choose[column], labels=column, color=color, baseline='zero')
    plt.title('国际旅游收入方式堆积面积图')
    plt.legend(loc='upper left')
    # 这里多绘制一张折线图是为了将所有情况都看清楚
    plt.subplot(2, 1, 2)
    plt.plot(choose['年份'], choose[column], label=column, color=color)
    plt.title('国际旅游收入方式折线图')
    plt.legend(loc='upper left')
    count += choose[column]
plt.show()
```

__还有一个要特别注意的细节是stackplot中设置图例名称是用labels比其他bar、plot用的label多一个s__

_输出结果_
> 因为这里颜色是用用numpy随机生成的所以结果就就以同一次运行生成的结果截图放入

__国际旅游收入方式__ 折线图&堆积面积图

![image](https://github.com/user-attachments/assets/64ae36ef-8037-4f00-ad18-e10cab5bffc4)

__各年龄段情况__ 折线图&堆积面积图

![image](https://github.com/user-attachments/assets/6334b4f5-9919-4064-a121-52bc29c0df6c)

__入境目的__ 折线图&堆积面积图

![image](https://github.com/user-attachments/assets/bf01215e-625e-45bb-a573-7c1c0de987d9)

__入境游客国家情况__ 折线图&堆积面积图

![image](https://github.com/user-attachments/assets/6839f42a-5847-4dd6-b86c-fe8a1f405ffd)

- 国际旅游收入方式折线图&堆积面积图中可以发现旅游收入以交通收入为主，特别是长途交通，排开交通收入则是以住宿、餐饮为主要收入方式，是符合实际情况的
- 各年龄段情况折线图&堆积面积图中也可以发现外国来客主要是以25-44、44-65两个年龄段为主，即以中青年为主，主要可能也是因为这两个年龄段比65岁以上年龄段拥有更多的精力游行，同时比14岁以下、15-24两个年龄段拥有更充足的经济实力和诸如工作等原因前来中国，符合实际情况
- 入境目的折线图&堆积面积图可以观察到入境游客主要是为观光游览，其次就是参加会议的工作需要
- 入境游客国家情况折线图&堆积面积图中可以发现亚洲游客明显多于其他国家，一个是中国文化对亚洲有更强吸引力，其次是亚洲涵盖范围大，包括了多个国家并且人口众多，相对而言来客数量多也不足为奇

# 报告呈现
> 这里的报告就是结合以上内容在power BI再绘制图片形成的简单报告，主要就是为了练一下power BI
_以下是报告截图：_
> 
![image](https://github.com/user-attachments/assets/738d97bc-6402-44ca-94e5-18848fa5bb86)

![image](https://github.com/user-attachments/assets/7f968b14-7e5a-4afc-a05f-c40a3bcdde10)

![image](https://github.com/user-attachments/assets/265f8eb4-4ca3-4332-972c-e6d94da9c326)

![image](https://github.com/user-attachments/assets/f746b923-8837-4dd0-b721-d76c0c4d32ed)

![image](https://github.com/user-attachments/assets/2bcedc65-4c5e-4a84-94d0-3f034efb6396)

![image](https://github.com/user-attachments/assets/0915ade5-36cd-4e44-a3d6-63eafaaa2d77)

![image](https://github.com/user-attachments/assets/4e57fe17-438b-49ec-9450-cd91881adb87)

---

# 简单复盘
顺利完成，这个项目是用国家统计局的数据做的一个简单项目，也算是从头到尾自己练习了一遍，总体上还是满意的，毕竟也算是第一次从头到尾独立完成，也算是给近半年数据分析学习交份答卷。有一说一power BI 在做的时候还感觉很丑的，没想到导出PDF居然看着还过得去
_不足_
> 这次还是发现挺多不足之处的：
- __时间安排不合理：__ 首先是本来计划两天完成的，不过最后还是三天才搞定，本来还想着报告一个做的很快，没想到要做大半天这么花时间，不过可能也是因为每天只有上午4小时来做有关，如果安排全天来做的话安排两天是可以完成的，不过一整天都做这个不现实
- __代码不熟练：__ 在使用python绘制图表的时候还是不够熟练，还是要翻看之前整理的资料，特别是绘制最后的堆积图改了好久，还是要多练习
- __流程有待优化：__ 绘制图表其实有不少都是类似的，完全可以做一些模板提高效率，就像预处理那样（真的香，很方便，补了文件处理和转置就直接拿出来用）。还有报表也有必要做一个模板，提高效率
- __分析简单：__ 总体来看这个项目其实分析的东西都比较粗浅，而且数据源单一，这一套流程对实际的分析可能也没有太多的帮助，而且没有很好的头绪把自己会的一些建模分析也融入进来，后续还要通过书籍或者看更多项目再深入学习一些内容，暂定是找一些更深入的数据分析项目继续拆解，还有推进数据挖掘和爬虫的学习
