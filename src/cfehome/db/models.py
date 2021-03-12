
from django.db import models
from django.utils import timezone

class BasePublishModel(models.Model):
    class PublishStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Published'
        DRAFT = 'DR', 'Draft'
        PRIVATE = 'PR', 'Private'
    state = models.CharField(max_length=2, default=PublishStateOptions.DRAFT, choices=PublishStateOptions.choices)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True) # auto set when the state changes to `PUBLISH`
    timestamp = models.DateTimeField(auto_now_add=True) # auto set when this object was created
    updated = models.DateTimeField(auto_now=True) # auto set when this object was lasted saved

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.state_is_published and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        else:
            self.publish_timestamp = None
        super().save(*args, **kwargs)

    @property
    def state_is_published(self):
        return self.state == self.PublishStateOptions.PUBLISH
    
    @property
    def is_published(self):
        publish_timestamp = self.publish_timestamp
        return self.state_is_published and publish_timestamp < timezone.now()