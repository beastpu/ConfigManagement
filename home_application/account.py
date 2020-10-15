import requests
import json
from django.http import HttpResponse

def role_check(func):
    url="http://paas.bk.91act.com/api/c/compapi/v2/bk_login/get_user/"
    headers = {'content-type': 'application/json'}
    def func_in(request):
        if request.user.is_authenticated():
            token = request.COOKIES.get("bk_token", None)
            username = request.user.username
            content = {"bk_app_code":"cmdb","bk_app_secret":"195c589f-ef72-449f-8fb2-7962b499838b","bk_token":token}
            res=requests.post(url,data=json.dumps(content),headers=headers)
            res_data = res.json()
            role_id = res_data["data"]["bk_role"]          
        return func(request,role_id)
    return func_in

def role_check_2(func):
    url="http://paas.bk.91act.com/api/c/compapi/v2/bk_login/get_user/"
    headers = {'content-type': 'application/json'}
    def func_in(request,project_id):
        if request.user.is_authenticated():
            token = request.COOKIES.get("bk_token", None)
            username = request.user.username
            content = {"bk_app_code":"cmdb","bk_app_secret":"195c589f-ef72-449f-8fb2-7962b499838b","bk_token":token}
            res=requests.post(url,data=json.dumps(content),headers=headers)
            res_data = res.json()
            role_id = res_data["data"]["bk_role"]          
        return func(request,project_id,role_id)
    return func_in

def is_post_method(func):
    def my_function(request, *args, **kwargs):
        if request.method == "POST":
            # do somthing
            return func(request, *args, **kwargs)
        else:
            # do something
            return HttpResponse(
                json.dumps({
                    "result": False,
                    "data": [],
                    "message": "fff",
                    "code": -1
                }), content_type='application/json')

    return my_function
