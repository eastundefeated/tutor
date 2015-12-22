#coding=utf8
from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from forms import *
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
import datetime
import hashlib
university_dict = {}
for item in university_choice:
    university_dict[item[0]] = item[1]
university_choice = (("001","哈尔滨工业大学"), ("002","哈尔滨工程大学"),("003","东北林业大学"),("004","黑龙江大学"),
                    ("005","哈尔滨理工大学"),("006","东北农业大学"),("007","哈尔滨医科大学"),("008","黑龙江中医药大学"),
                    ("010","哈尔滨师范大学"),("011","哈尔滨商业大学"),("012","哈尔滨学院"),("013","黑龙江工程学院"),
                    ("014","黑龙江科技学院"),("015","哈尔滨德强商务学院"),("016","哈尔滨体育学院"),("017","黑龙江东方学院"),)
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
	    request.session['next'] = request.path
            return HttpResponseRedirect('/login/')
    return login_check
#忘记密码
@csrf_exempt
def forgetPassword(request):
    if request.method == "POST":
	mail = request.POST.get("email")
	try:
	    user = User.objects.get(email=mail)
	except User.DoesNotExist:
	    return HttpResponse("<h1>Invalid email!</h1>")
	url = "http://localhost:8000/setpassword/"+str(user.userid)+"/"+hashlib.md5(str(user.password)).hexdigest()+"/"
	content = u"<html><body>尊敬的%s,请复制该链接或直接点击打开来完成重置密码<a href=%s>%s</a></body></html>"%(user.username,url,url)
	msg = EmailMultiAlternatives("重置密码",content,"2770837735@qq.com",[mail])
        msg.attach_alternative(content, "text/html")
	msg.send()
	return HttpResponse("<h1>验证邮件已发往您的邮箱!</h1>")
    return render(request,"forgetpassword.html")
#邮箱验证
def activeMail(request,userid,password):
    print "there"
    user = get_object_or_404(User,userid=userid)
    print "here"
    if hashlib.md5(str(user.password)).hexdigest() == password and not user.is_active:
        user.is_active = True
	user.save()
	request.session['userid'] = userid
	messages.success(request,"邮箱验证成功")
	return HttpResponseRedirect('/index/')
    else:
	return HttpResponseRedirect('/')
#重置密码
@csrf_exempt
def resetPassword(request,userid,password):
    user = get_object_or_404(User,userid=userid)
    if hashlib.md5(str(user.password)).hexdigest() == password:
        if request.method == "POST":
	    form = PasswordReset(request.POST)
	    if form.is_valid():
		user.password = request.POST.get('password1')
		user.save()
		request.session['userid'] = userid
		messages.success(request,"密码重置成功")
		return HttpResponseRedirect('/index/')
        else:
	    form = PasswordReset()
	return render(request,"password.html",locals())
    else:
	return HttpResponseRedirect('/')
#修改密码
@csrf_exempt
@login_required
def changePassword(request):
    user = User.objects.get(userid=request.session['userid'])
    if request.method == "POST":
	form = PasswordChange(request.POST)
	if form.is_valid():
	    if user.password==form.cleaned_data.get("password_orgin"):
		user.password = request.POST.get('password1')
		user.save()
		messages.success(request,"修改密码成功")
		return HttpResponseRedirect('/index/')
	    else:
		messages.error(request,"原始密码错误")
    else:
	form = PasswordChange()
    return render(request,"password.html",locals())

#表单是否可见
def changeFormState():
    for employ in Employ.objects.filter(is_visible=True):
	if employ.pub_date.replace(tzinfo=None) + datetime.timedelta(days=employ.valid_days) < datetime.datetime.now():
	    employ.is_visible = False
    for askemploy in AskEmploy.objects.filter(is_visible=True):
	if askemploy.pub_date.replace(tzinfo=None) + datetime.timedelta(days=askemploy.valid_days) < datetime.datetime.now():
	    askemploy.is_visible = True
@csrf_exempt
@redirect_to_index
def register(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
	    user.has_image = False
	    user.save()
            url = "http://localhost:8000/activemail/"+str(user.userid)+"/"+hashlib.md5(user.password).hexdigest()+"/"
	    content = u"<p>尊敬的%s,请复制该链接或直接点击打开来完成激活<a href=%s>%s</a></p>"%(user.username,url,url)
	    msg = EmailMultiAlternatives("激活邮件",content,"2770837735@qq.com",[form.cleaned_data.get("email")])
	    msg.send()
	    return HttpResponse("<h2>邮件已经发送到您的邮箱</h2>")
    else:
        form = CreateForm()
    return render(request, "register.html", {'form':form})
def mainpage(request):
    user = False
    if "userid" in request.session:
	user = User.objects.get(userid=request.session['userid'])
    tutors = User.objects.filter(identity=False).order_by("-score")[:5] if User.objects.filter(identity=False).count()>5 else User.objects.filter(identity=False).order_by("-score")
    exps = Exp.objects.order_by("-pub_date")[:5] if Exp.objects.count()>5 else Exp.objects.order_by("-pub_date")
    subject_c = {"Math":0,"English":0,"Chinese":0,"Physic":0,"Chemistry":0,"Biology":0}
    for key in subject_c.keys():
	subject_c[key] = Employ.objects.filter(subject__subject__in = [key]).count()
    subject_count = subject_c.items()
    subject_count.sort(key = lambda x:x[1],reverse=True)
    date_count = []
    for i in range(1,8):
	date_count.append((i,Employ.objects.filter(pub_date__week_day=i).count()))
    date_count.sort(key = lambda x:x[1],reverse=True)
    return render(request,"mainpage.html",locals())
@csrf_exempt
@redirect_to_index
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
                username = request.POST.get('username')
                try:
                    user = User.objects.get(username=username)
                    if user.password==request.POST.get('password'):
			if user.is_active:
			    request.session['userid'] = user.userid
                            if 'next' in request.session:
		    		url = request.session['next']
		    		del request.session['next']
			    else:
		    		url = '/index/'
			    return HttpResponseRedirect(url)
			else:
			    messages.warnning(request,"该用户未被激活")
                    else:
                        messages.error(request,"用户名或密码错误")
                except User.DoesNotExist:
                    messages.error(request,"该用户不存在,请先注册")
    else:
        form = LoginForm()
    return render(request, "login.html", {'form':form})
@csrf_exempt
@login_required
def logout(request):
    if request.method == "POST":
	if "yes" in request.POST:
    	    del request.session["userid"]
	    messages.success(request,"退出成功")
	    return HttpResponseRedirect("/")
	else:
	    return HttpResponseRedirect("/index/")
    return render(request,"logout.html")


#个人主页
@login_required
def index(request):
    global university_dict
    changeFormState()
    user = User.objects.get(userid=request.session['userid'])
    identity = user.identity
    hirecount = user.hire_to.count()
    commentcount = user.receivecomment.filter(is_read=False).count()
    messagecount = user.receivemessage.filter(is_read=False).count()
    if identity:
	forms = AskEmploy.objects.filter(is_visible=True).order_by("-pub_date")[:5] if AskEmploy.objects.filter(is_visible=True).count()>5 else AskEmploy.objects.filter(is_visible=True).order_by("-pub_date")
	if user.employ_set.exists():
	    employ = user.employ_set.latest("pub_date")
	    if employ.subject.exists():
		tutorset = employ.subject.all()[0].user_set.filter(identity=False,state='F')
	    	for subject in employ.subject.all():
		    tutorset = tutorset | subject.user_set.filter(identity=False,state='F')
	    if employ.gender2 != "N":
		tutorset = tutorset.filter(gender=employ.gender2)
	    tutorset = tutorset.order_by("-score").distinct()
	else:
	    tutorset = User.objects.filter(identity=False,state='F').order_by("-score").distinct()
	tutorset = tutorset[:5] if tutorset.count()>5 else tutorset
    else:
	if user.askemploy_set.exists():
	    employ = user.askemploy_set.latest("pub_date")
	    if employ.subject.exists():
		forms = employ.subject.all()[0].employ_set.filter(is_visible=True)
	    	for subject in employ.subject.all():
		    forms = forms | subject.employ_set.filter(is_visible=True)
	    forms = forms.distinct()
	else:
	    forms = Employ.objects.filter(is_visible=True).order_by("-pub_date").distinct()
	forms = forms[:5] if forms.count()>5 else forms
	tutorset = User.objects.filter(identity=False).order_by("-score")[:5] if User.objects.filter(identity=False).count()>5 else User.objects.filter(identity=False).order_by("-score")
    dict_subject = []
    for form in forms:
        dict_subject.append((form,form.subject.all()))
    return render(request,'index.html' ,locals())
#个人资料
@csrf_exempt
@login_required
def myinfo(request):
    global university_dict
    user = User.objects.get(userid=request.session['userid'])
    identity = user.identity
    if identity:
    	if request.method=="POST":
            form = ParentForm(request.POST,instance=user)
            if form.is_valid() and form.has_changed():
                form.save()
	        messages.success(request,"修改成功")
    	else:
            form = ParentForm(instance=user)
    else:
    	if request.method=="POST":
            form = TutorForm(request.POST,instance=user)
            if form.is_valid() and form.has_changed():
                form.save()
		messages.success(request,"修改成功")
    	else:
            form = TutorForm(instance=user)
    return render(request,'info.html',locals())
#上传图片
@csrf_exempt
@login_required
def uploadimage(request):
    user = User.objects.get(userid = request.session["userid"])
    if request.method == 'POST':
        if 'image' in request.FILES:
            image=request.FILES["image"]
            img=Image.open(image)
            img.thumbnail((200,180),Image.ANTIALIAS)
            name='./Tutor/static/image/'+str(user.userid)+'.png'
            img.save(name,"png")
	    messages.success(request,"图片上传成功")
	    user.has_image = True
	    user.save()
            return HttpResponseRedirect("/index/")
    return render(request,'image.html')
#家长搜索家教，以及家教发布的表单
#家教搜索家长发布的表单
@csrf_exempt
@login_required
def search(request):
    user = User.objects.get(userid=request.session['userid'])
    identity = user.identity
    form = searchAskEmployForm() if user.identity else searchEmployForm()
    forms = AskEmploy.objects.filter(is_visible=True).order_by("-pub_date") if user.identity else Employ.objects.filter(is_visible=True).order_by("-pub_date")       
    url = "" 
    if request.method == "GET":
        for key,value in request.GET.items():
	    if key!="page":
	        url+="&"+key+"="+value
	if "pub_date" in request.GET and request.GET.get('pub_date') != "all":
	    forms = forms.filter(pub_date__gte=datetime.datetime.now()-datetime.timedelta(days=1)) if request.POST.get('pub_date') == "day" else forms.filter(pub_date__gte=datetime.datetime.now()-datetime.timedelta(days=7))
	if "gender" in request.GET and not user.identity and request.GET.get('gender')!='N':
	    forms = forms.filter(Q(gender2=request.GET.get('gender'))|Q(gender2='N'))
       	forms = forms.filter(subject__subject__in=request.GET.getlist('subject')) if 'subject' in request.GET and request.GET.getlist('subject') else forms
	forms = forms.filter(subject__grade=request.GET.get('grade')) if "grade" in request.GET and request.GET.get('grade')!='N' else forms
	if 'salary' in request.GET and request.GET.get('salary') != 'N':
	    if request.GET.get('salary') == '0':
		forms = forms.filter(salary__lte=50.0)
	    else:
		if request.GET.get('salary') == '1':
		    forms = forms.filter(salary__gt=50.0,salary__lte=100.0)
	        else:
		    forms = forms.filter(salary__gt=100.0)	
    paginator = Paginator(forms, 6) # Show 25 contacts per page
    page = request.GET.get('page','1')
    try:
        forms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        forms = paginator.page(1)
    except EmptyPage:
        forms = paginator.page(paginator.num_pages)
    return render(request,'search.html',locals())
@csrf_exempt
@login_required
def searchTutor(request):
    global university_dict
    user = User.objects.get(userid=request.session['userid'])
    tutorset = User.objects.filter(identity=False).order_by("-score")
    form = searchTutorForm()
    url = "" 
    if not user.identity:
	return HttpResponseRedirect("/index/")
    if request.method == "GET":
	for key,value in request.GET.items():
	    if key!="page":
	        url+="&"+key+"="+value
	fm = request.GET
        tutorset = tutorset.filter(username__icontains=request.GET.get('username')) if 'username' in request.GET and request.GET.get('username') else tutorset
	tutorset = tutorset.filter(gender=request.GET.get('gender')) if 'gender' in request.GET and request.GET['gender'] and request.GET['gender']!='N' else tutorset
	tutorset = tutorset.filter(subject__grade=request.GET['grade']) if 'grade' in request.GET and request.GET['grade'] and request.GET['grade']!='N' else tutorset
	tutorset = tutorset.filter(subject__subject__in=request.GET.getlist('subject')) if 'subject' in request.GET and request.GET.getlist('subject') else tutorset
    paginator = Paginator(tutorset, 6) # Show 25 contacts per page
    page = request.GET.get('page','1')
    try:
        tutors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tutors = paginator.page(1)
    except EmptyPage:
        tutors = paginator.page(paginator.num_pages)
    return render(request,"search_tutor.html",locals())
@csrf_exempt
@login_required
def publishform(request):
    global university_dict
    user = User.objects.get(userid=request.session['userid'])
    if request.method == "POST":
	if "delete" in request.POST:
	    form = EmployForm() if user.identity else AskEmployForm()
	    classname = Employ if user.identity else AskEmploy
	    try:
		classname.objects.get(id=request.POST.get('delete')).delete()        
		messages.success(request,"删除成功")
	    except classname.DoesNotExist:
		pass
	else:   
	    form = EmployForm(request.POST) if user.identity else AskEmployForm(request.POST)
	    if form.is_valid():
	        fm = form.save()
	        fm.user = user
	        fm.save()
	        messages.success(request,"表单发布成功")
    else:
	form = EmployForm() if user.identity else AskEmployForm()
    forms = Employ.objects.order_by("-is_visible").order_by("-pub_date").distinct() if user.identity else AskEmploy.objects.order_by("-is_visible").order_by("-pub_date").distinct()
    paginator = Paginator(forms, 6) # Show 25 contacts per page
    page = request.GET.get('page','1')
    try:
        forms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        forms = paginator.page(1)
    except EmptyPage:
        forms = paginator.page(paginator.num_pages)
    return render(request,"publishform.html",locals())
@csrf_exempt
@login_required
def message(request):
    user = User.objects.get(userid = request.session['userid'])
    if request.method == "POST" and "delete" in request.POST:
	try:
	    Message.objects.get(id=request.POST.get('delete'))
	    messages.success(request,"删除成功")
	except Message.DoesNotExist:
	    pass
    for m in Message.objects.filter(to_user=user,is_read=False).distinct():
	m.is_read = True
	m.save()
    mess = Message.objects.filter(to_user=user).order_by("-is_read").order_by("-pub_date")
    paginator = Paginator(mess, 6) 
    page = request.GET.get('page','1')
    try:
        mess = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mess = paginator.page(1)
    except EmptyPage:
        mess = paginator.page(paginator.num_pages)
    return render(request,"message.html",locals())    

@csrf_exempt
@login_required
def comment(request):
    user = User.objects.get(userid = request.session['userid'])
    for m in Comment.objects.filter(to_user=user,is_read=False).distinct():
	m.is_read = True
	m.save()
    mess = Comment.objects.filter(to_user=user).order_by("-is_read").order_by("-pub_date")
    paginator = Paginator(mess, 6) 
    page = request.GET.get('page','1')
    try:
        mess = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mess = paginator.page(1)
    except EmptyPage:
        mess = paginator.page(paginator.num_pages)
    return render(request,"comment.html",locals())    

def exp(request):
    user = False if not "userid" in request.session else User.objects.get(userid=request.session['userid'])
    mess = Exp.objects.order_by("-pub_date")
    paginator = Paginator(mess, 10) 
    page = request.GET.get('page','1')
    try:
        mess = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mess = paginator.page(1)
    except EmptyPage:
        mess = paginator.page(paginator.num_pages)
    return render_to_response("exp.html",locals())

@csrf_exempt
@login_required
def share(request):
    user = User.objects.get(userid=request.session['userid'])
    if request.method == "POST":
	if "delete" in request.POST:
	    try:
	        Exp.objects.get(id=request.POST.get('delete')).delete()
	        messages.success(request,"删除成功")
	    except Exp.DoesNotExist:
		pass
	elif "save" in request.POST:
    	    form = ExpForm(request.POST)
	    if form.is_valid():
	        exp = form.save()
	        exp.user = user
 	        exp.save()
	        messages.success(request,"发表成功!")
    else:
	form = ExpForm()
    forms = Exp.objects.filter(user=user).order_by('-pub_date').distinct()
    paginator = Paginator(forms, 6) # Show 25 contacts per page
    page = request.GET.get('page','1')
    try:
        forms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        forms = paginator.page(1)
    except EmptyPage:
        forms = paginator.page(paginator.num_pages)
    return render_to_response("share.html",locals())
@csrf_exempt
def information(request,userid):
    global university_dict
    u = get_object_or_404(User,userid=userid)
    can_hire = False
    can_comment = False
    if "userid" in request.session:
	user = User.objects.get(userid=request.session['userid'])
        if user == u:
	    return HttpResponseRedirect("/index/")
	if not (u.identity and user.identity):
	    if user.identity and EmployRelationship.objects.filter(parent=user,tutor=u,is_valid=False,has_comment=False).exists():
		can_comment = True
	    elif (not user.identity) and EmployRelationship.objects.filter(parent=u,tutor=user,is_valid=False,has_comment=False).exists():
		can_comment = True
            else:
		pass
	    can_hire = True
	    if user.identity and EmployRelationship.objects.filter(parent=user,tutor=u,is_valid=True).exists():
		can_hire = False
	    elif (not user.identity) and EmployRelationship.objects.filter(parent=u,tutor=user,is_valid=True).exists():
	        can_hire = False
	    else:
		pass
	if request.method == "POST":
	    if "mess" in request.POST:
		Message.objects.create(content=request.POST.get("message"),is_read=False,from_user=user,to_user=u,pub_date=datetime.datetime.now())
		messages.success(request,"留言成功")
	    elif "hire" in request.POST:
		Hire.objects.create(is_read=False,from_user=user,to_user=u,pub_date=datetime.datetime.now())
		messages.success(request,"请求发送成功")
	    elif "comment" in request.POST and can_comment:
		form = CommentParentForm(request.POST) if user.identity else CommentParentForm(request.POST)
		fm = Comment()
		fm.content = request.POST.get("content")
		fm.from_user = user
		fm.is_read = False
		fm.to_user = u
                fm.score = request.POST.get("score") if user.identity else 0
		fm.pub_date = datetime.datetime.now()
		fm.save()
                if user.identity:
		    u.count_comment+=1
                    u.total_score+=int(request.POST.get("score"))
		    u.score = u.total_score*1.0/u.count_comment
		    u.save() 
		messages.success(request,"评论成功")
		e = EmployRelationship.objects.filter(parent=user,tutor=u,is_valid=False,has_comment=False)[0] if user.identity else EmployRelationship.objects.filter(parent=u,tutor=user,is_valid=False,has_comment=False)[0]
		e.has_comment = True
		e.save()
	else:
	    form = CommentTutorForm() if user.identity else CommentParentForm()
    else:
	user = False
    mess = Message.objects.filter(to_user=u).order_by("-pub_date")
    paginator = Paginator(mess, 6) 
    page = request.GET.get('page','1')
    try:
        mess = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mess = paginator.page(1)
    except EmptyPage:
        mess = paginator.page(paginator.num_pages)
    comments = Comment.objects.filter(to_user=u).order_by("-pub_date")
    paginator1 = Paginator(comments, 6) 
    page1 = request.GET.get('page1','1')
    try:
        comments = paginator1.page(page1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator1.page(1)
    except EmptyPage:
        comments = paginator1.page(paginator1.num_pages)
    return render(request,"information.html",locals())
@csrf_exempt
@login_required
def hire(request):
    user = User.objects.get(userid=request.session['userid'])
    hires = Hire.objects.filter(to_user=user).order_by("-pub_date")  
    if request.method == "POST":
	if 'ignore' in request.POST:
	    try:	    
		Hire.objects.get(id=request.POST.get("ignore")).delete()
                messages.success(request,"删除成功")
	    except Hire.DoesNotExist:
		pass
        elif "agree" in request.POST:
	    try:
		ask = Hire.objects.get(id=request.POST.get("agree"))
		if user.identity:
		    try:
			e = EmployRelationship.objects.get(parent=user,tutor=ask.from_user,is_valid=True)
			messages.info(request,"你们的雇佣关系已存在")
                    except EmployRelationship.DoesNotExist:
		       messages.success(request,"雇佣成功")
		       EmployRelationship.objects.create(parent=user,tutor=ask.from_user,is_valid=True,pub_date=datetime.datetime.now(),has_comment=False)
		else:
		    try:
                        e =EmployRelationship.objects.get(tutor=user,parent=ask.from_user,is_valid=True)
			messages.info(request,"你们的雇佣关系已存在")
                    except EmployRelationship.DoesNotExist:
                       messages.success(request,"雇佣成功")
		       EmployRelationship.objects.create(tutor=user,parent=ask.from_user,is_valid=True,pub_date=datetime.datetime.now(),has_comment=False)
		Hire.objects.get(id=request.POST.get("agree")).delete()		
	    except Hire.DoesNotExist:
		pass
        elif "deletehistory" in request.POST:
	    try:
		EmployRelationship.objects.get(id=request.POST.get("deletehistory")).delete()
	        messages.success(request,"删除成功")
            except EmployRelationship.DoesNotExist:
		pass
	elif "disable" in request.POST:
	    try:
		e = EmployRelationship.objects.get(id=request.POST.get("disable"))
		e.is_valid = False	        
		e.save()
		messages.success(request,"解除关系成功")
            except EmployRelationship.DoesNotExist:
		pass
	else:
	    pass
    paginator = Paginator(hires, 6) 
    page = request.GET.get('page','1')
    try:
        hires = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hires = paginator.page(1)
    except EmptyPage:
        hires = paginator.page(paginator.num_pages) 
    mess = EmployRelationship.objects.filter(parent=user).order_by("-is_valid").order_by("-pub_date") if user.identity else EmployRelationship.objects.filter(tutor=user).order_by("-is_valid").order_by("-pub_date")
    paginator1 = Paginator(mess, 6) 
    page1 = request.GET.get('page1','1')
    try:
        mess = paginator1.page(page1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mess = paginator1.page(1)
    except EmptyPage:
        mess = paginator1.page(paginator1.num_pages)
    return render(request,"hire.html",locals())
@csrf_exempt
@login_required
def showemploy(request,id):
    user = User.objects.get(userid=request.session['userid'])
    employ = get_object_or_404(Employ,id=id)
    return render(request,"employ.html",locals())
@csrf_exempt
@login_required    
def showaskemploy(request,id):
    user = User.objects.get(userid=request.session['userid'])
    employ = get_object_or_404(AskEmploy,id=id)
    return render(request,"askemploy.html",locals())
