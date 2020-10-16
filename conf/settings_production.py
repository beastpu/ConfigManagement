# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

用于正式环境的全局配置
"""
import os

# ===============================================================================
# 数据库设置, 正式环境数据库设置
# ===============================================================================
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': os.environ.get('DB_NAME'),
#       'USER': os.environ.get('DB_USERNAME'),
#        'PASSWORD': os.environ.get('DB_PASSWORD'),
#        'HOST': os.environ.get('DB_HOST'),
#        'PORT': os.environ.get('DB_PORT'),
#    },
#}


DATABASES = {
	# 默认db，主要记录主要和公用信息
         'default': {
            'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'p$
            'NAME': 'cmdb',                    # Or path to database file if usi$
            'USER': 'root',
            'PASSWORD': '***',
            'HOST': '10.10.4.12',
            'PORT': '3306',                         # Set to empty string for defau$
#            #'OPTIONS':{
            #    'init_command':'SET storage_engine=INNODB',
            #},
        }
}

#import os
#from settings import BASE_DIR
#DATABASES = {
#	'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        }
#    }

