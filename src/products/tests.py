from django.test import TestCase
from django.utils.text import slugify
from .models import Product


class ProductTestCase(TestCase):
    # fixtures = ['products/fixtures/products']
    def create_draft_items(self):
        data = {
            "title": "Draft item",
            "price": 12.99
        }
        self.draft_a = Product.objects.create(**data)
        self.draft_b = Product.objects.create(**data)
        self.draft_c = Product.objects.create(**data)
        self.draft_count = 3

    def create_published_items(self):
        data = {
            "title": "Draft item",
            "price": 12.99,
            "state": Product.ProductStateOptions.PUBLISH
        }
        self.pub_a = Product.objects.create(**data)
        self.pub_b = Product.objects.create(**data)
        self.pub_c = Product.objects.create(**data)
        self.pub_count = 3

    def create_unique_slug_items(self):
        my_non_unique_title = 'This is a title test for slugify only it should not work anywhere else'
        data = {
            "title": my_non_unique_title,
            "price": 12.99,
        }
        self.slug_title = my_non_unique_title
        self.slug_slug = slugify(my_non_unique_title)
        self.slug_a = Product.objects.create(**data)
        self.slug_b = Product.objects.create(**data)
        self.slug_c = Product.objects.create(**data)       
        self.unique_slug_count = 3

    def setUp(self):
        self.create_unique_slug_items()
        self.create_draft_items()
        self.create_published_items()

    def test_queryset_exists(self):
        qs = Product.objects.all()
        self.assertTrue(qs.exists())
    
    def test_draft_count(self):
        qs = Product.objects.filter(state=Product.ProductStateOptions.DRAFT)
        self.assertEqual(qs.count(), self.draft_count + self.unique_slug_count)
    
    def test_published_property(self):
        self.assertTrue(self.pub_a.is_published)
        self.assertTrue(self.pub_b.is_published)
        self.assertTrue(self.pub_c.is_published)
        
    def test_publish_count(self):
        qs = Product.objects.filter(state=Product.ProductStateOptions.PUBLISH)
        self.assertEqual(qs.count(), self.pub_count)

    def test_publish_count_manager(self):
        manager_qs = Product.objects.published()
        custom_qs_filter = Product.objects.all().published()
        self.assertEqual(custom_qs_filter.count(), manager_qs.count(), self.pub_count)
        manager_qs_ids = list(manager_qs.values_list('id', flat=True))
        custom_qs_ids = list(custom_qs_filter.values_list('id', flat=True))
        self.assertEqual(manager_qs_ids, custom_qs_ids)
        self.assertEqual(len(custom_qs_ids), len(manager_qs_ids), self.pub_count)

    def test_slug_count(self):
        qs = Product.objects.filter(slug__icontains=self.slug_slug)
        self.assertEqual(qs.count(), self.unique_slug_count)
    
    def test_slug_title_signal(self):
        self.assertEqual(self.slug_a.slug, self.slug_slug)

    def test_slug_unique_on_extra(self):
        self.assertNotEqual(self.slug_slug, self.slug_b.slug)
        self.assertNotEqual(self.slug_slug, self.slug_c.slug)
        self.assertNotEqual(self.slug_b.slug, self.slug_c.slug)
    