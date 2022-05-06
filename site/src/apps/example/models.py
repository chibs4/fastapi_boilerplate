from tortoise import fields

from db.model import Model


class Example(Model):
    name = fields.CharField(max_length=100, unique=True)
    description = fields.CharField(max_length=3024, null=True)

    class Meta:
        table = "example"
        ordering = ["id"]
