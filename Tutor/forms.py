# -*- coding:utf-8 -*-
from django import forms
from models import *
#from django.forms import ModelForm

grade_choice = (('Primary', '小学'), ('J1', '初一'), ('J2', '初二'), ('J3','初三'),
                    ('H1', '高一'), ('H2', '高二'), ('H3', '高三'))
subject_choice = (('Math', '数学'),('Chinese', '语文'),("English", '英语'),
                    ('Physic', "物理"), ('Chemistry', '化学'), ('Biology', '生物'))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=10,widget=forms.TextInput(attrs={"placeholder":"用户名"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"密码"}))

class BaseCreateForm(forms.Form):
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={'placeholder':'用户名'}),
        error_messages={
            'required':"用户名不能为空",
        })
    error_messages = {
        'password_mismatch':"请输入相同的密码",
    }
    gender = forms.ChoiceField(choices=(('M', '男'), ('F', '女')))
    password = forms.CharField(
	error_messages={
            'required':"密码不能为空",
        },
        widget=forms.PasswordInput(attrs={"placeholder":"密码"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder":"邮箱:xxxx@qq.com"}),
	error_messages={
            'required':"邮箱不能为空",
	    'invalid':"邮箱格式无效",
        }
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"重复密码"}),
	error_messages={
            'required':"请重复密码",
        })
    def clean_password_confirm(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

class CreateParent(BaseCreateForm,forms.ModelForm):
    class Meta:
        model = Parent
        fields = ["username", "password", "password_confirm", "gender", "email"]

class CreateTutor(BaseCreateForm,forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ["username", "password", "password_confirm", "gender", "email"]

class EmployForm(forms.ModelForm):
    info1 = forms.CharField(label="子女信息补充",required = False,
    widget=forms.Textarea(attrs={"cols":30,"rows":5}))
    info2 = forms.CharField(label="家教要求补充",required = False,
    widget=forms.Textarea(attrs={"cols":30,"rows":5}))
    info3 = forms.CharField(label="其他",required = False,
    widget=forms.Textarea(attrs={"cols":30,"rows":5}))
    class Meta:
        model = Employ
        exclude = ['parent','pub_date']
class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        exclude = ['userid','username','score','password','gender']
class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['userid','password','username','gender']

class ExpForm(forms.ModelForm):
    title = forms.CharField(label="标题",max_length=20,
      error_messages={
	'required':"标题不能为空",
    })
    class Meta:
	model = Exp
	exclude = ['tutor','pub_date']
