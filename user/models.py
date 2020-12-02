from django.db import models

class User(models.Model):
    nickname     = models.CharField(max_length= 45)
    phone_number = models.CharField(max_length= 11)
    password     = models.CharField(max_length= 200)
    email        = models.EmailField()
    image_url    = models.URLField(max_length= 200)
    created_at   = models.DateTimeField(auto_now_add= True)
    updated_at   = models.DateTimeField(auto_now= True)

    class Meta :
        db_table = 'users'

class UserBook(models.Model):



