# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from class_interface.models import *
from class_interface.form import HomeworkForm


def attach_http_status(json_obj, code):
    if code == 200:
        json_obj.update({'code': code, 'msg': 'success'})
    if code == 500:
        json_obj.update({'code': code, 'msg': 'failed'})
    if code == 405:
        json_obj.update({'code': code, 'msg': 'method not allowed'})
    return json_obj


def index(request):
    current_status = Student.objects.first()
    course_list = []
    for course in current_status.course.all():
        course_info = dict(name=course.name, id=course.pk)
        course_list.append(course_info)
    json_dict = attach_http_status({'courses': course_list}, 200)
    return JsonResponse(json_dict)


def get_all_test(request, pk):
    course = Course.objects.get(pk=pk)
    test_list = []
    for test in course.test_set.all():
        test_info = dict(name=test.name, id=test.pk, duration=test.duration, is_on=test.is_on, is_used=test.is_used)
        test_list.append(test_info)
    json_dict = attach_http_status({'tests': test_list}, 200)
    return JsonResponse(json_dict)


def get_current_test(request, pk):
    test = Test.objects.get(pk=pk)
    problem_list = []
    for problem in test.problem_set.all():
        problem_info = dict(name=problem.name, id=problem.pk, correctAnswer=problem.correct_answer, answers=[])
        for answer in problem.answer_set.all():
            answer_info = dict(name=answer.name, choice=answer.label)
            problem_info['answers'].append(answer_info)
        problem_list.append(problem_info)
    json_dict = attach_http_status({'problems': problem_list}, 200)
    return JsonResponse(json_dict)


# 选项计数
def count_up(request, pk, choice):
    problem = Problem.objects.get(pk=pk)
    answer = problem.answer_set.get(label=choice)
    answer.selected_number += 1
    json_dict = attach_http_status({}, 200)
    return JsonResponse(json_dict)


# 统计正确率
def correct_rate(request, pk):
    problem = Problem.objects.get(pk=pk)
    answers = problem.answer_set.all()
    number_dict = dict(rates=[], correct_answer=problem.correct_answer.upper())
    for answer in answers:
        answer_num = dict(number=answer.selected_number, label=answer.label.upper())
        number_dict['rates'].append(answer_num)
    json_dict = attach_http_status(number_dict, 200)
    return JsonResponse(json_dict)


# 课程列表, 以及作业列表
def get_all_course_info(request):
    courses = Course.objects.all()
    courses_list = []
    for course in courses:
        course_info = dict(name=course.name, id=course.pk)
        courses_list.append(course_info)
    json_dict = attach_http_status({'courses': courses_list}, 200)
    return JsonResponse(json_dict)


# 课程资料数据
def get_current_course_data(request, pk):
    course = Course.objects.get(pk=pk)
    data_list = []
    for data in course.coursedata_set.all():
        data_info = dict(name=data.name, fileUrl=data.course_file.url, id=data.pk)
        data_list.append(data_info)
    json_dict = attach_http_status({'data': data_list, 'name': course.name}, 200)
    return JsonResponse(json_dict)


# 改变标志位
def reverse_the_status(request, pk):
    current_test = Test.objects.get(pk=pk)
    current_test.reverse_status()
    current_test.save()
    json_dict = attach_http_status({}, 200)
    return JsonResponse(json_dict)


def get_the_status(request, pk):
    current_test = Test.objects.get(pk=pk)
    status = current_test.is_on
    json_dict = attach_http_status({'status': status}, 200)
    return JsonResponse(json_dict)


def post_homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            homework_img = request.FILES.get('homework_img')
            student = Student.objects.first()
            if name and homework_img:
                homework_obj = Homework.objects.create(name=name, homework_img=homework_img, student=student)
                homework_obj.save()
                json_dict = attach_http_status({}, 200)
                return JsonResponse(json_dict)
        else:
            json_dict = attach_http_status({}, 500)
            return JsonResponse(json_dict)
    else:
        json_dict = attach_http_status({}, 405)
        return JsonResponse(json_dict)
