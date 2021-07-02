from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeletableQuerySetMixin(object):
    """
    自定义软删除查询基类
    QuerySet for SoftDeletableModel. Instead of removing instance sets
    its ``is_deleted`` field to True.
    """

    def delete(self):
        """
        Soft delete objects from queryset (set their ``is_deleted``
        field to True)
        """
        self.update(deleted_at=timezone.now())


class SoftDeletableQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    pass


class SoftDeletableManagerMixin(object):
    """
    Manager that limits the queryset by default to show only not deleted
    instances of model.
    """
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self):
        """
        Return queryset limited to not deleted entries.
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).filter(deleted_at=None)


class SoftDeletableManager(SoftDeletableManagerMixin, models.Manager):
    """
    软删除管理类
    """
    pass
