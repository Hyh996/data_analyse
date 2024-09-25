# 用于转换个别非平衡面板数据并将excel中多个sheet合并
import pandas as pd
# 非平衡面板转平衡面板
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

# 非平衡面板转平衡面板并合并多个sheet表
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
