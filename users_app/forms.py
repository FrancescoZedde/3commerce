from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from users_app.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1']
    
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        #self.fields['username'].help_text = None
        #self.fields['username'].label = 'Email'
        self.fields['password1'].help_text = None
        #self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['password'].label = 'Password'


class WhitelistForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)

class ContactForm(forms.Form):

    options = (("account","Account related problems"),
    ("feature","Request feature"),
    ("payment","Billing"),
    ("bug","Report bug"),
    ("other","Other"))

    email_address = forms.EmailField(max_length = 150)
    problem = forms.TypedChoiceField(label='',choices=options, required=True)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)

class WooCommerceConnectForm(forms.Form):
    woocommerce_store_name = forms.CharField(max_length = 30, required=True, help_text='store name')
    woocommerce_host = forms.CharField(max_length = 100, required=True, help_text='Paste in format "https://yourdomain.com"')
    woocommerce_consumer_key = forms.CharField(max_length = 250, required=True, help_text='Public key')
    woocommerce_secret_key = forms.CharField(max_length = 250, required=True, help_text='Secret key')

class ShopifyConnectForm(forms.Form):
    shopify_store_name = forms.CharField(max_length = 30, required=True, help_text='Paste you store name. Example: if your URL is https://yourshop.myshopify.com, then you must paste only "yourshop"')
    shopify_host = forms.CharField(max_length = 100, required=True, help_text='Paste in format "https://yourdomain.com"')
    shopify_consumer_key = forms.CharField(max_length = 250, required=True, help_text='Public key')
    shopify_secret_key = forms.CharField(max_length = 250, required=True, help_text='Secret key')
    def __init__(self, *args, **kwargs):
        super(ShopifyConnectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['shopify_store_name'].label = False


class CJDropshippingConnectForm(forms.Form):
    cjdropshipping_email = forms.CharField(max_length = 250, required=True, help_text='Email')
    cjdropshipping_api_key = forms.CharField(max_length = 250, required=True, help_text='API key')
    def __init__(self, *args, **kwargs):
        super(CJDropshippingConnectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['cjdropshipping_email'].label = False
        self.fields['cjdropshipping_api_key'].label = False