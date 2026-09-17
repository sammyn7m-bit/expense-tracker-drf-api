from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
     )
    title = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.ForeignKey( Category, on_delete=models.PROTECT, related_name="expenses")
    description = models.TextField(blank = True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
