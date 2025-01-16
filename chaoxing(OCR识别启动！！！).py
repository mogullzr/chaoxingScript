import random

import cv2
import numpy as np
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


# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
def OCR(img_name):
    # 初始化PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # 使用中文模型

    # 读取图片
    img_path = img_name
    result = ocr.ocr(img_path, cls=True)

    # 提取识别结果
    problem_content = ""
    boxes = []
    txts = []
    scores = []
    question_boxes = []  # 存储可能是题目的区域
    isQuestion = False

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text = line[1][0]  # 识别到的文本
            confidence = line[1][1]  # 置信度
            box = line[0]  # 文本区域框

            # 将结果添加到列表中
            boxes.append(box)
            txts.append(text)
            scores.append(confidence)

            flag = is_question(text)
            print(text)
            # 判断是否是题目区域（根据关键词或位置）
            if flag:
                # 1.保存内容，这种情况不会存在确实的情况
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
                problem_content += text + "\n"  # 将题目内容拼接
        # 此时我们得判断一下这个题目内容是否存在确实情况，若存在缺失，则直接 pass
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

    # 可视化结果
    image = Image.open(img_path).convert('RGB')
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')

    # 将PIL图像转换为OpenCV格式98
    im_show_cv = np.array(im_show)
    im_show_cv = cv2.cvtColor(im_show_cv, cv2.COLOR_RGB2BGR)

    # 标注题目区域（用红色框标注）
    for box in question_boxes:
        # 将box坐标转换为整数
        box = np.array(box).astype(int)
        # 绘制红色框
        cv2.polylines(im_show_cv, [box], isClosed=True, color=(0, 0, 255), thickness=2)

    # 保存可视化结果
    cv2.imwrite('result.jpg', im_show_cv)
    print("可视化结果已保存为 result.jpg")

    return problem_content

def is_question(text):
    """
    判断是否是题目区域的逻辑
    """
    # 关键词匹配
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
    """
    对截图进行裁剪
    :param pic_name: 截图路径
    :param crop_area: 裁剪区域 (left, top, right, bottom)
    """
    # 打开截图
    image = Image.open(pic_name)

    # 裁剪图片
    cropped_image = image.crop(crop_area)

    # 保存裁剪后的图片
    cropped_image.save(pic_name)
    print(f"裁剪后的图片已保存到: crop_{pic_name}")

def get_image(pic_name, driver):
    # 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    total_height = driver.execute_script("return document.documentElement.scrollHeight")
    print(width, total_height)
    # 将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, total_height)

    # 初始化变量
    scroll_height = 0  # 当前滚动高度
    problem_content_all = ""  # 存储所有识别到的题目内容

    while scroll_height < total_height:
        # 滚动页面
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(0.5)  # 等待页面滚动完成

        # 截取当前屏幕
        driver.save_screenshot(pic_name)
        print(f"截图已保存: {pic_name}")

        # 裁剪指定区域
        crop_area = (240, 550, width + 300, total_height - 100)
        # crop_area = (240, 0, width, min(800, total_height - scroll_height))  # 裁剪区域 (left, top, right, bottom)
        crop_screenshot(pic_name, crop_area)

        # 对裁剪后的图片进行 OCR 识别
        problem_content = OCR(pic_name)

        # problem_content_all += problem_content + "\n"  # 将识别内容追加到总结果中

        # 更新滚动高度
        scroll_height += 200
    # 截取全屏截图
    # driver.save_screenshot(pic_name)
    # 裁剪指定区域
    # crop_area = (240, 800, width + 300, total_height - 100)  # 裁剪区域 (left, top, right, bottom)
    # crop_screenshot(pic_name, crop_area)

    # 获取到识别的题目
    # problem_content = OCR(pic_name)

    # 然后开始AI问答环节了嘻嘻
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

        # 等待题目元素加载完成
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

        # 找到所有题目的容器
        questions = driver.find_elements(By.CLASS_NAME, "singleQuesId")

        # 遍历每个题目
        for question in questions:
            # 找到当前题目的选项容器
            try:
                question_options = question.find_element(By.CLASS_NAME, "Zy_ulTop")
            except Exception as e:
                print(f"未找到当前题目的选项容器: {e}")
                continue

            # 找到当前题目的所有选项
            options = question_options.find_elements(By.CLASS_NAME, "font-cxsecret")

            # 假设正确答案是 （根据实际情况调整）
            correct_answer = answer_list[index]
            index += 1

            # 遍历选项，找到正确答案并点击
            for option in options:
                # 获取选项的 data 属性值（A、B、C、D）
                option_value = option.find_element(By.CSS_SELECTOR, "span.num_option").text.strip()

                # 如果选项的值与正确答案匹配，则点击
                if option_value == correct_answer:
                    # 使用 JavaScript 将选项滚动到视口中
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)

                    # 点击选项
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

# 你输入的参数
if __name__ == '__main__':
    driver = initialize_webdriver()
    # 1.登录
    url = "https://passport2.chaoxing.com/login"
    login(driver, url, "14796733539", "jiaming456..")

    # 2.进入指定的课程并开始刷题
    # 2.1.进入指定课程
    driver.get(
        "https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?courseid=246182440&clazzid=105994963&cpi=429125567&enc=d38fec312d20ff6d45e9c40f8319e175&t=1736753265615&pageHeader=1&v=0")

    time.sleep(1)
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    # 2.2.1.进入观看视频页面
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "catalog_sbar")))
    catalog_0 = driver.find_elements(By.CLASS_NAME, "catalog_sbar")[0]
    catalog_0.click()

    print(driver.page_source)
    # 2.2.2.选择右侧的
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "posCatalog_level"))
    )

    # 找到所有 class 为 "posCatalog_level" 的 div 元素
    pos_catalog_levels = driver.find_elements(By.CLASS_NAME, "posCatalog_level")

    # 遍历每个 posCatalog_level
    for level in pos_catalog_levels:
        # 动态等待 level 下的 ul li 元素加载完成
        try:
            WebDriverWait(level, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul li"))
            )
        except Exception as e:
            print(f"level 下的 li 元素加载失败: {e}")
            continue

        # 找到该 level 下的所有 ul li 元素
        list_items = level.find_elements(By.CSS_SELECTOR, "ul li")

        # 遍历每个 li 元素
        for li in list_items:
            # 动态等待 li 中的可点击元素加载完成
            try:
                button = WebDriverWait(li, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.posCatalog_select, span.posCatalog_name"))
                )
                # 使用 ActionChains 模拟点击
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                ActionChains(driver).move_to_element(button).click().perform()

                print(f"Clicked: {button.text}")  # 打印点击的按钮文本
            except Exception as e:
                print(f"Could not click element: {e}")
    # 2.3.写章节测试
    chapter_test = driver.find_elements(By.CSS_SELECTOR, "li[title='章节测验']")
    if chapter_test != []:
        chapter_test[0].click()
    chapter_test = driver.find_elements(By.CSS_SELECTOR, "li[title='测验']")
    if chapter_test != []:
        chapter_test[0].click()

    time.sleep(3)

    # 3.
    pic_name = r'./chaoxing.png'
    get_image(pic_name, driver)

    time.sleep(1000)
    # 4.