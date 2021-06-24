from tortoise import Model, fields


class AbstractAdmin(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)

    is_active = fields.BooleanField(default=True)

    create_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
