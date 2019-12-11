from django.db import models
from django.utils import timezone

# Create your models here.
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=20) # 教师名字
    teacher_id = models.CharField(max_length=15,unique=True) # 教师ID 唯一
    teacher_pwd = models.CharField(max_length=30) # 教师密码
    def __str__(self):
        return self.teacher_name

class Student(models.Model):
    stu_name = models.CharField(max_length=20) # 学生名字
    stu_id = models.CharField(max_length=15,unique=True) # 学生id 唯一
    stu_pwd = models.CharField(max_length=30) # 学生密码
    def __str__(self):
        return self.stu_name

class Course(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    course_name =  models.CharField(max_length=50) # 课程名字
    course_id = models.CharField(max_length=20,unique=True) # 课程id 唯一 用于辨别课程
    course_starttime = models.DateTimeField("start time") # 课程开始时间
    course_endtime = models.DateTimeField("end time") # 课程结束时间
    course_stu_num = models.IntegerField(default=0) # 学生数
    def __str__(self):
        return self.course_name
    def is_begin(self):
        return self.course_starttime <= timezone.now() # 是否已经过了开始时间
    def is_end(self):
        return self.course_endtime <= timezone.now() # 是否已经过了结束时间

class Announcement(models.Model): # 公告
    course = models.ForeignKey(Course,on_delete=models.CASCADE) # 绑定课程
    anno_title = models.CharField(max_length=50) # 标题
    anno_content = models.TextField(default="") # 内容
    anno_pubtime = models.DateTimeField() # 发布时间
    def __str__(self):
        return f"{self.anno_title}"

class Knowledge(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    knowledge_name = models.CharField(max_length=30)
    def __str__(self):
        return f'{self.course.course_name}--{self.knowledge_name}'

class SelectQuestion(models.Model): # 选择题
    knowledge = models.ForeignKey(Knowledge,on_delete=models.CASCADE) # 对应知识
    question_text = models.CharField(max_length=200) # 问题描述
    total_submit = models.IntegerField(default=0) # 总提交人数
    correct_submit = models.IntegerField(default=0) # 正确人数
    answer = models.CharField(max_length=1,choices=[('A','Answer A'),('B','Answer B'),('C','Answer C'),('D','Answer D')]) # 问题答案
    choice_A = models.CharField(max_length=100) # 选项A
    choice_B = models.CharField(max_length=100) # 选项B
    choice_C = models.CharField(max_length=100) # 选项C
    choice_D = models.CharField(max_length=100) # 选项D
    question_analysis = models.TextField(default="") # 问题解析
    def __str__(self):
        return self.question_text

class DesignQuestion(models.Model): # 程序设计题
    knowledge = models.ForeignKey(Knowledge,on_delete=models.CASCADE) # 对应知识
    question_text = models.CharField(max_length=200) # 问题描述
    question_language = models.CharField(max_length=30,choices=[('C','C language'),('C++','C plus plus'),('Python','Python'),('Verilog','Verilog')]) # 需要的语言
    total_submit = models.IntegerField(default=0) # 总提交人数
    correct_submit = models.IntegerField(default=0) # 正确人数
    example_input = models.CharField(max_length=100) # 示例输入
    example_output = models.CharField(max_length=100) # 示例输出
    question_analysis = models.TextField(default="") # 问题解析
    def __str__(self):
        return self.question_text

class DrawQuestion(models.Model):
    knowledge = models.ForeignKey(Knowledge,on_delete=models.CASCADE) # 对应知识
    question_text = models.CharField(max_length=200) # 问题描述
    total_submit = models.IntegerField(default=0) # 总提交人数
    correct_submit = models.IntegerField(default=0) # 正确人数
    def __str__(self):
        return self.question_text

