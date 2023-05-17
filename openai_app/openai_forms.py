from django import forms
from django.forms import ModelForm, TextInput, Textarea
from main_app.models import InventoryItem, Variant
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper

class ChatGPTAsk(forms.Form):
    question = forms.CharField(max_length = 250, required=True, help_text='Ask whatever you want')
    n_copies = forms.IntegerField(max_value=4, min_value=1, initial=3,help_text='n images', widget=forms.NumberInput(attrs={'class': 'max_words'}))
    def __init__(self, *args, **kwargs):
        super(ChatGPTAsk, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['question'].label = False
        self.fields['n_copies'].label = False
        

tone_of_voice = [('funny', 'Funny'),
                ('professional','Professional'),
                ('excited','Excited'),
                ('descriptive', 'Descriptive'),
                ('humorous', 'Humorous'),
                ('inspirational', 'Inspirational'),
                ('formal', 'Formal'),]

languages = [   ('english','English'),
                ('italian', 'Italian'),
                ('french','French'),
                ('spanish', 'Spanish'),]

class BlogArticleForm(forms.Form):
    form_id = forms.CharField(initial='blog-article',widget = forms.HiddenInput())
    topic = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'style':''}))
    word_count = forms.IntegerField(initial=110)
    keywords = forms.CharField(max_length=50)
    target_audience = forms.CharField(max_length=50)
    #purpose = forms.CharField(max_length=100)
    tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style':'', 'size':'1'}))
    language = forms.ChoiceField(choices=languages)
    #style = forms.CharField(max_length=100)
    
class BlogIdeasForm(forms.Form):
    form_id = forms.CharField(initial='blog-ideas',widget = forms.HiddenInput())
    topic = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'style':''}))
    #word_count = forms.IntegerField(initial=110)
    keywords = forms.CharField(max_length=50)
    target_audience = forms.CharField(max_length=50)
    language = forms.ChoiceField(choices=languages)
    #purpose = forms.CharField(max_length=100)
    #tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style':'', 'size':'1'}))
    #style = forms.CharField(max_length=100)

class BlogPlagiarismForm(forms.Form):
    form_id = forms.CharField(initial='blog-plagiarism',widget = forms.HiddenInput())
    text = forms.CharField(label='Paste your text:', help_text='', widget=forms.Textarea(attrs={
                                                    'class': "form-control",
                                                    'rows': 15, 
                                                    'style': 'max-width: 100%; font-size: 12px;',
                                                    }))

class FacebookAdsForm(forms.Form):
    form_id = forms.CharField(initial='facebook-ads',widget=forms.HiddenInput())
    topic = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'style': 'font-size: 12px;'}))
    tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style': 'font-size: 12px;', 'size': '1'}))
    keywords = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'style': 'font-size: 12px;'}))
    target_audience = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'style': 'font-size: 12px;'}))
    word_count = forms.IntegerField(initial=100, widget=forms.NumberInput(attrs={'style': 'font-size: 12px;'}))
    n_copies = forms.IntegerField(initial=3, widget=forms.NumberInput(attrs={'style': 'font-size: 12px;'}))
    emoji = forms.BooleanField(label='Check to use emoji',initial=False, required=False, widget=forms.CheckboxInput(attrs={'style': 'font-size: 12px;'}))
    bullet_list = forms.BooleanField(label='Check to use bullet point list',initial=False, required=False, widget=forms.CheckboxInput(attrs={'style': 'font-size: 12px;'}))
    language = forms.ChoiceField(choices=languages, widget=forms.Select(attrs={'style': 'font-size: 12px;', 'size': '1'}))


class FacebookPostForm(forms.Form):
    form_id = forms.CharField(initial='facebook-post',widget=forms.HiddenInput())
    topic = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'style': 'font-size: 12px;'}))
    tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style': 'font-size: 12px;', 'size': '1'}))
    keywords = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'style': 'font-size: 12px;'}))
    target_audience = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'style': 'font-size: 12px;'}))
    word_count = forms.IntegerField(initial=100, widget=forms.NumberInput(attrs={'style': 'font-size: 12px;'}))
    n_copies = forms.IntegerField(initial=3, widget=forms.NumberInput(attrs={'style': 'font-size: 12px;'}))
    emoji = forms.BooleanField(label='Check to use emoji',initial=False, required=False, widget=forms.CheckboxInput(attrs={'style': 'font-size: 12px;'}))
    bullet_list = forms.BooleanField(label='Check to use bullet point list',initial=False, required=False, widget=forms.CheckboxInput(attrs={'style': 'font-size: 12px;'}))
    language = forms.ChoiceField(choices=languages, widget=forms.Select(attrs={'style': 'font-size: 12px;', 'size': '1'}))
        

class FacebookPostIdeasForm(forms.Form):
    form_id = forms.CharField(initial='facebook-post-ideas',widget = forms.HiddenInput())
    topic = forms.CharField(max_length=100)
    #tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style':'', 'size':'1'}))
    keywords = forms.CharField(max_length=50)
    target_audience = forms.CharField(max_length=50)
    language = forms.ChoiceField(choices=languages)
    #word_count = forms.IntegerField(initial=100)
    #purpose = forms.CharField(max_length=100)


class InstagramPostForm(forms.Form):
    form_id = forms.CharField(initial='instagram-post',widget = forms.HiddenInput())
    topic = forms.CharField(max_length=100)
    tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style':'', 'size':'1'}))
    keywords = forms.CharField(max_length=50)
    target_audience = forms.CharField(max_length=50)
    word_count = forms.IntegerField(initial=100)
    #purpose = forms.CharField(max_length=100)
    n_copies = forms.IntegerField(initial=3)
    language = forms.ChoiceField(choices=languages)
    emoji = forms.BooleanField(label='Use emoji',initial=False, required=False)
    bullet_list = forms.BooleanField(label='Use bullet point list',initial=False, required=False)

class InstagramTagsForm(forms.Form):
    form_id = forms.CharField(initial='instagram-tags',widget = forms.HiddenInput())
    topic = forms.CharField(max_length=100)
    keywords = forms.CharField(label="Related tags:",max_length=50)
    target_audience = forms.CharField(max_length=50)
    #word_count = forms.IntegerField(initial=20)
    language = forms.ChoiceField(choices=languages)

class GoogleAdsTitleForm(forms.Form):
    form_id = forms.CharField(initial='google-ads-title',widget = forms.HiddenInput())
    topic = forms.CharField(label="Product/Service Name",max_length=100)
    n_copies = forms.IntegerField(initial=3)
    language = forms.ChoiceField(choices=languages)

class GoogleAdsDescriptionForm(forms.Form):
    form_id = forms.CharField(initial='google-ads-description',widget = forms.HiddenInput())
    topic = forms.CharField(label="Product/Service Name",max_length=100)
    n_copies = forms.IntegerField(initial=3)
    language = forms.ChoiceField(choices=languages)

class EmailMarketingForm(forms.Form):
    form_id = forms.CharField(initial='email-marketing',widget = forms.HiddenInput())
    topic = forms.CharField(max_length=100)
    tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style':'', 'size':'1'}))
    keywords = forms.CharField(max_length=50)
    target_audience = forms.CharField(max_length=50)
    word_count = forms.IntegerField(initial=100)
    #purpose = forms.CharField(max_length=100)

class AmazonProductDescription(forms.Form):
    form_id = forms.CharField(initial='amazon-description',widget = forms.HiddenInput())
    topic = forms.CharField(max_length=100)
    tone = forms.ChoiceField(choices=tone_of_voice, widget=forms.Select(attrs={'style':'', 'size':'1'}))
    keywords = forms.CharField(max_length=50)
    target_audience = forms.CharField(max_length=50)
    word_count = forms.IntegerField(initial=100)
    #purpose = forms.CharField(max_length=100)
