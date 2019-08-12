# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^project/(?P<project_id>[0-9]+)/$', views.detail, name='detail'),
     # url(r'^project/(?P<project_id>[0-9]+)/addConfig/$', views.addConfig, name='addConfig'),
    url(r'^project/(?P<project_id>[0-9]+)/getdir/$', views.getdir,name='getdir'),
    url(r'^project/(?P<project_id>[0-9]+)/editDir/$', views.editDir,name='editDir'),
    url(r'^addProject/$', views.addProject,name='addProject'),
    #url(r'^home/$', views.home,name='home'),
    url(r'^readme/$', views.readme,name='readme'),
    url(r'^contactus/$', views.contactus,name='contactus'),
    url(r'^project/(?P<project_id>[0-9]+)/getConf/$', views.getConf,name='getConf'),
    url(r'^project/(?P<project_id>[0-9]+)/updateConf/$', views.updateConf,name='updateConf'),
    url(r'^project/(?P<project_id>[0-9]+)/createConf/$', views.createConf,name='createConf'),
    url(r'^project/(?P<project_id>[0-9]+)/(?P<config_id>[0-9]+)/history/$', views.historyConf,name='historyConf'),
    url(r'^project/(?P<project_id>[0-9]+)/(?P<config_id>[0-9]+)/(?P<confHistory_id>[0-9]+)/compare/$', views.compare,name='compare'),
    # url(r'^project/(?P<project_id>[0-9]+)/(?P<fileName>[-\w]+)/(?P<config_id>[0-9]+)/compare/$', views.compare,name='compare'),
    url(r'^project/(?P<project_id>[0-9]+)/(?P<config_id>[0-9]+)/(?P<confHistory_id>[0-9]+)/rollBack/$', views.rollBack,name='rollBack'),
    url(r'^configApi/(?P<config_id>[0-9]+)/$', views.configApi,name='configApi'),
    url(r'^readme/$', views.readme,name='readme'),
    url(r'^download/(?P<node_id>[0-9]+)/$', views.download,name='downlaod'),
    url(r'^upload/$', views.upload,name='upload'),


]
