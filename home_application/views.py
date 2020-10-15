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
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from models import *
#from account import role_check,is_post_method,role_check_2
import json 
import re
from django.shortcuts import render as drender
from django.utils.decorators import method_decorator
from collections import namedtuple


@role_check
def index(request,role_id):
    if request.method == 'GET':
        
#        if username not in userList:
#                return render(request, '/home_application/contact.html')
        project_list=Project.objects.all()
        context={"plist":project_list,"username":request.user.username,"role_id":role_id}
        return render(request, '/home_application/index.html', context)


@role_check_2
def detail(request,project_id,role_id):
       
    p=Project.objects.get(id=project_id)
    context={"project":p,"username":request.user.username,"role_id":role_id}
    return render(request, 'home_application/detail.html',context)


def addProject(request):
    if request.method == 'POST':
       pname=request.POST["pname"]
       code_name=request.POST["code_name"]
       p=Project(name=pname,code_name=code_name)
       p.save()
       return HttpResponseRedirect(reverse('index'))
    
def deleteProject(request):
    pass

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

def copyDir(request,project_id):
    """
    copy module
    """
    print request.GET
    service,src_module,des_module = request.GET.get("service"),request.GET.get("src_module"),request.GET.get("des_module")
    service_obj = Project.objects.get(id=project_id).service_set.get(name=str(service))
    module = Project.objects.get(id=project_id).service_set.get(name=str(service)).module_set.get(name=src_module)
    new_module = Module.objects.create(name=des_module,service=service_obj)
    config_obj = module.config_set.all()
    for obj in config_obj:
        Config.objects.create(fileName=obj.fileName,content=obj.content,module=new_module)
        
    return HttpResponseRedirect(reverse('detail',kwargs={"project_id":project_id}))    


def editDir(request,project_id):
    
    if request.POST:
        edit_id=request.POST["edit_id"]
        edit_content=request.POST["edit_content"]
        edit_type=request.POST["edit_type"]
        print re.match('service',edit_type)   
        if request.POST.has_key('save'):
            
            if re.match('project',edit_type) != None:
                s = Project.objects.get(id=edit_id)
                s.name=edit_content
                s.save()
            elif re.match('service',edit_type) != None:
                s = Service.objects.get(id=edit_id)
                s.name=edit_content
                s.save()
            elif re.match('module',edit_type) != None:
                m = Module.objects.get(id=edit_id)
                m.name = edit_content
                m.save()
            elif re.match('config',edit_type) != None:
                c = Config.objects.get(id=edit_id)
                c.fileName = edit_content
		print c.fileName
                c.save()
            else:
                print "edit_type not exeist"

        if  request.POST.has_key('delete'):
           
         
             if re.match('service',edit_type) != None:              
                Service.objects.get(id=edit_id).delete()
             elif re.match('module',edit_type) != None:
                m = Module.objects.get(id=edit_id).delete()
             elif re.match('config',edit_type) !=None:
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

def get_config_list(request):
    """
     通过项目 服务 模块名 获取所有配置
    """
    
    data = request.POST
    project,service,module = data.get("project"),data.get("service"),data.get("module")
    config_obj_list = Project.objects.get(name=project).service_set.get(name=service).module_set.get(name=module).config_set.all() 
    res_data = {obj.fileName:obj.content for obj in config_obj_list}
    return JsonResponse(res_data)




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



def contacts(request):
    """
    联系我们
    """
    project_list=Project.objects.all()
    p=Project.objects.get(id=1)
    s=p.service_set.all()
    context={"slist":s,"plist":project_list}
    return render(request, '/home_application/contact.html')

def healthz(request):
    """
    健康检查
    """
    return HttpResponse("ok")
