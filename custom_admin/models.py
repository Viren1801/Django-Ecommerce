from datetime import date, datetime

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True,null=False,blank=False)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff status'),default=False)


	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, null=True,unique=True)
	parent = models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name='catagory_created_by',default='',null=True,blank=True)
	created_date = models.DateField(auto_now_add=True)
	modify_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name='catogory_modify_by',default='',null=True,blank=True)
	modify_date = models.DateField(auto_now=True)
	status=models.BooleanField()

	class meta:
		ordering = ['-created_date']
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __str__(self):
		full_path = [self.name]
		p = self.parent
		while p is not None:
			full_path.append(p.name)
			p= p.parent
		return (' -> '.join(full_path[::-1]))
