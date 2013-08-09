from django.conf.urls import *
from zhyserver.settings import *
from django.conf.urls.static import static
urlpatterns = patterns('classmate.views',
    url(r'^$', 'index'),
    url(r'^index/', 'index'),
    url(r'^test/', 'test'),
    url(r'^weixin/', 'weixin'),
    url(r'^album/', 'album'),
    url(r'^sms/', 'sms'),
    url(r'^bye/', 'bye'),

    url(r'^createclass/', 'create_class'),
    url(r'^changeclass/(\d+)/$', 'change_class'),
    url(r'^enterclass/(\d+)/$', 'enter_class'),

    url(r'^createstudent/(\d+)/$', 'create_student'),
    url(r'^changestudent/(\d+)/$', 'change_student'),
) + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += patterns('classmate.ajax',
    url(r'^ajax/queryclass/', 'query_class'),
    url(r'^ajax/createclass/', 'create_class'),
    url(r'^ajax/querycollege/', 'query_college'),
    url(r'^ajax/querydepartment/', 'query_department'),
    url(r'^ajax/querylogin/', 'query_login'),
    url(r'^ajax/upload/(\d+)/$', 'upload'),
    
    url(r'^ajax/queryalbum/', 'query_album'),
)

urlpatterns += patterns('classmate.interface',
    url(r'^interface/validate/', 'validate'),
)