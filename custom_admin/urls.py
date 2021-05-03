from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views
from .views import CategoryList,ProductList

app_name = 'custom_admin'

urlpatterns = [
path('', views.index, name='index'),
path('login/',views.login, name = 'login'),
#path('register/',views.register, name = 'register'),
path('logout/',views.logoutUser, name = 'logout'),

# user management
path('users/', views.UserList, name='UserList'),
path('users/user_add', views.UserAdd, name='UserAdd'),
path('users/user_update/<int:id>', views.UserUpdate, name='UserUpdate'),
path('users/user_delete/<int:id>', views.UserDelete, name='UserDelete'),
path('users/user_change', views.UserChange, name='UserChange'),
path('users/user_change_psw', views.UserChangePsw, name='UserChangePsw'),
# category management
path('category/', views.category, name ='category'),
path('category/category_add', views.category_add, name ='AddCategory'),
path('category/category_update/<int:id>', views.category_update, name ='UpdateCategory'),
path('category/category_delete/<int:id>', views.category_delete, name ='CategoryDelete'),
path('category/', CategoryList.as_view(), name='category_test'),

# product attribute management
path('product_attribute/', views.Product_Attribute, name ='ProductAttribute'),
path('product_attribute/product_attribute_add/', views.ProductAttribute_add, name ='AddProductAttribute'),
path('product_attribute/product_attribute_update/<int:id>', views.product_attribute_update, name ='UpdateProductAttribute'),
path('product_attribute/product_attribute_delete/<int:id>', views.product_attribute_delete, name ='DeleteProductAttribute'),

    # product attribute value
path('product_attribute_value/', views.Product_Attribute_Value, name='ProductAttributeValue'),
path('product_attribute_value/product_attribute_value_add/', views.ProductAttributeValue_add, name='AddProductAttributeValue'),
path('product_attribute_value/product_attribute_value_update/<int:id>', views.ProductAttributeValue_update,name='UpdateProductAttributeValue'),
path('product_attribute_value/product_attribute_value_delete/<int:id>', views.ProductAttributeValue_delete,name='DeleteProductAttributeValue'),


path('product/', views.product, name ='product'),
path('product/product_add', views.product_add, name ='AddProduct'),
path('product/product_update/<int:id>', views.product_update, name ='UpdateProduct'),
path('product/product_delete/<int:id>', views.product_delete, name ='ProductDelete'),
path('product/', ProductList.as_view(), name='product_list'),
path('product/product_add/ajax/load-attribute/', views.load_product_attribute_value, name='ajax_load_product_attribute_value'),

]
