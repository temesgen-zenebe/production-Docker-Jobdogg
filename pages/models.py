from django.db import models

# Create your models here.
class MyEmptyModel(models.Model):
    pass

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email