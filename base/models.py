import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .managers import SoftDeletableManager


class SoftDeletableModel(models.Model):
    """
    自定义软删除抽象基类
    An abstract base class model with a ``is_deleted`` field that
    marks entries that are not going to be used anymore, but are
    kept in db for any reason.
    Default manager returns only not-deleted entries.
    """
    deleted_at = models.DateTimeField("删除时间", null=True, default=None, blank=True)

    class Meta:
        abstract = True

    objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_deleted`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.deleted_at = timezone.now()
            self.save(using=using)
        else:
            return super(SoftDeletableModel, self).delete(using=using, *args, **kwargs)


class UUIDFieldModel(models.Model):
    """
    时间抽象类
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        # 不生成表
        abstract = True


class TimeAtSchemaModel(models.Model):
    """
    时间抽象类
    """
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        # 不生成表
        abstract = True


class HiddenSchemaModel(models.Model):
    """
    隐藏抽象类
    """
    hidden = models.BooleanField(default=False, verbose_name="隐藏")

    class Meta:
        abstract = True


class StatusSchemaModel(models.Model):
    """
    状态抽象类
    """
    status = models.BooleanField(default=True, verbose_name="状态")

    class Meta:
        abstract = True


class OwnerSchemaModel(models.Model):
    """
    谁的 抽象类
    """
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Owner")

    class Meta:
        abstract = True


class TimeAtSchemaSoftDeletable(TimeAtSchemaModel, SoftDeletableModel):
    """
    时间 软删除类
    """

    class Meta:
        # 不生成表
        abstract = True


class StatusTimeAtSchemaSoftDeletable(TimeAtSchemaModel, SoftDeletableModel, StatusSchemaModel):
    """
    状态 时间 软删除类
    """

    class Meta:
        abstract = True


class UUIDFieldTimeAtSchemaSoftDeletable(TimeAtSchemaModel, SoftDeletableModel, UUIDFieldModel):
    """
    默认类
    不生成表
    abstract = True
    """

    class Meta:
        abstract = True


class HiddenTimeAtSchemaSoftDeletable(TimeAtSchemaModel, SoftDeletableModel, HiddenSchemaModel):
    """
    隐藏 时间 软删除类
    """

    class Meta:
        abstract = True


class OwnerTimeAtSchemaSoftDeletable(TimeAtSchemaModel, SoftDeletableModel, OwnerSchemaModel):
    """
    谁的 时间 软删除类
    """

    class Meta:
        abstract = True


class DefaultModel(TimeAtSchemaModel, SoftDeletableModel, StatusSchemaModel, HiddenSchemaModel, OwnerSchemaModel):
    """
    谁的 隐藏 UUID 状态 时间 软删除类
    """

    class Meta:
        abstract = True
