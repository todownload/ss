from django.http import HttpResponseRedirect, HttpResponse ,Http404,HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_POST # 装饰器

from .models import *

import os
response="""
    <head>
    <title>Asw</title>
    <link rel="shortcut icon" href="/Tapp/static/Tapp/images/favicon.ico" type="image/x-icon">
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



class DrawDetailView(generic.DetailView):
    model = DrawQuestion
    template_name = 'Tapp/drawDetail.html'
    context_object_name = 'draw'

@require_POST
def handleDraw(request,pk): # 处理绘图题
    try:
        draw = DrawQuestion.objects.get(pk=pk)
    except Exception:
        return HttpResponse("No such draw question")
    try:
        asw = request.POST['asw']
    except Exception:
        return HttpResponse("Submit no answer")
    try:
        content = f"<p>{asw}</p>"
        return HttpResponse(content=content)
    except Exception:
        return HttpResponse("Unknown Error")


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
                    os.system(cmd)
                    if not (compare(directory+fileN+".txt",tmpOutput)):
                        testCase = open(tmpInput,'r').readlines()
                        reason = "<h3>在此用例下出错</h3>"
                        for line in testCase:
                            tmp = "<p>"+line+"</p><br>"
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
这是一个为文件处理提供工具函数的部分
"""

from random import randint
import os

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













