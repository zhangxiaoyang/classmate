#-*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import sys
import re
from models import *
from forms import *

def index(request):
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals())
def test(request):
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals())
'''
Class
'''
def create_class(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            depid = int(re.sub(r'[^0-9]','',form.cleaned_data['department']))
            c = Class(classnum=form.cleaned_data['classnum'],
                department=Department(depid=depid),
                year=form.cleaned_data['year'],
                slogon=form.cleaned_data['slogon'],
                quest1=form.cleaned_data['quest1'],
                quest2=form.cleaned_data['quest2'],
                quest3=form.cleaned_data['quest3'],
                answer1=form.cleaned_data['answer1'],
                answer2=form.cleaned_data['answer2'],
                answer3=form.cleaned_data['answer3'])
            c.save()
            classid = [i for i in Class.objects.all()][-1].classid
            u = User.objects.create_user(str(classid))
            s = Student(studentnum=form.cleaned_data['studentnum'],
                classs=Class(classid=classid),
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                qq=form.cleaned_data['qq'],
                weibo=form.cleaned_data['weibo'],
                mail=form.cleaned_data['mail'],
                position=form.cleaned_data['position'],
                birthday=form.cleaned_data['birthday'])
            s.save()  
            return HttpResponseRedirect('/')
    else: form = RegisterForm()
    province = []
    tmp = []
    for i in Province.objects.all():
        province.append({'name':i.proname, 'id':int(i.proid)})
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/')
def change_class(request, classid):
    if str(classid) != str(request.user):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            classid = int(classid)
            c = Class.objects.filter(classid=classid).update(
                slogon=form.cleaned_data['slogon'],
                quest1=form.cleaned_data['quest1'],
                quest2=form.cleaned_data['quest2'],
                quest3=form.cleaned_data['quest3'],
                answer1=form.cleaned_data['answer1'],
                answer2=form.cleaned_data['answer2'],
                answer3=form.cleaned_data['answer3'])
            return HttpResponseRedirect('/')
    else:
        c = [i for i in Class.objects.filter(classid=classid)][0]
        form = ClassForm({'slogon':c.slogon, 'quest1':c.quest1,\
            'quest2':c.quest2, 'quest3':c.quest3, 'answer1':c.answer1,\
            'answer2':c.answer2, 'answer3':c.answer3})
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals(), context_instance=RequestContext(request))

def enter_class(request, classid):
    content = {'validate':True, 'profile':False, 'classid':classid}
    quest   = {}
    stu     = {}
    if request.method == 'POST':
        print request.POST
        form = ValidateForm(request.POST)
        if form.is_valid():
            answer1 = form.cleaned_data['answer1']
            answer2 = form.cleaned_data['answer2']
            answer3 = form.cleaned_data['answer3']
            c = [i for i in Class.objects.filter(classid=classid)][0]
            if answer1.encode('utf8') in c.answer1.split('|') and\
                answer2.encode('utf8') in c.answer2.split('|') and\
                answer3.encode('utf8') in c.answer3.split('|'):
                content.update({'validate':False, 'profile':True})
                for i in Student.objects.filter(classs=Class(classid=classid)):
                    addr = i.position.split('(')[0]
                    lng  = i.position.split('(')[1].split(',')[0]
                    lat  = i.position.split('(')[1].split(',')[1].replace(')','')
                    
                    if i.birthday == '':birth = '暂无'
                    elif i.birthday[0] == 'g':birth = i.birthday[1:]+'(公历)'
                    else:birth = i.birthday[1:]+'(农历)'

                    if i.name == '': i.name = '暂无'
                    if i.qq == '': i.qq = '暂无'
                    if i.weibo == '': i.weibo = '暂无'
                    if i.phone == '': i.phone = '暂无'
                    if i.mail == '': i.mail = '暂无'
                    stu.update({str(i.studentid):{'studentnum':i.studentnum,\
                        'name':i.name, 'qq':i.qq,\
                        'weibo':i.weibo, 'phone':i.phone, 'mail':i.mail,\
                        'birth':birth, 'addr':addr, 'lng':lng, 'lat':lat}})
                user =  authenticate(username=str(classid))
                login(request, user)   
    c = [i for i in Class.objects.filter(classid=classid)][0]
    quest.update({'answer1':[c.quest1,'']})
    quest.update({'answer2':[c.quest2,'']})
    quest.update({'answer3':[c.quest3,'']})   
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals(), context_instance=RequestContext(request))

'''
Student
'''
@login_required(login_url='/')
def create_student(request, classid):    
    if str(classid) != str(request.user):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            classid = int(classid)
            s = Student(studentnum=form.cleaned_data['studentnum'],
                classs=Class(classid=classid),
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                qq=form.cleaned_data['qq'],
                weibo=form.cleaned_data['weibo'],
                mail=form.cleaned_data['mail'],
                position=form.cleaned_data['position'],
                birthday=form.cleaned_data['birthday'])
            s.save()  
            return HttpResponseRedirect('/')
    else: form = StudentForm()
    
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals(), context_instance=RequestContext(request))
@login_required(login_url='/')
def change_student(request, studentid):
    if str(classid) != str(request.user):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            s = Student.objects.filter(studentid=studentid).update(
                studentnum=form.cleaned_data['studentnum'],
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                qq=form.cleaned_data['qq'],
                weibo=form.cleaned_data['weibo'],
                mail=form.cleaned_data['mail'],
                position=form.cleaned_data['position'],
                birthday=form.cleaned_data['birthday'])
            return HttpResponseRedirect('/')
    else:
        s = [i for i in Student.objects.filter(studentid=studentid)][0]
        form = StudentForm({'studentnum':s.studentnum,\
                'name':s.name, 'qq':s.qq, 'weibo':s.weibo,\
                'phone':s.phone, 'mail':s.mail, 'birthday':s.birthday,
                'position':s.position})
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals(), context_instance=RequestContext(request))
