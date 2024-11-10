# 数据分析项目（北京租房数据分析）
项目链接
https://github.com/TurboWay/bigdata_analyse/tree/main/RentFromDanke
该文档是基于项目文件租房数据分析.md结合一定个人理解所进行的内化整理
（文档里面“项目原本代码”部分是直接复制的，所有东西包括原作者信息都没有删除）
相关附件
[图片]
数据预处理
项目原本代码
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/12/25 13:49
# @Author : way
# @Site :
# @Describe: 数据处理

import re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

############################################# 合并数据文件 ##########################################################
dir = r"C:\Users\Administrator\Desktop\RentFromDanke"
data_list = []
for i in range(1, 9):
    path = f"{dir}\\bj_danke_{i}.csv"
    data = pd.read_csv(path)
    data_list.append(data)
data = pd.concat(data_list)

############################################### 数据清洗 #############################################################
#  数据重复处理: 删除重复值
# print(data[data.duplicated()])
data.drop_duplicates(inplace=True)
data.reset_index(drop=True, inplace=True)

# 缺失值处理：直接删除缺失值所在行，并重置索引
# print(data.isnull().sum())
data.dropna(axis=0, inplace=True)
data.reset_index(drop=True, inplace=True)

# 异常值清洗
data['户型'].unique()
# print(data[data['户型'] == '户型'])
data = data[data['户型'] != '户型']

# 清洗，列替换
data.loc[:, '地铁'] = data['地铁'].apply(lambda x: x.replace('地铁：', ''))

# 增加列
data.loc[:, '所在楼层'] = data['楼层'].apply(lambda x: int(x.split('/')[0]))
data.loc[:, '总楼层'] = data['楼层'].apply(lambda x: int(x.replace('层', '').split('/')[-1]))
data.loc[:, '地铁数'] = data['地铁'].apply(lambda x: len(re.findall('线', x)))
data.loc[:, '距离地铁距离'] = data['地铁'].apply(lambda x: int(re.findall('(\d+)米', x)[-1]) if re.findall('(\d+)米', x) else -1)

# 数据类型转换
data['价格'] = data['价格'].astype(np.int64)
data['面积'] = data['面积'].astype(np.int64)
data['距离地铁距离'] = data['距离地铁距离'].astype(np.int64)

################################################## 数据保存 #########################################################
# 查看保存的数据
print(data.info)

# 保存清洗后的数据 csv
# data.to_csv('D:/GitHub/bigdata_analyse/rent.csv', index=False)

# 保存清洗后的数据 sqlite
engine = create_engine('sqlite:///D:/GitHub/bigdata_analyse/rent.db')
data.to_sql('rent', con=engine, index=False, if_exists='append')
运行效果
[图片]
清洗后的数据：
[图片]
拆解分析
合并数据
该脚本读取多个CSV文件并将它们连接到单个DataFrame中
dir = r"C:\Users\Administrator\Desktop\RentFromDanke"
data_list = []
for i in range(1, 9):
    path = f"{dir}\\bj_danke_{i}.csv"
    data = pd.read_csv(path)
    data_list.append(data)
data = pd.concat(data_list)
数据清洗
- 重复值:删除重复的行。
#  数据重复处理: 删除重复值
# print(data[data.duplicated()])
data.drop_duplicates(inplace=True)
data.reset_index(drop=True, inplace=True)
https://awrmjmi97zs.feishu.cn/sync/Lnt1dc5oqsRKxxbmxdwcrOjXn0b
—— 同步块原文：pandas库
reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')
各个参数介绍
level：可以是int, str, tuple, or list, default None等类型，可以只从索引中删除给定级别。默认情况下删除所有级别。
drop：bool, default False。不要尝试在数据帧列中插入索引。这会将索引重置为默认的整数索引。
inplace：bool, default False。修改数据帧（不要创建新对象）。
col_level：int or str, default=0。如果列有多个级别，则确定将标签插入到哪个级别。默认情况下，它将插入到第一层。
col_fill：object, default。如果列有多个级别，则确定其他级别的命名方式。如果没有，则复制索引名称。
原文链接：
https://blog.csdn.net/xiewenrui1996/article/details/109055070
- 缺失值:删除缺失值的行。
# 缺失值处理：直接删除缺失值所在行，并重置索引
# print(data.isnull().sum())
data.dropna(axis=0, inplace=True)
data.reset_index(drop=True, inplace=True)
https://awrmjmi97zs.feishu.cn/sync/UEOndrKSus9uxVbAepCcnXkInIc
—— 同步块原文：pandas库
- 异常值和特定清理:删除'户型'等于'户型'的行，可能是错误地包含在数据中的标题行。
# 异常值清洗
data['户型'].unique()
data = data[data['户型'] != '户型']
unique() 函数将返回一个新的列表，其中的元素保持原有顺序，且不含重复元素。
注意
- unique() 函数只能用于可迭代对象，如列表、元组、集合等。
- unique() 函数返回的是一个新的列表，不会修改原有可迭代对象中的元素。
- unique() 函数是以元素的值作为唯一性的判断标准，而不是以元素的内存地址判断是否相同。
- unique() 函数对于不可哈希的对象（如列表、集合等）会报错，所以在使用时需要确保可迭代对象中的元素是可哈希的。
原文链接：
https://geek-docs.com/python/python-ask-answer/61_hk_1707440910.html
- 字符串清理:从'地铁'列中删除'地铁:'前缀。
- 列转换:从'楼层'和'地铁'列中提取数值以创建新列。
# 清洗，列替换
data.loc[:, '地铁'] = data['地铁'].apply(lambda x: x.replace('地铁：', ''))
# 增加列，主要是对原来信息的分割，增加、细化分析内容
data.loc[:, '所在楼层'] = data['楼层'].apply(lambda x: int(x.split('/')[0]))
data.loc[:, '总楼层'] = data['楼层'].apply(lambda x: int(x.replace('层', '').split('/')[-1]))
data.loc[:, '地铁数'] = data['地铁'].apply(lambda x: len(re.findall('线', x)))
data.loc[:, '距离地铁距离'] = data['地铁'].apply(lambda x: int(re.findall('(\d+)米', x)[-1]) if re.findall('(\d+)米', x) else -1)
- 数据类型转换:将特定列转换为整数类型。
# 数据类型转换
data['价格'] = data['价格'].astype(np.int64)
data['面积'] = data['面积'].astype(np.int64)
data['距离地铁距离'] = data['距离地铁距离'].astype(np.int64)
保存数据
使用SQLAlchemy将清理后的数据保存到CSV文件和SQLite数据库中
# 查看保存的数据
print(data.info)

# 保存清洗后的数据 csv
# data.to_csv('D:/GitHub/bigdata_analyse/rent.csv', index=False)

# 保存清洗后的数据 sqlite
engine = create_engine('sqlite:///D:/GitHub/bigdata_analyse/rent.db')
data.to_sql('rent', con=engine, index=False, if_exists='append')
engine = create_engine('sqlite:///D:/GitHub/bigdata_analyse/rent.db')格式参考：
https://awrmjmi97zs.feishu.cn/sync/VxIsdmcpIsXUJwbHcNLc3Nq3ngc
—— 同步块原文：数据分析项目（野蛮时代）
当然，这里sqlite:///D:/GitHub/bigdata_analyse/rent.db有所不同，是直接用的路径
具体分析
项目原本代码
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/12/29 13:36
# @Author : way
# @Site :
# @Describe: 数据可视化

# 解决中文字体问题
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('sqlite:///D:/GitHub/bigdata_analyse/rent.db')

# 地区-房源
sql = """
select 位置1, count(1) as total, count(distinct 小区) as com, sum(价格)/sum(面积) as per
from rent
group by 位置1
"""
data = pd.read_sql(con=engine, sql=sql)
data = data.sort_values(by='total', ascending=False)
plt.bar(data['位置1'], data['total'], label='房源数量')
for x, y in zip(data['位置1'], data['total']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.show()

# 小区-租金/平米
sql = """
select 小区, 位置1, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by 小区, 位置1
order by per desc
limit 10
"""
data = pd.read_sql(con=engine, sql=sql)
data = data.sort_values(by='per')
plt.barh(data['小区'], data['per'], label='租金(元/平米)', color='g')
for x, y in zip(data['小区'], data['per']):
    plt.text(y, x, y, ha='left', va='center', fontsize=11)
plt.legend()
plt.show()

# 户型-房源数量
sql = """
select substr(户型, 0, 3) as 户型, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by substr(户型, 0, 3)
order by 1
"""
data = pd.read_sql(con=engine, sql=sql)
plt.bar(data['户型'], data['total'], label='房源数量')
for x, y in zip(data['户型'], data['total']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.show()

# 电梯房-房源数量
sql = """
select case when 总楼层 > 7 then '电梯房' else '非电梯房' end as tp, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by case when 总楼层 > 7 then '电梯房' else '非电梯房' end
order by total desc
"""
data = pd.read_sql(con=engine, sql=sql)
plt.pie(data['total'],
        labels=data['tp'],
        colors=['m','g'],
        startangle=90,
        shadow= True,
        explode=(0,0.1),
        autopct='%1.1f%%')
plt.title('房源数量占比')
plt.show()

plt.bar(data['tp'], data['per'], label='租金(元/平米)')
for x, y in zip(data['tp'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.show()

# 电梯楼层-价格
sql = """
select case when 总楼层 > 7 then '电梯房'
            else '非电梯房' end as tp1,
       case when 1.0 * 所在楼层/总楼层 > 0.66 then '高层'
            when 1.0 * 所在楼层/总楼层 > 0.33 then '中层'
            else '低层' end as tp2,
       count(1) as total, sum(价格)/sum(面积) as per
from rent
group by case when 总楼层 > 7 then '电梯房'
              else '非电梯房' end,
         case when 1.0 * 所在楼层/总楼层 > 0.66 then '高层'
              when 1.0 * 所在楼层/总楼层 > 0.33 then '中层'
              else '低层' end
order by 1, 2  desc
"""
data = pd.read_sql(con=engine, sql=sql)
data['floor'] = data['tp1'] + '(' + data['tp2'] + ')'
plt.plot(data['floor'], data['total'], label='房源数量')
for x, y in zip(data['floor'], data['total']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.plot(data['floor'], data['per'], label='租金(元/平米)')
for x, y in zip(data['floor'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.show()

# 地铁数-租金
sql = """
select 地铁数, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by 地铁数
order by 1
"""
data = pd.read_sql(con=engine, sql=sql)
data['地铁数'] = data['地铁数'].astype(np.str)
plt.plot(data['地铁数'], data['per'], label='租金(元/平米)')
for x, y in zip(data['地铁数'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.xlabel('地铁数')
plt.show()

# 地铁距离-租金
sql = """
select case when 距离地铁距离 between 0 and 500 then '500米以内'
         when 距离地铁距离 between 501 and 1000 then '1公里以内'
         when 距离地铁距离 between 1001 and 1500 then '1.5公里以内'
         else '1.5公里以外' end as ds,
      count(1) as total, sum(价格)/sum(面积) as per
from rent
group by case when 距离地铁距离 between 0 and 500 then '500米以内'
           when 距离地铁距离 between 501 and 1000 then '1公里以内'
           when 距离地铁距离 between 1001 and 1500 then '1.5公里以内'
        else '1.5公里以外' end
order by 1
"""
data = pd.read_sql(con=engine, sql=sql)
map_dt = {
    '1.5公里以外': 4,
    '1.5公里以内': 3,
    '1公里以内': 2,
    '500米以内': 1
}
data['st'] = data['ds'].apply(lambda x: map_dt[x])
data.sort_values(by='st', inplace=True)
plt.plot(data['ds'], data['per'], label='租金(元/平米)')
for x, y in zip(data['ds'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.xlabel('距离地铁距离')
plt.show()
运行效果
[图片]
拆解分析
字体设置:确保汉字的正确显示
# 解决中文字体问题
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
之前整理过的seaborn库中用的也是同样的解决方法
https://awrmjmi97zs.feishu.cn/sync/Usj4dZwVxsSjNdblQwIc30Vhn0e
—— 同步块原文：seaborn库
连接到数据库:使用SQLAlchemy连接到包含租赁数据的SQLite数据库。
engine = create_engine('sqlite:///D:/GitHub/bigdata_analyse/rent.db')
地区分析
按位置1分组，汇总各个地区租房数量，然后绘制柱状图查看地区与房源之间的关系，判断这个地区的租房市场情况。
# 地区-房源
sql = """
select 位置1, count(1) as total, count(distinct 小区) as com, sum(价格)/sum(面积) as per
from rent
group by 位置1
"""
# 导入数据
data = pd.read_sql(con=engine, sql=sql)
data = data.sort_values(by='total', ascending=False)
# 分组并绘制
plt.bar(data['位置1'], data['total'], label='房源数量')
for x, y in zip(data['位置1'], data['total']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
# 设置标签
plt.legend()
# 显示
plt.show()
[图片]
从上图看来朝阳、通州、丰台几个区租房市场都是比较活跃的
租金分析
按每平方米租金排名前10的社区:按小区和位置分组，汇总得到总租金和每平方米平均租金，然后绘制前10个社区的水平条形图。
# 小区-租金/平米
sql = """
select 小区, 位置1, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by 小区, 位置1
order by per desc
limit 10
"""
data = pd.read_sql(con=engine, sql=sql)
data = data.sort_values(by='per')
plt.barh(data['小区'], data['per'], label='租金(元/平米)', color='g')
for x, y in zip(data['小区'], data['per']):
    plt.text(y, x, y, ha='left', va='center', fontsize=11)
plt.legend()
plt.show()
[图片]
户型分析
获取户型的前两个字符的价值计数并绘制条形图，找出租房者的租房倾向
# 户型-房源数量
sql = """
select substr(户型, 0, 3) as 户型, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by substr(户型, 0, 3)
order by 1
"""
data = pd.read_sql(con=engine, sql=sql)
plt.bar(data['户型'], data['total'], label='房源数量')
for x, y in zip(data['户型'], data['total']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.show()
这个地方有点奇怪，检查了也没有找到是哪里的问题
运行出来的代码是这样的：
[图片]
原项目租房数据分析.md中给出的效果是这样的：
[图片]
通过这个图看出租房倾向，暂时还不知道为啥自己运行出来的有问题
创建一个新列电梯房，按它分组，汇总得到总租金和每平方米的平均租金，然后绘制一个饼图和一个条形图。（根据国家规定楼层 7 层以上需要装电梯，根据楼层数是否大于7来判断房源是否有电梯）
# 电梯房-房源数量
sql = """
select case when 总楼层 > 7 then '电梯房' else '非电梯房' end as tp, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by case when 总楼层 > 7 then '电梯房' else '非电梯房' end
order by total desc
"""
data = pd.read_sql(con=engine, sql=sql)
plt.pie(data['total'],
        labels=data['tp'],
        colors=['m','g'],
        startangle=90,
        shadow= True,
        explode=(0,0.1),
        autopct='%1.1f%%')
plt.title('房源数量占比')
plt.show()

plt.bar(data['tp'], data['per'], label='租金(元/平米)')
for x, y in zip(data['tp'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.show()
[图片]
有电梯的房源相对更多（毕竟楼层高，其中的房子会更多）
[图片]
有电梯的会贵一点
创建一个新列楼层类型，按电梯房和楼层类型分组，汇总得到总租金和每平方米的平均租金，然后绘制折线图。
# 电梯楼层-价格
sql = """
select case when 总楼层 > 7 then '电梯房'
            else '非电梯房' end as tp1,
       case when 1.0 * 所在楼层/总楼层 > 0.66 then '高层'
            when 1.0 * 所在楼层/总楼层 > 0.33 then '中层'
            else '低层' end as tp2,
       count(1) as total, sum(价格)/sum(面积) as per
from rent
group by case when 总楼层 > 7 then '电梯房'
              else '非电梯房' end,
         case when 1.0 * 所在楼层/总楼层 > 0.66 then '高层'
              when 1.0 * 所在楼层/总楼层 > 0.33 then '中层'
              else '低层' end
order by 1, 2  desc
"""
data = pd.read_sql(con=engine, sql=sql)
data['floor'] = data['tp1'] + '(' + data['tp2'] + ')'
plt.plot(data['floor'], data['total'], label='房源数量')
for x, y in zip(data['floor'], data['total']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.plot(data['floor'], data['per'], label='租金(元/平米)')
for x, y in zip(data['floor'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.show()
[图片]
不管是电梯房还是非电梯房，低楼层的租金都会比较贵一些。而非电梯房的高层房源不容易租出去，低层因为相对便宜更好租出
交通分析
按地铁数分组，汇总得到总租金和每平方米的平均租金，然后绘制折线图。
# 地铁数-租金
sql = """
select 地铁数, count(1) as total, sum(价格)/sum(面积) as per
from rent
group by 地铁数
order by 1
"""
data = pd.read_sql(con=engine, sql=sql)
data['地铁数'] = data['地铁数'].astype(np.str)
# 这个地方 np.str 应该修改成 np.str_ 不然会报错无法绘制折线图
plt.plot(data['地铁数'], data['per'], label='租金(元/平米)')
for x, y in zip(data['地铁数'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.xlabel('地铁数')
plt.show()
[图片]
将距离地铁距离分类，按这些分类分组，汇总得到总租金和每平方米的平均租金，然后绘制折线图。
# 地铁距离-租金
sql = """
select case when 距离地铁距离 between 0 and 500 then '500米以内'
         when 距离地铁距离 between 501 and 1000 then '1公里以内'
         when 距离地铁距离 between 1001 and 1500 then '1.5公里以内'
         else '1.5公里以外' end as ds,
      count(1) as total, sum(价格)/sum(面积) as per
from rent
group by case when 距离地铁距离 between 0 and 500 then '500米以内'
           when 距离地铁距离 between 501 and 1000 then '1公里以内'
           when 距离地铁距离 between 1001 and 1500 then '1.5公里以内'
        else '1.5公里以外' end
order by 1
"""
data = pd.read_sql(con=engine, sql=sql)
map_dt = {
    '1.5公里以外': 4,
    '1.5公里以内': 3,
    '1公里以内': 2,
    '500米以内': 1
}
data['st'] = data['ds'].apply(lambda x: map_dt[x])
data.sort_values(by='st', inplace=True)
plt.plot(data['ds'], data['per'], label='租金(元/平米)')
for x, y in zip(data['ds'], data['per']):
    plt.text(x, y, y, ha='center', va='bottom', fontsize=11)
plt.legend()
plt.xlabel('距离地铁距离')
plt.show()
[图片]
可以发现租金和地铁数呈正相关，和地铁距离呈负相关。也就是租房数据分析.md中说的“从地理位置上来看，交通越便利，租金也越贵”


