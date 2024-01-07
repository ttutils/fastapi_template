import logging

from fastapi import APIRouter, Depends

from api.base import resp_200, resp_400
from api.oauth2 import verify_token, create_token

test1 = APIRouter()


@test1.get('test')
def test(token: bool = Depends(verify_token)):
    logging.info(f'调用成功,token={token}')
    return resp_200(message=f'调用成功,token={token}')

@test1.get('/test222')
def test222():
    token_data = create_token(1)
    return resp_200(message=f'{token_data}')