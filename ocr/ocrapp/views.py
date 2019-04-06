from django.shortcuts import render,redirect
from ocrapp.forms import *
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import re
import os
import requests
import PIL
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import LoginView, LogoutView

#image resize function
'''def resizeAndCrop(imgPath):
    im = Image.open(imgPath)
    os.remove(imgPath)
    x, y = im.size
    yNew = 256
    xNew = yNew
    if x > y:
        xNew = round(x * 256 / y)
    else:
        yNew = round(y * 256 / x)
    resizedImage = im.resize((int(xNew), int(yNew)), PIL.Image.ANTIALIAS)
    print("SAVE", imgPath)
    im.save(imgPath)
    return imgPath
'''

def home(request):
    if request.method == "POST":
        s_form = sub_form(request.POST)
        if s_form.is_valid():
            s_form.save()
            return render(request,'ocrapp/home.html')

    else:
        s_form = sub_form()
        return render(request,'ocrapp/home.html',{'sub_form':s_form})

@login_required
def index(request):
    return render(request, 'ocrapp/index.html')

def about(request):
    feed_list  = []
    feed = feedback.objects.all()
    for x in feed:
        feed_list.append(x)
    return render(request,'ocrapp/about.html',{'feed':feed_list})


#aadhar verification being done here
@login_required
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
            doc_name = request.session['doc_name'].strip()
            doc_id = request.session['doc_id'].strip()
            doc_dob = request.session['doc_dob'].strip()
            a_from = aadhar_from({'name':doc_name,'id_num':doc_id,'dob':doc_dob})
            return render(request,'ocrapp/verify.html',{'aadhar_from':a_from,'doc_type':"AADHAR CARD"})

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
            doc_name = request.session['doc_name'].strip()
            doc_id = request.session['doc_id'].strip()
            doc_dob = request.session['doc_dob'].strip()
            p_from = pan_from({'name':doc_name,'id_num':doc_id,'dob':doc_dob})
            return render(request,'ocrapp/verify.html',{'aadhar_from':p_from,'doc_type':"PAN CARD"})







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

@login_required
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
        request.session['username'] = username
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                print("login successful")
                return HttpResponseRedirect(reverse('home'))
                #return render(request, 'ocrapp/index.html',)
            else:
                return HttpResponse("account not active")
        else:
            print("login failed for {}".format(username))
            return HttpResponse("invalid login credentials !!")
    return render(request, 'ocrapp/login.html',)



# class UserLoginView(LoginView):
#     template_name = 'notes/login.html'


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout'))


def feedback_view(request):
    if request.method == 'POST':
        feed_form = feedback_form(request.POST)

        if feed_form.is_valid():
            feed_form.save()

            return redirect("http://beginners.pythonanywhere.com/")

    else:
        def spch():

            with sr.Microphone() as source:
                print("SAY SOMETHING")
                audio = r.listen(source)
                print("TIME OVeR. THANKS")
            text = r.recognize_google(audio,)
            return text

        voice_text = spch()
        username = request.session['username']
        feed_form = feedback_form({'feedback_name':username,'feedback_comment':voice_text})
    return render(request,'ocrapp/feedback.html',{'feedback_form':feed_form})

def feedback_hindi(request):
    if request.method == 'POST':
        feed_form = feedback_form(request.POST)

        if feed_form.is_valid():
            feed_form.save()

            return redirect("http://beginners.pythonanywhere.com/")


    else:
        def spch():

            with sr.Microphone() as source:
                print("SAY SOMETHING")
                audio = r.listen(source)
                print("TIME OVeR. THANKS")
            text = r.recognize_google(audio, language='hi-IN')
            return text

        voice_text = spch()
        username = request.session['username']
        feed_form = feedback_form({'feedback_name':username,'feedback_comment':voice_text})
    return render(request,'ocrapp/feedback.html',{'feedback_form':feed_form})


@login_required
def photo(request):
    if request.method == 'POST':
        #uploading images
        #im_form = photo_form({'im_username':request.session['username']},request.POST, request.FILES)
        im_form = photo_form(request.POST, request.FILES)
        if im_form.is_valid():
            im_form.save()
            #extracting the file name of the image being uploaded
            for filename, file in request.FILES.items():
                f_name = request.FILES[filename].name

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path =  os.path.join(BASE_DIR, 'media/images/')
            final_path = os.path.join(path,f_name)
            #path_im = resizeAndCrop(final_path)
            #im_path = os.path.abspath(path_im)



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
        try:
            #extracting text out of the document
            test_file = ocr_space_file(filename=final_path, language='eng')
            test_file = test_file[test_file.index('"ParsedText":')+14:test_file.index('","ErrorMessage"')]
            result = test_file.split('\\r\\n')

            for word in result:
                if word.find("DOB") != -1:
                    request.session['doc_type'] = "aadhar"
                if re.search("INCOME|TAX|Permanent", word):
                    request.session['doc_type'] = "pan"

            if request.session['doc_type'] == 'aadhar':
                request.session['doc_name'] = result[2]
                #request.session['doc_id'] = result[5]
                #request.session['doc_dob'] = result[3].split(':')[1]
                for i in result:
                    x = re.search('DOB', i)
                    if x:
                        request.session['doc_dob'] = i.split(':')[1]
                        break
                    else:
                        request.session['doc_dob'] = "Enter your DOB"
                for i in result:
                    y = re.search('([0-9]{4} ){2}', i)
                    if y:
                        request.session['doc_id'] = i
                        break
                    else:
                        request.session['doc_id'] = "Enter your UIDAI ID"



            #if request.session['doc_type'] == 'pan':
                #request.session['doc_name'] = result[5]
                #request.session['doc_id'] = result[3]
                #request.session['doc_dob'] = result[9]
            if request.session['doc_type'] == 'pan':
                #PAN NUMBER
                for i in result:
                    x_id = re.search('([A-Z]{5}[0-9]{4}[A-Z])', i)
                    if x_id:
                        request.session['doc_id'] = i
                        break
                    else:
                        request.session['doc_id'] = "Enter your PAN ID"
                #DOB
                for i in result:
                    x_dob = re.search('(/[0-9]{2})|(1[0-9]{2})', i)
                    if x_dob:
                        request.session['doc_dob'] = i
                        break
                    else:
                        request.session['doc_dob'] = "Enter your DOB"

                #NAME
                c = re.search('[A-Z0-9]{10}', result[5])
                if c:
                    request.session['doc_name'] = result[1]
                else:
                    request.session['doc_name'] = result[5]


            #displaying the extracted details on the webpage
            return redirect("http://beginners.pythonanywhere.com/ocrapp/aadhar")
            #return render(request,'ocrapp/result.html',{'f_name':result,'im_name':im_name})
            #return redirect('index')
        except:
            pass
        else:
            return render(request,'ocrapp/verify.html',)
    else:
        im_form = photo_form()
    return render(request,'ocrapp/index.html',{'im_form':im_form})


@login_required
def community_form_view(request):
    if request.method == 'POST':
        c_form = community_form(request.POST,request.FILES)
        if c_form.is_valid():
            c_form.save()
            return redirect('http://beginners.pythonanywhere.com/')
    else:
        username = request.session['username']
        c_form = community_form({'name':username})
        return render(request,'ocrapp/comm_post_page.html',{'c_form':c_form,'name':username})


'''def community_filter(request):
    if request.method === 'POST':


    else:
        return render(request,'ocrapp/about.html')

'''
@login_required
def investor_view(request):
    investor_list = []
    sub_list = []
    posts = community.objects.order_by('tag')
    sub_data = sub.objects.order_by('sub_status')
    for x in sub_data:
        sub_list.append(x)
    for entry in posts:
        if entry.tag == 'investor':
                    investor_list.append(entry)

    sub_new_list = []
    for sub_try in sub_list:
        if sub_try.sub_status == 1 :
            for post in investor_list:
                if post.amount <= 100000:
                    sub_new_list.append(post)
    return render(request,'ocrapp/investor.html',{'investor_list':investor_list,'sub':set(sub_new_list)})

@login_required
def investee_view(request):
    investee_list = []
    sub_list = []
    posts = community.objects.order_by('tag')
    sub_data = sub.objects.order_by('sub_status')
    for x in sub_data:
        sub_list.append(x)
    for entry in posts:
        if entry.tag == 'investee':
                    investee_list.append(entry)
    sub_new_list = []
    for sub_try in sub_list:
        if sub_try.sub_status == 1 :
            for post in investee_list:
                if post.amount <= 100000:
                    sub_new_list.append(post)
    return render(request,'ocrapp/investee.html',{'investee_list':investee_list,'sub':set(sub_new_list)})

@login_required
def sub_view(request):
    if request.method == "POST":
        s_form = sub_form(request.POST)
        if s_form.is_valid():
            s_form.save()
            return render(request,'ocrapp/home.html')

    else:
        s_form = sub_form()
        return render(request,'ocrapp/home.html',{'sub_form':s_form})
