#coding=utf8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from forms import *
from django.db.models import Q
from PIL import Image
def redirect_to_index(fn):
    def login_check(request,*args):
        if 'userid' in request.session:
            messages.info(request,"您已登陆")
            return HttpResponseRedirect('/index/')
        else:
            return fn(request,*args)
    return login_check
def login_required(fn):
    def login_check(request,*args):
        if 'userid' in request.session:
            return fn(request,*args)
        else:
            messages.warning(request,"请先登陆")
            return HttpResponseRedirect('/login/')
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
                messages.success(request,"注册成功")
                return HttpResponseRedirect('/index/')
        else:
            form = CreateTutor(request.POST)
            if form.is_valid():
                tutor = form.save()
                request.session['userid'] = tutor.userid
                request.session['identity'] = "t"
                messages.success(request,"注册成功")
                return HttpResponseRedirect('/index/')
    else:
        form = BaseCreateForm()
    return render(request, "register.html", {'form':form})
@csrf_exempt
@redirect_to_index
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if request.POST.get('identity') == "tutor":
            if form.is_valid():
                username = request.POST.get('username')
                try:
                    tutor = Tutor.objects.get(username=username)
                    if(tutor.password==request.POST.get('password')):
 			request.session['userid'] = tutor.userid
                	request.session['identity'] = "t"
                        return HttpResponseRedirect('/index/')
                    else:
                        messages.error(request,"用户名或密码错误")
                except Tutor.DoesNotExist:
                    messages.error(request,"该用户不存在")
        else:
            if form.is_valid():
                username = request.POST.get('username')
                try:
                    parent = Parent.objects.get(username=username)
                    if(parent.password==request.POST.get('password')):
			request.session['userid'] = parent.userid
                	request.session['identity'] = "p"
                        return HttpResponseRedirect('/index/')
                    else:
                        messages.error(request,"用户名或密码错误")
                except Parent.DoesNotExist:
                    messages.error(request,"该用户不存在")
    else:
        form = LoginForm()
    return render(request, "login.html", {'form':form})
@csrf_exempt
@login_required
def logout(request):
    if request.method == "POST":
	if "yes" in request.POST:	
    	    del request.session["userid"]
    	    del request.session["identity"]
	    messages.success(request,"退出成功")
	    return HttpResponseRedirect("/login/")
	else:
	    return HttpResponseRedirect("/index/")
    return render(request,"logout.html")
#parent
@login_required
def index(request):	
    userid = request.session["userid"]
    if request.session['identity'] == 'p':
 	user = Parent.objects.get(userid = userid)
	if user.receivecomment.count()>2:
	    tpcomment = user.receivecomment.all()[:2]
	else:
	    tpcomment = user.receivecomment.all()
	if user.receivemessage.count()>2:
	    tpmessage = user.receivemessage.all()[:2]
	else:
	    tpmessage = user.receivemessage.all()
    	username = user.username
    	return render(request,'pindex.html' ,locals())
    else:
	user = Tutor.objects.get(userid = userid)
	username = user.username
        return render(request,'tindex.html' ,locals())
@csrf_exempt
@login_required
def myinfo(request):
    identity = request.session['identity']
    userid = request.session["userid"]
    if request.session["identity"] == "p":
	user = Parent.objects.get(userid=userid)
    	if request.method=="POST":
            form = ParentForm(request.POST,instance=user)
            if form.is_valid() and form.has_changed():
               form.save()
    	else:
            form = ParentForm(instance=user)
        return render(request,'pinfo.html',locals())
    else:
	user = Tutor.objects.get(userid=userid)
    	if request.method=="POST":
            form = TutorForm(request.POST,instance=user)
            if form.is_valid() and form.has_changed():
               form.save()
    	else:
            form = TutorForm(instance=user)
        return render(request,'tinfo.html',locals())
@csrf_exempt
@login_required
def uploadimage(request):
    userid = request.session["userid"]
    identity = request.session['identity']
    if request.method == 'POST':       
        if 'image' in request.FILES:
            image=request.FILES["image"]
            img=Image.open(image)
            img.thumbnail((112,54),Image.ANTIALIAS)
            name='./Tutor/static/image/'+str(identity)+str(userid)+'.png'
            img.save(name,"png")
	    messages.success("图片上传成功")
            return HttpResponseRedirect("/index/")
    return render(request,'image.html')
@csrf_exempt
@login_required
def search(request):
    userid = request.session["userid"]
    identity = request.session['identity']
    if identity == "p":
	user = Parent.objects.get(userid=userid)
	dict_subject = []
	for tutor in Tutor.objects.all():
	     if tutor.subject.count()>2:
	         dict_subject.append((tutor,tutor.subject.all()[:2]))
	     else:
		 dict_subject.append((tutor,tutor.subject.all())) 	
	if request.method == "POST":
	    grade=request.POST.get('grade')
	    subjectlist = request.POST.getlist('subject')
	    if grade!='N' and subjectlist:	    
		tutorset = Tutor.objects.filter(subject__grade=grade,subject__subject__in=subjectlist)		
	    elif grade!='N':
		tutorset = Tutor.objects.filter(subject__grade=grade)
	    elif subjectlist:
		tutorset = Tutor.objects.filter(subject__subject__in=subjectlist)
	    else:
		tutorset = Tutor.objects.order_by('-score')
	    if 'content' in request.POST:
	        content = request.POST.get('content')
		tutorset = tutorset.filter(username__contains=content)
	    if request.POST.get('gender')!='N':
		tutorset = tutorset.filter(gender=request.POST.get('gender'))
	    dict_subject = []
	    for tutor in tutorset:
		if tutor.subject.count()>2:
	     	    dict_subject.append((tutor,tutor.subject.all()[:2]))
	        else:
		    dict_subject.append((tutor,tutor.subject.all())) 		
        return render(request,'psearch.html',locals())
    else:
	user = Tutor.objects.get(userid=userid)
	return render(request,'tsearch.html',locals())
@csrf_exempt
@login_required
def publishform(request):
    if Tutor.objects.count()>5:
    	tutors = Tutor.objects.all()[:5]
    else:
	tutors = Tutor.objects.all()
    userid = request.session['userid']
    identity = request.session['identity']
    if identity == 't':
	messages.warning(request,"您没有该功能!")
	return HttpResopnseRedirect('/index/')
    user = Parent.objects.get(userid=userid)
    if request.method == 'POST':
	if "delete" in request.POST:
	     Employ.objects.get(id=request.POST.get("delete")).delete()
	     form = EmployForm()
	     messages.success(request,"删除成功")
	else:
	    form = EmployForm(request.POST)
	    if form.is_valid():
	        employ = form.save()
	        employ.parent = user
	        employ.save()
		if employ.subject.all():
		    print "hello"
		else:
		    print 'I am here'
    	        messages.success(request,"发布成功")
		form = EmployForm()
    else:
	form = EmployForm()
    if user.employ_set.count()>4:
	forms = user.employ_set.all()[:4]
    else:
	forms = user.employ_set.all()
    dict_subject = []
    for fm in forms:
	if fm.subject.count()>2:
	    dict_subject.append((fm,fm.subject.all()[:2]))
        else:
	    dict_subject.append((fm,fm.subject.all()))
    return render(request,"publishform.html",locals())
@csrf_exempt
@login_required
def message(request):
    userid = request.session['userid']
    identity = request.session['identity']
    if identity == "p":
	user = Parent.objects.get(userid=userid)
	tpmessage = user.receivemessage.all()
        tpcomment = user.receivecomment.all()
	if Tutor.objects.count()>5:
    	    tutors = Tutor.objects.all()[:5]
        else:
	    tutors = Tutor.objects.all()
	if request.method == 'POST':
	    if "delete" in request.POST:
	        messages.success(request,"删除成功")
	if user.employ_set.count()>4:
            forms = user.employ_set.all()[:4]
        else:
	    forms = user.employ_set.all()
        dict_subject = []
        for fm in forms:
	    if fm.subject.count()>2:
	        dict_subject.append((fm,fm.subject.all()[:2]))
            else:
	        dict_subject.append((fm,fm.subject.all()))	
	return render(request,"pmessage.html",locals())
    else:
	user = Tutor.objects.get(userid=userid)
	return render(request,"tmessage.html",locals())
    
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
