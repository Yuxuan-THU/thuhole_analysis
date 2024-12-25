# thuhole_analysis

## :hugs: Brief Introduction

This project is dedicated to two purposes:：

* Scraping text content from Tsinghua University's anonymous social platform "New T Treehole" using Python.
* Classifying and analyzing the text using machine learning.

## :boom: Re-Implementation

### Step 1: Install Python and Related Python Libraries

1. Install Python 
2. Install Related Python Libraries

    ```bash
    pip install -r requirements_spider.txt
    ```

### Step 2: Retrieve Post Text

**Input:**  

* Username
* Password
* Starting Post ID
* Ending Post ID

**Output:** data/original_thuhole_texts

**Command:**

```bash
python spider_thuhole.py
```

**Note:** You need to link your Tsinghua email (student email, staff email, or alumni email) to your GitHub account, and then log in to the website [https://new-t.github.io/](https://new-t.github.io/?) via GitHub. The username you enter is the linked email, and the password is your GitHub password. Since we are retrieving posts from the present to the past along a timeline, the starting post number must be **greater** than the ending post number.
