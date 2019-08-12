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

from common.mymako import render_mako_context as render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from models import *
import json 
from django.shortcuts import render as drender

def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
                username = request.user.username
        project_list=Project.objects.all()
        context={"plist":project_list,"username":username}
        return render(request, '/home_application/index.html', context)
    # else:

    #     pname=request.POST["pname"]
    #    p=Project(name=pname)
    #    p.save()
def detail(request,project_id):
    
    
    p=Project.objects.get(id=project_id)
    context={"project":p,"username":request.user.username}
    return render(request, 'home_application/detail.html',context)

def addProject(request):
   
    if request.method == 'POST':
       pname=request.POST["pname"]
       code_name=request.POST["code_name"]
       p=Project(name=pname,code_name=code_name)
       p.save()
       return HttpResponseRedirect(reverse('index'))
def deleteProject(request):
    paas

#构建目录树结构
def createDic(id,parent,text):
    dic={}
    dic["id"]=id
    dic["parent"]=parent
    dic["text"]=text
    return dic

def getdir(request,project_id):
    p=Project.objects.get(id=project_id)
    s_list=p.service_set.all()
    dct=[{"id":"project"+str(p.id),"parent":"#","text":p.code_name,"type":"project"}]
    for s in s_list:
        dct.append(createDic("service"+str(s.id),"project"+str(p.id),s.name))
        m_list=s.module_set.all()
        for m in m_list:
            dct.append(createDic("module"+str(m.id),"service"+str(s.id),m.name))
            config_list=m.config_set.all()
            for config in config_list:
                 dct.append(createDic("config"+str(config.id),"module"+str(m.id),config.fileName))
    
    return HttpResponse(json.dumps(dct))

def editDir(request,project_id):
    print "start"
    if request.POST:
        edit_id=request.POST["edit_id"]
        edit_content=request.POST["edit_content"]
        edit_type=request.POST["edit_type"]
        
        if request.POST.has_key('save'):
            
            if edit_type == "project":
                p = Project.objects.get(id=edit_id)
                p.code_name = edit_content
                p.save()
            elif edit_type == "service":
                s = Service.objects.get(id=edit_id)
                s.name=edit_content
                s.save()
            elif edit_type == "module":
                m = Module.objects.get(id=edit_id)
                m.name = edit_content
                m.save()
            elif edit_type == "config":
                c = Config.objects.get(id=edit_id)
                c.name = edit_content
                c.save()
            else:
                print "edit_type not exeist"

        if  request.POST.has_key('delete'):
             if edit_type == "project":
                Project.objects.get(id=edit_id).delete()
             elif edit_type == "service":
                Service.objects.get(id=edit_id).delete()
             elif edit_type == "module":
                m = Module.objects.get(id=edit_id).delete()
             elif edit_type == "config":
                c = Config.objects.get(id=edit_id).delete()
             else:
                print "edit_type not exeist"     
        
    return HttpResponseRedirect(reverse('detail',kwargs={"project_id":project_id}))


def getConf(request,project_id):
     node_id=request.POST.get("node_id") 
     config=Config.objects.get(id=int(node_id))
     context={"content":config.content,"config_id":config.id}
     return HttpResponse(json.dumps(context))

def updateConf(request,project_id):
    # 接口content-type置为application/json - calabash
    if request.method == 'POST':
        request_body = json.loads(request.body)
        content= request_body.get('content')
        comment= request_body.get('comment')
        node_id= request_body.get("selected_node_id")
        config=Config.objects.get(id=node_id)
        config.content=content
        config.comment=comment
        config.save()
        print config.comment
        config.confighistory_set.create(fileName=config.fileName,config=config,content=config.content,comment=config.comment,create_user=request.user.username)
        
        return HttpResponse(json.dumps("sucess"),content_type="application/json")

def createConf(request,project_id):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        project=Project.objects.get(id=project_id)
        service=request_body.get('service')
        module= request_body.get('module')
        fileName=request_body.get('fileName')
        content= request_body.get('content')
        service_object,create=Service.objects.get_or_create(name=service,project=project)
        module_object,create=Module.objects.get_or_create(name=module,service=service_object)
        Config.objects.get_or_create(fileName=fileName,content=content,module=module_object,comment="")
        return HttpResponse("sucess")
        # return HttpResponseRedirect(reverse('detail',kwargs={"project_id":project_id}))



def historyConf(request,project_id,config_id):
    p=Project.objects.get(id=project_id)
    config_object = Config.objects.get(id=config_id)
    historyConf = config_object.confighistory_set.all()
    # ".".join(hconf.create_time.split(".")[:-1])
    context={"project":p,"username":request.user.username,"historyConf":historyConf,}
    return render(request, 'home_application/history.html',context)
   

def compare(request,project_id,config_id,confHistory_id):
    config_object = Config.objects.get(id=config_id)
    historyConf_object = ConfigHistory.objects.get(id=confHistory_id)
    context={"config_object":config_object,"historyConf_object":historyConf_object,"username":request.user.username}
    return render(request, 'home_application/compare.html',context,)

def rollBack(request,project_id,config_id,confHistory_id):
    config_object = Config.objects.get(id=config_id)
    historyConf_object = ConfigHistory.objects.get(id=confHistory_id)
    config_object.content=historyConf_object.content
    config_object.save()
    return  HttpResponseRedirect(reverse('detail',kwargs={"project_id":project_id}))

def configApi(request,config_id):
    config_object = Config.objects.get(id=config_id)
    return HttpResponse(config_object.content)


def readme(request):
    """
    首页
    """
    return render(request, 'home_application/README.html',{"username":request.user.username})

def download(request,node_id):
    config=Config.objects.get(id=int(node_id))
    response = HttpResponse(config.content)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(config.fileName)
    return response
    
def upload(request):
     if request.method == 'POST':
        file=request.FILES['file']
     return HttpResponse(file.chunks())



def contactus(request):
    """
    联系我们
    """
    project_list=Project.objects.all()
    p=Project.objects.get(id=1)
    s=p.service_set.all()
    context={"slist":s,"plist":project_list}
    return render(request, '/home_application/contact.html')
