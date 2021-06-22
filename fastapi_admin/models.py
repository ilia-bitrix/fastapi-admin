from tortoise import Model, fields


class AbstractAdmin(Model):
    name = fields.CharField(max_length=50, pk=True)
    email = fields.CharField(max_length=120, unique=True)
    password = fields.CharField(max_length=250)
    is_super = fields.BooleanField(default=True)
    is_active = fields.BooleanField(default=False)
    create_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
