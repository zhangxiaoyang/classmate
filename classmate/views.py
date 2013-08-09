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
import json
from bae.core import const
from bae.api import bcs
#import urllib2
def index(request):
    classes = []
    for i in Class.objects.all():
        classes.append('%s/%s' % (i.department.college.colname, i.classnum))
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals())
def bye(request):
    logout(request)    
    classes = []
    for i in Class.objects.all():
        classes.append('%s/%s' % (i.department.college.colname, i.classnum+'班'))
    return render_to_response('index.html', locals())
def weixin(request):
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals())
def album(request):
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals())
def sms(request):
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals())
def test(request):
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals())
'''
Class
'''
def create_class(request):
    try: studentid = [i for i in Student.objects.all()][-1].studentid+1
    except: studentid = 1
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
                birthday=form.cleaned_data['birthday'],
                weixin=form.cleaned_data['weixin'])
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
    HOST = const.BCS_ADDR
    AK = const.ACCESS_KEY
    SK = const.SECRET_KEY
    bname = 'mediaavatar'
    baebcs = bcs.BaeBCS(HOST, AK, SK)
    e, d = baebcs.list_objects(bname)
    imgids = []
    d = str(d).replace('\'', '\"')
    d = json.loads(d)
    for i in d:
        try:
            imgid = int(i.replace('.jpg','').replace('/',''))
            imgids.append(imgid)
        except:pass
            
    if str(classid) == str(request.user):
        content.update({'validate':False, 'profile':True})

        for i in Student.objects.filter(classs=Class(classid=classid)):
            try:
                pt = re.compile(r'\(\d+\.\d+,\d+\.\d+\)')
                s = pt.findall(i.position)[-1].replace('(','').replace(')','')
                lng = s.split(',')[0]
                lat = s.split(',')[1]
                addr = i.position.replace('('+lng+','+lat+')', '')
            except:
                addr = '暂无'
                lng = '10.0'
                lat = '10.0'
            if i.birthday == '':birth = '暂无'
            elif i.birthday[0] == 'g':birth = i.birthday[1:]+'(公历)'
            else:birth = i.birthday[1:]+'(农历)'

            if i.name == '': i.name = '暂无'
            if i.qq == '': i.qq = '暂无'
            if i.weibo == '': i.weibo = '暂无'
            if i.phone == '': i.phone = '暂无'
            if i.mail == '': i.mail = '暂无'
            if i.weixin == '': i.weixin = '暂无'
            if i.studentid in imgids:
                imgid = str(i.studentid)
            else:imgid = 'error'
            stu.update({str(i.studentid):{'studentnum':i.studentnum,\
                'name':i.name, 'qq':i.qq,\
                'weibo':i.weibo, 'phone':i.phone, 'mail':i.mail,\
                'birth':birth, 'addr':addr, 'lng':lng, 'lat':lat, 'imgid':imgid, 'weixin':weixin}})

    elif request.method == 'POST':
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
                    try:
                        pt = re.compile(r'\(\d+\.\d+,\d+\.\d+\)')
                        s = pt.findall(i.position)[-1].replace('(','').replace(')','')
                        lng = s.split(',')[0]
                        lat = s.split(',')[1]
                        addr = i.position.replace('('+lng+','+lat+')', '')
                    except:
                        addr = '暂无'
                        lng = '10.0'
                        lat = '10.0'
                        
                    if i.birthday == '':birth = '暂无'
                    elif i.birthday[0] == 'g':birth = i.birthday[1:]+'(公历)'
                    else:birth = i.birthday[1:]+'(农历)'

                    if i.name == '': i.name = '暂无'
                    if i.qq == '': i.qq = '暂无'
                    if i.weibo == '': i.weibo = '暂无'
                    if i.phone == '': i.phone = '暂无'
                    if i.mail == '': i.mail = '暂无'
                    if i.studentid in imgids:
                        imgid = str(i.studentid)
                    else:imgid = 'error'
                    stu.update({str(i.studentid):{'studentnum':i.studentnum,\
                        'name':i.name, 'qq':i.qq,\
                        'weibo':i.weibo, 'phone':i.phone, 'mail':i.mail,\
                        'birth':birth, 'addr':addr, 'lng':lng, 'lat':lat, 'imgid':imgid, 'weixin':weixin}})
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
    studentid = [i for i in Student.objects.all()][-1].studentid+1
    if str(classid) != str(request.user):
        return HttpResponseRedirect('/')
    classid = int(classid)
    if request.method == 'POST':
        form = StudentForm(request.POST, classid=classid)
        if form.is_valid():
            s = Student(studentid=studentid,studentnum=form.cleaned_data['studentnum'],
                classs=Class(classid=classid),
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                qq=form.cleaned_data['qq'],
                weibo=form.cleaned_data['weibo'],
                mail=form.cleaned_data['mail'],
                position=form.cleaned_data['position'],
                birthday=form.cleaned_data['birthday'],
                weixin=form.cleaned_data['weixin'])
            s.save()  
            return HttpResponseRedirect('/enterclass/'+str(classid))
    else: form = StudentForm(classid=classid)
    
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals(), context_instance=RequestContext(request))
@login_required(login_url='/')
def change_student(request, studentid):
    classid = [i for i in Student.objects.filter(studentid=studentid)][-1].classs
    classid = int(classid.classid)
    if str(classid) != str(request.user):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = StudentForm(request.POST, classid=None)
        if form.is_valid():
            s = Student.objects.filter(studentid=studentid).update(
                studentnum=form.cleaned_data['studentnum'],
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                qq=form.cleaned_data['qq'],
                weibo=form.cleaned_data['weibo'],
                mail=form.cleaned_data['mail'],
                position=form.cleaned_data['position'],
                birthday=form.cleaned_data['birthday'],
                weixin=form.cleaned_data['weixin'])
            return HttpResponseRedirect('/enterclass/'+str(classid))
    else:
        s = [i for i in Student.objects.filter(studentid=studentid)][0]
        form = StudentForm({'studentnum':s.studentnum,\
                'name':s.name, 'qq':s.qq, 'weibo':s.weibo,\
                'phone':s.phone, 'mail':s.mail, 'birthday':s.birthday,
                'position':s.position,'weixin':s.weixin}, classid=None)
    return render_to_response(sys._getframe().f_code.co_name + '.html', locals(), context_instance=RequestContext(request))
