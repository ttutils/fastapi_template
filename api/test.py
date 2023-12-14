import logging
import os, subprocess, uuid

from fastapi import APIRouter

from api.base import resp_200, resp_400


test = APIRouter()


@test.get('test')
def test():
    return resp_200