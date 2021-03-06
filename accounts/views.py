from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserRegistrationForm, UserLoginForm
from subscription.models import UserSubscription, SubscriptionType
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def register(request):
    """
    A view that manages the registration form.
    If method is GET, an empty registration form is rendered.
    If method is POST, the user is saved and then logged in.
    """
    if request.method == 'POST':
        #print(request.POST.keys())
        #dict_keys(['csrfmiddlewaretoken', 'username', 'email', 'password1', 'password2'])
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            # create the user in the database
            registration_form.save()

            user = auth.authenticate(request.POST.get('email'),
                                    password=request.POST.get('password1'))

            if user is not None:
                # save user id in the session
                auth.login(request, user)

                messages.success(request, 'You have successfully registered.')

                return redirect(reverse('subscription:choose_subscription'))
            else:
                messages.error(request, 'Unable to log you in at this time!')
    else:
        registration_form = UserRegistrationForm()

    context = {'registration_form': registration_form}
    return render(request, 'accounts/register.html', context)

@login_required
def profile(request):
    """
    A view that displays the profile page of a logged in user.
    """
    try:
        user_subscription = UserSubscription.objects.get(user_id=request.user.id)
    except UserSubscription.DoesNotExist:
        user_subscription = None

    context = {'user_subscription': user_subscription}
    return render(request, 'accounts/profile.html', context)

@login_required
def logout(request):
    """
    A view that logs the user out and redirects back to the index page.
    """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect(reverse('home:index'))

def login(request):
    """
    A view that manages the login form.
    If method is GET, an empty login form is rendered.
    If method is POST, the user is logged in.
    """
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request.POST.get('username_or_email'),
                                    password=request.POST.get('password'))

            if user is not None:
                # save user id in the session
                auth.login(request, user)

                # update subscription status
                try:
                    user_subscription = UserSubscription.objects.get(user_id=request.user.id)
                except UserSubscription.DoesNotExist:
                    user_subscription = None
                
                if user_subscription:
                    if user_subscription.end_date < timezone.now():
                        user_subscription.status = 'Expired'

                messages.success(request, 'You have successfully logged in.')

                if request.GET and request.GET.get('next') != '':
                    next = request.GET.get('next')
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('search:all_charts'))
            else:
                login_form.add_error(None, 'Your username or password are incorrect.')
    else:
        login_form = UserLoginForm()

    context = {'login_form': login_form, 'next': request.GET.get('next', '')}
    return render(request, 'accounts/login.html', context)