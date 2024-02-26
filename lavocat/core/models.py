from django.db import models
from django.utils import timezone


class SoftDeletableQuerySet(models.query.QuerySet):
    def delete(self, soft=True):
        if soft:
            updated_count = self.update(deleted_at=timezone.now())
            return updated_count, {self.model._meta.label: updated_count}
        else:
            return super().delete()


class SoftDeleteManager(models.Manager):
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(deleted_at=None)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, soft=True):
        if soft:
            self.deleted_at = timezone.now()
            self.save(using=using)
        else:
            return super().delete(using=using, keep_parents=keep_parents)


class ModelBase(SoftDeleteModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserAllowed(ModelBase):
    email = models.EmailField(unique=True)
