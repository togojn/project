from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    #デフォルトのURLでは拠点一覧を表示
    path('base/', views.BaseList.as_view(), name='base_list'),

    #<int:pk>にはBaseModelのnameに割り振られた数値が設定される
    path('base/<int:pk>/seat/', views.SeatList.as_view(), name='seat_list'),

    #日付未指定の場合は当日、日付指定の場合は該当日でのカレンダー表示
    path('base/<int:pk>/calendar/', views.SeatList.as_view(), name='calendar'),
    path('base/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.SeatList.as_view(), name='calendar'),

    path('base/<int:pk>/booking/<int:no>/<int:year>/<int:month>/<int:day>/', views.Booking.as_view(), name='booking'),

    path('scheduledelete/<int:pk>/delete/', views.ScheduleDelete.as_view(), name='scheduledelete'),

    #path('scheduledelete/<int:pk>/delete/<int:no>/<int:year>/<int:month>/<int:day>/', views.ScheduleDelete.as_view(), name='scheduledelete'),
    
    #path('base/<int:pk>/scheduledelete/<int:no>/<int:year>/<int:month>/<int:day>/', views.ScheduleDelete.as_view(), name='scheduledelete'),
    #path('base/<int:pk>/booking/<int:no>/<int:year>/<int:month>/<int:day>/scheduledelete/<int:sche>/', views.ScheduleDelete.as_view(), name='scheduledelete'),

    #錦糸町座席表 表示用URL
    path('base/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/Map1/', views.SeatMap1.as_view(), name='SeatMap1'),
    #錦糸町座席表 表示用URL
    path('base/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/Map2/', views.SeatMap2.as_view(), name='SeatMap2'),

]