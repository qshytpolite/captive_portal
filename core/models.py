from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base class that adds created and updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'
        abstract = True


class Settings(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value[:30]}..."

    class Meta:
        ordering = ['key']
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
