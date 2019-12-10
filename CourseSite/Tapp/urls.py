from django.urls import path
from . import views

app_name = "Tapp"
urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('register/mid/',views.midRegisterView,name='midRegister'),
    path('login/',views.login,name='login'),
    path('login/mid/',views.midLoginView,name='midLogin'),
    path('courses/',views.allCourse,name='courses'),
    path('courses/<int:pk>/',views.CourseDetailView.as_view(),name='courseDetail'),
    path('usr/<int:pk>/',views.UserDetailView.as_view(),name="userDetail"),
    path('courses/select/<int:pk>/',views.SelectDetailView.as_view(),name="selectDetail"),
    path('courses/draw/<int:pk>/',views.DrawDetailView.as_view(),name="drawDetail"),
    path('courses/design/<int:pk>/',views.DesignDetailView.as_view(),name="designDetail")
]
