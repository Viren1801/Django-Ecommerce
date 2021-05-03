from django import forms
from .models import Category,ProductAttribute,ProductAttributeValues,Product,ProductImage,ProductAttributeAssoc
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):

    class Meta:
        User = get_user_model()
        model = User
        # fields = '__all__'
        fields = ('email','first_name','last_name','groups','user_permissions','is_active','password1','password2','is_staff')



    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
        self.fields['groups'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserUpdateForm(UserChangeForm):

    class Meta:
        User = get_user_model()
        model = User
        fields = ('email','first_name','last_name','groups','is_active')



    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
        self.fields['groups'].widget.attrs['class'] = 'form-control'


# class RegisterForm(UserCreationForm):
#
#     class Meta:
#         User = get_user_model()
#         model = User
#         fields = ('email','first_name','last_name','password1','password2',)
#
#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs['class'] = 'form-control'
#         self.fields['email'].widget.attrs['placeholder'] = 'email'
#         self.fields['first_name'].widget.attrs['class'] = 'form-control'
#         self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
#         self.fields['last_name'].widget.attrs['class'] = 'form-control'
#         self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['placeholder'] = 'password'
#         self.fields['password2'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'


class ChangeDetailForm(forms.ModelForm):

    class Meta:
        User = get_user_model()
        model = User
        fields = ('first_name','last_name',)

    def __init__(self, *args, **kwargs):
        super(ChangeDetailForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'first_name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last_name'

class OldPassForm(forms.Form):
    old_password = forms.CharField()

    class Meta:
        fields = ('old_password',)

    def __init__(self, *args, **kwargs):
        super(OldPassForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'old_password'
        self.fields['old_password'].widget.attrs['autocomplete'] = 'off'


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name','status','parent')
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),

        }

class ProductAttributeForm(forms.ModelForm):

    class Meta:
        model = ProductAttribute
        fields = ('name','description_text')

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class']='form-control'
        self.fields['description_text'].widget.attrs['class']='form-control'



class ProductAttributeValueForm(forms.ModelForm):

    class Meta:
        model = ProductAttributeValues
        fields = ('attribute_name','attribute_value')

    def __init__(self, *args, **kwargs):
        super(ProductAttributeValueForm, self).__init__(*args, **kwargs)
        self.fields['attribute_name'].widget.attrs['class'] = 'form-control'
        self.fields['attribute_value'].widget.attrs['class'] = 'form-control'

class ProductForm(forms.ModelForm):


    class Meta:
        TRUE_FALSE_CHOICES = [
            (True , 'True'),
            (False, 'False'),

        ]

        model = Product
        # fields ='__all__'
        fields = ('name','product_categories','status','short_description','lond_description','price','special_price','special_price_from','special_price_to','meta_title','meta_description','meta_keywords','is_featured','quantity')
        widgets = {

            'name':forms.TextInput(attrs={'class':'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'lond_description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=TRUE_FALSE_CHOICES,attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'is_featured':forms.Select(choices=TRUE_FALSE_CHOICES ,attrs={'class':'form-control'})

        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['product_categories'].widget.attrs['class'] = 'select2'
        self.fields['product_categories'].widget.attrs['multiple'] = 'multiple'
        self.fields['product_categories'].widget.attrs['data-dropdown-css-class'] = "se1lect2-blue"
        self.fields['product_categories'].widget.attrs['style'] = 'width: 100%;'
        self.fields['special_price_from'].widget.attrs['class'] = 'datepicker form-control'
        self.fields['special_price_from'].widget.attrs['autocomplete'] = 'off'
        self.fields['special_price_to'].widget.attrs['class'] = 'datepicker form-control'
        self.fields['special_price_to'].widget.attrs['autocomplete'] = 'off'

class ProductImageForm(forms.ModelForm):
    class Meta:
        model =ProductImage
        fields = '__all__'
        exclude = ['created_by','modify_by','created_date','modify_date','product']

    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)
        self.fields['image_name'].widget.attrs['class']='form-control'



class ProductAttributeAssocForm(forms.ModelForm):

    class Meta:
        model = ProductAttributeAssoc
        fields = ('product_attribute_id','product_attribute_value_id')
        widgets = {
        'product_attribute_id': forms.Select(attrs={'class': 'form-control p-id-changed'}),
        'product_attribute_value_id': forms.Select(attrs={'class': 'form-control p-value-changed'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_attribute_value_id'].queryset = ProductAttributeValues.objects.none()

        if self.add_prefix('product_attribute_id') in self.data:
            try:
                product_attribute_id = int(self.data.get(self.add_prefix('product_attribute_id')))
                self.fields['product_attribute_value_id'].queryset = ProductAttributeValues.objects.filter(attribute_name=product_attribute_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['product_attribute_value_id'].queryset = self.instance.product_attribute_id.productattributevalues_set.all()
