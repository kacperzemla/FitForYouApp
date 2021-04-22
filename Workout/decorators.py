#tutaj będą decorators ( takie coś co obsługuje autoryzacje i uprawnienia)
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func): #jako argument bierze funkcje widoku z views.py, który znajduje się pod dekoratorem
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated: #sprawdzamy czy użytkownik jest zalogowny jesli tak to przenosimy go do profile a jak nie to wywołujemy view_func czyli po prostu podstrone do ktorej chcielismy sie dostac
            return redirect('profile')
        else:
            return view_func(request, *args, **kwargs)


    return wrapper_func