from django.urls import path
from ocrapp import views

app_name = 'ocrapp'

urlpatterns = [
	path('',views.photo,name='photo'),
	path('result/',views.result,name = 'result'),
	path('aadhar/',views.aadhar,name = 'aadhar'),
	path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.LogoutView.as_view(),name='logout'),
    path('register/',views.register,name='register'),
	path('feedback/',views.feedback,name = 'feedback'),
	path('community/',views.community_form_view,name='community_form_view'),
	#path('dashboard/',views.dashboard,name= 'dashboard'),
]
