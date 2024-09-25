# 用于修改文件名称，可以作为模板保存并根据需要修改
import os

# 文件夹路径
path = os.path.abspath(r'对应路径\A赛数据 - 副本')
# 文件后缀
filename_extenstion = '.xlsx'
# 汇总后的列名
new_filename = ['data_1', 'data_2', 'data_3', 'data_4', 'data_5', 'data_6', 'data_7']

count = 0
for filename in os.listdir(path):
    # 按.xlsx后缀匹配
    if os.path.splitext(filename)[1] == filename_extenstion:
        t = os.path.splitext(filename)[0]
        # 拼接.xlsx后缀，生成完整文件名
        os.rename(os.path.join(path,t + filename_extenstion),os.path.join(path,new_filename[count] + filename_extenstion))
        count += 1
