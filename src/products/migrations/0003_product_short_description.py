# Generated by Django 3.1.7 on 2021-03-10 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.CharField(default='I dont like this desc', max_length=220),
            preserve_default=False,
        ),
    ]
