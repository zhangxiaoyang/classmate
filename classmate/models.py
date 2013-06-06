from django.db import models

# Create your models here.
# CREATE DATABASE `classmate` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;

class Province(models.Model):
    proid   = models.IntegerField(primary_key=True)
    proname = models.CharField(max_length=20)

class College(models.Model):
    province = models.ForeignKey(Province, db_column='proid')
    colid    = models.IntegerField(primary_key=True)
    colname  = models.CharField(max_length=128)

class Department(models.Model):
    depid   = models.AutoField(primary_key=True)
    college = models.ForeignKey(College, db_column='colid')
    depname = models.CharField(max_length=128)

class Class(models.Model):
    classid = models.AutoField(primary_key=True)
    classnum = models.CharField(max_length=20)
    department = models.ForeignKey(Department, db_column='depid')
    slogon    = models.TextField()
    year    = models.CharField(max_length=4)
    quest1  = models.TextField()
    quest2  = models.TextField()
    quest3  = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()
    answer3 = models.TextField()

class Student(models.Model):
    studentid = models.AutoField(primary_key=True)
    studentnum = models.CharField(max_length=20)
    classs    = models.ForeignKey(Class, db_column='classid')
    name      = models.CharField(max_length=20)
    phone     = models.CharField(max_length=20)
    qq        = models.CharField(max_length=20)
    weibo     = models.CharField(max_length=20)
    mail      = models.EmailField()
    position  = models.TextField()
    birthday  = models.CharField(max_length=9)