from django.http import HttpResponseRedirect, HttpResponse ,Http404,HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_POST # 装饰器

from .models import *

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


# def courses(request): # 课程索引
#     try:
#         stu = Student.objects.get(stu_id=request.POST['usr_count'])
#     except Exception:
#         # return Http404("Please login first!")
#         # return HttpResponse("Please login first!") # 避免非用户通过查看源代码访问此页面
#         return HttpResponseRedirect(reverse('Tapp:login',args=())) # 跳转回会登录页面
#     else:
#         all_courses = Course.objects.all()
#         # outputs = '<br>'.join([c.course_name for c in all_courses])
#         # return HttpResponse(content=outputs)
#         context = {"all_courses":all_courses} # 创建上下文对象
#         return render(request,"Tapp/courses.html",context) # 渲染模板

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
    # except Exception: # 用于断点调试
    #     return HttpResponse("No such course")
    # try:
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
        return HttpResponse("Submit no answer")
    try:
        select.total_submit +=1
        select.save()
        if (select.answer==asw):
            select.correct_submit +=1
            select.save()
            return HttpResponse("<h2>You are right</h2>")
        return HttpResponse("<h2>wrong answer</h2>")
    except Exception:
        return HttpResponse("<h2>Unknown Error</h2>")

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

class DesignDetailView(generic.DetailView):
    model = DesignQuestion
    template_name = 'Tapp/designDetail.html'
    context_object_name = 'design'


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
        content = f"<p>{asw}</p>"
        return HttpResponse(content=content)
    except Exception:
        return HttpResponse("Unknown Error")



# def course_detail(request,c_id): # 依主码来找
#     c = get_object_or_404(Course,pk=c_id) # 快捷函数 得到对象 或抛出404
#     context = {"course":c}
#     return render(request,"Tapp/course_detail.html",context)




