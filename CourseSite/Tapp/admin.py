from django.contrib import admin

from .models import *

# Register your models here.

class CourseInline(admin.TabularInline):
    model=Course
    fieldsets = (
        ("CourseInfo", {
            'fields': (
                'course_name',
                'course_id',
                'course_stu_num'
            ),
        }),
        ("DatetimeInfo",{
            'fields':(
                'course_starttime',
                'course_endtime'
            )
        })
    )
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

class SelectQuestionInline(admin.TabularInline):
    model = SelectQuestion
    fieldsets = (
        ("AnswerInfo", {
            'fields': (
                "total_submit",
                "correct_submit"
            ),
        }),
        ("QuestionIfo",{
            'fields':(
                "question_text",
                "answer",
                "choice_A",
                "choice_B",
                "choice_C",
                "choice_D",
            ),
        }),
    )
    extra = 1

class DrawQuestionInline(admin.TabularInline):
    model = DrawQuestion
    fieldsets = (
        ("AnswerInfo", {
            'fields': (
                "total_submit",
                "correct_submit"
            ),
        }),
        ("QuestionInfo",{
            "fields":(
                "question_text",
            )
        }),
    )
    extra = 1

class DesignQuestionInline(admin.TabularInline):
    model =DesignQuestion
    fieldsets = (
        ("AnswerInfo", {
            'fields': (
                "total_submit",
                "correct_submit"
            ),
        }),
        ("QuestionInfo",{
            "fields":(
                "question_text",
                "example_input",
                "example_output",
                "inputFile",
                "outputFile",
            )
        }),
    )
    extra = 1

class KnowledgeAdmin(admin.ModelAdmin):
    fields = ['knowledge_name']
    inlines = [SelectQuestionInline,DrawQuestionInline,DesignQuestionInline]


admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Knowledge,KnowledgeAdmin)
admin.site.register(Announcement,AnnouncementAdmin)


