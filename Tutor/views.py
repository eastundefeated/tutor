#coding=utf8
from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from forms import *
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
import datetime
import hashlib
import math
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
def forgetPassword(request):
    if request.method == "POST":
	mail = request.POST.get("email")
	try:
	    user = User.objects.get(email=mail)
	except Tutor.DoesNotExist:
	    return HttpResponse("<h1>Invalid email!</h1>")
	url = "localhost:8000/setpassword/"
	url += str(user.userid)+"/"+hashlib.md5(str(user.password)).hexdigest()+"/"
	content = "<html><body>尊敬的%s,请复制该链接或直接点击打开来完成重置密码<a href=%s>%s</a></body></html>"%(user.username,url,url)
	msg = EmailMessage("重置密码",content,"2770837735@qq.com",[mail])
	msg.send()
	return HttpResponse("<h1>验证邮件已发往您的邮箱!</h1>")
#邮箱验证
def activeMail(request,userid,password):
    user = get_object_or_404(User,userid=userid)
    if hashlib.md5(str(user.password)).hexdigest() == password and not user.is_active:
        user.is_active = True
	user.save()
	request.session['userid'] = userid
	messages.success(request,"邮箱验证成功")
	return HttpResponseRedirect('/index/')
    else:
	return HttpResponseRedirect('/')
#重置密码
def resetPassword(request,userid,password):
    user = get_object_or_404(User,userid=userid)
    if hashlib.md5(str(user.password)).hexdigest() == password:
        if request.method == "POST":
	    form = PasswordReset(request.POST)
	    if form.is_valid():
		user.password = request.POST.get('password1')
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
    is_change = True
    user = User.objects.get(userid=request.session['userid'])
    if request.method == "POST":
	form = PasswordChange(request.POST)
	if form.is_valid():
	    if request.POST.get('password_origin')==user.password:
		user.password = request.POST.get('password1')
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
            request.session['userid'] = user.userid
            messages.success(request,"注册成功")
            if 'next' in request.session:
		url = request.session['next']
	        del request.session['next']
	    else:
	        url = '/index/'
	    return HttpResponseRedirect(url)
    else:
        form = CreateForm()
    return render(request, "register.html", {'form':form})
def mainpage(request):
    pass
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
	    return HttpResponseRedirect("/login/")
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
    hirecount = user.hire_to.filter(is_read=False).count()
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
    userid = request.session["userid"]
    identity = request.session['identity']
    if identity == "p":
	user = Parent.objects.get(userid=userid)
	tutorset = Tutor.objects.order_by('-score')	
	if request.method == "POST":
	    grade=request.POST.get('grade')
	    subjectlist = request.POST.getlist('subject')
	    if grade!='N' and subjectlist:	    
		tutorset = tutorset.filter(subject__grade=grade,subject__subject__in=subjectlist)		
	    elif grade!='N':
		tutorset = tutorset.filter(subject__grade=grade)
	    elif subjectlist:
		tutorset = tutorset.filter(subject__subject__in=subjectlist)
	    else:
		pass
	    if 'content' in request.POST:
	        content = request.POST.get('content')
		tutorset = tutorset.filter(username__contains=content)
	    if request.POST.get('gender')!='N':
		tutorset = tutorset.filter(gender=request.POST.get('gender'))
	    print tutorset
	dict_subject = []
	for tutor in tutorset.distinct():
	    if tutor.subject.count()>2:
	 	dict_subject.append((tutor,tutor.subject.all()[:2]))
	    else:
		dict_subject.append((tutor,tutor.subject.all())) 		
        return render(request,'psearch.html',locals())
    else:
	user = Tutor.objects.get(userid=userid)
	forms = Employ.objects.all()
	if request.method == "POST":
	    tutorgender = request.POST.get('tutorgender')
	    grade = request.POST.get('grade')
	    subject_list = request.POST.getlist('subject')
	    forms = forms.filter(Q(gender2=tutorgender)|Q(gender2="N")) if tutorgender != "N" else forms
	    forms = forms.filter(subject__grade=grade) if grade != "N" else forms
	    forms = forms.filter(subject__subject__in=subject_list) if subject_list else forms	
	dict_subject = []
    	for fm in forms:
	    dict_subject.append((fm,(fm.subject.all()[:5] if fm.subject.count()>5 else fm.subject.all())))	
	return render(request,'tsearch.html',locals())
@csrf_exempt
@login_required
def searchTutor(request):
    global university_dict
    user = User.objects.get(userid=request.session['userid'])
    if not user.identity:
	return HttpResponseRedirect("/index/")
    if request.method == "POST":
	tutorset = User.objects.filter(identity=False).all()	
	form = searchTutorForm(request.POST)
	fm = request.POST
        tutorset = tutorset.filter(username__icontains=fm['username']) if fm['username'] else tutorset
	tutorset = tutorset.filter(gender=fm['gender']) if fm['gender']!='N' else tutorset
	tutorset = tutorset.filter(subject__grade=fm['grade']) if fm['grade']!='N' else tutorset
	tutorset = tutorset.filter(subject__subject__in=fm['subject']) if fm['subject'] else tutorset
    else:
	tutorset = User.objects.filter(identity=False).order_by("-score")
	form = searchTutorForm() 
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
	form = EmployForm(request.POST) if user.identity else AskEmployForm(request.POST)
	if form.is_valid():
	    fm = form.save()
	    if user.identity:
		fm.parent = user
	    else:
		fm.tutor = user
	    fm.save()
	    messages.success(request,"表单发布成功")
	    return HttpResponseRedirect("/index/")
    else:
	form = EmployForm() if user.identity else AskEmployForm()
    return render(request,"publishform.html",locals())
@csrf_exempt
@login_required
def message(request):
    university_dict = {}
    for item in university_choice:
        university_dict[item[0]] = item[1]
    userid = request.session['userid']
    identity = request.session['identity']
    if identity == "p":
	user = Parent.objects.get(userid=userid)
	tpmessage = user.receivemessage.all()
        tpcomment = user.receivecomment.all()
	if Tutor.objects.count()>10:
    	    tutors = Tutor.objects.all()[:10]
        else:
	    tutors = Tutor.objects.all()
	if request.method == 'POST':
	    if "delete" in request.POST:
		try:
		    TPMessage.objects.get(ID=request.POST.get("delete")).delete()
		    messages.success(request,"删除成功")
		except TPMessage.DoesNotExist:
		    pass
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
	tpmessage = user.receivemessage.all()
        tpcomment = user.receivecomment.all()
	if Tutor.objects.count()>10:
    	    tutors = Tutor.objects.all()[:10]
        else:
	    tutors = Tutor.objects.all()
	if request.method == 'POST':
	    if "delete" in request.POST:
		try:
		    PTMessage.objects.get(ID=request.POST.get("delete")).delete()
	            messages.success(request,"删除成功")
  		except PTMessage.DoesNotExist:
		    pass
	if Employ.objects.count()>4:
            forms = Employ.objects.all()[:4]
        else:
	    forms = Employ.objects.all()
        dict_subject = []
        for fm in forms:
	    if fm.subject.count()>2:
	        dict_subject.append((fm,fm.subject.all()[:2]))
            else:
	        dict_subject.append((fm,fm.subject.all()))	
	return render(request,"tmessage.html",locals())
@login_required
def showdetail(request,id):
    if request.session['identity'] == 'p':
	return HttpResponseRedirect('/index/')
    else:
	user = Tutor.objects.get(userid=request.session['userid'])
	employ = get_object_or_404(Employ,id=id)
	import datetime
	subject_list = employ.subject.all()
	validtime = employ.pub_date + datetime.timedelta(days=employ.valid_days)
	return render_to_response("employ.html",locals())
	
@csrf_exempt
@login_required
def share(request):   
    user = User.objects.get(userid=request.session['userid'])
    if request.method == "POST":
	if "delete" in request.POST:
	    Exp.objects.get(id=request.POST.get('delete')).delete()
	    messages.success(request,"删除成功")
	    return HttpResponseRedirect("/index/")
	elif "save" in request.POST:
    	    form = ExpForm(request.POST)
	    if form.is_valid():
	        exp = form.save()
	        exp.user = user
 	        exp.save()
	        messages.success(request,"发表成功!")
	        return HttpResponseRedirect("/index/")
    else:
	form = ExpForm()
    forms = user.exp_set.all()
    return render_to_response("share.html",locals())
@csrf_exempt
@login_required
def pinformation(request,userid):
    if request.session['identity'] == "p":
	return HttpResponseRedirect('/index/')
    else:
	user = Tutor.objects.get(userid=request.session['userid'])
        parent = get_object_or_404(Parent,userid=userid)	
	if request.method == "POST":
	    if "ccommit" in request.POST:
		TPComment.objects.create(from_user=user,to_user=parent,content=request.POST.get("content"))
		messages.success(request,"评论成功") 	
		return HttpResponseRedirect('/index/')
	    elif "mcommit" in request.POST:
		TPMessage.objects.create(from_user=user,to_user=parent,content=request.POST.get("content"))
		messages.success(request,"留言成功") 	
		return HttpResponseRedirect('/index/')
            else:
		pass
	comment_list = parent.receivecomment.all()
        message_list = parent.receivemessage.all() 
        return render(request,"pinformation.html",locals()) 
@csrf_exempt
@login_required
def tinformation(request,userid):
    if request.session['identity'] == "t":
	return HttpResponseRedirect('/index/')
    else:
	user = Parent.objects.get(userid=request.session['userid'])
        tutor = get_object_or_404(Tutor,userid=userid)
	university_dict = {}
	for item in university_choice:
	    university_dict[item[0]] = item[1]
	subject_list = tutor.subject.all()
	if request.method == "POST":
	    if "ccommit" in request.POST:
		PTComment.objects.create(from_user=user,to_user=tutor,content=request.POST.get("content"))
		messages.success(request,"评论成功") 	
		return HttpResponseRedirect('/index/')
	    elif "mcommit" in request.POST:
		PTMessage.objects.create(from_user=user,to_user=tutor,content=request.POST.get("content"))
		messages.success(request,"留言成功") 	
		return HttpResponseRedirect('/index/')
            else:
		pass
	comment_list = tutor.receivecomment.all()
        message_list = tutor.receivemessage.all() 
        return render(request,"tinformation.html",locals()) 	
@csrf_exempt
@login_required
def comment(request):
    pass
