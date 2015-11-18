#coding=utf8
from django.shortcuts import render,render_to_response
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from models import Parent,Tutor,Subject,TPMessage,PTMessage,PTComment,TPComment,Employ
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
#from forms import LoginForm,RegisterForm,parent_form
from forms import CreateTutor, CreateParent, LoginForm, parent_form,tutor_form,employ_form
from django.db.models import Q

def redirect_to_index(fn, url="../index/"):
    def login_check(request,*args):
        if 'userid' in request.session:
            userid = request.session['userid']
            identity = request.session['identity']
            if identity == 'p':
                return HttpResponseRedirect('/index_parent')
            if identity == 't':
                return HttpResponseRedirect('/index_tutor')
        else:
            return fn(request,*args)
    return login_check
def login_required(fn,url="../login"):
    def login_check(request,*args):
        if 'userid' in request.session:
            return fn(request,*args)
        else:
            return HttpResponseRedirect(url)
    return login_check
@csrf_exempt
@redirect_to_index
def register(request):
    if request.method == 'POST':
        identity = request.POST.get("identity")
        if identity == "parent":
            form = CreateParent(request.POST)
            if form.is_valid():
                parent = form.save()
                request.session['userid'] = parent.userid
                request.session['identity'] = "p"
                return HttpResponseRedirect('/index_parent/')
            return render(request, "register.html", {'form':form})
        else:
            form = CreateTutor(request.POST)
            if form.is_valid():
                #return HttpResponse('tutor')
                tutor = form.save()
                request.session['userid'] = tutor.userid
                request.session['identity'] = "t"
                
                return HttpResponseRedirect('/index_tutor/')
        
            return render(request, "register.html", {'form':form})
    else:
        form = CreateTutor()
    return render(request, "register.html", {'form':form})
@csrf_exempt
@redirect_to_index
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if request.POST.get('identity') == "tutor":
            if form.is_valid():
                username = request.POST.get('username')
                tutor_list = Tutor.objects.filter(username=username)
                
                if tutor_list:
                    tutor = Tutor.objects.get(username=request.POST.get('username'))
                    
                    if request.POST.get("password") == tutor.password:
                        #return HttpResponse('tutor')
                        request.session["userid"] = tutor.userid
                        
                        request.session["identity"] = "t"
                        
                        return HttpResponseRedirect('/index_tutor/')
                    else:
                        errors = "用户名或密码不正确!"
                        return render(request, "login.html", {'form':form,"errors":errors})
                else:
                    errors = "用户名不存在"
                    return render(request, "login.html", {'form':form,"errors":errors})
        else:
            if form.is_valid():
                username = request.POST.get('username')
                parent_list = Parent.objects.filter(username=username)
                if parent_list:
                    parent = Parent.objects.get(username=request.POST.get('username'))
                    if request.POST.get('password') == parent.password:
                        request.session["userid"] = parent.userid
                        request.session["identity"] = "p"
                        return HttpResponseRedirect('/index_parent/')
                    else:
                        errors =  "用户名或密码错误"
                        return render(request, "login.html", {'form':form,"errors":errors})
                else:
                    errors = "用户名不存在"
                    return render(request, "login.html", {'form':form,"errors":errors})
    else:
        form = LoginForm()
    
    return render(request, "login.html", {'form':form})

"""
@login_required
def index(request):
    if request.method == "POST":
        if "logout" in request.POST:
            del request.session["userid"]
            del request.session["identity"]
            return HttpResponse("You log out successfully!")
    identity = request.session["identity"]
    userid = request.session["userid"]
    if identity == 'p':
        current_parent = Parent.objects.get(userid=userid)
        return render(request, "index.html", {"parent":current_parent,"comments":current_parent.receivecomment.all(),
                                              "messages":current_parent.receivemessage.all()})
    else:
        current_tutor = Tutor.objects.get(userid=userid)
        return render(request, "index.html", {"username":current_tutor.username})
"""

    

@csrf_exempt
@login_required
def logout(request):
    userid = request.session["userid"]
    identity = request.session["identity"]
    if request.method == "POST":
        if "logout" in request.POST:
            select = request.POST['logout']
            if select == "yes":
                del request.session["userid"]
                del request.session["identity"]
                return HttpResponse("You log out successfully!")
            else:
                if identity == "p":
                    return HttpResponseRedirect('/index_parent/')
                else:
                    return HttpResponseRedirect('/index_tutor/')
    return render_to_response('logout.html')

"""
    identity = request.session["identity"]
    userid = request.session["userid"]
    if identity == 'p':
        current_parent = Parent.objects.get(userid=userid)
        return render(request, "index.html", {"parent":current_parent,"comments":current_parent.receivecomment.all(),
                                              "messages":current_parent.receivemessage.all()})
    else:
        current_tutor = Tutor.objects.get(userid=userid)
        return render(request, "index.html", {"username":current_tutor.username})
"""
        

#parent
@login_required
def index_parent(request):
    userid = request.session["userid"]
    username = Parent.objects.get(userid = userid).username
    
    return render_to_response('index_parent.html' ,{'username':username})
    
@csrf_exempt
@login_required
def myinfo_parent(request):
    userid = request.session["userid"]
    user = Parent.objects.get(userid = userid)
    if request.method == "POST":
        pf = parent_form(request.POST)
        try:
            if pf.is_valid():
                user.realname = pf.cleaned_data['realname']
                user.email = pf.cleaned_data['email']   
                #user.gender = gender
                user.age = int(pf.cleaned_data['age'])
                user.qq = int(pf.cleaned_data['qq'])
                user.phone = int(pf.cleaned_data['phone'])
                user.address = pf.cleaned_data['address']
                user.information = pf.cleaned_data['information']
                user.save()        
                return render_to_response('myinfo_parent.html',{'username':user.username,'user':user})
        except:
            return render_to_response('myinfo_parent.html',{'username':user.username,'user':user})
    return render_to_response('myinfo_parent.html',{'username':user.username,'user':user})


@csrf_exempt
@login_required
def search_tutor(request):
    userid = request.session["userid"]
    username = Parent.objects.get(userid = userid).username
    if request.method == "GET" and 'q' in request.GET:
        q = request.GET['q']
        if q:
            select = request.GET['select']
            if select == '0':
                tutors = Tutor.objects.filter(username__startswith = q)
            if select == '1':
                tutors = Tutor.objects.filter(realname__startswith = q)
            if select == '2':
                tutors = Tutor.objects.filter(university__startswith = q)
            if select == '3':
                tutors = Tutor.objects.filter(userid = q)
            if len(tutors):
                return render_to_response('search_tutor.html',{'username':username,'sucess':True,'tutors':tutors})
            else:
                error = '未查询到此用户!'
                return render_to_response('search_tutor.html',{'username':username,'error': error,'sucess':False})
        else:
            error = '请输入要查询的信息!'
            return render_to_response('search_tutor.html',{'username':username,'error': error})
    if request.method == "POST":
        if 'grade' in request.POST and 'subject' in request.POST and 'gender' in request.POST:
            grade = request.POST.get('grade')
            subject = request.POST.get('subject')
            gender = request.POST.get('gender')
            if len(grade) and len(subject) and len(gender):
                try:
                    tutors = Subject.objects.get(Q(grade = grade),Q(subject = subject))
                    tutors = tutors.tutor_set.all()
                    if gender == 'N':
                        if tutors:
                            return render_to_response('search_tutor.html',{'username':username,'sucess':True,'tutors':tutors})
                        else:
                            error = '未查询到符合条件的用户!'
                            return render_to_response('search_tutor.html',{'username':username,'error': error})
                    else:
                        tutors = tutors.filter(gender = gender)
                        if tutors:
                            return render_to_response('search_tutor.html',{'username':username,'sucess':True,'tutors':tutors})
                        else:
                            error = '未查询到符合条件的用户!'
                            return render_to_response('search_tutor.html',{'username':username,'error': error})
                except:
                    error = '未查询到符合条件的用户!'
                    return render_to_response('search_tutor.html',{'username':username,'error': error})
        else:
            error = "请输入完整的筛选信息!"
            return render_to_response('search_tutor.html',{'username':username,'error': error})
    error = "请选择一种查询方式查询"
    return render_to_response('search_tutor.html',{'username':username,'error': error})

@csrf_exempt
@login_required
def employ_tutor(request):
    userid = request.session["userid"]
    username = Parent.objects.get(userid = userid).username
    if request.method == 'POST':
        ef = employ_form(request.POST)
        if ef.is_valid():
            parent = Parent.objects.get(userid = userid)
            gender1 = ef.cleaned_data['gender1']
            age = ef.cleaned_data['age']
            subject = ef.cleaned_data['subject']
            grade = ef.cleaned_data['grade']
            info1 = ef.cleaned_data['info1']
            gender2 = ef.cleaned_data['gender2']
            info2 = ef.cleaned_data['info2']
            way = ef.cleaned_data['way']
            site = ef.cleaned_data['site']
            time = ef.cleaned_data['time']
            salary = ef.cleaned_data['salary']
            linkman = ef.cleaned_data['linkman']
            phone =  ef.cleaned_data['phone'],
            info3 = ef.cleaned_data['info3']
            #return HttpResponse('sucess')
            employ = Employ.objects.create(
                parent = parent,gender1 = gender1,
                age = age,
                subject = subject,grade = grade,
                info1 = info1,gender2 = gender2,
                info2 = info2,
                way = way,site = site,
                time = time,salary = salary,
                linkman = linkman,phone =  phone,
                info3 = info3
                )
            employ.save()
    return render_to_response('employ_tutor.html',{'username':username})

@login_required
def message_parent(request):
    userid = request.session["userid"]
    username = Parent.objects.get(userid = userid).username
    user = Parent.objects.get(username = username)
    tpm = TPMessage.objects.filter(to_user = user)
    ptm = PTMessage.objects.filter(from_user = user)
    return render_to_response('message_parent.html',{'username':username,'TPMessage':tpm,'PTMessage':ptm})

@login_required
def comment_parent(request):
    userid = request.session["userid"]
    username = Parent.objects.get(userid = userid).username
    user = Parent.objects.get(username = username)
    tpc = TPComment.objects.filter(to_user = user)
    ptc = PTComment.objects.filter(from_user = user)
    return render_to_response('comment_parent.html',{'username':username,'PTComment':ptc,'TPComment':tpc})

@login_required
def index_tutor(request):
    userid = request.session["userid"]
    username = Tutor.objects.get(userid = userid).username
    
    return render_to_response('index_tutor.html' ,{'username':username})

@login_required
def message_tutor(request):
    userid = request.session["userid"]
    username = Tutor.objects.get(userid = userid).username
    user = Tutor.objects.get(username = username)
    tpm = TPMessage.objects.filter(from_user = user)
    ptm = PTMessage.objects.filter(to_user = user)
    return render_to_response('message_tutor.html',{'username':username,'TPMessage':ptm,'PTMessage':tpm})

@login_required
def comment_tutor(request):
    userid = request.session["userid"]
    username = Tutor.objects.get(userid = userid).username
    user = Tutor.objects.get(username = username)
    tpc = TPComment.objects.filter(from_user = user)
    ptc = PTComment.objects.filter(to_user = user)
    return render_to_response('comment_tutor.html',{'username':username,'PTComment':ptc,'TPComment':tpc})


@csrf_exempt
@login_required
def myinfo_tutor(request):
    userid = request.session["userid"]
    user = Tutor.objects.get(userid = userid)
    if request.method == "POST":
        tf = tutor_form(request.POST)
        try:
            if tf.is_valid():
                user.realname = tf.cleaned_data['realname']
                user.email = tf.cleaned_data['email']   
                #user.gender = gender
                user.age = int(tf.cleaned_data['age'])
                user.qq = int(tf.cleaned_data['qq'])
                user.phone = int(tf.cleaned_data['phone'])
                user.major = tf.cleaned_data['major']
                user.university = tf.cleaned_data['university']
                user.information = tf.cleaned_data['information']
                #return HttpResponse(user.information)
                user.save()        
                return render_to_response('myinfo_tutor.html',{'username':user.username,'user':user})
        except:
            return render_to_response('myinfo_tutor.html',{'username':user.username,'user':user})
    return render_to_response('myinfo_tutor.html',{'username':user.username,'user':user})

@csrf_exempt
@login_required
def tutor(request,i):
    username = i
    userid = request.session["userid"]
    user = Parent.objects.get(userid = userid)
    tutor = Tutor.objects.get(username = username)
    if request.method == "POST":
        comment = request.POST['comment']
        ptm = PTMessage.objects.create(from_user = user,to_user = tutor,content = comment)
        
    return render_to_response('tutor.html',{'username':user.username,'tutor':tutor})

@csrf_exempt
@login_required
def parent(request,i):
    username = i
    userid = request.session["userid"]
    user = Tutor.objects.get(userid = userid)
    tutor = Parent.objects.get(username = username)
    if request.method == "POST":
        message = request.POST['message']
        ptm = TPMessage.objects.create(from_user = user,to_user = tutor,content = message)
        
    return render_to_response('parent.html',{'username':user.username,'tutor':tutor})
