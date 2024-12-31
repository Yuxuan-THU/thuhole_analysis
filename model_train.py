import os
import numpy as np
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import joblib
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from albert_zh.extract_feature import BertVector
import pandas as pd

# 读取文本文件并转换为 DataFrame
def read_txt_file(file_path):
    texts, labels = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')  # 假设是tab分隔的文本和标签
            if len(parts) == 2:
                labels.append(parts[0])
                texts.append(parts[1])
    return pd.DataFrame({'text': texts, 'label': labels})

# 读取数据
def load_data(train_file_path, test_file_path):
    train_df = read_txt_file(train_file_path)
    test_df = read_txt_file(test_file_path)
    return train_df, test_df

# 进行文本编码
def encode_texts(train_df, test_df, bert_model):
    f = lambda text: bert_model.encode([text])["encodes"][0]
    train_df['x'] = train_df['text'].apply(f)
    test_df['x'] = test_df['text'].apply(f)
    return np.array([vec for vec in train_df['x']]), np.array([vec for vec in test_df['x']]), np.array([vec for vec in train_df['label']]), np.array([vec for vec in test_df['label']])

# 模型训练与评估
def train_and_evaluate(x_train, x_test, y_train, y_test):
    # 获取当前工作目录路径
    current_dir = os.path.dirname(__file__)
    
    # 设置模型保存路径
    output_dir = os.path.join(current_dir, 'models')
    
    # 如果模型文件夹不存在，则创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Logistic Regression
    lr = LR(random_state=123)
    lr.fit(x_train, y_train)
    y_pred = lr.predict(x_test)
    print("Logistic Regression Model")
    print("混淆矩阵", confusion_matrix(y_true=y_test, y_pred=y_pred))
    print("正确率：", accuracy_score(y_test, y_pred))
    print(classification_report(y_true=y_test, y_pred=y_pred, digits=4))

    # 保存模型
    joblib.dump(lr, os.path.join(output_dir, "LR.model"))

    # Naive Bayes Model
    gnb = GaussianNB()
    gnb.fit(x_train, y_train)
    y_pred = gnb.predict(x_test)
    print("\nNaive Bayes Model")
    print("混淆矩阵", confusion_matrix(y_true=y_test, y_pred=y_pred))
    print("正确率：", accuracy_score(y_test, y_pred))
    print(classification_report(y_true=y_test, y_pred=y_pred, digits=4))

    # 保存模型
    joblib.dump(gnb, os.path.join(output_dir, "NB.model"))

    # SVM model
    svc = SVC(kernel="rbf")
    svc.fit(x_train, y_train)
    y_pred = svc.predict(x_test)
    print("\nSVM Model")
    print("混淆矩阵", confusion_matrix(y_true=y_test, y_pred=y_pred))
    print("正确率：", accuracy_score(y_test, y_pred))
    print(classification_report(y_true=y_test, y_pred=y_pred, digits=4))

    # 获取SVM模型的预测结果
    print("\nSVM模型的预测结果：")
    for idx in range(len(y_test)):
        print(f"索引 {idx}, 真实标签: {y_test[idx]}, 预测标签: {y_pred[idx]}")

    # 保存SVM模型
    joblib.dump(svc, os.path.join(output_dir, "SVM.model"))

# 主函数
def main():
    # 获取当前文件夹路径
    current_dir = os.path.dirname(__file__)
    print(f"当前工作目录: {current_dir}")

    # 输入文件夹的相对路径
    train_file_path = os.path.join(current_dir, 'data_labeled_for_ml', 'train.txt')
    test_file_path = os.path.join(current_dir, 'data_labeled_for_ml', 'test.txt')

    # 输出模型的路径 (根目录下的 models 文件夹)
    output_dir = os.path.join(current_dir, 'models')
    # 如果模型文件夹不存在，则创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 加载BERT模型
    bert_model = BertVector(pooling_strategy="REDUCE_MEAN", max_seq_len=200)

    # 加载数据
    train_df, test_df = load_data(train_file_path, test_file_path)

    # 编码文本
    x_train, x_test, y_train, y_test = encode_texts(train_df, test_df, bert_model)

    # 训练并评估模型
    train_and_evaluate(x_train, x_test, y_train, y_test)

if __name__ == '__main__':
    main()
