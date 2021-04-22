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
from .forms import TrainingForm, ExerciseForm
from django.forms import inlineformset_factory
# Create your views here.

@unauthenticated_user # w plik decorators.py znajduje się funkcja, która sprawdza czy użytkownik jest zalogowany i blokuje dostęp do podstron przed, którymi dodamy tzw. "decorator" czyli to co jest tutaj
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
                user = user,
                name = 'default',
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
    context = {'name':name,'email':email,'phone':phone}
    return render(request, 'Workout/profile.html', context)


def createTraning(request,pk):
    TrainingFormSet = inlineformset_factory(Customer,Training,fields=('exercise','weigth','sesion','reps','customer'),can_delete = False ,extra = 10)
    customer = Customer.objects.get(id=pk)
    formset = TrainingFormSet(queryset=Training.objects.none(), instance=customer)
    #form = TrainingForm(initial={'user':user})
    if request.method == 'POST':
        #print('Printing post:' ,request.POST)
        formset = TrainingFormSet(request.POST ,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('training')

    context = {'formset':formset}

    return render(request ,'Workout/createTraning.html', context)

def diet(request):
    context = {}
    return render(request, 'Workout\diet.html', context)

@login_required(login_url='main')
def training(request):
    training = request.user.customer.training_set.all()

    #trainingCount = training.count()
   #myTrainingFilter = TrainingFilter(request.GET,queryset=training)
    #training = myTrainingFilter.qs

    context = {'traning':training }
    #, 'myTrainingFilter':myTrainingFilter}


    return render(request, 'Workout/training.html', context)


@login_required(login_url='main')
def exercises(request):
    exercises  = Exercises.objects.all()
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


def deleteTraining(request,pk):
    training = Training.objects.get(id=pk)
    if request.method == "POST":
        training.delete()
        return redirect('training')
    context={'training' :training}
    return render(request,'Workout/deleteTraining.html',context)

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

def updateProfile(request):
    return render(request,'Workout/updateprofile.html')