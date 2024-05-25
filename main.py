import os
import re
import pandas as pd

def filter_chinese_only(text):
    # 正则表达式匹配非中文字符并替换为空
    cleaned_text = re.sub(r'[^0-9\u4e00-\u9fff]', '', text)
    return cleaned_text


def count_java_comments(file_path):
    if not file_path.endswith('.java'):
        return 0

    with open(file_path, 'r', encoding='utf-8') as file:
        single_line_comments = 0
        multi_line_comment_start = False
        for line in file:
            # 处理单行注释
            if re.match(r'^\s*//.*$', line):
                single_line_comments += 1
            # 处理多行注释
            if re.match(r'/\*', line):
                multi_line_comment_start = True
            elif re.match(r'\*/', line):
                multi_line_comment_start = False
            elif multi_line_comment_start:
                single_line_comments += 1  # 在多行注释内计为一行

        return single_line_comments

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

    dir = 'C:/Users/xiadong/Desktop/实训作业/'

    # 获取目录下所有子目录
    subfolders = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]

    # 读取Excel文件
    df = pd.read_excel('D:/作业打分表.xlsx')

    # 遍历并打印每个子目录
    for folder in subfolders:
        all_names = collect_homework_data(dir + folder)

        # 遍历字符串数组，如果第一列的值与数组中的字符串匹配，将第三列设为100
        for s in all_names:
            df.loc[df['姓名'] == s, folder] = 100

    # 保存更改到Excel文件
    df.to_excel('D:/作业打分表3.xlsx', index=False)

