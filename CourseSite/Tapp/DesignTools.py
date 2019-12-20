

"""
这是一个为文件处理提供工具函数的文件
"""

from random import randint
import os

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

def decodeFile(inputPath:str, aswPath:str,pk:int, Num:int, StoreDirectory:str):
    """获取第 Num 个 问题答案对 并储存在文件中 返回文件

    inputPath -- 输入文件路径

    aswPath -- 输出文件路径

    Num -- 第几个

    pk -- 题目id

    StoreDirectory -- 存储路径名
    """
    inputFile = StoreDirectory+str(pk)+"_"+str(Num)+"input.txt" # 文件路径名
    if os._exists(inputFile): # 若已存在
        pass
    else:
        inputLines = open(inputPath,'r').readlines() # 获取内容
        l = len(inputLines)
        count = 1
        cur = 0
        while cur<l and count<Num: # 找到对应输入用例
            if inputLines[cur][0]=='=' and inputLines[cur][1]=='=' and inputLines[cur][2]=='=':
                count += 1
            cur += 1
        if cur>=l:
            return None
        with open(inputFile, 'w') as fw:# 写入目标文件
            for i in range(cur,l):
                if inputLines[i][0]=='=' and inputLines[i][1]=='=' and inputLines[i][2]=='=':# 遇到终止行则停止
                    break;
                fw.write(inputLines[i])
        pass
    aswFile = StoreDirectory+str(pk)+"_"+str(Num)+"asw.txt" # 文件路径名
    if os._exists(aswFile): # 若已存在
        pass
    else:
        inputLines = open(aswPath,'r').readlines() # 获取内容
        l = len(inputLines)
        count = 1
        cur = 0
        while cur<l and count<Num: # 找到对应输入用例
            if inputLines[cur][0]=='=' and inputLines[cur][1]=='=' and inputLines[cur][2]=='=':
                count += 1
            cur += 1
        if cur>=l:
            return None
        with open(aswFile, 'w') as fw:# 写入目标文件
            for i in range(cur,l):
                if inputLines[i][0]=='=' and inputLines[i][1]=='=' and inputLines[i][2]=='=':# 遇到终止则停止
                    break;
                fw.write(inputLines[i])
            pass
        pass
    return inputFile,aswFile


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

def compare(outputPath:str, aswPath:str):
    """将程序输出与答案进行比对

    outputPath -- 程序输出文件路径

    aswPath -- 答案文件路径
    """
    x = open(outputPath).readlines()
    y = open(aswPath).readlines()
    rx =[]
    ry =[]
    #  处理文件 去除空行
    for line in x:
        if len(line.strip())>0:
            rx.append(line.strip())
            # print(line.strip())
    for line in y:
        if len(line.strip())>0:
            ry.append(line.strip())
            # print(line.strip())
    if len(rx)!=len(ry): # 先比行数
        return False
    l = len(rx)
    for i in range(0,l): # 逐行比值
        if rx[i]!=ry[i]:
            return False
    return True










