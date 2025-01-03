import pandas as pd
from wordcloud import WordCloud

# 读取Excel文件
file_path = 'topic_count.xlsx'  # 替换为需要读取的Excel文件路径，路径按你自己需要来
df = pd.read_excel(file_path, engine='openpyxl')

# 提取第二列的数值作为权重，根据需要的列调整就行，第三列就改成[:, 2]
weights = df.iloc[:, 1].values

# 计算权重，这里是一个简单的函数，可以根据需要修改
def calculate_weight(value):
    return value * 1

# 计算权重
weighted_weights = [calculate_weight(x) for x in weights]

# 创建一个词云图
import matplotlib.pyplot as plt
# 设置颜色序列(多彩"jet"，暖色"magma"，冷色"viridis")
colormap = "jet"
# 设置自定义字体路径，路径按实际需要来
font_path = "Windows\Fonts\simhei.ttf"

# 设置词云图的相关参数
wordcloud = WordCloud(width=1000, height=800, background_color='white',\
font_path=font_path,colormap=colormap)
# 将第一列与第二列（或第n列，根据你对weights的设置而改变）联系起来，建立键值对
frequencies = dict(zip(df.iloc[:, 0], weighted_weights))
wordcloud.generate_from_frequencies(frequencies=frequencies)

# 显示词云图
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off") # 隐藏坐标轴
plt.show()

# 保存词云图
wordcloud.to_file('wordcloud.png')
