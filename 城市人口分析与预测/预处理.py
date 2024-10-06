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


# 这个部分本来是考虑搭建特征工程或引入外部变量可能会用到所以写的，但实际上并没有完成特征工程的搭建，也就没有用到
# import pandas as pd
# # 筛选数据完整度最高的2015-2021年剔除年龄结构数据处理并保存，用于构建特征工程后再预测
# # 筛选数据完整度最高的2015-2021年
# years_to_filter = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
# filtered_df = df[df['年份'].isin(years_to_filter)]
# # 剔除年龄结构数据
# df_dropped = filtered_df.drop(columns=['0-14','15-64','65+'])
# # 定义一个函数来合并列值
# def combine_values(x):
#     return [val for val in x if pd.notna(val)]
# # 应用函数并使用agg进行分组合并
# result = df_dropped.groupby(['年份', '城市名称']).agg(combine_values).reset_index()
# # 将结果转换为单个值
# for col in ['employeesNumber','towner_disposableIcome']:
#     result[col] = result[col].apply(lambda x: x[0] if x else None)
# # 缺失值处理：直接删除缺失值所在行，并重置索引
# result.dropna(axis=0, inplace=True)
# result.reset_index(drop=True, inplace=True)
# # 修改城市名称，将city1转为1
# # 创建一个映射字典，将城市名称映射到一个唯一的数字
# city_mapping = {city: i + 1 for i, city in enumerate(result['城市名称'].unique())}
# # 使用映射字典替换城市名称
# result['城市名称'] = result['城市名称'].map(city_mapping)
# # 检查
# print(result)
# # 输出csv
# result.to_csv(r'对应路径\2015-2021年人口规模预测数据集.csv', index=False)
