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

# 绘制国际旅游收入方式折线图&堆积面积图（往下三张图基本同理，这个可以直接单独摘出来当堆积图的模板）
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
