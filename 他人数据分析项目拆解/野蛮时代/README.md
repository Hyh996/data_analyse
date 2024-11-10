# 数据分析项目（野蛮时代）

项目链接：
https://github.com/TurboWay/bigdata_analyse/tree/main/AgeOfBarbarians

该文档是基于项目文件 [野蛮时代数据分析.md](https://github.com/TurboWay/bigdata_analyse/blob/main/AgeOfBarbarians/%E9%87%8E%E8%9B%AE%E6%97%B6%E4%BB%A3%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90.md) 结合一定个人理解所进行的内化整理
> （文档里面“项目原本代码”部分是直接复制的，所有东西包括原作者信息都没有删除）
---
## 数据预处理
### 项目原本代码
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/12/30 14:40
# @Author : way
# @Site : 
# @Describe:  数据处理

import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

############################################# 合并数据文件 ##########################################################
# 只取用于分析的字段，因为字段数太多，去掉没用的字段可以极大的节省内存和提高效率
dir = r"C:\Users\Administrator\Desktop\AgeOfBarbarians"
data_list = []
for path in os.listdir(dir):
    path = os.path.join(dir, path)
    data = pd.read_csv(path)
    data = data[
        ['user_id', 'register_time', 'pvp_battle_count', 'pvp_lanch_count', 'pvp_win_count', 'pve_battle_count',
         'pve_lanch_count', 'pve_win_count', 'avg_online_minutes', 'pay_price', 'pay_count']
    ]
    data_list.append(data)
data = pd.concat(data_list)

############################################# 输出处理 ##########################################################
# 没有重复值
# print(data[data.duplicated()])

# 没有缺失值
# print(data.isnull().sum())

############################################# 数据保存 ##########################################################
# 保存清洗后的数据 mysql
engine = create_engine('mysql://root:root@172.16.122.25:3306/test?charset=utf8')
data.to_sql('age_of_barbarians', con=engine, index=False, if_exists='append')
```
### 拆解分析
> 这段代码是一个Python脚本，用于处理和合并数据文件，然后将其保存到MySQL数据库中。
#### 前期准备
1. 导入必要的库：
- os：用于操作文件和目录。
- pandas (pd)：用于数据处理和分析。
- numpy (np)：用于数值计算（但在这段代码中没有被使用）
- sqlalchemy：用于连接和操作数据库。
```python
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
```
2. 设置数据目录：
  - dir 变量设置了包含数据文件的目录路径。
**注意是目录而不是特定的某一个文件**
```python
dir = r"C:\Users\Administrator\Desktop\AgeOfBarbarians"
```
#### 数据处理
1. 读取和处理数据
使用 os.listdir(dir) 获取目录中的所有文件名。遍历这些文件名，对于每个文件，使用 pd.read_csv 读取CSV文件。然后，使用切片操作选择需要的列，并将选择后的数据添加到 data_list 列表中。
```python
data_list = []
for path in os.listdir(dir):
    path = os.path.join(dir, path)
    data = pd.read_csv(path)
    data = data[
        ['user_id', 'register_time', 'pvp_battle_count', 'pvp_lanch_count', 'pvp_win_count', 'pve_battle_count',
         'pve_lanch_count', 'pve_win_count', 'avg_online_minutes', 'pay_price', 'pay_count']
    ]
    data_list.append(data)
```
注意这里目录是只读取了两个文件，最好新建一个文件夹读取，不然会在读取时报错（亲测发现的，检查了好久，如果直接读取网盘下载的文件因为其中几个是解释性质的文件，会影响分析导致报错）
下载文件目录

![image](https://github.com/user-attachments/assets/87d1d049-5080-4521-b5b7-61f2657a44f3)

修改后

![image](https://github.com/user-attachments/assets/6e28db8b-4a4d-4679-be75-e69d316203f8)

2. 合并数据
使用 pd.concat(data_list) 将所有数据框合并成一个单独的数据框。
```python
data = pd.concat(data_list)
```
用print(data.head(5))看：

![image](https://github.com/user-attachments/assets/8c108023-fb29-4b86-b7da-5fcf97ae75a7)

3. 数据检查
代码中包含两个注释掉的打印语句，用于检查数据中是否有重复值或缺失值。
```python
# 没有重复值
print(data[data.duplicated()])

# 没有缺失值
print(data.isnull().sum())
```

![image](https://github.com/user-attachments/assets/f7070bea-794b-4a69-b694-aead199e9293)

4. 数据保存：
使用 sqlalchemy.create_engine 创建数据库引擎，连接到MySQL数据库。

注意这里是先导入了from sqlalchemy import create_engine才直接engine = create_engine('mysql://root:root@172.16.122.25:3306/test?charset=utf8')

使用 data.to_sql 方法将清洗后的数据保存到名为 'age_of_barbarians' 的MySQL表中。参数 index=False 表示不保存行索引，if_exists='append' 表示如果表已存在，则追加数据。
- 'mysql'：表示数据库类型是MySQL。
- 'root:root@172.16.122.25:3306'：表示数据库的用户名、密码和地址。其中，用户名是'root'，密码是'root'，地址是'172.16.122.25'，端口号是'3306'。
- '/test'：表示要连接的数据库名称是'test'。
```python
# 保存清洗后的数据 mysql
engine = create_engine('mysql://root:root@172.16.122.25:3306/test?charset=utf8')
data.to_sql('age_of_barbarians', con=engine, index=False, if_exists='append')
```
这个地方换上自己的信息运行连接数据库的时候，连接不上，暂时没有找到是什么问题（后续修正）
### 修改尝试
参考之前做过的数据预处理，在原基础上加入内容
```python
import os
import pandas as pd

# 合并数据文件
# 只取用于分析的字段，因为字段数太多，去掉没用的字段可以极大的节省内存和提高效率
dir = r"C:\Users\86198\Desktop\tap4fun竞赛数据"

data_list = []
for path in os.listdir(dir):
    path = os.path.join(dir, path)
    data = pd.read_csv(path, encoding="utf-8")
    # 这里是因为之前读取文件的时候反复报错就加了一个报错处理，其实按照原来那样就可以，单纯只是懒得删
    try:
        data = data[
            ['user_id', 'register_time', 'pvp_battle_count', 'pvp_lanch_count',
             'pvp_win_count','pve_battle_count','pve_lanch_count', 'pve_win_count',
             'avg_online_minutes', 'pay_price', 'pay_count']
        ]
        data_list.append(data)
    except KeyError:
        continue
data = pd.concat(data_list)
# 输出处理
# 检查重复值
# print(data[data.duplicated()])
# 重复值处理：默认保留第一个重复值
# data.drop_duplicates(inplace = True)

# 检查缺失值
# print(data.isnull().sum())
# 删除缺失值（行删除法）
# data.dropna()

# 数据保存
# 输出excel文件
data.to_csv(r'C:\Users\86198\Desktop\tap4fun竞赛数据\connect_data.csv', index=False, encoding='utf_8')
```

![image](https://github.com/user-attachments/assets/5d717f6c-80ea-4e98-aff3-fd0e297aa12d)

## 具体分析
### 用sql分析
#### 项目原本代码
> 以下SQL查询提供了对游戏用户行为的深入分析，包括用户数量、活跃度、付费情况和游戏习惯等多个维度。
> （这些数据有助于理解用户群体、优化游戏设计和制定市场策略）
```SQL
-- 修改字段类型
alter table age_of_barbarians modify register_time timestamp(0);
alter table age_of_barbarians modify avg_online_minutes float(10, 2);
alter table age_of_barbarians modify pay_price float(10, 2);

-- 1.用户分析

-- 用户总量
select count(1) as total, count(distinct user_id) as users
from age_of_barbarians

-- PU ( Paying Users）：付费用户总量
select sum(case when pay_price > 0 then 1 else 0 end) as `付费用户`,
       sum(case when pay_price > 0 then 0 else 1 end) as `非付费用户`
from age_of_barbarians

-- DNU（Daily New Users）： 每日游戏中的新登入用户数量，即每日新用户数。
```
点击：点击广告页或者点击广告链接数
下载：点击后成功下载用户数
安装：下载程序并成功安装用户数
激活：成功安装并首次激活应用程序
注册：产生user_id
DNU：产生user_id并且首次登陆
```
select cast(register_time as date) as day,
       count(1) as dnu
from age_of_barbarians
group by cast(register_time as date)
order by day;

-- 每小时的新登入用户数量
select hour(cast(register_time as datetime)) as hour,
       count(1) as dnu
from age_of_barbarians
group by hour(cast(register_time as datetime))
order by hour;


--2.用户活跃度分析

-- DAU、WAU、MAU（Daily Active Users、Weekly Active Users、Monthly Active Users）：每日、每周、每月登陆游戏的用户数，一般为自然周与自然月。

-- 平均在线时长
select avg(avg_online_minutes) as `平均在线时长`,
       sum(case when pay_price > 0 then avg_online_minutes else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户在线时长`,
       sum(case when pay_price > 0 then 0 else avg_online_minutes end) / sum(case when pay_price > 0 then 0 else 1 end) as `非付费用户在线时长`
from age_of_barbarians;



--3.用户付费情况分析

-- APA（Active Payment Account）：活跃付费用户数。
select count(1) as APA from age_of_barbarians where pay_price > 0 and avg_online_minutes > 0; -- 60987

-- ARPU(Average Revenue Per User) ：平均每用户收入。
select sum(pay_price)/sum(case when avg_online_minutes > 0 then 1 else 0 end) from age_of_barbarians;  -- 0.582407

-- ARPPU (Average Revenue Per Paying User)： 平均每付费用户收入。
select sum(pay_price)/sum(case when avg_online_minutes > 0 and pay_price > 0 then 1 else 0 end)  from age_of_barbarians; -- 29.190265

-- PUR(Pay User Rate)：付费比率，可通过 APA/AU 计算得出。
select sum(case when avg_online_minutes > 0 and pay_price > 0 then 1 else 0 end) / sum(case when avg_online_minutes > 0 then 1 else 0 end)
from age_of_barbarians;  -- 0.02

-- 付费用户人数，付费总额，付费总次数，平均每人付费，平均每人付费次数，平均每次付费
select  count(1) as pu,  -- 60988
        sum(pay_price) as sum_pay_price,  -- 1780226.7
        avg(pay_price) as avg_pay_price,  -- 29.189786
        sum(pay_count) as sum_pay_count,  -- 193030
        avg(pay_count) as avg_pay_count,  -- 3.165
        sum(pay_price) / sum(pay_count) as each_pay_price -- 9.222539
from age_of_barbarians
where pay_price > 0;


--4.用户习惯分析

--胜率
select 'PVP' as `游戏类型`,
       sum(pvp_win_count) / sum(pvp_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pvp_win_count else 0 end) / sum(case when pay_price > 0 then pvp_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pvp_win_count else 0 end) / sum(case when pay_price = 0 then pvp_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians
union all
select 'PVE' as `游戏类型`,
       sum(pve_win_count) / sum(pve_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pve_win_count else 0 end) / sum(case when pay_price > 0 then pve_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pve_win_count else 0 end) / sum(case when pay_price = 0 then pve_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians

--pvp场次
select 'PVP' as `游戏类型`,
       avg(pvp_battle_count) as `平均场次`,
       sum(case when pay_price > 0 then pvp_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pvp_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
union all
select 'PVE' as `游戏类型`,
       avg(pve_battle_count) as `均场次`,
       sum(case when pay_price > 0 then pve_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pve_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
```

#### 拆解分析
这段SQL代码包含了几个部分，每部分都针对一个名为 age_of_barbarians 的数据库表进行操作和分析。
1. 修改字段类型：
使用 ALTER TABLE 语句来修改 register_time 字段为 timestamp 类型，avg_online_minutes 和 pay_price 字段为 float 类型，并且指定了小数位数。
```SQL
-- 修改字段类型
alter table age_of_barbarians modify register_time timestamp(0);
alter table age_of_barbarians modify avg_online_minutes float(10, 2);
alter table age_of_barbarians modify pay_price float(10, 2);
```
2. 用户分析：
**用户总量**：计算总记录数和不同 user_id 的数量。
**付费用户总量**：使用 CASE 语句来区分付费用户和非付费用户，并计算它们的数量。
```SQL
-- 1.用户分析

-- 用户总量
select count(1) as total, count(distinct user_id) as users
from age_of_barbarians

-- PU ( Paying Users）：付费用户总量
select sum(case when pay_price > 0 then 1 else 0 end) as `付费用户`,
       sum(case when pay_price > 0 then 0 else 1 end) as `非付费用户`
from age_of_barbarians

-- DNU（Daily New Users）： 每日游戏中的新登入用户数量，即每日新用户数。
```
点击：点击广告页或者点击广告链接数
下载：点击后成功下载用户数
安装：下载程序并成功安装用户数
激活：成功安装并首次激活应用程序
注册：产生user_id
DNU：产生user_id并且首次登陆
```
select cast(register_time as date) as day,
       count(1) as dnu
from age_of_barbarians
group by cast(register_time as date)
order by day;
```
3. 每日新用户数（DNU）：
将 register_time 转换为日期格式，然后按天分组统计新用户数量。
每小时的新用户数量：将 register_time 转换为日期时间格式，并按小时分组统计新用户数量。
```SQL
-- 每小时的新登入用户数量
select hour(cast(register_time as datetime)) as hour,
       count(1) as dnu
from age_of_barbarians
group by hour(cast(register_time as datetime))
order by hour;
```
4. 用户活跃度分析：
计算平均在线时长，以及付费用户和非付费用户的平均在线时长。
```SQL
--2.用户活跃度分析

-- DAU、WAU、MAU（Daily Active Users、Weekly Active Users、Monthly Active Users）：每日、每周、每月登陆游戏的用户数，一般为自然周与自然月。

-- 平均在线时长
select avg(avg_online_minutes) as `平均在线时长`,
       sum(case when pay_price > 0 then avg_online_minutes else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户在线时长`,
       sum(case when pay_price > 0 then 0 else avg_online_minutes end) / sum(case when pay_price > 0 then 0 else 1 end) as `非付费用户在线时长`
from age_of_barbarians;
```

5. 用户付费情况分析：
**活跃付费用户数（APA）**：计算活跃付费用户的数量。
**平均每用户收入（ARPU）**：计算总收入除以活跃用户数。
**每付费用户平均收入（ARPPU）**：计算总收入除以付费用户数。
**付费比率（PUR）**：计算付费用户占活跃用户的比例。
统计付费用户人数、付费总额、付费总次数，以及平均每人付费金额和次数。
```SQL
--3.用户付费情况分析

-- APA（Active Payment Account）：活跃付费用户数。
select count(1) as APA from age_of_barbarians where pay_price > 0 and avg_online_minutes > 0; -- 60987

-- ARPU(Average Revenue Per User) ：平均每用户收入。
select sum(pay_price)/sum(case when avg_online_minutes > 0 then 1 else 0 end) from age_of_barbarians;  -- 0.582407

-- ARPPU (Average Revenue Per Paying User)： 平均每付费用户收入。
select sum(pay_price)/sum(case when avg_online_minutes > 0 and pay_price > 0 then 1 else 0 end)  from age_of_barbarians; -- 29.190265

-- PUR(Pay User Rate)：付费比率，可通过 APA/AU 计算得出。
select sum(case when avg_online_minutes > 0 and pay_price > 0 then 1 else 0 end) / sum(case when avg_online_minutes > 0 then 1 else 0 end)
from age_of_barbarians;  -- 0.02

-- 付费用户人数，付费总额，付费总次数，平均每人付费，平均每人付费次数，平均每次付费
select  count(1) as pu,  -- 60988
        sum(pay_price) as sum_pay_price,  -- 1780226.7
        avg(pay_price) as avg_pay_price,  -- 29.189786
        sum(pay_count) as sum_pay_count,  -- 193030
        avg(pay_count) as avg_pay_count,  -- 3.165
        sum(pay_price) / sum(pay_count) as each_pay_price -- 9.222539
from age_of_barbarians
where pay_price > 0;
```
6. 用户习惯分析：
**胜率**：计算PVP和PVE模式下的平均胜率、付费用户胜率和非付费用户胜率。
**PVP场次**：计算PVP和PVE模式下的平均场次、付费用户平均场次和非付费用户平均场次。
```SQL
--4.用户习惯分析

--胜率
select 'PVP' as `游戏类型`,
       sum(pvp_win_count) / sum(pvp_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pvp_win_count else 0 end) / sum(case when pay_price > 0 then pvp_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pvp_win_count else 0 end) / sum(case when pay_price = 0 then pvp_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians
union all
select 'PVE' as `游戏类型`,
       sum(pve_win_count) / sum(pve_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pve_win_count else 0 end) / sum(case when pay_price > 0 then pve_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pve_win_count else 0 end) / sum(case when pay_price = 0 then pve_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians

--pvp场次
select 'PVP' as `游戏类型`,
       avg(pvp_battle_count) as `平均场次`,
       sum(case when pay_price > 0 then pvp_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pvp_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
union all
select 'PVE' as `游戏类型`,
       avg(pve_battle_count) as `均场次`,
       sum(case when pay_price > 0 then pve_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pve_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
```
### 用python分析
```pythoin
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/12/30 15:46
# @Author : way
# @Site : 
# @Describe:

import os
import pandas as pd
from sqlalchemy import create_engine
from pyecharts import options as opts
from pyecharts.charts import Pie, Line, Bar, Liquid

engine = create_engine('mysql://root:root@172.16.122.25:3306/test?charset=utf8')

# PU 占比
sql = """
select sum(case when pay_price > 0 then 1 else 0 end) as `付费用户`,
       sum(case when pay_price > 0 then 0 else 1 end) as `非付费用户`
from age_of_barbarians
"""
data = pd.read_sql(con=engine, sql=sql)
c1 = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(data.columns, data.values[0])],
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} 占比: {d}%"))
    .render("pie_pu.html")
)
os.system("pie_pu.html")

# DNU 柱形图
sql = """
select cast(register_time as date) as day,
       count(1) as dnu
from age_of_barbarians
group by cast(register_time as date)
order by day;
"""
data = pd.read_sql(con=engine, sql=sql)

c2 = (
    Bar()
    .add_xaxis(list(data['day']))
    .add_yaxis("新增用户数", list(data['dnu']))
    .set_global_opts(title_opts=opts.TitleOpts(title="每日新增用户数量"))
    .render("bar_dnu.html")
)
os.system("bar_dnu.html")

# 每小时注册情况
sql = """
select hour(cast(register_time as datetime)) as hour,
       count(1) as dnu
from age_of_barbarians
group by hour(cast(register_time as datetime))
order by hour;
"""
data = pd.read_sql(con=engine, sql=sql)
c3 = (
    Line()
    .add_xaxis(list(data['hour']))
    .add_yaxis("新增用户数", list(data['dnu']))
    .set_global_opts(title_opts=opts.TitleOpts(title="每小时新增用户数量"))
    .render("line_dnu.html")
)
os.system("line_dnu.html")

# 每小时注册情况
sql = """
select avg(avg_online_minutes) as `平均在线时长`,
       sum(case when pay_price > 0 then avg_online_minutes else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费玩家在线时长`,
       sum(case when pay_price > 0 then 0 else avg_online_minutes end) / sum(case when pay_price > 0 then 0 else 1 end) as `非付费玩家在线时长`
from age_of_barbarians;
"""
data = pd.read_sql(con=engine, sql=sql)
c4 = (
    Bar()
    .add_xaxis(list(data.columns))
    .add_yaxis("平均在线时长(单位：分钟)", list(data.values[0]))
    .set_global_opts(title_opts=opts.TitleOpts(title="平均在线时长"))
    .render("bar_online.html")
)
os.system("bar_online.html")

# 付费比率
sql = """
select sum(case when avg_online_minutes > 0 and pay_price > 0 then 1 else 0 end) / sum(case when avg_online_minutes > 0 then 1 else 0 end) as `rate`
from age_of_barbarians;  
"""
data = pd.read_sql(con=engine, sql=sql)
c5 = (
    Liquid()
    .add("lq", [data['rate'][0], data['rate'][0]])
    .set_global_opts(title_opts=opts.TitleOpts(title="付费比率"))
    .render("liquid_base.html")
)
os.system("liquid_base.html")

# 用户游戏胜率
sql = """
select 'PVP' as `游戏类型`,
       sum(pvp_win_count) / sum(pvp_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pvp_win_count else 0 end) / sum(case when pay_price > 0 then pvp_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pvp_win_count else 0 end) / sum(case when pay_price = 0 then pvp_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians
union all
select 'PVE' as `游戏类型`,
       sum(pve_win_count) / sum(pve_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pve_win_count else 0 end) / sum(case when pay_price > 0 then pve_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pve_win_count else 0 end) / sum(case when pay_price = 0 then pve_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians
"""
data = pd.read_sql(con=engine, sql=sql)
c6 = (
    Bar()
    .add_dataset(
    source=[data.columns.tolist()] + data.values.tolist()
    )
    .add_yaxis(series_name="平均胜率", y_axis=[])
    .add_yaxis(series_name="付费用户胜率", y_axis=[])
    .add_yaxis(series_name="非付费用户胜率", y_axis=[])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="游戏胜率"),
        xaxis_opts=opts.AxisOpts(type_="category"),
    )
    .render("dataset_bar_rate.html")
)
os.system("dataset_bar_rate.html")

# 用户游戏场次
sql = """
select 'PVP' as `游戏类型`,
       avg(pvp_battle_count) as `平均场次`,
       sum(case when pay_price > 0 then pvp_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pvp_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
union all 
select 'PVE' as `游戏类型`,
       avg(pve_battle_count) as `均场次`,
       sum(case when pay_price > 0 then pve_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pve_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
"""
data = pd.read_sql(con=engine, sql=sql)
c7 = (
    Bar()
    .add_dataset(
    source=[data.columns.tolist()] + data.values.tolist()
    )
    .add_yaxis(series_name="平均场次", y_axis=[])
    .add_yaxis(series_name="付费用户平均场次", y_axis=[])
    .add_yaxis(series_name="非付费用户平均场次", y_axis=[])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="游戏场次"),
        xaxis_opts=opts.AxisOpts(type_="category"),
    )
    .render("dataset_bar_times.html")
)
os.system("dataset_bar_times.html")
```
#### 拆解分析
这段Python脚本使用了pyecharts库来生成图表，用于可视化数据库中的数据。本质上是借助sqlalchemy库使用sql辅助分析并将数据库查询结果转换为图表，以便于分析和展示。
1. 创建数据库引擎：
  - 使用 sqlalchemy.create_engine 创建连接到MySQL数据库的引擎。
```python
engine = create_engine('mysql://root:root@172.16.122.25:3306/test?charset=utf8')
```
2. 绘制图表：
  - 使用 pandas 的 read_sql 方法执行SQL查询并获取数据。
  - 使用 pyecharts 库中的图表类（如Pie, Line, Bar, Liquid）来创建不同类型的图表。
  - 每个图表都设置了一些选项，如标题、轴标签、数据标签格式等。
  - 图表渲染为HTML文件，并使用 os.system 命令在默认的网页浏览器中打开。
**PU占比**
使用饼图展示付费用户和非付费用户的比例。
```python
# PU 占比
sql = """
select sum(case when pay_price > 0 then 1 else 0 end) as `付费用户`,
       sum(case when pay_price > 0 then 0 else 1 end) as `非付费用户`
from age_of_barbarians
"""
data = pd.read_sql(con=engine, sql=sql)
c1 = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(data.columns, data.values[0])],
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} 占比: {d}%"))
    .render("pie_pu.html")
)
os.system("pie_pu.html")
```
在默认的web浏览器中打开生成的HTML文件
- **适用于macOS**: system("open pie_pu.html")  
- **用于Windows8**: system("start pie_pu.html")  
- **适用于Linux**: system("xdg-open pie_pu.html")  

**DNU柱形图**
展示每日新增用户数量的柱形图。
```python
# DNU 柱形图
sql = """
select cast(register_time as date) as day,
       count(1) as dnu
from age_of_barbarians
group by cast(register_time as date)
order by day;
"""
data = pd.read_sql(con=engine, sql=sql)

c2 = (
    Bar()
    .add_xaxis(list(data['day']))
    .add_yaxis("新增用户数", list(data['dnu']))
    .set_global_opts(title_opts=opts.TitleOpts(title="每日新增用户数量"))
    .render("bar_dnu.html")
)
os.system("bar_dnu.html")
```
**每小时注册情况**
使用折线图展示每小时的新增用户数量。
```python
# 每小时注册情况
sql = """
select hour(cast(register_time as datetime)) as hour,
       count(1) as dnu
from age_of_barbarians
group by hour(cast(register_time as datetime))
order by hour;
"""
data = pd.read_sql(con=engine, sql=sql)
c3 = (
    Line()
    .add_xaxis(list(data['hour']))
    .add_yaxis("新增用户数", list(data['dnu']))
    .set_global_opts(title_opts=opts.TitleOpts(title="每小时新增用户数量"))
    .render("line_dnu.html")
)
os.system("line_dnu.html")
```
**平均在线时长**
使用柱形图展示平均在线时长，包括付费用户和非付费用户。
```python
# 平均在线时长
sql = """
select avg(avg_online_minutes) as `平均在线时长`,
       sum(case when pay_price > 0 then avg_online_minutes else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费玩家在线时长`,
       sum(case when pay_price > 0 then 0 else avg_online_minutes end) / sum(case when pay_price > 0 then 0 else 1 end) as `非付费玩家在线时长`
from age_of_barbarians;
"""
data = pd.read_sql(con=engine, sql=sql)
c4 = (
    Bar()
    .add_xaxis(list(data.columns))
    .add_yaxis("平均在线时长(单位：分钟)", list(data.values[0]))
    .set_global_opts(title_opts=opts.TitleOpts(title="平均在线时长"))
    .render("bar_online.html")
)
os.system("bar_online.html")
```
**付费比率**
使用水波图展示付费用户的比例。
```python
# 付费比率
sql = """
select sum(case when avg_online_minutes > 0 and pay_price > 0 then 1 else 0 end) / sum(case when avg_online_minutes > 0 then 1 else 0 end) as `rate`
from age_of_barbarians;  
"""
data = pd.read_sql(con=engine, sql=sql)
c5 = (
    Liquid()
    .add("lq", [data['rate'][0], data['rate'][0]])
    .set_global_opts(title_opts=opts.TitleOpts(title="付费比率"))
    .render("liquid_base.html")
)
os.system("liquid_base.html")
```
**用户游戏胜率**
使用柱形图展示不同用户类型的游戏胜率。
```python
# 用户游戏胜率
sql = """
select 'PVP' as `游戏类型`,
       sum(pvp_win_count) / sum(pvp_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pvp_win_count else 0 end) / sum(case when pay_price > 0 then pvp_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pvp_win_count else 0 end) / sum(case when pay_price = 0 then pvp_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians
union all
select 'PVE' as `游戏类型`,
       sum(pve_win_count) / sum(pve_battle_count) as `平均胜率`,
       sum(case when pay_price > 0 then pve_win_count else 0 end) / sum(case when pay_price > 0 then pve_battle_count else 0 end) as `付费用户胜率`,
       sum(case when pay_price = 0 then pve_win_count else 0 end) / sum(case when pay_price = 0 then pve_battle_count else 0 end) as `非付费用户胜率`
from age_of_barbarians
"""
data = pd.read_sql(con=engine, sql=sql)
c6 = (
    Bar()
    .add_dataset(
    source=[data.columns.tolist()] + data.values.tolist()
    )
    .add_yaxis(series_name="平均胜率", y_axis=[])
    .add_yaxis(series_name="付费用户胜率", y_axis=[])
    .add_yaxis(series_name="非付费用户胜率", y_axis=[])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="游戏胜率"),
        xaxis_opts=opts.AxisOpts(type_="category"),
    )
    .render("dataset_bar_rate.html")
)
os.system("dataset_bar_rate.html")
```
**用户游戏场次**
使用柱形图展示不同用户类型的平均游戏场次。
```python
# 用户游戏场次
sql = """
select 'PVP' as `游戏类型`,
       avg(pvp_battle_count) as `平均场次`,
       sum(case when pay_price > 0 then pvp_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pvp_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
union all 
select 'PVE' as `游戏类型`,
       avg(pve_battle_count) as `均场次`,
       sum(case when pay_price > 0 then pve_battle_count else 0 end) / sum(case when pay_price > 0 then 1 else 0 end) as `付费用户平均场次`,
       sum(case when pay_price = 0 then pve_battle_count else 0 end) / sum(case when pay_price = 0 then 1 else 0 end) as `非付费用户平均场次`
from age_of_barbarians
"""
data = pd.read_sql(con=engine, sql=sql)
c7 = (
    Bar()
    .add_dataset(
    source=[data.columns.tolist()] + data.values.tolist()
    )
    .add_yaxis(series_name="平均场次", y_axis=[])
    .add_yaxis(series_name="付费用户平均场次", y_axis=[])
    .add_yaxis(series_name="非付费用户平均场次", y_axis=[])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="游戏场次"),
        xaxis_opts=opts.AxisOpts(type_="category"),
    )
    .render("dataset_bar_times.html")
)
os.system("dataset_bar_times.html")
```
### 修改尝试
*这里是尝试基于具体分析绕过sql代码的修改*
代码
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 导入数据
df = pd.read_csv(r'C:\Users\86198\Desktop\connect_data.csv')

# 将register_time转换为datetime
df['register_time'] = pd.to_datetime(df['register_time'])

# 1. 用户分析

# 用户总量
total_users = len(df)
distinct_users = df['user_id'].nunique()

# PU (Paying Users)：付费用户总量
paying_users = df['pay_price'].apply(lambda x: 1 if x > 0 else 0).sum()
non_paying_users = df['pay_price'].apply(lambda x: 0 if x > 0 else 1).sum()

# 绘制付费用户占总用户比例
sizes = [total_users, paying_users]
labels = ['total_users', 'paying_users']
plt.pie(sizes, labels=labels)
plt.show()

# DNU（Daily New Users）:每日新增用户
df['day'] = df['register_time'].dt.date
daily_new_users = df.groupby('day').size().reset_index(name='dnu')
plt.figure(figsize=(12, 6))
sns.lineplot(data=daily_new_users, x='day', y='dnu')
plt.title('Daily New Users')
plt.xlabel('Day')
plt.ylabel('New Users')
plt.xticks(rotation=45)
plt.show()

# 每小时的新登入用户数量
df['hour'] = df['register_time'].dt.hour
hourly_new_users = df.groupby('hour').size().reset_index(name='dnu')
sns.lineplot(data=hourly_new_users, x='hour', y='dnu')
plt.title('Hourly New Users')
plt.xlabel('Hour')
plt.ylabel('New Users')
plt.show()

# 2. 用户活跃度分析

# 平均在线时长
average_online_minutes = df['avg_online_minutes'].mean()
paying_user_online_minutes = df.loc[df['pay_price'] > 0, 'avg_online_minutes'].mean()
non_paying_user_online_minutes = df.loc[df['pay_price'] == 0, 'avg_online_minutes'].mean()

online_minutes = ['average_online_minutes','paying_user_online_minutes','non_paying_user_online_minutes']
online_minutes_value = [average_online_minutes,paying_user_online_minutes,non_paying_user_online_minutes]
plt.bar(online_minutes, online_minutes_value)
plt.xticks(rotation=45)
plt.show()

# 3. 用户付费情况分析

# APA（Active Payment Account）:有效付款帐户
apa = df[(df['pay_price'] > 0) & (df['avg_online_minutes'] > 0)].shape[0]

# ARPU（Average Revenue Per User）:每用户平均收益
arpu = df['pay_price'].sum() / df.loc[df['avg_online_minutes'] > 0].shape[0]

# ARPPU (Average Revenue Per Paying User):每付费用户平均收益
arppu = df['pay_price'].sum() / df[(df['avg_online_minutes'] > 0) & (df['pay_price'] > 0)].shape[0]

# PUR（Pay User Rate）:付费用户率
pur = df[(df['avg_online_minutes'] > 0) & (df['pay_price'] > 0)].shape[0] / df[df['avg_online_minutes'] > 0].shape[0]

# 付费用户人数，付费总额，付费总次数，平均每人付费，平均每人付费次数，平均每次付费
pay_stats = df[df['pay_price'] > 0].agg({
    'user_id': 'count',
    'pay_price': ['sum', 'mean'],
    'pay_count': ['sum', 'mean']
})
each_pay_price = pay_stats.loc['sum', 'pay_price'] / pay_stats.loc['sum', 'pay_count']

# 4. 用户习惯分析

# 胜率
pvp_stats = df[['pvp_win_count', 'pvp_battle_count', 'pay_price']].copy()
pve_stats = df[['pve_win_count', 'pve_battle_count', 'pay_price']].copy()

def calculate_win_rate(stats, battle_type):
    stats[f'{battle_type}_win_rate'] = stats[f'{battle_type}_win_count'] / stats[f'{battle_type}_battle_count']
    avg_win_rate = stats[f'{battle_type}_win_rate'].mean()
    paying_win_rate = stats[stats['pay_price'] > 0][f'{battle_type}_win_rate'].mean()
    non_paying_win_rate = stats[stats['pay_price'] == 0][f'{battle_type}_win_rate'].mean()
    return avg_win_rate, paying_win_rate, non_paying_win_rate

pvp_avg_win_rate, pvp_paying_win_rate, pvp_non_paying_win_rate = calculate_win_rate(pvp_stats, 'pvp')
pve_avg_win_rate, pve_paying_win_rate, pve_non_paying_win_rate = calculate_win_rate(pve_stats, 'pve')
win_rate_x = ['pvp_avg_win_rate', 'pvp_paying_win_rate', 'pvp_non_paying_win_rate','pve_avg_win_rate', 'pve_paying_win_rate', 'pve_non_paying_win_rate']
win_rate_y = [pvp_avg_win_rate, pvp_paying_win_rate, pvp_non_paying_win_rate,pve_avg_win_rate, pve_paying_win_rate, pve_non_paying_win_rate]
plt.bar(win_rate_x, win_rate_y)
plt.xticks(rotation=45)
plt.show()

# 平均场次
def calculate_avg_battles(stats, battle_type):
    avg_battles = stats[f'{battle_type}_battle_count'].mean()
    paying_avg_battles = stats[stats['pay_price'] > 0][f'{battle_type}_battle_count'].mean()
    non_paying_avg_battles = stats[stats['pay_price'] == 0][f'{battle_type}_battle_count'].mean()
    return avg_battles, paying_avg_battles, non_paying_avg_battles

pvp_avg_battles, pvp_paying_avg_battles, pvp_non_paying_avg_battles = calculate_avg_battles(pvp_stats, 'pvp')
pve_avg_battles, pve_paying_avg_battles, pve_non_paying_avg_battles = calculate_avg_battles(pve_stats, 'pve')
avg_battles_x = ['pvp_avg_battles', 'pvp_paying_avg_battles', 'pvp_non_paying_avg_battles', 'pve_avg_battles', 'pve_paying_avg_battles', 'pve_non_paying_avg_battles']
avg_battles_y = [pvp_avg_battles, pvp_paying_avg_battles, pvp_non_paying_avg_battles, pve_avg_battles, pve_paying_avg_battles, pve_non_paying_avg_battles]
plt.bar(win_rate_x, win_rate_y)
plt.xticks(rotation=45)
plt.show()

# 输出结果
print(f"'总用户数': {total_users}")
print(f"'不同用户': {distinct_users}")
print(f"'付费用户': {paying_users}")
print(f"'非付费用户': {non_paying_users}")
print(daily_new_users.head())
print(hourly_new_users.head())
print(f"'平均上网时间': {average_online_minutes}")
print(f"'付费用户上网时间': {paying_user_online_minutes}")
print(f"'非付费用户在线分钟数': {non_paying_user_online_minutes}")
print(f"'有效付款帐户': {apa}")
print(f"'每用户平均收益': {arpu}")
print(f"'每付费用户平均收益': {arppu}")
print(f"'付费用户率': {pur}")
print(pay_stats)
print(f"'平均每次付费': {each_pay_price}")
print(f"'PVP平均胜率': {pvp_avg_win_rate}")
print(f"'PVP付费胜率': {pvp_paying_win_rate}")
print(f"'PVP非付费胜率': {pvp_non_paying_win_rate}")
print(f"'PVE平均胜率': {pve_avg_win_rate}")
print(f"'PVE付费胜率': {pve_paying_win_rate}")
print(f"'PVE非付费胜率': {pve_non_paying_win_rate}")
print(f"'PVP平均战斗数': {pvp_avg_battles}")
print(f"'PVP平均战斗付费': {pvp_paying_avg_battles}")
print(f"'PVP非付费平均战斗': {pvp_non_paying_avg_battles}")
print(f"'PVE平均战斗数': {pve_avg_battles}")
print(f"'PVE平均战斗付费': {pve_paying_avg_battles}")
print(f"PVE非付费平均战斗: {pve_non_paying_avg_battles}")
```
结果
|||
|----|----|
|![image](https://github.com/user-attachments/assets/32a7c745-4e08-4d36-a3f2-e5c5aa8d0d10)|![image](https://github.com/user-attachments/assets/cc712262-a894-467f-9d63-cd2322d256d2)|

这里画的饼图有问题labels = ['total_users', 'paying_users']应该改成labels = ['non_paying_users', 'paying_users']

另外“每小时的新登入用户数量”部分原来项目实例里是画的柱状图，个人是觉得折线图也可以找出突出时间段，就直接用折线图
