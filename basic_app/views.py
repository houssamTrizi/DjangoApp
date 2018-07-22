from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def index(request):
    return render(request, "basic_app/index.html")


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse("index"))


def registration(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_info_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = user_info_form.save(commit=False)
            profile.user = user

            profile.profile_pic = request.FILES.get("profile_pic")

            profile.save()

            registered = True
        else:
            print(user_form.errors, user_info_form.errors)
    else:
        user_form = UserForm()
        user_info_form = UserProfileInfoForm()

    context = {
        'registered': registered,
        'user_form': user_form,
        'user_info_form': user_info_form
    }
    return render(request, "basic_app/registration.html", context=context)


def user_login(request):

    if request.method == "POST":
        print(request)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            print("user is authenticated")
            if user.is_active:
                login(request, user)
                print('user is active')
                return HttpResponseRedirect(redirect_to=reverse("index"))

            else:
                return HttpResponse("User account is not active!")
        else:
            print("Someone tried to login and failed!")
            print("The user credentials are username: {}, password: {}".format(username, password))
            return HttpResponse('invalid credentials')

    return render(request, "basic_app/login.html")
