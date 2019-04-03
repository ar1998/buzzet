from django.shortcuts import render,redirect
from ocrapp.forms import *
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import re
import os
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

#global variables

#doc_name = "name"

def index(request):
    return render(request, 'ocrapp/index.html')

def photo(request):
    if request.method == 'POST':
        #uploading images
        im_form = photo_form(request.POST, request.FILES)
        if im_form.is_valid():
            im_form.save()
            #extracting the file name of the image being uploaded
            for filename, file in request.FILES.items():
                f_name = request.FILES[filename].name
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path =  os.path.join(BASE_DIR, 'media/images')
            final_path = os.path.join(path,f_name)



            def ocr_space_file(filename, overlay=False, api_key='20636de03588957', language='eng'):
                """ OCR.space API request with local file.

                :param filename: Your file path & name.
                :param overlay: Is OCR.space overlay required in your response.
                                Defaults to False.
                :param api_key: OCR.space API key.
                                Defaults to 'helloworld'.
                :param language: Language code to be used in OCR.
                                List of available language codes can be found on https://ocr.space/OCRAPI
                                Defaults to 'en'.
                :return: Result in JSON format.
                """

                payload = {'isOverlayRequired': overlay,
                           'apikey': api_key,
                           'language': language,
                           }
                with open(filename, 'rb') as f:
                    r = requests.post('https://api.ocr.space/parse/image',
                                      files={filename: f},
                                      data=payload,
                                      )
                return r.content.decode()

            #extracting text out of the document
            test_file = ocr_space_file(filename=final_path, language='eng')
            test_file = test_file[test_file.index('"ParsedText":')+14:test_file.index('","ErrorMessage"')]
            result = test_file.split('\\r\\n')

            for word in result:
                if word.find("DOB") != -1:
                    request.session['doc_type'] = "aadhar"
                if word.find("INCOME") != -1:
                    request.session['doc_type'] = "pan"

            if request.session['doc_type'] == 'aadhar':
                request.session['doc_name'] = result[2]
                request.session['doc_id'] = result[5]
                request.session['doc_dob'] = result[3].split(':')[1]
                for i in result:
                    x = re.search('DOB', i)
                    if x:
                        request.session['doc_dob'] = i.split(':')[1]
                    y = re.search('[0-9]{4}\s{4}', i)
                    if y:
                        request.session['doc_id'] = i

            #if request.session['doc_type'] == 'pan':
                #request.session['doc_name'] = result[5]
                #request.session['doc_id'] = result[3]
                #request.session['doc_dob'] = result[9]
            if request.session['doc_type'] == 'pan':
                for i in result:
                    x_id = re.search('[A-Z0-9]{10}', i)
                    x_dob = re.search('/', i)
                    if x_id:
                        request.session['doc_id'] = i
                    if x_dob:
                        request.session['doc_dob'] = i
                c = re.search('[A-Z0-9]{10}', result[5])
                if c:
                    request.session['doc_name'] = result[1]
                else:
                    request.session['doc_name'] = result[5]


            #displaying the extracted details on the webpage
            return render(request,'ocrapp/result.html',{'f_name':result})
            #return redirect('index')
    else:
        im_form = photo_form()
    return render(request,'ocrapp/base.html',{'im_form':im_form})


#aadhar verification being done here
def aadhar(request):
    if request.session['doc_type'] == 'aadhar':
        if request.method == 'POST':
            a_form = aadhar_from(request.POST)

            if a_form.is_valid():
                #extracting data from forms
                name = a_form.cleaned_data.get('name')
                id_num = a_form.cleaned_data.get('id_num')
                dob = a_form.cleaned_data.get('dob')
                #address = a_form.cleaned_data.get('address')

                aadhar_data = aadhar_verification_model.objects.all()
                #verifying the entered adhar details with the database
                for entry in aadhar_data:
                    if entry.name == name and entry.id_num == id_num and entry.dob == dob: #and entry.address == address:
                        new_entry = aadhar_registration_model(name=name,
                                                                id_num=id_num,
                                                                dob=dob)
                                                                #address=address)
                        new_entry.save()
                        return render(request,'ocrapp/succ.html',{'name':entry.name})

                    #else:
                    #    return HttpResponse("verification failed,please enter valid info !")
        else :
            #pre-filling the form
            doc_name = request.session['doc_name']
            doc_id = request.session['doc_id']
            doc_dob = request.session['doc_dob']
            a_from = aadhar_from({'name':doc_name,'id_num':doc_id,'dob':doc_dob})
            return render(request,'ocrapp/verify.html',{'aadhar_from':a_from,'doc_type':request.session['doc_type']})

    if request.session['doc_type'] == 'pan':
        if request.method == 'POST':
            p_form = pan_from(request.POST)

            if p_form.is_valid():
                #extracting data from forms
                name = p_form.cleaned_data.get('name')
                id_num = p_form.cleaned_data.get('id_num')
                dob = p_form.cleaned_data.get('dob')
                #address = a_form.cleaned_data.get('address')

                pan_data = pan_verification_model.objects.all()
                #verifying the entered adhar details with the database
                for entry in pan_data:
                    if entry.name == name and entry.id_num == id_num and entry.dob == dob: #and entry.address == address:
                        new_entry = pan_registration_model(name=name,
                                                                id_num=id_num,
                                                                dob=dob)
                                                                #address=address)
                        new_entry.save()
                        return render(request,'ocrapp/succ.html',{'name':entry.name})

                    #else:
                    #    return HttpResponse("verification failed,please enter valid info !")
        else :
            #pre-filling the form
            doc_name = request.session['doc_name']
            doc_id = request.session['doc_id']
            doc_dob = request.session['doc_dob']
            p_from = pan_from({'name':doc_name,'id_num':doc_id,'dob':doc_dob})
            return render(request,'ocrapp/verify.html',{'aadhar_from':p_from,'doc_type':request.session['doc_type']})







import speech_recognition as sr
r = sr.Recognizer()


def voice(request):
     def spch():

        with sr.Microphone() as source:
            print("SAY SOMETHING")
            audio = r.listen(source)
            print("TIME OVeR. THANKS")
        text = r.recognize_google(audio)
        return text


     voice_text = spch()

     return render(request,'ocrapp/result.html',{'f_name':voice_text})


def result(request):
    return render(request,'ocrapp/result.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['email'],
                                            password=request.POST['password'])
            # user.save()
            # user.set_password(user.password)

            user.save()

            registered = True
            return render(request,'ocrapp/login.html',{'user_form':user_form,
                                                     'registered':registered})
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'ocrapp/base.html',{'user_form':user_form,
                                                     'registered':registered})

def user_login(request):
    print(request, request.method)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                print("login successful")
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("account not active")
        else:
            print("login failed for {}".format(username))
            return HttpResponse("invalid login credentials !!")
    return render(request, 'ocrapp/login.html',)
from django.contrib.auth.views import LoginView, LogoutView


# class UserLoginView(LoginView):
#     template_name = 'notes/login.html'


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout'))
