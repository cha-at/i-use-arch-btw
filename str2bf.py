# 这个是我为了方便测试让Gemini快速写的
def string_to_brainfuck(text):
    bf_code = []
    
    for char in text:
        target = ord(char)
        
        # 寻找两个乘数，使它们的乘积接近目标 ASCII 值
        # 例如：72 (H) 可以分解为 8 * 9
        factor1 = 10
        factor2 = target // factor1
        remainder = target % factor1
        
        # 构建循环结构: +++++ [ > ++++++ < - ] > ++++ .
        setup = "+" * factor1
        loop = "[>" + ("+" * factor2) + "<-]>"
        finish = ("+" * remainder) + "."
        reset = "[-]<" # 清除当前格数值并回到原位，为下个字符做准备
        
        bf_code.append(setup + loop + finish + reset)
    
    return "".join(bf_code)

# 测试运行
input_str = "I use 'I use arch btw' lang btw."
result = string_to_brainfuck(input_str)

print(f"--- 原始字符串 ---\n{input_str}\n")
print(f"--- Brainfuck 代码 ---\n{result}\n")