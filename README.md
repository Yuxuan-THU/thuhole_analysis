# thuhole_analysis

## :hugs: Brief Introduction

This project is dedicated to two purposes:

* Scraping text content from Tsinghua University's anonymous social platform "New T Treehole" using Python.
* Classifying and analyzing the text using machine learning.

## :boom: Re-Implementation

### Step 1: Clone this Repository and Install Related Python Libraries

Clone this Repository

```bash
git clone https://github.com/Yuxuan-THU/thuhole_analysis.git
```

Install Related Python Libraries for Web Scraping Scrip

```bash
pip install -r requirements_spider.txt
```

**Note:** To successfully install Python packages, you may need to disable the network proxy.

### Step 2: Data collection: Retrieve Post Text

**Command:**

```bash
python data_collect.py
```

**Input:**  

* Username
* Password
* Starting Post ID
* Ending Post ID

**Note:** You need to link your Tsinghua email (student email, staff email, or alumni email) to your GitHub account, and then log in to the website [https://new-t.github.io/](https://new-t.github.io/?) via GitHub. The username you enter is the linked email, and the password is your GitHub password. Since we are retrieving posts from the present to the past along a timeline, the starting post number must be **greater** than the ending post number.

**Output:** 

data_posts/original_thuhole_texts

**Note:** In the data_posts/original_thuhole_texts/ folder, you will find multiple text files named in the format ××××××.txt, containing raw data from the specified start to end post IDs.

### Step 3: Data Structure: Write the Post Content to the Excel File

**Command:**

```bash
python data_structure.py
```

**Input:**  

data_posts/original_thuhole_texts

if you wish to use sample data：

data_posts/original_thuhole_texts_example.xlsx

**Output:** 

data_posts/original_extracted_texts.xlsx

### Step 4: Data Mining: Train the Models

**Command:**

Strong Recommendation: Create a Virtual Environment First.

```bash
conda create --name thuhole_analysis python=3.6
conda activate thuhole_analysis
```

Set up a GPU environment

```bash
pip install --ignore-installed --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple tensorflow-gpu==1.14.0
conda install -c anaconda cudatoolkit=10.1.243 cudnn=7.6.5
conda install cudatoolkit=10.0
```

Install Related Python Libraries for machine learning

```bash
pip install -r requirements_ml.txt
pip install --upgrade pandas openpyxl
```

Train the models

```bash
python model_train.py
```

**Input:**  

* data_labeled_for_ml/train.txt
* data_labeled_for_ml/test.txt

**Output:**  

* tmp_graph11
* models/LR.model
* models/NB.model
* models/SVM.model

### Step 4: Data Mining: Make Predictions with SVM Model

**Command:**

```bash
python model_predict.py
```

**Input:**  

* models/SVM.model
* data_posts/original_extracted_texts_example.xlsx

**Output:**  

* coded_original_extracted_texts.xlsx

**Note:** The script will take approximately 6 minutes to run.

