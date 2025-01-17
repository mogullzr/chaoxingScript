# import time
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#
# def initialize_webdriver():
#     options = webdriver.ChromeOptions()
#     # options.add_argument("--headless")  # 启用无头模式
#     options.add_argument("--disable-css")  # 禁用css
#     options.add_argument("--disable-images")  # 图片不加载
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option("useAutomationExtension", False)
#
#     driver = webdriver.Chrome(service=Service("../chromedriver_win32/chromedriver.exe"), options=options)
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => undefined
#         })
#         """
#     })
#     return driver
#
# def login(driver, phone, pwd):
#     driver.get("https://passport2.chaoxing.com/login")
#     print(driver.page_source)
#     WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-big-blue.margin-btm24")))
#
#     username_field = driver.find_element(By.ID, "phone")
#     password_field = driver.find_element(By.ID, "pwd")
#     username_field.send_keys(phone)
#     password_field.send_keys(pwd)
#     driver.find_element(By.CSS_SELECTOR, ".btn-big-blue.margin-btm24").click()
#     WebDriverWait(driver, 15).until(EC.url_changes("https://passport2.chaoxing.com/login"))
#     time.sleep(3)
#     driver.get(
#         "")
#
#     time.sleep(3)
#     iframe = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "iframe"))
#     )
#     driver.switch_to.frame(iframe)
#
#     # 进入观看视频页面
#     WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "catalog_sbar")))
#     catalog_0 = driver.find_elements(By.CLASS_NAME, "catalog_sbar")[0]
#     catalog_0.click()
#     time.sleep(1)
#
#     # 写章节测试
#     chapter_test = driver.find_elements(By.CSS_SELECTOR, "li[title='章节测验']")
#     if chapter_test != []:
#         chapter_test.click()
#
#
#
# if __name__ == '__main__':
#     # 初始化驱动
#     driver = initialize_webdriver()
#
#     # 1.登录学习通
#     login(driver, "14796733539", "jiaming456..")
#
# # from fontTools.ttLib import TTFont
# #
# #
# # def ttf_to_xml(ttf_path, xml_path):
# #     # 加载TTF文件
# #     font = TTFont(ttf_path)
# #
# #     # 将TTF文件保存为XML
# #     font.saveXML(xml_path)
# #
# #
# # if __name__ == "__main__":
# #     # 输入TTF文件路径和输出XML文件路径
# #     ttf_file = "chaoxing.ttf"
# #     xml_file = "chaoxing.xml"
# #
# #     # 转换TTF到XML
# #     ttf_to_xml(ttf_file, xml_file)
# #     print(f"TTF文件已成功转换为XML文件: {xml_file}")
#
#
# # 完整代码
# # import requests
# # import re
# # import base64
# # import io
# # from lxml import etree
# # from fontTools.ttLib import TTFont
# #
# # url = r'https://sz.58.com/chuzu/'
# # headers = {
# #     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
# # }
# # response = requests.get(url=url, headers=headers)
# # # 获取加密字符串
# # base64_str = re.search("base64,(.*?)'\)", response.text).group(1)
# # b = base64.b64decode(base64_str)
# # font = TTFont(io.BytesIO(b))
# # bestcmap = font['cmap'].getBestCmap()
# # newmap = dict()
# # for key in bestcmap.keys():
# #     value = int(re.search(r'(\d+)', bestcmap[key]).group(1)) - 1
# #     key = hex(key)  # 10十进制转换16进制
# #     newmap[key] = value
# # # 把页面上自定义字体替换成正常字体
# # response_ = response.text
# #
# # for key, value in newmap.items():
# #     key_ = key.replace('0x', '&#x') + ';'
# #     if key_ in response_:
# #         response_ = response_.replace(key_, str(value))
# # # 获取任意一个价钱
# # rec = etree.HTML(response_)
# # lis = rec.xpath('string(//div[@class="money"]/b[@class="strongbox"]/text())')
#
# # 输入字符串
# # input_str = "咥救咮咧戴咰咲咭咯、手套等选择"
# #
# # # 转换为 Unicode 编码的十六进制格式
# # unicode_codes = [f"0x{ord(char):04x}" for char in input_str]
# #
# # # 将结果拼接为字符串
# # result = " ".join(unicode_codes)
# #
# # # 输出结果
# # print(result)
#
# # 将 Unicode 编码转换为字符
# # unicode_code = "54A5"  # 这是你提供的 Unicode 编码
# # char = chr(int(unicode_code, 16))  # 将十六进制转换为十进制，再转换为字符
# #
# # # 输出结果
# # print(f"Unicode 编码 'uni{unicode_code}' 对应的字符是: {char}")
# # from fontTools.ttLib import TTFont
# #
# # font1 = TTFont('chaoxing.ttf')
# # mp = font1.getBestCmap() #可以看到字体和对应的编码信息
# # for key in mp:
# #     print(key, mp[key])
# # from fontTools.ttLib import TTFont
# # from fontTools.pens.recordingPen import RecordingPen
# # from xml.etree import ElementTree as ET
# # from reportlab.graphics import renderPM
# # from reportlab.graphics.shapes import Path, Drawing
# #
# # def ttglyph_to_recording_pen(ttglyph_data):
# #     """
# #     将 TTGlyph 数据转换为 RecordingPen 格式。
# #     """
# #     pen = RecordingPen()
# #     for contour in ttglyph_data.findall("contour"):
# #         points = contour.findall("pt")
# #         for i, pt in enumerate(points):
# #             x = int(pt.get("x"))
# #             y = int(pt.get("y"))
# #             on = int(pt.get("on"))
# #             if i == 0:
# #                 pen.moveTo((x, y))  # 第一个点是 moveTo
# #             else:
# #                 if on:
# #                     pen.lineTo((x, y))  # on="1" 是 lineTo
# #                 else:
# #                     # on="0" 是控制点，通常用于贝塞尔曲线
# #                     # 这里简化为 lineTo
# #                     pen.lineTo((x, y))
# #         pen.closePath()  # 闭合路径
# #     return pen.value
# #
# # def compare_glyphs(glyph1, glyph2):
# #     """
# #     比较两个字形的轮廓数据是否相同。
# #     """
# #     return glyph1 == glyph2
# #
# # def find_matching_glyph(target_glyph_data, font_path):
# #     """
# #     在字体文件中查找与目标字形数据匹配的汉字。
# #     """
# #     # 加载字体文件
# #     font = TTFont(font_path)
# #     glyph_set = font.getGlyphSet()
# #
# #     index = 1
# #     # 遍历字体文件中的所有字形
# #     for glyph_name in font.getGlyphOrder():
# #         print(glyph_name)
# #         glyph = glyph_set[glyph_name]
# #         pen = RecordingPen()
# #         glyph.draw(pen)
# #         glyph_data = pen.value
# #
# #         index += 1
# #         print(index)
# #         print(glyph)
# #         print(target_glyph_data)
# #         # 比较字形数据
# #         if compare_glyphs(glyph_data, target_glyph_data):
# #             # 获取字形的 Unicode 编码
# #             for table in font['cmap'].tables:
# #                 if glyph_name in table.cmap:
# #                     unicode_value = table.cmap[glyph_name]
# #                     return chr(unicode_value)  # 返回对应的汉字
# #
# #     return None  # 未找到匹配的字形
# #
# # def render_glyph_to_image(glyph_data, output_path):
# #     """
# #     将字形数据渲染为图像。
# #     """
# #     # 创建 Path 对象
# #     path = Path(points=[point for cmd, args in glyph_data for point in args[0]])
# #
# #     # 创建 Drawing 对象
# #     drawing = Drawing(400, 400)
# #     drawing.add(path)
# #
# #     # 渲染为 PNG 图像
# #     renderPM.drawToFile(drawing, output_path, fmt="PNG")
# #
# # def find_matching_char(ttglyph_data, font_path):
# #     """
# #     根据 TTGlyph 数据和字体文件路径查找匹配的汉字。
# #     """
# #     # 将 TTGlyph 数据转换为 RecordingPen 格式
# #     ttglyph = ET.fromstring(ttglyph_data)
# #     target_glyph_data = ttglyph_to_recording_pen(ttglyph)
# #
# #     # 查找匹配的汉字
# #     matching_char = find_matching_glyph(target_glyph_data, font_path)
# #     return matching_char, target_glyph_data
# #
# # # 示例 TTGlyph 数据（替换为你的数据）
# # ttglyph_data = """
# #     <TTGlyph name="uni9900" xMin="119" yMin="-76" xMax="953" yMax="815">
# #       <contour>
# #         <pt x="367" y="405" on="1"/>
# #         <pt x="306" y="405" on="1"/>
# #         <pt x="306" y="815" on="1"/>
# #         <pt x="367" y="815" on="1"/>
# #       </contour>
# #       <contour>
# #         <pt x="119" y="770" on="1"/>
# #         <pt x="180" y="770" on="1"/>
# #         <pt x="180" y="433" on="1"/>
# #         <pt x="119" y="433" on="1"/>
# #       </contour>
# #       <contour>
# #         <pt x="743" y="127" on="1"/>
# #         <pt x="743" y="201" on="1"/>
# #         <pt x="256" y="201" on="1"/>
# #         <pt x="256" y="127" on="1"/>
# #       </contour>
# #       <contour>
# #         <pt x="256" y="320" on="1"/>
# #         <pt x="256" y="249" on="1"/>
# #         <pt x="743" y="249" on="1"/>
# #         <pt x="743" y="320" on="1"/>
# #       </contour>
# #       <contour>
# #         <pt x="809" y="-2" on="1"/>
# #         <pt x="809" y="-52" on="0"/>
# #         <pt x="771" y="-65" on="1"/>
# #         <pt x="741" y="-74" on="0"/>
# #         <pt x="611" y="-74" on="1"/>
# #         <pt x="608" y="-59" on="0"/>
# #         <pt x="589" y="-20" on="1"/>
# #         <pt x="620" y="-21" on="0"/>
# #         <pt x="722" y="-21" on="1"/>
# #         <pt x="743" y="-20" on="0"/>
# #         <pt x="743" y="-2" on="1"/>
# #         <pt x="743" y="77" on="1"/>
# #         <pt x="256" y="77" on="1"/>
# #         <pt x="256" y="-76" on="1"/>
# #         <pt x="190" y="-76" on="1"/>
# #         <pt x="190" y="372" on="1"/>
# #         <pt x="809" y="372" on="1"/>
# #       </contour>
# #       <contour>
# #         <pt x="533" y="730" on="1"/>
# #         <pt x="578" y="642" on="0"/>
# #         <pt x="662" y="577" on="1"/>
# #         <pt x="751" y="642" on="0"/>
# #         <pt x="797" y="730" on="1"/>
# #       </contour>
# #       <contour>
# #         <pt x="885" y="775" on="1"/>
# #         <pt x="837" y="641" on="0"/>
# #         <pt x="716" y="540" on="1"/>
# #         <pt x="820" y="478" on="0"/>
# #         <pt x="953" y="454" on="1"/>
# #         <pt x="936" y="438" on="0"/>
# #         <pt x="911" y="396" on="1"/>
# #         <pt x="766" y="428" on="0"/>
# #         <pt x="662" y="501" on="1"/>
# #         <pt x="563" y="437" on="0"/>
# #         <pt x="435" y="402" on="1"/>
# #         <pt x="419" y="441" on="0"/>
# #         <pt x="401" y="459" on="1"/>
# #         <pt x="519" y="486" on="0"/>
# #         <pt x="610" y="542" on="1"/>
# #         <pt x="522" y="619" on="0"/>
# #         <pt x="472" y="728" on="1"/>
# #         <pt x="478" y="730" on="1"/>
# #         <pt x="438" y="730" on="1"/>
# #         <pt x="438" y="789" on="1"/>
# #         <pt x="834" y="789" on="1"/>
# #         <pt x="844" y="792" on="1"/>
# #       </contour>
# #       <instructions/>
# #     </TTGlyph>
# # """
# #
# # # 字体文件路径（替换为你的字体文件路径）
# # font_path = "chaoxing.ttf"
# #
# # # 查找匹配的汉字
# # matching_char, target_glyph_data = find_matching_char(ttglyph_data, font_path)
# #
# # if matching_char:
# #     print(f"匹配的汉字是: {matching_char}")
# #     # 渲染字形为图像
# #     render_glyph_to_image(target_glyph_data, "glyph.png")
# #     print("字形已渲染为 glyph.png")
# # else:
# #     print("未找到匹配的汉字。")