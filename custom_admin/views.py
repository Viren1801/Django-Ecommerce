from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError, transaction

# forms
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .forms import UserForm,ChangeDetailForm,OldPassForm,UserUpdateForm,CategoryForm,ProductAttributeForm,ProductAttributeValueForm,ProductImageForm,ProductAttributeAssocForm,ProductForm

from custom_admin.models import Category,ProductAttribute,ProductAttributeValues,Product,ProductImage, ProductAttributeAssoc

from django.forms import inlineformset_factory

from .decorators import unauthenticated_user, allowed_users
from .models import User

# Create your views here.
@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin','category_manager'])
def index(request):
    return render(request, 'custom_admin/starter.html')


# @unauthenticated_user
def login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        valuenext = request.POST.get('next')

        user = authenticate(request, username=username, password=password)

        groups = request.user.groups.values_list('name',flat = True)
        if user is not None and valuenext == '':

            if 'admin' or 'category_manager' in groups or user.is_superuser :
                auth_login(request, user)
                messages.success(request, 'you are logged in')
                return redirect('custom_admin:index')
            else:
                messages.warning(request, 'you are not authorized for it')
        elif user is not None and valuenext != '':

            if 'admin' or 'category_manager' in groups or user.is_superuser:
                auth_login(request, user)
                return redirect(valuenext)
            else:
                messages.warning(request, 'you are not authorized for it')
        else:
            messages.info(request, 'please enter right credentials')

    return render(request, 'custom_admin/login.html')


def logoutUser(request):
    logout(request)
    return redirect('custom_admin:login')


# @unauthenticated_user
# def register(request):
#
# 	if request.method == 'POST':
# 		user_form = UserForm(request.POST)
# 		profile_form = ProfileForm(request.POST)
# 		if user_form.is_valid() and profile_form.is_valid():
# 			form=user_form.save()
# 			profile_form = profile_form.save(commit=False)
# 			profile_form.user=form
# 			profile_form.save()
# 			# user = form.cleaned_data.get('username')
# 			messages.success(request, 'Your profile was successfully created!')
# 			return redirect('custom_admin:login')
# 		else:
# 			messages.error(request, ('Please correct the error below.'))
# 	else:
# 		user_form = UserForm()
# 		profile_form = ProfileForm()
# 	return render(request, 'custom_admin/register.html', {
# 		'user_form': user_form,
# 		'profile_form': profile_form
# 	})


# ----------------------------------------- users -------------------------------------------------
@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def UserList(request):
    users = User.objects.all()
    return render(request, 'custom_admin/user_list.html', {'users': users})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def UserChange(request):
    instance = request.user
    if request.method == 'POST':
        form = ChangeDetailForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('custom_admin:index')
    else:
        form = ChangeDetailForm(instance=instance)
    return render(request, 'custom_admin/change_detail.html', {'form': form})


@login_required(login_url='custom_admin:login')
def UserChangePsw(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            # instance = form.save(commit=False)
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                user = request.user
                print(user.password)
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'password change succesfully')
                    return redirect('custom_admin:index')
                else:
                    messages.warning(request, 'your current password  password is not matched ')
            else:
                messages.error(request, 'new password and current password is not matched ')

    form = ChangePasswordForm()

    return render(request, 'custom_admin/change_psw.html', {'form': form})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def UserAdd(request):
    if request.method == 'POST':

        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "user added succesfully")
            return redirect('custom_admin:UserList')
    else:
        form = UserForm()
    return render(request, 'custom_admin/user_add.html', {'form': form, })


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def UserUpdate(request, id):
    instance = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=instance)
        print('in view')
        if form.is_valid():
            form.save()
            messages.success(request, "user updated successfuly")
            return redirect('custom_admin:UserList')
    else:
        form = UserUpdateForm(instance=instance)

    return render(request, 'custom_admin/user_update.html', {'form': form, 'id': id})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def UserDelete(request, id):
    data = get_object_or_404(User, id=id)
    try:
        data.delete()
        messages.success(request, "user deleted succesfully")
    except IntegrityError:
        messages.warning(request, "user cant deleted because of integrity")

    return redirect('custom_admin:UserList')

#------------------------------------------category--------------------------------------------------

@login_required(login_url='custom_admin:login')
def category(request):

	categories=Category.objects.all()
	page = request.GET.get('page', 1)

	paginator = Paginator(categories, 4)
	try:
		categories = paginator.page(page)
	except PageNotAnInteger:
		categories = paginator.page(1)
	except EmptyPage:
		categories = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		page_n = request.POST.get('page_n', None)  # getting page number
		categories1 = paginator.page(page_n).object_list

		categories  =serializers.serialize('json',categories1)

		categories = list(paginator.page(page_n).object_list.values('id','name','parent','created_date',
															'modify_date'))
		return JsonResponse(categories,content_type='application/json',safe=False)

	return render(request, 'custom_admin/category.html',{'categories':categories})

@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin','category_manager'])
def category_add(request):
    if request.method == 'POST':

        form = CategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.modify_by = request.user
            instance.save()
            messages.success(request, "category added succesfully")
            return redirect('custom_admin:category_test')
    else:
        form = CategoryForm()
    return render(request, 'custom_admin/category_add.html', {'form': form, })


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin','category_manager'])
def category_update(request, id):
    instance = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=instance)
        # print(form)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modify_by = request.user
            instance.save()
            messages.success(request, "category updated successfuly")
            return redirect('custom_admin:category_test')
    else:
        form = CategoryForm(instance=instance)

    return render(request, 'custom_admin/category_update.html', {'form': form, 'id': id})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin','category_manager'])
def category_delete(request, id):
    data = get_object_or_404(Category, id=id)
    try:
        data.delete()
        messages.success(request, "category deleted succesfully")
    except IntegrityError:
        messages.warning(request, "category have child value or product so cant delete")

    return redirect('custom_admin:category_test')

@method_decorator(login_required(login_url='custom_admin:login'), name='dispatch')
class CategoryList(TemplateView):
    template_name = 'custom_admin/list/category_test.html'




# ------------------------------------------product attribute--------------------------------------------------
@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute(request):
    product_attributes = ProductAttribute.objects.all()

    return render(request, 'attribute/product_attribute.html', {'product_attributes': product_attributes})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def ProductAttribute_add(request):
    if request.method == 'POST':
        # import pdb
        # pdb.set_trace()
        form = ProductAttributeForm(request.POST)
        # print(form)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.modify_by = request.user
            instance.save()
            # form.save_m2m()
            messages.success(request, "product attribute  added succesfully")
            return redirect('custom_admin:ProductAttribute')
    else:
        form = ProductAttributeForm()
    return render(request, 'attribute/product_attribute_add.html', {'form': form, })


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def product_attribute_update(request, id):
    instance = get_object_or_404(ProductAttribute, id=id)
    if request.method == 'POST':
        form = ProductAttributeForm(request.POST, instance=instance)
        # print(form)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modify_by = request.user
            instance.save()
            # form.save_m2m()
            messages.success(request, "product attribute updated successfuly")
            return redirect('custom_admin:ProductAttribute')

    else:
        form = ProductAttributeForm(instance=instance)

    return render(request, 'attribute/product_attribute_update.html', {'form': form, 'id': id})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def product_attribute_delete(request, id):
    data = get_object_or_404(ProductAttribute, id=id)
    try:
        data.delete()
        messages.success(request, "product attribute deleted succesfully")
    except IntegrityError:
        messages.warning(request, "product attribute have products so cant delete")

    return redirect('custom_admin:ProductAttribute')


# ------------------------------------------product attribute value--------------------------------------------------

@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Value(request):
    product_attribute_values = ProductAttributeValues.objects.all()

    return render(request, 'attribute/product_attribute_value.html',
                  {'product_attribute_values': product_attribute_values})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def ProductAttributeValue_add(request):
    if request.method == 'POST':
        form = ProductAttributeValueForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.modify_by = request.user
            instance.save()
            # form.save_m2m()
            messages.success(request, "product attribute value  added succesfully")
            return redirect('custom_admin:ProductAttributeValue')

    form = ProductAttributeValueForm()
    return render(request, 'attribute/product_attribute_value_add.html', {'form': form, })


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def ProductAttributeValue_update(request, id):
    instance = get_object_or_404(ProductAttributeValues, id=id)
    if request.method == 'POST':
        form = ProductAttributeValueForm(request.POST, instance=instance)
        print(form)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modify_by = request.user
            instance.save()
            # form.save_m2m()
            messages.success(request, "product attribute value updated successfuly")
            return redirect('custom_admin:ProductAttributeValue')


    else:
        form = ProductAttributeValueForm(instance=instance)

    return render(request, 'attribute/product_attribute_value_update.html', {'form': form, 'id': id})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def ProductAttributeValue_delete(request, id):
    data = get_object_or_404(ProductAttributeValues, id=id)
    try:
        data.delete()
        messages.success(request, "product attribute deleted succesfully")
    except IntegrityError:
        messages.warning(request, "product attribute have products so cant delete")

    return redirect('custom_admin:ProductAttributeValue')


# ------------------------------------------product--------------------------------------------------

@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def product(request):
	products=Product.objects.all()
	return render(request, 'custom_admin/product.html',{'products':products})



@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def product_add(request):
    ProductImageFormset = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)
    ProductAttributeFormset = inlineformset_factory(Product, ProductAttributeAssoc, form=ProductAttributeAssocForm,
                                                    extra=1)

    if request.method == 'POST':

        form = ProductForm(request.POST)
        formset = ProductImageFormset(request.POST, request.FILES)
        formset2 = ProductAttributeFormset(request.POST)

        if form.is_valid() and formset.is_valid() and formset2.is_valid():
            with transaction.atomic():
                instance = form.save(commit=False)
                instance.created_by = request.user
                instance.modify_by = request.user
                instance.save()
                form.save_m2m()

                for image in formset:
                    if image.is_valid():
                        image = image.save(commit=False)
                        image.product = instance
                        image.save()

                for attribute in formset2:
                    if attribute.is_valid() and attribute.has_changed():
                        attribute = attribute.save(commit=False)
                        attribute.product_id = instance
                        attribute.save()

                messages.success(request, "product added succesfully")
            return redirect('custom_admin:product_list')

    else:
        form = ProductForm(request.GET or None)
        formset2 = ProductAttributeFormset()
        formset = ProductImageFormset()

    return render(request, 'custom_admin/product_add.html', {'form': form, 'formset2': formset2, 'formset': formset})


def load_product_attribute_value(request):
    product_attribute_id = request.GET.get('product_attribute_id')
    print(product_attribute_id)
    product_attribute_value_ids = ProductAttributeValues.objects.filter(attribute_name=product_attribute_id)
    return render(request, 'attribute/ajax/product_attribute_list_options.html',
                  {'product_attribute_value_ids': product_attribute_value_ids})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    ProductImageFormset = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)
    ProductAttributeFormset = inlineformset_factory(Product, ProductAttributeAssoc, form=ProductAttributeAssocForm,
                                                    extra=1)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormset(request.POST, request.FILES, instance=product)
        formset2 = ProductAttributeFormset(request.POST, instance=product)

        if form.is_valid() and formset.is_valid() and formset2.is_valid():
            with transaction.atomic():
                # import pdb
                # pdb.set_trace()
                instance = form.save(commit=False)
                instance.modify_by = request.user
                instance.save()
                form.save_m2m()
                formset2.save()

                for image in formset:
                    if image.is_valid() and image.has_changed():
                        image = image.save(commit=False)
                        image.product = instance
                        image.save()

                instance2 = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()

                instance3 = formset2.save(commit=False)
                for obj in formset2.deleted_objects:
                    obj.delete()

                messages.success(request, "product edited succesfully")
            return redirect('custom_admin:product_list')

    else:

        form = ProductForm(request.GET or None, instance=product)
        formset2 = ProductAttributeFormset(instance=product)
        formset = ProductImageFormset(instance=product)

    return render(request, 'custom_admin/product_update.html',
                  {'form': form, 'formset2': formset2, 'formset': formset, 'id': id})


@login_required(login_url='custom_admin:login')
@allowed_users(allowed_roles=['admin'])
def product_delete(request, id):
    data = get_object_or_404(Product, id=id)
    try:
        data.delete()
        messages.success(request, "product deleted succesfully")
    except IntegrityError:
        messages.warning(request, "product cant delete")

    return redirect('custom_admin:product_list')

@method_decorator(login_required(login_url='custom_admin:login'), name='dispatch')
class ProductList(TemplateView):
    template_name = 'custom_admin/list/product_list.html'
