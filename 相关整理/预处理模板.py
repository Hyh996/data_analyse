# 这是汇总整理的数据预处理模板，主要是整理了一些预处理经常用到的内容，建立目的主要是在需要进行数据预处理的时候直接复制改改就能用
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

# 保存清洗后的数据 csv，同理使用to_excel保存.xlsx
data.to_csv('对应文件的路径/保存文件名.csv', index=False)

# 保存清洗后的数据 mysql
engine = create_engine('mysql://用户名:密码@地址:端口号/数据库名称?charset=utf8')
data.to_sql('要保存的名称', con=engine, index=False, if_exists='append')
