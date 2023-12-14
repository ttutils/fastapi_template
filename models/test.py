from tortoise.models import Model
from tortoise import fields


class Test(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="名字", null=True)
