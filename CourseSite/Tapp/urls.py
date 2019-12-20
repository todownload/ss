from django.urls import path
from . import views

app_name = "Tapp"
urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('register/mid/',views.midRegisterView,name='midRegister'),
    path('login/',views.login,name='login'),
    path('login/mid/',views.midLoginView,name='midLogin'),
    path('courses/<int:spk>/',views.Courses ,name='courses'),
    path('courses/<int:spk>/<int:cpk>/sel/',views.handleSelectCourse,name="selectCourse"),
    path('courses/<int:spk>/<int:cpk>/exit/',views.handleExitCourse,name="exitCourse"),
    path('course/<int:pk>/',views.courseDetail,name='courseDetail'),
    path('usr/<int:pk>/',views.userDetail,name="userDetail"),
    path('course/<int:pk>/announcements/',views.Announcements,name='announcements'),
    path('knowledges/<int:pk>/',views.knowledgeDetail, name="knowledgeDetail"),
    path('courses/select/<int:pk>/',views.SelectDetailView.as_view(),name="selectDetail"),
    path('course/select/<int:pk>/res/',views.handleSelect,name="handleSelect"),
    path('courses/draw/<int:pk>/',views.DrawDetailView.as_view(),name="drawDetail"),
    path('courses/draw/<int:pk>/res/',views.handleDraw,name="handleDraw"),
    path('courses/design/<int:pk>/',views.DesignDetail ,name="designDetail"),
    path('course/design/<int:pk>/res/',views.handleDesign,name="handleDesign")
]
