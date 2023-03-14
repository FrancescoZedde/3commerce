from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class WooCommerceConnectForm(forms.Form):
    woocommerce_store_name = forms.CharField(max_length = 30, required=True, help_text='Your store name')
    woocommerce_host = forms.CharField(max_length = 100, required=True, help_text='Paste in format "https://yourdomain.com"')
    woocommerce_consumer_key = forms.CharField(max_length = 250, required=True, help_text='Public key')
    woocommerce_secret_key = forms.CharField(max_length = 250, required=True, help_text='Secret key')

class ShopifyConnectForm(forms.Form):
    shopify_store_name = forms.CharField(max_length = 30, required=True, help_text='Your store name')
    shopify_host = forms.CharField(max_length = 100, required=True, help_text='Paste in format "https://yourdomain.com"')
    shopify_consumer_key = forms.CharField(max_length = 250, required=True, help_text='Public key')
    shopify_secret_key = forms.CharField(max_length = 250, required=True, help_text='Secret key')