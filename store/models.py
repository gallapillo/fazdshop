from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import  ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewName, model_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewName, keyargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


# ****
#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Order
# ****
#6 Customer
#7 Specification


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Консоли': 'console__count',
        'Смартфоны': 'smartphone__count',
        'Ps3Game': 'ps3game__count',
        'Ps4Game': 'ps4game__count',
        'Видеокарты': 'graphicscard__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone','console','ps3game','ps4game','graphicscard' )
        qs = list(self.get_queryset().annotate(*models))
        #data = [dict(name=c['name'], slug=c['slug'], count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        qs = self.get_queryset().annotate(*models).values()
        #print(qs)
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return  reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    class Meta:
        abstract = True# нельзя создать миграцию

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True, default=0)
    title = models.CharField(max_length=255, verbose_name='Наименование', null=True, default=0)
    slug = models.SlugField(unique=True, null=True, default=0)
    image = models.ImageField(verbose_name='Изображение', null=True, default=0)
    description = models.TextField(null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', null=True, default=0)

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    display_resolution = models.CharField(max_length=255, verbose_name='Разрешение')
    processor_name = models.CharField(max_length=255, verbose_name='Название процессора')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    processor_cores = models.CharField(max_length=255, verbose_name='Кол-во ядер процессора')
    ram = models.CharField(max_length=255, verbose_name='ОЗУ')
    Video_name = models.CharField(max_length=255, verbose_name='Название видеокарты')
    Video = models.CharField(max_length=255, verbose_name='Кол-во видеопамяти')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время автономности')
    storage = models.CharField(max_length=255, verbose_name='Объем ПЗУ')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


    def get_absolute_url(self):
        return get_product_url(self,'product-detail')



class Ps3Game(Product):
    age = models.CharField(max_length=255, verbose_name='Возрастной рейтинг')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


    def get_absolute_url(self):
        return get_product_url(self,'product-detail')


class Ps4Game(Product):
    age = models.CharField(max_length=255, verbose_name='Возрастной рейтинг')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


    def get_absolute_url(self):
        return get_product_url(self,'product-detail')


class Console(Product):
    gen = models.CharField(max_length=255, verbose_name='Поколение консоли')
    manufacture = models.CharField(max_length=255, verbose_name='Производитель')
    year = models.CharField(max_length=255, verbose_name='Год производства')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


    def get_absolute_url(self):
        return get_product_url(self,'product-detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    display_resolution = models.CharField(max_length=255, verbose_name='Разрешение')
    processor_name = models.CharField(max_length=255, verbose_name='Название процессора')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    processor_cores = models.CharField(max_length=255, verbose_name='Кол-во ядер процессора')
    Video_name = models.CharField(max_length=255, verbose_name='Название видеокарты')
    accum_volume = models.CharField(max_length=255, verbose_name='объем аккумулятора')
    ram = models.CharField(max_length=255, verbose_name='ОЗУ')
    sd = models.BooleanField(default=True)
    storage = models.CharField(max_length=255, verbose_name='Объем ПЗУ')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')


    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


    def get_absolute_url(self):
        return get_product_url(self,'product-detail')


class GraphicsCard(Product):
    videoСard_name = models.CharField(max_length=255, verbose_name='Название видеокарты')
    videoСard_vram_count = models.CharField(max_length=255, verbose_name='Кол-во видеопамяти')
    videoСard_vram_type = models.CharField(max_length=255, verbose_name='Тип видеопамяти')
    videoCard_bus = models.CharField(max_length=255, verbose_name='Разрядность Шины')


    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


    def get_absolute_url(self):
        return get_product_url(self,'product-detail')



class CartProduct(Product):

    user = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, null=True, default=0)
    #product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)# положительная целое число
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)



class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE, null=True, default=0)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')#Свзяь многим к многим
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE )
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


#class Specifications(models.Model):

 #   content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  #  object_id = models.PositiveIntegerField()
   # name = models.CharField(max_length=255, verbose_name='Имя товара для харктеристик')

    #def __str__(self):
     #   return "Характеристика для товара: {}".format(self.name)



