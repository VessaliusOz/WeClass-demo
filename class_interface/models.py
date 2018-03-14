# -*-coding:utf-8-*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TeacherProfile(models.Model):
    class Meta:
        verbose_name = '老师'
        verbose_name_plural = verbose_name
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    school_num = models.CharField('学工号', max_length=30, default=None, null=True, blank=False)

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        TeacherProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_teacher_profile(sender, instance, **kwargs):
    instance.teacherprofile.save()


class Profession(models.Model):
    class Meta:
        verbose_name = '专业'
        verbose_name_plural = verbose_name
    name = models.CharField('专业', default=None, null=True, blank=False, max_length=20)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
    name = models.CharField('课程名称', default=None, null=True, blank=False, max_length=20)
    teacher = models.ForeignKey(TeacherProfile, default=None, null=True, blank=False, verbose_name='任课老师')

    def __unicode__(self):
        return self.name


class CourseData(models.Model):
    class Meta:
        verbose_name = '课程资料'
        verbose_name_plural = verbose_name
    name = models.CharField('资料名称', default=None, null=True, blank=False, max_length=20)
    course_file = models.FileField(upload_to='files/')
    course = models.ForeignKey(Course, verbose_name='相关课程', default=None, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
    name = models.CharField('姓名', max_length=10, default=None, null=True, blank=False)
    school_num = models.CharField('学号', max_length=20, default=None, null=True, blank=False)
    password = models.CharField('密码', max_length=50, default=None, null=True, blank=False)
    course = models.ManyToManyField(Course, verbose_name='选修课程')
    session = models.CharField("会话数据", max_length=50, default=None, null=True, blank=False)
    is_login = models.BooleanField("是否在线", default=False)

    def __unicode__(self):
        return self.name


class Test(models.Model):
    class Meta:
        verbose_name = '测试'
        verbose_name_plural = verbose_name
    course = models.ForeignKey(Course, verbose_name='课程', default=None, null=True, on_delete=models.SET_NULL)
    name = models.CharField('测试名称', max_length=50, default=None, null=True)
    is_on = models.BooleanField('是否开始', default=False)
    is_used = models.BooleanField('是否已经测试过', default=False)
    duration = models.IntegerField('测试时长', default=900, help_text='以秒为单位')

    def __unicode__(self):
        return self.name

    def reverse_status(self):
        self.is_on = not self.is_on


class Problem(models.Model):
    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
    test = models.ForeignKey(Test, verbose_name='测试', default=None, null=True, on_delete=models.SET_NULL)
    name = models.TextField('题目')
    sequence = models.IntegerField('题目序号', default=1, null=True, blank=False)
    correct_answer = models.CharField('正确答案', max_length=300, default=None, null=True)

    def __unicode__(self):
        return self.test.name + '问题' + str(self.sequence)


class Answer(models.Model):
    class Meta:
        verbose_name = '答案'
        verbose_name_plural = verbose_name
    name = models.CharField('答案内容', max_length=300, default=None, null=True)
    label = models.CharField('答案所在选项', max_length=1, default=None, null=True)
    problem = models.ForeignKey(Problem, verbose_name='题目', default=None, null=True, blank=False)
    selected_number = models.IntegerField('选择数目', default=0, null=True, blank=False)

    def __unicode__(self):
        return self.problem.__unicode__() + ' 选项' + str(self.label)


class Homework(models.Model):
    class Meta:
        verbose_name = '作业'
        verbose_name_plural = verbose_name
    student = models.ForeignKey(Student, verbose_name='学生', null=True, default=None, on_delete=models.CASCADE)
    homework_img = models.ImageField('作业图片', upload_to='homework_images/')
    name = models.CharField('作业名称', max_length=300, default=None, null=True)

    def __unicode__(self):
        return self.student.__unicode__() + ': ' + self.name
