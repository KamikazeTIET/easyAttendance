from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('mark/', views.mark, name='mark_attendance'),
    path('view/', views.view, name='view_attendance'),
    path('hostel-dashboard/', views.hostelDashboard, name='hostel_dashboard'),
    path('video-stream/', views.videoStream, name='video_camera'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('mark-manual/', views.manualMark, name='mark_manual'),
    path('send-mails/', views.sendMails, name='send_mails'),
]