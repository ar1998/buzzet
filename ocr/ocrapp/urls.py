from django.urls import path
from ocrapp import views

app_name = 'ocrapp'

urlpatterns = [
	path('',views.photo,name='photo'),
	path('about/',views.about,name='about'),
	path('result/',views.result,name = 'result'),
	path('aadhar/',views.aadhar,name = 'aadhar'),
	path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.LogoutView.as_view(),name='logout'),
    path('register/',views.register,name='register'),
	path('about/feedback_view/',views.feedback_view,name = 'feedback_view'),
	path('about/feedback_hindi/',views.feedback_hindi,name = 'feedback_hindi'),
	path('community/',views.community_form_view,name='community_form_view'),
	path('community/',views.community_form_view,name='community_form_view'),
	path('investor/',views.investor_view,name='investor'),
	path('investee/',views.investee_view,name='investee'),
	path('sub_view/',views.sub_view,name='sub_view'),
	#path('dashboard/',views.dashboard,name= 'dashboard'),
]
