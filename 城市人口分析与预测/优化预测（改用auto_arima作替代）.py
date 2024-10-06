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
data = pd.read_csv(r'对应路径\城市人口分析与预测常住人口数据.csv')
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
