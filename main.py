import logging
import os
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pyresp.pyresp import resp_200
from pyinitlog_util.pyinitlog_util import init_log

from api.user import user
from settings import TORTOISE_ORM

init_log()

# 初始化文件夹
for init_dir in ['web/static', 'web/admin']:
    if not os.path.exists(init_dir):
        os.makedirs(init_dir)

with open(os.getcwd() + '/version.py', encoding="utf-8") as f:
    version_var = {}
    exec(f.read(), version_var)
    VERSION = version_var['VERSION']

logging.info(f'当前服务端版本为：v{VERSION}')

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="fastapi_template",
    version=VERSION,
    description="fastapi模板仓库",
    contact={
        "name": "buyfakett",
        "url": "https://github.com/buyfakett",
        "email": "buyfakett@vip.qq.com",
    }
)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # 如果数据库为空，自动生成对应表单，生产环境不能开
    add_exception_handlers=True,  # 调试消息，生产环境不能开
)

app.include_router(user, prefix='/api/test', tags=['测试接口'])
app.mount("/static", StaticFiles(directory="web/static"), name="static")
app.mount("/admin", StaticFiles(directory="web/admin"), name="admin")

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 首页跳转
@app.get('/')
async def index():
    return RedirectResponse('/admin/index.html')


@app.get('/favicon.ico')
async def ico():
    return RedirectResponse('/admin/favicon.ico')


@app.get('/api/getServerVersion')
async def get_server_version():
    return resp_200(data={'version': VERSION}, message='获取版本号成功')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    uri = request.url.path
    start_time = time.time()
    if 'api' in uri:
        method = request.method
        url = request.base_url
        # 如果请求方法是 POST，则获取请求的 JSON 数据
        if request.method == "POST":
            body = await request.body()
            # 将请求体解码为字符串
            body_str = body.decode("utf-8")
        # 否则，设置为 None
        else:
            body_str = None
        logging.info(
            f'\n'
            f'\033[0;31m请求方式：\033[0;32m{method}\033[0m\n'
            f'\033[0;31m请求地址：\033[0;32m{url}\033[0m\n'
            f'\033[0;31m请求接口：\033[0;32m{uri}\033[0m\n'
            f'\033[0;31m请求头：\033[0;32m{request.headers}\033[0m\n'
            f'\033[0;31m请求入参：\033[0;32m{body_str}\033[0m\n'
            f'\033[0;31m请求参数：\033[0;32m{request.query_params}\033[0m'
        )
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 5))
    logging.info(f"\033[0;32m耗时: {str(round(process_time, 5))} s\033[0m")
    return response


if __name__ == "__main__":
    uvicorn.run(
        "setup:app",
        port=8000,
        reload=True,
    )
