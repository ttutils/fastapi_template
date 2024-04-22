# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2023/12/29 15:59
import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from pyresp.pyresp import resp_200, resp_400
from pyoauth2_util.oauth2 import create_token, verify_token
from models.user import User
from pyaes_util.aes_util import md5

user = APIRouter()


class LoginModel(BaseModel):
    user: str
    password: str


@user.post('/login', summary='登录')
async def login(item: LoginModel):
    try:
        user_data = await User.get(user=item.user)
    except:
        return resp_400(message='账号错误')
    if md5(item.password) != user_data.password:
        return resp_400(message='密码错误')
    token = create_token(user_data.id)
    return resp_200(message='登录成功', data={
        'token': token
    })


class ChangeUserModel(BaseModel):
    user: str
    password: str


@user.post('/change', summary='修改账号')
async def change_user(item: ChangeUserModel, user_info: int = Depends(verify_token)):
    try:
        user_data = await User.get(id=user_info['user_id'])
    except:
        return resp_400(message='没有该用户')
    user_data.user = item.user
    user_data.password = md5(item.password)
    try:
        await user_data.save()
    except Exception as e:
        logging.error(f"修改错误: {e}")
        return resp_400(message='修改错误')
    token_data = create_token(user_data.id)
    return resp_200(message='修改成功', data={
        'token': token_data
    })


class AddUserModel(BaseModel):
    user: str
    password: str
    is_admin: bool = False


@user.post('/add', summary='新增账号')
async def change_user(item: AddUserModel, user_info: int = Depends(verify_token)):
    if not user_info['is_admin']:
        return resp_400(message='不是管理员')
    item.password = md5(item.password)
    try:
        add_data = await User.create(**item.dict())
    except Exception as e:
        logging.error(f"插入错误: {e}")
        return resp_400(message='插入错误')
    token_data = create_token(add_data.id)
    resp_data = {
        "id": add_data.id,
        "token": token_data,
        "is_admin": add_data.is_admin,
    }
    return resp_200(data=resp_data, message='新增成功')
