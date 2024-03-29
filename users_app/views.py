from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from users_app.tokens import account_activation_token
from users_app.forms import UserRegistrationForm, ContactForm, WhitelistForm, CustomAuthenticationForm
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'main_app/dashboard.html')
    else:
        registration_form = UserRegistrationForm()
        context = {'registration_form':registration_form}
        return render(request, 'users_app/index.html', context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect(custom_login)
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect(index)

def activateEmail(request, user, to_email):
    mail_subject = 'SellFast - Activate your user account.'
    message = render_to_string('users_app/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def registration(request):
    if request.user.is_authenticated:
        return redirect(index)
    
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save(commit=False)
            user.is_active = False
            user.username = registration_form.cleaned_data.get('email')
            user.save()
            #activateEmail(request, user, registration_form.cleaned_data.get('email'))
            email = EmailMessage('User +1', 'daje', to=['francescozedde711@gmail.com'])
            email.send()
            #login(request, user)
            #messages.success(request, f"Hello <b>{user.username}</b>, your account has been created.")
            return redirect(index)
        else:
            for error in list(registration_form.errors.values()):
                messages.error(request, error)
                return redirect(registration)
    else:
        registration_form = UserRegistrationForm()
        context = {'registration_form':registration_form}
        return render(request, 'users_app/registration.html', context)


def custom_login(request):
    login_form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect(index)

    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"You're logged in!")
                return redirect(index)
        else:
            for error in list(login_form.errors.values()):
                messages.error(request, error)
                return redirect(custom_login)

    login_form = CustomAuthenticationForm()
    context = {'login_form':login_form}
    return render(request, 'users_app/login.html', context)


@login_required
def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'users_app/logout.html')
    else:
        return redirect(custom_login)


def contact(request):
    if request.method == 'GET':
        contact_form = ContactForm()
        context = {'contact_form':contact_form}
        return render(request, "users_app/contact.html", context)
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = contact_form.cleaned_data['problem'] 
            body = {
            'message': contact_form.cleaned_data['message'], 
            'email': contact_form.cleaned_data['email_address'], 
            }
            message = "\n".join(body.values())
            email = EmailMessage(subject, message, to=['sellfast.app@gmail.com'])
            if email.send():
                messages.success(request, f'Message received, talk to you soon!')
                return redirect(contact)
            else:
                messages.error(request, f'ERROR: contact us by email at sellfast.app@gmail.com')
                return redirect(contact)
        else:
            messages.error(request, f'Please insert a valid email value')
            return redirect(contact)

def whitelist(request):
    if request.method == 'GET':
        whitelist_form = WhitelistForm()
        context = {'whitelist_form':whitelist_form}
        return render(request, "users_app/whitelist.html", context)
    if request.method == 'POST':
        whitelist_form = WhitelistForm(request.POST)
        if whitelist_form.is_valid():
            subject = "Whitelist request" 
            body = {
            'first_name': whitelist_form.cleaned_data['first_name'], 
            'last_name': whitelist_form.cleaned_data['last_name'], 
            'email': whitelist_form.cleaned_data['email_address'], 
            }
            message = "\n".join(body.values())
            email = EmailMessage(subject, message, to=['sellfast.app@gmail.com'])
            if email.send():
                messages.success(request, f'We have received your message! We will contact you by email, check your inbox.')
                return redirect(whitelist)
            else:
                messages.error(request, f'ERROR: contact us by email at sellfast.app@gmail.com')
                return redirect(whitelist)
        else:
            messages.error(request, f'ERROR: contact us by email at sellfast.app@gmail.com')
            return redirect(whitelist)

def faq(request):
    return render(request, 'users_app/faq.html')


def terms_and_conditions(request):
    return render(request, 'users_app/terms_and_conditions.html')
