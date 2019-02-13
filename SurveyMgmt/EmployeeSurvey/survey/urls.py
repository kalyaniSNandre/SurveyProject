from django.conf.urls import url
from . import views
from django.urls import path

# SET THE NAMESPACE!
app_name = 'survey'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    # url(r'^survey/(?P<id>\d+)/$', views.survey_detail, name='survey_detail'),
    url(r'^my_surveys/$', views.EmployeeSurveys.as_view(), name='my_surveys'),
    url(r'^my_surveys/(?P<id>[-\w]+)/$', views.survey_detail, name='detail'),
    url(r'^confirm/(?P<uuid>\w+)/$', views.confirm, name='confirmation')
]
