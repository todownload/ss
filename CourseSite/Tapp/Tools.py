"""
这是一个为文件处理提高工具函数的文件
"""

from random import randint


suffix = { # 语言对应文件后缀
    'C':'.c',
    'C++':'.cpp',
    'Python':'.py',
    'Verilog':'.v'
}

def getSuffix(lang:str):
    if lang in list(suffix.keys()):
        return suffix[lang]
    else:
        return suffix['Python']

def getFileN(pk:int): # 产生随机的临时文件名 避免冲突
    fileN = str(pk)
    for i in range(0,8):
        fileN += str(randint(0,9))
    return fileN



def getCommand(lang:str, fileN:str, filePath:str, inputPath:str, outputDirectory:str):
    """产生执行的命令

    lang -- 语言

    fileN -- 随机文件名

    filePath -- 程序文件路径

    inputPath -- 输入文件路径

    outputDirectory -- 输出文件目录路径   输出文件 outputDirectory/fileN.txt
    """
    commands = ""
    Fix = suffix[lang]
    if lang=="C":
        commands = "gcc -o "+outputDirectory+fileN+" "+filePath+"; "+outputDirectory+fileN+" <"+inputPath+" >"+outputDirectory+fileN+".txt"
    elif lang=="C++":
        commands = "g++ -o "+outputDirectory+fileN+" "+filePath+"; "+outputDirectory+fileN+" <"+inputPath+" >"+outputDirectory+fileN+".txt"
    elif lang=="Python":
        commands = "python3 "+filePath + " <"+inputPath + " >"+outputDirectory+fileN+".txt"
    else:
        commands = "iverilog -o "+ outputDirectory + fileN+".vvp "+filePath+"; vvp "+fileN+".vvp <" +inputPath +" >"+outputDirectory +fileN+".txt"
    return commands





def main():
    print("This is just a tools file")

if __name__ == "__main__":
    main()






