from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def login(request):
    return HttpResponse('Pagina de login')

def registro(request):
    if request.method == 'GET':
        return render(request, 'home/registro.html')
    elif request.method == 'POST':
        username = request.POST['Login']
        password = request.POST['Password']
        return redirect('index')
