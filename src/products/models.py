# import datetime
from django.db import models
from django.utils import timezone
from .validators import validate_blocked_words

# (DB_VALUE, USER_FACING_VALUE)


# Create your models here.
class Product(models.Model):
    class ProductStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Published'
        DRAFT = 'DR', 'Draft'
        PRIVATE = 'PR', 'Private'
    
    title = models.CharField(max_length=120, validators=[validate_blocked_words])
    description = models.TextField(null=True) # null=True is an null value in db
    price = models.DecimalField(max_digits=20, decimal_places=2)
    state = models.CharField(max_length=2, default=ProductStateOptions.DRAFT, choices=ProductStateOptions.choices)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True) # auto set when the state changes to `PUBLISH`
    timestamp = models.DateTimeField(auto_now_add=True) # auto set when this object was created
    updated = models.DateTimeField(auto_now=True) # auto set when this object was lasted saved

    def save(self, *args, **kwargs):
        validate_blocked_words(self.title)
        if self.state_is_published and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        else:
            self.publish_timestamp = None
        super().save(*args, **kwargs)

    @property
    def state_is_published(self):
        return self.state == self.ProductStateOptions.PUBLISH
    
    @property
    def is_published(self):
        publish_timestamp = self.publish_timestamp
        return self.state_is_published and publish_timestamp < timezone.now()

    class Meta:
        ordering = ['-publish_timestamp', '-updated', '-timestamp']
        get_latest_by = ['-publish_timestamp', '-updated', '-timestamp']
        # products_product