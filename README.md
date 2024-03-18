<h1 align="center">fastapi_template</h1>

此项目是根据[@buyfakett](https://github.com/buyfakett)的fastapi使用习惯的模板仓库

项目目录：

```bash
.
├── api
│   └── test.py				# 路由和实现类
├── config
│   └── setting.yaml		# 配置文件
├── Dockerfile
├── main.py					# 启动文件
├── models
│   └── test.py				# 数据库模型类
├── README.md
├── requirements.txt		# 依赖
├── settings.py				# ORM数据库连接文件
└── util					# 工具
```

- 该仓库使用postgres作为数据库

- 配置文件放在config目录下，具体使用的时候`setting.DATABASE_HOST`

### 执行数据库迁移

```bash
# 第一次
aerich init -t settings.TORTOISE_ORM
aerich init-db
```

```bash
# 后面
aerich migrate
aerich upgrade
```
