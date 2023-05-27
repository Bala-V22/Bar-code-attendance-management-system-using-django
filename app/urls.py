from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    # path('video_stream/', views.video_stream, name='video_stream'),
    path('add_photos/', views.add_photos, name='add_photos'),
    path('add_photos/<slug:emp_id>/', views.create_barcode, name='create_barcode'),
    path('train_model/', views.log, name='train_model'),
    path('detected/', views.detected, name='detected'),
    path('train_model/loged/',views.com, name='train_model/loged/com'),
    # path('train_model/loged/com',views.com, name='train_model/loged/com'),
    path('identify/', views.identify, name='identify'),
    path('add_emp/', views.add_emp, name='add_emp'),
    path('absent/', views.absent, name='absent'),
    path('absent/send_mail/', views.send_mail, name='send_mail'),
    path('add_attent/', views.add_attent, name='add_attent'),
    path('threedays_absent/', views.threedays_absent, name='threedays_absent'),
    path('threedays_absent/send_mail/', views.send_mail, name='send_mail'),
    path('', views.login),
    path('train_model/loged', views.login),
    path('back/', views.stu_back),
    path('staff/loged', views.login),
    path('about/',views.about),
    path('staff/', views.add_staff),
    path('add_stu/',views.add_stu)

]