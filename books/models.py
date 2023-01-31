from django.db import models

class Book(models.Model):
    isbn = models.CharField(max_length=250, blank=True)
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=250, blank=True)
    year = models.PositiveIntegerField()

    def __format__(self):
        return self.title