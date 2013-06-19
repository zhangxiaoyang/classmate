#-*- coding: utf-8 -*-
# Create your views here.
# http://blog.csdn.net/liushuaikobe/article/details/8453716
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode  
import hashlib, time
import xml.etree.ElementTree as ET  
from models import *
import urllib2,urllib,httplib
import json
# 百度地图api
class xBaiduMap:
    def __init__(self,key='61b3496998c453868a95f9a2e3cc477f'):
        self.host='http://api.map.baidu.com'
        self.path='/geocoder?'
        self.param={'address':None,'output':'json','key':key,'location':None,'city':None}
    def getLocation(self,address,city=None):
        rlt=self.geocoding('address',address,city)
        if rlt!=None:
            l=rlt['result']
            if isinstance(l,list):
                return None
            return l['location']['lat'],l['location']['lng']
    def getAddress(self,lat,lng):
        rlt=self.geocoding('location',"{0},{1}".format(lat,lng))
        if rlt!=None:
            l=rlt['result']
            return l['formatted_address']
            #Here you can get more details about the location with 'addressComponent' key
            #ld=rlt['result']['addressComponent']
            #print(ld['city']+';'+ld['street'])
    def geocoding(self,key,value,city=None):
        if key=='location':
            if 'city' in self.param:
                del self.param['city']
            if 'address' in self.param:
                del self.param['address']
        elif key=='address':
            if 'location' in self.param:
                del self.param['location']
            if city==None and 'city' in self.param:
                del self.param['city']
            else:
                self.param['city']=city
        self.param[key]=value
        r=urllib.urlopen(self.host+self.path+urllib.urlencode(self.param))
        rlt=json.loads(r.read())
        if rlt['status']=='OK':
            return rlt
        else:
            #print "Decoding Failed"
            return None

def checkSignature(request):  
    TOKEN = 'zhangxiaoyang'  
    signature = request.GET.get('signature', None)  
    timestamp = request.GET.get('timestamp', None)  
    nonce = request.GET.get('nonce', None)  
    echoStr = request.GET.get('echostr',None)  
  
    token = TOKEN  
    tmpList = [token,timestamp,nonce]  
    tmpList.sort()  
    tmpstr = "%s%s%s" % tuple(tmpList)  
    tmpstr = hashlib.sha1(tmpstr).hexdigest()  
    if tmpstr == signature:  
        return echoStr  
    else:  
        return None 
@csrf_exempt  
def validate(request):  
    if request.method == 'GET':    
        response = HttpResponse(checkSignature(request),content_type="text/plain")  
        return response  
    elif request.method == 'POST':  
        response = HttpResponse(responseMsg(request),content_type="application/xml")  
        return response  
    else:  
        return None
 
def parseText(msg):
    querystr = msg.get('Content').strip()
    res = ''    
    openid = msg.get('FromUserName')
    classs = [i for i in Student.objects.filter(weixin=openid)][0].classs
    
    if querystr in ['帮助', 'help']:
        res = '= 小窗为您服务 =\n'
        res += '- 发送「同学姓名」查看其信息\n'
        res += '- 发送「所有/list」查看所有同学姓名\n'
        res += '- 发送「地理位置」修改当前位置\n'
        res += '- 发送「帮助/help」查看帮助\n'
        res += '- 你知道吗, 我还可以和你聊天呢, 随意调戏不客气~'
        return res
    elif querystr.lower() in ['所有', 'list']:
        for i in Student.objects.filter(classs=classs):
            res += i.name + '\n'
        return res
      
    # 返回查询的同学
    empty = True
    for i in Student.objects.filter(classs=classs, name=querystr):
        #lng  = i.position.split('(')[1].split(',')[0]
        #lat  = i.position.split('(')[1].split(',')[1].replace(')','')
        res += '[姓名]' + i.name + '\n' 
        res += '[学号]' + i.studentnum + '\n'
        if i.birthday != '':
            birth = ''
            if i.birthday[0] == 'g':birth = i.birthday[1:]+'(公历)'
            else:birth = i.birthday[1:]+'(农历)'
            res += '[破壳日]' + birth + '\n'
        addr = i.position.split('(')[0]
        res += '[地理位置]' + addr + '\n'
        if i.phone != '': res += '[联系方式]' + i.phone + '\n'
        if i.qq != '': res += '[QQ]' + i.qq + '\n'
        if i.weibo != '': res += '[微博]' + i.weibo + '\n'
        if i.mail != '': res += '[E-mail]' + i.mail + '\n'
        res += '\n'
        empty = False
    if empty: res = getAutoResponse(querystr)
    return res

def responseMsg(request):  
    rawStr = smart_str(request.raw_post_data)  
    msg = parseMsgXml(ET.fromstring(rawStr))
    openid = msg.get('FromUserName')
    res = ''
    msgtype = str(msg.get('MsgType'))
    
    if len([i for i in Student.objects.filter(weixin=openid)]) == 0:
        res = '您的OpenID: ' + openid + '\n小窗等不及了, 快加入我们吧: http://tongchuang.duapp.com'
    elif 'voice' == msgtype:
        res = '声音啥的小窗真的听不懂呀~'
    elif 'image' == msgtype:
        res = '小窗不近美色不看帅哥~'
    elif 'text' == msgtype:
        res = parseText(msg)
    elif 'location' == msgtype:
        lng = float(msg.get('Location_Y'))*1.0000568461567492425578691530827
        lat = float(msg.get('Location_X'))*1.0002012762190961772159526495686
        res = '%s(%f,%f)' % (xBaiduMap().getAddress(lat, lng),lng,lat)
        Student.objects.filter(weixin=openid).update(
            position=res)
        res = '当前位置成功修改为: ' + res 
    else:
        res = '这是神马东东, 来点动作片吧~'
    return getReplyXml(msg, res)
      
def getAutoResponse(s):
    res = '啥意思?'
    try:
        response = urllib2.urlopen('http://www.maiguangyang.com/api/msg.asp?Message='+s, timeout=10)
        res = response.read()
        if '@' in res: res = '啥意思?'
        res = res.replace('小y', '小窗').replace('小Y', '小窗')
    except:pass
    return res
    
def parseMsgXml(rootElem):  
    msg = {}  
    if rootElem.tag == 'xml':  
        for child in rootElem:  
            msg[child.tag] = smart_str(child.text)  
    return msg   
  
def getReplyXml(msg,replyContent):  
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";  
    extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',replyContent)  
    return extTpl 