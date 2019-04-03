from django.urls import path
from ocrapp import views

app_name = 'ocrapp'

urlpatterns = [
	path('photo/',views.photo,name='photo'),
	path('result/',views.result,name = 'result'),
	path('aadhar/',views.aadhar,name = 'aadhar'),
	path('voice/',views.voice,name='voice'),

]
