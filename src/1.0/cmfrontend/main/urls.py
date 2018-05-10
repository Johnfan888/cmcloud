"""CMC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, url
from main import views



urlpatterns = patterns('',
    url(r'^main/$', views.main, name="main"),
    url(r'^homepage/$', views.homepage, name="homepage"),
    url(r'^add/$', views.add, name="add"),
    url(r'^add_host/$', views.add_host, name="add_host"),
    url(r'^add_hostgroups/$', views.add_hostgroups, name="add_hostgroups"),
    url(r'^add_templates/$', views.add_templates, name="add_templates"),
    url(r'^add_itemgroups/$', views.add_itemgroups, name="add_itemgroups"),
    url(r'^add_items/$', views.add_items, name="add_items"),
    url(r'^add_triggers/$', views.add_triggers, name="add_triggers"),
    url(r'^add_action/$', views.add_action, name="add_action"),
    url(r'^add_action_child/$', views.add_action_child, name="add_action_child"),
    url(r'^monitoring/$', views.monitoring, name="monitoring"),
    url(r'^diagnosis/$', views.diagnosis, name="diagnosis"),
    url(r'^recovery/$', views.recovery, name="recovery"),
    url(r'^add_triggers_child/$', views.add_triggers_child, name="add_triggers_child"),
    url(r'^view_hostgroups/$', views.view_hostgroups, name="view_hostgroups"),
    url(r'^view_templates/$', views.view_templates, name="view_templates"),
    url(r'^view_host/$', views.view_host, name="view_host"),
    url(r'^view_action/$', views.view_action, name="view_action"),
    url(r'^view_itemgroups/$', views.view_itemgroups, name="view_itemgroups"),
    url(r'^view_items/$', views.view_items, name="view_items"),
    url(r'^view_triggers/$', views.view_triggers, name="view_triggers"),
    # url(r'^main/ajax/add/', views.ajax_test_add, name = 'ajax_test_add'),





                       )
