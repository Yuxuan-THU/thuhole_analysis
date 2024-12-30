import numpy as np
import joblib
from albert_zh.extract_feature import BertVector
import pandas as pd
import openpyxl
import os
from tqdm import tqdm  # 引入 tqdm 用于进度条显示

# 获取当前脚本所在的目录
current_dir = os.path.dirname(__file__)
print(f"当前工作目录: {current_dir}")

# 加载 Bert 模型（根据你的需求设置参数）
bert_model = BertVector(pooling_strategy="REDUCE_MEAN", max_seq_len=200)

# 定义文本转换函数 f
f = lambda text: bert_model.encode([text])["encodes"][0]

# 加载训练好的模型
svc = joblib.load(os.path.join(current_dir, 'models', 'SVM.model'))

# 获取 Excel 文件的路径
input_excel_path = os.path.join(current_dir, 'data_posts', 'original_extracted_texts_example.xlsx')
print(f"读取的 Excel 文件路径: {input_excel_path}")

# 读取 Excel 文件
df = pd.read_excel(input_excel_path, engine='openpyxl')

# 第一步：在 "main_post" 这一列左侧插入两个空白列，分别命名为“code”和“full_texts”
df.insert(df.columns.get_loc("main_post"), "code", "")  # 插入空白列 "code"
df.insert(df.columns.get_loc("main_post"), "full_texts", "")  # 插入空白列 "full_texts"

# 第二步：通过 NumPy 加速文本合并
full_texts = []
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="合并文本", ncols=100):
    # 获取 'main_post' 列及右边所有列的文本内容，使用向量化方式
    text_parts = row["main_post":].dropna().astype(str).values
    combined_text = " ".join(text_parts)
    full_texts.append(combined_text)
    
    # 每处理100行输出一次进度
    if (index + 1) % 100 == 0:
        print(f"已处理 {index + 1} 行...")

# 将合并后的文本赋值到 'full_texts' 列
df['full_texts'] = full_texts

# 第三步：过滤掉 'full_texts' 列中为 NaN 或空的行
df = df[df['full_texts'].notna() & (df['full_texts'] != '')]

# 输出进度
print(f"已处理 {df.shape[0]} 行数据")

# 第四步：对 full_texts 列进行预测
def predict_text(text):
    if text is None:
        text = ""  # 替换 None 为一个空字符串
    vec = np.array([f(text)])  # 这里 f 是用于文本向量化的函数
    y_predict = svc.predict(vec)
    return y_predict[0]  # 只取预测的类别

# 对 'full_texts' 列进行预测
predictions = [predict_text(text) for text in tqdm(df["full_texts"], desc="预测文本分类", ncols=100)]

# 将预测结果写入 'full_texts' 左侧的 'code' 列
df['code'] = predictions

# 输出为新的 Excel 文件
output_excel_path = os.path.join(current_dir, 'data_texts', "编码结果_with_predictions.xlsx")
df.to_excel(output_excel_path, index=False)

print(f"修改后的 Excel 文件已输出: {output_excel_path}")
