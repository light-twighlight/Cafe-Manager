from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

