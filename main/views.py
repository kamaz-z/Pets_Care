from django.shortcuts import render,redirect
from .form import Pets_Register_Form
def index(request):
    return render(request, 'main/index.html')

def register(request):
    return render(request, 'main/register.html')

def register_pets(request):
    form = Pets_Register_Form

    return render(request,'main/register_pets.html',{"form":form})
