from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView, DetailView
from survey import models
from django.contrib.auth.mixins import LoginRequiredMixin

# import settings

from .models import Question, Survey, Category
from .forms import ResponseForm


def index(request):
    return render(request, 'survey/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'survey/registration.html',
                  {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    count = 1
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            count += 1
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))

            return render(request, 'survey/login.html', {})
    else:
        return render(request, 'survey/login.html', {})


def survey_detail(request, id ):
    survey = Survey.objects.get(id=id)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    # print("categories for this survey:")
    print(" request.method ", request.method)
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            print(" i m in form save")
            return HttpResponseRedirect("/survey/confirm/%s" % response.interview_uuid)
    else:
        print("i m in else")
        form = ResponseForm(survey=survey)
        # print(form)
        # TODO sort by category
    return render(request, 'survey/survey.html', {'response_form': form, 'survey': survey,
                                                               'categories': categories})


def confirm(request, uuid):
    # email = settings.support_email
    # return render(request, 'confirm.html', {'uuid': uuid, "email":email })
    return render(request, 'survey/confirm.html', {'uuid': uuid})


class EmployeeSurveys(LoginRequiredMixin, ListView):
    context_object_name = 'UsersSurveys'
    model = models.UsersSurveys
    template_name = 'survey/employee_surveys.html'
    #paginate_by = 5

    def get_queryset(self):
        return models.UsersSurveys.objects.filter(user=self.request.user)

