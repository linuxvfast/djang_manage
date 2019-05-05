from django.conf.urls import url
from cmdb import views

urlpatterns = [
    url(r'^add$', views.add_info), #为表添加信息
    url(r'^business$', views.business),
    url(r'^host$', views.hosts),
    url(r'^test_ajax$', views.test_ajax),
    url(r'^edit_ajax$', views.edit_ajax),
    url(r'^add_more_to_more$', views.add_more_to_more),
]