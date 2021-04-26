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

from .forms import UserForm,ChangeDetailForm,OldPassForm,UserUpdateForm,CategoryForm

from custom_admin.models import Category

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
