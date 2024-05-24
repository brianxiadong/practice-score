import os
import re
import pandas as pd

def filter_chinese_only(text):
    # 正则表达式匹配非中文字符并替换为空
    cleaned_text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
    return cleaned_text

def collect_homework_data(path):
    all_names = set()

    # 使用os.walk遍历指定目录及其子目录
    for root, dirs, files in os.walk(path):
        for file in files:
            # 将当前目录下的文件名和子目录名添加到集合中
            all_names.add(filter_chinese_only(file))
        for dir in dirs:
             all_names.add(filter_chinese_only(dir))
    non_empty_strings = [s for s in all_names if s]
    return non_empty_strings


if __name__ == '__main__':
    all_names = collect_homework_data('C:/Users/xiadong/Desktop/实训作业/day02')

    # 读取Excel文件
    df = pd.read_excel('D:/作业打分表.xlsx')

    # 遍历字符串数组，如果第一列的值与数组中的字符串匹配，将第三列设为100
    for s in all_names:
        df.loc[df['姓名'] == s, 'day02'] = 100

    # 保存更改到Excel文件
    df.to_excel('D:/作业打分表.xlsx', index=False)


