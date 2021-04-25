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
from .forms import TrainingForm, CustomerForm, ExerciseForm
from django.forms import inlineformset_factory
from django.forms import inlineformset_factory  # kilka form naraz
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
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
                username=user.username,
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

    some_day_last_week =  timezone.now().date() - timedelta(days=7) #cofamy się tydzien do tylu

    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    # pobieramy dzień tygodnia some_day_last_week.isocalendar()[2] - to nasz dzień tygodnia a chcemy mieć
    # różnicę jaka nas dzieli od poniedziałku czyli -1 i odejmujemy te dni od aktualnego i mamy poniedzialek ostatniego tygodnia

    monday_of_this_week = monday_of_last_week + timedelta(days=7) #teraz dodajemy 7 dni i mamy poniedzialek tego tygodnia :)
    monday_of_next_week = monday_of_this_week+timedelta(days=7)
  #  print(monday_of_this_week)
  #  print(sunday_of_this_week)
    meals_of_last_week = request.user.customer.meal_set.all().filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week).order_by('-date')
    meals_of_this_week = request.user.customer.meal_set.all().filter(date__gte=monday_of_this_week, date__lt=monday_of_next_week).order_by('-date')
    #meals2 = Meal.objects.filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week)
    #gt -> greater than, lt - less than
    print(meals_of_last_week)
    context = {'meals_of_last_week': meals_of_last_week,'meals_of_this_week': meals_of_this_week}
    return render(request, 'Workout\diet.html', context)


@login_required(login_url='main')
def training(request):
    some_day_last_week =  timezone.now().date() - timedelta(days=7)

    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    monday_of_next_week = monday_of_this_week+timedelta(days=7)
  #  print(monday_of_this_week)
  #  print(sunday_of_this_week)
    training_of_last_week = request.user.customer.training_set.all().filter(date__gte=monday_of_last_week, date__lt=monday_of_this_week).order_by('-date')
    training_of_this_week = request.user.customer.training_set.all().filter(date__gte=monday_of_this_week, date__lt=monday_of_next_week).order_by('-date')
    print(training_of_this_week)
    exercises = Exercises.objects.all()

    context = {'exercises': exercises, 'training_of_last_week': training_of_last_week, 'training_of_this_week': training_of_this_week}
    return render(request, 'Workout/training.html', context)


@login_required(login_url='main')
def deleteTraining(request, pk):
    training = Training.objects.get(id=pk)
    if request.method == "POST":
        training.delete()
        return redirect('training')
    context = {'training': training}
    return render(request, 'Workout/deleteTraining.html', context)


def updateTraining(request,pk):
    training = Training.objects.get(id=pk)
    form = TrainingForm(instance = training)

    if request.method == "POST":
        form = TrainingForm(request.POST, instance = training)
        if form.is_valid():
            training.save()
        return redirect('training')

    context ={'form' :form}
    return render(request,'Workout/updateTraining.html',context) 


def createExercise(request):
    exercises = Exercises.objects.all()
    form = ExerciseForm()

    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('exercises')

    context ={'form' :form}
    return render(request,'Workout/createExercise.html',context) 

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
    weight = ''
    goal = ''
    proteins = 0
    fats = 0
    carbs = 0
    kcal = 0
    warning = ''
    if request.method == 'POST':
        try:
            weight = request.POST['weight']
        except:
            warning='Enter your weight!'
        try:
            goal = request.POST['choice']
        except:
            warning = 'Fill in the form'


    if goal == 'normal_intake':
        try:
            kcal = int(weight)*33
        except:
            warning = 'Fill in the form'
    if goal == 'mass':
        try:
            kcal = int(weight)*33+300
        except:
            warning = 'Fill in the form'
    if goal == 'reduction':
        try:
            kcal = int(weight)*33-300
        except:
            warning = 'Fill in the form'

    if goal =='normal_intake' or goal =='mass' or goal == 'reduction':
        try:
            proteins = 2* int(weight)
            fats = round(0.3 *int(kcal)/9)
            carbs =  (kcal - 9*fats - 4*proteins)//4
        except:
            pass

    context = {'kcal': kcal,'proteins': proteins,'fats': fats,'carbs': carbs,'warning': warning}


    return render(request, 'Workout/calculator.html', context)

@login_required(login_url='main')
def exercises(request):
    exercises  = Exercises.objects.all()
    print (exercises)
    chest = []
    legs = []
    abs_ =[]
    shoulders = []
    bic_tric = []
    booty =[]
    cardio =[]
    back = []
    for  cybant in exercises :
        if cybant.category ==  "CHEST":
            chest.append(cybant)
        elif cybant.category ==  "LEGS":
            legs.append(cybant)
        elif cybant.category ==  "ABS":
            abs_.append(cybant)
        elif cybant.category ==  "SHOULDERS":
            shoulders.append(cybant)
        elif cybant.category ==  "BICEPS & TRICEPS":
            bic_tric.append(cybant)
        elif cybant.category ==  "BOOTY":
            booty.append(cybant)
        elif cybant.category ==  "CARDIO":
            cardio.append(cybant)
        elif cybant.category ==  "BACK":
            back.append(cybant)
        
    context = {'chest':chest,'legs':legs,'back':back,'abs_':abs_,'shoulders':shoulders,'bic_tric':bic_tric,'cardio':cardio,'booty':booty}
    return render(request, 'Workout/exercises.html', context)
 

def friends(request):
    context = {}
    return render(request, 'Workout/friends.html',context)

def rankings(request):
    bufor = Training.objects.filter().order_by('-weigth')
    benchPressMasters = {}
    top5 = 0;
    for cybant in bufor:
        if cybant.getExerciseName() == "bench press" and  top5 < 5: 
            if cybant.customer.username in benchPressMasters:
                pass
            else:
                benchPressMasters[cybant.customer.username]=cybant
                top5 += 1
    squatMasters = {}
    top5 = 0;
    for cybant in bufor:
        if cybant.getExerciseName() == "squat" and  top5 < 5: 
            if cybant.customer.username in squatMasters:
                pass
            else:
                squatMasters[cybant.customer.username]=cybant
                top5 += 1
    deadLiftMasters = {}
    top5 = 0;
    for cybant in bufor:
        if cybant.getExerciseName() == "dead lift" and  top5 < 5: 
            if cybant.customer.username in deadLiftMasters:
                pass
            else:
                deadLiftMasters[cybant.customer.username]=cybant
                top5 += 1

    context ={'benchPressMasters' :benchPressMasters.values() , 'squatMasters' :squatMasters.values() , 'deadLiftMasters' :deadLiftMasters.values()}
    return render(request, 'Workout/rankings.html', context)

def allMeals(request):
    meals = request.user.customer.meal_set.all()
    context = {'meals': meals}
    return render(request,'Workout/allMeals.html',context)

def allTrainings(request):
    trainings = request.user.customer.training_set.all()
    print(trainings)
    context = {'trainings':trainings}
    return render(request,'Workout/allTrainings.html',context)