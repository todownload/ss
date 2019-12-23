from django.http import HttpResponseRedirect, HttpResponse ,Http404,HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_POST # 装饰器

from .models import *

import os
import time
response="""
    <head>
    <title>Asw</title>
    <link rel="shortcut icon" href="/static/Tapp/images/favicon.ico" type="image/x-icon">
    </head>
    <style>
    .btn-success {
    color: #ffffff;
    text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);
    background-color: #5bb75b;
    *background-color: #51a351;
    background-image: -moz-linear-gradient(top, #62c462, #51a351);
    background-image: -webkit-gradient(linear, 0 0, 0 100%, from(#62c462), to(#51a351));
    background-image: -webkit-linear-gradient(top, #62c462, #51a351);
    background-image: -o-linear-gradient(top, #62c462, #51a351);
    background-image: linear-gradient(to bottom, #62c462, #51a351);
    background-repeat: repeat-x;
    border-color: #51a351 #51a351 #387038;
    border-color: rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.25);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ff62c462', endColorstr='#ff51a351', GradientType=0);
    filter: progid:DXImageTransform.Microsoft.gradient(enabled=false);
    }

    .btn-warning {
    color: #ffffff;
    text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);
    background-color: #faa732;
    *background-color: #f89406;
    background-image: -moz-linear-gradient(top, #fbb450, #f89406);
    background-image: -webkit-gradient(linear, 0 0, 0 100%, from(#fbb450), to(#f89406));
    background-image: -webkit-linear-gradient(top, #fbb450, #f89406);
    background-image: -o-linear-gradient(top, #fbb450, #f89406);
    background-image: linear-gradient(to bottom, #fbb450, #f89406);
    background-repeat: repeat-x;
    border-color: #f89406 #f89406 #ad6704;
    border-color: rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.25);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#fffbb450', endColorstr='#fff89406', GradientType=0);
    filter: progid:DXImageTransform.Microsoft.gradient(enabled=false);
    }
    .btn-danger {
    color: #ffffff;
    text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);
    background-color: #da4f49;
    *background-color: #bd362f;
    background-image: -moz-linear-gradient(top, #ee5f5b, #bd362f);
    background-image: -webkit-gradient(linear, 0 0, 0 100%, from(#ee5f5b), to(#bd362f));
    background-image: -webkit-linear-gradient(top, #ee5f5b, #bd362f);
    background-image: -o-linear-gradient(top, #ee5f5b, #bd362f);
    background-image: linear-gradient(to bottom, #ee5f5b, #bd362f);
    background-repeat: repeat-x;
    border-color: #bd362f #bd362f #802420;
    border-color: rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.25);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffee5f5b', endColorstr='#ffbd362f', GradientType=0);
    filter: progid:DXImageTransform.Microsoft.gradient(enabled=false);
    }
    </style>
    """

# Create your views here.

def index(request):
    return render(request,'Tapp/login.html')

def login(request):
    return render(request,'Tapp/login.html')

def register(request):
    return render(request,"Tapp/register.html")

@require_POST
def midRegisterView(request): # 处理注册的中间层 只能由内部POST访问
    try:
        stu_name = request.POST['usr_name']
        stu_id = request.POST['usr_id']
        pwd = request.POST['usr_pwd']
        cof = request.POST['usr_cof']
        if stu_name =="" or stu_id == "" or pwd != cof:
            return HttpResponseRedirect(reverse('Tapp:register',args=()))
        Student.objects.create(stu_name=stu_name,stu_id=stu_id,stu_pwd=pwd)
        return HttpResponseRedirect(reverse('Tapp:login',args=()))
    except Exception:
        return HttpResponseRedirect(reverse('Tapp:register',args=()))


@require_POST
def midLoginView(request): # 处理login的中间层 只能由内部POST访问
    try:
        stu = Student.objects.get(stu_id=request.POST['usr_count'])
        if stu.stu_pwd == request.POST['usr_pwd']:
            return HttpResponseRedirect(reverse('Tapp:userDetail',args=(stu.pk,)))
        return HttpResponseRedirect(reverse('Tapp:login',args=()))
    except Exception:
        return HttpResponseRedirect(reverse('Tapp:login',args=()))

def Courses(request,spk):
    try:
        all_courses = Course.objects.all()
        stu = Student.objects.get(pk=spk)
        selectedCourses = stu.course_set.all()
        context = {"all_courses":all_courses, "selectedCourses":selectedCourses, "stu":stu}
        return render(request,"Tapp/allCourses.html",context=context)
    except Exception:
        return HttpResponse("<h2>Some error Happen</h2>")

    # def http_method_not_allowed(self, request):
    #     return HttpResponseNotAllowed(permitted_methods="POST GET")

@require_POST
def handleSelectCourse(request,spk,cpk):
    try:
        course = Course.objects.get(pk=cpk)
        student = Student.objects.get(pk=spk)
        student.course_set.add(course)
        student.save()
        course.course_stu_num += 1
        course.save()
        return HttpResponseRedirect(reverse("Tapp:courses",args=(spk,)))
    except Exception:
        return HttpResponseRedirect(reverse("Tapp:courses",args=(spk,)))

@require_POST
def handleExitCourse(request,spk,cpk):
    try:
        course = Course.objects.get(pk=cpk)
        student = Student.objects.get(pk=spk)
        student.course_set.remove(course)
        student.save()
        course.course_stu_num -= 1
        course.save()
        return HttpResponseRedirect(reverse("Tapp:courses",args=(spk,)))
    except Exception:
        return HttpResponseRedirect(reverse("Tapp:courses",args=(spk,)))


def userDetail(request,pk): # 用户信息
    try:
        stu = Student.objects.get(pk=pk)
        selected_courses = stu.course_set.all()
        context = {"usr":stu,"selected_courses":selected_courses}
        return render(request,'Tapp/userInfo.html',context)
    except Exception:
        return Http404("No such user")


def courseDetail(request,pk): # 课程信息
    try:
        course = Course.objects.get(pk=pk) # 课程
        announcements = course.announcement_set.all() # 所有公告
        if announcements:
            announcement = announcements.reverse()[0]
        else:
            announcement = None
        knowledges = course.knowledge_set.all() # 知识点
        context = {
            "course":course,
            "announcement":announcement,
            "knowledges":knowledges
        }
        return render(request,'Tapp/courseDetail.html',context)
    except Exception:
        return Http404("No such course")

def knowledgeDetail(request,pk): # 知识点信息
    try:
        knowledge = Knowledge.objects.get(pk=pk)
        selectSet = knowledge.selectquestion_set.all()
        drawSet = knowledge.drawquestion_set.all()
        designSet = knowledge.designquestion_set.all()
        context = {
            "knowledge":knowledge,
            "selectSet":selectSet,
            "drawSet":drawSet,
            "designSet":designSet
        }
        return render(request,'Tapp/knowledgeDetail.html',context)
    except Exception:
        return Http404("No such knowledge")

def Announcements(request,pk): # 公告
    try:
        course = Course.objects.get(pk=pk)
        announcements = course.announcement_set.all().reverse() # 所有公告
        context = {
            "course_name":course.course_name,
            "announcements":announcements
        }
        return render(request,'Tapp/announcements.html',context)
    except Exception:
        return Http404("No such course")



class SelectDetailView(generic.DetailView):
    model = SelectQuestion
    template_name = "Tapp/selectDetail.html"
    context_object_name = 'select'
    pass


@require_POST
def handleSelect(request,pk): # 处理选择题
    try:
        select = SelectQuestion.objects.get(pk=pk)
    except Exception:
        return HttpResponse("No such select question")
    try:
        asw = request.POST['question']
        # print(asw)
    except Exception:
        return HttpResponse(response+"<h2 class='btn-warning>'Submit no answer</h2>")
    try:
        select.total_submit +=1
        select.save()
        if (select.answer==asw):
            select.correct_submit +=1
            select.save()
            return HttpResponse(response+"<h2 class='btn-success'>You are right</h2>")
        return HttpResponse(response+"<h2 class='btn-danger'>wrong answer</h2>")
    except Exception:
        return HttpResponse(response+"<h2 class='btn-warning'>Unknown Error</h2>")


def DrawDetail(request,pk):
    try:
        draw = DrawQuestion.objects.get(pk=pk) # 获取对象
    except Exception:
        return HttpResponse(response+"<h1 class='btn-warning'>No such draw question<h1>")
    try:
        inputLines,aswLines = decodeTableFile(draw.question_file.path) # decode文件
        InputTH,InputTDList = decodeTable(inputLines) # 输入的表头和数据
        aswTH,aswTDList = decodeTable(aswLines) # 答案部分的表头和数据

        countList = [ i+1 for i in range(0,len(aswTDList[0])) ] # 每一列
        # 为了能保证每个input 有唯一的name
        emptyList = []
        for i in range(0,len(aswLines)):
            tmpList = []
            for j in range(0,len(aswTDList[0])):
                tmp = j + i*len(aswTDList[0])
                tmpList.append(tmp)
            emptyList.append(tmpList)

        # print(emptyList)
        imagePath = "Tapp/images/Draw/"+draw.question_image.path.split("\\")[-1] # 图片文件路径

        inNum = len(InputTH) # 输入口数量
        aswNum = len(aswTH) # 输出口数量
        inStr = ""
        aswStr = ""
        for i in range(0,inNum):
            inStr = inStr + InputTH[i] + " "
        for i in range(0,aswNum):
            aswStr = aswStr+aswTH[i]+" "

        if draw.question_type == 0: # 作图题
            context = {
                "draw":draw,
                "inputTH":InputTH,
                "inputTDList":InputTDList,
                "inputLines":inputLines,
                "aswTH":aswTH,
                "aswTDList":aswTDList,
                "countList":countList,
                "inNum":inNum,
                "aswNum":aswNum,
                "inStr":inStr,
                "aswStr":aswStr,
                "emptyList":emptyList, # 每行每列的值 用来给每个input 唯一的name
            }
        else: # 看图填表题
            context = {
                "draw":draw,
                "inputTH":InputTH,
                "inputTDList":InputTDList,
                "aswTH":aswTH,
                "aswTDList":aswTDList,
                "imagePath":imagePath, # 图
                "countList":countList,
                "emptyList":emptyList, # 每行每列的值 用来给input 唯一的name
            }
    # except Exception:
    #     return HttpResponse(response+"<h1 class='btn-warning'>Some thing wrong<h1>")
        return render(request,"Tapp/drawDetail.html",context)
    except Exception:
        return HttpResponse(response+"<h1 class='btn-warning'>Some thing wrong<h1>")

@require_POST
def handleDraw(request,pk): # 处理绘图题
    try:
        draw = DrawQuestion.objects.get(pk=pk)
    except Exception:
        return HttpResponse(response+"<h1 class='btn-warning'>No such draw question<h1>")
    try:
        draw.total_submit +=1 # 总提交次数加1
        draw.save()
        inputLines,aswLines = decodeTableFile(draw.question_file.path) # decode文件
        InputTH,InputTDList = decodeTable(inputLines) # 输入的表头和数据
        aswTH,aswTDList = decodeTable(aswLines) # 答案部分的表头和数据
        lineNum = len(aswTDList) # 行数
        colNum = len(aswTDList[0]) # 列数
        submitTable = []
        for i in range(0,lineNum):
            tmpList = []
            for j in range(0,colNum):
                tmp = j + i*colNum
                val = request.POST[str(tmp)]
                tmpList.append(val)
            submitTable.append(tmpList)
        # print(submitTable)
        if draw.question_type == 0: # 处理画图题
            res = compareTableAll(submitTable, aswTDList)
            print(submitTable)
            print(aswTDList)
            if res:
                draw.correct_submit += 1
                draw.save()
                return HttpResponse(response+"<h2 class='btn-success' >Right</h2>")
            else:
                return HttpResponse(response+"<h2 class='btn-danger'>Wrong Answer</h2>")
        else: # 处理填表题
            res = compareTable(submitTable, aswTDList)
            print(submitTable)
            print(aswTDList)
            if res:
                draw.correct_submit += 1
                draw.save()
                return HttpResponse(response+"<h2 class='btn-success' >Right</h2>")
            else:
                return HttpResponse(response+"<h2 class='btn-danger'>Wrong Answer</h2>")
            # print(table)
    except Exception:
        return HttpResponse(response+"<h2 class='btn-warning'>Unknown Error</h2>")



def DesignDetail(request,pk):
    try:
        design = DesignQuestion.objects.get(pk=pk)
        codetype = getTextType(design.question_language)
        context = {
            "design":design,
            "textType":codetype
        }
        return render(request,"Tapp/designDetail.html",context)
    except Exception:
        return HttpResponse("<h1>No such design question<h1>")


@require_POST
def handleDesign(request,pk): # 处理设计题
    try:
        design = DesignQuestion.objects.get(pk=pk)
    except Exception:
        return HttpResponse("No such design question")
    try:
        asw = request.POST['code']
    except Exception:
        return HttpResponse("Submit no answer")
    try:
        design.total_submit +=1 # 加上次数
        design.save()
        lang = design.question_language # 语言
        fileN = getFileN(pk) # 随机文件名
        fix = getSuffix(lang) # 文件后缀
        directory = "Files/" # 储存目录
        inputPath = design.inputFile.path # 输入文件
        aswPath = design.outputFile.path # 答案文件
        filePath = directory+fileN+fix # 代码文件
        with open(filePath,'w') as fw: # 写入代码
            fw.write(asw)
    # except Exception:
    #     return HttpResponse(response+"Here")
    # try:
        for i in range(1,11):
            tmpInput,tmpOutput =  decodeFile(inputPath, aswPath, pk, i, directory)
            if tmpInput and tmpOutput: # 如果还有测试用例且有结果
                cmd = getCommand(lang, fileN, filePath, tmpInput, directory)
                if cmd:
                    try:
                        res = os.system(cmd)
                        # print(res)
                        if  res != 0:
                            raise Exception
                    except Exception:
                        return HttpResponse(response+"<h2> class='btn-danger'>Runtime Error</h2>")
                    if not (compare(directory+fileN+".txt",tmpOutput)):
                        testCase = open(tmpInput,'r').readlines()
                        reason = "<h3>在此用例下出错</h3>"
                        for line in testCase:
                            tmp = "<pre>"+line+"</pre><br>"
                            reason+=tmp
                        return HttpResponse(response+"<h2 class='btn-danger'>Wrong Answer</h2>"+reason)
                else:
                    break
            else:
                break
        design.correct_submit +=1
        design.save()
        return HttpResponse(response+"<h2 class='btn-success' >Right</h2>")
    except Exception:
        return HttpResponse(response+"<h2 class='btn-warning'>Unknown Error</h2>")
    finally:
        os.remove(filePath)
        os.remove("Files/"+fileN+".txt" )



# def course_detail(request,c_id): # 依主码来找
#     c = get_object_or_404(Course,pk=c_id) # 快捷函数 得到对象 或抛出404
#     context = {"course":c}
#     return render(request,"Tapp/course_detail.html",context)



"""
这是一个为程序设计题处理提供工具函数的部分
"""

from random import randint

suffix = { # 语言对应文件后缀
    'C':'.c',
    'C++':'.cpp',
    'Python':'.py',
    'Verilog':'.v'
}

textType = { # 语言对应模式
    "C":"text/x-csrc",
    "C++":"text/x-c++src",
    "Python":"text/x-python",
    "Verilog":"x-verilog"
}

def getSuffix(lang:str):
    if lang in list(suffix.keys()):
        return suffix[lang]
    else:
        return suffix['Python']

def getTextType(lang:str):
    return textType[lang]

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
            return ("","")
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
            return ("","")
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

    outputDirectory -- 输出文件目录路径

    输出文件 outputDirectory/fileN.txt
    """
    commands = ""
    Fix = suffix[lang]
    if lang=="C":
        commands = "gcc -o "+outputDirectory+fileN+" "+filePath+"; "+outputDirectory+fileN+" <"+inputPath+" >"+outputDirectory+fileN+".txt"
    elif lang=="C++":
        commands = "g++ -o "+outputDirectory+fileN+" "+filePath+"; "+outputDirectory+fileN+" <"+inputPath+" >"+outputDirectory+fileN+".txt"
    elif lang=="Python":
        commands = "python "+filePath + " <"+inputPath + " >"+outputDirectory+fileN+".txt"
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


"""
这是为绘图题提供工具函数的部分
"""

def decodeTableFile(filePath:str):
    """对真值表文件进行处理 得到表格

    filePath -- 文件路径

    return inputLines,outputLines

    """
    lines = open(filePath,'r').readlines() # 获取所有的行
    inputLines = [] # 所有输入列
    aswLines = [] # 所有非输入列
    flag = 1 # 记录当前状态
    l = len(lines) # 行数
    for i in range(0,l):
        if lines[i][0]=='=' and lines[i][1]=='=' and lines[i][2]=='=': # 遇到终止行
            flag +=1
        else:
            line = lines[i]
            tmp = line.strip().split()
            tmpLine = []
            numLine = False # 判断行类型
            for item in tmp:
                if item: # 添加非空元素
                    if len(item)==1 and item>='0' and item<='1' : # 判断类型
                        tmpLine.append(int(item))
                    else:
                        tmpLine.append(item)
            if flag == 1:# 添加输入
                inputLines.append(tmpLine)
                pass
            else:
                aswLines.append(tmpLine)
                pass
    return inputLines,aswLines

def compareTable(submitTable:list,aswTable:list):
    """比较真值表结果

    submitTable -- 提交的真值表

    aswTable -- 答案真值表

    return Bool
    """
    if len(submitTable) != len(aswTable): # 如果长度不一样
        return False
    l = len(submitTable)
    for i in range(0,l):
        tmp1 = submitTable[i]
        tmp2 = aswTable[i]
        tmpL = len(tmp2)
        if len(tmp1)!=tmpL:# 某行的长度不一样
            return False
        for j in range(0,tmpL):# 某个值不一样
            if int(tmp1[j])!=int(tmp2[j]):
                return False
    return True

def compareTableAll(submitTable:list, aswTable:list):
    """比较两个表是否相同 相同的行可能在不同的行

    submitTable -- 提交的表

    sawTable -- 答案表

    比较方法 转化成字符串 排序 逐行比较
    """
    sub = []
    asw = []
    l = len(submitTable)
    if len(aswTable) != l:
        return False
    for i in range(0,l): # 转化为字符串
        tmp1 = submitTable[i]
        tmp2 = aswTable[i]
        tmpL = len(tmp1)
        if len(tmp2)!= tmpL:
            return False
        tmpS1 = ""
        tmpS2 = ""
        for j in range(0,tmpL):
            tmpS1 += str(tmp1[j])
            tmpS2 += str(tmp2[j])
        sub.append(tmpS1)
        asw.append(tmpS2)
    # 进行排序比较
    sortedSub = sorted(sub)
    sortedAsw = sorted(asw)
    for i in range(0,l):
        if sortedSub[i]!=sortedAsw[i]:
            return False
    return True



def decodeTable(Table:list):
    """将表格分成表头和表值两部分

    Table 表格

    return TH,TDList
    """
    if Table and len(Table)>1: # 若是为真
        head = []
        data = []
        for i in range(0,len(Table)):
            head.append(Table[i][0])
            data.append(Table[i][1:])
        return head[:],data[:]
    else:
        return [],[]
    pass


def test():
    """一个测试功能函数的测试函数
    """

    # Test decodeTableFile
    # print(decodeTableFile("Files/empty.json")) #  --- Pass

    # Test compareTable
    aswTable = [
        [1,1,1],
        [0,0,1],
        [0,1,0]
    ]
    rightTable = [
        [0,1,0],
        [1,1,1],
        [0,0,1]
    ]
    wrongTable = [
        [1,1,0],
        [0,0,1],
        [0,1,0]
    ]
    # print(compareTable(rightTable, aswTable))
    # print(compareTable(wrongTable,aswTable))
    # print(True)
    # -- Pass

    # Test decodeTable
    # inputLines,outputLines = decodeTableFile("Files/empty.json")
    # TH,TDList = decodeTable(inputLines)
    # print(TH)
    # print(TDList)
    # print(decodeTable(outputLines))
    # -- pass

    # Test compareTableAll
    # print(compareTableAll(rightTable,aswTable))
    # print(compareTableAll(wrongTable,aswTable))
    # -- pass


    pass












