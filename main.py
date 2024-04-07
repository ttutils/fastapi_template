import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pyresp.pyresp import resp_200
from colorlog import ColoredFormatter

from api.user import user
from settings import TORTOISE_ORM

# 日志记录器
logger = logging.getLogger()

# 设置日志级别，只有大于等于这个级别的日志才能输出
logger.setLevel(logging.INFO)

# 设置日志格式
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s %(white)s[%(asctime)s]%(reset)s "
    "%(blue)s[%(filename)s:%(lineno)d]%(reset)s %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# 输出到控制台
to_console = logging.StreamHandler()
to_console.setFormatter(formatter)
logger.addHandler(to_console)

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
async def main():
    return RedirectResponse('/admin/index.html')


@app.get('/api/getServerVersion')
async def get_server_version():
    return resp_200(data={'version': VERSION})


@app.middleware("http")
def add_process_time_header(request: Request, call_next):
    uri = request.url.path
    if 'api' in uri:
        method = request.method
        url = request.base_url
        logging.info(
            f'\n'
            f'\033[0;31m请求方式：\033[0;32m{method}\033[0m\n'
            f'\033[0;31m请求地址：\033[0;32m{url}\033[0m\n'
            f'\033[0;31m请求接口：\033[0;32m{uri}\033[0m\n'
            f'\033[0;31m请求头：\033[0;32m{request.headers}\033[0m\n'
            f'\033[0;31m请求入参：\033[0;32m{ request.json() if request.method == "POST" else None}\033[0m\n'
            f'\033[0;31m请求参数：\033[0;32m{request.query_params}\033[0m'
        )
    response = call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(
        "setup:app",
        port=8000,
        reload=True,
    )
