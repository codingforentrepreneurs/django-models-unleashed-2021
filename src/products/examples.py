from django.contrib.auth import get_user_model
from products.models import Product 

User = get_user_model()

abc = User.objects.last()
Product.objects.create(user=abc, title='My J user product', price=129.2)

datas = [
    {"title": "product 1", "price": 12.33},
    {"title": "product 2", "price": 52.33},
    {"title": "product 3", "price": 232.33},
]

first_product = datas[0]

not_saved_obj = Product(title='another one', price=123.12)
not_saved_obj.save()

Product.objects.create(title='another one', price=123.12)

Product(**first_product)

my_new_objs = []
for new_data in datas:
    # print(new_data)
    my_new_objs.append(Product(**new_data))


Product.objects.bulk_create(my_new_objs, ignore_conflicts=True)



# qs = Product.objects.all()
# qs.delete()

# obj = Product.objects.first()
# obj.delete()

# fixtures -> testing -> migrating data from databases

# psql, mysql

# db -> psql
# python manage.py inspectdb -> convert database table to django model