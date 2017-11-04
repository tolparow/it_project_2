from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from .forms import RegistrationForm, LoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse


@csrf_protect
def signup_view(request):
    """
    Context description:
    form - form with fields (see profile_management.forms.RegistrationForm)
    :param request:
    :return:
    """
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('confirm_your_email'))
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    context = {
        'form': form,
    }

    return TemplateResponse(request, 'www/profiles/signup.html', context)


@csrf_protect
def login_view(request):
    """
    Context description:
    form_valid - describes validity of the form
    email_not_confirmed - describes status of confirmation of the email
    :param request:
    :return:
    """
    form_valid = True
    email_not_confirmed = False

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    elif request.method == "POST":
        password = request.POST.get("password", "")
        username = request.POST.get("username", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.email_confirmed:
                login(request, user)
                if not request.POST.get('remember', None):
                    request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('home'))
            else:
                email_not_confirmed = True
        else:
            form_valid = False

    context = {
        'form_valid': form_valid,
        'email_not_confirmed': email_not_confirmed,
    }

    return TemplateResponse(request, 'www/profiles/login.html', context)

@csrf_protect
def restore_view(request):
    return TemplateResponse(request, 'www/profiles/restore.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
