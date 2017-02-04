from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import datetime
import re, bcrypt

name_regex = re.compile(r"^[a-zA-Z\-]+$")
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):

    def loginValidate(self, request):
        try:
            user = User.objects.get(user_name=request.POST['user_name'])
            password = request.POST['password'].encode()
            hashed_pw = user.pw_hash.encode()
            print user
            print password
            print hashed_pw

            if hashed_pw == bcrypt.hashpw(password, hashed_pw):
                return (True, user)

        except ObjectDoesNotExist:
            print("A user by that User Name does not exist.")
            pass

        return (False, ["Incorrect User Name/Email, or the User does not exist."])

    def regValidate(self, request):
        errors = []
        # hire_date = datetime.strptime(request.POST['hire_date'], '%Y-%m-%d')

        # if User.objects.filter(user_name=request.POST['user_name'].strip().lower()):
        if User.objects.filter(user_name=request.POST['user_name']):
            errors.append("A user with that User Name already exists!  Please Log In.")

        if len(request.POST['first_name']) < 3:
            errors.append("The First Name field cannot be blank! It must each have at least 3 characters.")

        elif not name_regex.match(request.POST['first_name']):
            errors.append("You may not include any numbers or special characters in the First Name.")

        if len(request.POST['user_name']) < 3:
            errors.append("The User Name field cannot be blank! It must each have at least 3 characters.")

        if len(request.POST['password']) < 8:
            errors.append('Your Password must contain 8 or more characters!')

        if request.POST['password'] != request.POST['confirm_pw']:
            errors.append('Your Password and Confirm Password must match!')

        if len(request.POST['hire_date']) >= 0:
            try:
                strp_hire_date = datetime.strptime(request.POST['hire_date'], '%Y-%m-%d')
                print "Stripped The Time"
            except:
                # strp_hire_date = datetime.strptime(request.POST['hire_date'], '%Y-%m-%d')
                errors.append('Please enter the valid date you were Hired on.')

        if errors:
            return(False, errors)

        #Create the PW Hash if no errors
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print pw_hash

        #Create New User once the PW is hashed
        # strp_hire_date = datetime.strptime(request.POST['hire_date'], '%Y-%m-%d')
        user = self.create(first_name=request.POST['first_name'], user_name=request.POST['user_name'], pw_hash=pw_hash, hire_date=strp_hire_date)
        print "created a user, at last"
        return (True, user)

class User(models.Model):
    # item = models.ForeignKey(Item)
    first_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    pw_hash = models.CharField(max_length=256)
    hire_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
