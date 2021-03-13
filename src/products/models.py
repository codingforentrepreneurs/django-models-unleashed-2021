# import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from .validators import validate_blocked_words


class ProductQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=Product.ProductStateOptions.PUBLISH, publish_timestamp__lte=now) 

# (DB_VALUE, USER_FACING_VALUE)
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def published(self):
        # Product.objects.published()
        # Product.objects.filter(title__icontains='Title').published()
        return self.get_queryset().published()

        

# Create your models here.
class Product(models.Model):
    class ProductStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Published'
        DRAFT = 'DR', 'Draft'
        PRIVATE = 'PR', 'Private'
    title = models.CharField(max_length=120, validators=[validate_blocked_words])
    description = models.TextField(null=True) # null=True is an null value in db
    tags = models.TextField(null=True)
    slug = models.SlugField(blank=True, null=True, db_index=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    state = models.CharField(max_length=2, default=ProductStateOptions.DRAFT, choices=ProductStateOptions.choices)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True) # auto set when the state changes to `PUBLISH`
    timestamp = models.DateTimeField(auto_now_add=True) # auto set when this object was created
    updated = models.DateTimeField(auto_now=True) # auto set when this object was lasted saved
    
    objects = ProductManager()
    
    class Meta:
        ordering = ['-updated', '-timestamp']
        # verbose_name = 'Product' 
        # verbose_name_plural =  'Products'
        # unique_together = [['title', 'order']]
        # db_table = '<appname>_<modelname>' # 'products_mycoolproduct'

    def get_absolute_url(self):
        "http://www.mysite.com/products/my-awesome-product/"
        "http://www.mysite.com/products/1/"
        return f"/product/{self.slug}/"


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




def slugify_pre_save(sender, instance, *args, **kwargs):
    # create my slug from my title
    if instance.slug is None or instance.slug == "":
        new_slug = slugify(instance.title)
        Klass = instance.__class__
        qs = Klass.objects.filter(slug=new_slug).exclude(id=instance.id)
        if qs.count() == 0:
            instance.slug = new_slug
        else:
            instance.slug = f"{new_slug}-{qs.count()}"


pre_save.connect(slugify_pre_save, sender=Product)