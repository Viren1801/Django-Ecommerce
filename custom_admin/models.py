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

class ProductAttribute(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=45,unique=True)
	description_text = models.TextField(null=True)
	created_by= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name='product_attribute_created_by',default='',null=True,blank=True)
	created_date = models.DateField(auto_now_add=True)
	modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_attribute_modify_by', default='', null=True, blank=True)
	modify_date = models.DateField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'product_atttribute'
		verbose_name= 'product attribute'
		verbose_name_plural = 'product attributes'

class ProductAttributeValues(models.Model):
	id = models.AutoField(primary_key=True)
	attribute_value = models.CharField(max_length=45)
	attribute_name = models.ForeignKey(ProductAttribute,on_delete= models.CASCADE)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_attribute_value_created_by',default='', null=True, blank=True)
	created_date = models.DateField(auto_now_add=True)
	modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_attribute_value_modify_by',default='', null=True, blank=True)
	modify_date = models.DateField(auto_now=True)


	def __str__(self):
		return self.attribute_value

class Product(models.Model):
	# import pdb
	# pdb.set_trace()
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, null=True)
	short_description = models.CharField(max_length=100,blank=True)
	lond_description = models.TextField(null=True)
	price = models.DecimalField(max_digits=9, decimal_places=2,null=True,validators=[MinValueValidator(0.0)])
	special_price = models.DecimalField(max_digits=9, decimal_places=2,null=True,blank=True,validators=[MinValueValidator(0.0)])
	special_price_from = models.DateField(blank=True,null= True)
	special_price_to = models.DateField(blank=True, null=True)
	quantity = models.IntegerField(null=True,validators=[MinValueValidator(0)])
	meta_title = models.CharField(max_length=50,null=True)
	meta_description=models.TextField(null=True)
	meta_keywords = models.TextField(null=True)
	product_categories = models.ManyToManyField(Category)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name='product_created_by',default='',null=True,blank=True)
	created_date = models.DateField(auto_now_add=True)
	modify_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name='product_modify_by',default='',null=True,blank=True)
	modify_date = models.DateField(auto_now=True)
	status=models.BooleanField()
	is_featured = models.BooleanField(default=False)

	class meta:
		ordering = ['-created_date']
		verbose_name = 'product'
		verbose_name_plural = 'products'

	@property
	def  special_price_test(self):
		if self.special_price and self.special_price_from and self.special_price_to:
			if date.today() > self.special_price_from and date.today() < self.special_price_to:
				return True
			else:
				return False
		else:
			return False

	@property
	def is_new(self):
		time_between_insertion = date.today() - self.created_date

		if time_between_insertion.days >15:
			return False
		else:
			return True


	def __str__(self):
		return self.name




class ProductImage(models.Model):
	id = models.AutoField(primary_key=True)
	image_name = models.ImageField(null=True,upload_to='uploads/product_images')
	status = models.BooleanField(default=False)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_image_created_by',default='', null=True, blank=True)
	created_date = models.DateField(auto_now_add=True)
	modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_image_modify_by',default='', null=True, blank=True)
	modify_date = models.DateField(auto_now=True)
	product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='product_image')

	class meta:
		db_table = 'product_image'
		verbose_name = 'product image'
		verbose_name_plural = 'product images'

	def __str__(self):
		return self.image_name



class ProductAttributeAssoc(models.Model):
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	product_attribute_id = models.ForeignKey(ProductAttribute,on_delete=models.DO_NOTHING)
	product_attribute_value_id = models.ForeignKey(ProductAttributeValues, on_delete=models.DO_NOTHING)

	class meta:
		db_table = 'product_attribute_assoc'
		verbose_name = 'product attribute assoc'
		verbose_name_plural = 'product attribute assoc'
