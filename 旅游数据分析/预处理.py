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
# # 保存数据进数据库
# engine = create_engine('mysql://031103:031103@localhost:3306/test?charset=utf8')
# data.to_sql('旅游数据汇总（04-18）', con=engine, index=False, if_exists='append')
