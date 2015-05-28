from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def messages(request , message_text):
    return render(request, 'my_login/messages/simple_message.html' , { 'message_text' : message_text })

def index(request):
    return render(request, 'my_login/messages/simple_message.html' , { 'message_text' : 'simple index page' })