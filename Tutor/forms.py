# -*- coding:utf-8 -*-
from django import forms
from django.utils.translation import  ugettext_lazy as _
from models import Tutor, Parent, Employ
#from django.forms import ModelForm

grade_choice = (('Primary', '小学'), ('J1', '初一'), ('J2', '初二'), ('J3','初三'),
                    ('H1', '高一'), ('H2', '高二'), ('H3', '高三'))
subject_choice = (('Math', '数学'),('Chinese', '语文'),("English", '英语'),
                    ('Physic', "物理"), ('Chemistry', '化学'), ('Biology', '生物'))

class LoginForm(forms.Form): 
    username = forms.CharField(max_length=10,widget=forms.TextInput(attrs={"placeholder":"用户名"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"密码"}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=10)
    password1 = forms.CharField(max_length=10)
    password2 = forms.CharField(max_length=10)
    email = forms.EmailField()
    def pwd_validate(self,p1,p2):
        return p1==p2
 

class parent_form(forms.Form):
    username = forms.CharField(max_length=10)
    realname = forms.CharField(max_length = 30)
    #gender = forms.CharField()
    email = forms.EmailField()
    age = forms.IntegerField()
    qq = forms.IntegerField()
    phone = forms.IntegerField()
    address = forms.CharField(max_length = 80)
    information = forms.CharField(max_length = 80)

class tutor_form(forms.Form):
    username = forms.CharField(max_length=10)
    realname = forms.CharField(max_length = 30)
    email = forms.EmailField()
    age = forms.IntegerField()
    qq = forms.IntegerField()
    phone = forms.IntegerField()
    major = forms.CharField(max_length=20)
    university = forms.CharField(max_length = 30)
    information = forms.CharField(max_length = 80)


class CreateTutor(forms.ModelForm):
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
        widget=forms.PasswordInput(attrs={"placeholder":"密码"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder":"邮箱:xxxx@qq.com"})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"重复密码"}))
    class Meta:
        model = Tutor
        fields = ["username", "password", "password_confirm", "gender", "email"]
    def clean_password_confirm(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
class CreateParent(CreateTutor):
    class Meta:
        model = Parent
        fields = ["username", "password", "password_confirm", "gender", "email"]


class employ_form(forms.ModelForm):
    class Meta:
        model = Employ
        exclude = ['parent','pub_date']
    

