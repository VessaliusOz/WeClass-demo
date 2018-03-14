# -*-coding: utf-8 -*-
import xadmin
from class_interface.models import *


class StudentAdmin(object):
    style_fields = {'course': 'm2m_transfer'}


class AnswerInline(object):
    model = Answer
    extra = 5


class CourseDataInline(object):
    model = CourseData
    extra = 10


class ProblemAdmin(object):
    inlines = [AnswerInline, ]
    inline_style = 'tab'


class CourseAdmin(object):
    inlines = [CourseDataInline,]
    inline_style = 'tab'


xadmin.site.register(TeacherProfile)
xadmin.site.register(Student, StudentAdmin)
xadmin.site.register(Test)
xadmin.site.register(Problem, ProblemAdmin)
xadmin.site.register(Answer)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseData)
xadmin.site.register(Homework)
