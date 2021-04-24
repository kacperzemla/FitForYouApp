from django.urls import path
from . import views

urlpatterns = [
    path('',views.main, name='main'),
    path('register',views.register, name="register"),
    path('profile',views.profile, name="profile"),
    path('login',views.loginPage, name="login"),
    path('logout',views.logoutUser, name="logout"),
    path('createTraning/<str:pk>',views.createTraning, name="createTraning"),
    path('deleteTraining/<str:pk>',views.deleteTraining, name='deleteTraining'),
    path('updateTraining/<str:pk>',views.updateTraining, name='updateTraining'),
    path('createExercise',views.createExercise, name='createExercise'),
    path('diet',views.diet,name='diet'),
    path('training',views.training, name='training'),
    path('exercises',views.exercises, name='exercises'),
    path('updateProfile',views.updateProfile, name='updateProfile'),
    path('createMeal/<str:pk>',views.createMeal, name="createMeal"),
    path('deleteMeal/<str:pk>',views.deleteMeal, name='deleteMeal'),
    path('calculator',views.calculator, name='calculator'),
    path('rankings',views.rankings, name='rankings'),
    path('friends',views.friends, name='friends'),
]