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

from django.db import models

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    code_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class Service(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)

class Module(models.Model):
    id=models.AutoField(primary_key=True)
    service=models.ForeignKey(Service, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)

class Config(models.Model):
    id=models.AutoField(primary_key=True)
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    fileName=models.CharField(max_length=200)
    content=models.TextField()
    comment=models.CharField(max_length=200)
    create_user=models.CharField(max_length=200)
    create_time=models.DateTimeField(auto_now=True)

class ConfigHistory(models.Model):
    id=models.AutoField(primary_key=True)
    config=models.ForeignKey(Config, on_delete=models.CASCADE)
    fileName=models.CharField(max_length=200)
    comment=models.CharField(max_length=200)
    content=models.TextField()
    create_user=models.CharField(max_length=200)
    create_time=models.DateTimeField(auto_now=True)
