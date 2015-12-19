#-*-coding:utf-8-*-
from django.db import models
subject_choice = (('Math', '数学'),('Chinese', '语文'),("English", '英语'),
                    ('Physic', "物理"), ('Chemistry', '化学'), ('Biology', '生物'))
dict_subject = {'Math':u'数学','Chinese':u'语文',"English":u'英语','Physic':u"物理",'Chemistry':u'化学','Biology':u'生物'}
grade_choice = (('Pr','小学'), ('J1', '初一'), ('J2', '初二'), ('J3','初三'),
                    ('H1', '高一'), ('H2', '高二'), ('H3', '高三'))
dict_grade = {'Pr':u'小学','J1':u"初一","J2":u"初二","J3":u"初三","H1":u"高一","H2":u"高二","H3":u"高三"}
age_choice = (('0','5岁以下'),('1','5岁至12岁'),('2','12至16岁'),('3','16岁以上'))
gender_choice = (('M', '男'), ('F', '女'))
state_choice = (('B', '忙碌'), ('F', '空闲'))
university_choice = (("001","哈尔滨工业大学"), ("002","哈尔滨工程大学"),("003","东北林业大学"),
                    ("004","黑龙江大学"),("005","哈尔滨理工大学"),("006","东北农业大学"),
                    ("007","哈尔滨医科大学"),("008","黑龙江中医药大学"),("010","哈尔滨师范大学"),
                    ("011","哈尔滨商业大学"),("012","哈尔滨学院"),("013","黑龙江工程学院"),
                    ("014","黑龙江科技学院"),("015","哈尔滨德强商务学院"),("016","哈尔滨体育学院"),("017","黑龙江东方学院"),
)

# Create your models here.
class Subject(models.Model):
    subject = models.CharField(max_length=10, choices=subject_choice)
    grade = models.CharField(max_length=10, choices=grade_choice)
    def __unicode__(self):
        return dict_grade[self.grade]+ dict_subject[self.subject]
    class Meta:
	unique_together = (("subject"),("grade"))
        ordering = ["grade","subject"]
class User(models.Model):
    #共享信息
    userid = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name="用户名", max_length=30, unique=True,)
    realname = models.CharField(verbose_name="真实姓名", max_length=30, blank=True)
    password = models.CharField(max_length=40,)
    has_image = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(verbose_name="电子邮箱",unique=True,)
    gender = models.CharField(verbose_name="性别", max_length=2, choices=gender_choice, default="M")
    age = models.IntegerField(verbose_name="年龄", null=True, blank=True)
    phone = models.CharField(verbose_name="电话", max_length=13, blank=True)
    qq = models.CharField(verbose_name="QQ", max_length=13, blank=True)
    information = models.TextField(verbose_name="补充信息", blank=True)
    identity = models.BooleanField(verbose_name="identity",default=True)
    #家教信息
    count_comment = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    score = models.FloatField(verbose_name="评分", default=0)
    state = models.CharField(verbose_name="状态", max_length=2, choices=state_choice, default='F')
    university = models.CharField(verbose_name="大学", max_length=30, blank=True, choices = university_choice)
    major = models.CharField(verbose_name="专业", max_length=40, blank=True)
    subject = models.ManyToManyField(Subject,verbose_name="科目", blank=True)
    #家长信息
    address = models.TextField(verbose_name="地址",blank=True)
    def __unicode__(self):
        return self.username
    class Meta:
        ordering = ["username"]

#雇佣关系中间类
class EmployRelationship(models.Model):
    parent = models.ForeignKey(User,related_name="employer")
    tutor = models.ForeignKey(User,related_name="employee")
    pub_date = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    has_comment = models.BooleanField(default=False)
    class Meta:
	ordering = ['-pub_date']
    def __unicode__(self):
	return self.parent.username + " has hired "+self.tutor.username


class Employ(models.Model):
    user = models.ForeignKey(User,blank=True,null=True)
    #子女信息
    is_visible = models.BooleanField(default=True)
    age = models.CharField(verbose_name="子女年龄", max_length = 2,choices=age_choice,default="3")
    gender1 = models.CharField(verbose_name="子女性别", max_length=2, choices=gender_choice,default="M")
    subject = models.ManyToManyField(Subject,verbose_name="辅导科目")
    info1 = models.TextField(verbose_name="子女额外信息描述", blank = True,)
    #家教信息
    gender2 = models.CharField(verbose_name="家教性别要求", max_length = 2,choices = (("N","男女不限"),("M","男"),("F","女")),default = "N")
    site = models.CharField(verbose_name="教学地点",max_length=10,choices=(('home',"家教上门"),('school',"学生上门")),default="home")
    from_time = models.DateField(verbose_name="起始时间")
    to_time = models.DateField(verbose_name="结束时间")
    info2 = models.TextField(verbose_name="家教额外要求", blank = True)
    salary = models.FloatField(verbose_name="薪水(元/小时)",null=True, blank=True)
    info3 = models.TextField(verbose_name="补充说明",blank = True)
    pub_date = models.DateTimeField(auto_now_add=True)
    valid_days = models.IntegerField(verbose_name="表单有效期(天)",default=30)
    class Meta:
        ordering = ['-pub_date',"salary"]
    def __unicode__(self):
        return self.user.username+str(self.pub_date)
#家教发布求职表单
class AskEmploy(models.Model):
    user = models.ForeignKey(User,blank=True,null=True)
    is_visible = models.BooleanField(default=True)
    from_time = models.DateField(verbose_name="起始时间")
    to_time = models.DateField(verbose_name="结束时间")
    info = models.TextField(verbose_name="额外要求")
    pub_date = models.DateTimeField(auto_now_add=True)
    salary = models.FloatField(verbose_name="薪水(元/小时)",null=True, blank=True)
    subject = models.ManyToManyField(Subject,verbose_name="科目")
    valid_days = models.IntegerField(verbose_name="表单有效期(天)",default=30)
    class Meta:
	ordering= ['-pub_date']
    def __unicode__(self):
	return self.user.username + str(self.pub_date)

#家教经历分享
class Exp(models.Model):
    user = models.ForeignKey(User,blank=True,null=True)
    title = models.CharField(verbose_name="标题",max_length=20,
      error_messages={
	'required':"标题不能为空",
    })
    content = models.TextField(verbose_name="内容",blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
	ordering = ['-pub_date']
    def __unicode__(self):
	return self.title
#留言
class Message(models.Model):
    is_read = models.BooleanField(default=False)
    from_user = models.ForeignKey(User,related_name="sendmessage")
    to_user = models.ForeignKey(User,related_name="receivemessage")
    content = models.TextField(verbose_name="内容",blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
	ordering = ['-pub_date']
    def __unicode__(self):
	return self.from_user.username + " send message to "+self.to_user.username
#评论
class Comment(models.Model):
    is_read = models.BooleanField(default=False)
    from_user = models.ForeignKey(User,related_name="sendcomment")
    to_user = models.ForeignKey(User,related_name="receivecomment")
    content = models.TextField(verbose_name="内容",blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    class Meta:
	ordering = ['-pub_date']
    def __unicode__(self):
	return self.from_user.username + " give a comment to "+self.to_user.username
#寻求雇佣
class Hire(models.Model):
    is_read = models.BooleanField(default=False)
    from_user = models.ForeignKey(User,related_name="hire_from")
    to_user = models.ForeignKey(User,related_name="hire_to")   
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
	ordering = ['-pub_date']
    def __unicode__(self):
	return self.from_user.username + " have a relationship with "+self.to_user.username

