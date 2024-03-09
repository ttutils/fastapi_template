# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2023/11/13 15:35
from util.config_util import Setting
setting = Setting()

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': str(setting.DATABASE_HOST),
                'port': str(setting.DATABASE_PORT),
                'user': str(setting.DATABASE_USER),
                'password': str(setting.DATABASE_PASSWORD),
                'database': str(setting.DATABASE_DATABASE),
            }
        }
    },
    'apps': {
        'models': {
            'models': ['aerich.models', 'models.test'],
            'default_connection': 'default',
        }
    },
}
