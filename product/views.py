from clinic.settings import MODELS_PER_PAGE
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.timezone import now
from product.forms import AddProductForm

from .models import Product, ProductImage
from panel.views import PanelView


class ProductView(PanelView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            is_valid = True
        except Product.DoesNotExist:
            product = None
            is_valid = False

        product.images = product.product_image_product.all()
        context = {'product': product, 'current_page': 'view_product', 'is_valid': is_valid}
        return render(request, 'product/product.html', context)


class ProductsView(PanelView):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, MODELS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'products': page_obj, 'current_page': 'products'}
        return render(request, 'product/products.html', context)


class DeleteProductView(PanelView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            product = None
        context = {'product': product, 'current_page': 'delete_product'}
        return render(request, 'product/delete_product.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('panel:product:product', pk)

        product = Product.objects.get(id=pk)
        product.delete()
        return redirect('panel:product:products')


class AddProductView(PanelView):
    def get(self, request):
        form = AddProductForm()
        context = {'form': form, 'current_page': 'add_product'}
        return render(request, 'product/add_product.html', context)

    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            form.cleaned_data.pop('images')
            form.cleaned_data.pop('captcha')
            new_product = Product(**form.cleaned_data,
                                  dateCreated=now,
                                  lastUpdated=now)
            new_product.save()
            for f in images:
                image = ProductImage(file=f, product=new_product)
                image.save()
            return redirect('panel:product:products')
        else:
            context = {'current_page': 'add_product', 'form': form}
            return render(request, 'product/add_product.html', context)


class EditProductView(PanelView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            product = None

        form = AddProductForm(instance=product)
        context = {'form': form, 'current_page': 'edit_product'}
        return render(request, 'product/edit_product.html', context)

    def post(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            product = None
        form = AddProductForm(request.POST, request.FILES, instance=product)
        images = request.FILES.getlist('images')
        if form.is_valid():
            form.cleaned_data.pop('images')
            form.cleaned_data.pop('captcha')

            product.save()
            for f in images:
                image = ProductImage(file=f, product=product)
                image.save()
            return redirect('panel:product:products')
        else:
            context = {'current_page': 'add_product', 'form': form}
            return render(request, 'product/add_product.html', context)