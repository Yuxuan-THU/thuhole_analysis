import random
import time
import os
import pyperclip
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def crawl_posts_to_txt(username, password, start_num, end_num, wait_time=5):
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # 目标文件夹路径：爬虫脚本所在目录下的 'data/original_thuhole_texts' 文件夹
    data_dir = os.path.join(script_dir, "data")
    output_dir = os.path.join(data_dir, "original_thuhole_texts")

    # 如果 'data' 文件夹不存在，则自动创建
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"文件夹 'data' 已创建：{data_dir}")

    # 如果 'original_thuhole_texts' 文件夹不存在，则自动创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"文件夹 'original_thuhole_texts' 已创建：{output_dir}")
    else:
        print(f"文件夹 'original_thuhole_texts' 已存在：{output_dir}")

    # 设置 Chrome 配置
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 在无界面模式下运行
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU
    chrome_options.add_argument("--no-sandbox")  # 如果在 Linux 上运行，使用此选项
    chrome_options.add_argument("--remote-debugging-port=9222")  # 启用调试端口

    # 使用 webdriver_manager 自动管理 ChromeDriver
    service = Service(ChromeDriverManager().install())

    # 初始化 WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=9223")  # 使用不同的端口
    driver = webdriver.Chrome(options=options)

    # 打开登录页面
    driver.get("https://api.tholeapis.top/_login/gh")

    # 等待用户名字段加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_field"))
    )

    # 定位到用户名字段并填写
    login_field = driver.find_element(By.ID, "login_field")
    login_field.send_keys(username)

    # 定位到密码字段并填写
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # 提交表单
    password_field.send_keys(Keys.RETURN)

    # 等待几秒钟，确保登录成功
    time.sleep(10)

    current_num = start_num
    while current_num >= end_num:
        print(f"正在爬取帖子 #{current_num}")

        search_box = driver.find_element(By.CLASS_NAME, "control-search")
        search_box.clear()
        search_box.send_keys(f"#{current_num}")
        search_box.send_keys(Keys.RETURN)
        time.sleep(4)

        # 等待页面加载
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        page_source = driver.page_source

        # 如果页面正在加载（例如包含 'loading' 的字符串），则刷新页面并重新搜索
        while "loading" in page_source.lower():
            print(f"帖子 #{current_num} 正在加载，等待 3 秒并刷新页面...")
            driver.refresh()  # 刷新页面
            time.sleep(5)  # 等待页面刷新
            search_box = driver.find_element(By.CLASS_NAME, "control-search")
            search_box.clear()
            search_box.send_keys(f"#{current_num}")
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        # 检查是否有“重新加载评论”按钮
        reload_button = driver.find_elements(By.XPATH, "//*[text()='重新加载评论']")

        if reload_button:
           print("发现“重新加载评论”按钮，正在点击...")
           reload_button[0].click()  # 点击重新加载评论按钮

        # 等待按钮消失，确保页面加载完成
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//*[text()='重新加载评论']"))
        )
        print("“重新加载评论”按钮已消失，继续爬取操作。")

        # 查找链接
        link = soup.find("a", href=f"##{current_num}")
        if not link:
            code_block = soup.find("code", class_="box-id")
            if code_block:
                link = code_block.find("a", href=f"##{current_num}")

        if link:
            try:
                post_link = driver.find_element(By.CSS_SELECTOR, f'a[href="##{current_num}"], code.box-id a[href="##{current_num}"]')
                post_link.click()
            except NoSuchElementException:
                print(f"未找到帖子链接：#{current_num}")
                current_num -= 1
                continue

            time.sleep(wait_time)

            post_content = pyperclip.paste()

            # 将爬取的帖子内容保存到 '爬取文本' 文件夹
            output_file = os.path.join(output_dir, f"{current_num}.txt")
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(post_content)
            print(f"帖子 #{current_num} 的内容已保存到 {output_file}")
        else:
            print(f"未找到帖子链接：#{current_num}")

        current_num -= 1
        time.sleep(random.randint(2, 4))

    # 关闭浏览器
    driver.quit()

if __name__ == "__main__":
    username = input("输入你用户名: ")
    password = input("输入密码: ")
    start_num = int(input("请输入开始爬取的帖子号(注意，开始爬取的帖子号在数值上高于结束的号码): "))
    end_num = int(input("请输入结束爬取的帖子号(注意，开始爬取的帖子号在数值上应当高于结束的号码): "))

    crawl_posts_to_txt(username, password, start_num, end_num)
