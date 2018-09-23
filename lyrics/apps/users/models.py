from __future__ import unicode_literals
import re 
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_reg(self, data):
        errors = []
        if len(data['name']) == 0 or len(data['alias']) == 0 or len(data['password']) == 0 or len(data['password_confirm']) == 0 or len(data['email']) == 0:
            errors.append("no blanks fields")
        if len(data['name']) < 2 or len(data['alias']) < 2:
            errors.append("Name fields must be 3 characters or more")
        if len(data['password']) < 8:
            errors.append("password must be 8 or more characters")  
        if not re.match(NAME_REGEX, data['name']) or not re.match(NAME_REGEX, data['alias']):
            errors.append('name fields must be ONLY characters')
        if not re.match(EMAIL_REGEX, data['email']):
            errors.append('please enter valid email')
        #platform suggests filter    
        if len(User.objects.filter(email=data['email'])) > 0:
            errors.append('email in use currently')
        if data['password'] != data['password_confirm']:
            errors.append('Oh nooo.... passwords are not a match.') 
        if not errors:
            hashed = bcrypt.hashpw((data['password'].encode()), bcrypt.gensalt(8))    
            new_user = self.create(
                name = data['name'],
                alias = data['alias'],
                email = data['email'],
                dob = data['dob'],
                password = hashed
            )           
            return new_user
        return errors  
    def validate_log(self, data):
        errors=[]
        if len(self.filter(email=data['email'])) > 0:
            user = self.filter(email=data['email'])[0]
            if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                errors.append('email or password do not match records')
        else:
            errors.append('email or password do not match records')  
        if errors:
            return errors
        return user                    

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #function to retrieve full name
    def __str__(self):
        return self.email    
