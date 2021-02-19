from django.db import transaction
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from django.http import HttpResponseRedirect

from .models import Notebook, Smartphone, Ps3Game, Ps4Game, Console, GraphicsCard, Category, LatestProducts, Customer, Cart

from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request , *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone','console','ps3game','ps4game','graphicscard')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'store/base.html', context)

#def test_view(request):
    #categories = Category.objects.get_categories_for_left_sidebar()
    #return render(request, 'store/base.html', {'categories': categories})


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
        'ps3game': Ps3Game,
        'ps4game': Ps4Game,
        'console': Console,
        'graphicscard': GraphicsCard,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'store/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        print(kwargs.get('ct_model'))
        print(kwargs.get('slug'))
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'store/category_detail.html'
    slug_url_kwarg = 'slug'

class AddToCartView(View):

    def get(self, request, *args, **kwargs):

        return HttpResponseRedirect('/cart/')



class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(name=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': cart,
            'categories': categories
        }
        return render(request, 'store/cart.html',context)