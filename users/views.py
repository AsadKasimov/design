from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, LoginForm
from .models import Product
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from .forms import ProductForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv


# Create your views here.
# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')




def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})






def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Уведомление о успешном добавлении товара
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})



def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})




# Отчет в формате HTML
def user_report(request):
    users = User.objects.all().order_by('-date_joined')  # Все пользователи, сортировка по дате регистрации
    return render(request, 'reports/user_report.html', {'users': users})

# Отчет в формате CSV
def user_report_csv(request):
    # Создание HTTP-ответа с заголовком для загрузки CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_report.csv"'

    # Создание объекта записи в CSV
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Date Joined', 'Is Staff'])

    # Добавление данных пользователей в CSV
    for user in User.objects.all().order_by('-date_joined'):
        writer.writerow([user.username, user.email, user.date_joined, user.is_staff])

    return response
