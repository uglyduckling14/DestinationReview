from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import models

class User(models.Model):
    def checkValidPassword(self):
        if self.password_hash.isalpha() or len(self.password_hash) <8:
            raise ValidationError("Password is not secure")
    
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique= True, validators=[EmailValidator(message="Email is invalid")])
    password_hash = models.CharField(max_length=50, validators=[checkValidPassword])        

    def checkValidEmail(self):
        if not "@" in self.email:
            raise ValidationError(message="Email is invalid!")
class Session(models.Model):
    token = models.CharField(max_length=300, unique= True, default = 1)
    user = models.OneToOneField(User, on_delete= models.CASCADE, null= True)

class Destination(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    review = models.TextField(max_length=300)
    rating = models.BigIntegerField()
    share_publicly = models.BooleanField(default=False, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, related_name="destination_set")