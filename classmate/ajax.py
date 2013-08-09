#-*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import sys
import json
from models import *
from zhyserver.settings import *
from PIL import Image
from bae.core import const
from bae.api import bcs
from cStringIO import StringIO
import urllib2
import re

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
  
def query_login(request):
    classid = request.GET.get('classid')
    res = ''
    for i in Class.objects.filter(classid=int(classid)):
        res = i.department.college.colname + ' ' + i.classnum 
        break
    return HttpResponse(json.dumps(res))   

def upload(request, studentid):
    filename = str(request.FILES['Filedata'].name)
    ext = filename.split('.')[-1]
    HOST = const.BCS_ADDR
    AK = const.ACCESS_KEY
    SK = const.SECRET_KEY
    bname = 'mediaavatar'
    baebcs = bcs.BaeBCS(HOST, AK, SK)
    data = request.FILES['Filedata'].read()

    img = Image.open(StringIO(data))
    img = img.resize((70, 70), Image.ANTIALIAS)
    img = img.convert('RGB')
    data = StringIO()
    img.save(data, 'jpeg')
    try:del_object(bname, '/'+str(studentid)+'.jpg')
    except:pass
    baebcs.put_object(bname, '/'+str(studentid)+'.jpg', data.getvalue())
    return HttpResponse(json.dumps(MEDIA_URL+str(studentid)+'.jpg')) 
  
 # album
def query_album(request):
    qq = request.GET.get('qq')
    agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
    res = ''
    # get route
    route = ''
    error = False
    try:
        url = 'http://route.store.qq.com/GetRoute?UIN='+qq
        req = urllib2.Request(url = url, headers = {'User-Agent':agent})
        response = urllib2.urlopen(req, timeout=10)
        res = response.read()
        pt = re.compile(r'<nu>(?P<url>.*?)</nu>', re.IGNORECASE)
        route = re.search(pt, res).group('url')
        route = route.split('.')[0]
    except:
        error = 'Error ocurred!'
        return HttpResponse(json.dumps(error))

    # 获取js传递过来的cookie
    #!!!!!!!
    
    # get album list
    try:
        url = 'http://'+route+'alist.photo.qq.com/fcgi-bin/fcg_list_album?uin='+qq
        req = urllib2.Request(url = url, headers = {'User-Agent':agent})
        response = urllib2.urlopen(req, timeout=10)
        res = response.read()
    except:
        error = 'Error ocurred!'
        return HttpResponse(json.dumps(error))
    if '<err>' in res:
        error = 'Login your qzone<http://qzone.qq.com> first!'
        return HttpResponse(json.dumps(res))
    #pt = re.compile(r'<createtime>(?P<createtime>.*?)</createtime>.*?<name>(?P<name>.*?)</name>.*?<pre>(?P<pre>.*?)</pre>', re.IGNORECASE)
    
    # get photo
    # hz plist.photo.qq.com/fcgi-bin/fcg_list_photo?uin=460639264&albumid=5c08731a-6f3d-49db-9f7f-06e3c93e93ca
    return HttpResponse(json.dumps(res))