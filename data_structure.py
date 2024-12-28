import re
import pandas as pd
import os

# 提取帖子编号
def extract_id(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()  # 读取并去掉第一行的空白字符

    # 使用正则表达式匹配两个#后面紧接着的数字
    pattern = r'##(\d+)'  # 匹配两个#后紧接着的数字
    numbers = re.findall(pattern, first_line)  # 只在第一行进行匹配

    return numbers


# 提取原帖内容
def extract_main_post(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 从第二行开始提取内容
    extracted_text = []
    for line in lines[1:]:  # 从第二行开始（索引1）
        if line.startswith('（'):  # 如果行首出现“（”，则停止
            break
        extracted_text.append(line.strip())  # 去除行尾的空白字符并保存

    # 返回提取的内容作为一个字符串，删除所有空格
    return "".join(extracted_text).replace(" ", "")  # 使用 replace 去掉空格


# 提取日期信息
def extract_date(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 遍历每一行，查找第一次出现“(”的行
    for line_num, line in enumerate(lines, start=1):
        if line.startswith('（'):  # 检查行首是否有"("
            # 使用正则表达式提取日期信息，日期格式为"10-28"
            date_pattern = r'(\d{1,2}-\d{1,2})'  # 匹配日期格式 10-28
            date_match = re.search(date_pattern, line)  # 在当前行中查找匹配的日期

            if date_match:
                # 如果找到日期，返回行号和日期信息
                return date_match.group(1)

    # 如果没有找到符合条件的行，返回 None
    return None


# 提取时刻信息
def extract_clock(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 遍历每一行，查找第一次出现“（”的行
    for line_num, line in enumerate(lines, start=1):
        if line.startswith('（'):  # 检查行首是否有"("
            # 使用正则表达式提取时刻信息，支持小时、分钟、秒钟一位或两位数
            time_pattern = r'(\d{1,2}:\d{1,2}:\d{1,2})'  # 匹配时刻格式 9:58:46 或 22:17:00
            time_match = re.search(time_pattern, line)  # 在当前行中查找匹配的时刻

            if time_match:
                # 如果找到时刻，返回行号和时刻信息
                return time_match.group(1)

    # 如果没有找到符合条件的行，返回 None
    return None


#提取关注量信息
def extract_attention(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 遍历每一行，查找第一次出现“(”的行
    for line_num, line in enumerate(lines, start=1):
        if line.startswith('（'):  # 检查行首是否有"("
            # 使用正则表达式提取“关注”之前的数字
            # (\d+) 匹配任意长度的数字，直到“关注”前
            pattern = r'(\d+)(?=\s*关注)'  # 这个模式匹配“关注”前的数字
            match = re.search(pattern, line)  # 在当前行中查找匹配的数字

            if match:
                # 如果找到数字，返回行号和数字
                return match.group(1)

    # 如果没有找到符合条件的行，返回 None
    return None


#提取回复量信息
def extract_reply(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 遍历每一行，查找第一次出现“(”的行
    for line_num, line in enumerate(lines, start=1):
        if line.startswith('（'):  # 检查行首是否有"("
            # 使用正则表达式提取“关注”之前的数字
            # (\d+) 匹配任意长度的数字，直到“关注”前
            pattern = r'(\d+)(?=\s*回复)'  # 这个模式匹配“关注”前的数字
            match = re.search(pattern, line)  # 在当前行中查找匹配的数字

            if match:
                # 如果找到数字，返回行号和数字
                return match.group(1)

    # 如果没有找到符合条件的行，返回 None
    return None


#提取回帖人名字
def extract_names(file_path):
    # 正则表达式：匹配【】之间的所有文本
    pattern = re.compile(r'【([^】]+)】')
    
    result = []  # 用于保存符合条件的行
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 从第二行开始，遍历每一行
    for i, line in enumerate(lines[1:], 2):  # 从第二行开始遍历，索引从2开始
        match = pattern.search(line)  # 在当前行中查找符合条件的文本
        if match:  # 如果匹配到并且【】之间有文本
            content = match.group(1)
            if any(char.isalpha() for char in content):  # 判断是否包含中文或英文字符
                result.append(line.strip())  # 将符合条件的行添加到结果列表中
    
    return result  # 返回符合条件的行列表


#提取每个回帖内容
def extract_lines_with_text_in_brackets(file_path):
    # 正则表达式：匹配【】之间的所有文本
    pattern = re.compile(r'【([^】]+)】')
    
    # 用于保存包含【】文本的行号
    line_numbers = []  
    result = []  # 用于保存段落的内容
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 遍历每一行
    for i, line in enumerate(lines[1:], 2):
        match = pattern.search(line)  # 在当前行中查找符合条件的文本
        if match:  # 如果匹配到并且【】之间有文本
            line_numbers.append(i)  # 记录该行的行号
    
    # 根据行号分段提取内容
    segments = []
    for i in range(1, len(line_numbers)):
        start_line = line_numbers[i-1] + 1  # 当前段的开始行
        end_line = line_numbers[i] - 1  # 当前段的结束行
        
        # 如果start_line <= end_line，则提取该段内容
        if start_line <= end_line:
            segments.append(lines[start_line-1:end_line])  # 保存该段内容
    
    # 提取从最后一个行号到文件末尾的内容
    if line_numbers:
        last_segment = lines[line_numbers[-1]:]  # 从最后一个行号到文件末尾
        segments.append(last_segment)
    
    # 将所有段落内容拼接成一个列表返回
    for segment in segments:
        result.append("".join(segment).strip())  # 将每个段落合并成一个字符串并去除空格
    
    return result



# 循环提取保存到excel文件
def extract_and_save_to_excel(folder_path, output_excel):
    data_list = []  # 存储所有提取的数据

    # 获取文件夹中所有文件的列表，并提取最小和最大编号
    all_files = os.listdir(folder_path)
    # 筛选出.txt文件并提取编号
    file_ids = [int(file.split('.')[0]) for file in all_files if file.endswith('.txt')]
    
    if not file_ids:
        print("没有找到有效的文件。")
        return

    start_id = min(file_ids)
    end_id = max(file_ids)

    print(f"开始编号: {start_id}, 结束编号: {end_id}")

    # 循环遍历指定编号范围内的文件
    for i in range(start_id, end_id + 1):
        file_name = f"{i}.txt"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):  # 确保文件存在
            # 提取信息
            id = extract_id(file_path)
            date = extract_date(file_path)
            clock = extract_clock(file_path)
            attention = extract_attention(file_path)
            reply = extract_reply(file_path)
            content = extract_main_post(file_path)
            names = extract_names(file_path)
            post = extract_lines_with_text_in_brackets(file_path)

            num_posts = len(post)

            # 创建数据字典
            data = {
                "id": id,
                "date": date,
                "clock": clock,
                "attention_num": attention,
                "reply_num": reply,
                "reply_id": ", ".join(names),
                "main_post": content
            }

            # 添加段落内容到数据字典
            for j, segment in enumerate(post):
                data[f"reply_post_{j+1}"] = segment  # 每个段落放到一个新列

            # 将数据添加到数据列表
            data_list.append(data)

    # 将所有数据写入DataFrame
    post_df = pd.DataFrame(data_list)

    # 将DataFrame保存为Excel文件
    post_df.to_excel(output_excel, index=False, engine='openpyxl')

    print(f"结构化的文本数据已成功保存到 {output_excel}")

##################################################
# 主函数
##################################################

# 当前文件夹路径
current_dir = os.path.dirname(__file__)

# 输入文件夹的相对路径
folder_path = os.path.join(current_dir, 'data', 'original_thuhole_texts')

# 输出的Excel文件路径
output_excel = os.path.join(current_dir, 'data', 'original_extracted_texts.xlsx')

# 调用函数
extract_and_save_to_excel(folder_path, output_excel)