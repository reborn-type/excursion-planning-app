from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Route, Excursion, Group, UserProfile
from .forms import RegisterForm, IDLoginForm, RouteForm, ExcursionForm

def index(request):
    """Главная страница"""
    return render(request, 'main/index.html')


def register_view(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Успешная регистрация! Ваш ID для входа: {user.id}")
            return redirect('main:route_list')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    """Вход по ID или по логину admin"""
    if request.method == 'POST':
        form = IDLoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['login_input'].strip()
            
            if login_input.lower() == 'admin':
                admin_user = User.objects.filter(is_staff=True).first()
                if admin_user:
                    login(request, admin_user)
                    messages.success(request, "Вы вошли как Администратор!")
                    return redirect('main:admin_panel')
                else:
                    messages.error(request, "Аккаунт администратора не найден в базе.")
            
            elif login_input.isdigit():
                user_id = int(login_input)
                user = User.objects.filter(id=user_id).first()
                if user:
                    login(request, user)
                    messages.success(request, f"С возвращением, {user.first_name}!")
                    return redirect('main:route_list')
                else:
                    messages.error(request, f"Пользователь с ID {user_id} не найден.")
            else:
                messages.error(request, "Введите числовой ID или 'admin'.")
    else:
        form = IDLoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('main:index')


def route_list(request):
    """Список маршрутов"""
    routes = Route.objects.all()
    return render(request, 'main/route_list.html', {'routes': routes})

def route_detail(request, pk):
    """Страница маршрута и проверка условий записи на экскурсию"""
    route = get_object_or_404(Route, pk=pk)
    user = request.user
    user_age = getattr(getattr(user, 'profile', None), 'age', None)

    excursions_info = []
    for excursion in route.excursions.all():
        group, _ = Group.objects.get_or_create(excursion=excursion)
        current_participants = group.participants.count()
        
        is_registered = user.is_authenticated and group.participants.filter(id=user.id).exists()
        can_join = False
        reason = ""

        if not user.is_authenticated:
            reason = "Войдите в аккаунт для записи"
        elif user.is_staff:
            reason = "Администратор не записывается на экскурсии"
        elif is_registered:
            reason = "Вы уже записаны"
        elif current_participants >= excursion.max_persons:
            reason = "Мест нет (группа заполнена)"
        elif user_age is not None and (user_age < excursion.min_age or user_age > excursion.max_age):
            reason = f"Не подходите по возрасту (требуется {excursion.min_age}–{excursion.max_age} лет, ваш возраст: {user_age})"
        else:
            can_join = True

        excursions_info.append({
            'excursion': excursion,
            'current_participants': current_participants,
            'can_join': can_join,
            'is_registered': is_registered,
            'reason': reason,
        })

    return render(request, 'main/route_detail.html', {
        'route': route,
        'excursions_info': excursions_info
    })
    

def join_excursion(request, excursion_id):
    """Обработка записи на экскурсию"""
    if not request.user.is_authenticated or request.user.is_staff:
        messages.error(request, "Ошибка доступа.")
        return redirect('main:route_list')

    excursion = get_object_or_404(Excursion, pk=excursion_id)
    group, _ = Group.objects.get_or_create(excursion=excursion)
    user_age = request.user.profile.age

    if group.participants.count() >= excursion.max_persons:
        messages.error(request, "Не удалось записаться: группа заполнена.")
    elif user_age < excursion.min_age or user_age > excursion.max_age:
        messages.error(request, "Не удалось записаться: вы не подходите по возрасту.")
    else:
        group.participants.add(request.user)
        messages.success(request, f"Вы успешно записались на экскурсию «{excursion.title}»!")

    return redirect('main:route_detail', pk=excursion.route.pk)


def admin_panel(request):
    """Панель администратора для создания/редактирования/удаления"""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Доступ разрешен только администраторам!")
        return redirect('main:login')

    routes = Route.objects.all()
    excursions = Excursion.objects.all()
    return render(request, 'main/admin_panel.html', {'routes': routes, 'excursions': excursions})


def route_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('main:login')

    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно создан!')
            return redirect('main:admin_panel')
    else: 
        form = RouteForm()
    return render(request, 'main/route_form.html', {'form': form, 'action': 'Создать'})


def route_update(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff: 
        return redirect('main:login')
    
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно обновлен')
            return redirect('main:admin_panel')
    else:
        form = RouteForm(instance=True)
    return render(request, 'main/route_form.html', {'form': form, 'action': 'Редактировать'})


def route_delete(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('main:login')
    
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        route.delete()
        messages.success(request, 'Маршрут удален!')
        return redirect('main:admin_panel')
    return render(request, 'main/confirm_delete.html', {'object': route, 'name': route.title, 'cancel_url': 'main:admin_panel'})


def excursion_create(request): 
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('main:login')
    
    if request.method == 'POST':
        form = ExcursionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Экскурсия успешно создана!')
            return redirect('main:admin_panel')
    else: 
        form = ExcursionForm()
    return render(request, 'main/excursion_form.html', {'form': form, 'action': 'Создать'})

def excursion_update(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('main:login')
    
    excursion = get_object_or_404(Excursion, pk=pk)
    if request.method == 'POST':
        form = ExcursionForm(request.POST, instance=Excursion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Экскурсия успешно обновлена!')
            return redirect('main:admin_panel')
        else: 
            form = ExcursionForm(instance=excursion)
        return render(request, 'main:execusion_form.html', {'form': form, 'action': 'Редактировать'})
    
    
def excursion_delete(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('main:login')
    
    excursion = get_object_or_404(Excursion, pk=pk)
    if request.method == 'POST':
        excursion.delete()
        messages.success(request, "Экскурсия удалена!")
        return redirect('main:admin_panel')
    return render(request, 'main/confirm_delete.html', {'object': excursion, 'name': excursion.title, 'cancel_url': 'main:admin_panel'})