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
def midRegisterView(request):
    try:
        stu_name = request.POST['usr_name']
        stu_id = request.POST['usr_id']
        pwd = request.POST['usr_pwd']
        cof = request.POST['usr_cof']
        if stu_name =="" or stu_id == "" or pwd != cof:
            return HttpResponseRedirect(reverse('Tapp:course',args=()))
        Student.objects.create(stu_name=stu_name,stu_id=stu_id,stu_pwd=pwd)
        # print("at db")
        return HttpResponseRedirect(reverse('Tapp:login',args=()))
    except Exception:
        return HttpResponseRedirect(reverse('Tapp:register',args=()))


@require_POST
def midLoginView(request): # 处理login的中间层 只能由内部POST访问
    try:
        stu = Student.objects.get(stu_id=request.POST['usr_count'])
        if stu.stu_pwd == request.POST['usr_pwd']:
            return HttpResponseRedirect(reverse('Tapp:courses',args=()))
        return HttpResponseRedirect(reverse('Tapp:login',args=()))
    except Exception:
        return HttpResponseRedirect(reverse('Tapp:login',args=()))

class CoursesView(generic.ListView):
    template_name = "Tapp/courses.html"
    context_object_name = "all_courses"
    def get_queryset(self):
        """Return all courses"""
        return Course.objects.all()
    # def http_method_not_allowed(self, request):
    #     return HttpResponseNotAllowed(permitted_methods="POST GET")

@require_POST
def allCourse(request):
    return CoursesView.as_view()

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

class UserDetailView(generic.DetailView):
    model = Student
    template_name = 'Tapp/userInfo.html'
    contest_object_name = 'usr'



class CourseDetailView(generic.DetailView): # 接受名为pk的参数 查找相应对象 会返回HTTP404
    model = Course
    template_name = "Tapp/course_detail.html"
    contest_object_name = "course"



class SelectDetailView(generic.DetailView):
    model = SelectQuestion
    template_name = "Tapp/selectDetail.html"
    contest_object_name = 'select'
    pass

class DrawDetailView(generic.DetailView):
    model = DrawQuestion
    template_name = 'Tapp/drawDetail.html'
    contest_object_name = 'draw'

class DesignDetailView(generic.DetailView):
    model = DesignQuestion
    template_name = 'Tapp/designDetail.html'
    contest_object_name = 'design'



# def course_detail(request,c_id): # 依主码来找
#     c = get_object_or_404(Course,pk=c_id) # 快捷函数 得到对象 或抛出404
#     context = {"course":c}
#     return render(request,"Tapp/course_detail.html",context)




