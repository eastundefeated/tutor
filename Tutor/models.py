#-*-coding:utf-8-*-
from django.db import models
subject_choice = (('Math', '数学'),('Chinese', '语文'),("English", '英语'),
                    ('Physic', "物理"), ('Chemistry', '化学'), ('Biology', '生物'))
grade_choice = (('小学', (('P1','小学一年级'),('P2','小学二年级'))), ('J1', '初一'), ('J2', '初二'), ('J3','初三'),
                    ('H1', '高一'), ('H2', '高二'), ('H3', '高三'))
age_choice = (('0','5岁以下'),('1','5岁至12岁'),('2','12至16岁'),('3','16岁以上'))
gender_choice = (('M', '男'), ('F', '女'))
state_choice = (('B', '忙碌'), ('F', '空闲'))
university_choice = (("哈尔滨工业大学","哈尔滨工业大学"), ("哈尔滨工程大学","哈尔滨工程大学"),
                    ("东北林业大学","东北林业大学"),
                    ("黑龙江大学","黑龙江大学"),
                    ("哈尔滨理工大学","哈尔滨理工大学"),
                    ("东北农业大学","东北农业大学"),
                    ("哈尔滨医科大学","哈尔滨医科大学"),
                    ("黑龙江中医药大学","黑龙江中医药大学"),
                    ("哈尔滨师范大学","哈尔滨师范大学"),
                    ("哈尔滨商业大学","哈尔滨商业大学"),
                    ("哈尔滨学院","哈尔滨学院"),
                    ("黑龙江工程学院","黑龙江工程学院"),
                    ("黑龙江科技学院","黑龙江科技学院"),
                    ("哈尔滨德强商务学院","哈尔滨德强商务学院"),
                    ("哈尔滨体育学院","哈尔滨体育学院"),
                    ("黑龙江东方学院","黑龙江东方学院"),
)
# Create your models here.
class Subject(models.Model):
    subject = models.CharField(max_length=10, choices=subject_choice)
    grade = models.CharField(max_length=10, choices=grade_choice)
    def __unicode__(self):
        return self.grade + ' ' + self.subject
class BaseProfile(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name="用户名", max_length=30, unique=True,
        error_messages={
            'required':"用户名不能为空",
            'unique':'该用户名已存在'
        })
    realname = models.CharField(verbose_name="真实姓名", max_length=30, blank=True)
    password = models.CharField(max_length=30,
        error_messages={
            'required':"密码不能为空",
        })
    email = models.EmailField(verbose_name="电子邮箱",
	error_messages={
            'required':"邮箱不能为空",
	    'invalid':"请输入核对邮箱格式",
        })
    gender = models.CharField(verbose_name="性别", max_length=2, choices=gender_choice, default="M")
    age = models.IntegerField(verbose_name="年龄", null=True, blank=True)
    phone = models.CharField(verbose_name="电话", max_length=13, blank=True)
    qq = models.CharField(verbose_name="QQ", max_length=13, blank=True)
    information = models.TextField(verbose_name="补充信息", blank=True)
    def __unicode__(self):
        return self.username
    class Meta:
        ordering = ["username"]
class Tutor(BaseProfile):
    score = models.IntegerField(verbose_name="评分", default=0)
    state = models.CharField(verbose_name="状态", max_length=2, choices=state_choice, default='F')
    university = models.CharField(verbose_name="大学", max_length=30, blank=True, choices = university_choice)
    major = models.CharField(verbose_name="专业", max_length=40, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)
class Parent(BaseProfile):
    address = models.TextField(verbose_name="地址",blank=True)
class BaseMessage(models.Model):
    ID = models.AutoField(primary_key=True)
    content = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-pub_date"]
class PTMessage(BaseMessage):
    from_user = models.ForeignKey(Parent, related_name="sendemessage")
    to_user = models.ForeignKey(Tutor, related_name="receivemessage")
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username
class TPMessage(BaseMessage):
    from_user = models.ForeignKey(Tutor, related_name="sendemessage")
    to_user = models.ForeignKey(Parent, related_name="receivemessage")
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username
class PTComment(BaseMessage):
    from_user = models.ForeignKey(Parent, related_name="sendecomment")
    to_user = models.ForeignKey(Tutor, related_name="receivecomment")
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username
class TPComment(BaseMessage):
    from_user = models.ForeignKey(Tutor, related_name="sendecomment")
    to_user = models.ForeignKey(Parent, related_name="receivecomment")
    def __unicode__(self):
        return self.from_user.username + " to " + self.to_user.username

class Employ(models.Model):
    parent = models.ForeignKey(Parent)
    #子女信息
    age = models.CharField(verbose_name="子女年龄", max_length = 2,choices=age_choice,default="3")
    gender1 = models.CharField(verbose_name="子女性别", max_length=2, choices=gender_choice)
    subject = models.ManyToManyField(Subject, blank=True)
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
