import tkinter as tk
from io import BytesIO
from tkinter import messagebox
import random
import cv2
import numpy as np
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def preprocess_image(img_path):
    """
    对验证码图片进行预处理
    """
    # 读取图片
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # 转为灰度图

    # 二值化处理
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # 去噪（可选）
    denoised_image = cv2.medianBlur(binary_image, 3)

    # 返回预处理后的图片
    return denoised_image

# PaddleOCR初始化
def OCR(img_name, language):
    ocr = PaddleOCR(use_angle_cls=True, lang=language)  # 使用中文、英文模型
    img_path = img_name
    result = ocr.ocr(img_path, cls=True)

    problem_content = ""
    boxes = []
    txts = []
    scores = []
    question_boxes = []
    isQuestion = False

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text = line[1][0]  # 识别到的文本
            confidence = line[1][1]  # 置信度
            box = line[0]  # 文本区域框

            boxes.append(box)
            txts.append(text)
            scores.append(confidence)

            flag = is_question(text)
            print(text)
            if flag:
                if (problem_content.find("单选题") != -1
                        or problem_content.find("多选题") != -1
                        or problem_content.find("判断题") != -1):
                    if (problem_content.find("单选题") != -1 or problem_content.find("多选题") != -1) and (
                            problem_content.find("A") != -1 and problem_content.find(
                        "B") != -1 and problem_content.find("D") != -1):
                        with open('problem_content.txt', 'a+', encoding='utf-8') as f:
                            current_content = f.read()
                            if current_content.find(problem_content) == -1:
                                f.write(problem_content + "\n----------------------")

                    elif problem_content.find("判断题") != -1:
                        with open('problem_content.txt', 'a+', encoding='utf-8') as f:
                            current_content = f.read()
                            if current_content.find(problem_content) == -1:
                                f.write(problem_content + "\n----------------------")
                print(problem_content)
                problem_content = text + "\n"
            else:
                problem_content += text + "\n"

        if (problem_content.find("单选题") != -1
                or problem_content.find("多选题") != -1
                or problem_content.find("判断题") != -1):
            if (problem_content.find("单选题") != -1 or problem_content.find("多选题") != -1) and (
                    problem_content.find("A") != -1 and problem_content.find(
                "B") != -1 and problem_content.find("D") != -1):
                with open('problem_content.txt', 'a+', encoding='utf-8') as f:
                    current_content = f.read()
                    if current_content.find(problem_content) == -1:
                        f.write(problem_content + "\n----------------------")

            elif problem_content.find("判断题") != -1:
                with open('problem_content.txt', 'a+', encoding='utf-8') as f:
                    current_content = f.read()
                    if current_content.find(problem_content) == -1:
                        f.write(problem_content + "\n----------------------")

    image = Image.open(img_path).convert('RGB')
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show_cv = np.array(im_show)
    im_show_cv = cv2.cvtColor(im_show_cv, cv2.COLOR_RGB2BGR)

    for box in question_boxes:
        box = np.array(box).astype(int)
        cv2.polylines(im_show_cv, [box], isClosed=True, color=(0, 0, 255), thickness=2)

    cv2.imwrite('result.jpg', im_show_cv)
    print("可视化结果已保存为 result.jpg")

    return problem_content


def is_question(text):
    keywords = ["单选题", "多选题", "判断题"]
    if any(keyword in text for keyword in keywords):
        return True
    return False


def DeepSeekAsk(prompt, temperature):
    api_key = "sk-ecee03845a1b42938fb66bae42694268"
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        stream=False
    )
    return response.choices[0].message.content


def initialize_webdriver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 启用无头模式
    options.add_argument("--disable-css")  # 禁用css
    options.add_argument("--disable-images")  # 图片不加载
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service("./chromedriver_win32/chromedriver.exe"), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    return driver


def crop_screenshot(pic_name, crop_area):
    image = Image.open(pic_name)
    cropped_image = image.crop(crop_area)
    cropped_image.save(pic_name)
    print(f"裁剪后的图片已保存到: crop_{pic_name}")


def get_image(pic_name, driver):
    width = driver.execute_script("return document.documentElement.scrollWidth")
    total_height = driver.execute_script("return document.documentElement.scrollHeight")
    print(width, total_height)
    driver.set_window_size(width, total_height)

    scroll_height = 0
    problem_content_all = ""

    while scroll_height < total_height:
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(0.1)
        driver.save_screenshot(pic_name)
        print(f"截图已保存: {pic_name}")

        crop_area = (240, 550, width + 300, total_height - 100)
        crop_screenshot(pic_name, crop_area)
        problem_content = OCR(pic_name, "ch")
        scroll_height += 300

    with open("./problem_content.txt", mode="r", encoding='utf-8') as f:
        prompt = '''请根据以下题目要求回答问题：

        所有题目的答案必须从选项 A、B、C、D 中选择。

        对于判断题，答案只能是 A 或 B，分别对应题目中的 A（对） 和 B（错）。

        如果题目重复出现，只需回答一次，不要重复回答。

        请严格按照题目编号顺序给出答案。

        最终你给出的答案格式应当类似于下面这样：C,A,A
        \n'''
        prompt += f.read()
        temperature = random.choice([0.8, 0.9, 1.0])
        answer = DeepSeekAsk(prompt, temperature)
        answer_list = answer.split(",")
        index = 0

        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "singleQuesId"))
        )

        questions = driver.find_elements(By.CLASS_NAME, "singleQuesId")

        for question in questions:
            try:
                question_options = question.find_element(By.CLASS_NAME, "Zy_ulTop")
            except Exception as e:
                print(f"未找到当前题目的选项容器: {e}")
                continue

            options = question_options.find_elements(By.CLASS_NAME, "font-cxsecret")
            correct_answer = answer_list[index]
            index += 1

            for option in options:
                option_value = option.find_element(By.CSS_SELECTOR, "span.num_option").text.strip()
                if option_value == correct_answer:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                    option.click()
                    print(f"已点击选项: {option_value}")
                    break


def login(driver, url, phone, pwd):
    driver.get(url)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-big-blue.margin-btm24")))

    username_field = driver.find_element(By.ID, "phone")
    password_field = driver.find_element(By.ID, "pwd")
    username_field.send_keys(phone)
    password_field.send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, ".btn-big-blue.margin-btm24").click()
    WebDriverWait(driver, 15).until(EC.url_changes("https://passport2.chaoxing.com/login"))


def time_to_seconds(time_str):
    parts = time_str.split(":")
    parts = [int(part) for part in parts]

    if len(parts) == 2:
        minutes, seconds = parts
        hours = 0
    elif len(parts) == 3:
        hours, minutes, seconds = parts
    else:
        raise ValueError("时间格式不正确，应为 '分:秒' 或 '时:分:秒'")

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def save_image_from_url(driver, image_url, save_path):
    """
        从URL下载图片并保存到本地
        :param image_url: 图片的URL地址
        :param save_path: 图片保存的本地路径（包括文件名和扩展名，如：'./image.jpg'）
        """
    try:
        # 发送HTTP GET请求获取图片内容
        cookies = driver.get_cookies()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0.0.0 Mobile Safari/537.36',
            'Cookie':  "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        }
        response = requests.get(image_url,headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 将图片内容转换为PIL图像对象
        image = Image.open(BytesIO(response.content))

        # 保存图片到本地
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(save_path)
        print(f"图片已保存到: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"下载图片失败: {e}")
    except Exception as e:
        print(f"保存图片失败: {e}")


def start(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )
    video = driver.find_elements(By.TAG_NAME, "video")
    actions = ActionChains(driver)
    actions.move_to_element(video[0]).click().perform()
    print("已尝试点击视频元素以开始播放。")

    disable_pause_script = """
        var video = document.querySelector('video');
        if (video) {
            video.addEventListener('pause', function(event) {
                video.play();
            });
        }
        """
    driver.execute_script(disable_pause_script)
    times = ""
    # 注意，容易出现突发情况，就是学习通要求验证码验证逻辑
    while True:
        video_progress = driver.find_elements(By.CLASS_NAME, "vjs-progress-holder")
        if video_progress:
            times = video_progress[0].get_attribute("aria-valuetext")
            if times.find("-") == -1:
                break
        else:
            # 验证码输入逻辑
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ccc"))
            )
            img_url = driver.find_element(By.ID, "ccc").get_attribute("src")
            # 1.保存图片
            save_path = "./downloaded_image.jpg"  # 替换为你想保存的本地路径
            save_image_from_url(driver, img_url, save_path)
            preprocess_image(save_path)
            time.sleep(2)

            # 2.开始识别图片中的字母
            confirm_content = (OCR(save_path, 'en')
                               .replace('"', '\\"')
                               .replace("'", "\\'")
                               .replace("\n", "\\n")) # 转义特殊字符

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "yzmInp"))
            )

            confirm_input = driver.find_element(By.CLASS_NAME, "yzmInp")
            driver.execute_script(f'document.getElementsByClassName("yzmInp")[0].value = "{confirm_content}";')

            time.sleep(1000)
    print(times)
    current_time, total_time = times.split(" of ")
    current_time = time_to_seconds(current_time)
    total_time = time_to_seconds(total_time)
    if total_time - current_time <= 10:
        return True
    return False


def start_thread(driver):
    while True:
        if not start(driver):
            print(1)
        else:
            driver.switch_to.default_content()
            break


# GUI部分
def create_gui():
    def on_login():
        account = entry_account.get()
        password = entry_password.get()
        course_name = entry_course.get()

        if not account or not password or not course_name:
            messagebox.showwarning("输入错误", "请填写所有字段！")
        else:
            messagebox.showinfo("登录成功", f"账号: {account}\n密码: {password}\n课程名称: {course_name}")
            # 关闭GUI窗口
            root.destroy()
            # 调用主逻辑
            start_main_logic(account, password, course_name)

    # 创建主窗口
    root = tk.Tk()
    root.title("课程登录系统")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg="#f0f0f0")

    # 创建标题标签
    label_title = tk.Label(root, text="超星刷课脚本", font=("Arial", 20), bg="#f0f0f0", fg="#333333")
    label_title.pack(pady=20)

    # 创建账号输入框
    frame_account = tk.Frame(root, bg="#f0f0f0")
    frame_account.pack(pady=10)
    label_account = tk.Label(frame_account, text="账号:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
    label_account.pack(side=tk.LEFT, padx=5)
    entry_account = tk.Entry(frame_account, font=("Arial", 12), width=20)
    entry_account.pack(side=tk.LEFT)

    # 创建密码输入框
    frame_password = tk.Frame(root, bg="#f0f0f0")
    frame_password.pack(pady=10)
    label_password = tk.Label(frame_password, text="密码:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
    label_password.pack(side=tk.LEFT, padx=5)
    entry_password = tk.Entry(frame_password, font=("Arial", 12), width=20, show="*")
    entry_password.pack(side=tk.LEFT)

    # 创建课程名称输入框
    frame_course = tk.Frame(root, bg="#f0f0f0")
    frame_course.pack(pady=10)
    label_course = tk.Label(frame_course, text="课程名称:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
    label_course.pack(side=tk.LEFT, padx=5)
    entry_course = tk.Entry(frame_course, font=("Arial", 12), width=20)
    entry_course.pack(side=tk.LEFT)

    # 创建登录按钮
    button_login = tk.Button(root, text="登录", font=("Arial", 14), bg="#4CAF50", fg="white", command=on_login)
    button_login.pack(pady=20)

    # 运行主循环
    root.mainloop()


# 主逻辑函数
def start_main_logic(account, password, course_name):
    driver = initialize_webdriver()
    url = "https://passport2.chaoxing.com/login"
    login(driver, url, account, password)

    # 登录完成之后进入指定的课程
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".course"))
    )

    # 提取所有课程
    course_elements = driver.find_elements(By.CSS_SELECTOR, ".course")
    for course_element in course_elements:
        # 提取课程名称
        course_name_element = course_element.find_element(By.CSS_SELECTOR, ".course-name")
        target_course_name = course_name_element.text

        # 提取 <a> 标签的 href 属性
        link_element = course_element.find_element(By.CSS_SELECTOR, ".course-cover a")
        course_url = link_element.get_attribute("href")

        print(f"当前课程名称: {course_name}")
        print(f"课程链接: {course_url}")

        # 检查是否匹配指定课程名称
        if course_name == target_course_name:
            print(f"找到目标课程: {course_name}，跳转到课程链接: {course_url}")
            driver.get(course_url)  # 跳转到目标课程链接
            break  # 如果只需要跳转第一个匹配的课程，可以使用 break
    time.sleep(3)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="章节"]'))
    )
    chapter_title = driver.find_element(By.CSS_SELECTOR, 'a[title="章节"]')
    chapter_title.click()

    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "catalog_sbar")))
    catalog_0 = driver.find_elements(By.CLASS_NAME, "catalog_sbar")[0]
    catalog_0.click()

    print(driver.page_source)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "posCatalog_level"))
    )

    pos_catalog_levels = driver.find_elements(By.CLASS_NAME, "posCatalog_level")

    for level in pos_catalog_levels:
        try:
            WebDriverWait(level, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul li"))
            )
        except Exception as e:
            print(f"level 下的 li 元素加载失败: {e}")
            continue

        list_items = level.find_elements(By.CSS_SELECTOR, "ul li")

        for li in list_items:
            try:
                button = WebDriverWait(li, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.posCatalog_select, span.posCatalog_name"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                ActionChains(driver).move_to_element(button).click().perform()
                print(f"Clicked: {button.text}")
            except Exception as e:
                print(f"Could not click element: {e}")


    # 看视频
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ans-attach-online"))
    )
    driver.switch_to.frame(iframe)
    print(driver.page_source)
    start_thread(driver)
    chapter_test = driver.find_elements(By.CSS_SELECTOR, "li[title='章节测验']")
    if chapter_test != []:
        chapter_test[0].click()
        pic_name = r'./chaoxing.png'
        get_image(pic_name, driver)
    chapter_test = driver.find_elements(By.CSS_SELECTOR, "li[title='测验']")
    if chapter_test != []:
        pic_name = r'./chaoxing.png'
        get_image(pic_name, driver)
        chapter_test[0].click()

    time.sleep(1000)

# 程序入口
if __name__ == '__main__':
    # 启动GUI
    create_gui()
