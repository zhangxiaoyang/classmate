from django.conf.urls import *

urlpatterns = patterns('classmate.views',
    url(r'^$', 'index'),
    url(r'^index/', 'index'),
    url(r'^test/', 'test'),

    url(r'^createclass/', 'create_class'),
    url(r'^changeclass/(\d+)/$', 'change_class'),
    url(r'^enterclass/(\d+)/$', 'enter_class'),

    url(r'^createstudent/(\d+)/$', 'create_student'),
    url(r'^changestudent/(\d+)/$', 'change_student'),
)

urlpatterns += patterns('classmate.ajax',
    url(r'^ajax/queryclass/', 'query_class'),
    url(r'^ajax/createclass/', 'create_class'),
    url(r'^ajax/querycollege/', 'query_college'),
    url(r'^ajax/querydepartment/', 'query_department'),
)