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
    path('friendProfile/<str:pk>',views.friendProfile, name='friendProfile'),
    path('friendBlock/<str:pk>',views.friendBlock, name='friendBlock'),
    path('friendDecline/<str:pk>',views.friendDecline, name='friendDecline'),
    path('friendConfirm/<str:pk>',views.friendConfirm, name='friendConfirm'),
    path('friendInvite/<str:pk>',views.friendInvite, name='friendInvite'),
    path('friendUnblock/<str:pk>',views.friendUnblock, name='friendUnblock'),
    path('messagesS/<str:pk>',views.messagesS, name='messagesS'),

    path('allTrainings',views.allTrainings, name='allTrainings'),
    path('allMeals', views.allMeals, name='allMeals'),
]