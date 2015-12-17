# -*- coding:utf-8 -*-
from django import forms
from models import *
#from django.forms import ModelForm
import hashlib
import datetime
grade_choice = (('Pr', '小学'), ('J1', '初一'), ('J2', '初二'), ('J3','初三'),('H1', '高一'), ('H2', '高二'), ('H3', '高三'))
subject_choice = (('Math', '数学'),('Chinese', '语文'),("English", '英语'),('Physic', "物理"), ('Chemistry', '化学'), ('Biology', '生物'))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"placeholder":"用户名"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"密码"}))
    identity = forms.ChoiceField(choices=((True,'家长'),(False,'家教')))

class CreateForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'用户名'}),error_messages={'required':"用户名不能为空",})
    error_messages = {'password_mismatch':"请输入相同的密码"}
    gender = forms.ChoiceField(choices=(('M', '男'), ('F', '女')))
    password = forms.CharField(error_messages={'required':"密码不能为空",},widget=forms.PasswordInput(attrs={"placeholder":"密码"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"邮箱:xxxx@qq.com"}),
	error_messages={'required':"邮箱不能为空",'invalid':"邮箱格式无效","invalid":"邮箱格式无效",})
    identity = forms.ChoiceField(choices=((True, '家长'), (False, '家教')))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"重复密码"}),
	error_messages={
            'required':"请重复密码",
        })
    def clean_password_confirm(self):
        password1,password2 = self.cleaned_data.get('password'),self.cleaned_data.get('password_confirm')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    class Meta:
	model = User
	fields = ['username','password','password_confirm','email', 'gender','identity'] 

class EmployForm(forms.ModelForm):
    error_messages = {"illegal_time_start":"开始日期不能晚于今日!","illegal_time_end":"结束日期不能早于开始日期"}
    info1 = forms.CharField(label="子女信息补充",required = False,
    widget=forms.Textarea(attrs={"cols":30,"rows":5}))
    info2 = forms.CharField(label="家教要求补充",required = False,
    widget=forms.Textarea(attrs={"cols":30,"rows":5}))
    info3 = forms.CharField(label="其他",required = False,
    widget=forms.Textarea(attrs={"cols":30,"rows":5}))
    class Meta:
        model = Employ
        exclude = ['parent','pub_date','is_visible']
    def clean_from_time(self):
	from_time = self.cleaned_data.get('from_time')
	today = datetime.date.today()
	if from_time < today:
	    raise forms.ValidationError(
                self.error_messages['illegal_time_start'],
                code='illegal_time_start',
            )
        return from_time
    def clean_to_time(self):
    	from_time,to_time = self.cleaned_data.get('from_time'),self.cleaned_data.get('to_time')
	if to_time <= from_time:
	    raise forms.ValidationError(
                self.error_messages['illegal_time_end'],
                code='illegal_time_end',
            )
        return to_time

class AskEmployForm(forms.ModelForm):
    error_messages = {"illegal_time_start":"开始日期不能晚于今日!","illegal_time_end":"结束日期不能早于开始日期"}
    info = forms.CharField(label="信息补充",required = False,
    widget=forms.Textarea(attrs={"cols":30,"rows":5}))
    class Meta:
        model = AskEmploy
        exclude = ['tutor','pub_date','is_visible']
    def clean_from_time(self):
	from_time = self.cleaned_data.get('from_time')
	today = datetime.date.today()
	if from_time < today:
	    raise forms.ValidationError(
                self.error_messages['illegal_time_start'],
                code='illegal_time_start',
            )
        return from_time
    def clean_to_time(self):
    	from_time = self.cleaned_data.get('from_time')
        to_time = self.cleaned_data.get('to_time')
	if from_time and to_time and from_time > to_time:
	    raise forms.ValidationError(
                self.error_messages['illegal_time_end'],
                code='illegal_time_end',
            )
        return to_time
    
class TutorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['realname','age','phone','qq','information','state','major','university','subject']

class ParentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['realname','age','phone','qq','information','address']

class ExpForm(forms.ModelForm):
    title = forms.CharField(label="标题",max_length=20,
      error_messages={
	'required':"标题不能为空",
    })
    class Meta:
	model = Exp
	exclude = ['user','pub_date']

#密码重置表单
class PasswordReset(forms.Form):
    error_messages = {
	"password_mismatch":"请输入相同的密码"
    }
    password1 = forms.CharField(max_length=30, error_messages={
            'required':"新密码不能为空",
        },
        widget=forms.PasswordInput(attrs={"placeholder":"新密码"}))
    password2 = forms.CharField(max_length=30, error_messages={
            'required':"重复密码不能为空",
        },
        widget=forms.PasswordInput(attrs={"placeholder":"重复新密码"}))
    def clean_password2(self):
	password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1!=password2:
	    raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
#密码修改表单
class PasswordChange(PasswordReset):
    error_messages = {
	"password_mismatch":"请输入相同的密码",
    }
    password_orgin = forms.CharField(max_length=30, error_messages={
            'required':"旧密码不能为空",},
        widget=forms.PasswordInput(attrs={"placeholder":"旧密码"}))

#搜索家教表单
class searchTutorForm(forms.Form):
    username = forms.CharField(label="家教名字(可不填)",max_length=30,required=False)
    gender = forms.ChoiceField(label="家教性别",choices=(('N','男女不限'),('M',"男"),('F',"女")))
    grade = forms.ChoiceField(label="辅导年级",choices=grade_choice)
    subject = forms.MultipleChoiceField(label="辅导科目",choices=subject_choice,widget=forms.CheckboxSelectMultiple())
#搜索家长发布的表单
class searchEmployForm(forms.Form):
    pub_date = forms.ChoiceField(label="发布日期",choices=(('all','全部'),('day','最近一天'),('week','最近一周')))
    salary = forms.ChoiceField(label="薪水",choices=(('N','未填'),('0','50以下'),('1','50-100'),('2','100以上')))
    grade = forms.ChoiceField(label="辅导年级",choices=grade_choice)
    subject = forms.MultipleChoiceField(label="辅导科目",choices=subject_choice,widget=forms.CheckboxSelectMultiple())
#搜索家教发布的表单
class searchAskEmployForm(searchEmployForm):
    pass
