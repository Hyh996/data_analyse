# 数据预处理（1.3）
## 前期准备
> 固定起手式

```python
# 必备
import pandas as pd
# 一般情况下encoding='gbk'或'utf-8'，实在不行上网查查改其他的，或者直接将原来的文档另存为csv utf-8的格式
file = pd.read_csv(r'对应文件的路径.csv',encoding='gbk')
```

> 备选常用
```python
# 一般情况下只有需要数值运算处理数据时才需要
import numpy as np
# 导出进数据库时需要，用于连接和操作数据库
from sqlalchemy import create_engine
```

## 处理主体
__常用函数__
### 排序
```python
# 按照日期排序
file['日期'] = pd.to_datetime(file['日期'])
file = file.sort_values(by='日期')
```

## sort_values()函数用途

pandas中的sort_values()函数原理类似于SQL中的order by，可以将数据集依照某个字段中的数据进行排序，该函数即可根据指定列数据也可根据指定行的数据排序。

```python
DataFrame.sort_values(by=‘##’,axis=0,ascending=True, inplace=False, na_position=‘last’)
```

> 参数说明：
- by：指定列名(axis=0或’index’)或索引值(axis=1或’columns’)
- axis：若axis=0或’index’，则按照指定列中数据大小排序；若axis=1或’columns’，则按照指定索引中数据大小排序，默认axis=0
- ascending：是否按指定列的数组升序排列，默认为True，即升序排列
- inplace：是否用排序后的数据集替换原来的数据，默认为False，即不替换
- na_position：{‘first’,‘last’}，设定缺失值的显示位置
___

### 空值处理
```python
# 检查是否存在空值
print(file.isnull().sum())
# 缺失值处理：直接删除缺失值所在行，并重置索引
# print(data.isnull().sum())
data.dropna(axis=0, inplace=True)
data.reset_index(drop=True, inplace=True)
```
如果我们要删除包含空字段的行，可以使用 dropna() 方法，语法格式如下：

```python
DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
```

参数说明：
- axis：默认为 0，表示逢空值剔除整行，如果设置参数 axis＝1 表示逢空值去掉整列。
- how：默认为 'any' 如果一行（或一列）里任何一个数据有出现 NA 就去掉整行，如果设置 how='all' 一行（或列）都是 NA 才去掉这整行。
- thresh：设置需要多少非空值的数据才可以保留下来的。
- subset：设置想要检查的列。如果是多个列，可以使用列名的 list 作为参数。
- inplace：如果设置 True，将计算得到的值直接覆盖之前的值并返回 None，修改的是源数据。

删除包含空数据的行：
__注意：使用该方法的前提是数据量足够大，如若数据量较少时直接进行删除的方法并不合适，可能会导致后续分析的结果并不能反映实际情况__

```python
import pandas as pd

df = pd.read_csv('property-data.csv')
new_df = df.dropna()
print(new_df.to_string())
以上实例输出结果如下：
![image](https://github.com/user-attachments/assets/43944780-f353-4336-bb2f-edee3761490c)
注意：默认情况下，dropna() 方法返回一个新的 DataFrame，不会修改源数据。
如果你要修改源数据 DataFrame, 可以使用 inplace = True 参数:
import pandas as pd

df = pd.read_csv('property-data.csv')

df.dropna(inplace = True)

print(df.to_string())
```
以上实例输出结果如下：
![image](https://github.com/user-attachments/assets/5ce5baec-0dc0-4911-ae03-697955ff4c16)

替换空单元格的常用方法是计算列的均值、中位数值或众数。
Pandas使用 mean()、median() 和 mode() 方法计算列的均值（所有值加起来的平均值）、中位数值（排序后排在中间的数）和众数（出现频率最高的数）。
使用 mean() 方法计算列的均值并替换空单元格：
```python
import pandas as pd

df = pd.read_csv('property-data.csv')
x = df["ST_NUM"].mean()
df["ST_NUM"].fillna(x, inplace = True)
print(df.to_string())
```
  
### 重置索引reset_index（）
重置数据帧的索引，并使用默认索引。如果数据帧具有多重索引，则此方法可以删除一个或多个level。

```python
reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')
```

> 参数说明
- level：可以是int, str, tuple, or list, default None等类型。作用是只从索引中删除给定级别。默认情况下删除所有级别。
- drop：bool, default False。不要尝试在数据帧列中插入索引。这会将索引重置为默认的整数索引。
- inplace：bool, default False。修改数据帧（不要创建新对象）。
- col_level：int or str, default=0。如果列有多个级别，则确定将标签插入到哪个级别。默认情况下，它将插入到第一层。
- col_fill：object, default。如果列有多个级别，则确定其他级别的命名方式。如果没有，则复制索引名称。
__返回：__
DataFrame or None。具有新索引的数据帧，如果inplace=True，则无索引。
当然还有同时存在两个表，可以互补缺失数据的情况
> 该例子截取自《利用python进行数据分析（第二版）》

对于DataFrame，combine first自然也会在列上做同样的事情，因此你可以将其看做:用传递对象中的数据为调用对象的缺失数据“打补丁":

df1

![image](https://github.com/user-attachments/assets/75f7dcaf-6876-4da9-bad1-7c5c5132994e)

df2

![image](https://github.com/user-attachments/assets/fc621f5f-c26d-4d07-a824-56bee8d1578d)

```python
ls = df1.combine first(df2)
print(ls)
```
![image](https://github.com/user-attachments/assets/30a0101c-6ee3-4b8f-ac97-b9d3cd0ce32d)


___

### 重复值处理
```python
#  数据重复处理: 删除重复值
print(data[data.duplicated()])
data.drop_duplicates(inplace=True)
data.reset_index(drop=True, inplace=True) # 同理以上重置索引内容
```
___

### 异常值处理
```python
# 去除异常值
file = file.loc[file['货量']<80000]
# 异常值清洗
data['户型'].unique()
# print(data[data['户型'] == '户型'])
data = data[data['户型'] != '户型']
```

删除重复数据，可以直接使用drop_duplicates() 方法。
```python
df.drop_duplicates(subset=['A','B','C'],keep='first',inplace=True)
```
- subset：表示要进去重的列名，默认为 None。
- keep：有三个可选参数，分别是 first、last、False，默认为 first，表示只保留第一次出现的重复项，删除其余重复项，last 表示只保留最后一次出现的重复项，False 则表示删除所有重复项。
- inplace：布尔值参数，默认为 False 表示删除重复项后返回一个副本，若为 Ture 则表示直接在原数据上删除重复项。

数据错误也是很常见的情况，我们可以对错误的数据进行替换或移除。
替换错误年龄数据：
```python
import pandas as pd

person = {
  "name": ['Google', 'Runoob' , 'Taobao'],
  "age": [50, 40, 12345]    # 12345 年龄数据是错误的
}
df = pd.DataFrame(person)
df.loc[2, 'age'] = 30      # 修改数据
print(df.to_string())
```
以上实例输出结果如下：
```python
     name  age
0  Google   50
1  Runoob   40
2  Taobao   30
```
也可以设置条件语句：
将 age 大于 120 的设置为 120:
```python
import pandas as pd

person = {
  "name": ['Google', 'Runoob' , 'Taobao'],
  "age": [50, 200, 12345]    
}
df = pd.DataFrame(person)
for x in df.index:
  if df.loc[x, "age"]  120:
    df.loc[x, "age"] = 120
print(df.to_string())
```
以上实例输出结果如下：
```python
     name  age
0  Google   50
1  Runoob  120
2  Taobao  120
```
也可以将错误数据的行删除：
将 age 大于 120 的删除:
```python
import pandas as pd

person = {
  "name": ['Google', 'Runoob' , 'Taobao'],
  "age": [50, 40, 12345]    # 12345 年龄数据是错误的
}
df = pd.DataFrame(person)
for x in df.index:
  if df.loc[x, "age"]  120:
    df.drop(x, inplace = True)
print(df.to_string())
```
以上实例输出结果如下：
```python
     name  age
0  Google   50
1  Runoob   40
```
___

### 插值处理
__以下内容直接引自链接中的项目内容__

[项目链接].(https://github.com/luanshiyinyang/DataMining)

# 该差值处理程序出处：

[链接].(https://github.com/luanshiyinyang/DataMining/blob/master/%E6%95%B0%E6%8D%AE%E9%A2%84%E5%A4%84%E7%90%86/%E6%8F%92%E5%80%BC%E5%A4%84%E7%90%86.py)

```python
import pandas as pd
from scipy.interpolate import lagrange

inputFile = './catering_sale.xls'
outputFile = './sales.xls'

data = pd.read_excel(inputFile)
# 异常值置为空
data[u'销量'][(data[u'销量'] < 400) | (data[u'销量'] > 5000)] = None

# 自定义列向量插值函数
# s为列向量，n为被插值的位置，k为取前后的数据个数，默认为5


def ployinterp_column(s, n, k=5):
    y = s[list(range(n-k, n)) + list(range(n+1, n+1+k))]
    y = y[y.notnull()]
    return lagrange(y.index, list(y))(n)


# 逐个元素判断是否需要插值
for i in data.columns:
    for j in range(len(data)):
        if (data[i].isnull())[j]:
            data[i][j] = ployinterp_column(data[i], j)
data.to_excel(outputFile)
```
___

### 转置
```python
# 转置前先设置好列索引
data.set_index('指标', inplace=True)
# 转置并将转置后的行标签转为第一列
data = data.T.rename_axis("年份").reset_index()
```
___

### 列替换
```python
# 清洗，列替换
data.loc[:, '地铁'] = data['地铁'].apply(lambda x: x.replace('地铁：', ''))
```
___

### 增加列
```python
# 增加列
data.loc[:, '所在楼层'] = data['楼层'].apply(lambda x: int(x.split('/')[0]))
data.loc[:, '总楼层'] = data['楼层'].apply(lambda x: int(x.replace('层', '').split('/')[-1]))
data.loc[:, '地铁数'] = data['地铁'].apply(lambda x: len(re.findall('线', x)))
data.loc[:, '距离地铁距离'] = data['地铁'].apply(lambda x: int(re.findall('(\d+)米', x)[-1]) if re.findall('(\d+)米', x) else -1)
```
___

### 转换数据类型
__可以先使用df.dtypes查看属性__
```python
# 查看属性
print(df.dtypes)
# 数据类型转换
data['价格'] = data['价格'].astype(np.int64)
data['面积'] = data['面积'].astype(np.int64)
data['距离地铁距离'] = data['距离地铁距离'].astype(np.int64)
```
> 通过astype()方法强制转换数据的类型
```python
astype(dypte, copy=True, errors = ‘raise’, **kwargs)
```
__参数说明：__
- dtype：表示数据类型，例如np.int32,np.float64等
- copy：是否建立副本，默认为True
- errors：错误采取的处理方式，可以取值为raise或ignore，默认为raise。其中raise表示允许引发异常，ignore表示抑制异常。

数据格式错误的单元格会使数据分析变得困难，甚至不可能。
我们可以通过包含空单元格的行，或者将列中的所有单元格转换为相同格式的数据。
以下实例会格式化日期：
```python
import pandas as pd
# 第三个日期格式错误
data = {
  "Date": ['2020/12/01', '2020/12/02' , '20201226'],
  "duration": [50, 40, 45]
}
df = pd.DataFrame(data, index = ["day1", "day2", "day3"])
df['Date'] = pd.to_datetime(df['Date'])
print(df.to_string())
```
以上实例输出结果如下：
```python
           Date  duration
day1 2020-12-01        50
day2 2020-12-02        40
day3 2020-12-26        45
```
___

### 规范化处理
同样直接同异常值插值处理部分，直接引用自同一项目。由于之前建模一直用的是R，规范化处理之前都是直接用R完成的，这个地方等后面有时间再内化补充
```python
data = pd.read_excel(file)
# 最小-最大规范化
print((data - data.min())/(data.max() - data.min()) )
# 零-均值规范化
print((data - data.mean())/data.std())
# 小数定标规范化
print(data/10**np.ceil(np.log10(data.abs().max())))
```
补充：R中规范化处理我自己常用的是直接将数值转为-1~1的方法
```R
# 数据标准化处理
s<-scale(w[,-2])
class(s)
s<-data.frame(s,index=c("area","year"))
```
___

### 离散化处理
> 同上异常值插值处理部分，直接引用自同一项目。这里还有点没有完全明白，暂时先不动，等内化了再调整内容
```python
# -*- coding: utf-8 -*-
# 直接引自：https://github.com/luanshiyinyang/DataMining/blob/master/%E6%95%B0%E6%8D%AE%E9%A2%84%E5%A4%84%E7%90%86/%E7%A6%BB%E6%95%A3%E5%8C%96%E5%A4%84%E7%90%86.py

# 数据规范化
import pandas as pd
from sklearn.cluster import KMeans

datafile = './discretization_data.xls'
data = pd.read_excel(datafile)
data = data[u'肝气郁结证型系数'].copy()
k = 4
# 等宽离散化
d1 = pd.cut(data, k, labels=range(k))

# 等频率离散化
w = [1.0 * i / k for i in range(k + 1)]
w = data.describe(percentiles=w)[4:4 + k + 1]  # 使用describe函数自动计算分位数
w[0] = w[0] * (1 - 1e-10)
d2 = pd.cut(data, w, labels=range(k))
kmodel = KMeans(n_clusters=k, n_jobs=4)  # 建立模型，n_jobs是并行数，一般等于CPU数较好
kmodel.fit(data.values.reshape((len(data), 1)))  # 训练模型
c = pd.DataFrame(kmodel.cluster_centers_).sort_values(0)  # 输出聚类中心，并且排序（默认是随机序的）
w = c.rolling(2).mean().iloc[1:]  # 相邻两项求中点，作为边界点
w = [0] + list(w[0]) + [data.max()]  # 把首末边界点加上
d3 = pd.cut(data, w, labels=range(k))


def cluster_plot(d, k):  # 自定义作图函数来显示聚类结果
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    plt.figure(figsize=(8, 3))
    for j in range(0, k):
        plt.plot(data[d == j], [j for i in d[d == j]], 'o')

    plt.ylim(-0.5, k - 0.5)
    return plt


cluster_plot(d1, k).show()

cluster_plot(d2, k).show()
cluster_plot(d3, k).show()
```
___

## 收尾
> 主要是数据处理完事后使用（文件处理那个地方每个都附带文件导出的处理），一般要么导出csv或xsld，要么导入进数据库
### 文件导出
```python
# 保存清洗后的数据 csv
data.to_csv('保存路径/文件名称.csv', index=False)
```
___
### 导入数据库
```python
# 保存清洗后的数据 mysql
engine = create_engine('mysql://root:root@172.16.122.25:3306/test?charset=utf8')
data.to_sql('age_of_barbarians', con=engine, index=False, if_exists='append')
```
__使用 sqlalchemy.create_engine 创建数据库引擎，连接到MySQL数据库。__
注意这里是先导入了
```python
from sqlalchemy import create_engine
```
才直接
```python
engine = create_engine('mysql://root:root@172.16.122.25:3306/test?charset=utf8')
```
使用 data.to_sql 方法将清洗后的数据保存到名为 'age_of_barbarians' 的MySQL表中。参数 index=False 表示不保存行索引，if_exists='append' 表示如果表已存在，则追加数据。
- 'mysql'：表示数据库类型是MySQL。
- 'root:root@172.16.122.25:3306'：表示数据库的用户名、密码和地址。其中，用户名是'root'，密码是'root'，地址是'172.16.122.25'，端口号是'3306'。
- '/test'：表示要连接的数据库名称是'test'。

![image](https://github.com/user-attachments/assets/653b9480-0ca5-4879-b979-22309c52e487)

___

# 完整实例
## 常用模板
> 仅包含导入，排序，数据类型转换，处理空值、重复值、异常值几个常用数据清洗步骤，处理步骤直接用块注释处理了，需要时再使用ctrl+/取消块注释
```python
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 一般情况下encoding='gbk'或'utf-8'，实在不行上网查查改其他的，或者直接将原来的文档另存为csv utf-8的格式
data = pd.read_csv(r'对应文件的路径.csv',encoding='gbk')

# 数据类型转换
# 查看属性
print(data.dtypes)
# # 转换int
# data['需要转换的列'] = data['需要转换的列'].astype(np.int64)

# # 按照某一列排序
# data['指定列'] = pd.to_datetime(data['指定列'])
# data = data.sort_values(by='指定列')

# 检查是否存在空值
print(data.isnull().sum())
# # 缺失值处理：直接删除缺失值所在行，并重置索引
# data.dropna(axis=0, inplace=True)
# data.reset_index(drop=True, inplace=True)

# 数据重复处理: 删除重复值
# 检查重复值
print(data[data.duplicated()])
# # 保留第一个出现的重复值
# data.drop_duplicates(keep = 'first',inplace=True)
# data.reset_index(drop=True, inplace=True)

# # 去除异常值
# data = data.loc[data['要处理的那一列']<设置限制值]

## 转置
## 转置前先设置好列索引
# data.set_index('指标', inplace=True)
## 转置并将转置后的行标签转为第一列
# data = data.T.rename_axis("年份").reset_index()

# 保存清洗后的数据 csv，同理使用to_excel保存.xlsx
data.to_csv('对应文件的路径/保存文件名.csv', index=False)

# 保存清洗后的数据 mysql
engine = create_engine('mysql://用户名:密码@地址:端口号/数据库名称?charset=utf8')
data.to_sql('要保存的名称', con=engine, index=False, if_exists='append')
```
