from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    # on_delete= models.CASCADE jezeli usuniemy uzytkownika tego glownego to to powiazanie tez zostanie usuniete
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    number = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    def __str__(self):
        return self.username


class Exercises(models.Model):

    CATEGORY = (
        ('CHEST','CHEST'),
        ('LEGS','LEGS'),
        ('ABS','ABS'),
        ('SHOULDERS','SHOULDERS'),
        ('BICEPS & TRICEPS','BICEPS & TRICEPS'),
        ('BOOTY','BOOTY'),
        ('CARDIO','CARDIO'),
        ('BACK','BACK')
    )

    LEVEL = (
        ('PROFESSIONAL','PROFESSIONAL'),
        ('BEGINNER','BEGINNER'),
        ('INTERMEDIATE' , 'INTERMEDIATE')
    )

    name = models.CharField(max_length=50 , null=True);
    category = models.CharField(max_length=50, null=True , choices=CATEGORY)
    level = models.CharField(max_length=50, null=True , choices=LEVEL)
    def __str__(self):
        return self.name


class Training(models.Model):

    date = models.DateTimeField(auto_now_add=True, null=True)
    exercise = models.ForeignKey(
        Exercises, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    weigth = models.IntegerField(null=True)
    sesion = models.IntegerField(null=True)
    reps = models.IntegerField(null=True)

    def getCustumerId(sef):
        return self.customer.id

    def getExerciseName(self):
        return self.exercise.name

    def getCustumerUsername(self):
        return self.customer.username


class Meal(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, null=True)
    carbs = models.IntegerField(null=True)
    fats = models.IntegerField(null=True)
    proteins = models.IntegerField(null=True)
    kcal = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.name

class Dialogues(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    sender =  models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL , related_name="senderText")
    receiver =  models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL , related_name="receiverText")
    text = models.CharField(max_length=200, null=True)

    @classmethod
    def create(cls, sender,receiver,text):
        newDialogue = cls(sender= sender , receiver= receiver , text=text)
        return newDialogue

class Relations(models.Model):
    STATUS = (
        ('invite' , 'invite'),
        ('friends' , 'friends'),
        ('blocked' , 'blocked'),
        ('declined' , 'declined'),
        ('banned' , 'banned')
    )

    status = models.CharField(max_length=50, null=True , choices=STATUS)
    sender =  models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL , related_name="sender")
    receiver =  models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL , related_name="receiver")

    @classmethod
    def create(cls, status,receiver,sender):
        newRelation = cls(status=status , receiver= receiver , sender= sender)
        return newRelation

    def makeFriendAgain(self):
        self.status = "friends"

    def blockRelations(self):
        self.status = "blocked"

    def banRelations(self):
        self.status = "banned"

    def declineRelations(self):
        self.status = "declined"

    def confirmRelations(self):
        self.status = "friends"