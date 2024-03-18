import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.user import user
from settings import TORTOISE_ORM

# 日志记录器
logger = logging.getLogger()

# 设置日志级别，只有大于等于这个级别的日志才能输出
logger.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter(
    "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]    %(message)s"
)

# 输出到控制台
to_console = logging.StreamHandler()
to_console.setFormatter(formatter)
logger.addHandler(to_console)

# 初始化文件夹
for init_dir in ['web/static', 'web/admin']:
    if not os.path.exists(init_dir):
        os.makedirs(init_dir)

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="fastapi_template",
    version="0.1.0",
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logging.info(
        f'\n请求方式：{request.method}\n请求地址：{request.base_url}\n请求接口：{request.url.path}\n请求头：{request.headers}\n请求入参：{await request.json() if request.method == "POST" else None}\n请求参数：{request.query_params}')
    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(
        "setup:app",
        port=8000,
        reload=True,
    )
