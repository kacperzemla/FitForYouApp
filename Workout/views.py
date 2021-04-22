from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import templates
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .forms import TrainingForm, CustomerForm
from django.forms import inlineformset_factory
from django.forms import inlineformset_factory  # kilka form naraz
# Create your views here.


@unauthenticated_user  # w plik decorators.py znajduje się funkcja, która sprawdza czy użytkownik jest zalogowany i blokuje dostęp do podstron przed, którymi dodamy tzw. "decorator" czyli to co jest tutaj
def main(request):
    return render(request, 'Workout/main.html')


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user,
                name='default',
            )
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}

    return render(request, 'Workout/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'Workout/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


# ta linijka zabezpiecza nam view przed wejściem jeśli nie jesteśmy zalogowani :), trzeba to dać przed każdą stroną, która ma być dostepna tylko dla użytkownika
@login_required(login_url='main')
def profile(request):
    name = request.user.customer.name
    email = request.user.customer.email
    phone = request.user.customer.number
    height = request.user.customer.height
    weight = request.user.customer.weight
    context = {'name': name, 'email': email,
               'phone': phone, 'height': height, 'weight': weight}
    return render(request, 'Workout/profile.html', context)


def createTraning(request, pk):
    TrainingFormSet = inlineformset_factory(Customer, Training, fields=(
        'exercise', 'weigth', 'sesion', 'reps', 'customer'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = TrainingFormSet(
        queryset=Training.objects.none(), instance=customer)
    #form = TrainingForm(initial={'user':user})
    if request.method == 'POST':
        #print('Printing post:' ,request.POST)
        formset = TrainingFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('training')

    context = {'formset': formset}

    return render(request, 'Workout/createTraning.html', context)


@login_required(login_url='main')
def diet(request):
    meals = request.user.customer.meal_set.all()
    context = {'meals': meals}
    return render(request, 'Workout\diet.html', context)


@login_required(login_url='main')
def training(request):
    exercises = Exercises.objects.all()
    traning = request.user.customer.training_set.all()
    context = {'exercises': exercises, 'traning': traning}
    return render(request, 'Workout/training.html', context)


@login_required(login_url='main')
def deleteTraining(request, pk):
    training = Training.objects.get(id=pk)
    if request.method == "POST":
        training.delete()
        return redirect('training')
    context = {'training': training}
    return render(request, 'Workout/deleteTraining.html', context)


@login_required(login_url='main')
def updateTraining(request, pk):
    training = Training.objects.get(id=pk)
    form = TrainingFormg(instance=training)
    context = {'form': form}
    return render(request, 'Workout/updateTraining.html', context)


@login_required(login_url='main')
def updateProfile(request):
    customer = request.user.customer
    # do naszego formularza przypisujemy aktualnie zalogowanego uzytkownika
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'Workout/updateprofile.html', context)


@login_required(login_url='main')
def createMeal(request, pk):
    MealFormSet = inlineformset_factory(Customer, Meal, fields=(
        'name', 'date', 'carbs', 'proteins', 'fats', 'kcal'), can_delete=False)
    customer = Customer.objects.get(id=pk)
    # ten queryset zapewnia ze w formularzu pojawią się pola tylko na nowe posilki a nie na te ktore juz sa
    formset = MealFormSet(queryset=Meal.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = MealFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('diet')
    context = {'formset': formset}
    return render(request, 'Workout/createMeal.html', context)


@login_required(login_url='main')
def deleteMeal(request, pk):
    meal = Meal.objects.get(id=pk)
    if request.method == "POST":
        meal.delete()
        return redirect('diet')

    context = {"meal": meal}
    return render(request, 'Workout/deleteMeal.html', context)


@login_required(login_url='main')
def calculator(request):
    text = ''
    text2 = ''
    if request.method == 'POST':
        try:
            text = request.POST['weight']
        except:
            text='Enter your weight!'
        try:
            text2 = request.POST['choice']
        except:
            text = 'Invalid data provided!'

    if text2 == 'normal_intake':
        try:
            text = int(text)*33
        except:
            text = 'Invalid data provided!'
    elif text2 == 'mass':
        try:
            text = int(text)*35
        except:
            text = 'Invalid data provided!'
    else:
        try:
            text = int(text)*31
        except:
            text = 'Invalid data provided!'

    context = {'text': text}
    print(text)
    print(text2)

    return render(request, 'Workout/calculator.html', context)
