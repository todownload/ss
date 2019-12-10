from django.contrib import admin

from .models import *

# Register your models here.

class CourseInline(admin.TabularInline):
    model=Course
    extra=1

class TeacherAdmin(admin.ModelAdmin):
    fields = ['teacher_name','teacher_id','teacher_pwd']
    inlines=[CourseInline]
    list_display = ( 'teacher_name', 'teacher_id' )

class StudentAdmin(admin.ModelAdmin):
    fields = ['stu_name','stu_id','stu_pwd']

class KnowledgeInline(admin.TabularInline):
    model = Knowledge
    extra = 1

class AnnouncementInline(admin.TabularInline):
    model = Announcement
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [ ('Course Info', {'fields':['course_name','teacher','course_id','course_stu_num']}),('DateTime Info', {'fields':['course_starttime','course_endtime']})  ]
    inlines = [KnowledgeInline, AnnouncementInline]

class AnnouncementAdmin(admin.ModelAdmin):
    fields = ['course','anno_pubtime','anno_title','anno_content']



admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Announcement,AnnouncementAdmin)
admin.site.register(SelectQuestion)
admin.site.register(DesignQuestion)
admin.site.register(DrawQuestion)
admin.site.register(Student,StudentAdmin)


