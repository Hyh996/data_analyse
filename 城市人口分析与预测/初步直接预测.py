import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings

# 忽略报错（主程序中mean_squared_error会导致报错，但并不影响程序运行，为了输出简洁的结果，这里采取直接忽略报错的方式）
warnings.filterwarnings('ignore',category=Warning)

# 指定默认字体，'SimHei'为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 加载数据
data = pd.read_csv(r'对应路径\城市人口分析与预测常住人口数据.csv')

# 创建列表（方便后续结果写入）
data_to_append = []

# 按照城市分组
grouped = data.groupby('城市名称')

# 遍历每个城市
for city, group_data in grouped:
    # 将人口数据转换为时间序列
    population_series = group_data.set_index('年份')['常住人口（万人）']

    # 平稳性检测
    adf_test = adfuller(population_series)
    print(f'\nCity: {city}')
    print('ADF Statistic: %f' % adf_test[0])
    print('p-value: %f' % adf_test[1])

    # 差分
    population_diff = population_series.diff().dropna()
    adf_test_diff = adfuller(population_diff)
    print('ADF Statistic (diff): %f' % adf_test_diff[0])
    print('p-value (diff): %f' % adf_test_diff[1])

    # # ACF和PACF图
    # plot_acf(population_diff, lags=14)
    # plot_pacf(population_diff, lags=6, method='ywm')
    # plt.show()

    # 模型定阶
    p = q = d = 0
    for i in range(5):
        for j in range(5):
            for k in range(5):
                try:
                    model = ARIMA(data, order=(i, d, j))
                    results = model.fit()
                    if results.aic < min_aic:
                        min_aic = results.aic
                        p, d, q = i, d, j
                except:
                    continue

    # 分割数据集,80%的数据用于训练，20%用于测试
    split_ratio = 0.8
    train_size = int(len(population_series) * split_ratio)
    train, test = population_series[0:train_size], population_series[train_size:]

    # 模型拟合
    model = ARIMA(train, order=(p, d, q))
    results = model.fit()
    # # 模型检验
    # results.plot_diagnostics(figsize=(21, 12))
    # plt.show()
    # 预测
    forecast = results.forecast(steps=len(test))
    # 计算预测值和真实值之间的MSE和RMSE
    mse = mean_squared_error(test, forecast)
    score =1/(1+mse)
    print(f'MSE: {mse}')
    print(f'评估得分: {score}')

    # 使用模型预测2023年的人口
    # 模型拟合
    model = ARIMA(population_series, order=(p, d, q))
    results = model.fit()
    # 预测
    forecast = results.forecast(steps=1).iloc[0]
    print(f'2023年预测值: {forecast}')
    # 结果统一写入列表
    end_result = []
    end_result.append(city)
    end_result.append("2023")
    end_result.append(forecast)
    data_to_append.append(end_result)

df = pd.DataFrame({'city_id':[],'year':[],'pred':[]})
new_data = pd.DataFrame(data_to_append, columns=['city_id','year','pred'])
df = df._append(new_data, ignore_index=True)
# 转换数据类型
df['city_id'] = df['city_id'].astype(str)
df['year'] = df['year'].astype(np.int64)
# 检查属性
df.info()
print(df)
# # 导出
df.to_csv(r'对应路径\submission.csv', index=False)
