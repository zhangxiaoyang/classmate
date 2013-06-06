#-*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import sys
import json
from models import *

def query_class(request):
    classnum = request.GET.get('classnum')
    res = []
    res.append({'classnum':u'没有找到班级', 'detail':(u'创建专属%s班' % classnum)})
    for i in Class.objects.filter(classnum=classnum):
        line = {}
        detail = '%s/%s/%s' % (i.department.college.province.proname,\
            i.department.college.colname, i.department.depname)
        line.update({'classnum':classnum, 'classid':i.classid, 'detail':detail})
        res.append(line)
    return HttpResponse(json.dumps(res))

def create_class(request):
    return HttpResponse(json.dumps([{'state':'state', 'process':'process'}]))

def query_college(request):
    proid = request.GET.get('proid')
    res = []
    for i in College.objects.filter(province=proid):
        res.append({'name':i.colname, 'link':i.colid})
    return HttpResponse(json.dumps(res))   

def query_department(request):
    colid = request.GET.get('colid')
    res = []
    for i in Department.objects.filter(college=colid):
        res.append({'name':i.depname, 'link':i.depid})
    return HttpResponse(json.dumps(res))   