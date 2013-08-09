#-*- coding: utf-8 -*-
from django import forms
from models import *
import re

class RegisterForm(forms.Form):
    college    = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'点我选择','readonly':'readonly','style':'background-color:white'}),required=True)
    department = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'点我选择','readonly':'readonly','style':'background-color:white'}),required=True)
    classnum   = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'4~20个数字'}),required=True, min_length=4, max_length=20)
    year       = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'示例: 2012'}),required=True)
    slogon  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=False)

    studentnum  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'4~20个数字'}),required=True, min_length=4, max_length=20)
    name        = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'1~6个数字'}),required=True, min_length=1, max_length=6)
    qq          = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'7~20个数字'}),min_length=7, max_length=20,required=False)
    weibo       = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'7~20个数字'}),min_length=7, max_length=20,required=False)
    mail        = forms.EmailField(widget=forms.TextInput(attrs={'class':'span12'}),required=False)
    phone       = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'4~12个数字'}),min_length=4, max_length=12,required=False)
    birthday    = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'点我选择','readonly':'readonly','style':'background-color:white'}),required=False)
    position    = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'点我选择','readonly':'readonly','style':'background-color:white'}),required=True)
    weixin      = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'OpenID不是微信号, 是一串杂七杂八的字符'}),min_length=7, max_length=35,required=False)
    
    quest1  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'示例: 我们班的美女?'}),required=True)
    quest2  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
    quest3  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
    answer1 = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'示例: 小龙女|黄蓉|林志玲'}),required=True)
    answer2 = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
    answer3 = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
    def clean_classnum(self):
        try:
            classnum = self.cleaned_data['classnum']
            int(classnum)
            depid = int(re.sub(r'[^0-9]','',self.cleaned_data['department']))
        except:
            raise forms.ValidationError("classnum field error!")   
        if 0 != len(Class.objects.filter(classnum=classnum, department=Department(depid=depid))):
            raise forms.ValidationError("该班级已经被注册")
        else: return classnum

    def clean_year(self):
        try:
            year = self.cleaned_data['year']
            int(year)
            if len(year) != 4:
                raise forms.ValidationError("year field error!")
            else:
                return year
        except:raise forms.ValidationError("year field error!")
    def clean_studentnum(self):
        try:
            studentnum = self.cleaned_data['studentnum']
            int(studentnum)
            return studentnum
        except:raise forms.ValidationError("studentnum field error!")
    def clean_birthday(self):
        try:
            birthday = self.cleaned_data['birthday']
            if birthday.strip() == '': return ''
            int(birthday[1:])
            if len(birthday) != 9 or birthday[0] not in ['g','n']:
                raise forms.ValidationError("birthday field error!")
            else:
                return birthday
        except:raise forms.ValidationError("birthday field error!")
    def clean_phone(self):
        try:
            phone = self.cleaned_data['phone']            
            if phone.strip() == '': return ''
            int(phone)
            return phone
        except:raise forms.ValidationError("phone field error!")
    def clean_qq(self):
        try:
            qq = self.cleaned_data['qq']          
            if qq.strip() == '': return ''
            int(qq)
            return qq
        except:raise forms.ValidationError("qq field error!")
    def clean_weibo(self):
        try:
            weibo = self.cleaned_data['weibo']        
            if weibo.strip() == '': return ''
            int(weibo)
            return weibo
        except:raise forms.ValidationError("weibo field error!")
class ValidateForm(forms.Form):
    answer1 = forms.CharField(required=True)
    answer2 = forms.CharField(required=True)
    answer3 = forms.CharField(required=True)

    def clean_answer1(self):
        try:
            answer1 = self.cleaned_data['answer1'].strip()
            if answer1 == '':
                raise forms.ValidationError("answer1 field error!")
            else:return answer1
        except:raise forms.ValidationError("answer1 field error!")
    def clean_answer2(self):
        try:
            answer2 = self.cleaned_data['answer2'].strip()
            if answer2 == '':
                raise forms.ValidationError("answer2 field error!")
            else:return answer2
        except:raise forms.ValidationError("answer2 field error!")
    def clean_answer3(self):
        try:
            answer3 = self.cleaned_data['answer3'].strip()
            if answer3 == '':
                raise forms.ValidationError("answer3 field error!")
            else:return answer3
        except:raise forms.ValidationError("answer3 field error!")

class StudentForm(forms.Form):
    studentnum  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'4~20个数字'}),required=True, min_length=4, max_length=20)
    name        = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'1~6个数字'}),required=True, min_length=1, max_length=6)
    qq          = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'7~20个数字'}),min_length=7, max_length=20,required=False)
    weibo       = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'7~20个数字'}),min_length=7, max_length=20,required=False)
    mail        = forms.EmailField(widget=forms.TextInput(attrs={'class':'span12'}),required=False)
    phone       = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'4~12个数字'}),min_length=4, max_length=12,required=False)
    birthday    = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'点我选择','readonly':'readonly','style':'background-color:white'}),required=False)
    position    = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'点我选择','readonly':'readonly','style':'background-color:white'}),required=True)
    weixin      = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'OpenID不是微信号, 是一串杂七杂八的字符'}),min_length=7, max_length=35,required=False)
        
    def __init__(self, *args, **kwargs):
        self.classid = kwargs.pop('classid')
        super(StudentForm, self).__init__(*args, **kwargs)
    
    def clean_studentnum(self):
        try:
            studentnum = self.cleaned_data['studentnum']
            int(studentnum)
        except:
            raise forms.ValidationError("studentnum field error!")  
        if self.classid == None:
            return studentnum
        if 0 != len(Student.objects.filter(studentnum=studentnum, classs=Class(classid=self.classid))):
            raise forms.ValidationError("该学号已经被注册")
        else: return studentnum
        
    def clean_birthday(self):
        try:
            birthday = self.cleaned_data['birthday']
            if birthday.strip() == '': return ''
            int(birthday[1:])
            if len(birthday) != 9 or birthday[0] not in ['g','n']:
                raise forms.ValidationError("birthday field error!")
            else:
                return birthday
        except:raise forms.ValidationError("birthday field error!")
    def clean_phone(self):
        try:
            phone = self.cleaned_data['phone']            
            if phone.strip() == '': return ''
            int(phone)
            return phone
        except:raise forms.ValidationError("phone field error!")
    def clean_qq(self):
        try:
            qq = self.cleaned_data['qq']          
            if qq.strip() == '': return ''
            int(qq)
            return qq
        except:raise forms.ValidationError("qq field error!")
    def clean_weibo(self):
        try:
            weibo = self.cleaned_data['weibo']        
            if weibo.strip() == '': return ''
            int(weibo)
            return weibo
        except:raise forms.ValidationError("weibo field error!")

class ClassForm(forms.Form):
    slogon  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=False)
    quest1  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'示例: 我们班的美女?'}),required=True)
    quest2  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
    quest3  = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
    answer1 = forms.CharField(widget=forms.TextInput(attrs={'class':'span12','placeholder':u'示例: 小龙女|黄蓉|林志玲'}),required=True)
    answer2 = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
    answer3 = forms.CharField(widget=forms.TextInput(attrs={'class':'span12'}),required=True)
  