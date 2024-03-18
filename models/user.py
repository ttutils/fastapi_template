# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2023/12/29 15:58
from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    user = fields.CharField(max_length=50, description="用户名")
    password = fields.CharField(max_length=255, description="密码")
    role = fields.CharField(max_length=50, description="角色", null=True)
    is_admin = fields.BooleanField(default=0, description="是否是管理员 0-普通用户 1-管理员")
