from django.shortcuts import render,redirect
from .form import Pets_Register_Form
from .models import Pets
def index(request):
    pets = Pets.objects.all()
    return render(request, 'main/index.html',{'pets':pets})

def register(request):
    return render(request, 'main/register.html')

def register_pets(request):
    if request.method == 'POST':
        # Передаємо і дані, і файли
        form = Pets_Register_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = Pets_Register_Form()
    return render(request, 'main/register_pets.html', {'form': form})
