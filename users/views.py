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

from users.tokens import account_activation_token
from users.forms import UserRegistrationForm, ContactForm
# Create your views here.

def index(request):
    return render(request, 'users/index.html')

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
    mail_subject = 'Activate your user account.'
    message = render_to_string('users/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
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
            user.save()
            activateEmail(request, user, registration_form.cleaned_data.get('email'))
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
        return render(request, 'users/registration.html', context)


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
                messages.success(request, f"welcome back <b>{user.username}</b>")
                return redirect(index)
        else:
            for error in list(login_form.errors.values()):
                messages.error(request, error)
                return redirect(custom_login)

    context = {'login_form':login_form}
    return render(request, 'users/login.html', context)


@login_required
def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'users/logout.html')
    else:
        return redirect(custom_login)


def contact(request):
    if request.method == 'GET':
        contact_form = ContactForm()
        context = {'contact_form':contact_form}
        return render(request, "users/contact.html", context)
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = "Website Inquiry" 
            body = {
            'first_name': contact_form.cleaned_data['first_name'], 
            'last_name': contact_form.cleaned_data['last_name'], 
            'email': contact_form.cleaned_data['email_address'], 
            'message':contact_form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())
            email = EmailMessage(subject, message, to=['sellfast.app@gmail.com'])
            if email.send():
                messages.success(request, f'We have received your message! We will contact you by email, check your inbox.')
                return redirect(contact)
            else:
                messages.error(request, f'ERROR: contact us by email at sellfast.app@gmail.com')
                return redirect(contact)


def faq(request):
    return render(request, 'users/faq.html')
