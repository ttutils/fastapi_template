import logging

from fastapi import APIRouter

from api.base import resp_200, resp_400


test1 = APIRouter()


@test1.get('test')
def test():
    logging.info('调用成功')
    return resp_200(message='调用成功')