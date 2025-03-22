from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass



class TodoQuerySet(models.QuerySet):
    def by_user(self, user):
        return self.filter(created_by=user)

    def not_deleted(self):
        return self.filter(deleted=False)
    
    def not_completed(self):
        return self.filter(completed=False)


class TodoManager(models.Manager):
    def get_queryset(self):
        return TodoQuerySet(self.model, using=self._db)

    def by_user(self, user, with_deleted=False, with_completed=True):
        queryset = self.get_queryset().by_user(user)
        if not with_deleted:
            queryset = queryset.not_deleted()
        if not with_completed:
             queryset = queryset.not_completed()
        return queryset


class Todo(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # Tracks completion status
    completed_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)  # Tracks completion status
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete support

    objects = TodoManager()

    class Meta:
        ordering = ["-created_at"]  # Newest first
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["completed"]),
        ]

    def __str__(self):
        if self. completed:
            return f"Todo #{self.id} by {self.created_by.email} - Completed"
        elif self. deleted:
            return f"Todo #{self.id} by {self.created_by.email} - Deleted"
        else:
            return f"Todo #{self.id} by {self.created_by.email}"

    def soft_delete(self):
        """Marks the task as deleted without actually removing it."""
        self.deleted = True
        self.deleted_at = datetime.now(tz=timezone.utc)
        self.save()

    def restore(self):
        """Restores a soft-deleted task."""
        self.deleted = False
        self.deleted_at = None
        self.save()

    def complete(self):
        """Marks the task as deleted without actually removing it."""
        self.completed = True
        self.completed_at = datetime.now(tz=timezone.utc)
        self.deleted = False
        self.deleted_at = None
        self.save()

    def uncomplete(self):
        """Restores a soft-deleted task."""
        self.completed = False
        self.completed_at = None
        self.deleted = False
        self.deleted_at = None
        self.save()

    def toggle_complete(self):
        if self.completed:
            self.uncomplete()
        else:
            self.complete()