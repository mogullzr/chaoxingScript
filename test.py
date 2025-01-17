# from openai import OpenAI
#
#
# def DeepSeekAsk(prompt, temperature):
#     api_key = "sk-ecee03845a1b42938fb66bae42694268"
#     message = {"role": "user", "content": prompt}
#     client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[message],
#         temperature=temperature,
#         stream=False
#     )
#     return response.choices[0].message.content
#
# if __name__ == '__main__':
#     prompt = '''请根据以下题目要求回答问题：
#             1.不要其他话语，我仅仅需要这些题目的选择答案哟
#
#             2.所有题目的答案必须从选项 A、B、C、D 中选择。
#
#             3.对于判断题，答案只能是 A 或 B，分别对应题目中的 A（对） 和 B（错）。
#
#             4.如果题目重复出现，只需回答一次，不要重复回答。
#
#             5.请严格按照题目编号顺序给出答案,1,2,3,4这样的题目序号顺序给出选择的答案。
#             最终你给出的答案格式应当类似于下面这样：选项1,选项2,选项3
#
#             6.注意：请你忽略我的答案，这可能是错误答案哟；同时请你注意每道题目开头的【】
#             里面内容判断这道题目是什么类型的题目
#             \n'''
#     prompt += '''1【单选题】关于安全电压，下列说法中错误的是()。
# 1【单选题】关于安全电压，下列说法中错误的是()。
# 1【单选题】关于安全电压，下列说法中错误的是()。
# A、
# 安全电压是指不会引起生命危险的电压
# 1【单选题】关于安全电压，下列说法中错误的是()。
# A、
# 安全电压是指不会引起生命危险的电压
# B、
# 安全电压是绝对的
# C、
# 我国规定的安全电压为36V
# D、
# 各个国家的安全电压规定不完全同
# 1【单选题】关于安全电压，下列说法中错误的是()。
# A、安全电压是指不会引起生命危险的电压
# B、安全电压是绝对的
# C、
# 我国规定的安全电压为36V
# D、各个国家的安全电压规定不完全同
# 33.3
# 分
# 2【多选题】关于预防实验室触电，下列说法中正确的是()。
# 2【多选题】关于预防实验室触电，下列说法中正确的是()。
# A、不能用潮湿的手接触电器、灯头、插头
# B、所有电源的裸露部分都应有绝缘装置
# C
# 绝缘不良的电线可以继续使用
# 2【多选题】关于预防实验室触电，下列说法中正确的是()。
# A、不能用潮湿的手接触电器、灯头、插头
# B、所有电源的裸露部分都应有绝缘装置
# C、绝缘不良的电线可以继续使用
# D、维修或安装电器设备时，必须先切断电
# 3【判断题】任何情况下，在安全电压范围内都不会发生触电事故。()
# 3【判断题】任何情况下，在安全电压范围内都不会发生触电事故。()
# '''
#     print(DeepSeekAsk(prompt, 1.3))

def remove_line_with_string(file_path, target_string):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 过滤掉包含目标字符串的行
    filtered_lines = [line for line in lines if target_string not in line]

    # 将过滤后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)

# 示例：删除文件中包含“我的答案：”的行
file_path = 'problem_content.txt'  # 替换为你的文件路径
target_string = '我的答案：'
remove_line_with_string(file_path, target_string)