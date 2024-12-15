import pandas as pd
import semopy

data = semopy.examples.political_democracy.get_data()

desc = '''
# 定义测量模型
ind60 =~ x1 + x2 +x3
dem60 =~ y1 + y2 + y3 + y4
dem65 =~ y5 + y6 + y7 + y8
# 定义结构模型
dem60 ~ ind60
dem65 ~ ind60 + dem60
# 协方差
y1 ~~ y5
y2 ~~ y4 +y6
y3 ~~ y7
y4 ~~ y8
y6 ~~ y8
'''

# 将上述文本转化为 semopy 库中的模型
mod = semopy.Model(desc)

# 对数据进行拟合和估计
res_opt = mod.fit(data)
estimates = mod.inspect()
print(estimates)

# 查看拟合指数
calc_stats = semopy.stats.calc_stats(mod)
print(calc_stats)

# 导出excel表格
# 创建一个简单的 DataFrame
df = pd.DataFrame(estimates)
stats = pd.DataFrame(calc_stats)

# 将 DataFrame 导出到 Excel 文件
df.to_excel('output_PoliticalDemocracy_estimates.xlsx', index=False, engine='openpyxl')
stats.to_excel('output_PoliticalDemocracy_stats.xlsx', index=False, engine='openpyxl')

# 报告
model = semopy.ModelMeans(desc)
model.fit(data)
semopy.report(model, "PoliticalDemocracy")

# 显示 Graphviz 图
graw = semopy.semplot(estimates,"tp.png")
print(graw)
