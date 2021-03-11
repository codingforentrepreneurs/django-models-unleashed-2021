from django.db import models

from .validators import validate_blocked_words

# Create your models here.
class Product(models.Model):
    """
    admin.site.register(Product)
    """
    title = models.CharField(max_length=120, validators=[validate_blocked_words])
    description = models.TextField(null=True) # null=True is an null value in db
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)

    """
    def clean(self):
        '''
        Django Model Forms / Django Forms
        Project.objects.create() -> not call .clean()
        '''
        if self.title == self.description:
            raise ValidationError("Make the description different")
    """