from django.shortcuts import render,redirect
from .form import Pets_Register_Form ,Register_Form,Finf_Pet_Form
from .models import Pets,find_Pets,Find_Home
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        # 1. Якщо користувач увійшов (True), request.user — це реальний User.
        # Спокійно фільтруємо його тварин за ID.
        pets = Pets.objects.filter(user=request.user)
    else:
        # 2. Якщо це AnonymousUser (False), ми сюди навіть не ліземо!
        # Замість цього миттєво створюємо порожній список через .none()
        pets = Pets.objects.none()
        
    return render(request, 'main/index.html', {'pets': pets})

def register(request):

    if request.method == "POST":
        form = Register_Form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = Register_Form()

    return render(
        request,
        "main/register.html",
        {"form": form}
    )

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            error = 'ви ввели шось не те'
            return render(request,'main/login.html',{'error':error})


    return render(request,'main/login.html')
@login_required(login_url='login')
def register_pets(request):
    if request.method == 'POST':
        form = Pets_Register_Form(request.POST, request.FILES)

        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()

            return redirect('home')

    else:
        form = Pets_Register_Form()

    return render(request, 'main/register_pets.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect("home")

def find_pets(request):
    # ── КРОК 1: ОБРОБКА ВІДПРАВКИ ФОРМИ (Користувач натиснув "Опублікувати") ──
    if request.method == 'POST':
        # Створюємо форму і наповнюємо її текстом (request.POST) та картинками (request.FILES)
        form = Finf_Pet_Form(request.POST, request.FILES) 
        
        # Перевіряємо, чи користувач заповнив усе правильно
        if form.is_valid():
            lost_pet = form.save(commit=False) # Кажемо: "Підготуй запис, але в базу поки не кидай"
            lost_pet.user = request.user       # Вказуємо, ХТО саме автор цього оголошення
            lost_pet.save()                    # А ось тепер остаточно зберігаємо в базу даних!
            
            return redirect('find_pets')       # Очищаємо сторінку (перенаправляємо самі на себе)

    # ── КРОК 2: ЗВИЧАЙНЕ ВІДКРИТТЯ СТОРІНКИ (Користувач просто зайшов) ──
    else:
        form = Finf_Pet_Form() # Даємо йому просто чисту, порожню форму для заповнення

    # ── КРОК 3: ВИВЕДЕННЯ СПИСКУ ОГОЛОШЕНЬ ──
    # Незалежно від того, чи ми щось зберігали, чи просто зайшли — нам треба показати стрічку оголошень.
    # Беремо ВСІ записи з бази даних і сортуємо їх: від найновіших до найстаріших за допомогою мінуса (-created_at)
    lost_pets_list = find_Pets.objects.all().order_by('-created_at')

    # Віддаємо в HTML-шаблон три речі: сам запит (request), форму (нову або з помилками) та список тварин
    return render(request, 'main/find_pets.html', {
        'form': form,
        'find_pets': lost_pets_list
    })

@login_required(login_url='login')
def ai(request):
    return render(request,'main/AI.html')

def find_home(request):
    pets = Find_Home.objects.all()
    return render(request,'main/find_home.html',{'pets':pets})


