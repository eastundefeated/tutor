#coding=utf8
from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from forms import *
from django.db.models import Q
from django.core.mail import EmailMessage
from PIL import Image
import hashlib
university_choice = (("001","哈尔滨工业大学"), ("002","哈尔滨工程大学"),
                    ("003","东北林业大学"),
                    ("004","黑龙江大学"),
                    ("005","哈尔滨理工大学"),
                    ("006","东北农业大学"),
                    ("007","哈尔滨医科大学"),
                    ("008","黑龙江中医药大学"),
                    ("010","哈尔滨师范大学"),
                    ("011","哈尔滨商业大学"),
                    ("012","哈尔滨学院"),
                    ("013","黑龙江工程学院"),
                    ("014","黑龙江科技学院"),
                    ("015","哈尔滨德强商务学院"),
                    ("016","哈尔滨体育学院"),
                    ("017","黑龙江东方学院"),
)
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
		parent.is_active = True
		parent.save()
                request.session['userid'] = parent.userid
                request.session['identity'] = "p"
                messages.success(request,"注册成功")
		url = 'id'+str(parent.userid)+'password'+hashlib.sha1(request.POST.get("password")).hexdigest()
		html_content = '<p>尊敬的用户请点击<a href="http://localhost:8000/%s/">%s</a>激活邮件</p>'%(url,url)
		subject = "邮箱激活"
		msg = EmailMessage(subject,html_content,"2770837735@qq.com",['2770837735@qq.com'])
		msg.content_subtype = "html" 
		msg.send()
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
        form = CreateParent()
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
                    if tutor.password==request.POST.get('password'):
			if tutor.is_active:
			    request.session['userid'] = tutor.userid
                	    request.session['identity'] = "t"
                            return HttpResponseRedirect('/index/')
			else:
			    messages.warnning(request,"该用户未被激活")
                    else:
                        messages.error(request,"用户名或密码错误")
                except Tutor.DoesNotExist:
                    messages.error(request,"该用户不存在")
        else:
            if form.is_valid():
                username = request.POST.get('username')
                try:
                    parent = Parent.objects.get(username=username)
                    if parent.password==request.POST.get('password'):
			if parent.is_active:
			    request.session['userid'] = parent.userid
                	    request.session['identity'] = "p"
                            return HttpResponseRedirect('/index/')
			else:
			    messages.warning(request,"该用户未被激活")
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
    university_dict = {}	
    for item in university_choice:
        university_dict[item[0]] = item[1]
    if request.session['identity'] == 'p':
	if Tutor.objects.count()>5:
	    tutorset = Tutor.objects.all()[:5]
	else:
	    tutorset = Tutor.objects.all()	
	user = Parent.objects.get(userid = userid)
	if user.employ_set.count()>0:
	    fm = user.employ_set.all()[0]
	    if fm.gender2 == "N":
		pass
	    else:
		tutorset = tutorset.filter(gender=fm.gender2)
	    tutorset = list(tutorset)
	    tutorset.sort(key = lambda x:len(set(x.subject.all())&set(fm.subject.all())),reverse=True)
	forms = (user.employ_set.all()[:2] if (user.employ_set.count()>2) else user.employ_set.all())
	dict_subject = []
	for form in forms:
	    dict_subject.append((form,(form.subject.all()[:3] if (form.subject.count()>3) else form.subject.all())))
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
	if user.receivecomment.count()>2:
	    ptcomment = user.receivecomment.all()[:2]
	else:
	    ptcomment = user.receivecomment.all()
	if user.receivemessage.count()>2:
	    ptmessage = user.receivemessage.all()[:2]
	else:
	    ptmessage = user.receivemessage.all()
	forms = Employ.objects.all()[:4] if Employ.objects.count()>4 else Employ.objects.all()
	dict_subject = []
	for form in forms:
	    dict_subject.append((form,(form.subject.all()[:3] if (form.subject.count()>3) else form.subject.all())))
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
	        messages.success(request,"修改成功")
    	else:
            form = ParentForm(instance=user)
        return render(request,'pinfo.html',locals())
    else:
	user = Tutor.objects.get(userid=userid)
    	if request.method=="POST":
            form = TutorForm(request.POST,instance=user)
            if form.is_valid() and form.has_changed():
                form.save()
		messages.success(request,"修改成功")
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
            img.thumbnail((200,180),Image.ANTIALIAS)
            name='./Tutor/static/image/'+str(identity)+str(userid)+'.png'
            img.save(name,"png")
	    messages.success(request,"图片上传成功")
            return HttpResponseRedirect("/index/")
    return render(request,'image.html')
@csrf_exempt
@login_required
def search(request):
    university_dict = {}
    for item in university_choice:
        university_dict[item[0]] = item[1]
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
def publishform(request):
    university_dict = {}
    for item in university_choice:
        university_dict[item[0]] = item[1]
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
	     try:
	         Employ.objects.get(id=request.POST.get("delete")).delete()
	         form = EmployForm()
	         messages.success(request,"删除成功")
	     except Employ.DoesNotExist:
		 form = EmployForm()
	elif "save" in request.POST:
	    form = EmployForm(request.POST)
	    if form.is_valid():
	        employ = form.save()
	        employ.parent = user
	        employ.save()
    	        messages.success(request,"发布成功")
		return HttpResponseRedirect('/index/')
	else:
	    form = EmployForm()
    else:
	form = EmployForm()
    if user.employ_set.count()>3:
	forms = user.employ_set.all()[:3]
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
    userid = request.session['userid']
    identity = request.session['identity']
    if identity == 'p':
   	return HttpResponseRedirect('/index/')
    user = Tutor.objects.get(userid=userid)
    if request.method == "POST":
	if "delete" in request.POST:
	    Exp.objects.get(id=request.POST.get('delete')).delete()
	    messages.success(request,"删除成功")
	    return HttpResponseRedirect("/index/")
	elif "save" in request.POST:
    	    form = ExpForm(request.POST)
	    if form.is_valid():
	        exp = form.save()
	        exp.tutor = user
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
	
