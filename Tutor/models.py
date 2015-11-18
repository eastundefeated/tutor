#-*-coding:utf-8-*-
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
subject_choice = (('Math', '数学'),('Chinese', '语文'),("English", '英语'),
                    ('Physic', "物理"), ('Chemistry', '化学'), ('Biology', '生物'))
grade_choice = (('小学', (('P1','小学一年级'),('P2','小学二年级'))), ('J1', '初一'), ('J2', '初二'), ('J3','初三'),
                    ('H1', '高一'), ('H2', '高二'), ('H3', '高三'))
age_choice = (('0','5岁以下'),('1','5岁至12岁'),('2','12至16岁'),('3','16岁以上'))
gender_choice = (('M', '男'), ('F', '女'))
state_choice = (('B', '忙碌'), ('F', '空闲'))
# Create your models here.
class Subject(models.Model):
    subject = models.CharField(max_length=10, choices=subject_choice)
    grade = models.CharField(max_length=10, choices=grade_choice)
    def __unicode__(self):
        return self.grade + ' ' + self.subject

class Tutor(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True,
        error_messages={
            'required':"用户名不能为空",
            'unique':"该用户名已存在",
        }
    )
    password = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.CharField(max_length=2, choices=gender_choice, default="M")
    state = models.CharField(max_length=2, choices=state_choice, default='F')
    realname = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    qq = models.CharField(max_length=13, blank=True)
    university = models.CharField(max_length=30, blank=True)
    major = models.CharField(max_length=40, blank=True)
    information = models.CharField(max_length=80, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)
    def __unicode__(self):
        return self.username
class Parent(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30,unique=True,
        error_messages={
            'required':"用户名不能为空",
            'unique':"该用户名已存在",
        })
    realname = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    qq = models.CharField(max_length=13, blank=True)
    gender = models.CharField(max_length=2, choices=gender_choice)
    address = models.CharField(max_length=80, blank=True)
    information = models.CharField(max_length=80, blank=True)
    def __unicode__(self):
        return self.username

class PTMessage(models.Model):
    ID = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(Parent, related_name="sendemessage")
    to_user = models.ForeignKey(Tutor, related_name="receivemessage")
    content = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-pub_date"]
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username
class TPMessage(models.Model):
    ID = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(Tutor, related_name="sendemessage")
    to_user = models.ForeignKey(Parent, related_name="receivemessage")
    content = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-pub_date"]
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username
class PTComment(models.Model):
    ID = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(Parent, related_name="sendecomment")
    to_user = models.ForeignKey(Tutor, related_name="receivecomment")
    content = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-pub_date"]
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username
class TPComment(models.Model):
    ID = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(Tutor, related_name="sendecomment")
    to_user = models.ForeignKey(Parent, related_name="receivecomment")
    content = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-pub_date"]
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username

class Employ(models.Model):
    parent = models.ForeignKey(Parent)
    #子女信息
    age = models.CharField(verbose_name="子女年龄", max_length = 2,choices=age_choice,default="3")
    gender1 = models.CharField(verbose_name="子女性别", max_length=2, choices=gender_choice)
    subject = models.ManyToManyField(verbose_name="科目", Subject, blank=True)
    info1 = models.TextField(verbose_name="子女额外信息描述", blank = True,)
    #家教信息
    gender2 = models.CharField(verbose_name="家教性别要求", max_length = 2,choices = (("N","男女不限"),("M","男"),("F","女")),default = "N")
    info2 = models.TextField(verbose_name="家教额外要求", blank = True)
    site = models.CharField(verbose_name="上课地点", max_length=15, blank=True)
    time = models.CharField(verbose_name="子女性别", max_length=15, blank=True)
    salary = models.FloatField(null=True, blank=True)
    
    info3 = models.TextField(blank = True)
    
    pub_date = models.DateTimeField(auto_now_add=True)
    valid_days = models.IntegerField(default=30)
    class Meta:
        ordering = ['-pub_date']
    def __unicode__(self):
        return self.parent.username


#class Employ
